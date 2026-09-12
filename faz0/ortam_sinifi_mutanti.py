#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ORTAM SINIFI MUTANTI (besli-paket/IS_EMRI_B4.md, B4-3 + B4-4 + grep tuzagi).

NEDEN VAR
  `faz0/ortam_olcum.sh` (root + mount + useradd gerektirir) UC bulguyu olcer ama
  KENDI KODA DOKUNMAZ — yalniz olcer. Bu dosya tam tersidir: KOR KAPI PROTOKOLU
  (her bulguya AYRI mutant + pozitif kontrol) ile `hafiza.py`nin KENDI duzeltmesini
  sinar. Kosum icin root/useradd/mount GEREKMEZ — KAPI-B'nin POSIX dizin-izni
  kolu haric, hepsi normal kullanici ile kosar (KAPI-B-IZOLASYON fault-injection
  ile root/izin gerektirmeden AYNI son-ag dalini platformdan BAGIMSIZ sinar).

NE OLCER — DORT KAPI
  KAPI-A (B4-3)    : salt-okunur canli + bekleyen fragman -> `derle` sonrasi
                     defterlerde "canliya eklendi" beyani OLMAMALI; izin
                     duzeltilip yeniden derlenince `kapi` YESIL (KALICI kirmizi
                     KALMAMALI).
  KAPI-B GERCEK    : `arsiv/hafiza` 555 iken `muhur` -> "ARAC KUSURUDUR" ibaresi
                     YOK, ham PermissionError YOK, "DIZIN YAZILAMAZ" TEMIZ
                     teshisi VAR, cikis kodu 3. POSIX + root-OLMAYAN kullanici
                     gerektirir; kosulamiyorsa OLCULEMEDI (fazB_senaryolari
                     kalibi — "temiz" DENMEZ).
  KAPI-B IZOLASYON : `kilit_al` fault-injection ile PermissionError(EACCES)
                     ATAR (gercek dosya izni YOK, platformdan BAGIMSIZ); son
                     agin EACCES/EPERM/EROFS dali TEMIZ teshis vermeli, cikis 3.
                     KAPI-B GERCEK'in olculemedigi platformlarda (Windows) bile
                     son ag dalini dogrudan sinar.
  KAPI-C (pozitif) : izinli normal ortamda `not`+`derle`+`kapi` -> `derle`
                     exit 0, fragman islenir, kapi YESIL. Duzeltmenin normal
                     yolu BOZMADIGININ kanitidir.
  KAPI-D (grep)    : `ortam_olcum.sh`'nin B4-4 siniflandirma deseni, DOGRU
                     mesajlari ("... ARAC KUSURU DEGIL") yanlis saymamali;
                     YALNIZ gercek yanlis-teshis metnini ("ARAC KUSURUDUR")
                     yakalamali.

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. B4-1 (ENOSPC/tmpfs) bu dosyanin kapsami DISINDA — `ortam_olcum.sh`
     KAPANMIS diyor, bu turun KALEM'leri B4-3/B4-4/grep'tir.
  2. KAPI-B GERCEK, root olarak kosulursa ya da Windows'ta kosulursa OLCULEMEDI
     yazar — "temiz" DENMEZ (ROOT NOTU: root icin os.access 0444'te de True
     doner; Windows dizin izni POSIX anlaminda zorlanamaz).
  3. Performans / hiz bu dosyanin ekseni degil.

CIKIS KODLARI
  0  dort kapi de (olculebilen kapsamda) temiz VE her UYGULANABILIR mutant ISIRDI
  1  bir kapi KIRMIZI ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor/betik okunamadi, kurulum basarisiz, POSIX-ozel kol bu
     platformda/kullanicida kosulamadi) — ve kirmizi/kacan YOK
"""
import io
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI (olcum aracina da konur)
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")
VARSAYILAN_BETIK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "ortam_olcum.sh")


class Kurulamadi(Exception):
    """Test KURULUMU basarisiz (bozuk proje, git yok vb.) — KAPI HUKMU DEGILDIR."""


def _posix_non_root():
    """KAPI-B GERCEK icin zemin: POSIX + root OLMAYAN kullanici.

    ROOT NOTU (hafiza.py `_yazma_on_kontrol` ile AYNI): root icin os.access
    0444/0555'te de True doner (POSIX). Bu dal ancak root OLMAYAN kullanicida
    olculebilir."""
    if sys.platform == "win32":
        return False
    try:
        return os.geteuid() != 0
    except AttributeError:
        return False


def kos(motor, *argv, kok=None):
    """`_komut`/`_kapi_kos` ile AYNI cagrı kalibi (hafiza.py): -X utf8 +
    PYTHONIOENCODING=utf-8 — Windows'ta cp1254 cocugu bozmasin."""
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _proje_kur(taban, ad, motor):
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    k, c = kos(motor, "kur", kok=kok)
    if k != 0:
        raise Kurulamadi("kur basarisiz (exit %d): %s" % (k, c[:200]))
    return kok


_HAM_IZLER = ("Traceback (most recent", "PermissionError", "OSError:")


def _ham_iz_var_mi(c):
    return [x for x in _HAM_IZLER if x in c]


# ============================================================ KAPI-A (B4-3)

_KAPI_A_FI_SNIPPET = """
import sys, os, importlib.util
spec = importlib.util.spec_from_file_location("hafiza_izole_a", %(motor)r)
hafiza = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hafiza)

_canli_yolu = os.path.realpath(%(canli)r)
_gercek_yaz = hafiza.yaz
def _sahte_yaz(p, s):
    if os.path.realpath(p) == _canli_yolu:
        raise OSError(13, "Permission denied (injected)", p)
    return _gercek_yaz(p, s)
hafiza.yaz = _sahte_yaz

sys.argv = ["hafiza.py", "derle", "--kok=" + %(kok)r]
try:
    hafiza._guvenli_calistir()
except SystemExit as e:
    sys.stderr.write("FI_EXIT=%%s\\n" %% e.code)
"""

_KAPI_A_DEFTERLER = ["_YENI_SATIRLAR.txt", "_KOVA.json", "_TASINMA.jsonl", "_DUZELTMELER.json"]


def kapi_a(motor, taban):
    """`yaz(y.canli, ...)` BASARISIZ OLURSA (nedeni ONEMSIZ), hicbir arsiv/beyan
    yazisi GERCEKLESMEMIS OLMALI (KALEM 1'in erteleme sirasi). Gercek dosya
    izni YERINE `hafiza.yaz` uzerinde fault-injection kullanilir: boylece
    KALEM 1'in AYRI "ucuz ek guvence" on-kontrolu (canli BASTAN salt-okunursa
    erken/temiz durur) bu testi GOLGELEMEZ — asil sinanan, kontrolden SONRA
    baska bir nedenle basarisiz olan bir `yaz()` cagrisinin ERTELEME SIRASINI
    bozup bozmadigidir."""
    kok = _proje_kur(taban, "kapi_a", motor)
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=ilk not metni", kok=kok)
    if k != 0:
        raise Kurulamadi("ilk not yazilamadi (exit %d): %s" % (k, c[:200]))
    k, c = kos(motor, "derle", kok=kok)
    if k != 0:
        raise Kurulamadi("ilk derle basarisiz (exit %d): %s" % (k, c[:200]))
    # AYNI konu tekrar: ikinci derle'de `eski` blogu BULUNUR -> `_arsive_tasi`
    # tetiklenir (M-A'nin hedef aldigi TAM kod yolu).
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=ikinci not metni", kok=kok)
    if k != 0:
        raise Kurulamadi("ikinci not yazilamadi (exit %d): %s" % (k, c[:200]))

    canli = os.path.join(kok, "PROJE_HAFIZA.md")
    h = os.path.join(kok, "arsiv", "hafiza")
    onceki = {}
    for d in _KAPI_A_DEFTERLER:
        p = os.path.join(h, d)
        onceki[d] = io.open(p, "rb").read() if os.path.isfile(p) else None
    canli_onceki = io.open(canli, "rb").read()

    kod = _KAPI_A_FI_SNIPPET % {"motor": motor, "canli": canli, "kok": kok}
    r = subprocess.run([sys.executable, "-X", "utf8", "-c", kod],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    c = (r.stdout or "") + (r.stderr or "")
    if not re.search(r"FI_EXIT=(-?\d+)", c):
        raise Kurulamadi("fault-injection kurulumu cokmus/exit kodu basilmadi: %s" % c[:300])

    bulgular = []
    if "ARAC KUSURUDUR" in c:
        bulgular.append("derle (yaz basarisiz OLUNCA) 'ARAC KUSURUDUR' yanlis teshisi verdi")
    canli_sonra = io.open(canli, "rb").read()
    if canli_sonra != canli_onceki:
        bulgular.append("canli dosya DEGISTI — 'yaz basarisiz oldu' senaryosunda BEKLENMEYEN "
                         "bir sekilde icerik degismis (fault-injection sizdirdi)")
    for d in _KAPI_A_DEFTERLER:
        p = os.path.join(h, d)
        simdiki = io.open(p, "rb").read() if os.path.isfile(p) else None
        if simdiki != onceki[d]:
            bulgular.append("yaz(y.canli) BASARISIZ OLDUGU halde '%s' defteri DEGISTI — "
                             "arsiv/beyan yazisi erteleme SIRASINDAN ONCE calismis "
                             "(B4-3 sinifi)" % d)
    return bulgular


# ============================================================ KAPI-B (B4-4)

def kapi_b_gercek(motor, taban):
    """GERCEK senaryo: `arsiv/hafiza` 555 iken `muhur`. POSIX + root-olmayan
    kullanici gerektirir; saglanamiyorsa None (OLCULEMEDI, 'temiz' DENMEZ)."""
    if not _posix_non_root():
        return None
    kok = _proje_kur(taban, "kapi_b_gercek", motor)
    hedef = os.path.join(kok, "arsiv", "hafiza")
    eski_mod = stat.S_IMODE(os.stat(hedef).st_mode)
    os.chmod(hedef, 0o555)
    try:
        k, c = kos(motor, "muhur", "izin denemesi gerekcesi uzun aciklama metni", kok=kok)
    finally:
        os.chmod(hedef, eski_mod)
    bulgular = []
    if "ARAC KUSURUDUR" in c:
        bulgular.append("YANLIS TESHIS: cikti 'ARAC KUSURUDUR' tasiyor (son ag/genel "
                         "catch-all'a dusmus)")
    iz = _ham_iz_var_mi(c)
    if iz:
        bulgular.append("HAM IZ/ISTISNA goruldu: %s :: %s" % (iz, c[:200]))
    if "DIZIN YAZILAMAZ" not in c:
        bulgular.append("TEMIZ 'DIZIN YAZILAMAZ' teshisi YOK (kilit_al on-kontrolu devrede "
                         "degil gibi gorunuyor): %s" % c[:300])
    if k != 3:
        bulgular.append("cikis kodu %d (beklenen 3)" % k)
    return bulgular


_IZOLASYON_SNIPPET = """
import sys, importlib.util
spec = importlib.util.spec_from_file_location("hafiza_izole", %(motor)r)
hafiza = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hafiza)

def _patlat(y):
    raise PermissionError(13, "Permission denied", %(yol)r)
hafiza.kilit_al = _patlat

sys.argv = ["hafiza.py", "muhur", "--kok=" + %(kok)r, "izolasyon mutant denemesi gerekcesi"]
try:
    hafiza._guvenli_calistir()
except SystemExit as e:
    sys.stderr.write("IZOLASYON_EXIT=%%s\\n" %% e.code)
"""


def kapi_b_izolasyon(motor, taban):
    """`kilit_al` fault-injection ile PermissionError(EACCES) ATAR — gercek
    dosya izni GEREKMEZ, platformdan BAGIMSIZ. Son agin EACCES/EPERM/EROFS
    dalini TEK BASINA, kilit_al on-kontrolunden BAGIMSIZ sinar."""
    kok = _proje_kur(taban, "kapi_b_izole", motor)
    yol = os.path.join(kok, "arsiv", "hafiza", ".kilit")
    kod = _IZOLASYON_SNIPPET % {"motor": motor, "yol": yol, "kok": kok}
    r = subprocess.run([sys.executable, "-X", "utf8", "-c", kod],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    c = (r.stdout or "") + (r.stderr or "")
    bulgular = []
    m = re.search(r"IZOLASYON_EXIT=(-?\d+)", c)
    if not m:
        raise Kurulamadi("izolasyon kurulumu cokmus/exit kodu basilmadi: %s" % c[:300])
    kod_ = int(m.group(1))
    if "ARAC KUSURUDUR" in c:
        bulgular.append("YANLIS TESHIS: izole senaryoda 'ARAC KUSURUDUR' basildi")
    iz = [x for x in _HAM_IZLER if x in c and x != "PermissionError"]
    # NOT: "PermissionError" kelimesi BURADA beklenir (biz atiyoruz); ham iz
    # arama listesi bu fonksiyonda o kelimeyi HARIC tutar, Traceback/OSError kalir.
    if iz:
        bulgular.append("HAM IZ goruldu: %s :: %s" % (iz, c[:200]))
    if kod_ != 3:
        bulgular.append("izole senaryoda cikis kodu %d (beklenen 3)" % kod_)
    return bulgular


def kapi_b(motor, taban_gercek, taban_izole):
    """KAPI-B'nin IKI kolu: en az biri (mumkunse ikisi de) olculur. `gercek`
    OLCULEMEDI olsa bile `izolasyon` HER platformda olculur — son ag dali
    hic bir zaman TAMAMEN karanlikta kalmaz."""
    bg = kapi_b_gercek(motor, taban_gercek)
    bi = kapi_b_izolasyon(motor, taban_izole)
    return bg, bi


# ============================================================ KAPI-C (pozitif)

def kapi_c(motor, taban):
    """Izinli normal ortamda not+derle+kapi normal yolu BOZULMAMALI."""
    kok = _proje_kur(taban, "kapi_c", motor)
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=pozitif kontrol notu", kok=kok)
    if k != 0:
        raise Kurulamadi("not basarisiz (exit %d): %s" % (k, c[:200]))
    gunluk = os.path.join(kok, "gunluk")
    if not [f for f in os.listdir(gunluk) if f.endswith(".md")]:
        raise Kurulamadi("not fragman uretmedi")
    k, c = kos(motor, "derle", kok=kok)
    bulgular = []
    if k != 0:
        bulgular.append("derle BASARISIZ oldu (exit %d), normal yol BOZULDU: %s" % (k, c[:300]))
        return bulgular
    kalan = [f for f in os.listdir(gunluk) if f.endswith(".md")]
    if kalan:
        bulgular.append("derle SONRASI gunluk/ altinda islenmemis fragman KALDI: %s" % kalan)
    canli = io.open(os.path.join(kok, "PROJE_HAFIZA.md"), encoding="utf-8").read()
    if "pozitif kontrol notu" not in canli:
        bulgular.append("derle icerigi CANLIYA YAZMADI (fragman islenmedi)")
    k, c = kos(motor, "kapi", kok=kok)
    if k != 0:
        bulgular.append("kapi KIRMIZI (normal yoldan SONRA): %s" % c[:300])
    return bulgular


# ============================================================ KAPI-D (grep tuzagi)

_ORNEK_METINLER = {
    # Motorun SON AGININ (duzeltme ONCESI hali / genel catch-all) ciktisi —
    # YAKALANMALI (bu GERCEK yanlis-teshistir).
    "yanlis_son_ag": (
        "HATA: BEKLENMEYEN DURUM — bu bir ARAC KUSURUDUR, senin dosyalarinin hukmu degil.\n"
        "  PermissionError: [Errno 13] Permission denied: '.../.kilit'\n"
        "  DIKKAT: islem YARIDA kesildi. Dosyalarin DEGISMIS OLABILIR."),
    # `_yazma_on_kontrol` (DOSYA kolu) — YAKALANMAMALI (DOGRU teshis).
    "dogru_dosya": (
        "HATA: DOSYA SALT-OKUNUR, YAZILAMAZ: x\n"
        "  Izin: 0o444. Bu bir ARAC KUSURU DEGIL, dosya sisteminin hukmudur;\n"
        "  arac hicbir seye DOKUNMADI (dosyan oldugu gibi duruyor)."),
    # `_yazma_on_kontrol` (DIZIN kolu, `kilit_al`in kullandigi AYNI yol) —
    # YAKALANMAMALI (DOGRU teshis; B4-4'un asil duzeltme hedefi).
    "dogru_dizin": (
        "HATA: DIZIN YAZILAMAZ: x\n"
        "  Atomik yazim ayni dizinde gecici bir dosya kurar; bu dizin yazmaya kapali.\n"
        "  Bu bir ARAC KUSURU DEGIL."),
    # Son agin YENI EACCES/EPERM/EROFS dali (KALEM 2) — YAKALANMAMALI.
    "dogru_sonag_izin": (
        "HATA: IZIN/DOSYA SISTEMI HATASI — islem tamamlanamadi.\n"
        "  Yol: x\n"
        "  Bu bir ARAC kusuru degil; dosya sisteminin hukmudur."),
}


def _grep_desenini_oku(sh_metni):
    m = re.search(r'grep -q "([^"]+)"; then t="ARAC-KUSURU\(yanlis\)"', sh_metni)
    return m.group(1) if m else None


def kapi_d(sh_metni):
    desen = _grep_desenini_oku(sh_metni)
    if desen is None:
        raise Kurulamadi("B4-4 siniflandirma deseni ortam_olcum.sh icinde BULUNAMADI")
    bulgular = []
    for ad, metin in _ORNEK_METINLER.items():
        eslesti = desen in metin
        beklenen = (ad == "yanlis_son_ag")
        if eslesti != beklenen:
            bulgular.append(
                "desen %r, '%s' metnini %s (beklenen: %s)"
                % (desen, ad, "YAKALADI" if eslesti else "YAKALAMADI",
                   "YAKALAMALI" if beklenen else "YAKALAMAMALI"))
    return bulgular


# ================================================================ MUTANTLAR

def _degistir(s, eski, yeni, etiket):
    n = s.count(eski)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [%s]: %r\n"
                         % (n, etiket, eski[:70]))
        return None
    return s.replace(eski, yeni, 1)


# ---- M-A: erteleme sirasi GERI ALINIR (KAPI-A'yi isirmali) ----------------

_MA_ADIM1_ESKI = (
    "            ertele.append((_arsive_tasi, (L[eski[0]:eski[1] + 1],\n"
    "                          \"konu '%s' guncellendi — onceki blok emekli "
    "(log-compaction)\" % konu)))\n"
)
_MA_ADIM1_YENI = (
    "            _arsive_tasi(y, L[eski[0]:eski[1] + 1],\n"
    "                         \"konu '%s' guncellendi — onceki blok emekli "
    "(log-compaction)\" % konu)\n"
)
_MA_ADIM2_ESKI = (
    "    if eklenen_satirlar:\n"
    "        # KALEM 1: ERTELENIR (bkz. yukarisi).\n"
    "        ertele.append((_canli_ekle_beyan, (eklenen_satirlar,\n"
    "                      \"derleme: canliya eklenen bloklar (baseline-sonrasi "
    "kapsam)\")))\n"
)
_MA_ADIM2_YENI = (
    "    if eklenen_satirlar:\n"
    "        _canli_ekle_beyan(y, eklenen_satirlar,\n"
    "                          \"derleme: canliya eklenen bloklar (baseline-sonrasi "
    "kapsam)\")\n"
)
_MA_ADIM3_ESKI = (
    "                        # KALEM 1: ERTELENIR (bkz. yukarisi).\n"
    "                        ertele.append((_beyan_duzeltme, (si, norm(ss), norm(yeni_s),\n"
    "                                      \"derleme: son guncelleme damgasi (yapisal, "
    "her turda zorunlu)\")))\n"
)
_MA_ADIM3_YENI = (
    "                        _beyan_duzeltme(y, si, norm(ss), norm(yeni_s),\n"
    "                                        \"derleme: son guncelleme damgasi (yapisal, "
    "her turda zorunlu)\")\n"
)


def m_a_sira_geri_alinir(s):
    """KALEM 1'in TERSI: beyan/arsiv cagrilari `yaz(y.canli)`dan ONCE, DOGRUDAN
    calisir — B4-3'un TA KENDISI (canli yazimi yarida kesilirse defterler
    GERCEKLESMEMIS bir islemi anlatir)."""
    s = _degistir(s, _MA_ADIM1_ESKI, _MA_ADIM1_YENI, "M-A/adim1-arsive_tasi")
    if s is None:
        return None
    s = _degistir(s, _MA_ADIM2_ESKI, _MA_ADIM2_YENI, "M-A/adim2-canli_ekle_beyan")
    if s is None:
        return None
    s = _degistir(s, _MA_ADIM3_ESKI, _MA_ADIM3_YENI, "M-A/adim3-beyan_duzeltme")
    return s


# ---- M-B-kilit: kilit_al on-kontrolu SOKULUR -------------------------------

_MB_KILIT_ESKI = "    _yazma_on_kontrol(p, kod=3)\n"
_MB_KILIT_YENI = "    pass  # MUTANT: kilit_al on-kontrolu SOKULDU\n"


def m_b_kilit_sokulur(s):
    """KALEM 2 "Ek (kok)" SOKULUR: `.kilit` acilisi yine on-kontrolsuz, ham
    PermissionError son aga (hala oradaysa) ya da genel catch-all'a duser."""
    return _degistir(s, _MB_KILIT_ESKI, _MB_KILIT_YENI, "M-B-kilit")


# ---- M-B-sonag: son agin EACCES/EPERM/EROFS dali SOKULUR -------------------

_MB_SONAG_ESKI = (
    "        # KALEM 2 (besli-paket/IS_EMRI_B4.md, B4-4, Onur kilidi 9 Eyl 2026\n"
    "        # \"Son agda izin sinifi dali\"): ENOSPC'nin YANINA izin/dosya-sistemi\n"
    "        # sinifi (EACCES/EPERM/EROFS) -- olculdu: bu sinif buraya hic dalsiz\n"
    "        # dusuyor, asagidaki genel \"BEKLENMEYEN DURUM — ARAC KUSURUDUR\" metni ile\n"
    "        # ham PermissionError'i kullaniciya gosteriyordu. Dogru dil motorda ZATEN\n"
    "        # VAR (_yazma_on_kontrol: \"Bu bir ARAC KUSURU DEGIL, dosya sisteminin\n"
    "        # hukmudur\") -- o dil buraya TASINIR. `_yazma_on_kontrol`/`kilit_al`\n"
    "        # on-kontrolleri BU sinifi cogunlukla ONCEDEN yakalar; buraya dusen,\n"
    "        # o on-kontrollerin KAPSAMADIGI bir yoldur (son savunma).\n"
    "        if isinstance(_hata, OSError) and getattr(_hata, \"errno\", None) in (\n"
    "                _errno.EACCES, _errno.EPERM, _errno.EROFS):\n"
    "            try:\n"
    "                _yol = getattr(_hata, \"filename\", None) or \"?\"\n"
    "                sys.stderr.write(\n"
    "                    \"HATA: IZIN/DOSYA SISTEMI HATASI — islem tamamlanamadi.\\n\"\n"
    "                    \"  Yol: %s\\n\"\n"
    "                    \"  Bu bir ARAC kusuru degil; dosya sisteminin hukmudur.\\n\"\n"
    "                    \"  DIKKAT: yazma YARIDA kalmis olabilir; bu mesaj hicbir sey \"\n"
    "                    \"vaat ETMEZ.\\n\"\n"
    "                    \"  CIKIS YOLU:  chmod u+w %s        (Windows:  attrib -r %s)\\n\"\n"
    "                    \"  Once durumu OLC: python hafiza.py kapi\\n\"\n"
    "                    % (_yol, _yol, _yol))\n"
    "            except BaseException:\n"
    "                pass\n"
    "            sys.exit(3)\n"
)
_MB_SONAG_YENI = "        # MUTANT: son agin EACCES/EPERM/EROFS dali SOKULDU\n"


def m_b_sonag_sokulur(s):
    """Son agin YENI dali SOKULUR — EACCES/EPERM/EROFS tekrar dalsiz, genel
    catch-all'a (ARAC KUSURUDUR + ham iz) duser."""
    return _degistir(s, _MB_SONAG_ESKI, _MB_SONAG_YENI, "M-B-sonag")


def m_b_ikisi_de_sokulur(s):
    """KALEM 2'nin TAMAMI geri alinir — olculen GERCEK B4-4 bulgusunun
    TA KENDISI (en gercekci/tam mutant)."""
    s = m_b_kilit_sokulur(s)
    if s is None:
        return None
    return m_b_sonag_sokulur(s)


# ---- M-C: erteleme dali 'hic yazma'ya cevrilir -----------------------------

_MC_ESKI = (
    "    for _fn, _args in ertele:\n"
    "        _fn(y, *_args)\n"
)
_MC_YENI = "    pass  # MUTANT: erteleme HIC UYGULANMIYOR\n"


def m_c_erteleme_hic_yazmaya_cevrilir(s):
    """Duzeltme NORMAL yolu bozmamali: erteleme listesi HIC uygulanmazsa
    (kayitlar toplanir ama hiçbiri diske yazilmaz) basarili `derle` SONRASI
    bile beyan defterleri guncellenmez -> kapi KIRMIZI olmali (KAPI-C isirir)."""
    return _degistir(s, _MC_ESKI, _MC_YENI, "M-C")


MUTANTLAR_HAFIZA = [
    ("M-A  erteleme sirasi geri alinir", m_a_sira_geri_alinir, "KAPI-A"),
    ("M-B-kilit  kilit_al on-kontrolu sokulur", m_b_kilit_sokulur, "KAPI-B"),
    ("M-B-sonag  son ag EACCES/EPERM/EROFS dali sokulur", m_b_sonag_sokulur, "KAPI-B"),
    ("M-B-ikisi  KALEM 2'nin tamami geri alinir", m_b_ikisi_de_sokulur, "KAPI-B"),
    ("M-C  erteleme dali 'hic yazma'ya cevrilir", m_c_erteleme_hic_yazmaya_cevrilir, "KAPI-C"),
]


# ---- M-D: ortam_olcum.sh deseni ESKI HALINE dondurulur ---------------------

def m_d_desen_eskiye_donduru(s):
    return _degistir(s, 'grep -q "ARAC KUSURUDUR"', 'grep -q "ARAC KUSURU"', "M-D")


# ===================================================================== main

def _rapor_kapi(ad, bulgular_fn, *args):
    """Bir KAPI fonksiyonunu kosar, (KIRMIZI mi, OLCULEMEDI mi, mesajlar) doner."""
    try:
        sonuc = bulgular_fn(*args)
    except Kurulamadi as e:
        return None, True, [str(e)]
    if sonuc is None:       # kapi_b_gercek: platform/kullanici uygun degil
        return None, True, []
    return bool(sonuc), False, sonuc


def _kapi_a_calistir(motor):
    taban = tempfile.mkdtemp(prefix="ortamsinif_a_")
    try:
        return kapi_a(motor, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)


def _kapi_b_calistir(motor):
    taban_g = tempfile.mkdtemp(prefix="ortamsinif_bg_")
    taban_i = tempfile.mkdtemp(prefix="ortamsinif_bi_")
    try:
        bg = kapi_b_gercek(motor, taban_g)
        bi = kapi_b_izolasyon(motor, taban_i)
    finally:
        shutil.rmtree(taban_g, ignore_errors=True)
        shutil.rmtree(taban_i, ignore_errors=True)
    # bg None ise (OLCULEMEDI) yalniz bi'ye bakilir; ikisi de bossa temiz.
    birlesik = list(bi) + (list(bg) if bg else [])
    return birlesik if (bg or bi) else [], (bg is None)


def _kapi_c_calistir(motor):
    taban = tempfile.mkdtemp(prefix="ortamsinif_c_")
    try:
        return kapi_c(motor, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN_MOTOR)
    sh_yolu = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(VARSAYILAN_BETIK)
    print("=== ORTAM SINIFI MUTANTI === motor: %s" % motor)
    print("    betik: %s · platform: %s" % (sh_yolu, sys.platform))

    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    try:
        sh_metni = io.open(sh_yolu, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — betik okunamadi: %s" % e)
        return 2

    olculemeyen = 0
    kirmizi = 0

    # -------------------------------------------------- KAPI-A
    try:
        b_a = _kapi_a_calistir(motor)
        print("  KAPI-A  (B4-3)          : %s" % ("KIRMIZI" if b_a else "YESIL"))
        for b in b_a:
            print("      - %s" % b)
        if b_a:
            kirmizi += 1
    except Kurulamadi as e:
        print("  KAPI-A  (B4-3)          : OLCULEMEDI — %s" % e)
        olculemeyen += 1
        b_a = None

    # -------------------------------------------------- KAPI-B
    try:
        b_b, b_olculemedi_kismi = _kapi_b_calistir(motor)
        etiket = "YESIL" if not b_b else "KIRMIZI"
        if b_olculemedi_kismi:
            etiket += " (GERCEK kol OLCULEMEDI — POSIX+root-olmayan gerektirir; "
            etiket += "IZOLASYON kolu olculdu)"
        print("  KAPI-B  (B4-4)          : %s" % etiket)
        for b in b_b:
            print("      - %s" % b)
        if b_b:
            kirmizi += 1
    except Kurulamadi as e:
        print("  KAPI-B  (B4-4)          : OLCULEMEDI — %s" % e)
        olculemeyen += 1
        b_b = None

    # -------------------------------------------------- KAPI-C
    try:
        b_c = _kapi_c_calistir(motor)
        print("  KAPI-C  (pozitif kontrol): %s" % ("KIRMIZI" if b_c else "YESIL"))
        for b in b_c:
            print("      - %s" % b)
        if b_c:
            kirmizi += 1
    except Kurulamadi as e:
        print("  KAPI-C  (pozitif kontrol): OLCULEMEDI — %s" % e)
        olculemeyen += 1
        b_c = None

    # -------------------------------------------------- KAPI-D
    try:
        b_d = kapi_d(sh_metni)
        print("  KAPI-D  (grep tuzagi)   : %s" % ("KIRMIZI" if b_d else "YESIL"))
        for b in b_d:
            print("      - %s" % b)
        if b_d:
            kirmizi += 1
    except Kurulamadi as e:
        print("  KAPI-D  (grep tuzagi)   : OLCULEMEDI — %s" % e)
        olculemeyen += 1
        b_d = None

    # ====================================================== MUTANTLAR
    print("\n--- MUTANT SINAMASI (hafiza.py kaynagina textual sabotaj) ---")
    kacan = 0
    for ad, fn, kapi_etiket in MUTANTLAR_HAFIZA:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  %-46s -> OLCULEMEDI (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        d = tempfile.mkdtemp(prefix="ortamsinif_mut_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            t2 = os.path.join(d, "senaryolar")
            os.makedirs(t2)
            if kapi_etiket == "KAPI-A":
                isirdi = bool(_kapi_a_calistir(sahte))
                olculebilir = True
            elif kapi_etiket == "KAPI-B":
                bm, olculemedi_kismi = _kapi_b_calistir(sahte)
                isirdi = bool(bm)
                # M-B-kilit, GERCEK kolu OLCULEMEDIGI platformlarda (Windows)
                # tek basina ISOLASYON kolundan yakalanamayabilir — bu BEKLENEN
                # bir olcum sinirdir, SESSIZCE "ISIRDI" SAYILMAZ.
                olculebilir = not (olculemedi_kismi and not isirdi and ad.startswith("M-B-kilit"))
            else:  # KAPI-C
                isirdi = bool(_kapi_c_calistir(sahte))
                olculebilir = True
        except Kurulamadi as e:
            print("  %-46s -> OLCULEMEDI (kurulum: %s)" % (ad, e))
            olculemeyen += 1
            continue
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if not olculebilir:
            print("  %-46s -> OLCULEMEDI (bu platformda GERCEK kol yok, "
                  "izolasyon bu mutanti goremiyor)" % ad)
            olculemeyen += 1
        elif isirdi:
            print("  %-46s -> ISIRDI (%s)" % (ad, kapi_etiket))
        else:
            print("  %-46s -> KACTI (%s KOR)" % (ad, kapi_etiket))
            kacan += 1

    print("\n--- MUTANT SINAMASI (ortam_olcum.sh kaynagina textual sabotaj) ---")
    bozuk_sh = m_d_desen_eskiye_donduru(sh_metni)
    if bozuk_sh is None or bozuk_sh == sh_metni:
        print("  %-46s -> OLCULEMEDI (mutant KURULAMADI)" % "M-D  desen eskiye dondurulur")
        olculemeyen += 1
    else:
        try:
            b_d_mut = kapi_d(bozuk_sh)
        except Kurulamadi as e:
            print("  %-46s -> OLCULEMEDI (%s)" % ("M-D  desen eskiye dondurulur", e))
            olculemeyen += 1
        else:
            if b_d_mut:
                print("  %-46s -> ISIRDI (KAPI-D)" % "M-D  desen eskiye dondurulur")
            else:
                print("  %-46s -> KACTI (KAPI-D KOR)" % "M-D  desen eskiye dondurulur")
                kacan += 1

    print()
    if kacan:
        print("SONUC: KIRMIZI — %d mutant KACTI (kapi kor)." % kacan)
        return 1
    if kirmizi:
        print("SONUC: KIRMIZI — %d kapi kendisi kirmizi (mutant sinamasindan ONCE)." % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem kosulamadi/kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    print("SONUC: YESIL — dort kapi de temiz, her mutant ISIRDI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

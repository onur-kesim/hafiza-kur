#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H9 KESME MUTANTI (M-Y4) — `_kapi_h9`nun "git deposu OKUNAMADI" hukmu, git'in
ilk satirini KIRPMADAN mi basiyor? (kalem5-tarama/IS_EMRI_SIK_A.md D2, Onur
kilidi SIK A, 19 Agu 2026 · dayanak: kalem5-tarama/KALEM5_KESME_TARAMASI.md)

NEDEN VAR
  `olculemedi_kesme_mutanti.py`nin (M-Y3, D1) ikiz kardesi: AYNI kalibin
  ikinci uyesi. `hafiza.py` satir ~3956, git alt-surecinin stderr'inin ILK
  SATIRINI `[:120]` ile kesiyordu; o satir (`fatal: ...`) sik sik KOK
  DIZININ YOLUNU tasir. Kok uzunsa yol KIRPILIR, kullanici HANGI DIZIN
  oldugunu YARIM gorur.

NE OLCER — CIFT KOLLU (M-Y3 ile AYNI kalip; POSIX SARTI YOK, UC PLATFORMDA KAPI)
    M-Y4 UZUN KOL : kok >= 170 karakter. Motora ESKI kesme ([:120]) GERI
                    enjekte edilir; H9 satiri KIRPILMALI (kapanis tirnagi
                    `'` ile BITMEMELI) — kapi kusuru DOGRU yakaladi (ISIRDI).
    M-Y4 KISA KOL : kok "kisa" — AMA bu ARTIK bir VARSAYIM DEGIL, bir OLCUM
                    (20 Agu 2026 duzeltmesi, asagidaki 🔴 nota bak). Kolun
                    KENDI ON SARTI ("kirpilmamis H9 mesaji esigin altinda
                    mi") sabotajsiz/duzeltilmis motorla ONCE OLCULUR; ancak
                    saglaniyorsa sabotaj kosulur ve KEHANET (satir kapanis
                    tirnagi `'` ile BITMELI — KACIS BEKLENEN) sinanir. On
                    sart SAGLANMIYORSA kol OLCULEMEDI doner, ASLA BEKLENMEDIK
                    DONMEZ — kor kolun ON SARTININ sinamadigi bir hal, bir
                    kusur BULGUSU degildir.

  🔴 DUZELTME 1 (Onur kilidi 20 Agu 2026, Cowork CI 32250138848 + yerel
  yeniden uretim): KISA KOL "kok kisa = mkdtemp varsayilani" VARSAYIMINI
  tasiyordu. `tempfile.mkdtemp()`nin varsayilan tabani PLATFORMA GORE COK
  FARKLI: Linux ~24 karakter (mesaj 24+53=77, esik 120'nin ALTINDA — kor
  kalir, DOGRU), macOS ~68 karakter (mesaj 68+53=121, esik 120'nin
  USTUNDE — KIRPILIR, kor kol kor KALMAZ). CI'da `H9 kesme mutanti
  (macos-latest)` bu yuzden KIRMIZI yandi: `1/2 kol - 1 beklenmedik`.
  UZUN KOL YESILDI — yani ε₂ tetikleyicisinin KENDISI macOS'ta calisiyor;
  kusur yalniz KISA KOL'un ON SART VARSAYIMINDAYDI.
  Kok'u KENDIMIZ kisa kurmak TEK BASINA YETMEZ: macOS `/tmp`yi
  `/private/tmp`e cozer ve git REALPATH basar (M-A8 dersiyle AYNI mayin —
  H16-KESME-DUZELTME-BRIEF.md). Bu yuzden BIRINCI duzeltme kok'u KISALTMAK
  DEGIL, kolun ON SARTINI dogrudan OLCMEKTIR: duzeltilmis motorla (sabotaj
  YOK) ayni kok/ortamda H9 satiri BIR KEZ kosulur, mesaj uzunlugu esikle
  (dinamik olarak `_SABOTAJLI`den okunur, sabit YAZILMAZ) karsilastirilir.
  Ilk yazimda esikten TUREYEN bir PAY (`esik // 10`) ile bir "guvenli sinir"
  belirleniyordu; bu DUZELTME 3'te KALDIRILDI (asagiya bak, CI #83) —
  karsilastirma simdi DOGRUDAN esige karsi: asilirsa OLCULEMEDI (exit 2),
  asilmazsa sabotaj kosulur.

  🔴 DUZELTME 2 (Onur kilidi 20 Agu 2026, SIK (a) — "kisa tabani KUR"):
  DUZELTME 1 DOGRUYDU ve yalanci kirmiziyi bitirdi — dogrulandi (kok 66-170
  arasi butun ara degerler exit 2, 0 beklenmedik). AMA "exit 2 de sifirdan
  farkli" ve `h9_kesme_mutanti` isinde `continue-on-error` YOK ⇒ macOS
  KALICI KIRMIZI kalirdi (dogru kirmizi, ama hala kirmizi). Cozum
  DUZELTME 1'i GEREKSIZ KILMAZ, ONA EKLENIR: KISA KOL artik KENDI kisa
  tabanini `_kisa_taban_ac()` ile ACAR (POSIX literal `/tmp` altinda,
  varsa) — `mkdtemp(dir=...)` acikca `dir` verilince TMPDIR/TMP/TEMP ortam
  degiskenlerini YOK SAYAR. OLCULDU (Linux): dis TMPDIR 48/110/150 iken
  bile kok hep ~22 kaliyor, 2/2 exit 0. macOS icin bu bir TAHMINdir (kok
  ~33, mesaj ~86 — esigin (120) altinda BEKLENIYOR); ON SART OLCUMU
  (DUZELTME 1) GEREKSIZ OLMAZ — GERCEK OTORITE odur, kisa taban yalnizca
  on sartin cogu ortamda kendiliginden saglanmasini KOLAYLASTIRIR.
  🔴 DOGRULANDI (CI #83 `32374821806`, is `macos-latest`): SUCCESS —
  `_kisa_taban_ac()` `/private/tmp` realpath'ine RAGMEN calisti, bu
  tahmin TUTTU.

  🔴 DUZELTME 3 (Onur kilidi 20 Agu 2026, CI #83 `32374821806`, is
  `96443570144` KIRMIZI): `windows-latest`de ON SART OLCUMU "112 > guvenli
  sinir=108 (esik=120-pay=12)" icin OLCULEMEDI dondu — AMA 112 < 120:
  gercek sabotaj KIRPMAZDI, kol DOGRU olcerdi. Reddeden fiziksel esik
  DEGIL, PAY'in KENDISIYDI. ON SART, sabotajin kullanacagi AYNI kokte
  AYNI mesaji olcuyor (H9 satiri) — ikisi arasindaki TEK fark kesmenin
  kendisi (`[:120]`); ARADA GURULTU YOK, bu yuzden pay HICBIR SEYI
  KORUMUYORDU, yalniz 109-120 bandini (Windows'un varsayilan kok/
  kullanici-adi uzunlugu tam bu bantta) yalanci OLCULEMEDI'ye
  CEVIRIYORDU. DUZELTME: `pay` KALDIRILDI, karsilastirma FIZIKLE AYNI:
  `mesaj_uzunlugu > esik` ⇒ OLCULEMEDI, `<= esik` ⇒ kol kosar (Cowork
  olcumu: mesaj 119→exit 0, 120(=esik)→exit 0, 121→exit 2, 122→exit 2,
  123→exit 2 — `[:120]` TAM 120 karakterlik dizgeyi kesmez, esikte
  ölçüt birebir dogru). 🔴 PAY GERI EKLENMEZ: on sart GURULTUSUZ oldugu
  icin (ayni kok, ayni ortam, TEK degisken kesmenin kendisi) fiziksel
  esikten daha KATI bir olcut hicbir seyi korumaz, yalniz yalanci-
  kirmizi uretir — sonraki tur "guvenlik payi ekleyeyim" DEMESIN.

URETIM TARIFI (SIK EPSILON, 19 Agu 2026 Onur kilidi — birebir OLCULDU)
  git init + commit -> `kur` -> defterler commit'lenir -> `kapi`, git'in KENDI
  sahiplik denetimi `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` ile tetiklenmis olarak
  kosulur. Git `fatal: detected dubious ownership in repository at '<KOK>'`
  verir (exit 128); hem `log` hem `rev-parse --git-dir` duser -> `_kapi_h9`nun
  OKUNAMADI dali kosar. Olculmus imza: kisa kokte 72 karakter (H9 satiri 98),
  uzun kokte 252 (H9 satiri 278).

  🔴 NEDEN `chown` DEGIL (19 Agu 2026, CI #80 `32236392253` ISIRDI): eski tarif
  `chown -R nobody <KOK>` idi. `chown` ile BASKA kullaniciya sahiplik devri
  POSIX'te ROOT ister; GitHub runner'i `runner` kullanicisidir, root DEGILDIR
  -> UC PLATFORMDA DA "kum havuzu kurulamadi" (exit 2). Arac DURUST davrandi;
  kusur ORTAM VARSAYIMINDAYDI. `GIT_TEST_ASSUME_DIFFERENT_OWNER` AYNI mesaji
  uretir, ROOT/sudo GEREKTIRMEZ ve DOSYA SISTEMINE DOKUNMAZ.

  🔴 KALAN ACIK RISK (gizlenmez): degisken git'in KENDI TEST kancasidir; upstream
  kaldirirsa ya da runner'da kuresel `safe.directory` onu etkisizlestirirse mesaj
  URETILMEZ. O halde bu arac SESSIZCE GECMEZ: H9 OKUNAMADI satirini bulamaz ve
  OLCULEMEDI (exit 2) doner — OLCULDU (bkz. asagidaki kuresel-ayar bagisikligi).
  Kuresel ayar bagisikligi icin `GIT_CONFIG_GLOBAL/SYSTEM=os.devnull` +
  `GIT_CONFIG_NOSYSTEM=1` de gecirilir; `safe.directory=*` tanimliyken bile
  iki kol da BEKLENDIGI GIBI olctu.

CAPA (H16-KESME-DUZELTME-BRIEF.md §5 dersi): motora KOD PARCACIGIYLA anchor
atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI (proje sozlesmesi)
  0  iki kolun IKISI DE BEKLENDIGI GIBI (KISA icin 'beklenen' KACIStir)
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  OLCULEMEDI (BEKLENMEDIK yoksa) — tetikleyici mesaji uretmediyse DAHIL
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI (olcum aracina da konur)
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []          # (ad, durum, ayrinti)


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ (D2)
# KALEM 1'in TERSİ (D2): duzeltilmis motora `[0][:120]` kesmesini GERI
# enjekte eder. `.split("\n")[0]`nin KENDISI DOKUNULMAZ (IS_EMRI_SIK_A.md §2)
# — yalniz kuyruktaki `[:120]` eklenir/cikarilir.
_DUZELTILMIS = '_sb = (r.stderr or _rg.stderr or "").strip().split("\\n")[0]'
_SABOTAJLI = '_sb = (r.stderr or _rg.stderr or "").strip().split("\\n")[0][:120]'


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (kalem5-tarama/IS_EMRI_SIK_A.md D2, hafiza.py "
            "_kapi_h9())." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=120, env=None):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if env:
        o.update(env)
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="h9-mut", GIT_AUTHOR_EMAIL="h9-mut@example.invalid",
    GIT_COMMITTER_NAME="h9-mut", GIT_COMMITTER_EMAIL="h9-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kok_hedef_uzunlukta(taban_dizini, hedef_uzunluk):
    """bkz. olculemedi_kesme_mutanti.py._kok_hedef_uzunlukta — AYNI mantik,
    dolgu HEX OLMAYAN ("zq" tekrari)."""
    on_ek = os.path.join(taban_dizini, "")
    gerekli = hedef_uzunluk - len(on_ek)
    if gerekli < 1:
        return None
    dolgu = ("zq" * ((gerekli // 2) + 1))[:gerekli]
    kok = on_ek + dolgu
    os.makedirs(kok, exist_ok=True)
    return kok


# 🔴 AD, YAPILAN ISI SOYLER (M-A8 dersi: adi "realpath maskesi" olup KESMEYI olcen
# bir mutant, maskeyi hic olcmedigini UC AY gizledi). Burada sahiplik DEVREDILMEZ;
# git'in sahiplik DENETIMI supheli hale getirilir. Ad da onu soyler.
_OLCUM_ORTAMI = {
    "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1",   # tetikleyici (root/sudo GEREKMEZ)
    "GIT_CONFIG_NOSYSTEM": "1",               # kuresel/sistem `safe.directory`
    "GIT_CONFIG_GLOBAL": os.devnull,          # bagisikligi — OLCULDU: `*` tanimli
    "GIT_CONFIG_SYSTEM": os.devnull,          # olsa bile iki kol da olcuyor
}


def _sahipligi_supheli_kil():
    """SIK EPSILON: dosya sistemine DOKUNMAZ, kullanici/izin DEGISTIRMEZ.
    Git'in kendi sahiplik denetimi cevre degiskeniyle tetiklenir; uretilen mesaj
    `chown` tarifiyle BIREBIR AYNIDIR (olculdu 19 Agu 2026, git 2.43.0)."""
    return dict(_OLCUM_ORTAMI)


def _kum_havuzu_kur(motor, kok):
    """Uretim tarifi (IS_EMRI_SIK_A.md §4, OLCULDU): git init+commit -> kur ->
    defterler commit'lenir -> depo BASKA kullaniciya devredilir. Motora
    DOKUNMAZ, yalniz komut satirindan cagirir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c = _kos(motor, ["kur", "--ad", "Y4", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))


def _h9_satiri(cikti):
    return next((s for s in cikti.splitlines() if "H9: git deposu OKUNAMADI" in s), None)


_H9_ONEK = "H9: git deposu OKUNAMADI: "


def _h9_mesaj_govdesi(satir):
    """H9 satirindaki, KESMENIN GERCEKTEN uygulandigi parca — `_h9_onek`den
    SONRAKI kisim (bkz. hafiza.py _kapi_h9: `[:120]` `_sb`ye uygulanir,
    "H9: git deposu OKUNAMADI: " oneki SONRADAN eklenir). `startswith`
    DEGIL `split`: basili satir "  ? " ile GIRINTILIDIR (main()'in `O`
    listesi basma bicimi), satir ONEKLE BASLAMAZ — yalniz ICERIR."""
    parca = satir.split(_H9_ONEK, 1)
    return parca[1] if len(parca) == 2 else satir


def _sabotaj_esigi():
    """`_SABOTAJLI` dizgesinden kesme esigini (bugun 120) OKUR — sabit
    YAZILMAZ, sabotaj degisirse bu da otomatik degisir (H16-KESME-DUZELTME-
    BRIEF.md §5 capa dersiyle AYNI ilke: kod parcaciginin KENDISINDEN oku,
    ayri bir sabit YAZMA)."""
    m = re.search(r"\[:(\d+)\]", _SABOTAJLI)
    if not m:
        raise AracKusuru("sabotaj esigi _SABOTAJLI dizgesinden okunamadi (desen degisti mi?)")
    return int(m.group(1))


def _my4_kol(taban, ad, hedef_uzunluk, beklenen_kirpilmamis):
    try:
        esik = _sabotaj_esigi()
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    alt = os.path.join(taban, "u" if hedef_uzunluk else "k")
    os.makedirs(alt, exist_ok=True)
    if hedef_uzunluk:
        kok = _kok_hedef_uzunlukta(alt, hedef_uzunluk)
        if kok is None:
            _kayit(ad, OLCULEMEDI, "hedef uzunluk (%d) bu ortamda kurulamadi" % hedef_uzunluk)
            return
    else:
        kok = os.path.join(alt, "kk")
        os.makedirs(kok, exist_ok=True)
    try:
        _kum_havuzu_kur(MOTOR, kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    sab_dizin = os.path.join(alt, "sab")
    os.makedirs(sab_dizin, exist_ok=True)
    motor_sab = _sabotajli_motor(sab_dizin)
    rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok],
                 env=_sahipligi_supheli_kil())
    satir = _h9_satiri(c)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H9 OKUNAMADI satiri bulunamadi (kok uzunlugu=%d, exit=%s) — "
              "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ olabilir "
              "(surum/platform). SESSIZ GECIS DEGIL, OLCULEMEDI. Ham cikti kuyrugu:\n%s"
              % (len(kok), rc, c[-500:]))
        return
    kirpilmamis = satir.rstrip().endswith("'")
    dogru = (kirpilmamis == beklenen_kirpilmamis)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "kok uzunlugu=%d | sabotajli motor ([:%d] geri) | satir kapanis tirnagi "
          "(') ile bitiyor (kirpilmamis)=%s (beklenen: %s)\n      satir: %s"
          % (len(kok), esik, "VAR" if kirpilmamis else "yok",
             "VAR" if beklenen_kirpilmamis else "yok", satir.strip()))


def my4_uzun_kol(taban):
    try:
        # olculemedi_kesme_mutanti.py ile ayni ders: 200 Windows'ta MAX_PATH'e
        # carpiyordu (git commit'in .git/objects yazimi); 170 mesaj esigini
        # (>120) rahatca asiyor. Bu kol zaten POSIX-disi platformda hic
        # kosmuyor (main() basinda OLCULEMEDI), ama Linux/macOS icin de
        # tutarli tek sabit deger tercih edildi.
        _my4_kol(taban,
                "M-Y4 UZUN KOL: kok>=170, sabotajli motor H9 satirini KIRPMALI (ISIRMALI)",
                170, False)
    except AracKusuru as e:
        _kayit("M-Y4 UZUN KOL", OLCULEMEDI, str(e))


def _kisa_taban_ac():
    """KISA KOL icin GENEL `mkdtemp` yerine KISA bir taban acar (20 Agu 2026
    ikinci duzeltme, Onur kilidi SIK (a) — kisa tabani KUR). POSIX'te
    literal `/tmp` altinda (varsa): `tempfile.mkdtemp(dir=...)` acikca
    `dir` verilince TMPDIR/TMP/TEMP ortam degiskenlerini YOK SAYAR, bu
    yuzden disaridan enjekte edilmis UZUN bir TMPDIR (baska bir aracin
    testi, ya da enjeksiyon) KISA KOL'u ARTIK ETKILEMEZ. OLCULDU (Linux):
    dis TMPDIR 48/110/150 iken bile bu yolla kok hep ~22 karakter kaliyor.

    🔴 GARANTI DEGIL, IYILESTIRME: macOS `/tmp`yi `/private/tmp`e
    REALPATH'ler (M-A8 mayini, H16-KESME-DUZELTME-BRIEF.md) — bu TAHMIN idi
    (kok ~33, mesaj ~86, esigin altinda BEKLENIYORDU); CI #83 `32374821806`
    macos-latest'te SUCCESS ile DOGRULADI. Bu yuzden kisa taban ON SART
    OLCUMUNU GEREKSIZ KILMAZ — ölçüm hala OTORITEDIR, kisa taban yalnizca
    cogu ortamda on sartin KENDILIGINDEN saglanmasini kolaylastiran bir
    on-hazirliktir. `/tmp` yoksa (POSIX-disi/Windows) GENEL varsayilana
    duser."""
    if os.name == "posix" and os.path.isdir("/tmp"):
        try:
            return tempfile.mkdtemp(prefix="h16km_", dir="/tmp")
        except OSError:
            pass
    return tempfile.mkdtemp(prefix="h16km_")


def my4_kisa_kol():
    """20 Agu 2026: UC duzeltme BIRLIKTE calisir.
    (1) "kisa kok" bir VARSAYIM DEGIL, bir OLCUMDUR (ilk duzeltme):
        `tempfile.mkdtemp()`nin GENEL varsayilan tabani Linux'ta ~24,
        macOS'ta ~68 karakterdir — macOS'ta mesaj (68+53=121) esigi (120)
        ASAR ve kor kol kor KALMAZ (CI 32250138848, Onur kilidi). Kolun
        KENDI ON SARTI ("kirpilmamis H9 mesaji esigin altinda mi")
        sabotajsiz/duzeltilmis motorla ONCE OLCULUR; ancak SAGLANIYORSA
        sabotaj kosulur. Saglanmiyorsa OLCULEMEDI (exit 2) doner — ASLA
        BEKLENMEDIK: bir kusur BULGUSU degil, bu ortamda olculemeyen bir
        ON SARTTIR.
    (2) Kisa taban artik AYRICA KURULUYOR (ikinci duzeltme, `_kisa_taban_ac`):
        ON SART OLCUMU DOGRUdur ama "exit 2 de sifirdan farkli" ve
        `h9_kesme_mutanti` isinde `continue-on-error` YOK — yalanci kirmizi
        DURUST kirmiziya donse de macOS KALICI KIRMIZI kalirdi. Kok'u
        `/tmp` altinda BIZ kisa kurmak (1)'i GEREKSIZ KILMAZ — (1) hala
        OTORITEDIR, (2) yalnizca cogu ortamda on sartin kendiliginden
        saglanmasini kolaylastirir. (macOS `/private/tmp` REALPATH riski
        bir TAHMINdi; CI #83 `32374821806` SUCCESS ile DOGRULADI.)
    (3) ON SART karsilastirmasinda PAY YOK (ucuncu duzeltme, CI #83 is
        `96443570144` windows-latest KIRMIZI): esikten TUREYEN bir pay
        (`esik // 10`) mesaj=112'yi esik=120'nin ALTINDAYKEN bile
        OLCULEMEDI'ye ceviriyordu — sabotaj GERCEKTE kirpmazdi. On sart
        GURULTUSUZ oldugu icin (sabotajin AYNI kokte AYNI mesaji, tek
        fark kesmenin kendisi) pay hicbir seyi korumuyordu; simdi
        `mesaj_uzunlugu > esik` FIZIGIN KENDISI."""
    ad = "M-Y4 KISA KOL (KOR KOL): kisa kokte AYNI sabotaj GORUNMEZ KALMALI (KACMASI BEKLENEN)"
    try:
        kisa_taban = _kisa_taban_ac()
    except OSError as e:
        _kayit(ad, OLCULEMEDI, "kisa taban acilamadi: %s" % e)
        return
    try:
        alt = os.path.join(kisa_taban, "k")
        os.makedirs(alt, exist_ok=True)
        kok = os.path.join(alt, "kk")
        os.makedirs(kok, exist_ok=True)
        try:
            esik = _sabotaj_esigi()
            _kum_havuzu_kur(MOTOR, kok)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "on sart hazirlanamadi: %s" % e)
            return

        # --- ON SART OLCUMU: duzeltilmis (sabotajsiz) motorla BIR KEZ kos -----
        env = _sahipligi_supheli_kil()
        rc0, c0 = _kos(MOTOR, ["kapi", "--kok=" + kok], env=env)
        satir0 = _h9_satiri(c0)
        if satir0 is None:
            _kayit(ad, OLCULEMEDI,
                  "on sart OLCULEMEDI: duzeltilmis motorla H9 OKUNAMADI satiri "
                  "bulunamadi (kok uzunlugu=%d, exit=%s) — "
                  "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ olabilir "
                  "(surum/platform). Ham cikti kuyrugu:\n%s" % (len(kok), rc0, c0[-500:]))
            return
        mesaj_uzunlugu = len(_h9_mesaj_govdesi(satir0))
        # DUZELTME 3 (20 Agu 2026, CI #83): PAY YOK — on sart GURULTUSUZ
        # (sabotajin kullanacagi AYNI kokte AYNI mesaji olcer, TEK degisken
        # kesmenin kendisi), bu yuzden karsilastirma DOGRUDAN fizikle AYNI:
        # sabotaj `[:esik]` KIRPAR ancak mesaj esigi ASARSA. Bir PAY EKLEMEK
        # yalniz yalanci-kirmizi uretir (Windows CI #83, mesaj=112<esik=120
        # gercekte kirpilmazdi) — pay BURAYA GERI EKLENMEZ.
        if mesaj_uzunlugu > esik:
            _kayit(ad, OLCULEMEDI,
                  "ON SART SAGLANMIYOR (bu ortamda kisa kol OLCULEMEZ — kusur "
                  "BULGUSU DEGIL): kirpilmamis H9 mesaj uzunlugu=%d > esik=%d. "
                  "kok uzunlugu=%d, kok=%s\n"
                  "      ham (sabotajsiz) satir: %s"
                  % (mesaj_uzunlugu, esik, len(kok), kok,
                     satir0.strip()))
            return

        # --- ON SART SAGLANDI: simdi sabotaji kos, KEHANETI sina --------------
        sab_dizin = os.path.join(alt, "sab")
        os.makedirs(sab_dizin, exist_ok=True)
        try:
            motor_sab = _sabotajli_motor(sab_dizin)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "sabotajli motor kurulamadi: %s" % e)
            return
        rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok], env=env)
        satir = _h9_satiri(c)
        if satir is None:
            _kayit(ad, OLCULEMEDI,
                  "sabotajli kosumda H9 OKUNAMADI satiri bulunamadi (kok uzunlugu=%d, "
                  "exit=%s) — on sart olcumunde VARDI, sabotajli kosumda YOK: "
                  "tutarsizlik. Ham cikti kuyrugu:\n%s" % (len(kok), rc, c[-500:]))
            return
        kirpilmamis = satir.rstrip().endswith("'")
        _kayit(ad, BEKLENDIGI_GIBI if kirpilmamis else BEKLENMEDIK,
              "kisa taban=%s | ON SART OLCULDU: kirpilmamis mesaj uzunlugu=%d "
              "(esik=%d) | sabotajli motor ([:%d] geri) "
              "| satir kapanis tirnagi (') ile bitiyor (kirpilmamis)=%s "
              "(beklenen: VAR)\n      kok uzunlugu=%d, kok=%s"
              % (kisa_taban, mesaj_uzunlugu, esik, esik,
                 "VAR" if kirpilmamis else "yok", len(kok), kok))
    finally:
        shutil.rmtree(kisa_taban, ignore_errors=True)


def main():
    print("=" * 82)
    print("H9 KESME MUTANTI (M-Y4) — _kapi_h9 OKUNAMADI hukmu kirpilmadan mi basiyor?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h16km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        my4_uzun_kol(taban)
        my4_kisa_kol()
        print()
        for ad, durum, ayrinti in SONUC:
            print("  %-16s %s" % (durum, ad))
            print("  %-16s   %s" % ("", ayrinti))
        print(CIZGI)
        beklenmedik = sum(1 for _, d, _ in SONUC if d == BEKLENMEDIK)
        olculemedi = sum(1 for _, d, _ in SONUC if d == OLCULEMEDI)
        gibi = len(SONUC) - beklenmedik - olculemedi
        print("SONUC: %d/%d kol BEKLENDIGI GIBI - %d beklenmedik - %d olculemedi"
              % (gibi, len(SONUC), beklenmedik, olculemedi))
        if beklenmedik:
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

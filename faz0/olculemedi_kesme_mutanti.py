#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OLCULEMEDI KESME MUTANTI (M-Y3) — `kapi_yalit()`nin OLCULEMEDI hukmu, dosya
adini KIRPMADAN mi basiyor? (kalem5-tarama/IS_EMRI_SIK_A.md D1, Onur kilidi
SIK A, 19 Agu 2026 · dayanak: kalem5-tarama/KALEM5_KESME_TARAMASI.md)

NEDEN VAR
  18 Agu turunda `hafiza.py:3326`deki sabit `kesildi[:160]` kaldirildi (H16-
  KESME-DUZELTME-BRIEF.md). AYNI KALIBIN bir uyesi daha vardi ve o turda
  ATLANDI: `kapi_yalit()` (satir ~379), bir kapiyi YALITTIGINDA bastigi
  OLCULEMEDI hukmunu `ilk[:150]` ile kesiyordu — `ilk`, SON_HATA[0]nin ILK
  SATIRI, ve o satir sik sik `oldur()`un yazdigi bir DOSYA YOLU tasir (ornek:
  H8/korunan kapisinin "DOSYA UTF-8 DEGIL: <yol>" mesaji). Kok dizini uzunsa
  yol KIRPILIR ve kullaniciya HANGI DOSYA oldugu YARIM gosterilir.

  Bu is emri o duzeltmeyi TAMAMLAR (KALEM 5 taramasinin SIK A'si); yeni bir
  kural ACMAZ — ayni kalibin ikinci ISIRIsi, tek seferlik.

NE OLCER — CIFT KOLLU (--uzun-yol dersinin M-Y2 kalibi)
  Bir kolun ISIRMASI kadar, AYNI kolun YANLIS ORTAMDA (kisa yolda) KACMASI da
  olculmelidir — yoksa bir sonraki turde biri bu kapiyi kisa `/tmp`e tasir ve
  kapi sessizce kor olur (DURUM.md: "OLCUMU KOSTUM, ONU KORUYAN KAPIYI
  KOSMADIM").
    M-Y3 UZUN KOL : kok >= 170 karakter (bkz. asagidaki 200->170 notu).
                    Motora ESKI kesme ([:150]) GERI enjekte edilir;
                    OLCULEMEDI satiri KIRPILMALI (`NOTLAR.md` ile
                    BITMEMELI) — kapi kusuru DOGRU yakaladi (ISIRDI).
    M-Y3 KISA KOL : kok "kisa" — AMA bu ARTIK bir VARSAYIM DEGIL, bir OLCUM
                    (4 Eylul 2026 duzeltmesi, asagidaki 🔴 nota bak). Kolun
                    KENDI ON SARTI ("kirpilmamis OLCULEMEDI mesaji esigin
                    altinda mi") sabotajsiz/duzeltilmis motorla ONCE
                    OLCULUR; ancak saglaniyorsa sabotaj kosulur ve KEHANET
                    (satir `NOTLAR.md` ile BITMELI — KACIS BEKLENEN) sinanir.
                    On sart SAGLANMIYORSA kol OLCULEMEDI doner, ASLA
                    BEKLENMEDIK DONMEZ — kor kolun ON SARTININ sinamadigi
                    bir hal, bir kusur BULGUSU degildir.

  🔴 DUZELTME (Onur kilidi 4 Eylul 2026, IS_EMRI_MY3.md — dayanak
  OLCUM_RAPORU_MY3.md): KISA KOL "kok kisa = mkdtemp varsayilani" VARSAYIMINI
  tasiyordu; bu, M-Y4'un (h9_kesme_mutanti.py) 20 Agu 2026'da kapattigi
  kusurun BIREBIR AYNISIYDI (KALEM5_KESME_TARAMASI.md sinifinin ikinci
  uyesi, ikinci kez ISIRDI — DURUM.md'nin "iki kez isirmayan olay kural
  olamaz" maddesi geregi artik kalici kural). Duzeltme M-Y4 ile AYNI UC
  parcadan olusur: (1) on sart bir OLCUMDUR, VARSAYIM DEGIL — duzeltilmis
  motorla (sabotaj YOK) ayni kok/ortamda OLCULEMEDI satiri BIR KEZ kosulur,
  mesaj uzunlugu esikle (dinamik olarak `_SABOTAJLI`den okunur, sabit
  YAZILMAZ) karsilastirilir; (2) kok'un KENDISI `_kisa_taban_ac()` ile
  KISA KURULUR (POSIX `/tmp` altinda, `dir=` acikca verilince disaridan
  enjekte edilmis TMPDIR'i YOK SAYAR) — bu ON SART OLCUMUNU GEREKSIZ KILMAZ,
  yalniz cogu ortamda on sartin kendiliginden saglanmasini KOLAYLASTIRIR;
  (3) karsilastirmada PAY YOK — `mesaj_uzunlugu > esik` FIZIGIN KENDISI,
  esikten TUREYEN bir pay M-Y4'un Windows CI #83'unde yalanci-kirmizi
  uretmisti (ayni fizik burada da GECERLI, bkz. `my3_kisa_kol` docstring'i).

URETIM TARIFI (IS_EMRI_SIK_A.md §4, birebir OLCULDU)
  git init + commit -> `kur` -> `korunan --dosya=NOTLAR.md --bas=BASLA
  --son=BITIS --gerekce=<>=15 karakter>` -> NOTLAR.md UTF-8 DISI bayta
  (`\\xff\\xfe`) cevrilir -> `kapi` -> `? H8 (NOTLAR.md): OLCULEMEDI — DOSYA
  UTF-8 DEGIL: <yol>`. Olculmus imza: kisa kokte girdi ~43 karakter, uzun
  kokte ~244 (H16-KOK-SEBEP-RAPORU.md mayini: dolgu HEX OLMAYAN, "zq" tekrari
  — `<SHA>` desenine yakalanmasin).

CAPA (H16-KESME-DUZELTME-BRIEF.md §5 dersi): motora KOD PARCACIGIYLA anchor
atilir, satir NUMARASIYLA DEGIL — motor degisirse `count()!=1` ARAC KUSURU
verir, YANLIS yere yamanmaz.

CIKIS KODLARI (proje sozlesmesi)
  0  iki kolun IKISI DE BEKLENDIGI GIBI (KISA icin 'beklenen' KACIStir)
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
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


# --------------------------------------------------------------- SABOTAJ (D1)
# KALEM 1'in TERSİ (D1): duzeltilmis motora `ilk[:150]` kesmesini GERI
# enjekte eder. Iki dize de hafiza.py:379'un BUGUNKU (duzeltilmis) ve DUN
# (sabotajli) haliyle BIREBIR eslesir — motor degisirse bu sabotaj da
# degismelidir (altin_olcut_mutanti.py'nin ESKI_TAM kalibiyla ayni ders).
_DUZELTILMIS = 'O.append("%s: OLCULEMEDI — %s" % (etiket, ilk))'
_SABOTAJLI = 'O.append("%s: OLCULEMEDI — %s" % (etiket, ilk[:150]))'


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (kalem5-tarama/IS_EMRI_SIK_A.md D1, hafiza.py "
            "kapi_yalit())." % n)
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
    GIT_AUTHOR_NAME="olculemedi-mut", GIT_AUTHOR_EMAIL="olculemedi-mut@example.invalid",
    GIT_COMMITTER_NAME="olculemedi-mut", GIT_COMMITTER_EMAIL="olculemedi-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kok_hedef_uzunlukta(taban_dizini, hedef_uzunluk):
    """`taban_dizini` altinda tam `hedef_uzunluk` karaktere ulasan bir kok
    dizini kurar; kurulamazsa None doner (cagiran OLCULEMEDI ilan eder,
    sessizce atlamaz). Dolgu HEX OLMAYAN, notr ("zq" tekrari — H16-KOK-SEBEP-
    RAPORU.md §2b mayini: hex dolgu `<SHA>` sanilip YANLIS maskelenir)."""
    on_ek = os.path.join(taban_dizini, "")
    gerekli = hedef_uzunluk - len(on_ek)
    if gerekli < 1:
        return None
    dolgu = ("zq" * ((gerekli // 2) + 1))[:gerekli]
    kok = on_ek + dolgu
    os.makedirs(kok, exist_ok=True)
    return kok


def _kum_havuzu_kur(motor, kok):
    """Uretim tarifi (IS_EMRI_SIK_A.md §4, OLCULDU): git init+commit -> kur ->
    korunan (H8) -> NOTLAR.md UTF-8 DISI bayta cevrilir. Motora DOKUNMAZ,
    yalniz komut satirindan cagirir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c = _kos(motor, ["kur", "--ad", "Y3", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    notlar = os.path.join(kok, "NOTLAR.md")
    with open(notlar, "w", encoding="utf-8", newline="\n") as f:
        f.write("not\nBASLA\nkorunan icerik satiri\nBITIS\n")
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))
    rc, c = _kos(motor, ["korunan", "--kok=" + kok, "--dosya=NOTLAR.md",
                         "--bas=BASLA", "--son=BITIS",
                         "--gerekce=olculemedi kesme mutanti icin korunan blok"])
    if rc != 0:
        raise AracKusuru("korunan basarisiz (exit=%s): %s" % (rc, c[-300:]))
    with open(notlar, "wb") as f:
        f.write(b"\xff\xfe")


def _olculemedi_satiri(cikti):
    return next((s for s in cikti.splitlines() if "H8 (NOTLAR.md): OLCULEMEDI" in s), None)


_OLCULEMEDI_AYRAC = "OLCULEMEDI — "


def _olculemedi_mesaj_govdesi(satir):
    """H8 OLCULEMEDI satirindaki, KESMENIN GERCEKTEN uygulandigi parca —
    `_OLCULEMEDI_AYRAC`dan SONRAKI kisim (bkz. hafiza.py kapi_yalit():
    `ilk[:150]` `ilk`ye uygulanir, "%s: OLCULEMEDI — " oneki SONRADAN
    eklenir). `startswith` DEGIL `split`: basili satir "  ? " ile
    GIRINTILIDIR (main()'in `O` listesi basma bicimi), satir ONEKLE
    BASLAMAZ — yalniz ICERIR. Ayrac BULUNAMAZSA None doner — h9_kesme_
    mutanti.py'nin `_h9_mesaj_govdesi`sinden FARKLI olarak satirin
    KENDISINE SESSIZCE DUSMEZ: cagiran (my3_kisa_kol) None'i OLCULEMEDI
    ilan eder (IS_EMRI_MY3.md KALEM 1c)."""
    parca = satir.split(_OLCULEMEDI_AYRAC, 1)
    return parca[1] if len(parca) == 2 else None


def _sabotaj_esigi():
    """`_SABOTAJLI` dizgesinden kesme esigini (bugun 150) OKUR — sabit
    YAZILMAZ, sabotaj degisirse bu da otomatik degisir (H16-KESME-DUZELTME-
    BRIEF.md §5 capa dersiyle AYNI ilke: kod parcaciginin KENDISINDEN oku,
    ayri bir sabit YAZMA — bkz. h9_kesme_mutanti.py'nin ayni adli
    fonksiyonu, M-Y4)."""
    m = re.search(r"\[:(\d+)\]", _SABOTAJLI)
    if not m:
        raise AracKusuru("sabotaj esigi _SABOTAJLI dizgesinden okunamadi (desen degisti mi?)")
    return int(m.group(1))


def _my3_kol(taban, ad, hedef_uzunluk, beklenen_kirpilmamis):
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
    rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok])
    satir = _olculemedi_satiri(c)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H8 OLCULEMEDI satiri bulunamadi (kok uzunlugu=%d, exit=%s) — ham cikti kuyrugu:\n%s"
              % (len(kok), rc, c[-500:]))
        return
    kirpilmamis = satir.rstrip().endswith("NOTLAR.md")
    dogru = (kirpilmamis == beklenen_kirpilmamis)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "kok uzunlugu=%d | sabotajli motor ([:150] geri) | satir NOTLAR.md ile "
          "bitiyor (kirpilmamis)=%s (beklenen: %s)\n      satir: %s"
          % (len(kok), "VAR" if kirpilmamis else "yok",
             "VAR" if beklenen_kirpilmamis else "yok", satir.strip()))


def my3_uzun_kol(taban):
    # IS_EMRI_SIK_A.md hedefi kok>=200 idi (Linux'ta OLCULDU). Windows'ta 220
    # denendi ve git commit "Filename too long" verdi (.git/objects/xx/<hash>
    # kok'un UZERINE ~42 karakter daha ekliyor, MAX_PATH'i asiyor — H16-KESME-
    # DUZELTME-BRIEF KALEM 2'nin AYNI dersi). 170 uc platformda da mesaj
    # esigini (>150) rahatca asiyor ve git nesne yazimina pay birakiyor.
    _my3_kol(taban,
            "M-Y3 UZUN KOL: kok>=170, sabotajli motor OLCULEMEDI satirini KIRPMALI (ISIRMALI)",
            170, False)


def _kisa_taban_ac():
    """KISA KOL icin GENEL `mkdtemp` yerine KISA bir taban acar (M-Y4'ten
    (h9_kesme_mutanti.py) BIREBIR tasindi, yalniz `prefix`). POSIX'te
    literal `/tmp` altinda (varsa): `tempfile.mkdtemp(dir=...)` acikca
    `dir` verilince TMPDIR/TMP/TEMP ortam degiskenlerini YOK SAYAR, bu
    yuzden disaridan enjekte edilmis UZUN bir TMPDIR (baska bir aracin
    testi, ya da enjeksiyon) KISA KOL'u ARTIK ETKILEMEZ. OLCULDU (Linux):
    dis TMPDIR 48/110/150 iken bile bu yolla kok hep ~22 karakter kaliyor.

    🔴 GARANTI DEGIL, IYILESTIRME: macOS `/tmp`yi `/private/tmp`e
    REALPATH'ler (M-A8 mayini, H16-KESME-DUZELTME-BRIEF.md) — bu TAHMIN idi
    (kok ~33, mesaj ~62, esigin altinda BEKLENIYORDU); M-Y4'te CI #83
    `32374821806` macos-latest'te SUCCESS ile DOGRULANMISTI. Bu yuzden kisa
    taban ON SART OLCUMUNU GEREKSIZ KILMAZ — ölçüm hala OTORITEDIR, kisa
    taban yalnizca cogu ortamda on sartin KENDILIGINDEN saglanmasini
    kolaylastiran bir on-hazirliktir. `/tmp` yoksa (POSIX-disi/Windows)
    GENEL varsayilana duser."""
    if os.name == "posix" and os.path.isdir("/tmp"):
        try:
            return tempfile.mkdtemp(prefix="y3km_", dir="/tmp")
        except OSError:
            pass
    return tempfile.mkdtemp(prefix="y3km_")


def my3_kisa_kol():
    """4 Eylul 2026 duzeltmesi (IS_EMRI_MY3.md, dayanak OLCUM_RAPORU_MY3.md):
    kisa kolun ON SARTI ("kirpilmamis OLCULEMEDI mesaji esigin altinda mi")
    artik bir VARSAYIM DEGIL, bir OLCUMDUR — M-Y4'un (h9_kesme_mutanti.py,
    20 Agu 2026) BIREBIR ayni duzeltmesi, D1'in ikiz kardesi D... icin
    tekrarlandi (KALEM5_KESME_TARAMASI.md sinifinin ikinci uyesi, ikinci
    kez ISIRDI). Eski hal `hedef_uzunluk=0` ile `_my3_kol`e dusuyordu ve
    kokun (`mkdtemp` varsayilani) HER PLATFORMDA mesaji esigin (150) ALTINDA
    tutacagini VARSAYIYORDU — OLCUM_RAPORU_MY3.md §1'in gosterdigi gibi bu
    bir olcum degildi, kaynaktan OKUNMUSTU.

    Duzeltilmis akis (kum havuzu kurulduktan sonra, sabotajli motor
    kosulmadan ONCE):
      1. `_sabotaj_esigi()` ile esik OKUNUR (bugun 150, sabit YAZILMAZ).
      2. Kisa taban `_kisa_taban_ac()` ile ACILIR (M-Y4 ile ayni ilke: kisa
         taban bir GARANTI DEGIL, IYILESTIRMEDIR — asagidaki ON SART
         OLCUMUNU GEREKSIZ KILMAZ).
      3. TEMIZ (sabotajsiz) motorla BIR KEZ `kapi --kok=<kok>` kosulur.
      4. H8 (NOTLAR.md): OLCULEMEDI satiri YOKSA -> OLCULEMEDI (kok
         uzunlugu, exit, ham cikti kuyrugu (son 500 karakter) kayda yazilir).
      5. `_olculemedi_mesaj_govdesi(satir0)` None DONERSE (ayrac
         bulunamadi) -> OLCULEMEDI (sessizce atlanmaz, KALEM 1c).
      6. `mesaj_uzunlugu = len(govde0)`; `mesaj_uzunlugu > esik` ISE ->
         OLCULEMEDI (bu ortamda kisa kol OLCULEMEZ — kusur BULGUSU DEGIL).
      7. On sart SAGLANDIYSA sabotajli motor kosulur ve KEHANET (satir
         NOTLAR.md ile BITMELI — KACIS BEKLENEN) sinanir.

    🔴 PAY YOK VE GERI EKLENMEZ (IS_EMRI_MY3.md KALEM 1d, OLCUM_RAPORU_MY3.md
    §3'un dersi — M-Y4'un CI #83 windows-latest yalanci-kirmizisiyla AYNI
    fizik): on sart, sabotajin kullanacagi AYNI kokte AYNI mesaji olcer;
    aradaki TEK degisken kesmenin KENDISIDIR, GURULTU YOKTUR. Karsilastirma
    fizikle birebir ayni olmalidir: `mesaj_uzunlugu > esik`. `>=` de
    YANLISTIR — [:150] TAM 150 karakterlik dizgeyi KESMEZ (OLCUM_RAPORU_MY3.md
    §3: kok=121/mesaj=150 sabotajli motorda da KIRPMADI). Bir sonraki tur
    "guvenlik payi ekleyeyim" DEMESIN: pay esikten TUREYEN her ne olursa
    olsun, GURULTUSUZ bir on sarti fizikten daha KATI hale getirir ve
    yalniz yalanci-OLCULEMEDI uretir, hicbir seyi KORUMAZ."""
    ad = "M-Y3 KISA KOL (KOR KOL): kisa kokte AYNI sabotaj GORUNMEZ KALMALI (KACMASI BEKLENEN)"
    try:
        esik = _sabotaj_esigi()
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
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
            _kum_havuzu_kur(MOTOR, kok)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "on sart hazirlanamadi: %s" % e)
            return

        # --- ON SART OLCUMU: duzeltilmis (sabotajsiz) motorla BIR KEZ kos -----
        rc0, c0 = _kos(MOTOR, ["kapi", "--kok=" + kok])
        satir0 = _olculemedi_satiri(c0)
        if satir0 is None:
            _kayit(ad, OLCULEMEDI,
                  "on sart OLCULEMEDI: duzeltilmis motorla H8 (NOTLAR.md): "
                  "OLCULEMEDI satiri bulunamadi (kok uzunlugu=%d, exit=%s). "
                  "Ham cikti kuyrugu:\n%s" % (len(kok), rc0, c0[-500:]))
            return
        govde0 = _olculemedi_mesaj_govdesi(satir0)
        if govde0 is None:
            _kayit(ad, OLCULEMEDI,
                  "on sart OLCULEMEDI: '%s' ayraci satirda bulunamadi (kok "
                  "uzunlugu=%d)\n      ham satir: %s"
                  % (_OLCULEMEDI_AYRAC, len(kok), satir0.strip()))
            return
        mesaj_uzunlugu = len(govde0)
        # PAY YOK (yukaridaki docstring'e bak): karsilastirma DOGRUDAN esige
        # karsi, fizikten daha KATI bir esik YOK. Pay BURAYA GERI EKLENMEZ.
        if mesaj_uzunlugu > esik:
            _kayit(ad, OLCULEMEDI,
                  "ON SART SAGLANMIYOR (bu ortamda kisa kol OLCULEMEZ — kusur "
                  "BULGUSU DEGIL): kirpilmamis OLCULEMEDI mesaj uzunlugu=%d > "
                  "esik=%d. kok uzunlugu=%d, kok=%s\n"
                  "      ham (sabotajsiz) satir: %s"
                  % (mesaj_uzunlugu, esik, len(kok), kok, satir0.strip()))
            return

        # --- ON SART SAGLANDI: simdi sabotaji kos, KEHANETI sina --------------
        sab_dizin = os.path.join(alt, "sab")
        os.makedirs(sab_dizin, exist_ok=True)
        try:
            motor_sab = _sabotajli_motor(sab_dizin)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "sabotajli motor kurulamadi: %s" % e)
            return
        rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok])
        satir = _olculemedi_satiri(c)
        if satir is None:
            _kayit(ad, OLCULEMEDI,
                  "sabotajli kosumda H8 (NOTLAR.md): OLCULEMEDI satiri "
                  "bulunamadi (kok uzunlugu=%d, exit=%s) — on sart olcumunde "
                  "VARDI, sabotajli kosumda YOK: tutarsizlik. Ham cikti "
                  "kuyrugu:\n%s" % (len(kok), rc, c[-500:]))
            return
        kirpilmamis = satir.rstrip().endswith("NOTLAR.md")
        _kayit(ad, BEKLENDIGI_GIBI if kirpilmamis else BEKLENMEDIK,
              "kisa taban=%s | ON SART OLCULDU: kirpilmamis mesaj uzunlugu=%d "
              "(esik=%d) | sabotajli motor ([:%d] geri) "
              "| satir NOTLAR.md ile bitiyor (kirpilmamis)=%s "
              "(beklenen: VAR)\n      kok uzunlugu=%d, kok=%s"
              % (kisa_taban, mesaj_uzunlugu, esik, esik,
                 "VAR" if kirpilmamis else "yok", len(kok), kok))
    finally:
        shutil.rmtree(kisa_taban, ignore_errors=True)


def main():
    print("=" * 82)
    print("OLCULEMEDI KESME MUTANTI (M-Y3) — kapi_yalit() OLCULEMEDI hukmu kirpilmadan mi basiyor?")
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
        try:
            my3_uzun_kol(taban)
            my3_kisa_kol()
        except AracKusuru as e:
            print("\nARAC KUSURU: %s" % e)
            return 3
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

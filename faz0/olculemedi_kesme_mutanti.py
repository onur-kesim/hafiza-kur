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
    M-Y3 UZUN KOL : kok >= 200 karakter. Motora ESKI kesme ([:150]) GERI
                    enjekte edilir; OLCULEMEDI satiri KIRPILMALI (`NOTLAR.md`
                    ile BITMEMELI) — kapi kusuru DOGRU yakaladi (ISIRDI).
    M-Y3 KISA KOL : kok kisa (mkdtemp varsayilani, ~dolgusuz). AYNI sabotaj;
                    mesaj zaten <150 karakter oldugu icin GORUNMEZ KALMALI
                    (satir `NOTLAR.md` ile BITMELI) — bu KACIS BEKLENEN ve
                    ISTENEN sonuctur, kapinin KENDI korlugunu olcer.

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


def my3_kisa_kol(taban):
    _my3_kol(taban,
            "M-Y3 KISA KOL (KOR KOL): kisa kokte AYNI sabotaj GORUNMEZ KALMALI (KACMASI BEKLENEN)",
            0, True)


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
            my3_kisa_kol(taban)
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

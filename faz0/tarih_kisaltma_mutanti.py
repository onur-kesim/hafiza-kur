#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TARIH KISALTMA MUTANTI — `AYLAR` sozlugu Turkce ay KISALTMALARINI taniyor
mu, ve tanimazsa H12 ile H14 BIRLIKTE kor mu kaliyor?
(besli-paket/IS_EMRI.md KALEM 1, Onur kilidi 6 Eylul 2026)

NEDEN VAR (6 Eylul 2026 DOGFOOD TURUNUN BULGUSU — ISIRDI)
  hafiza-kur, KENDI deposuna `devral` ile kuruldu (bulut klonunda, salt
  deneme) ve kapi FAIL verdi. Iki bulgu `?` (OLCULEMEDI) tipindeydi:
      ? H12: 'Son guncelleme' satiri var ama tarih COZULEMEDI
      ? H14: hafiza tarihi cozulemedi — disiplin OLCULEMIYOR
  Yani urunun ANA VAADI olan iki TAZELIK kapisi, hafiza-kur'un KENDI
  `DURUM.md`'sinde aylardir HIC olcmuyordu. O dosya `Son guncelleme:
  4 Eyl 2026 · bu dosya <=8 KB · ...` diyordu.

  🔴 ILK HIPOTEZ YANLISTI ve bu, ISI EMRI YAZILMADAN once olculdu:
  `·` ayraci sanildi. `tarih_coz` DOGRUDAN cagrilarak matris kosuldu:
      '6 Eylül 2026 · bu dosya ≤8 KB · **x**'  -> 2026-09-06   COZULUYOR
      '2026-09-06 · bu dosya ≤8 KB'            -> 2026-09-06   COZULUYOR
      '06.09.2026 · bu dosya'                  -> 2026-09-06   COZULUYOR
      '6 Eyl 2026'                             -> None         COZULEMIYOR
  ⇒ ayrac SORUN DEGIL. KOK: `AYLAR` sozlugu yalniz TAM ay adlarini
  iceriyordu (`ocak`..`aralik`); Turkce KISALTMA (`Eyl`, `Agu`, `Sub`)
  yoktu. `tarih_coz` ikinci desende `AYLAR.get(slug(...))` yapip None
  donunce `_h12_tazelik` `t_son=None` uretiyor — ve **H14 ayni degeri
  kullandigi icin O DA susuyor**. TEK kok, IKI kor kapi.

  Duzeltme: `AYLAR`'a on iki kisaltma eklendi. Anahtarlar `slug()`
  ciktisidir; `slug("Ağu")=="agu"`, `slug("Şub")=="sub"` OLCULDU.

  🔴 NEDEN CI BUNU GORMEDI: `capraz.yml` kendi SENTETIK deneme projesinde
  kosuyor; hafiza-kur'un KENDI belgeleri olcum kumesinde HIC yoktu. Bu
  mutant o bosluga da bir capa atar: senaryosu, projenin kendi `DURUM.md`
  baslik satirinin BICIMIDIR (`<tarih> · <ek metin> · **<kalin>**`).

NE OLCER (BES KOL — dordu kehanetli, biri KAPSAM sinavi)
  Sabotaj `AYLAR`'daki kisaltma blogunu DUSURUR (kusurun kendisi: sozluk
  eski haline, yalniz tam adlara doner).

  1. H12 POZITIF KONTROL : sabotajSIZ motor + kisaltmali tarih ->
                           hukum "H12: son guncelleme N gun once" TASIR.
  2. H12 MUTANT          : sabotajLI motor + AYNI vaka -> hukum
                           "tarih COZULEMEDI" der (kusur GERI GELDI).
  3. H14 POZITIF KONTROL : sabotajSIZ motorda H14 "cozulemedi" DEMEZ.
  4. H14 MUTANT          : sabotajLI motorda H14 "cozulemedi" DER.
                           (3+4 birlikte: TEK kok IKI kapiyi susturuyor.)
  5. KAPSAM SINAVI       : sabotajLI motorda TAM ay adi ("6 Eylül 2026")
                           HALA cozulur. Sabotaj yalniz KISALTMA eksenini
                           kapatmali; tum tarih ayristirmasini kirsaydi
                           1-4 numarali kollar bu sinifi degil KOMSU bir
                           sinifi olcerdi (sabotaj sinamasi, SKILL.md §5).

  Olculen: `kapi`nin **stdout**'undaki hukum satirlarinin METNI.
  `stderr` AYRI boruda tutulur, BIRLESTIRILMEZ. `kapi`nin ham exit kodu
  KEHANET DEGILDIR: bu vakada H9 (commit'siz depo) zaten bir `?` uretir,
  yani exit iki halde de aynidir — olculen sey hukum METNIDIR.

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL —
motor degisirse `count()!=1` ARAC KUSURU verir, YANLIS yere yamanmaz.

CIKIS KODLARI (proje sozlesmesi)
  0  BES kolun BESI DE BEKLENDIGI GIBI
  1  en az bir kol BEKLENMEDIK
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi)
"""
import datetime as _dt
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

# Turkce ay KISALTMALARI — motordaki AYLAR anahtarlariyla AYNI eksen.
AY_KISA = ["Oca", "Şub", "Mar", "Nis", "May", "Haz",
           "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
AY_TAM = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
          "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# H12'nin OLCTUGU hal: N listesine dusen taze hukum.
_H12_OLCTU = re.compile(r"H12: son guncelleme \d+ gun once")
# H12'nin OLCEMEDIGI hal: O listesine dusen itiraf.
_H12_KOR = "tarih COZULEMEDI"
# H14'un OLCEMEDIGI hal.
_H14_KOR = "hafiza tarihi cozulemedi"


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ
# `AYLAR`'daki KISALTMA blogunu dusurur. Kalan sozluk gecerli Python'dur
# (tam adlar sondaki virgulle biter, blok `}` ile kapanir) — yani sabotaj
# SOZDIZIMI kirmaz, yalniz KISALTMA eksenini kapatir. 5. kol tam bunu olcer.
_DUZELTILMIS = '''         "oca": 1, "sub": 2, "mar": 3, "nis": 4, "may": 5, "haz": 6,
         "tem": 7, "agu": 8, "eyl": 9, "eki": 10, "kas": 11, "ara": 12}'''
_SABOTAJLI = '''         }'''


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (besli-paket/IS_EMRI.md KALEM 1, hafiza.py AYLAR)." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=180):
    """`stdout` ve `stderr` AYRI doner — BIRLESTIRILMEZ."""
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git(kok, *args):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, **_GIT_ORTAM))
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="tk-mut", GIT_AUTHOR_EMAIL="tk-mut@example.invalid",
    GIT_COMMITTER_NAME="tk-mut", GIT_COMMITTER_EMAIL="tk-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _damgayi_yaz(kok, metin):
    """Canli hafizanin 'Son guncelleme' satirini VERILEN metinle degistirir.
    Bicim, hafiza-kur'un KENDI DURUM.md baslik satirindan alinmistir:
        '<tarih> · <duz metin> · **<kalin metin>**'
    Yani senaryo, projenin gercek belgesinin BICIMIDIR — sentetik degil."""
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    s = open(p, encoding="utf-8", newline="").read()
    yeni = "> Son guncelleme: %s · bu dosya <=8 KB · **kapanan bolum tek satira iner**" % metin
    s2, adet = re.subn(r"> Son gu[nü]celleme:[^\n]*", yeni, s, count=1)
    if adet != 1:
        raise AracKusuru("'Son guncelleme' satiri canli hafizada bulunamadi (%d)" % adet)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s2)


def _kum_havuzu(motor, kok, damga):
    """git init -> `kur` -> canli hafizanin damgasi VERILEN bicime cevrilir.
    KUM HAVUZU PAYLASILMAZ: her cagiran KENDI `kok`unu verir (paylasilan kum
    havuzu YALANCI KIRMIZI uretir — DURUM.md 'olcum aleti yalani', vaka 7)."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "TK", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    _damgayi_yaz(kok, damga)


def _kapi_hukmu(motor, kok):
    rc, c, e = _kos(motor, ["kapi", "--kok=" + kok])
    if rc is None:
        raise AracKusuru("kapi ZAMAN ASIMI: " + e)
    return c


def _bugun_kisa():
    b = _dt.date.today()
    return "%d %s %d" % (b.day, AY_KISA[b.month - 1], b.year)


def _bugun_tam():
    b = _dt.date.today()
    return "%d %s %d" % (b.day, AY_TAM[b.month - 1], b.year)


# ------------------------------------------------------------------ KOLLAR
def _kol_h12(motor, kok, ad, isaret_bekleniyor):
    """isaret_bekleniyor=True  -> H12 OLCMELI ('son guncelleme N gun once')
       isaret_bekleniyor=False -> H12 KOR olmali ('tarih COZULEMEDI')"""
    _kum_havuzu(motor, kok, _bugun_kisa())
    c = _kapi_hukmu(motor, kok)
    olctu = bool(_H12_OLCTU.search(c))
    kor = _H12_KOR in c
    if olctu and kor:
        return _kayit(ad, OLCULEMEDI, "hem OLCTU hem KOR satiri var — hukum belirsiz")
    if not olctu and not kor:
        return _kayit(ad, OLCULEMEDI, "H12 hakkinda HICBIR satir yok (hukum kanali degisti?)")
    if olctu == isaret_bekleniyor:
        return _kayit(ad, BEKLENDIGI_GIBI,
                      "H12 %s (beklenen)" % ("OLCTU" if olctu else "KOR"))
    _kayit(ad, BEKLENMEDIK,
           "H12 %s, beklenen %s" % ("OLCTU" if olctu else "KOR",
                                    "OLCTU" if isaret_bekleniyor else "KOR"))


def _kol_h14(motor, kok, ad, kor_bekleniyor):
    _kum_havuzu(motor, kok, _bugun_kisa())
    c = _kapi_hukmu(motor, kok)
    kor = _H14_KOR in c
    if kor == kor_bekleniyor:
        return _kayit(ad, BEKLENDIGI_GIBI,
                      "H14 %s (beklenen)" % ("KOR" if kor else "OLCTU"))
    _kayit(ad, BEKLENMEDIK,
           "H14 %s, beklenen %s" % ("KOR" if kor else "OLCTU",
                                    "KOR" if kor_bekleniyor else "OLCTU"))


def _kol_kapsam(motor, kok, ad):
    """SABOTAJ SINAMASI: sabotajli motorda TAM ay adi HALA cozulmeli.
    Cozulmuyorsa sabotaj kisaltma eksenini degil TUM tarih ayristirmasini
    kirmistir ve yukaridaki kollar KOMSU bir sinifi olcuyordur."""
    _kum_havuzu(motor, kok, _bugun_tam())
    c = _kapi_hukmu(motor, kok)
    if _H12_OLCTU.search(c):
        return _kayit(ad, BEKLENDIGI_GIBI, "TAM ay adi sabotajli motorda da cozuldu")
    _kayit(ad, BEKLENMEDIK,
           "sabotaj TAM ay adini da kirdi — kapsam GENIS, kollar komsu sinifi olcuyor")


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    gecici = tempfile.mkdtemp(prefix="tkm_")
    try:
        try:
            sab = _sabotajli_motor(gecici)
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
        try:
            _kol_h12(MOTOR, os.path.join(gecici, "a"), "1. H12 POZITIF KONTROL", True)
            _kol_h12(sab, os.path.join(gecici, "b"), "2. H12 MUTANT", False)
            _kol_h14(MOTOR, os.path.join(gecici, "c"), "3. H14 POZITIF KONTROL", False)
            _kol_h14(sab, os.path.join(gecici, "d"), "4. H14 MUTANT", True)
            _kol_kapsam(sab, os.path.join(gecici, "e"), "5. KAPSAM SINAVI (tam ay adi)")
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    print("=" * 82)
    print("TARIH KISALTMA MUTANTI — AYLAR sozlugu kisaltmalari taniyor mu?")
    print("=" * 82)
    for ad, durum, ayrinti in SONUC:
        print("  %-26s %-16s %s" % (ad, durum, ayrinti))
    print(CIZGI)
    bek = sum(1 for _, d, _ in SONUC if d == BEKLENDIGI_GIBI)
    print("SONUC: %d/%d kol BEKLENDIGI GIBI" % (bek, len(SONUC)))
    if any(d == BEKLENMEDIK for _, d, _ in SONUC):
        return 1
    if any(d == OLCULEMEDI for _, d, _ in SONUC):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

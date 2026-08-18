#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — YAPI KAPISI MUTANTI (H16) — 11 proje hali + 9 motor mutanti.

NEDEN VAR (kaynak: YAPI_KAPISI_TASARIM.md 12 Agu + ADR_H16_UYGULAMA_KISITI.md
17 Agu 2026): `kapi` yalnizca `y.h`in (arsiv/hafiza) dizin olup olmadigina
bakiyordu; diger UC dizin (`y.gunluk` · `y.gunluk_ars` · `y.kararlar`) hem
"dizin degil" hem "proje disina kacis" sinifinda TAMAMEN OLCULMUYORDU. Bozuk
projede `kapi` exit 0 (YESIL) diyordu ve stdout/stderr'de bozuk dizinin adi
HIC gecmiyordu (grep sayimi 0) — hukum yalniz yanlis degil, GIZLIYDI. `derle`
ayni bozmayi TEMIZ hata ile yakaliyordu: bilgi URUNDE vardi, OLCUM KAPISINDA
yoktu. H16 bu boslugu `_kapi_h16` ile kapatir (bkz. hafiza.py, fonksiyonun
kendi docstring'i).

NE OLCER — 11 proje hali (p00 NOTR ADLANDIRMAYLA — asagida neden)
  p00 y0_temiz      KONTROL 1  exit 0, H16 hicbir satir basmaz (temiz emsali)
  p01 y1_kararlar_dosya         exit 1, [H16] ve "kararlar"
  p02 y2_kararlar_yok           exit 1, [H16] ve "kararlar"
  p03 y3_gunluk_dosya           exit 1, [H16] ve "gunluk"
  p04 y4_gunluk_yok             exit 1, [H16] ve "gunluk"
  p05 y5_ars_gunluk_dosya       exit 1, [H16]
  p06 y6_arsiv_dosya  KONTROL 2 exit 1, bulgu [H6] KALMALI, [H16] DEGIL (§4.3)
  p07 y7_kararlar_kacis         exit 1, [H16] ve GERCEK hedef yolu ciktida
  p08 y8_gunluk_kacis           exit 1, [H16]
  p09 y9_h_kacis                exit 1, [H16] — BUGUN exit 3 idi (§4.4)
  p10 y10_ic_link     KONTROL 3 exit 0, proje ICINE link kusur DEGIL

  🔴 KUM HAVUZU DIZIN ADLARI NOTR (p00…p10) — OLCULDU (17 Agu, ADR §3.1):
  ilk kosumda `kararlar`/`gunluk` grep sayaci senaryo dizin ADINI (orn.
  `y1_kararlar_dosya`) `kok:` basligindan sayiyordu — olcum aracinin KENDI
  adlandirmasi olctugu metne siziyordu. Nötr ad + DESENLE kok maskeleme
  (esitlikle degil) bu sizmayi kapatir.

NE OLCER — 9 motor mutanti (M-Y1..M-Y9, YAPI_KAPISI_TASARIM.md §6.2)
  M-Y1 KAPI DUSURME    · M-Y2 KAPSAM DARALTMA · M-Y3 SILINMIS->NOT
  M-Y4 `oldur` DONUSU  · M-Y5 TEMIZDE KONUS   · M-Y6 gunluk_ars DUSUR
  M-Y7 SINIR KAYMASI   · M-Y8 KACIS DUSURME   · M-Y9 KACISTA `oldur`
  M-Y5/M-Y7/M-Y9 birer OLCUT mutantidir (kapinin degil, MALIYET ve SOZLESME
  iddialarinin isirip isirmadigini olcerler); ucu de zorunludur.
  Her mutant icin YALNIZ "isirdi" yazilmaz — HANGI hallerde (kac olcumde)
  fark verdigi tek tek yazilir (FAZC kalibi): M-Y2/M-Y6 ve M-Y8/M-Y9
  ORTUSEBILIR (tasarim kendi uyarisi) — ortusme GIZLENMEZ, sayilarak gosterilir.

NE OLCMEZ (SINIR — gizlenmez)
  1. KAÇIŞ halleri (p07/p08/p09/p10) bir dizin-kacis baglantisi gerektirir.
     POSIX'te `os.symlink`; Windows'ta NTFS JUNCTION (`mklink /J`) — bu
     AYRICALIK GEREKTIRMEZ (`os.symlink` Gelistirici Modu/Yonetici ister,
     WinError 1314 OLCULDU; junction istemez, OLCULDU 17 Agu). Junction'in
     `kok_disina_mi`/`shutil.rmtree` karsisinda symlink'le AYNI davrandigi
     AYRICA dogrulandi (Python 3.12 `os.path.isjunction()` farkindaligi).
     Baglanti hicbir yontemle kurulamazsa o HAL OLCULEMEDI sayilir, sessizce
     ATLANMAZ — YOK-SAYILMAZ, HERKESE YAZILIR.
  2. "p00 çıktısı bölme öncesiyle bit-bit ayni" iddiasinin ASIL kaniti
     `faz0/altin_cikti.py --karsilastir` (kabul olcutu madde a; kumedeki
     kayit sayisi ARTEFAKTTAN okunur, burada sabit YAZILMAZ — bir onceki
     sayi bayatladi, bkz. `faz0/altin_kapi.json`) — bu dosya p00'i yalniz
     "exit 0 ve H16 sessiz" olarak dogrular
     ve motoru IKI KEZ kosarak DETERMINIZM'i sinar; 22 referansla bit-bit
     karsilastirma bu dosyanin ekseni DEGILDIR (ortusen olcum onlenir).
  3. Windows/macOS harici platformlar kosulmadi; kacis sinifinin oradaki
     davranisi (junction, reparse point, NFD) CI'nindir.

CIKIS KODLARI
  0  11 halin (kacis haric OLCULEBILEN hepsi) referans hukmu dogru VE
     9/9 mutant ISIRDI
  1  bir hal beklenmedik hukum verdi ya da bir mutant KACTI
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi, git yok) — sessiz PASS yok
"""
import io
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
            pass


VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")

CIZGI = "-" * 82


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi — kapinin/mutantin kor oldugu ANLAMINA GELMEZ."""


def _dizin_link_kur(link, hedef):
    """Dizin icin bir 'kacis' baglantisi kurar. Windows'ta `os.symlink()`
    Gelistirici Modu/Yonetici GEREKTIRIR (WinError 1314, OLCULDU 17 Agu
    2026); NTFS JUNCTION (`mklink /J`) ise AYRICALIK GEREKTIRMEZ ve
    `os.path.realpath()`/`os.path.isdir()` onu sembolik linkle AYNI sekilde
    cozer (OLCULDU: `kok_disina_mi` yalniz realpath karsilastirir, junction'i
    da symlink'i de es davranir). `shutil.rmtree` Python 3.12'de
    `os.path.isjunction()` FARKINDADIR — junction'i SILER, HEDEFE dokunmaz
    (AYRICA DOGRULANDI). POSIX'te duz `os.symlink` kullanilir."""
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", link, hedef],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode != 0:
            raise OSError(r.stderr.decode("utf-8", "replace"))
    else:
        os.symlink(hedef, link, target_is_directory=True)


def _kacis_baglanti_calisir_mi(taban):
    """Bu ortamda dizin-kacis baglantisi (junction/symlink) KURULABILIYOR mu?"""
    d = os.path.join(taban, "_link_probu")
    os.makedirs(d)
    hedef = os.path.join(d, "hedef")
    os.makedirs(hedef)
    link = os.path.join(d, "link")
    try:
        _dizin_link_kur(link, hedef)
        return os.path.isdir(link)
    except OSError:
        return False
    finally:
        shutil.rmtree(d, ignore_errors=True)


# --------------------------------------------------------------- PROJE HALLERI
def _proje_kur(motor, taban, ad):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)   # `kur` --kok'un ONCEDEN VAR olmasini ister ("kok yok")
    p = subprocess.run([sys.executable, motor, "kur", "--kok=" + kok, "--ad=proj"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, p.stderr.decode("utf-8", "replace")[:200]))
    return kok


def _dizin_sil(p0):
    if os.path.isdir(p0) and not os.path.islink(p0):
        shutil.rmtree(p0)
    elif os.path.lexists(p0):
        os.remove(p0)


def _dosya_yap(p0):
    _dizin_sil(p0)
    with io.open(p0, "w", encoding="utf-8") as f:
        f.write("bozuk\n")


def _kacis_link(p0, harici_hedef):
    _dizin_sil(p0)
    _dizin_link_kur(p0, harici_hedef)


# (ad, kurucu(kok, harici), kacis_mi, kontrol_notu)
def _hal_p00(kok, harici):
    pass


def _hal_p01(kok, harici):
    _dosya_yap(os.path.join(kok, "kararlar"))


def _hal_p02(kok, harici):
    _dizin_sil(os.path.join(kok, "kararlar"))


def _hal_p03(kok, harici):
    _dosya_yap(os.path.join(kok, "gunluk"))


def _hal_p04(kok, harici):
    _dizin_sil(os.path.join(kok, "gunluk"))


def _hal_p05(kok, harici):
    _dosya_yap(os.path.join(kok, "arsiv", "hafiza", "gunluk"))


def _hal_p06(kok, harici):
    _dosya_yap(os.path.join(kok, "arsiv"))


def _hal_p07(kok, harici):
    _kacis_link(os.path.join(kok, "kararlar"), harici)


def _hal_p08(kok, harici):
    _kacis_link(os.path.join(kok, "gunluk"), harici)


def _hal_p09(kok, harici):
    _kacis_link(os.path.join(kok, "arsiv", "hafiza"), harici)


def _hal_p10(kok, harici):
    ic = os.path.join(kok, "_ic_hedef")
    os.makedirs(ic, exist_ok=True)
    _kacis_link(os.path.join(kok, "kararlar"), ic)


HALLER = [
    ("p00", "y0_temiz (KONTROL 1)", _hal_p00, False),
    ("p01", "y1_kararlar_dosya", _hal_p01, False),
    ("p02", "y2_kararlar_yok", _hal_p02, False),
    ("p03", "y3_gunluk_dosya", _hal_p03, False),
    ("p04", "y4_gunluk_yok", _hal_p04, False),
    ("p05", "y5_ars_gunluk_dosya", _hal_p05, False),
    ("p06", "y6_arsiv_dosya (KONTROL 2)", _hal_p06, False),
    ("p07", "y7_kararlar_kacis", _hal_p07, True),
    ("p08", "y8_gunluk_kacis", _hal_p08, True),
    ("p09", "y9_h_kacis", _hal_p09, True),
    ("p10", "y10_ic_link (KONTROL 3)", _hal_p10, True),
]

# Beklenen HUKUM (yalniz REFERANS/duzeltilmis motor icin — mutant kosumlarinda
# kullanilmaz, mutant kosumlari yalniz REFERANSLA kiyaslar).
BEKLENEN = {
    "p00": (0, None, None),                 # exit 0, [H16] YOK
    "p01": (1, "[H16]", "kararlar"),
    "p02": (1, "[H16]", "kararlar"),
    "p03": (1, "[H16]", "gunluk"),
    "p04": (1, "[H16]", "gunluk"),
    "p05": (1, "[H16]", None),
    "p06": (1, "[H6]", "[H16]-YOK"),         # ozel: [H6] VAR, [H16] YOK olmali
    "p07": (1, "[H16]", None),
    "p08": (1, "[H16]", None),
    "p09": (1, "[H16]", None),
    "p10": (0, None, None),
}


def _kapi_kos(motor, kok):
    p = subprocess.run([sys.executable, motor, "kapi", "--kok=" + kok],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def _maskele(metin, kok):
    """Yol maskelemesi DESENLE (esitlikle degil — md.8'in bedeli odenmis dersi)."""
    m = re.sub(r'--kok="[^"]*"', '--kok="<KOK>"', metin)
    m = m.replace(kok, "<KOK>").replace(kok.replace(os.sep, "/"), "<KOK>")
    try:
        rk = os.path.realpath(kok)
        m = m.replace(rk, "<KOK>").replace(rk.replace(os.sep, "/"), "<KOK>")
    except OSError:
        pass
    return m


def kume_uret(motor, taban, atlanan_haller, harici):
    """Her hal icin (exit, maskelenmis_cikti). `atlanan_haller` kacis
    kurulamayan hallerin adlarini tasir (OLCULEMEDI, sessiz PASS degil).
    `harici` TUM kosumlar (referans/determinizm/her mutant) arasinda
    PAYLASILAN SABIT bir dizindir — kacis mesajindaki GERCEK hedef yolu
    (§ y7 kabul olcutu) boylece kosumdan kosuma DEGISMEZ; degisseydi
    determinizm kolu her seferinde SAHTE bir fark uretirdi (kok DISINDAKI
    bir yol, kok-tabanli maskelemenin kapsami disinda kalir)."""
    olcum = {}
    for ad, _aciklama, kurucu, kacis_mi in HALLER:
        if ad in atlanan_haller:
            continue
        kok = _proje_kur(motor, taban, ad)
        kurucu(kok, harici)
        kod, cikti = _kapi_kos(motor, kok)
        olcum[ad] = (kod, _maskele(cikti, kok))
    return olcum


def referans_hukmu_dogrula(olcum):
    """REFERANS (duzeltilmis, mutantsiz) motorun 11 halin HEPSINDE beklenen
    hukmu verdigini dogrular. Donen: bulgu listesi (bos ise hepsi dogru)."""
    b = []
    for ad, _aciklama, _kurucu, _kacis_mi in HALLER:
        if ad not in olcum:
            continue
        kod, cikti = olcum[ad]
        exp_kod, exp_var, exp_kelime = BEKLENEN[ad]
        if kod != exp_kod:
            b.append("%s: exit %d (beklenen %d)" % (ad, kod, exp_kod))
            continue
        if ad == "p06":
            if "[H6]" not in cikti:
                b.append("%s: [H6] bulgusu YOK (§4.3 ihlali)" % ad)
            if "[H16]" in cikti:
                b.append("%s: [H16] de gecti — H6/H16 SINIRI bulanik (§4.3 ihlali)" % ad)
            continue
        if exp_var and exp_var not in cikti:
            b.append("%s: %s bulgusu YOK" % (ad, exp_var))
        if exp_kelime and exp_kelime not in cikti:
            b.append("%s: bulguda '%s' kelimesi GECMIYOR (gizli hukum riski)" % (ad, exp_kelime))
    return b


# --------------------------------------------------------------- MUTANTLAR
# Her hedef motorda TEK YERDE gecmeli — `_tek_yerde` ile dogrulanir. Anchor
# secmeden ONCE motorda kac kez gectigi SAYILIR (olculmus vaka: replace(...,1)
# yanlis fonksiyona kurabilir).
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n"
                         % (n, hedef[:70]))
        return False
    return True


_CAGRI = "    _kapi_h16(F, N, O, y)\n"

_FOR_TUPLE = ('for ad, d in (("kararlar", y.kararlar), ("gunluk", y.gunluk),\n'
             '                  ("gunluk_ars", y.gunluk_ars), ("h", y.h)):')

_FAIL_LAMBDA_ARDINDAN_FOR = ('fail = lambda k, m: F.append("[%s] %s" % (k, m))\n'
                             '    ' + _FOR_TUPLE)

_KACIS_DALI = ('        elif kok_disina_mi(y.kok, d):\n'
              '            fail("H16", "%s PROJE DISINA BAGLI: %s -> %s" '
              '% (ad, d, os.path.realpath(d)))')

_H6_BLOK_VE_CAGRI = (
    '    if not os.path.isdir(y.h):\n'
    '        # KALEM C (Onur kilidi 18 Agu 2026, H16-DUZELTME-BRIEF.md §3): "YOK"/\n'
    '        # "DIZIN DEGIL" ayrimi + TEK `fail()` cagrisi gerekcesi icin bkz.\n'
    '        # `_kapi_h16`nin docstring\'i (asagida) — [H6] etiketi burada KALIR.\n'
    '        fail("H6", ("HAFIZA DIZINI DIZIN DEGIL: %s — bir dosya, "\n'
    '                    "kirik link ya da link dongusu kaplamis olabilir. Tasi ya "\n'
    '                    "da sil." % y.h)\n'
    '                   if os.path.lexists(y.h) else\n'
    '                   "HAFIZA DIZINI YOK: %s — arsiv tabani kayip." % y.h)\n'
    '        return\n'
    '    _kapi_h16(F, N, O, y)'
)


def m_y1_kapi_dusurme(s):
    """M-Y1: `_kapi_h16` cagrisi dagitimdan SILINIR -> kapi hic olculmez."""
    yeni = '    pass  # MUTANT M-Y1: _kapi_h16 cagrisi dagitimdan silindi\n'
    return s.replace(_CAGRI, yeni, 1) if _tek_yerde(s, _CAGRI) else None


def m_y2_kapsam_daraltma(s):
    """M-Y2: H16'nin dizin listesi (y.h,)'ye INER -> bugunku bosluk geri gelir."""
    yeni = 'for ad, d in (("h", y.h),):  # MUTANT M-Y2: kapsam (y.h,)e daraltildi'
    return s.replace(_FOR_TUPLE, yeni, 1) if _tek_yerde(s, _FOR_TUPLE) else None


def m_y3_silinmis_not(s):
    """M-Y3: "yok" dali `fail` yerine `not`(N.append) yazar -> exit 1 -> 0."""
    hedef = ('        if not os.path.lexists(d):\n'
             '            fail("H16", "%s YOK: %s" % (ad, d))')
    yeni = ('        if not os.path.lexists(d):\n'
            '            N.append("H16: %s YOK: %s" % (ad, d))  # MUTANT M-Y3')
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m_y4_oldur_donusu(s):
    """M-Y4: H16'nin `fail` kapanisi `oldur()`e doner -> naif duzeltme sinifi
    geri sizar (exit 1 -> 3, 16 kapinin TUMU kesilir)."""
    yeni = ('fail = lambda k, m: oldur("[%s] %s" % (k, m))  # MUTANT M-Y4\n'
            '    ' + _FOR_TUPLE)
    return s.replace(_FAIL_LAMBDA_ARDINDAN_FOR, yeni, 1) if _tek_yerde(s, _FAIL_LAMBDA_ARDINDAN_FOR) else None


def m_y5_temizde_konus(s):
    """M-Y5 (OLCUT mutanti): H16 her kosumda kosulsuz bir NOT basar -> altin
    kume FARK vermeli (temizde sessizlik iddiasinin kendi kaniti)."""
    yeni = ('fail = lambda k, m: F.append("[%s] %s" % (k, m))\n'
            '    N.append("H16: yapi kontrolu calisti")  # MUTANT M-Y5\n'
            '    ' + _FOR_TUPLE)
    return s.replace(_FAIL_LAMBDA_ARDINDAN_FOR, yeni, 1) if _tek_yerde(s, _FAIL_LAMBDA_ARDINDAN_FOR) else None


def m_y6_gunluk_ars_dusur(s):
    """M-Y6: yalniz `y.gunluk_ars` listeden CIKARILIR -> o hal tek basina
    olculmez (M-Y2'den FARKLI: digerleri hala olculur)."""
    yeni = ('for ad, d in (("kararlar", y.kararlar), ("gunluk", y.gunluk),\n'
            '                  ("h", y.h)):  # MUTANT M-Y6: gunluk_ars dusuruldu')
    return s.replace(_FOR_TUPLE, yeni, 1) if _tek_yerde(s, _FOR_TUPLE) else None


def m_y7_sinir_kaymasi(s):
    """M-Y7 (OLCUT mutanti): H16, H6'nin erken cikisinin ONUNE alinir ->
    y6_arsiv_dosya kolu [H6]'dan [H16]'ya doner, ADDITIVE kisit BOZULUR."""
    yeni = (
        '    _kapi_h16(F, N, O, y)  # MUTANT M-Y7: H6 erken cikisinin ONUNE alindi\n'
        '    if not os.path.isdir(y.h):\n'
        '        fail("H6", ("HAFIZA DIZINI DIZIN DEGIL: %s — bir dosya, "\n'
        '                    "kirik link ya da link dongusu kaplamis olabilir. Tasi ya "\n'
        '                    "da sil." % y.h)\n'
        '                   if os.path.lexists(y.h) else\n'
        '                   "HAFIZA DIZINI YOK: %s — arsiv tabani kayip." % y.h)\n'
        '        return'
    )
    return s.replace(_H6_BLOK_VE_CAGRI, yeni, 1) if _tek_yerde(s, _H6_BLOK_VE_CAGRI) else None


def m_y8_kacis_dusurme(s):
    """M-Y8: `kok_disina_mi` cagrisi H16'dan CIKARILIR -> kacis sinifi (y7/
    y8/y9) HICBIRI olculmez, sessizce YESIL kalir."""
    yeni = ('        elif False:  # MUTANT M-Y8: kacis kontrolu dusuruldu\n'
            '            fail("H16", "%s PROJE DISINA BAGLI: %s -> %s" '
            '% (ad, d, os.path.realpath(d)))')
    return s.replace(_KACIS_DALI, yeni, 1) if _tek_yerde(s, _KACIS_DALI) else None


def m_y9_kaciste_oldur(s):
    """M-Y9 (OLCUT mutanti): YALNIZ `y.h` kacisi eski `oldur` yoluna geri
    konur -> §4.4'un sozlesme degisikligi (exit 3 -> 1) SESSIZCE geri alinir;
    kararlar/gunluk kacisi (y7/y8) ETKILENMEZ — M-Y8'den bu yuzden AYRI eksen."""
    yeni = ('        elif kok_disina_mi(y.kok, d):\n'
            '            if d is y.h:  # MUTANT M-Y9: y.h kacisi eski oldur yoluna donuyor\n'
            '                oldur("DIZIN PROJE DISINA BAGLI: %s -> %s" % (d, os.path.realpath(d)))\n'
            '            fail("H16", "%s PROJE DISINA BAGLI: %s -> %s" '
            '% (ad, d, os.path.realpath(d)))')
    return s.replace(_KACIS_DALI, yeni, 1) if _tek_yerde(s, _KACIS_DALI) else None


MUTANTLAR = [
    ("M-Y1 KAPI DUSURME", m_y1_kapi_dusurme, "kapi hic olculmuyor"),
    ("M-Y2 KAPSAM DARALTMA", m_y2_kapsam_daraltma, "bugunku bosluk geri gelir"),
    ("M-Y3 SILINMIS->NOT", m_y3_silinmis_not, "onaylanan hukum sessizce gevser"),
    ("M-Y4 `oldur` DONUSU", m_y4_oldur_donusu, "naif duzeltme sinifi geri sizar"),
    ("M-Y5 TEMIZDE KONUS", m_y5_temizde_konus, "altin kume FARK vermeli"),
    ("M-Y6 gunluk_ars DUSUR", m_y6_gunluk_ars_dusur, "yeni hal tek basina olculmez"),
    ("M-Y7 SINIR KAYMASI", m_y7_sinir_kaymasi, "y6 kolu [H6]->[H16] doner"),
    ("M-Y8 KACIS DUSURME", m_y8_kacis_dusurme, "kacis sinifi hic olculmez"),
    ("M-Y9 KACISTA `oldur`", m_y9_kaciste_oldur, "sozlesme degisikligi geri alinir"),
]


def _git_var():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except OSError:
        return False


def main():
    _cikti_kodlamasini_guvenceye_al()
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    yol = os.path.abspath(yol)
    print(CIZGI)
    print("YAPI KAPISI MUTANTI (H16) — motor: %s · platform: %s" % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    if not _git_var():
        print("SONUC: OLCULEMEDI — `git` yok.")
        return 2
    try:
        kaynak = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="h16_probu_")
    harici = os.path.join(taban, "harici")   # TEK, PAYLASILAN kacis hedefi (bkz. kume_uret)
    os.makedirs(harici, exist_ok=True)
    baglanti_var = _kacis_baglanti_calisir_mi(taban)
    atlanan = set()
    if not baglanti_var:
        atlanan = set(ad for ad, _a, _k, kacis_mi in HALLER if kacis_mi)
        print("OLCULEMEDI (ortam kisiti): dizin-kacis baglantisi (junction/symlink) "
              "bu ortamda KURULAMIYOR -> %d HAL atlaniyor: %s"
              % (len(atlanan), ", ".join(sorted(atlanan))))
        print(CIZGI)

    try:
        referans = kume_uret(yol, os.path.join(taban, "ref"), atlanan, harici)
    except Kurulamadi as e:
        shutil.rmtree(taban, ignore_errors=True)
        print("SONUC: OLCULEMEDI — referans kume kurulamadi: %s" % e)
        return 2
    # TEMIZ KOL: ayni motor iki kez -> FARK YOK (duzenek determinist mi? FAZC kalibi)
    try:
        ikinci = kume_uret(yol, os.path.join(taban, "ref2"), atlanan, harici)
    except Kurulamadi as e:
        shutil.rmtree(taban, ignore_errors=True)
        print("SONUC: OLCULEMEDI — determinizm kolu kurulamadi: %s" % e)
        return 2
    determinizm_farki = [ad for ad in referans if referans[ad] != ikinci.get(ad)]
    if determinizm_farki:
        shutil.rmtree(taban, ignore_errors=True)
        print("SONUC: OLCULEMEDI — duzenek determinist degil (%s) — mutant hukmu ANLAMSIZ."
              % ", ".join(determinizm_farki))
        return 2
    print("  DETERMINIZM KOLU (ayni motor 2 kez)   FARK YOK — %d/%d hal olculebildi"
          % (len(referans), len(HALLER)))

    bulgu = referans_hukmu_dogrula(referans)
    if bulgu:
        print("\nSONUC: KIRMIZI — referans motor beklenen hukmu vermiyor:")
        for x in bulgu:
            print("  - %s" % x)
        shutil.rmtree(taban, ignore_errors=True)
        return 1
    print("  REFERANS HUKUM DOGRULAMASI             TUTUYOR — 11/11 hal (olculebilenler) beklendigi gibi")
    print(CIZGI)

    isirdi, kacti, olculemeyen = [], [], []
    for ad, fn, aciklama in MUTANTLAR:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  ?  %-24s OLCULEMEDI  mutant KURULAMADI" % ad)
            olculemeyen.append(ad)
            sys.stdout.flush()
            continue
        try:
            compile(bozuk, "<mutant>", "exec")
        except SyntaxError as e:
            print("  ?  %-24s OLCULEMEDI  mutant DERLENMIYOR: %s" % (ad, e))
            olculemeyen.append(ad)
            continue
        d = os.path.join(taban, ad.split()[0])
        os.makedirs(d, exist_ok=True)
        sahte = os.path.join(d, "hafiza.py")
        with io.open(sahte, "w", encoding="utf-8", newline="") as f:
            f.write(bozuk)
        try:
            yeni = kume_uret(sahte, os.path.join(d, "hal"), atlanan, harici)
        except Kurulamadi as e:
            print("  ?  %-24s OLCULEMEDI  hal kurulamadi: %s" % (ad, e))
            olculemeyen.append(ad)
            shutil.rmtree(d, ignore_errors=True)
            continue
        farklilar = sorted(ah for ah in referans if referans[ah] != yeni.get(ah))
        shutil.rmtree(d, ignore_errors=True)
        if farklilar:
            isirdi.append(ad)
            print("  +  %-24s ISIRDI      %d olcumde fark (%s) · %s"
                  % (ad, len(farklilar), ",".join(farklilar), aciklama))
        else:
            kacti.append(ad)
            print("  !  %-24s KACTI       0 olcumde fark · %s" % (ad, aciklama))
            print("     -> kapi BU SINIF icin KOR; H16 o sinifta OLCULMEMISTIR.")
        sys.stdout.flush()

    shutil.rmtree(taban, ignore_errors=True)
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemeyen), len(MUTANTLAR)))
    if atlanan:
        print("  🔴 %d HAL (kacis sinifi) bu ortamda OLCULEMEDI (symlink yok) — "
              "yukaridaki fark sayilari bu haller HARIC kalan kumeden gelir." % len(atlanan))
    if olculemeyen:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = H16'nin bu sinif icin KOR oldugu anlamina gelir.")
        return 1
    print("  Tasarimin ongordugu her sinif olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

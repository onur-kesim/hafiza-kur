#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALTIN CIKTI — kapi ciktisi DEGISTI mi? (Faz C esdegerlik kapisi)

NEDEN VAR
  Faz C `_kapi_govde`'yi (748 satir, CC 284) kapi basina saf fonksiyonlara boluyor.
  Bir REFACTORING'in vaadi tektir: DAVRANIS AYNI KALIR. Ama bu vaat, olculmedigi
  surece bir dilektir — ve bu depoda dilekler iki kez "bitti" diye beyan edildi.

  Mevcut kosucular (t_y3 · t_y42 · isir · faz senaryolari) bir kapinin NOTUNUN
  sessizce kaybolmasini GORMEZ: hepsi hukum/exit seviyesinde olcer, kapi ciktisini
  SATIR SATIR karsilastirmaz. Bu arac tam o boslugu kapatir.

NE OLCER
  Determinist kurulmus N proje HALI icin `kapi` ve `kapi --siki` ciktisini ve cikis
  kodunu kaydeder; sonra ayni halleri yeniden kurup BIT-BIT karsilastirir.
  Tek bir satir kaybolur, eklenir ya da degisirse: FARK.

NORMALLESTIRME — AZ OLMALI, cunku her normalizasyon bir KORLUK ADAYIDIR
  Yalniz kacinilmaz gurultu silinir:
    <KOK>   proje koku (gecici dizin her kosumda farkli)
    <TARIH> ISO tarih   (2026-08-10 -> yarin baska)
    <GUN>   "N gun once"
    <SHA>   16+ hex dizisi
  Baska HICBIR SEY normallestirilmez. Surum satiri BILEREK normallestirilmez:
  bolme surumu degistirmemelidir, degistiriyorsa gorulmelidir.

  🔴 Normallestirmenin kendisi kor olabilir — bu yuzden `--kendini-sina` vardir:
  motora kasitli bir NOT DEGISIKLIGI enjekte eder ve aracin FARK demesini bekler.
  Demezse arac kordur ve exit 1 verir. Olcum araci once KENDINI kanitlar.

KULLANIM
  python3 faz0/altin_cikti.py --kaydet faz0/altin_kapi.json
  python3 faz0/altin_cikti.py --karsilastir faz0/altin_kapi.json
  python3 faz0/altin_cikti.py --kendini-sina

CIKIS KODLARI (proje sozlesmesi)
  0 fark yok / arac isirdi · 1 FARK VAR (ya da arac KOR) · 2 OLCULEMEDI · 3 ARAC KUSURU
"""
import argparse
import json
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
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78


class Kurulamadi(Exception):
    pass


# --------------------------------------------------------------- NORMALLESTIRME

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")
_RE_GUN = re.compile(r"\b\d+ gun once\b")
_RE_KOK_YOLU = re.compile(r"<KOK>([\\/][^\s:;,'\"]*)")


def normalize(metin, kok):
    """Kacinilmaz gurultuyu siler. HER EKLENEN DESEN BIR KORLUK ADAYIDIR:
    yeni desen eklemeden once `--kendini-sina` yeniden kosulmalidir.

    KALEM A (Onur kilidi 18 Agu 2026, H16-DUZELTME-BRIEF.md §1 — ENGELLEYICI):
    `kok` ile `os.path.realpath(kok)` AYRI dizgeler olabilir (Windows 8.3/uzun
    ad, macOS `/private` oneki, symlink'li TMPDIR — `realpath(kok) != kok`
    olan HER ortamda). `_kapi_h16`nin kacis mesaji sag yarisina
    `os.path.realpath(d)` basar; yalniz `kok` maskelenince sag yari CIPLAK
    kalir ve iki ayri kosum (farkli gecici taban) arasinda SAHTE FARK uretir.
    OLCULDU: CI (Windows runner) + Linux'ta symlink'li TMPDIR ile YENIDEN
    URETILDI. ⇒ `realpath(kok)` da maskelenir.

    🔴 SIRALAMA TUZAGI: `kok` ve `realpath(kok)` BIRBIRININ ONEKI olabilir
    (macOS `/var/folders/X` ve `/private/var/folders/X`). Kisa aday ONCE
    uygulanirsa UZUN adayin ICINI bozar (`/private/var/folders/X` ->
    `/private<KOK>` — YARIM maskeleme, <KOK> ayri bir yol parcasinin ICINDE
    kalir). ⇒ iki aday UZUNLUGA GORE AZALAN sirada uygulanir; esitlerse
    (Linux'ta olagan hal, symlink yoksa) ikinci gecis etkisizdir, zararsizdir.
    """
    try:
        _rk = os.path.realpath(kok)
    except OSError:
        _rk = kok
    m = metin
    for _aday in sorted({kok, _rk}, key=len, reverse=True):
        m = m.replace(_aday, "<KOK>")
        # Windows'ta ayni yol ters bolu ile de basilabilir.
        m = m.replace(_aday.replace("/", "\\"), "<KOK>")
    # HATA ve KESILME halleri kok ALTINDAKI yolu da basiyor
    # ("DOSYA UTF-8 DEGIL: <KOK>/arsiv/hafiza/_CIPA.json"). Windows'ta ayni yol
    # ters bolu ile gelir. Desen YALNIZ <KOK>'e YAPISIK yol belirtecine dokunur;
    # baska hicbir ters bolu degismez. IKI SINIRI VAR, ikisi de bilincli:
    #   (1) KORLUK ADAYI: bir urun degisikligi bir mesajdaki yol AYIRICISINI
    #       degistirseydi gizlenirdi. Hicbir kapinin ayirici uzerine hukum
    #       vermedigi VARSAYILIYOR — bu OLCULMEDI, raporda ilan edildi.
    #   (2) Yakalama BOSLUKTA durur: "<KOK>/a b\\c.md" ikinci ayiriciyi
    #       kanonlastirmaz. Kok ALTINDAKI adlari MOTOR uretiyor ve iclerinde
    #       bosluk yok; kokun kendisindeki bosluk zaten <KOK> ile siliniyor.
    # 🔴 DESEN BIR KEZ BOZUK YAZILDI: `[^\\s...]` yerine `[^\\\\s...]` gecmisti
    # (kacis karakteri fazlaydi) ve sinif "bosluk" degil "ters bolu + s harfi"
    # oluyordu; yakalama "arsiv"in s'sinde duruyor, yalniz ILK ayirici
    # kanonlasiyordu. Linux'ta desen zaten etkisiz oldugu icin hicbir yerel
    # olcum bunu gostermedi — bagimsiz denetci Windows ciktisini yeniden kurup
    # buldu (11 Agu 2026). YEREL YESIL, PLATFORMA OZGU BIR DESENI KANITLAMAZ.
    m = _RE_KOK_YOLU.sub(lambda x: "<KOK>" + x.group(1).replace("\\", "/"), m)
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    m = _RE_GUN.sub("<GUN> gun once", m)
    return m


# --------------------------------------------------------------- PROJE HALLERI
# Her hal DETERMINISTIK kurulur: ayni komutlar, ayni sirayla, ayni metinlerle.
# Metinlerde tarih/rastgelelik YOKTUR — olcum kendi gurultusunu uretmemelidir.

# --------------------------------------------------------------- BOZMALAR
# Bir proje halini KIRMIZI ya da KESILMIS yapan DETERMINISTIK bozmalar. Hepsi
# PROJE HALINDEN uretilir; motora KOD ENJEKTE EDILMEZ (altin kume urunun kendi
# davranisini kilitler, yamanin davranisini degil).
#
# 🔴 NEDEN GEREKLI (Faz C dersi, olculdu 11 Agu 2026): ozgun altin kumenin 10
# olcumunun 10'u exit 0'di. Bir kapi YARIDA kesilirse o ana kadarki bulgu
# KAYBOLABILIR ve hukum FAIL(2)/exit 1 -> FAIL(1)/exit 3'e doner. YALNIZ YESIL
# YOLU kapsayan bir esdegerlik kumesi bunu GORMESI MUMKUN DEGILDIR. Faz C'de
# tam bu oldu ve uc esdegerlik ayagi da kacirdi.
#
# `kapi` KOMUTUNUN DEGER KUMESI {0, 1, 3}. exit 2 ve 130 kumede YOKTUR, ama bu
# bir KAPSAM BOSLUGU DEGIL, olculen komutun URETMEDIGI kodlardir:
#   exit 2   motorun sozlesmesinde `oldur()`un verdigi TEMIZ KULLANIM/GIRDI hukmu
#            (`def oldur(msg, kod=2)`); cmd_kapi icinde hic `oldur()`/`sys.exit`
#            YOKTUR, her kapi istisnasi kapi_yalit ile 3 e doner. `oldur()` yolu
#            BASKA komutlarla olculur (`isir` taze projede exit 2 verir).
#   exit 130 KeyboardInterrupt — harici SINYAL gerektirir, proje HALI degildir.
# Ilk yazimda ikisi de "stderr yazilamiyor / zamanlamaya bagli" diye YANLIS
# gerekcelendirilmisti; bagimsiz denetci motorun kendi sozlesmesini gosterip
# curuttu (11 Agu 2026).

KURAL_SAYISI = 3          # olculdu: 1 kural bile exit 1 uretiyor; 3 okunur bir
                          # FAIL(3) verir ve referans dosyasini sismez tutar.


def _yol(kok, rel):
    return os.path.join(kok, *rel.split("/"))


def _boz_kural_yanlis_ev(kok, n):
    """Projenin kendi doktrinini ihlal eden satirlar: GERCEK kapi bulgusu (exit 1).
    Tarif boru_probu.py'den alindi (orada kanitlanmis KIRMIZI yapici)."""
    p = _yol(kok, "PROJE_HAFIZA.md")
    L = open(p, encoding="utf-8").read().split("\n")
    i = next((i for i, x in enumerate(L)
              if x.startswith("## GUNCEL") or "GUNCEL" in x or "G\u00dcNCEL" in x), 2)
    L = L[:i + 2] + ["- PAZARLIKSIZ: kural %d yanlis evde duruyor." % k
                     for k in range(n)] + L[i + 2:]
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))


def _boz_gecersiz_utf8(kok, rel):
    """Dosya UTF-8 DEGIL -> kapi YARIDA KESILIR. Mesaj metni platformdan
    BAGIMSIZDIR (motorun kendi cumlesi); yol <KOK> ile normallestirilir."""
    with open(_yol(kok, rel), "wb") as f:
        f.write(b"\xff\xfe gecersiz utf8 \xc3\x28")


def _boz_dizin_yap(kok, rel):
    """Duzenli dosya olmasi gereken yer DIZIN -> ayni kesilme SINIFI, FARKLI
    mesaj. Iki mesaji ayri ayri kilitlemek, sinifin tek cumleye daralmasini
    onler (ortusen tespit korlugu)."""
    p = _yol(kok, rel)
    os.remove(p)
    os.makedirs(p)


def _boz_kacis_link(kok, rel):
    """H16 (Onur kilidi 17 Agu 2026, YAPI_KAPISI_TASARIM.md §4.4): `rel`
    dizini PROJE DISINA baglanir (`arsiv/hafiza` icin: y9_h_kacis). Bugune
    kadar exit 3 (KESILME) idi; H16 ile exit 1 (olculmus kirmizi) olur —
    sozlesme degisikligi burada KALICI olarak kilitlenir.

    Harici hedef `kok + "_disari"` — `kok`in kendisini ONEK olarak tasir,
    boylece `normalize()`nin `m.replace(kok, "<KOK>")` cagrisi bu yolu da
    <KOK>_disari'ya indirger (AYRI bir desen EKLEMEDEN). Sabit-taban disinda
    (SIBLING olarak taban'in kendi altinda) bir hedef secilseydi, iki ayri
    `--kaydet`/`--karsilastir` kosumu FARKLI gecici taban kullandigi icin
    "gercek hedef yolu" metni HER SEFERINDE degisir ve bu kayit KALICI
    OLARAK sahte-FARK uretirdi (OLCULDU, yapi_kapisi_mutanti.py'nin ilk
    surumunde ayni sinif kusur cikti — DUZELTILDI, aynisi burada da
    onceden onlenir).

    Windows'ta `os.symlink` Gelistirici Modu/Yonetici ister (WinError 1314,
    OLCULDU); NTFS JUNCTION (`mklink /J`) istemez ve `kok_disina_mi`/
    `os.path.realpath` karsisinda symlink'le AYNI davranir (AYRICA
    dogrulandi, Python 3.12 `os.path.isjunction()` farkindaligi `shutil.
    rmtree`yi de guvenli kilar). POSIX'te duz `os.symlink` kullanilir."""
    harici = kok + "_disari"
    os.makedirs(harici, exist_ok=True)
    p = _yol(kok, rel)
    # `kur` az once bu yolu SIRADAN bir dizin olarak yaratti (bozma her zaman
    # taze bir proje uzerinde kosar) — link/junction OLASILIGI yok, bu yuzden
    # `os.path.isjunction` (yalniz 3.12+) GEREKMEZ, `shutil.rmtree` yeter.
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.lexists(p):
        os.remove(p)
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", p, harici],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode != 0:
            raise OSError(r.stderr.decode("utf-8", "replace"))
    else:
        os.symlink(harici, p, target_is_directory=True)


BOZMALAR = {
    "kural_yanlis_ev": _boz_kural_yanlis_ev,
    "gecersiz_utf8": _boz_gecersiz_utf8,
    "dizin_yap": _boz_dizin_yap,
    "kacis_link": _boz_kacis_link,
}

# --------------------------------------------------------------- PROJE HALLERI
# (ad, kurulum adimlari, gitli, bozmalar)
# Her hal DETERMINISTIK kurulur: ayni komutlar, ayni sirayla, ayni metinlerle.
# Metinlerde tarih/rastgelelik YOKTUR — olcum kendi gurultusunu uretmemelidir.

_NOT = ["not", "--konu=genel-durum", "--metin=altin cikti olcum notu"]

HALLER = [
    # --- YESIL YOLU (ozgun kume; exit 0) ---
    ("h1_taze", [], False, []),
    ("h2_fragman", [_NOT], False, []),
    ("h3_derlenmis", [_NOT, ["derle"]], False, []),
    ("h4_kararli", [_NOT, ["derle"], ["karar", "--baslik=Altin cikti kapisi"]], False, []),
    ("h5_gitli", [_NOT, ["derle"]], True, []),
    # >>> GENISLEME BASI — bu isaret faz0/altin_kapi_mutanti.py tarafindan
    # ANAHTAR olarak kullanilir (genislemeden ONCEKI kapsami yeniden uretmek
    # icin). ISARETI SILME ya da DEGISTIRME; mutant "isaret bulunamadi" der.
    # --- HATA YOLU: gercek kapi bulgusu, kesilme YOK (exit 1) ---
    ("h6_fail", [], False, [("kural_yanlis_ev", KURAL_SAYISI)]),
    # --- KESILME YOLU: bulgunun TAMAMI kesilme, HUKUM YOK (exit 3) ---
    ("h7_kesilme", [], False, [("gecersiz_utf8", "PROJE_HAFIZA.md")]),
    ("h8_kesilme_dizin", [], False, [("dizin_yap", "PROJE_HAFIZA.md")]),
    ("h9_kesilme_erken", [], False, [("gecersiz_utf8", "arsiv/hafiza/_CIPA.json")]),
    # --- KARISIK: gercek bulgu VE kesilme birlikte (exit 1) ---
    #     Faz C kusurunun TAM SEKLI. Kismi cikti dusuruldugunde bu iki kayit
    #     FAIL(2)/1 -> FAIL(1)/3 ve FAIL(5)/1 -> FAIL(1)/3 olur; yukaridaki
    #     bes yesil kayit ise HIC DEGISMEZ. Ayrimi tasiyan tek sey bunlardir.
    ("h10_karisik_az", [], False, [("kural_yanlis_ev", KURAL_SAYISI),
                                   ("gecersiz_utf8", "arsiv/hafiza/_KOVA.json")]),
    ("h11_karisik_cok", [], False, [("kural_yanlis_ev", KURAL_SAYISI),
                                    ("gecersiz_utf8", "KONULAR.md")]),
    # --- H16 SOZLESME DEGISIKLIGI: y.h (arsiv/hafiza) PROJE DISINA link ---
    # (Onur kilidi 17 Agu 2026, YAPI_KAPISI_TASARIM.md §4.4/kabul olcutu j).
    # BUGUNE KADAR bu hal exit 3 (KESILME) idi; H16 ile exit 1 (olculmus
    # kirmizi, bulgu [H16]) olur. Kayit YALNIZ ekleniyor (ADDITIVE) — mevcut
    # 11 kayit DEGISMEDI, bu 12.si.
    ("h12_h_kacis", [], False, [("kacis_link", "arsiv/hafiza")]),
    # <<< GENISLEME SONU
]


OLCUM_KOMUTLARI = [["kapi"], ["kapi", "--siki"]]


def kos(motor, arglar, kok, saniye=300):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        # DUZELTME-1: universal newline + acik kodlama. Cikplak `text=True` YETMEZ:
        # ust surecin varsayilan kodlamasi UTF-8 degilse (LC_ALL=C) UnicodeDecodeError
        # atar ve exit 1 = "FARK VAR" olarak raporlanir — Y-4 sinifi arac kusuru.
        # `-X utf8` de eklendi: kardes araclarin (t_y3 · t_y42 · fazC) hepsi kullaniyor.
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok=" + kok],
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def hal_kur(motor, taban, ad, adimlar, gitli, bozmalar=()):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    if gitli:
        try:
            subprocess.run(["git", "init", "-q", kok], check=True,
                           capture_output=True, timeout=60)
        except (OSError, subprocess.SubprocessError) as e:
            raise Kurulamadi("%s: git init basarisiz: %s" % (ad, e))
    rc, c = kos(motor, ["kur", "--ad", "ALTIN"], kok)
    if rc != 0:
        raise Kurulamadi("%s: kur exit=%s · %s" % (ad, rc, c[-200:]))
    for adim in adimlar:
        rc, c = kos(motor, adim, kok)
        if rc not in (0, 1):     # 1 = kapi kirmizisi; kurulum icin kabul
            raise Kurulamadi("%s: %s exit=%s · %s" % (ad, adim[0], rc, c[-200:]))
    # Bozmalar KURULUM BITTIKTEN SONRA, sirayla uygulanir. Sira onemlidir:
    # kural_yanlis_ev PROJE_HAFIZA.md'yi UTF-8 okur, gecersiz_utf8'ten SONRA
    # gelirse patlar. HALLER'de dogru sira YAZILIDIR; burada dogrulaniyor.
    for islem, arg in bozmalar:
        try:
            BOZMALAR[islem](kok, arg)
        except (KeyError, OSError, ValueError, UnicodeDecodeError) as e:
            raise Kurulamadi("%s: bozma '%s(%r)' uygulanamadi: %s: %s"
                             % (ad, islem, arg, type(e).__name__, e))
    return kok


def kume_uret(motor, taban):
    """Tum halleri kurar, olcum komutlarini kosar, NORMALLESTIRILMIS kume dondurur."""
    kume = []
    for ad, adimlar, gitli, bozmalar in HALLER:
        kok = hal_kur(motor, taban, ad, adimlar, gitli, bozmalar)
        for komut in OLCUM_KOMUTLARI:
            rc, c = kos(motor, komut, kok)
            if rc is None:
                raise Kurulamadi("%s / %s: zaman asimi" % (ad, " ".join(komut)))
            kume.append({"hal": ad, "komut": " ".join(komut), "exit": rc,
                         "cikti": normalize(c, kok)})
    return kume


_ZORUNLU_ALAN = ("hal", "komut", "exit", "cikti")


def _kume_sekli_dogrula(kume):
    """DUZELTME-3: referansin SEKLINI kapida sinar. Bir alan eksikse ya da tur
    yanlissa burada ARAC KUSURU (exit 3) olur; asagida ham traceback ile exit 1
    (= 'davranis DEGISTI') OLMAZ. Bir olcum aracinin en zararli hali sessiz
    kalmasi degil, KENDI kusurunu URUN regresyonu diye raporlamasidir."""
    if not isinstance(kume, list):
        raise TypeError("'kume' bir liste olmali, %s geldi" % type(kume).__name__)
    if not kume:
        raise ValueError("'kume' BOS — bos referans 'fark yok' demek DEGILDIR")
    for n, k in enumerate(kume):
        if not isinstance(k, dict):
            raise TypeError("kayit #%d bir nesne olmali, %s geldi"
                            % (n, type(k).__name__))
        for alan in _ZORUNLU_ALAN:
            if alan not in k:
                raise KeyError("kayit #%d: '%s' alani YOK" % (n, alan))
        if not isinstance(k["cikti"], str):
            raise TypeError("kayit #%d: 'cikti' metin olmali, %s geldi"
                            % (n, type(k["cikti"]).__name__))


def farklari_bul(altin, yeni):
    """Iki kumeyi ANAHTARLI karsilastirir. Kayip ve fazla kayit da FARKTIR —
    yalnizca ortak anahtarlari karsilastirmak, silinen bir olcumu gizler."""
    def anahtar(k):
        return (k["hal"], k["komut"])

    a = {anahtar(k): k for k in altin}
    y = {anahtar(k): k for k in yeni}
    farklar = []
    for k in sorted(set(a) | set(y)):
        if k not in y:
            farklar.append((k, "OLCUM KAYBOLDU (altin kumede var, yenide YOK)", "KAYIP"))
            continue
        if k not in a:
            farklar.append((k, "YENI OLCUM (altin kumede YOK)", "FAZLA"))
            continue
        if a[k]["exit"] != y[k]["exit"]:
            farklar.append((k, "EXIT DEGISTI: %s -> %s" % (a[k]["exit"], y[k]["exit"]), "EXIT"))
        if a[k]["cikti"] != y[k]["cikti"]:
            metin, adlandirildi = satir_farki(a[k]["cikti"], y[k]["cikti"])
            farklar.append((k, "CIKTI DEGISTI:\n" + metin,
                            "SATIR" if adlandirildi else "ADLANDIRILAMADI"))
    return farklar


# `splitlines()` esit liste veriyorsa ilk ayrisma ZORUNLU OLARAK bir SATIR SINIRI
# karakterindedir — bu yuzden tabloda YALNIZ onlar vardir. NBSP · BOM · SEKME ·
# BOSLUK · ZWSP satir siniri DEGILDIR: onlar satir listesini degistirir, dolayisiyla
# ADLANDIRILABILIR bir satir farki uretir ve buraya HIC ULASAMAZ. (Olculdu 11 Agu
# 2026: satir_farki("a b", "a\xa0b") -> adlandirildi=True.) Liste CPython'un
# str.splitlines() sinir kumesidir; bir uyesi eksik kalirsa hukum "?" olur.
_SINIR_ADI = {
    "\r": "SATIR SONU (CR)",
    "\x0b": "DIKEY SEKME (VT)",
    "\x0c": "SAYFA SONU (FF)",
    "\x1c": "DOSYA AYIRICI (FS)",
    "\x1d": "GRUP AYIRICI (GS)",
    "\x1e": "KAYIT AYIRICI (RS)",
    "\x85": "SONRAKI SATIR (NEL, U+0085)",
    "\u2028": "SATIR AYIRICI (U+2028)",
    "\u2029": "PARAGRAF AYIRICI (U+2029)",
}


def gorunmez_teshis(eski, yeni):
    """DUZELTME-2 destegi: iki metin farkli ama satir bazinda ADLANDIRILAMIYORSA
    kusur GORUNMEZ bir karakterdedir. Onu GIZLENEMEZ kilar: ilk ayrisma noktasinin
    repr penceresini ve sinif adini basar. 'Hedef engellemek degil, gizlenemez kilmak.'"""
    n = min(len(eski), len(yeni))
    i = 0
    while i < n and eski[i] == yeni[i]:
        i += 1
    bas = max(0, i - 24)
    if i >= len(eski) or i >= len(yeni):
        # Biri otekinin oneki. Satir listeleri esitken bu ancak SONDAKI bir satir
        # siniri karakteriyle olur (ornek: "a\n" ile "a").
        sinif = ("AYRISMA YOK (metinler esit — ARAC KUSURU adayi)"
                 if len(eski) == len(yeni)
                 else "SONDAKI SATIR SINIRI (uzunluk farki)")
    else:
        sinif = "?"
        for m in (eski, yeni):
            if m[i] in _SINIR_ADI:
                sinif = _SINIR_ADI[m[i]]
                break
    return ("      GORUNMEZ FARK · sinif: %s · ilk ayrisma indeksi: %d\n"
            "        ALTIN: %r\n        YENI : %r"
            % (sinif, i, eski[bas:i + 12], yeni[bas:i + 12]))


def satir_farki(eski, yeni):
    """(metin, adlandirildi) dondurur. adlandirildi=False ise fark SATIR duzeyinde
    gorunmuyor — bu bir URUN farki DEGIL, ARAC/ORTAM farki olabilir; cagiran onu
    ADLANDIRILAMADI olarak siniflar ve OLCULEMEDI hukmu verir."""
    e, y = eski.splitlines(), yeni.splitlines()
    out = []
    for i in range(max(len(e), len(y))):
        se = e[i] if i < len(e) else "<YOK>"
        sy = y[i] if i < len(y) else "<YOK>"
        if se != sy:
            out.append("      satir %d:\n        ALTIN: %s\n        YENI : %s" % (i + 1, se, sy))
    if out:
        # SESSIZ KAP YOK: kesme oldugunda KAC satirin gizlendigi BASILIR. 202
        # bulgulu bir hal kolayca 12'yi asar; sessiz kesme "hepsi bu" diye
        # okunur. Projenin kendi kurali: bir sinir konuluyorsa NE DUSTUGU yazilir.
        kesik = len(out) - 12
        if kesik > 0:
            return ("\n".join(out[:12])
                    + "\n      ... %d SATIR FARKI DAHA GIZLENDI (toplam %d); "
                      "tam liste icin altin kumeyi elle karsilastir."
                      % (kesik, len(out))), True
        return "\n".join(out), True
    return gorunmez_teshis(eski, yeni), False


# --------------------------------------------------------------- KENDINI SINA
# Arac once KENDINI kanitlar: motora kasitli bir NOT DEGISIKLIGI enjekte edilir.
# Bu bir URUN kusuru degildir; aracin GORME YETISINI olcer.

SABOTAJ_ESKI = 'N.append("H13: %d seri tanimli" % len(seriler))'
SABOTAJ_YENI = 'N.append("H13: %d seri tanimlandi" % len(seriler))'


def sabotajli_motor(motor, hedef_dizin):
    metin = open(motor, encoding="utf-8").read()
    n = metin.count(SABOTAJ_ESKI)
    if n != 1:
        raise Kurulamadi(
            "kendini-sina: sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse "
            "SABOTAJ DA DEGISMELIDIR — aksi halde arac KENDINI SINAMIYOR demektir." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(SABOTAJ_ESKI, SABOTAJ_YENI, 1))
    return p


def kendini_sina(motor):
    print(CIZGI)
    print("KENDINI SINA — arac bir NOT DEGISIKLIGINI goruyor mu?")
    print("  sabotaj: 'H13: %d seri tanimli' -> 'H13: %d seri tanimlandi'")
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="altin_sina_")
    try:
        altin = kume_uret(motor, os.path.join(taban, "temiz"))
        sab_dizin = os.path.join(taban, "sabotajli_motor")
        os.makedirs(sab_dizin)
        sab = sabotajli_motor(motor, sab_dizin)
        yeni = kume_uret(sab, os.path.join(taban, "sabotajli"))
    except Kurulamadi as e:
        print("OLCULEMEDI: %s" % e)
        return 2
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    farklar = farklari_bul(altin, yeni)
    ilgili = [f for f in farklar if "tanimlandi" in f[1] or "tanimli" in f[1]]
    print("  toplam fark kaydi : %d" % len(farklar))
    print("  H13 satirini yakalayan kayit: %d" % len(ilgili))
    if not ilgili:
        print()
        print("KOR: arac kasitli NOT DEGISIKLIGINI GORMEDI.")
        print("  Muhtemel sebep: normallestirme cok agresif ya da olcum halleri")
        print("  o kapiya hic ugramiyor. Bu bir URUN kusuru DEGIL, ARAC korlugudur.")
        return 1
    print()
    print("ISIRDI: arac tek satirlik bir not degisikligini yakaladi.")
    return 0


# --------------------------------------------------------------- ANA

def main():
    ap = argparse.ArgumentParser(description="kapi ciktisi esdegerlik kapisi")
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--kaydet", metavar="DOSYA", help="altin kumeyi bu dosyaya yaz")
    g.add_argument("--karsilastir", metavar="DOSYA", help="altin kumeyle karsilastir")
    g.add_argument("--kendini-sina", action="store_true",
                   dest="kendini_sina", help="arac gorebiliyor mu (SABOTAJ)")
    a = ap.parse_args()

    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2

    if a.kendini_sina:
        return kendini_sina(motor)

    taban = tempfile.mkdtemp(prefix="altin_")
    try:
        kume = kume_uret(motor, taban)
    except Kurulamadi as e:
        print("OLCULEMEDI: %s" % e)
        return 2
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    if a.kaydet:
        with open(a.kaydet, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"kume": kume}, f, ensure_ascii=False, indent=2)
        print("ALTIN KUME yazildi: %s  (%d olcum)" % (a.kaydet, len(kume)))
        print("  NOT: bu dosya bir KANITTIR. Bolme sonrasi UZERINE YAZILMAZ;")
        print("       --karsilastir ile SINANIR.")
        return 0

    try:
        altin = json.load(open(a.karsilastir, encoding="utf-8"))["kume"]
        _kume_sekli_dogrula(altin)
    except (OSError, ValueError, KeyError, TypeError) as e:
        # DUZELTME-3: SEKIL denetimi. Once yalniz json.load sarilmisti; bozuk ya da
        # kesik bir referans dosyasi farklari_bul icinde KeyError/TypeError atip HAM
        # TRACEBACK ile exit 1 veriyordu — yani ARAC KUSURU "davranis DEGISTI" (URUN
        # hukmu) olarak okunuyordu. Bu, duzeltme-2'nin kapattigi kusurun BASKA BIR
        # KAPIDAN geri gelmesidir; iki kapi ayni tezi tasir, ikisi de kapanir.
        print("ARAC KUSURU: altin kume okunamadi ya da SEKLI BOZUK (%s): %s: %s"
              % (a.karsilastir, type(e).__name__, e))
        print("  Bu bir URUN hukmu DEGILDIR. Referans dosyasi --kaydet ile")
        print("  yeniden uretilir; onceki dosya BIR KANITTIR, ustune yazilmadan once")
        print("  neden bozuldugu ayrilir (kesik indirme? birlestirme catismasi?).")
        return 3

    farklar = farklari_bul(altin, kume)
    print(CIZGI)
    print("ALTIN CIKTI KARSILASTIRMASI")
    print("  altin kume : %s (%d olcum)" % (a.karsilastir, len(altin)))
    print("  bu kosum   : %d olcum" % len(kume))
    print(CIZGI)
    if not farklar:
        print("FARK YOK — kapi ciktisi ve cikis kodlari BIT-BIT ayni.")
        print("  (Normallestirilen: <KOK> · <TARIH> · <GUN> · <SHA>. Baska hicbir sey.)")
        return 0
    for (hal, komut), aciklama, _sinif in farklar:
        print("  FARK  %-14s %-12s | %s" % (hal, komut, aciklama))
    print(CIZGI)
    # DUZELTME-2: satir duzeyinde ADLANDIRILAMAYAN fark bir URUN hukmu DEGILDIR.
    # Eski surum bunu "davranis DEGISTI" (exit 1) diye raporluyordu; oysa sebep
    # aracin/ortamin kendisi olabilir (satir sonu ve akrabalari). Y-4 sinifi:
    # "olcemedigini ARAC KUSURU diye mi raporluyor?" — evet demeli, 1 dememeli.
    adsiz = [f for f in farklar if f[2] == "ADLANDIRILAMADI"]
    if adsiz:
        print("OLCULEMEDI: %d farkin %d'i satir duzeyinde ADLANDIRILAMADI." % (len(farklar), len(adsiz)))
        print("  Bu bir URUN regresyonu DEGIL diye okunmaz; ama 'davranis DEGISTI'")
        print("  diye de okunmaz. Gorunmez karakter sinifi yukarida repr ile basildi.")
        print("  Ilk bakilacak yer: cocuk surecin satir sonu kipi ve altin kumenin")
        print("  kaydedildigi platform. Once o AYRILIR, sonra urun hukmu verilir.")
        return 2
    print("SONUC: %d FARK — davranis DEGISTI." % len(farklar))
    return 1


if __name__ == "__main__":
    sys.exit(main())

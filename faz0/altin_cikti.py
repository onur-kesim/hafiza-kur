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


def normalize(metin, kok):
    """Kacinilmaz gurultuyu siler. HER EKLENEN DESEN BIR KORLUK ADAYIDIR:
    yeni desen eklemeden once `--kendini-sina` yeniden kosulmalidir."""
    m = metin.replace(kok, "<KOK>")
    # Windows'ta ayni yol ters bolu ile de basilabilir.
    m = m.replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    m = _RE_GUN.sub("<GUN> gun once", m)
    return m


# --------------------------------------------------------------- PROJE HALLERI
# Her hal DETERMINISTIK kurulur: ayni komutlar, ayni sirayla, ayni metinlerle.
# Metinlerde tarih/rastgelelik YOKTUR — olcum kendi gurultusunu uretmemelidir.

HALLER = [
    ("h1_taze", [], False),
    ("h2_fragman", [["not", "--konu=genel-durum", "--metin=altin cikti olcum notu"]], False),
    ("h3_derlenmis", [["not", "--konu=genel-durum", "--metin=altin cikti olcum notu"],
                      ["derle"]], False),
    ("h4_kararli", [["not", "--konu=genel-durum", "--metin=altin cikti olcum notu"],
                    ["derle"],
                    ["karar", "--baslik=Altin cikti kapisi"]], False),
    ("h5_gitli", [["not", "--konu=genel-durum", "--metin=altin cikti olcum notu"],
                  ["derle"]], True),
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


def hal_kur(motor, taban, ad, adimlar, gitli):
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
    return kok


def kume_uret(motor, taban):
    """Tum halleri kurar, olcum komutlarini kosar, NORMALLESTIRILMIS kume dondurur."""
    kume = []
    for ad, adimlar, gitli in HALLER:
        kok = hal_kur(motor, taban, ad, adimlar, gitli)
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
        return "\n".join(out[:12]), True
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

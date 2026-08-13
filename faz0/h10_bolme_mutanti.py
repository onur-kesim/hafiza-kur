#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H10 ALT-BOLME MUTANTI — `_kapi_h10`un dort parcasi arasindaki kenarlar OLCULUYOR mu?

h1/h14/h4 mutantlariyla ayni sozlesme. H10'un farki: parcalar SAF DEGILDIR
(dordu de hukum basar), dolayisiyla burada olculen yalniz VERI kenarlari degil,
HUKUM KANALLARIDIR da — bir parcaya F ya da O yerine bos liste verildiginde
bulgunun sessizce kaybolup kaybolmadigi.

IKI SUTUN: KENDI KUMESI · ALTIN KUME
HAL KAPISI: temiz kolda her halin ciktisinda bir H10 satiri BULUNMALIDIR.

CIKIS KODU  0 her mutant ISIRDI · 1 en az biri KACTI · 2 OLCULEMEDI
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
ALTIN_ARAC = os.path.join(KOK, "faz0", "altin_cikti.py")
ALTIN_KUME = os.path.join(KOK, "faz0", "altin_kapi.json")
CIZGI = "-" * 84

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")
_RE_GUN = re.compile(r"\b\d+ gun once\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun once", m)


# --------------------------------------------------------------- PROJE HALLERI
#   h_temiz      dokunulmamis proje            -> yalniz "N blok / M ayrik konu" notu
#   h_cift       ayni konuda iki canli blok    -> KONU TEKILLIGI KIRIK
#   h_cit        kapanmamis kod citi           -> KAPANMAMIS KOD CITI
#   h_girintili  girintili blok isareti        -> GIRINTILI blok isareti
#   h_gizli      cit icinde YENI konulu blok   -> O.append (OLCULEMEDI hukmu)
#   h_cakisan    cit icinde CANLIDAKI konu     -> gizli/canli konu cakismasi
#   h_bozuk      oksuz kapanis isareti         -> BOZUK BLOK YAPISI
#   h_tanimsiz   KONULAR.md'de olmayan konu    -> tanimsiz konu
#   h_cift_cit   cift konu + kapanmamis cit     -> IKI parca da F'e yazar
#                (SIRA mutanti ancak boyle olculebilir: ayni kanalda iki yazar)
HALLER = [
    ("h_temiz", "temiz"), ("h_cift", "cift"), ("h_cit", "cit"),
    ("h_girintili", "girintili"), ("h_gizli", "gizli"), ("h_cakisan", "cakisan"),
    ("h_bozuk", "bozuk"), ("h_tanimsiz", "tanimsiz"), ("h_cift_cit", "cift_cit"),
]

OLCUM_KOMUTLARI = [["kapi"]]
HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h10 mutanti icin ilk kayit"],
            ["derle"]]

BLOK = '<!-- blok konu="%s" guncel="2026-01-01" kaynak="-" -->\n%s\n<!-- /blok -->'


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _ekle(kok, metin):
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    if not os.path.isfile(p):
        raise Kurulamadi("canli hafiza yok")
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write("\n" + metin + "\n")


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H10MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))
    if tip == "temiz":
        pass
    elif tip == "cift":
        _ekle(kok, BLOK % ("genel-durum", "Ayni konuda IKINCI canli blok."))
    elif tip == "cit":
        _ekle(kok, "```\nkapanmamis cit — dosyanin sonuna kadar uzuyor")
    elif tip == "girintili":
        _ekle(kok, '  <!-- blok konu="sonraki-adim" guncel="2026-01-01" kaynak="-" -->\n'
                   '  girintili isaret — hicbir olcume girmez\n  <!-- /blok -->')
    elif tip == "gizli":
        _ekle(kok, "```\n" + (BLOK % ("belgelenmis-ornek", "cit icinde ORNEK blok.")) + "\n```")
    elif tip == "cakisan":
        _ekle(kok, "```\n" + (BLOK % ("genel-durum", "cit icinde CANLIDAKI konu.")) + "\n```")
    elif tip == "bozuk":
        _ekle(kok, "<!-- /blok -->")
    elif tip == "tanimsiz":
        _ekle(kok, BLOK % ("uydurma-konu-x", "KONULAR.md'de tanimsiz konu."))
    elif tip == "cift_cit":
        _ekle(kok, BLOK % ("genel-durum", "Ayni konuda IKINCI blok."))
        _ekle(kok, "```\nkapanmamis cit")
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


def haller_kur(motor_temiz, taban):
    return {ad: hal_kur(motor_temiz, ad, tip, taban) for ad, tip in HALLER}


def kume_olc(motor, kokler, hedef_taban):
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        for komut in OLCUM_KOMUTLARI:
            rc, c = kos(motor, komut, kok)
            out[(ad, " ".join(komut))] = (rc, normalize(c, kok))
    return out


def farklari_bul(a, b):
    farklar = []
    for anahtar in sorted(set(a) | set(b)):
        x, y = a.get(anahtar), b.get(anahtar)
        if x is None or y is None:
            farklar.append((anahtar, "olcum EKSIK"))
        elif x[0] != y[0]:
            farklar.append((anahtar, "exit %s -> %s" % (x[0], y[0])))
        elif x[1] != y[1]:
            farklar.append((anahtar, "cikti degisti"))
    return farklar


def _h10_satiri(cikti):
    satirlar = [s.strip() for s in cikti.split("\n")]
    for d in satirlar:
        if d.startswith("[H10]"):
            return d
    for d in satirlar:
        if "H10:" in d[:12]:
            return d
    return None


# --------------------------------------------------------------------- MUTANTLAR
CAGRI_TEK = "    bl, say = _h10_tekillik(F, y)"
CAGRI_CIT = "    _ham = _h10_cit(F, O, y)"
CAGRI_YAPI = "    _h10_yapi(F, _ham)"
CAGRI_SOZ = "    _h10_sozluk(F, y, say)"
DONUS = "    _h10_sozluk(F, y, say)\n    return bl"
N_SATIRI = '    N.append("H10: %d blok / %d ayrik konu" % (len(bl), len(say)))'

MUTANTLAR = [
    ("M-H10a KENAR say", "TEKILLIK -> SOZLUK: konu kumesi kopar (tanimsiz konu gorunmez)",
     [(CAGRI_SOZ, "    _h10_sozluk(F, y, {})")]),
    ("M-H10b KENAR _ham", "CIT -> YAPI: ham satirlar kopar (bozuk blok yapisi gorunmez)",
     [(CAGRI_YAPI, "    _h10_yapi(F, [])")]),
    ("M-H10c KANAL O", "CIT'in O kanali kopar — OLCULEMEDI hukmu sessizce kaybolur",
     [(CAGRI_CIT, "    _ham = _h10_cit(F, [], y)")]),
    ("M-H10d KANAL F", "TEKILLIK'in F kanali kopar — bulgular sessizce kaybolur",
     [(CAGRI_TEK, "    bl, say = _h10_tekillik([], y)")]),
    # 🔴 ILK SIRA MUTANTI KACTI VE DEGISTIRILDI (13 Agu 2026, olculdu):
    # `_h10_yapi` (F kanali) ile `N.append` (N kanali) yer degistirince cikti
    # DEGISMIYOR — cunku bulgular ve notlar AYRI BOLUMLERDE basilir; sira yalniz
    # AYNI KANAL icinde gozlenebilir. O mutant ESDEGERDI, kume kor degildi.
    # Esdeger bir mutanti "kacti" diye raporlamak SAHTE KIRMIZIDIR (Y-4 dersi),
    # bu yuzden mutant AYNI KANALA yazan iki parcaya tasindi ve kumeye `h_cift_cit`
    # hali eklendi (tekillik F'e yazar VE cit F'e yazar).
    ("M-H10e SIRA", "TEKILLIK ile CIT yer degistirir — ayni kanalda (F) sira sozlesmedir",
     [(CAGRI_TEK + "\n" + CAGRI_CIT, CAGRI_CIT + "\n" + CAGRI_TEK)]),
    ("M-H10f DONUS bl", "kapinin DONUS degeri kopar — H12 blok listesini kaybeder (kapilar arasi kenar)",
     [(DONUS, "    _h10_sozluk(F, y, say)\n    return []")]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:55]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def altin_isiriyor_mu(sabotajli):
    if not (os.path.isfile(ALTIN_ARAC) and os.path.isfile(ALTIN_KUME)):
        return None, "altin arac/kume yok"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", ALTIN_ARAC,
                            "--motor", sabotajli, "--karsilastir", ALTIN_KUME],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900)
    except Exception as e:
        return None, "kosulamadi: %s" % e
    c = (r.stdout or "") + (r.stderr or "")
    return (False, "FARK YOK") if "FARK YOK" in c else (True, "fark VAR")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    ap.add_argument("--altin-atla", action="store_true")
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz.")
        return 2

    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("H10 ALT-BOLME MUTANTI — parcalar arasi kenarlar ve HUKUM KANALLARI")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h10mut_")
    try:
        try:
            kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
            referans = kume_olc(motor, kokler, os.path.join(taban, "ref"))
            ikinci = kume_olc(motor, kokler, os.path.join(taban, "ref2"))
        except Kurulamadi as e:
            print("OLCULEMEDI: referans/temiz kol kurulamadi: %s" % e)
            return 2
        tk = farklari_bul(referans, ikinci)
        print("  TEMIZ KOL (ayni motor 2 kez)   %s"
              % ("FARK YOK" if not tk else "FARK VAR: %s" % tk[:3]))
        if tk:
            print("\nOLCULEMEDI: duzenek determinist degil.")
            return 2
        imzalar = {ad: referans[(ad, "kapi")] for ad, _ in HALLER}
        atessiz = [ad for ad, _ in HALLER if _h10_satiri(imzalar[ad][1]) is None]
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            print("     %-12s exit %s · %s" % (ad, e, (_h10_satiri(c) or "(H10 SATIRI YOK)")[:60]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H10'u hic ateslemedi: %s" % ", ".join(atessiz))
            return 2
        if tekil < 2:
            print("\nOLCULEMEDI: haller ayrismiyor — kume korlestirici.")
            return 2
        print(CIZGI)
        print("  %-22s %-11s %-26s %s" % ("mutant", "KENDI", "iz", "ALTIN KUME"))
        print(CIZGI)

        isirdi, kacti, olculemedi, altin_kor = [], [], [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yeni = kume_olc(sab, kokler, os.path.join(d, "hal"))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-22s OLCULEMEDI  %s" % (ad, e))
                continue
            farklar = farklari_bul(referans, yeni)
            if a.altin_atla:
                alt_txt = "(atlandi)"
            else:
                alt, sebep = altin_isiriyor_mu(sab)
                alt_txt = {True: "ISIRDI", False: "KOR (FARK YOK)", None: "OLCULEMEDI"}[alt]
                if alt is False:
                    altin_kor.append(ad)
                if alt is None:
                    alt_txt += " · " + sebep
            if farklar:
                isirdi.append(ad)
                izler = sorted({k[0] for k, _ in farklar})
                print("  +  %-22s ISIRDI      %-26s %s"
                      % (ad, "%d olcum: %s" % (len(farklar), ",".join(h[2:] for h in izler)[:14]),
                         alt_txt))
            else:
                kacti.append(ad)
                print("  !  %-22s KACTI       %-26s %s" % (ad, "-", alt_txt))
                print("     -> kenar BU KUMEDE KOR: %s" % aciklama)
            sys.stdout.flush()
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if not a.altin_atla:
        if altin_kor:
            print("  ALTIN KUME %d mutanta KOR: %s" % (len(altin_kor), ", ".join(altin_kor)))
        else:
            print("  ALTIN KUME her mutanti gordu — bu mutant KANIT olarak kalir.")
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kumenin KOR oldugu kenar.")
        return 1
    print("  H10 bolmesinin her kenari ve her hukum kanali olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H4 ALT-BOLME MUTANTI — `_kapi_h4`un dort parcasi arasindaki kenarlar OLCULUYOR mu?

`h14_bolme_mutanti.py` ile ayni sozlesme ve ayni gerekce. H4 icin bosluk sunda:
altin kumenin halleri OLU BAGLANTI icermez (taze kurulmus projelerde canli
hafizada backtick'li yol beyani yoktur), dolayisiyla H4 orada cogunlukla HIC
konusmaz. Konusmayan bir kapinin kenarlari "FARK YOK" ile kanitlanamaz.

IKI SUTUN: KENDI KUMESI · ALTIN KUME  (bkz. h1/h14 mutantlari)
HAL KAPISI: temiz kolda her halin ciktisinda bir H4 satiri BULUNMALIDIR.

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
#   h_olu       backtick'li yol hicbir yerde yok            -> OLU BAGLANTI
#   h_tasinmis  ayni ad arsiv altinda duruyor               -> TASINMIS notu (fail DEGIL)
#   h_ayni_ad   ayni ad var ama baglam tutmuyor             -> OLU + "yol tutmuyor"
#   h_kirpma    12 olu baglanti                             -> ekranda kirpma satiri
#   h_tas_kirp  7 tasinmis                                  -> tasinmis kirpma notu
#   h_markdown  []() bicimli olu baglanti                   -> ikinci tarama dongusu
#   h_turkce    TURKCE adli olu baglanti (Fable Bulgu 4)    -> UNICODE regex dali
HALLER = [
    ("h_olu", "olu"),
    ("h_tasinmis", "tasinmis"),
    ("h_ayni_ad", "ayni_ad"),
    ("h_kirpma", "kirpma"),
    ("h_tas_kirp", "tas_kirp"),
    ("h_markdown", "markdown"),
    ("h_turkce", "turkce"),
]

OLCUM_KOMUTLARI = [["kapi"]]
HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h4 mutanti icin ilk kayit"],
            ["derle"]]


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _ekle(kok, satirlar):
    """Canli hafizaya satir ekler. H4 YALNIZ canli dosyayi tarar."""
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    if not os.path.isfile(p):
        raise Kurulamadi("canli hafiza yok")
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write("\n" + "\n".join(satirlar) + "\n")


def _dosya(kok, rel, icerik="# h4 mutanti\n"):
    p = os.path.join(kok, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(icerik)


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H4MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))

    if tip == "olu":
        _ekle(kok, ["Kaynak dosya: `belgeler/yok.md` (hicbir yerde yok)."])
    elif tip == "tasinmis":
        _dosya(kok, "arsiv/belgeler/rapor.md")
        _ekle(kok, ["Rapor burada: `belgeler/rapor.md`."])
    elif tip == "ayni_ad":
        _dosya(kok, "baska/rapor2.md")
        _ekle(kok, ["Rapor burada: `belgeler/rapor2.md`."])
    elif tip == "kirpma":
        _ekle(kok, ["Kayit %d: `belgeler/yok%02d.md`" % (i, i) for i in range(1, 13)])
    elif tip == "tas_kirp":
        for i in range(1, 8):
            _dosya(kok, "arsiv/belgeler/tas%02d.md" % i)
        _ekle(kok, ["Tasinan %d: `belgeler/tas%02d.md`" % (i, i) for i in range(1, 8)])
    elif tip == "markdown":
        _ekle(kok, ["Ayrinti [su belgede](belgeler/md_yok.md) duruyor."])
    elif tip == "turkce":
        # 🔴 Fable Bulgu 4: regex ASCII oldugunda TURKCE adli olu baglanti SESSIZCE
        # atlaniyordu. Ad yalniz METINDE gecer; diske Turkce diyakritikli dosya
        # YAZILMAZ (proje kirmizi cizgisi: macOS NFC/NFD cipayi kirar).
        _ekle(kok, ["Musteri dosyasi: `belgeler/m\u00fc\u015fteri_\u00f6zeti.md` ve `belgeler/olcum.md`."])
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


def haller_kur(motor_temiz, taban):
    """Haller TEMIZ motorla BIR KEZ kurulur (h1 turunun dersi)."""
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


def _h4_satiri(cikti):
    satirlar = [s.strip() for s in cikti.split("\n")]
    for d in satirlar:
        if d.startswith("[H4]"):
            return d
    for d in satirlar:
        if "H4:" in d[:12]:
            return d
    return None


# --------------------------------------------------------------------- MUTANTLAR
CAGRI_ADAY = "    aday = _h4_adaylar(metin)"
CAGRI_HAVUZ = "        havuz = _h4_havuz(kok)"
CAGRI_SINIF = "        olu, tasinmis = _h4_siniflandir(eksik, havuz)"
CAGRI_HUKUM = "        _h4_hukum(F, N, olu, tasinmis)"
KORUMA_EKSIK = "    if eksik:\n        # Tasinmis mi"   # 3 kez gecen tek satir DEGIL: yorumla capalanir

MUTANTLAR = [
    ("M-H4a KENAR metin", "EBEVEYN -> ADAYLAR: canli metin kenari kopar (bos dizge)",
     [(CAGRI_ADAY, "    aday = _h4_adaylar(\"\")")]),
    ("M-H4b KENAR kok", "EBEVEYN -> HAVUZ: kok kenari kopar (havuz bos kalir)",
     [(CAGRI_HAVUZ, "        havuz = _h4_havuz(os.path.join(kok, '_yok_'))")]),
    ("M-H4c KENAR havuz", "HAVUZ -> SINIFLANDIRMA: havuz kopar (tasinmis HEP olu gorunur)",
     [(CAGRI_SINIF, "        olu, tasinmis = _h4_siniflandir(eksik, {})")]),
    ("M-H4d KENAR eksik", "EBEVEYN -> SINIFLANDIRMA: eksik listesi kopar (bos liste)",
     [(CAGRI_SINIF, "        olu, tasinmis = _h4_siniflandir([], havuz)")]),
    ("M-H4e KENAR olu", "SINIFLANDIRMA -> HUKUM: olu listesi kopar — FAIL'ler sessizce kaybolur",
     [(CAGRI_HUKUM, "        _h4_hukum(F, N, [], tasinmis)")]),
    ("M-H4f KORUMA SOKME", "'if eksik:' dali silinir — kapi hic konusmaz",
     [(KORUMA_EKSIK, "    if False:\n        # Tasinmis mi")]),
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
    if "FARK YOK" in c:
        return False, "FARK YOK"
    return True, "fark VAR"


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
    print("H4 ALT-BOLME MUTANTI — parcalar arasi kenarlar OLCULUYOR mu?")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h4mut_")
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
            print("\nOLCULEMEDI: duzenek determinist degil — mutant hukmu ANLAMSIZ.")
            return 2
        print("  referans olcum sayisi          %d" % len(referans))
        imzalar = {ad: referans[(ad, "kapi")] for ad, _ in HALLER}
        atessiz = [ad for ad, _ in HALLER if _h4_satiri(imzalar[ad][1]) is None]
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            print("     %-12s exit %s · %s" % (ad, e, (_h4_satiri(c) or "(H4 SATIRI YOK)")[:62]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H4'u hic ateslemedi: %s" % ", ".join(atessiz))
            return 2
        if tekil < 2:
            print("\nOLCULEMEDI: haller birbirinden ayrismiyor — kume korlestirici.")
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
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kenar saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kumenin KOR oldugu kenar.")
        return 1
    print("  H4 bolmesinin her kenari olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

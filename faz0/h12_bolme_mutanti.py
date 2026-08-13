#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H12 ALT-BOLME MUTANTI — kenarlar ve HUKUM KANALLARI olculuyor mu?

h1/h14/h4/h10 mutantlariyla ayni sozlesme. H12'nin ozelligi: bolmede kalibin iki
ucu bir arada — `_h12_tazelik` UC kanali birden kullanir (F·N·O), `_h12_sapma_haritasi`
HIC hukum basmaz (saf). Bu yuzden mutantlar hem VERI kenarlarini hem UC KANALI
tek tek koparir.

HAL KAPISI: temiz kolda her halin ciktisinda bir H12 satiri BULUNMALIDIR.
CIKIS KODU  0 hepsi ISIRDI · 1 en az biri KACTI · 2 OLCULEMEDI
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
_RE_GUN = re.compile(r"\b\d+ gun\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun", m)


# --------------------------------------------------------------- PROJE HALLERI
#   h_temiz       taze proje                      -> "son guncelleme N gun once" NOTU (N)
#   h_bayat       tarih bayatlik tavaninin otesi  -> FAIL (F)
#   h_gelecek     tarih GELECEKTE                 -> FAIL (F) + t_son None'a duser
#   h_cozulemez   tarih cozulemiyor               -> O.append (OLCULEMEDI kanali)
#   h_satirsiz    'Son guncelleme' satiri YOK     -> FAIL (F)
#   h_canli_bayat blok eski, fragman yeni         -> CANLI BAYAT (sapma hukmu)
#   h_bekleyen    derlenmemis fragman             -> "N fragman DERLENMEYI bekliyor" (N)
HALLER = [
    ("h_temiz", "temiz"), ("h_bayat", "bayat"), ("h_gelecek", "gelecek"),
    ("h_cozulemez", "cozulemez"), ("h_satirsiz", "satirsiz"),
    ("h_canli_bayat", "canli_bayat"), ("h_bekleyen", "bekleyen"),
]

OLCUM_KOMUTLARI = [["kapi"]]


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _canli(kok):
    return os.path.join(kok, "PROJE_HAFIZA.md")


def _tarih_degistir(kok, yeni):
    """'Son guncelleme' satirindaki tarihi degistirir (canli + snapshot)."""
    hedefler = [_canli(kok), os.path.join(kok, "arsiv", "hafiza", "_KAYNAK.md")]
    yazildi = 0
    for p in hedefler:
        if not os.path.isfile(p):
            continue
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r"(Son g[uü]ncelleme:\s*)(\d{4}-\d{2}-\d{2})", r"\g<1>" + yeni, s, count=1)
        if s2 != s:
            open(p, "w", encoding="utf-8", newline="").write(s2)
            yazildi += 1
    if not yazildi:
        raise Kurulamadi("'Son guncelleme' satiri bulunamadi")


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H12MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    rc, c = kos(motor, ["not", "--konu=genel-durum", "--tur=durum",
                        "--metin=h12 mutanti icin ilk kayit"], kok)
    if rc != 0:
        raise Kurulamadi("not basarisiz (%s)" % ad)
    if tip != "bekleyen":                    # bekleyen halinde fragman DERLENMEZ
        rc, c = kos(motor, ["derle"], kok)
        if rc != 0:
            raise Kurulamadi("derle basarisiz (%s)" % ad)

    if tip in ("temiz", "bekleyen"):
        pass
    elif tip == "bayat":
        _tarih_degistir(kok, "2026-01-01")
    elif tip == "gelecek":
        _tarih_degistir(kok, "2099-01-01")
    elif tip == "cozulemez":
        p = _canli(kok)
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r"(Son g[uü]ncelleme:\s*)(\d{4}-\d{2}-\d{2})", r"\g<1>yakinda", s, count=1)
        if s2 == s:
            raise Kurulamadi("tarih satiri bulunamadi")
        open(p, "w", encoding="utf-8", newline="").write(s2)
    elif tip == "satirsiz":
        p = _canli(kok)
        s = [x for x in open(p, encoding="utf-8").read().split("\n")
             if "Son guncelleme" not in x and "Son güncelleme" not in x]
        open(p, "w", encoding="utf-8", newline="").write("\n".join(s))
    elif tip == "canli_bayat":
        # Blok BASLIGINDAKI `guncel` eskiye cekilir; arsivlenmis fragman BUGUN
        # tarihli oldugu icin sapma hukmu ateslenir.
        p = _canli(kok)
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r'(<!--\s*blok konu="genel-durum"[^>]*?guncel=")(\d{4}-\d{2}-\d{2})',
                    r"\g<1>2026-01-01", s, count=1)
        if s2 == s:
            raise Kurulamadi("genel-durum blok basligi bulunamadi")
        open(p, "w", encoding="utf-8", newline="").write(s2)
    else:
        raise Kurulamadi("bilinmeyen hal: %s" % tip)
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


def _h12_satiri(cikti):
    satirlar = [s.strip() for s in cikti.split("\n")]
    for d in satirlar:
        if d.startswith("[H12]"):
            return d
    for d in satirlar:
        if "H12:" in d[:12]:
            return d
    return None


# --------------------------------------------------------------------- MUTANTLAR
CAGRI_TAZ = "    t_son = _h12_tazelik(F, N, O, rc, y)"
CAGRI_HAR = "    en_yeni = _h12_sapma_haritasi(y, ks)"
CAGRI_HUK = "    _h12_sapma_hukmu(F, N, y, bl, en_yeni)"
DONUS = "    _h12_sapma_hukmu(F, N, y, bl, en_yeni)\n    return t_son"

MUTANTLAR = [
    ("M-H12a KANAL F", "TAZELIK'in F kanali kopar — bayatlik FAIL'i sessizce kaybolur",
     [(CAGRI_TAZ, "    t_son = _h12_tazelik([], N, O, rc, y)")]),
    ("M-H12b KANAL N", "TAZELIK'in N kanali kopar — 'son guncelleme' notu kaybolur",
     [(CAGRI_TAZ, "    t_son = _h12_tazelik(F, [], O, rc, y)")]),
    ("M-H12c KANAL O", "TAZELIK'in O kanali kopar — OLCULEMEDI hukmu kaybolur",
     [(CAGRI_TAZ, "    t_son = _h12_tazelik(F, N, [], rc, y)")]),
    ("M-H12d KENAR en_yeni", "HARITA -> HUKUM kenari kopar (CANLI BAYAT gorunmez)",
     [(CAGRI_HUK, "    _h12_sapma_hukmu(F, N, y, bl, {})")]),
    ("M-H12e KENAR bl", "canli blok listesi kopar — sapma hukmu hicbir blogu goremez",
     [(CAGRI_HUK, "    _h12_sapma_hukmu(F, N, y, [], en_yeni)")]),
    ("M-H12f DONUS t_son", "kapinin DONUS degeri kopar — H14 tarihi kaybeder (kapilar arasi kenar)",
     [(DONUS, "    _h12_sapma_hukmu(F, N, y, bl, en_yeni)\n    return None")]),
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
        print("OLCULEMEDI: git yok.")
        return 2

    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("H12 ALT-BOLME MUTANTI — kenarlar ve UC HUKUM KANALI")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h12mut_")
    try:
        try:
            kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
            referans = kume_olc(motor, kokler, os.path.join(taban, "ref"))
            ikinci = kume_olc(motor, kokler, os.path.join(taban, "ref2"))
        except Kurulamadi as e:
            print("OLCULEMEDI: referans kol kurulamadi: %s" % e)
            return 2
        tk = farklari_bul(referans, ikinci)
        print("  TEMIZ KOL (ayni motor 2 kez)   %s"
              % ("FARK YOK" if not tk else "FARK VAR: %s" % tk[:3]))
        if tk:
            print("\nOLCULEMEDI: duzenek determinist degil.")
            return 2
        imzalar = {ad: referans[(ad, "kapi")] for ad, _ in HALLER}
        atessiz = [ad for ad, _ in HALLER if _h12_satiri(imzalar[ad][1]) is None]
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            print("     %-14s exit %s · %s" % (ad, e, (_h12_satiri(c) or "(H12 SATIRI YOK)")[:58]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H12'yi hic ateslemedi: %s" % ", ".join(atessiz))
            return 2
        if tekil < 2:
            print("\nOLCULEMEDI: haller ayrismiyor.")
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
            print("  ALTIN KUME her mutanti gordu.")
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kumenin KOR oldugu kenar.")
        return 1
    print("  H12 bolmesinin her kenari ve her hukum kanali olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

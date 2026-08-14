#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H11 ALT-BOLME MUTANTI — kenarlar ve hukum kanallari olculuyor mu?

h1/h4/h10/h12 mutantlariyla ayni sozlesme. H11'in ozellikleri:

  * DORT parca da yalniz `F` kullanir; `N` ince ebeveynde, `O` HIC kullanilmaz.
    Yani "kanal" ekseninde H11 tek renklidir — asil is KENARLARDADIR.
  * `harita` kenarinin IKI tuketicisi var (`_h11_baglanti`, `_h11_canli_link`);
    ikisi AYRI AYRI koparilir. Tek mutantla olculselerdi biri hic olculmemis
    olabilirdi (ORTUSEN TESPIT KORLUGU MASKELER).
  * `_h11_govde` BAGLANTI dongusunun ICINDEN cagrilir — sira korunsun diye.
    Kendi kanali ve kendi kenari (`k`, `m`) ayrica olculur.
  * `ks` DONUS kenari H12'ye gider. Onu olcmek icin `h_h12_sapmasi` hali var:
    orada bir KARAR, canli bloktan daha yeni tek kayittir; `return []` olursa
    H12'nin CANLI BAYAT hukmu sessizce kaybolur.

HAL KAPISI: temiz kolda her halin ciktisinda bir H11 satiri BULUNMALIDIR.
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

UZUN = ("Baglam yazildi. " * 20)          # >200 karakter: 'kabul' kapisini susturur
KISA = "kisa."                            # <200 karakter: 'kabul ama govde bos' ates


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun", m)


ADR_SABLON = """---
no: {no:04d}
baslik: {baslik}
durum: {durum}
tarih: {tarih}
konu: {konu}
yerini-aldigi: {ya}
yerine-gecen: {yg}
---

# {no:04d} — {baslik}

## Baglam
{govde}
"""


def adr_yaz(kok, no, ad, durum="onerildi", konu="genel-durum", ya="-", yg="-",
            govde=UZUN, tarih="2026-01-05"):
    d = os.path.join(kok, "kararlar")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "%04d-%s.md" % (no, ad))
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(ADR_SABLON.format(no=no, baslik=ad.replace("-", " "), durum=durum,
                                  tarih=tarih, konu=konu, ya=ya, yg=yg, govde=govde))
    return "%04d-%s.md" % (no, ad)


def canliya_ekle(kok, satir):
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write("\n" + satir + "\n")


# --------------------------------------------------------------- PROJE HALLERI
#  ONBIR HUKUM, ONBIR HAL + temiz + karar-yok + H12 donus kenari = ONDORT.
#  Her hal TEK hukmu atesler; boylece bir mutant kacinca hangi hukum korledi
#  belli olur. Ortusen haller kullanilmadi: iki hukum ayni halde ateslenirse
#  mutant ikisini de olcuyor sanilir, oysa birini hic olcmuyor olabilir.
def _h_yok(kok):
    pass


def _h_temiz(kok):
    adr_yaz(kok, 1, "ilk-karar")
    adr_yaz(kok, 2, "ikinci-karar", durum="kabul")


def _h_tekrar(kok):
    adr_yaz(kok, 1, "birinci")
    adr_yaz(kok, 1, "birinci-kopya")


def _h_bosluk(kok):
    adr_yaz(kok, 1, "birinci")
    adr_yaz(kok, 3, "ucuncu")


def _h_yg_sayi_degil(kok):
    adr_yaz(kok, 1, "birinci", durum="yerine-gecildi", yg="abc")


def _h_yg_yok(kok):
    adr_yaz(kok, 1, "birinci", durum="yerine-gecildi", yg="0009")


def _h_tek_yonlu(kok):
    adr_yaz(kok, 1, "birinci", durum="yerine-gecildi", yg="0002")
    adr_yaz(kok, 2, "ikinci", ya="-")


def _h_durum_uyumsuz(kok):
    adr_yaz(kok, 1, "birinci", durum="onerildi", yg="0002")
    adr_yaz(kok, 2, "ikinci", ya="0001")


def _h_ya_sayi_degil(kok):
    adr_yaz(kok, 1, "birinci", ya="xyz")


def _h_ya_yok(kok):
    adr_yaz(kok, 1, "birinci", ya="0007")


def _h_kabul_bos(kok):
    adr_yaz(kok, 1, "birinci", durum="kabul", govde=KISA)


def _h_link_yok(kok):
    adr_yaz(kok, 1, "birinci")
    canliya_ekle(kok, "Ayrinti: [karar](kararlar/0009-olmayan-karar.md)")


def _h_link_yerine_gecilmis(kok):
    adr_yaz(kok, 1, "birinci", durum="yerine-gecildi", yg="0002")
    adr_yaz(kok, 2, "ikinci", ya="0001")
    canliya_ekle(kok, "Ayrinti: [karar](kararlar/0001-birinci.md)")


def _h_h12_sapmasi(kok):
    # H11 -> H12 DONUS kenari. `acilis-protokolu` blogunun ARKASINDA FRAGMAN
    # YOKTUR (SAB_CANLI sablonundan gelir), bu yuzden o konuda blogtan daha yeni
    # tek kayit KARAR dosyasidir. `ks` donusu bosalirsa H12'nin CANLI BAYAT
    # hukmu sessizce kaybolur.
    adr_yaz(kok, 1, "birinci", konu="acilis-protokolu", tarih="2026-12-31")
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    s = open(p, encoding="utf-8").read()
    s2 = re.sub(r'(<!--\s*blok konu="acilis-protokolu"[^>]*?guncel=")(\d{4}-\d{2}-\d{2})',
                r"\g<1>2026-01-01", s, count=1)
    if s2 == s:
        raise Kurulamadi("acilis-protokolu blok basligi bulunamadi")
    open(p, "w", encoding="utf-8", newline="").write(s2)


HALLER = [
    ("h_yok", _h_yok),
    ("h_temiz", _h_temiz),
    ("h_tekrar", _h_tekrar),
    ("h_bosluk", _h_bosluk),
    ("h_yg_sayi_degil", _h_yg_sayi_degil),
    ("h_yg_yok", _h_yg_yok),
    ("h_tek_yonlu", _h_tek_yonlu),
    ("h_durum_uyumsuz", _h_durum_uyumsuz),
    ("h_ya_sayi_degil", _h_ya_sayi_degil),
    ("h_ya_yok", _h_ya_yok),
    ("h_kabul_bos", _h_kabul_bos),
    ("h_link_yok", _h_link_yok),
    ("h_link_yerine_gecilmis", _h_link_yerine_gecilmis),
    ("h_h12_sapmasi", _h_h12_sapmasi),
]

OLCUM_KOMUTLARI = [["kapi"]]


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def hal_kur(motor, ad, hazirlik, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H11MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    rc, c = kos(motor, ["not", "--konu=genel-durum", "--tur=durum",
                        "--metin=h11 mutanti icin ilk kayit"], kok)
    if rc != 0:
        raise Kurulamadi("not basarisiz (%s)" % ad)
    rc, c = kos(motor, ["derle"], kok)
    if rc != 0:
        raise Kurulamadi("derle basarisiz (%s)" % ad)
    hazirlik(kok)
    return kok


def haller_kur(motor_temiz, taban):
    return {ad: hal_kur(motor_temiz, ad, hazirlik, taban) for ad, hazirlik in HALLER}


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


def _h11_satiri(cikti):
    satirlar = [s.strip() for s in cikti.split("\n")]
    for d in satirlar:
        if d.startswith("[H11]"):
            return d
    for d in satirlar:
        if "H11:" in d[:12]:
            return d
    return None


# --------------------------------------------------------------------- MUTANTLAR
CAGRI_NUM = "        _h11_numara(F, ks)"
CAGRI_BAG = "        _h11_baglanti(F, ks, harita)"
CAGRI_LNK = "        _h11_canli_link(F, y, harita)"
CAGRI_GOV = "        _h11_govde(F, k, m)"
DONUS = "        N.append(\"H11: henuz karar dosyasi yok\")\n    return ks"

MUTANTLAR = [
    ("M-H11a KANAL F numara", "NUMARA'nin F kanali kopar — no tekrari/boslugu sessizce kaybolur",
     [(CAGRI_NUM, "        _h11_numara([], ks)")]),
    ("M-H11b KANAL F baglanti", "BAGLANTI'nin F kanali kopar — yerine-gecme hukumleri kaybolur",
     [(CAGRI_BAG, "        _h11_baglanti([], ks, harita)")]),
    ("M-H11c KANAL F govde", "GOVDE'nin F kanali kopar — 'kabul ama bos' sessizce kaybolur",
     [(CAGRI_GOV, "        _h11_govde([], k, m)")]),
    ("M-H11d KANAL F link", "CANLI LINK'in F kanali kopar — kirik/bayat karar linki kaybolur",
     [(CAGRI_LNK, "        _h11_canli_link([], y, harita)")]),
    ("M-H11e KENAR harita->bag", "BAGLANTI harita'yi kaybeder (hedef ADR'ler gorunmez olur)",
     [(CAGRI_BAG, "        _h11_baglanti(F, ks, {})")]),
    ("M-H11f KENAR harita->lnk", "CANLI LINK harita'yi kaybeder (IKINCI tuketici ayri olculur)",
     [(CAGRI_LNK, "        _h11_canli_link(F, y, {})")]),
    ("M-H11g KENAR ks->numara", "NUMARA ks'i kaybeder — tekrar/bosluk hic bakilmaz",
     [(CAGRI_NUM, "        _h11_numara(F, [])")]),
    ("M-H11h KENAR ks->baglanti", "BAGLANTI ks'i kaybeder — dongu hic donmez (govde de olculmez)",
     [(CAGRI_BAG, "        _h11_baglanti(F, [], harita)")]),
    ("M-H11i DONUS ks", "kapinin DONUS degeri bosalir — H12 kararlari kaybeder (kapilar arasi)",
     [(DONUS, "        N.append(\"H11: henuz karar dosyasi yok\")\n    return []")]),
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
    print("H11 ALT-BOLME MUTANTI — kenarlar ve hukum kanallari")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h11mut_")
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
        atessiz = [ad for ad, _ in HALLER if _h11_satiri(imzalar[ad][1]) is None]
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            print("     %-22s exit %s · %s" % (ad, e, (_h11_satiri(c) or "(H11 SATIRI YOK)")[:52]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H11'i hic ateslemedi: %s" % ", ".join(atessiz))
            return 2
        if tekil < 2:
            print("\nOLCULEMEDI: haller ayrismiyor.")
            return 2
        print(CIZGI)
        print("  %-26s %-11s %-26s %s" % ("mutant", "KENDI", "iz", "ALTIN KUME"))
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
                print("  ?  %-26s OLCULEMEDI  %s" % (ad, e))
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
                print("  +  %-26s ISIRDI      %-26s %s"
                      % (ad, "%d olcum: %s" % (len(farklar), ",".join(h[2:] for h in izler)[:14]),
                         alt_txt))
            else:
                kacti.append(ad)
                print("  !  %-26s KACTI       %-26s %s" % (ad, "-", alt_txt))

        print(CIZGI)
        print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
              % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
        if altin_kor:
            print("  ALTIN KUME %d mutanta KOR: %s" % (len(altin_kor), ", ".join(altin_kor)))
        if olculemedi:
            print("  OLCULEMEDI — duzenek kurulamadi.")
            return 2
        if kacti:
            print("  KIRMIZI: kacan mutant KOR bir kenar/kanal demektir.")
            return 1
        print("  H11 bolmesinin her kenari ve her hukum kanali olculuyor.")
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

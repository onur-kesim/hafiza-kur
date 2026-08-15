#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KARMASIKLIK MUTANTI — olcut aracinin KENDISI dogru olcutte mi?

NEDEN AYRI BIR MUTANT
---------------------
`faz0/karmasiklik.py` bir OLCUM ARACIDIR ve doktrin 1 araclara da isler:
"olculmeyen kapinin hukmu YOKTUR." Arac bir sayi basiyor diye o sayinin
DOGRU OLCUTTE oldugu anlasilmaz. ADR'nin (faz0/ADR_CC_OLCUTU.md §7) kabul
sarti aciktir: *"arac kendi mutantiyla sinanir: bilerek ic fonksiyonlu bir
ornek verilir; sayac ic govdeyi sayarsa ISIRMALI."*

Bu dosya o sarti ve yedi kardesini olcer. Her mutant ARACIN kaynagini tek bir
noktadan bozar; SABIT bir ornek modul uzerinde sonucun DEGISMESI beklenir.

    FARK VAR   -> ISIRDI      olcutun o maddesi gercekten olculuyor
    FARK YOK   -> KACTI       madde KOR; arac o kurali aslinda uygulamiyor
    kurulamadi -> OLCULEMEDI  ARAC KUSURU (Y-4 dersi: sahte kirmizi uretme)

Ornek modulun beklenen degerleri ELLE hesaplanmistir ve KONTROL kolu once
onlari dogrular; tutmuyorsa mutant hukmu ANLAMSIZDIR ve betik durur.

Ayrica CIPA olarak gercek motordan iki deger sinanir, HER GUNCELLEMEDE radon ile
CAPRAZLANARAK: cmd_isir 17 (13 Agu'dan beri sabit) · cmd_devral 88 -> 97 (15 Agu).

KULLANIM     python3 faz0/karmasiklik_mutanti.py
CIKIS KODU   0 hepsi isirdi · 1 en az biri kacti · 2 OLCULEMEDI
"""
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARAC = os.path.join(KOK, "faz0", "karmasiklik.py")
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 84


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Olcutun dogru oldugu anlamina GELMEZ."""


# --------------------------------------------------------------- ORNEK MODUL
# Her fonksiyon TEK BIR kurali ayirt eder. Beklenen degerler elle hesaplandi.
ORNEK = '''
def sade():
    return 1

def dallar(a, b):
    if a:
        return 1
    return 2 if b else 3

def dongu(xs):
    for x in xs:
        pass
    while xs:
        break
    return 0

def yakala():
    try:
        pass
    except ValueError:
        pass
    except KeyError:
        pass

def mantik(a, b, c):
    if a and b and c:
        return 1
    return 0

def uretec(xs):
    return [x for x in xs if x > 1 if x < 9]

def baglam(p):
    with open(p) as f:
        return f.read()

def iddia(x):
    assert x
    return x

def dis(xs):
    def ic(y):
        if y:
            return 1
        return 0
    for x in xs:
        ic(x)
    return 0

def lam(xs):
    f = lambda y: 1 if y else 0
    return [f(x) for x in xs]
'''

# 🔴 ESIK KOLLARI — ilk surumde YOKTU ve M-K8 bu yuzden KACTI (olculdu 13 Agu 2026):
# ornegin en yuksek CC'si 4 idi, tavani 20'den 100'e cikarmak HICBIR SEYI
# degistirmiyordu. Mutant kusurlu degildi, ORNEK o kurali GOREMIYORDU.
# Ders: bir esigi olcen mutantin ornegi o esigi ASMALIDIR.
AGIR_IF = 24          # CC = 1 + 24 = 25  -> CC tavanini (20) asar
UZUN_SATIR = 90       # satir tavanini (80) asar, CC = 1
ORNEK += "\ndef agir(x):\n    n = 0\n"
ORNEK += "".join("    if x == %d:\n        n += 1\n" % i for i in range(AGIR_IF))
ORNEK += "    return n\n"
ORNEK += "\ndef uzun(x):\n" + "".join("    x += %d\n" % i for i in range(UZUN_SATIR)) + "    return x\n"

# ad -> CC   (elle hesaplandi; KONTROL kolu bunu dogrular)
BEKLENEN = {
    "agir": 1 + AGIR_IF,   # esik kolu: CC tavanini asar
    "uzun": 1,             # esik kolu: satir tavanini asar, CC dusuk
    "sade": 1,        # taban
    "dallar": 3,      # 1 + If + IfExp
    "dongu": 3,       # 1 + For + While
    "yakala": 3,      # 1 + iki ExceptHandler   (try GOVDESI sayilmaz)
    "mantik": 4,      # 1 + If + BoolOp(3 deger -> +2)
    "uretec": 4,      # 1 + comprehension + iki filtre `if`
    "baglam": 1,      # `with` SAYILMAZ
    "iddia": 1,       # `assert` SAYILMAZ
    "dis": 2,         # 1 + For          (ic fonksiyona INILMEZ)
    "dis.ic": 2,      # 1 + If           (AYRI kayit)
    "lam": 2,         # 1 + comprehension (lambda govdesi sayilmaz)
}

# Gercek motordan capa degerler — radon ile caprazlandi.
#   13 Agu 2026: cmd_isir 17 · cmd_devral 88
#   15 Agu 2026: cmd_devral 88 -> 97. Sebep BILINEN ve BEYANLI — BITTI md.6
#     `cmd_devral`a kesif/durma dallarini ekledi (`--kesif` kolu · `--canli`/`--esle`
#     celiskisi · DURMA KURALI · coklu `canli` adayi uyarisi). CI #56 bu kapiyi UC
#     PLATFORMDA kirmizi yakti; kapi gorevini YAPTI, sessizce gecmedi.
#   🔴 CAPA, ARACIN KENDI CIKTISINDAN GUNCELLENMEZ — oyle yapilirsa capa kendi
#     kendini onaylar ve hicbir suruklenmeyi bir daha yakalayamaz. 15 Agu'da
#     BAGIMSIZ olculdu: `python -m radon cc -s skill/scripts/hafiza.py` ->
#     `cmd_devral - F (97)`, `cmd_isir - C (17)`; ayni radon eski motorda 88 diyor.
#     Yani ikili (arac, radon) YENI degerde de anlasiyor.
CIPA = {"cmd_isir": 17, "cmd_devral": 97}

# ------------------------------------------------------------------ MUTANTLAR
# (ad, aciklama, [(eski, yeni)], ayirt eden ornek)
INIS_SATIRI = ("        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):\n"
               "            continue                       # ayri fonksiyon, ayri esik\n")

MUTANTLAR = [
    ("M-K1 INIS", "ic def/lambda govdesine INILIR (ADR'nin reddettigi olcut)",
     [(INIS_SATIRI, "")], "dis · lam"),
    ("M-K2 COMP-IF", "comprehension icindeki `if`ler sayilmaz",
     [("            n += 1 + len(d.ifs)            # uretecin kendisi + her filtre",
       "            n += 1")], "uretec"),
    ("M-K3 BOOLOP", "BoolOp dallari sayilmaz",
     [("        elif isinstance(d, ast.BoolOp):\n"
       "            n += len(d.values) - 1         # a and b and c -> iki dal\n", "")], "mantik"),
    ("M-K4 WITH", "`with` SAYILIR (radon uyumunu bozar)",
     [("        if isinstance(d, _BIRIM):",
       "        if isinstance(d, (ast.With, ast.AsyncWith)):\n"
       "            n += 1\n"
       "        elif isinstance(d, _BIRIM):")], "baglam"),
    ("M-K5 EXCEPT", "`except` dallari sayilmaz",
     [("ast.While, ast.ExceptHandler)", "ast.While)")], "yakala"),
    ("M-K6 SATIR", "satir sayimi bozulur (end_lineno yerine tek satir)",
     [('"satir": c.end_lineno - c.lineno + 1', '"satir": 1')], "satir sutunu"),
    ("M-K7 SIRA", "siralama TERS (determinist cikti sozlesmesi)",
     [('bulunan.sort(key=lambda x: (-x["cc"], x["ad"]))',
       'bulunan.sort(key=lambda x: (x["cc"], x["ad"]))')], "cikti sirasi"),
    ("M-K8 CC ESIGI", "CC tavani sessizce 100'e cikar",
     [("TAVAN_CC = 20", "TAVAN_CC = 100")], "agir"),
    ("M-K9 SATIR ESIGI", "satir tavani sessizce 1000'e cikar",
     [("TAVAN_SATIR = 80", "TAVAN_SATIR = 1000")], "uzun"),
]


def olc(arac, dosya):
    """{ad: (cc, satir)} + ham cikti. Arac exit 2 verirse Kurulamadi."""
    r = subprocess.run([sys.executable, "-X", "utf8", arac, dosya, "--json"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    if r.returncode == 2:
        raise Kurulamadi("arac OLCULEMEDI dedi: %s" % (r.stdout or r.stderr)[:120])
    import json as _j
    try:
        d = _j.loads(r.stdout)
    except Exception as e:
        raise Kurulamadi("arac ciktisi JSON degil (%s): %s" % (e, (r.stdout or r.stderr)[:120]))
    sira = [f["ad"] for f in d["fonksiyonlar"]]
    return ({f["ad"]: (f["cc"], f["satir"]) for f in d["fonksiyonlar"]},
            sira, d["ihlal_sayisi"])


def sabotajli(kaynak, degisimler, dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:55]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli arac derlenmiyor: %s" % e)
    p = os.path.join(dizin, "karmasiklik.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def main():
    if not os.path.isfile(ARAC):
        print("OLCULEMEDI: arac yok: %s" % ARAC)
        return 2
    kaynak = open(ARAC, encoding="utf-8").read()
    taban = tempfile.mkdtemp(prefix="kmut_")
    ornek = os.path.join(taban, "ornek.py")
    with open(ornek, "w", encoding="utf-8", newline="\n") as f:
        f.write(ORNEK)

    print(CIZGI)
    print("KARMASIKLIK MUTANTI — olcut araci DOGRU OLCUTTE mi?")
    print("arac: %s" % ARAC)
    print(CIZGI)

    # ---- KONTROL 1: temiz arac, elle hesaplanan degerleri veriyor mu? ----
    try:
        ref, ref_sira, ref_ihlal = olc(ARAC, ornek)
    except Kurulamadi as e:
        print("OLCULEMEDI: referans olcum kurulamadi: %s" % e)
        return 2
    yanlis = [(k, v, ref.get(k, (None,))[0]) for k, v in BEKLENEN.items()
              if ref.get(k, (None,))[0] != v]
    if yanlis:
        print("  KONTROL 1 (elle hesap)          BOZUK")
        for k, b, g in yanlis:
            print("     %-12s beklenen %s · arac %s" % (k, b, g))
        print("\nOLCULEMEDI: arac ornek modulde bile beklenen degeri vermiyor;")
        print("mutant hukmu ANLAMSIZ olurdu. Once olcut/ornek uyusmazligi cozulmeli.")
        return 2
    print("  KONTROL 1 (elle hesap, %2d deger) TUTUYOR" % len(BEKLENEN))

    # ---- KONTROL 2: gercek motorda capa degerler ----
    if os.path.isfile(MOTOR):
        try:
            m, _, _ = olc(ARAC, MOTOR)
        except Kurulamadi as e:
            print("  KONTROL 2 (motor capasi)        OLCULEMEDI: %s" % e)
            return 2
        kotu = [(k, v, m.get(k, (None,))[0]) for k, v in CIPA.items()
                if m.get(k, (None,))[0] != v]
        if kotu:
            print("  KONTROL 2 (motor capasi)        BOZUK")
            for k, b, g in kotu:
                print("     %-12s beklenen %s · arac %s" % (k, b, g))
            print("\nKIRMIZI: arac gercek motorda kayitli capa degerleri vermiyor.")
            print("Ya olcut degisti (ADR guncellenmeli) ya da motor degisti.")
            return 1
        print("  KONTROL 2 (motor capasi, %d deger) TUTUYOR" % len(CIPA))
    else:
        print("  KONTROL 2 (motor capasi)        ATLANDI — motor yok")

    print(CIZGI)
    isirdi, kacti, olculemedi = [], [], []
    for ad, aciklama, degisimler, ayirt in MUTANTLAR:
        d = os.path.join(taban, ad.split()[0])
        os.makedirs(d, exist_ok=True)
        try:
            sab = sabotajli(kaynak, degisimler, d)
            yeni, yeni_sira, yeni_ihlal = olc(sab, ornek)
        except Kurulamadi as e:
            olculemedi.append(ad)
            print("  ?  %-14s OLCULEMEDI  %s" % (ad, e))
            continue
        degisen = [k for k in set(ref) | set(yeni) if ref.get(k) != yeni.get(k)]
        farkli = bool(degisen) or yeni_sira != ref_sira or yeni_ihlal != ref_ihlal
        if farkli:
            isirdi.append(ad)
            iz = ("%d fonksiyonda deger" % len(degisen)) if degisen else (
                "sira" if yeni_sira != ref_sira else "ihlal %d->%d" % (ref_ihlal, yeni_ihlal))
            print("  +  %-14s ISIRDI   %-22s [%s] %s" % (ad, iz, ayirt, aciklama))
        else:
            kacti.append(ad)
            print("  !  %-14s KACTI    %s" % (ad, aciklama))
            print("     -> olcutun bu maddesi KOR: arac kurali uygulamiyor olabilir.")
        sys.stdout.flush()

    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'olcut saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = olcutun KANITSIZ maddesi.")
        return 1
    print("  Olcutun her maddesi olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

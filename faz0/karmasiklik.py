#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KARMASIKLIK OLCERI — CLAUDE.md §5'in "CC >20 yok" kuralinin OLCUM YOLU.

NEDEN VAR
---------
CLAUDE.md §5 "hicbiri CC >20" diyordu ama HANGI CC oldugunu soylemiyordu.
Olculdu (11 Agu 2026): `cmd_isir` icin iki savunulabilir metrik 8,6 kat farkli
sayi veriyordu (ic fonksiyonlara INEREK 137 · INMEDEN 17) ve ayni bayt dizisi
projenin kendi belgelerinde iki KARSIT hukumle geciyordu. Karar defteri:
`faz0/ADR_CC_OLCUTU.md`.

Kural bir ARACA baglanmadan hukum veremez: "olcum araci kurulu olan kural
talimati prozayla tekrar etmez, aracin adini yazar."

OLCUT — TAM TANIM (pazarlik burada biter)
-----------------------------------------
    CC = 1
       + If · IfExp · For · AsyncFor · While · ExceptHandler   (her biri +1)
       + comprehension (+1) VE icindeki her `if` (+1)
       + BoolOp basina (deger_sayisi - 1)

    IC ICE `def` ve `lambda` GOVDESINE INILMEZ — her biri AYRI fonksiyondur
    ve kendi esigine tabidir. (ADR karari, 12 Agu 2026.)

    SAYILMAZ: `with` · `try` govdesi (yalniz `except` sayilir) · `else`
    dallari · `assert`.

🔴 BU KUME KEYFI DEGIL, DIS TANIKLA SECILDI (olculdu 13 Agu 2026)
    `radon cc` ile ayni motorun 179 fonksiyonu uzerinde caprazlandi:
    yukaridaki kume ile **178/179 BIREBIR** tutuyor. Iki kusur bu caprazlamada
    bulundu ve duzeltildi:
        * comprehension icindeki `if`ler SAYILMIYORDU  (radon sayiyor)
        * `with` SAYILIYORDU                            (radon saymiyor)
    Ayrica ADR'nin ic-ice karari dogrulandi: radon da `cmd_isir` icin 17 der.

    radon BIR BAGIMLILIK DEGILDIR ve bu betik onu CAGIRMAZ — yalniz olcut
    secilirken bir kez capraz kontrol olarak kullanildi. Bu dosya stdlib `ast`
    ile calisir, sifir bagimlilik kirilmaz.

    KALAN TEK UYUSMAZLIK: `zincir_dogrula` — bu arac 40, radon 41 der.
    SEBEBI OLCULMEDI. Bir fonksiyonluk fark hukmu degistirmiyor (ikisi de
    esigin ustunde), ama BILINEN ve KAPATILMAMIS bir farktir.

KULLANIM
    python3 faz0/karmasiklik.py skill/scripts/hafiza.py
    python3 faz0/karmasiklik.py skill/scripts/hafiza.py --ihlal
    python3 faz0/karmasiklik.py skill/scripts/hafiza.py --json
    python3 faz0/karmasiklik.py skill/scripts/hafiza.py --kapi

CIKIS KODU
    0  olculdu (rapor kipi HER ZAMAN 0 doner — bu bir OLCUM, kapi degil)
    1  --kapi verildi VE en az bir ihlal var
    2  OLCULEMEDI (dosya yok / ayristirilamiyor) — "temiz" DEMEK DEGILDIR
"""
import argparse
import ast
import json
import sys

TAVAN_CC = 20
TAVAN_SATIR = 80

# Her biri +1. `Try` govdesi BILEREK yok: yalniz `ExceptHandler` sayilir.
_BIRIM = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)


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


def cc(fn):
    """Fonksiyonun KENDI GOVDESINDEN karmasiklik. Ic def/lambda'ya INMEZ."""
    n = 1
    yigin = list(ast.iter_child_nodes(fn))
    while yigin:
        d = yigin.pop()
        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue                       # ayri fonksiyon, ayri esik
        if isinstance(d, _BIRIM):
            n += 1
        elif isinstance(d, ast.comprehension):
            n += 1 + len(d.ifs)            # uretecin kendisi + her filtre
        elif isinstance(d, ast.BoolOp):
            n += len(d.values) - 1         # a and b and c -> iki dal
        yigin.extend(ast.iter_child_nodes(d))
    return n


def fonksiyonlar(kaynak):
    """[{ad, cc, satir, bas}] — CC azalan, esitlikte ada gore. DETERMINIST."""
    agac = ast.parse(kaynak)
    bulunan = []

    def gez(dugum, onek):
        for c in ast.iter_child_nodes(dugum):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ad = onek + c.name
                bulunan.append({"ad": ad, "cc": cc(c),
                                "satir": c.end_lineno - c.lineno + 1,
                                "bas": c.lineno})
                gez(c, ad + ".")           # ic fonksiyonlar AYRI kayit
            elif isinstance(c, ast.ClassDef):
                gez(c, onek + c.name + ".")
            else:
                gez(c, onek)

    gez(agac, "")
    bulunan.sort(key=lambda x: (-x["cc"], x["ad"]))
    return bulunan


def main():
    ap = argparse.ArgumentParser(description="fonksiyon basina karmasiklik ve satir")
    ap.add_argument("dosya")
    ap.add_argument("--ihlal", action="store_true", help="yalniz esigi asanlar")
    ap.add_argument("--json", action="store_true", dest="js")
    ap.add_argument("--kapi", action="store_true",
                    help="ihlal varsa exit 1 (rapor kipinde HER ZAMAN 0)")
    a = ap.parse_args()

    try:
        kaynak = open(a.dosya, encoding="utf-8").read()
    except OSError as e:
        print("OLCULEMEDI: dosya okunamadi: %s" % e)
        return 2
    try:
        hepsi = fonksiyonlar(kaynak)
    except SyntaxError as e:
        print("OLCULEMEDI: ayristirilamadi: %s" % e)
        return 2

    ihlal = [f for f in hepsi
             if f["cc"] > TAVAN_CC or f["satir"] > TAVAN_SATIR]

    if a.js:
        print(json.dumps({"dosya": a.dosya, "tavan_cc": TAVAN_CC,
                          "tavan_satir": TAVAN_SATIR,
                          "fonksiyon_sayisi": len(hepsi),
                          "ihlal_sayisi": len(ihlal),
                          "fonksiyonlar": ihlal if a.ihlal else hepsi},
                         ensure_ascii=False, indent=1))
        return 1 if (a.kapi and ihlal) else 0

    liste = ihlal if a.ihlal else hepsi
    print("KARMASIKLIK — %s" % a.dosya)
    print("  olcut: kendi govde CC · ic def/lambda'ya INILMEZ  (faz0/ADR_CC_OLCUTU.md)")
    print("  tavan: CC %d · satir %d" % (TAVAN_CC, TAVAN_SATIR))
    print("-" * 70)
    print("  %-38s %5s %6s %8s" % ("fonksiyon", "CC", "satir", "bas"))
    for f in liste:
        im = "!" if (f["cc"] > TAVAN_CC or f["satir"] > TAVAN_SATIR) else " "
        print("%s %-38s %5d %6d %8d" % (im, f["ad"][:38], f["cc"], f["satir"], f["bas"]))
    print("-" * 70)
    print("  fonksiyon: %d · CC>%d: %d · satir>%d: %d · ihlal (birlesik): %d"
          % (len(hepsi), TAVAN_CC, sum(1 for f in hepsi if f["cc"] > TAVAN_CC),
             TAVAN_SATIR, sum(1 for f in hepsi if f["satir"] > TAVAN_SATIR), len(ihlal)))
    if not a.kapi:
        print("  (rapor kipi: bu bir OLCUMDUR, kapi degil — exit 0)")
    return 1 if (a.kapi and ihlal) else 0


if __name__ == "__main__":
    sys.exit(main())

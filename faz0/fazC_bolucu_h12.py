#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h12` BOLME URETECI.

Kalip `fazC_bolucu_h10.py` ile AYNIDIR (KANAL KAPISI dahil). H12'de kalibin iki
ucu da bir arada gorunur: `_h12_tazelik` UC KANALI birden kullanir (F, N, O),
`_h12_sapma_haritasi` ise HIC hukum basmaz — yani ayni bolmede hem "dolu" hem
"bos" bolge var. Kanal kapisi ikisini de ayni olcutle ele alir:

    bolgenin kullandigi her hukum kanali, parcanin imzasinda BULUNMAK ZORUNDA
    (kullanmadigini tasimak zorunda DEGIL — saf parca saf kalir).
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

BEKLENEN_SHA = "09f248963b352387ee2816980cb164abbf3c4d9a92be973ca9e107742df63a68"

H12_DEF = 3713         # def _kapi_h12(F, N, O, rc, y, bl, ks):
H12_LAMBDA = 3714
H12_YORUM = 3715       # # ---- H12 BAYATLIK ---
H12_RETURN = 3758      # return t_son
H12_SONRASI = 3759

A = (3716, 3733, 0)    # TAZELIK   : 'Son guncelleme' cozumu + bayatlik -> t_son
B = (3734, 3748, 0)    # SAPMA HARITASI : fragman/karar tarihleri      -> en_yeni
C = (3749, 3757, 0)    # SAPMA HUKMU    : CANLI BAYAT + bekleyen fragman

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'

# (ad, imza, bolge, kuyruk, lambda gerekli mi)
PARCALAR = [
    ("_h12_tazelik", "def _h12_tazelik(F, N, O, rc, y):", A, "    return t_son", True),
    ("_h12_sapma_haritasi", "def _h12_sapma_haritasi(y, ks):", B, "    return en_yeni", False),
    ("_h12_sapma_hukmu", "def _h12_sapma_hukmu(F, N, y, bl, en_yeni):", C, None, True),
]

BASLIK = '''
# ----------------------------------------------- H12 ALT-BOLMESI (FAZ C)
# `_kapi_h12` (46 satir, CC 25) UC parcaya bolundu; ince `_kapi_h12` en sona konur.
#
# 🔴 BU BOLMEDE KALIBIN IKI UCU DA VAR:
#   `_h12_tazelik`        UC kanali birden kullanir (F · N · O) -> ucunu de ALIR
#   `_h12_sapma_haritasi` HIC hukum basmaz (olculdu: 0)         -> SAF, kanal ALMAZ
#   `_h12_sapma_hukmu`    F ve N kullanir                       -> ikisini ALIR
# Uretec bunu her kosumda AST ile olcer (KANAL KAPISI); imza eksikse YAZMAZ.
# Kullanilmayan kanali tasitmak da bir maliyet olurdu: "koruma" adi altinda
# olculmemis parametre birikir. Olcut tek: KULLANDIGINI TASI.
#
# Parcalar arasi veri IKI KENARDIR ve ikisi de imzada gorunur:
#     t_son    TAZELIK -> ebeveyn (donus degeri; H14 bunu kullanir)
#     en_yeni  SAPMA HARITASI -> SAPMA HUKMU
'''.strip("\n")


def hukum_haritasi(kaynak):
    agac = ast.parse(kaynak)
    bulunan = []
    for d in ast.walk(agac):
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "fail":
            etiket = "?"
            if d.args and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str):
                etiket = d.args[0].value
            bulunan.append((d.lineno, d.col_offset, etiket))
    bulunan.sort()
    return [(i + 1, e) for i, (_, _, e) in enumerate(bulunan)]


def kanallar(kaynak, bas, son):
    agac = ast.parse(kaynak)
    bulunan = set()
    for d in ast.walk(agac):
        if not isinstance(d, ast.Call) or not (bas <= getattr(d, "lineno", 0) <= son):
            continue
        f = d.func
        if isinstance(f, ast.Name) and f.id == "fail":
            bulunan.add("F")
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) \
                and f.attr == "append" and f.value.id in ("F", "N", "O"):
            bulunan.add(f.value.id)
    return bulunan


def tasi(L, parca):
    bas, son, dedent = parca
    cikti = []
    for i in range(bas, son + 1):
        s = L[i - 1]
        if not s.strip():
            cikti.append("")
            continue
        if not s.startswith(" " * dedent):
            raise SystemExit("OLCULEMEDI: satir %d beklenen %d bosluk ile baslamiyor: %r"
                             % (i, dedent, s[:60]))
        cikti.append(s[dedent:])
    return cikti


def main():
    sha = hashlib.sha256(open(KAYNAK, "rb").read()).hexdigest()
    if sha != BEKLENEN_SHA:
        print("OLCULEMEDI: girdi motoru beklenen SHA degil.")
        print("  beklenen: %s\n  bulunan : %s" % (BEKLENEN_SHA, sha))
        return 2

    ham = open(KAYNAK, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in ham else "\n"
    L = ham.split(nl)
    onceki = hukum_haritasi(ham)

    # --- 1) yapisal dogrulama ---
    assert L[H12_DEF - 1] == "def _kapi_h12(F, N, O, rc, y, bl, ks):", L[H12_DEF - 1]
    assert L[H12_LAMBDA - 1] == LAMBDA, repr(L[H12_LAMBDA - 1])
    assert L[H12_YORUM - 1].strip().startswith("# ---- H12 BAYATLIK"), L[H12_YORUM - 1]
    assert L[A[0] - 1].strip() == 'gun = rc["bayatlik_gun"]', L[A[0] - 1]
    assert L[B[0] - 1].strip().startswith("# sapma:"), L[B[0] - 1]
    assert L[C[0] - 1].strip().startswith("for _, _, oz in bl:"), L[C[0] - 1]
    assert L[H12_RETURN - 1].strip() == "return t_son", L[H12_RETURN - 1]
    assert L[H12_SONRASI - 1].strip() == "" and L[H12_SONRASI].strip() == "", "kuyruk bos degil"
    assert L[H12_SONRASI + 1].startswith("def _kapi_h13("), L[H12_SONRASI + 1]

    # --- 1b) KANAL KAPISI ---
    for ad, imza, bolge, _, _ in PARCALAR:
        gerekli = kanallar(ham, bolge[0], bolge[1])
        var = {p.strip() for p in imza.split("(", 1)[1].rstrip("):").split(",")}
        eksik = gerekli - var
        if eksik:
            print("KIRMIZI: %s bolgesi %s kanalini kullaniyor ama imzada YOK: %s"
                  % (ad, ",".join(sorted(eksik)), imza))
            return 1
        print("  kanal kapisi: %-20s kullanilan %-7s imza TASIYOR"
              % (ad, ",".join(sorted(gerekli)) or "(SAF)"))

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H12_DEF - 1]
    yeni += BASLIK.split("\n")
    yeni.append("")
    yeni.append("")
    for ad, imza, bolge, kuyruk, lam in PARCALAR:
        yeni.append(imza)
        if lam:
            yeni.append(LAMBDA)
        yeni += tasi(L, bolge)
        if kuyruk:
            yeni.append(kuyruk)
        yeni.append("")
        yeni.append("")

    yeni.append(L[H12_DEF - 1])                  # def _kapi_h12(...)  BIREBIR
    yeni.append(L[H12_YORUM - 1])                # yorum               BIREBIR
    yeni.append("    t_son = _h12_tazelik(F, N, O, rc, y)")
    yeni.append("    en_yeni = _h12_sapma_haritasi(y, ks)")
    yeni.append("    _h12_sapma_hukmu(F, N, y, bl, en_yeni)")
    yeni.append(L[H12_RETURN - 1])               # return t_son        BIREBIR

    yeni += L[H12_SONRASI - 1:]
    metin = nl.join(yeni)

    # --- 3) kapilar ---
    compile(metin, "<h12-bolme>", "exec")
    sonraki = hukum_haritasi(metin)
    if onceki != sonraki:
        print("KIRMIZI: hukum haritasi DEGISTI (%d -> %d)." % (len(onceki), len(sonraki)))
        for i, (a, b) in enumerate(zip(onceki, sonraki)):
            if a != b:
                print("  ilk fark #%d: %s -> %s" % (i + 1, a, b))
                break
        return 1

    with open(HEDEF, "w", encoding="utf-8", newline="") as f:
        f.write(metin)
    print("YAZILDI: %s" % HEDEF)
    print("  hukum  : %d -> %d  (sira->kapi eslemesi AYNI)" % (len(onceki), len(sonraki)))
    print("  satir  : %d -> %d" % (len(L), len(yeni)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

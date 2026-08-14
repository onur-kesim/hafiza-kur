#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h11` BOLME URETECI.

Kalip `fazC_bolucu_h12.py` ile AYNIDIR (KANAL KAPISI dahil). H11'in kendine ozgu
IKI kisiti var ve tasarimi bunlar belirledi:

1. 🔴 SIRA KORUNMAK ZORUNDA. BAGLANTI ve GOVDE kontrolleri ayni `for k in ks`
   dongusunun icinde. Ayri fonksiyona alip AYRI DONGU yapmak `F` listesindeki
   hukum sirasini degistirirdi: her ADR icin (baglanti, govde) yerine
   (tum baglantilar), (tum govdeler). Altin kumenin bit-bit esdegerlik kapisi
   bunu KIRARDI — ve kumenin fark etmemesine guvenmek bir kumar olurdu.
   Bu yuzden `_h11_govde` DONGU ICINDEN cagrilir; sira birebir korunur.

2. H11 `O` kanalini HIC kullanmiyor (olculdu: dort bolgenin dordu de yalniz F).
   `N` yalnizca ince ebeveynde (sayac notu + "karar yok" notu). Kanal kapisi
   bunu her kosumda AST ile olcer; parcalar yalnizca F alir.

   NOT (bulgu, DUZELTILMEDI): "yerine-gecen SAYI DEGIL" bir OLCULEMEDI hali
   olabilirdi ama FAIL basiliyor. Bu bolme ADDITIVE'dir — davranisa dokunmaz.

Parcalar arasi veri UC KENARDIR ve ucu de imzada gorunur:
    harita   ebeveyn -> BAGLANTI ve CANLI LINK (IKI tuketici, ayri ayri olculur)
    k, m     BAGLANTI -> GOVDE (dongu ici kenar)
    ks       ebeveyn -> NUMARA, BAGLANTI  ·  ve ebeveynden H12'ye (donus)
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

BEKLENEN_SHA = "61283ff7d755ffc719ea7fe74045740f6dc305e18a8f39a7cd9df48482152629"

H11_DEF = 3663         # def _kapi_h11(F, N, O, y):
H11_LAMBDA = 3664
H11_YORUM = 3665       # # ---- H11 KARAR BUTUNLUGU (ADR) ---
H11_KS = 3666          # ks = adr_listesi(y)
H11_IF = 3667          # if ks:
H11_HARITA = 3675      # harita = {k["no"]: k for k in ks}
H11_N = 3707           # N.append("H11: %d karar ...")
H11_ELSE = 3708
H11_N2 = 3709
H11_RETURN = 3710      # return ks
H11_SONRASI = 3711

A = (3668, 3674, 4)    # NUMARA     : no tekrari + numara boslugu
B = (3676, 3698, 4)    # BAGLANTI   : yerine-gecme cifti (for k in ks dongusu)
C = (3699, 3700, 8)    # GOVDE      : durum kabul ama govde bos
D = (3701, 3706, 4)    # CANLI LINK : canli hafizanin karar linkleri

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'
GOVDE_CAGRISI = "        _h11_govde(F, k, m)"

# (ad, imza, bolge, kuyruk, lambda gerekli mi)
PARCALAR = [
    ("_h11_numara", "def _h11_numara(F, ks):", A, None, True),
    ("_h11_govde", "def _h11_govde(F, k, m):", C, None, True),
    ("_h11_baglanti", "def _h11_baglanti(F, ks, harita):", B, GOVDE_CAGRISI, True),
    ("_h11_canli_link", "def _h11_canli_link(F, y, harita):", D, None, True),
]

BASLIK = '''
# ----------------------------------------------- H11 ALT-BOLMESI (FAZ C)
# `_kapi_h11` (48 satir, CC 23) DORT parcaya bolundu; ince `_kapi_h11` en sona konur.
#
#   `_h11_numara`      no tekrari + numara boslugu          -> F
#   `_h11_govde`       durum 'kabul' ama govde bos          -> F   (DONGU ICINDEN)
#   `_h11_baglanti`    yerine-gecme cifti tutarli mi        -> F
#   `_h11_canli_link`  canli hafizanin karar linkleri       -> F
#
# 🔴 SIRA KORUNDU: GOVDE ayri bir donguye alinmadi, BAGLANTI dongusunun icinden
# cagriliyor. Ayri dongu olsaydi hukum sirasi (her ADR icin baglanti+govde)
# yerine (tum baglantilar sonra tum govdeler) olur ve altin kumenin bit-bit
# esdegerlik kapisi kirilirdi. Bolme davranisi degistirmez — sirayi da.
#
# H11 `O` kanalini HIC kullanmaz; `N` yalniz ince ebeveynde. Kanal kapisi bunu
# her kosumda AST ile olcer: KULLANDIGINI TASI, kullanmadigini tasima.
#
# UC KENAR, ucu de imzada:
#     harita   ebeveyn -> BAGLANTI ve CANLI LINK (iki tuketici)
#     k, m     BAGLANTI -> GOVDE (dongu ici)
#     ks       ebeveyn -> NUMARA, BAGLANTI  (ve ebeveynden H12'ye donus)
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
    assert L[H11_DEF - 1] == "def _kapi_h11(F, N, O, y):", L[H11_DEF - 1]
    assert L[H11_LAMBDA - 1] == LAMBDA, repr(L[H11_LAMBDA - 1])
    assert L[H11_YORUM - 1].strip().startswith("# ---- H11 KARAR BUTUNLUGU"), L[H11_YORUM - 1]
    assert L[H11_KS - 1].strip() == "ks = adr_listesi(y)", L[H11_KS - 1]
    assert L[H11_IF - 1].strip() == "if ks:", L[H11_IF - 1]
    assert L[A[0] - 1].strip().startswith('nolar = [k["no"]'), L[A[0] - 1]
    assert L[H11_HARITA - 1].strip() == 'harita = {k["no"]: k for k in ks}', L[H11_HARITA - 1]
    assert L[B[0] - 1].strip() == "for k in ks:", L[B[0] - 1]
    assert L[C[0] - 1].strip().startswith('if m.get("durum") == "kabul"'), L[C[0] - 1]
    assert L[D[0] - 1].strip().startswith("for m in re.findall("), L[D[0] - 1]
    assert L[H11_N - 1].strip().startswith('N.append("H11: %d karar'), L[H11_N - 1]
    assert L[H11_ELSE - 1].strip() == "else:", L[H11_ELSE - 1]
    assert L[H11_N2 - 1].strip().startswith('N.append("H11: henuz karar'), L[H11_N2 - 1]
    assert L[H11_RETURN - 1].strip() == "return ks", L[H11_RETURN - 1]
    assert L[H11_SONRASI - 1].strip() == "" and L[H11_SONRASI].strip() == "", "kuyruk bos degil"

    # --- 1b) KANAL KAPISI ---
    for ad, imza, bolge, _, _ in PARCALAR:
        gerekli = kanallar(ham, bolge[0], bolge[1])
        var = {p.strip() for p in imza.split("(", 1)[1].rstrip("):").split(",")}
        eksik = gerekli - var
        if eksik:
            print("KIRMIZI: %s bolgesi %s kanalini kullaniyor ama imzada YOK: %s"
                  % (ad, ",".join(sorted(eksik)), imza))
            return 1
        print("  kanal kapisi: %-18s kullanilan %-7s imza TASIYOR"
              % (ad, ",".join(sorted(gerekli)) or "(SAF)"))

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H11_DEF - 1]
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

    yeni.append(L[H11_DEF - 1])                  # def _kapi_h11(...)  BIREBIR
    yeni.append(L[H11_YORUM - 1])                # yorum               BIREBIR
    yeni.append(L[H11_KS - 1])                   # ks = adr_listesi(y) BIREBIR
    yeni.append(L[H11_IF - 1])                   # if ks:              BIREBIR
    yeni.append(L[H11_HARITA - 1])               # harita = {...}      BIREBIR
    yeni.append("        _h11_numara(F, ks)")
    yeni.append("        _h11_baglanti(F, ks, harita)")
    yeni.append("        _h11_canli_link(F, y, harita)")
    yeni.append(L[H11_N - 1])                    # N.append(sayac)     BIREBIR
    yeni.append(L[H11_ELSE - 1])                 # else:               BIREBIR
    yeni.append(L[H11_N2 - 1])                   # N.append(karar yok) BIREBIR
    yeni.append(L[H11_RETURN - 1])               # return ks           BIREBIR

    yeni += L[H11_SONRASI - 1:]
    metin = nl.join(yeni)

    # --- 3) kapilar ---
    compile(metin, "<h11-bolme>", "exec")
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

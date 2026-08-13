#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h4` BOLME URETECI.

`fazC_bolucu_h14.py` kalibinin aynisi (kalip artik sabittir):
  * girdi motorunun SHA256'si kapisi — betik TEK ATIMLIKTIR
  * govdeler ELLE YAZILMAZ, satirlar BIREBIR tasinir; dedent satir basina dogrulanir
  * BOS BOLGE KAPISI: saf donuse cevrilen bolgelerde hukum cagrisi SIFIR olmali
  * hukum haritasi (sira -> kapi etiketi) uretim oncesi/sonrasi karsilastirilir
  * uretilen dosya derlenmezse YAZILMAZ
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

BEKLENEN_SHA = "b0750786bcc45451a53cc0157da8d573a61eb43fbefb2654f6c2d2cd6a0a085a"

H4_DEF = 3265          # def _kapi_h4(F, N, O, kok, y):
H4_LAMBDA = 3266
H4_YORUM = 3267        # # ---- H4 OLU BAGLANTI ---
H4_METIN = 3268        # metin = oku(y.canli)
H4_EKSIK = 3288        # eksik = [...]
H4_IF = 3289           # if eksik:
H4_IC_YORUM = 3290     # "Tasinmis mi, yok mu?" yorumu
H4_SON = 3325
H4_SONRASI = 3326

# (ilk, son, dedent)
A = (3269, 3287, 0)    # ADAYLAR       : backtick + markdown tarama -> aday
B = (3291, 3295, 4)    # HAVUZ         : os.walk -> havuz
C = (3296, 3316, 4)    # SINIFLANDIRMA : olu / tasinmis
D = (3317, 3325, 4)    # HUKUM         : TEK hukum bolgesi (F ve N burada)

SAF_BOLGELER = [("adaylar", 3269, 3287), ("havuz", 3291, 3295),
                ("siniflandirma", 3296, 3316)]

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'

BASLIK = '''
# ------------------------------------------------ H4 ALT-BOLMESI (FAZ C)
# `_kapi_h4` (61 satir, CC 32) DORT parcaya bolundu; ince `_kapi_h4` en sona konur.
# Kalip `_kapi_h14` turunun aynisidir ve gerekceleri de aynidir:
#
# 🔴 SIRA: faz0/sabotaj.py hukum cagrilarini (lineno, col) sirasina gore
# numaralandirir; parcalar kapinin kendi yerinde ve kosum sirasinda durur.
#
# 🔴 UC PARCA F/N/O ALMIYOR: hukum listelerini DONDUREN bir parca yarida
# SystemExit atarsa toplanan bulgu KAYBOLUR (11 Agu 2026 olcumu). Burada koruma
# sokulmuyor: tasinan uc bolgede hukum cagrisi sayisi OLCULDU ve SIFIR — uretec
# her kosumda yeniden olcer ve sifir degilse YAZMAZ. `_h4_hukum` F ve N ALIR.
#
# `fail` ADI DEGISTIRILEMEZ: sabotaj.py AST'te Name.id == "fail" arar.
#
# Parcalar arasi veri DORT KENARDIR ve hepsi imzada gorunur:
#     metin           EBEVEYN       -> ADAYLAR
#     aday            ADAYLAR       -> ebeveyn (eksik listesi ebeveynde uretilir)
#     eksik, havuz    EBEVEYN/HAVUZ -> SINIFLANDIRMA
#     olu, tasinmis   SINIFLANDIRMA -> HUKUM
'''.strip("\n")


def hukum_haritasi(kaynak):
    """[(sira, kapi_etiketi)] — sabotaj.py ile AYNI siralama kurali."""
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


def hukum_cagrilari(kaynak, bas, son):
    """Bolgedeki fail(...) VE F/N/O.append(...) cagrilari."""
    agac = ast.parse(kaynak)
    bulunan = []
    for d in ast.walk(agac):
        if not isinstance(d, ast.Call) or not (bas <= getattr(d, "lineno", 0) <= son):
            continue
        f = d.func
        ad = None
        if isinstance(f, ast.Name):
            ad = f.id
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            ad = "%s.%s" % (f.value.id, f.attr)
        if ad == "fail" or ad in ("F.append", "N.append", "O.append"):
            bulunan.append((d.lineno, ad))
    return sorted(bulunan)


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
    assert L[H4_DEF - 1] == "def _kapi_h4(F, N, O, kok, y):", L[H4_DEF - 1]
    assert L[H4_LAMBDA - 1] == LAMBDA, repr(L[H4_LAMBDA - 1])
    assert L[H4_YORUM - 1].strip().startswith("# ---- H4 OLU BAGLANTI"), L[H4_YORUM - 1]
    assert L[H4_METIN - 1].strip() == "metin = oku(y.canli)", L[H4_METIN - 1]
    assert L[A[0] - 1].strip().startswith("# Yalniz TAM backtick"), L[A[0] - 1]
    assert L[3270 - 1].strip() == "aday = set()", L[3270 - 1]
    assert L[H4_EKSIK - 1].strip().startswith("eksik = [p for p in sorted(aday)"), L[H4_EKSIK - 1]
    assert L[H4_IF - 1].strip() == "if eksik:", L[H4_IF - 1]
    assert L[H4_IC_YORUM - 1].strip().startswith("# Tasinmis mi"), L[H4_IC_YORUM - 1]
    assert L[B[0] - 1].strip() == "havuz = {}", L[B[0] - 1]
    assert L[C[0] - 1].strip().startswith("# SESSIZ KIRPMA YOK"), L[C[0] - 1]
    assert L[D[0] - 1].strip().startswith("for p0, yer in tasinmis[:5]:"), L[D[0] - 1]
    assert L[H4_SON - 1].strip().endswith("% (len(olu) - 10))"), L[H4_SON - 1]
    assert L[H4_SONRASI - 1].strip() == "" and L[H4_SONRASI].strip() == "", "kuyruk bos degil"
    assert L[H4_SONRASI + 1].startswith("def _kapi_h5("), L[H4_SONRASI + 1]

    # --- 1b) BOS BOLGE KAPISI ---
    kirletmis = [(ad, bas, son, hukum_cagrilari(ham, bas, son))
                 for ad, bas, son in SAF_BOLGELER]
    kirletmis = [x for x in kirletmis if x[3]]
    if kirletmis:
        print("KIRMIZI: saf donuse cevrilecek bolgede HUKUM CAGRISI var.")
        for ad, bas, son, c in kirletmis:
            print("  %s (%d-%d): %s" % (ad, bas, son, c))
        return 1
    print("bos bolge kapisi: 3 bolgede hukum cagrisi = 0 (OLCULDU)")

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H4_DEF - 1]
    yeni += BASLIK.split("\n")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h4_adaylar(metin):")
    yeni += tasi(L, A)
    yeni.append("    return aday")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h4_havuz(kok):")
    yeni += tasi(L, B)
    yeni.append("    return havuz")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h4_siniflandir(eksik, havuz):")
    yeni += tasi(L, C)
    yeni.append("    return olu, tasinmis")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h4_hukum(F, N, olu, tasinmis):")
    yeni.append(LAMBDA)
    yeni += tasi(L, D)
    yeni.append("")
    yeni.append("")

    yeni.append(L[H4_DEF - 1])                    # def _kapi_h4(...)   BIREBIR
    yeni.append(L[H4_YORUM - 1])                  # yorum               BIREBIR
    yeni.append(L[H4_METIN - 1])                  # metin = oku(...)    BIREBIR
    yeni.append("    aday = _h4_adaylar(metin)")
    yeni.append(L[H4_EKSIK - 1])                  # eksik = [...]       BIREBIR
    yeni.append(L[H4_IF - 1])                     # if eksik:           BIREBIR
    yeni.append(L[H4_IC_YORUM - 1])               # ic yorum            BIREBIR
    yeni.append("        havuz = _h4_havuz(kok)")
    yeni.append("        olu, tasinmis = _h4_siniflandir(eksik, havuz)")
    yeni.append("        _h4_hukum(F, N, olu, tasinmis)")

    # --- 3) dokunulmayan kuyruk ---
    yeni += L[H4_SONRASI - 1:]
    metin = nl.join(yeni)

    # --- 4) kapilar ---
    compile(metin, "<h4-bolme>", "exec")
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

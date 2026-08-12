#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h1` BOLME URETECI.

`fazC_bolucu.py`'nin kalibini izler ve ayni gerekceye dayanir: govdeler ELLE
YENIDEN YAZILMAZ, kaynak satirlar BIREBIR tasinir. Tek fark, tasinan satirlarin
girintisinin TEKDUZE bir miktar azaltilmasidir (govdenin tamami tek bir
`if os.path.isfile(y.snap):` icinde yasiyordu). Dedent mekaniktir ve satir
basina DOGRULANIR: her bos olmayan satirin en az o kadar bosluk ile basladigi
iddia edilir, yoksa betik durur.

Ureteci calistirmadan once ve sonra dogrular:
  * girdi motorunun SHA256'si beklenen mi (bu betik TEK ATIMLIKTIR)
  * bolum sinirlari, def satiri, koruma satiri ve girinti degismemis mi
  * hukum cagrisi sayisi ve (sira -> kapi etiketi) eslemesi DEGISMEDI
  * uretilen dosya derleniyor
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

# Bu betik TEK ATIMLIKTIR ve satir numaralarina baglidir; yalnizca asagidaki
# SHA'ya sahip motora uygulanabilir. Baska bir girdiye uygulanirsa satirlar
# kayar ve sessizce YANLIS bir dosya uretir — bu yuzden kapi ONCE gelir.
BEKLENEN_SHA = "480cbd529b65f0071ea764cb9c337aa989abde3537fbd40718739046c7279640"

H1_DEF = 3063          # def _kapi_h1(F, N, O, kok, rc, y, siki):
H1_LAMBDA = 3064       # fail tanimi
H1_YORUM = 3065        # # ---- H1 BUTUNLUK + KOVA ----
H1_KORUMA = 3066       # if os.path.isfile(y.snap):
H1_SON = 3188          # kapinin son satiri
H1_SONRASI = 3189      # buradan sonrasi dokunulmaz (iki bos satir + def _kapi_h2)

# (ad, ilk, son, dedent)
A = (3067, 3086, 4)    # BEYAN  : snapshot + duzeltmeler + yeniler -> bekle
B = (3088, 3104, 4)    # GERCEK : canli + arsiv (yalitimli)        -> var
C = (3105, 3133, 4)    # FARK   : KAYIP / BEYANSIZ EKLENMIS
D1 = (3134, 3144, 4)   # KOVA sarmalayici: koruma + kv okuma/dogrulama
DBEK = (3145, 3166, 8) # KOVA beklenen listesi — SAF (hukum cagrisi YOK)
D2 = (3167, 3188, 4)   # KOVA: tasinma karsilastirmasi + kacan + hedef

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'

BASLIK = '''
# ------------------------------------------------ H1 ALT-BOLMESI (FAZ C)
# `_kapi_h1` (126 satir, CC 54) bes parcaya bolundu. Parcalar KAPININ KENDI
# YERINDE ve KOSUM SIRASINDA durur; ince `_kapi_h1` en sona konur.
#
# 🔴 SIRA NEDEN BOYLE: faz0/sabotaj.py her hukum cagrisini (lineno, col)
# sirasina gore numaralandirir ve 61 maddelik kapsam envanteri o numaralara
# baglidir. Parcalar baska bir sirayla yazilirsa numaralandirma kayar ve
# envanter karsilastirilamaz hale gelir — yani olcum kaybolur.
#
# 🔴 F/N/O NEDEN HALA PARAMETRE: 11 Agu 2026'da olculdu ve geri alindi —
# saf donus biciminde bir parca yarida SystemExit atarsa o ana kadar
# toplanan hukum yerel listede kalir ve KAYBOLUR. Koruma kanitsiz sokulmez.
#
# TEK ISTISNA `_h1_kova_bek`: o blokta HIC hukum cagrisi yoktur (olculdu:
# 0 adet), dolayisiyla kaybedilecek bulgu da yoktur. Saflik orada bir tercih
# degil, olcumle guvenli kilinmis bir sadelestirmedir.
#
# `fail` ADI DEGISTIRILEMEZ: sabotaj.py cagrilari AST'te Name.id == "fail"
# diye arar. Ad degisirse hicbir hedef bulunmaz ve kapsam envanteri sessizce
# 0'a duser.
#
# Parcalar arasi veri TAM DORT KENARDIR ve hepsi imzada gorunur:
#     bekle  BEYAN -> FARK        snapL, duz  BEYAN -> KOVA
#     var    GERCEK -> FARK       canliA      GERCEK -> KOVA
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


def tasi(L, parca):
    """Satirlari BIREBIR tasir, yalnizca tekduze girintiyi azaltir.

    Her bos olmayan satirin en az `dedent` kadar bosluk ile basladigi
    DOGRULANIR; aksi halde betik durur (sessiz bozma yok)."""
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
        print("  beklenen: %s" % BEKLENEN_SHA)
        print("  bulunan : %s" % sha)
        print("  Bu betik TEK ATIMLIKTIR (satir numaralarina bagli).")
        return 2

    ham = open(KAYNAK, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in ham else "\n"
    L = ham.split(nl)
    onceki = hukum_haritasi(ham)

    # --- 1) yapisal dogrulama ---
    assert L[H1_DEF - 1] == "def _kapi_h1(F, N, O, kok, rc, y, siki):", L[H1_DEF - 1]
    assert L[H1_LAMBDA - 1] == LAMBDA, repr(L[H1_LAMBDA - 1])
    assert L[H1_YORUM - 1].strip().startswith("# ---- H1 "), L[H1_YORUM - 1]
    assert L[H1_KORUMA - 1].strip() == "if os.path.isfile(y.snap):", L[H1_KORUMA - 1]
    assert L[3087 - 1].strip() == "", "A ile B arasi bos degil"
    assert L[H1_SON - 1].strip().endswith("len(yok)))"), L[H1_SON - 1]
    assert L[H1_SONRASI - 1].strip() == "" and L[H1_SONRASI].strip() == "", "kuyruk bos degil"
    assert L[H1_SONRASI + 1].startswith("def _kapi_h2("), L[H1_SONRASI + 1]

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H1_DEF - 1]                       # 1..3062 dokunulmaz
    yeni += BASLIK.split("\n")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h1_beyan(F, y):")
    yeni.append(LAMBDA)
    yeni += tasi(L, A)
    yeni.append("    return snapL, bekle, duz")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h1_gercek(F, O, kok, rc, y):")
    yeni.append(LAMBDA)
    yeni += tasi(L, B)
    yeni.append("    return canliA, var")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h1_fark(F, N, y, siki, bekle, var):")
    yeni.append(LAMBDA)
    yeni += tasi(L, C)
    yeni.append("")
    yeni.append("")

    yeni.append("def _h1_kova_bek(kv, snapL, duz):")
    yeni += tasi(L, DBEK)
    yeni.append("    return bek")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h1_kova(F, y, snapL, duz, canliA):")
    yeni.append(LAMBDA)
    yeni += tasi(L, D1)
    yeni.append("        bek = _h1_kova_bek(kv, snapL, duz)")
    yeni += tasi(L, D2)
    yeni.append("")
    yeni.append("")

    yeni.append("def _kapi_h1(F, N, O, kok, rc, y, siki):")
    yeni.append(L[H1_YORUM - 1])
    yeni.append("    if not os.path.isfile(y.snap):")
    yeni.append("        return")
    yeni.append("    snapL, bekle, duz = _h1_beyan(F, y)")
    yeni.append("    canliA, var = _h1_gercek(F, O, kok, rc, y)")
    yeni.append("    _h1_fark(F, N, y, siki, bekle, var)")
    yeni.append("    _h1_kova(F, y, snapL, duz, canliA)")

    # --- 3) dokunulmayan kuyruk ---
    yeni += L[H1_SONRASI - 1:]

    metin = nl.join(yeni)

    # --- 4) kapilar ---
    compile(metin, "<h1-bolme>", "exec")
    sonraki = hukum_haritasi(metin)
    if onceki != sonraki:
        print("KIRMIZI: hukum haritasi DEGISTI.")
        print("  once  : %d madde" % len(onceki))
        print("  sonra : %d madde" % len(sonraki))
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

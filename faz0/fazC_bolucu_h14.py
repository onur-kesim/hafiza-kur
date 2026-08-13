#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h14` BOLME URETECI.

`fazC_bolucu_h1.py`'nin kalibini izler ve ayni gerekceye dayanir: govdeler ELLE
YENIDEN YAZILMAZ, kaynak satirlar BIREBIR tasinir. Tasinan satirlarin girintisi
TEKDUZE 4 bosluk azaltilir (govdenin tamami `else:` icinde, girinti 8'de
yasiyordu). Dedent mekaniktir ve satir basina DOGRULANIR.

H1'DEN TEK FARK — BIR KAPI DAHA: H1'de parcalarin hepsi F/N/O aliyordu; burada
uc parca ALMIYOR. Bu bir tercih degil, olculmus bir hukumdur ve uretec her
kosumda yeniden olcer (`bos_bolge_kapisi`): tasinan uc bolgede hukum cagrisi
(fail / F.append / N.append / O.append) sayisi SIFIR olmalidir. Sifir degilse
uretec YAZMAZ — cunku o zaman "saf donus" bicimi kismi ciktiyi soker
(11 Agu 2026'da `_kapi_govde` bolmesinde olculdu).

Ureteci calistirmadan once ve sonra dogrular:
  * girdi motorunun SHA256'si beklenen mi (bu betik TEK ATIMLIKTIR)
  * bolum sinirlari, def satiri, dal satirlari ve girinti degismemis mi
  * tasinan uc bolgede hukum cagrisi SIFIR mi  (bu betige OZGU kapi)
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
BEKLENEN_SHA = "b954e0cbf772b3c72ae974f94c50f55780f763f6e8d121c355d56a2a2f9a0ec5"

H14_DEF = 3755         # def _kapi_h14(F, N, O, kok, rc, y, t_son):
H14_LAMBDA = 3756      # fail tanimi
H14_YORUM = 3757       # # ---- H14 DISIPLIN ...
H14_GECIKME = 3758     # gecikme = rc["hafiza_gecikme_gun"]
H14_IF = 3759          # if gecikme <= 0:
H14_O1 = 3760          # O.append(... KAPALI ...)
H14_ELIF = 3761        # elif not t_son:
H14_O2 = 3762          # O.append(... OLCULEMIYOR ...)
H14_ELSE = 3763        # else:
H14_SON = 3858         # kapinin son satiri
H14_SONRASI = 3859     # buradan sonrasi dokunulmaz

# (ilk, son, dedent)
A = (3765, 3805, 4)    # GIT DURUMU  : kirli/izlenen siniflari      -> git_var, kirli, izlenen
B1 = (3764, 3764, 4)   # ADAY TARAMA : `haric` kumesi (walk'in girdisi)
B2 = (3806, 3820, 4)   # ADAY TARAMA : os.walk                      -> adaylar
C = (3821, 3843, 4)    # EN YENI     : siniflandirma + toplu git log -> en_yeni_t, en_yeni_f
D = (3844, 3858, 4)    # HUKUM       : TEK hukum bolgesi (F ve N burada)

# Hukum cagrisi TASIMAMASI gereken bolgeler (bu betige ozgu kapi).
SAF_BOLGELER = [("git durumu", 3765, 3805), ("aday tarama", 3764, 3764),
                ("aday tarama", 3806, 3820), ("en yeni tarih", 3821, 3843)]

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'

BASLIK = '''
# ----------------------------------------------- H14 ALT-BOLMESI (FAZ C)
# `_kapi_h14` (104 satir, CC 35) DORT parcaya bolundu. Parcalar KAPININ KENDI
# YERINDE ve KOSUM SIRASINDA durur; ince `_kapi_h14` en sona konur.
#
# 🔴 SIRA NEDEN BOYLE: faz0/sabotaj.py her hukum cagrisini (lineno, col)
# sirasina gore numaralandirir ve kapsam envanteri o numaralara baglidir.
# Parcalar baska bir sirayla yazilirsa numaralandirma kayar ve olcum
# karsilastirilamaz hale gelir.
#
# 🔴 UC PARCA NEDEN F/N/O ALMIYOR: 11 Agu 2026'da olculdu ve geri alindi —
# hukum listelerini DONDUREN bir parca yarida SystemExit atarsa o ana kadar
# toplanan bulgu KAYBOLUR. Koruma kanitsiz sokulmez; burada da sokulmuyor.
# Tasinan uc bolgede (git durumu · aday tarama · en yeni tarih) hukum cagrisi
# sayisi OLCULDU ve SIFIR — uretec bunu her kosumda yeniden olcer ve sifir
# degilse YAZMAZ. Kaybedilecek bulgu olmadigi icin saflik bir tercih degil,
# olcumle guvenli kilinmis bir sadelestirmedir (`_h1_kova_bek` ile ayni gerekce).
# `_h14_hukum` ise F ve N ALIR: butun fail()/N.append cagrilari orada yasar.
#
# `fail` ADI DEGISTIRILEMEZ: sabotaj.py cagrilari AST'te Name.id == "fail"
# diye arar. Ad degisirse hicbir hedef bulunmaz ve kapsam envanteri sessizce
# 0'a duser.
#
# Parcalar arasi veri TAM BES KENARDIR ve hepsi imzada gorunur:
#     git_var, kirli, izlenen   GIT DURUMU  -> EN YENI
#     adaylar                   ADAY TARAMA -> EN YENI
#     en_yeni_t, en_yeni_f      EN YENI     -> HUKUM
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
    """[bolgedeki (satir, ad)] — fail(...) VE F/N/O.append(...) cagrilari.

    `hukum_haritasi` yalniz `fail`i sayar (sabotaj.py'nin kurali). Kismi cikti
    sorusu icin bu yetmez: `N.append` / `O.append` de hukumdur ve saf donus
    biciminde ayni sekilde kaybolur. Bu yuzden bolge kapisi ikisini de arar."""
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
    assert L[H14_DEF - 1] == "def _kapi_h14(F, N, O, kok, rc, y, t_son):", L[H14_DEF - 1]
    assert L[H14_LAMBDA - 1] == LAMBDA, repr(L[H14_LAMBDA - 1])
    assert L[H14_YORUM - 1].strip().startswith("# ---- H14 DISIPLIN"), L[H14_YORUM - 1]
    assert L[H14_GECIKME - 1].strip() == 'gecikme = rc["hafiza_gecikme_gun"]', L[H14_GECIKME - 1]
    assert L[H14_IF - 1].strip() == "if gecikme <= 0:", L[H14_IF - 1]
    assert L[H14_O1 - 1].strip().startswith("O.append("), L[H14_O1 - 1]
    assert L[H14_ELIF - 1].strip() == "elif not t_son:", L[H14_ELIF - 1]
    assert L[H14_O2 - 1].strip().startswith("O.append("), L[H14_O2 - 1]
    assert L[H14_ELSE - 1].strip() == "else:", L[H14_ELSE - 1]
    assert L[B1[0] - 1].strip().startswith('haric = {".git"'), L[B1[0] - 1]
    assert L[A[0] - 1].strip().startswith("# Fable Bulgu 9"), L[A[0] - 1]
    assert L[3783 - 1].strip().startswith('git_var = bool(shutil.which("git"))'), L[3783 - 1]
    assert L[B2[0] - 1].strip().startswith("adaylar = []"), L[B2[0] - 1]
    assert L[C[0] - 1].strip() == "en_yeni_t, en_yeni_f = None, None", L[C[0] - 1]
    assert L[3832 - 1].strip() == "if temiz:", L[3832 - 1]
    assert L[D[0] - 1].strip() == "if en_yeni_t is None:", L[D[0] - 1]
    assert L[H14_SON - 1].strip().endswith("t_son.isoformat()))"), L[H14_SON - 1]
    assert L[H14_SONRASI - 1].strip() == "" and L[H14_SONRASI].strip() == "", "kuyruk bos degil"
    assert "ISIRMA KANITI" in L[H14_SONRASI + 1], L[H14_SONRASI + 1]

    # --- 1b) BOS BOLGE KAPISI (bu betige ozgu) ---
    # Saf donuse cevrilen bolgeler hukum TASIMAMALI. Tasiyorlarsa kismi cikti
    # garantisi sokuluyor demektir ve uretec YAZMAZ.
    kirletmis = []
    for ad, bas, son in SAF_BOLGELER:
        c = hukum_cagrilari(ham, bas, son)
        if c:
            kirletmis.append((ad, bas, son, c))
    if kirletmis:
        print("KIRMIZI: saf donuse cevrilecek bolgede HUKUM CAGRISI var.")
        for ad, bas, son, c in kirletmis:
            print("  %s (%d-%d): %s" % (ad, bas, son, c))
        print("  Saf bicim bu bulgulari yarida kesilmede KAYBEDER (11 Agu 2026 olcumu).")
        return 1
    print("bos bolge kapisi: 4 bolgede hukum cagrisi = 0 (OLCULDU)")

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H14_DEF - 1]                      # 1..3754 dokunulmaz
    yeni += BASLIK.split("\n")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h14_git_durumu(kok):")
    yeni += tasi(L, A)
    yeni.append("    return git_var, kirli, izlenen")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h14_adaylar(kok, y):")
    yeni += tasi(L, B1)
    yeni += tasi(L, B2)
    yeni.append("    return adaylar")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h14_en_yeni(kok, adaylar, git_var, kirli, izlenen):")
    yeni += tasi(L, C)
    yeni.append("    return en_yeni_t, en_yeni_f")
    yeni.append("")
    yeni.append("")

    yeni.append("def _h14_hukum(F, N, gecikme, t_son, en_yeni_t, en_yeni_f):")
    yeni.append(LAMBDA)
    yeni += tasi(L, D)
    yeni.append("")
    yeni.append("")

    yeni.append(L[H14_DEF - 1])                   # def _kapi_h14(...)  BIREBIR
    yeni.append(L[H14_YORUM - 1])                 # yorum satiri        BIREBIR
    yeni.append(L[H14_GECIKME - 1])               # gecikme = ...       BIREBIR
    yeni.append(L[H14_IF - 1])                    # if gecikme <= 0:    BIREBIR
    yeni.append(L[H14_O1 - 1])                    # O.append(...)       BIREBIR
    yeni.append(L[H14_ELIF - 1])                  # elif not t_son:     BIREBIR
    yeni.append(L[H14_O2 - 1])                    # O.append(...)       BIREBIR
    yeni.append(L[H14_ELSE - 1])                  # else:               BIREBIR
    yeni.append("        git_var, kirli, izlenen = _h14_git_durumu(kok)")
    yeni.append("        adaylar = _h14_adaylar(kok, y)")
    yeni.append("        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, adaylar, git_var, kirli, izlenen)")
    yeni.append("        _h14_hukum(F, N, gecikme, t_son, en_yeni_t, en_yeni_f)")

    # --- 3) dokunulmayan kuyruk ---
    yeni += L[H14_SONRASI - 1:]

    metin = nl.join(yeni)

    # --- 4) kapilar ---
    compile(metin, "<h14-bolme>", "exec")
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

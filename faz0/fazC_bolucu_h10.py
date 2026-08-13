#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C ALT-BOLME — `_kapi_h10` BOLME URETECI.

Kalip h14/h4 ile aynidir; TEK FARK BIR KAPININ GENISLETILMESIDIR.

🔴 BOS BOLGE KAPISI -> KANAL KAPISI (bu betikte genelestirildi)
h14 ve h4'te tasinan bolgelerde hukum cagrisi SIFIRDI, dolayisiyla parcalar saf
donebiliyordu ve uretec "sifir mi" diye soruyordu. H10'da durum TERSTIR: dort
bolgenin DORDU de hukum basar (fail · F.append · O.append). Burada "sifir mi"
sorusu anlamsiz olurdu; sorulmasi gereken sudur:

    bir bolge hangi HUKUM KANALLARINI kullaniyorsa, o parcanin IMZASI o kanallari
    TASIMAK ZORUNDADIR.

Uretec bunu AST ile olcer: `fail`/`F.append` -> F · `N.append` -> N ·
`O.append` -> O. Imza eksikse dosya YAZILMAZ. Boylece 11 Agu 2026'da olculen
kismi-cikti kaybi (saf donuse cevrilen bir parcanin bulgusunun SystemExit'te
kaybolmasi) mekanik olarak imkansizlasir — hem bos hem dolu bolgede.
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

BEKLENEN_SHA = "fb64f25a907e7275c0f0a6882e913156166a7e0c5f4a553770012125a431354c"

H10_DEF = 3537         # def _kapi_h10(F, N, O, y):
H10_LAMBDA = 3538
H10_YORUM = 3539       # # ---- H10 KONU TEKILLIGI ...
H10_N = 3609           # N.append("H10: %d blok / %d ayrik konu" ...)
H10_RETURN = 3617      # return bl
H10_SONRASI = 3618

# (ilk, son, dedent) — govde satirlari zaten fonksiyon govdesi girintisinde (4),
# hedef de fonksiyon govdesi oldugu icin dedent 0'dir.
A = (3540, 3548, 0)    # TEKILLIK : canli bloklar + konu sayimi   -> bl, say
B = (3549, 3584, 0)    # CIT      : kod citi · girintili · gizli  -> _ham
C = (3585, 3608, 0)    # YAPI     : blok acilis/kapanis taramasi
D = (3610, 3616, 0)    # SOZLUK   : KONULAR.md tanimliligi

LAMBDA = '    fail = lambda k, m: F.append("[%s] %s" % (k, m))'

# (ad, imza, bolge, kuyruk satiri)
PARCALAR = [
    ("_h10_tekillik", "def _h10_tekillik(F, y):", A, "    return bl, say"),
    ("_h10_cit", "def _h10_cit(F, O, y):", B, "    return _ham"),
    ("_h10_yapi", "def _h10_yapi(F, _ham):", C, None),
    ("_h10_sozluk", "def _h10_sozluk(F, y, say):", D, None),
]

BASLIK = '''
# ----------------------------------------------- H10 ALT-BOLMESI (FAZ C)
# `_kapi_h10` (81 satir, CC 27) DORT parcaya bolundu; ince `_kapi_h10` en sona konur.
#
# 🔴 BURADA PARCALAR SAF DEGIL — VE OLMAMALI. h14/h4'te tasinan bolgelerde hukum
# cagrisi sifirdi; H10'da dordu de hukum basar. Bu yuzden hepsi F alir, `_h10_cit`
# ayrica O alir (kod bolgesinde gizlenen bloklar icin OLCULEMEDI hukmu basar).
# Gerekce 11 Agu 2026'da olculdu: hukum listesini DONDUREN bir parca yarida
# SystemExit atarsa o ana kadar toplanan bulgu KAYBOLUR. Uretec bunu artik
# mekanik olarak dogrular (KANAL KAPISI): bolgenin kullandigi her hukum kanali
# parcanin imzasinda BULUNMAK ZORUNDA.
#
# 🔴 `N.append` EBEVEYNDE KALDI: "%d blok / %d ayrik konu" notu YAPI taramasindan
# SONRA, SOZLUK denetiminden ONCE basilir. Sira sozlesmedir (faz0/sabotaj.py
# hukum cagrilarini lineno sirasina gore numaralandirir), bu yuzden not satiri
# tasinmadi — oldugu yerde, iki cagri arasinda duruyor.
#
# Parcalar arasi veri UC KENARDIR ve hepsi imzada gorunur:
#     bl    TEKILLIK -> ebeveyn (donus degeri)
#     say   TEKILLIK -> SOZLUK
#     _ham  CIT      -> YAPI
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
    """Bolgenin kullandigi HUKUM KANALLARI: {'F','N','O'} alt kumesi."""
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
    assert L[H10_DEF - 1] == "def _kapi_h10(F, N, O, y):", L[H10_DEF - 1]
    assert L[H10_LAMBDA - 1] == LAMBDA, repr(L[H10_LAMBDA - 1])
    assert L[H10_YORUM - 1].strip().startswith("# ---- H10 KONU TEKILLIGI"), L[H10_YORUM - 1]
    assert L[A[0] - 1].strip() == "bl = canli_bloklar(y)", L[A[0] - 1]
    assert L[B[0] - 1].strip().startswith("# Fable Bulgu 6"), L[B[0] - 1]
    assert L[C[0] - 1].strip().startswith("acik, hatali, asilan = None, [], None"), L[C[0] - 1]
    assert L[H10_N - 1].strip().startswith('N.append("H10: %d blok'), L[H10_N - 1]
    assert L[D[0] - 1].strip().startswith("if os.path.isfile(y.konular):"), L[D[0] - 1]
    assert L[H10_RETURN - 1].strip() == "return bl", L[H10_RETURN - 1]
    assert L[H10_SONRASI - 1].strip() == "" and L[H10_SONRASI].strip() == "", "kuyruk bos degil"
    assert L[H10_SONRASI + 1].startswith("def _kapi_h11("), L[H10_SONRASI + 1]

    # --- 1b) KANAL KAPISI ---
    for ad, imza, bolge, _ in PARCALAR:
        gerekli = kanallar(ham, bolge[0], bolge[1])
        var = {p.strip() for p in imza.split("(", 1)[1].rstrip("):").split(",")}
        eksik = gerekli - var
        if eksik:
            print("KIRMIZI: %s bolgesi %s kanalini kullaniyor ama imzada YOK: %s"
                  % (ad, ",".join(sorted(eksik)), imza))
            print("  Saf/eksik imza, yarida kesilmede o kanalin bulgusunu KAYBEDER.")
            return 1
        print("  kanal kapisi: %-14s kullanilan %-9s imza TASIYOR"
              % (ad, ",".join(sorted(gerekli)) or "(yok)"))

    # --- 2) yeni parcalar ---
    yeni = []
    yeni += L[: H10_DEF - 1]
    yeni += BASLIK.split("\n")
    yeni.append("")
    yeni.append("")
    for ad, imza, bolge, kuyruk in PARCALAR:
        yeni.append(imza)
        yeni.append(LAMBDA)
        yeni += tasi(L, bolge)
        if kuyruk:
            yeni.append(kuyruk)
        yeni.append("")
        yeni.append("")

    yeni.append(L[H10_DEF - 1])                  # def _kapi_h10(...)  BIREBIR
    yeni.append(L[H10_YORUM - 1])                # yorum               BIREBIR
    yeni.append("    bl, say = _h10_tekillik(F, y)")
    yeni.append("    _ham = _h10_cit(F, O, y)")
    yeni.append("    _h10_yapi(F, _ham)")
    yeni.append(L[H10_N - 1])                    # N.append(...)       BIREBIR
    yeni.append("    _h10_sozluk(F, y, say)")
    yeni.append(L[H10_RETURN - 1])               # return bl           BIREBIR

    # --- 3) dokunulmayan kuyruk ---
    yeni += L[H10_SONRASI - 1:]
    metin = nl.join(yeni)

    # --- 4) kapilar ---
    compile(metin, "<h10-bolme>", "exec")
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

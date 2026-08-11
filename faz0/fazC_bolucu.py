#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C — _kapi_govde BOLME URETECI.

Govdeler ELLE YENIDEN YAZILMAZ: kaynak satirlar BIREBIR tasinir. Elle yazim
bit-bit esdegerligi bir yazim hatasiyla kaybettirir; bu betik o riski kaldirir.

Ureteci calistirmadan once ve sonra AST duzeyinde dogrular:
  * fail() cagri sayisi ve (sira -> kapi etiketi) eslemesi DEGISMEDI
  * yeni dosya derleniyor
"""
import ast
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

# (ad, ilk satir, son satir, parametreler, ek donus degeri)
BOLUMLER = [
    ("h0",  2970, 2992, ["y"],                       None),
    ("h1",  2994, 3117, ["kok", "rc", "y", "siki"],  None),
    ("h2",  3119, 3127, ["rc", "y"],                 None),
    ("h3",  3129, 3133, ["rc", "y"],                 None),
    ("h4",  3135, 3193, ["kok", "y"],                None),
    ("h5",  3195, 3224, ["rc", "y"],                 None),
    ("h6",  3226, 3244, ["y"],                       None),
    ("h7",  3246, 3263, ["rc", "y"],                 None),
    ("h8",  3265, 3308, ["kok", "y"],                None),
    ("h9",  3310, 3347, ["kok", "y"],                None),
    ("h10", 3349, 3426, ["y"],                       "bl"),
    ("h11", 3428, 3472, ["y"],                       "ks"),
    ("h12", 3474, 3516, ["rc", "y", "bl", "ks"],     "t_son"),
    ("h13", 3518, 3534, ["kok", "rc", "y"],          None),
    ("h15", 3537, 3588, ["rc", "y"],                 None),
    ("h14", 3590, 3691, ["kok", "rc", "y", "t_son"], None),
]

PRE_BAS, PRE_SON = 2950, 2968      # ortak baglam + erken cikis kapilari
GOVDE_DEF = 2949                   # def _kapi_govde(a, F, N, O):
GOVDE_RETURN = 3693                # bare return
EK_BAS = 3694                      # buradan sonrasi dokunulmaz

CAGRI = {
    "h0":  "_kapi_h0(F, N, O, y)",
    "h1":  "_kapi_h1(F, N, O, kok, rc, y, siki)",
    "h2":  "_kapi_h2(F, N, O, rc, y)",
    "h3":  "_kapi_h3(F, N, O, rc, y)",
    "h4":  "_kapi_h4(F, N, O, kok, y)",
    "h5":  "_kapi_h5(F, N, O, rc, y)",
    "h6":  "_kapi_h6(F, N, O, y)",
    "h7":  "_kapi_h7(F, N, O, rc, y)",
    "h8":  "_kapi_h8(F, N, O, kok, y)",
    "h9":  "_kapi_h9(F, N, O, kok, y)",
    "h10": "bl = _kapi_h10(F, N, O, y)",
    "h11": "ks = _kapi_h11(F, N, O, y)",
    "h12": "t_son = _kapi_h12(F, N, O, rc, y, bl, ks)",
    "h13": "_kapi_h13(F, N, O, kok, rc, y)",
    "h15": "_kapi_h15(F, N, O, rc, y)",
    "h14": "_kapi_h14(F, N, O, kok, rc, y, t_son)",
}

DAGITIM_BASLIK = """
    # ---- KAPILAR -------------------------------------------------------
    # Her kapi AYRI bir fonksiyondur; sira BURADA gorunur ve dosyadaki tanim
    # sirasiyla aynidir — H15'in H14'ten ONCE kosmasi dahil (cikti sirasi
    # sozlesmedir).
    #
    # 🔴 F/N/O NEDEN DISARIDAN VERILIR (kapilar neden "saf" DEGIL):
    # Ilk tasarim her kapinin kendi (bulgular, notlar, olculemedi) uclusunu
    # DONDURMESIYDI. OLCULDU (11 Agu 2026) ve GERI ALINDI: o bicimde bir kapi
    # yarida SystemExit atarsa (or. H0 once CIPA BOZULDU yazar, sonra ayni
    # kapida _ZINCIR.jsonl gecersiz UTF-8 cikip oldur() calisir) kapinin O ANA
    # KADAR TOPLADIGI bulgu yerel listede kalir ve KAYBOLUR.
    #     bolme oncesi : FAIL (2 bulgu) · [H0] CIPA BOZULDU var · exit 1
    #     saf bicimde  : FAIL (1 bulgu) · [H0] KAYIP             · exit 3
    # Yani OLCULMUS BIR KIRMIZI, "hukum yok"a donusuyordu. cmd_kapi'nin kendi
    # sozlesmesi bunun tersini garanti eder: "ne olursa olsun O ANA KADAR
    # TOPLANAN hukum basilir". Saflik bir tercih, o garanti bir KORUMADIR ve
    # korumalar kanitsiz sokulmez. Kapilar toplayiciya DOGRUDAN yazar; boylece
    # bolme oncesiyle ayni liste nesnesi, ayni anda dolar.
    #
    # Uc kapi bir sonrakine veri tasir ve bu bagimlilik IMZADA gizlenemez:
    #     bl  H10 -> H12        ks  H11 -> H12        t_son  H12 -> H14
    # Tuketici yeniden HESAPLAMAZ: canli_bloklar()/adr_listesi() ikinci kez
    # tam tarama demektir ve B-6 (300k satirda kapi < 8 sn) zaten sinirdadir.""".strip("\n")

EKLE_YARDIMCI = ""

BASLIK_YORUM = '''
# --------------------------------------------------------- KAPI GOVDELERI
# FAZ C: her kapi AYRI bir fonksiyondur — girdisi imzasinda gorunur, hukmunu
# imzada verilen toplayiciya (F/N/O) yazar. Hicbiri YAZDIRMAZ (print yok).
# Toplayicinin neden DONUS DEGERI degil de PARAMETRE oldugu _kapi_govde'deki
# KAPILAR blogunda olculmus gerekcesiyle yazilidir: saf donus bicimi, kapi
# yarida kesilirse o ana kadarki bulguyu KAYBEDIYORDU.
#
# NEDEN BURADA (dosyanin sonunda, _kapi_govde'den SONRA): faz0/sabotaj.py her
# hukum cagrisini (lineno, col) sirasina gore numaralandirir ve kapsam
# envanteri o numaralara baglidir. Bu fonksiyonlar _kapi_govde'den ONCE
# tanimlanirsa numaralandirma 3 kayar ve envanter karsilastirilamaz hale gelir.
#
# `fail` ADI DEGISTIRILEMEZ: sabotaj.py cagrilari AST'te Name.id == "fail"
# diye arar. Ad degisirse hicbir hedef bulunmaz ve kapsam envanteri sessizce
# 0'a duser — yani olcum kaybolur, kirmizi gorunmez.
#
# AYRICA: bu blokta ve asagidaki govdelerde, hukum cagrisinin metnini ACIK
# YAZMAKTAN kacinilir. Olculdu (11 Agu 2026): esdegerlik olcutlerinden biri
# duz bir metin aramasidir (grep -c) ve bir YORUM satiri bile onu kaydirir —
# ilk uretimde sayi 61 yerine 63 cikti. Olcut kirilgandir; asil degismez olan
# sabotaj.py'nin AST sayimidir, ama kirilgan olcutu kendi prozanla bozma.
'''.strip("\n")


def fail_haritasi(kaynak):
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


# Bu betik TEK ATIMLIKTIR ve satir numaralarina baglidir: yalnizca asagidaki
# SHA'ya sahip motora uygulanabilir. Baska bir girdiye uygulanirsa satirlar
# kayar ve sessizce YANLIS bir dosya uretir — bu yuzden kapi ONCE gelir.
BEKLENEN_SHA = "a1fc24bbfa7a98aa1cb7cfb6d0427219b13117e618a061c8c7fec6ec802ed62d"


def main():
    import hashlib
    sha = hashlib.sha256(open(KAYNAK, "rb").read()).hexdigest()
    if sha != BEKLENEN_SHA:
        print("OLCULEMEDI: girdi motoru beklenen SHA degil.")
        print("  beklenen: %s" % BEKLENEN_SHA)
        print("  bulunan : %s" % sha)
        print("  Bu betik TEK ATIMLIKTIR (satir numaralarina bagli). Yeni bir bolme")
        print("  gerekiyorsa BOLUMLER tablosu yeniden OLCULMELIDIR.")
        return 2
    ham = open(KAYNAK, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in ham else "\n"
    L = ham.split(nl)          # 0-tabanli; L[i] == kaynagin (i+1). satiri

    onceki = fail_haritasi(ham)

    # --- 1) dogrulama: sinirlar bos, def satiri beklenen ---
    assert L[GOVDE_DEF - 1].startswith("def _kapi_govde("), L[GOVDE_DEF - 1]
    assert L[GOVDE_RETURN - 1].strip() == "return", repr(L[GOVDE_RETURN - 1])
    for _, bas, son, _, _ in BOLUMLER:
        assert L[bas - 2].strip() == "", "bolum oncesi satir bos degil: %d" % (bas - 1)

    # --- 2) yeni _kapi_govde ---
    yeni = []
    yeni += L[: PRE_SON]                      # 1..2968  (def + ortak baglam + kapilar)
    yeni.append("")
    yeni += DAGITIM_BASLIK.split("\n")
    for ad, _, _, _, _ in BOLUMLER:
        yeni.append("    " + CAGRI[ad])
    yeni.append("")
    yeni.append("    return")
    yeni.append("")
    yeni.append("")

    # --- 3) kapi govdeleri (BIREBIR tasinir) ---
    yeni += BASLIK_YORUM.split("\n")
    for ad, bas, son, parametreler, ek in BOLUMLER:
        yeni.append("")
        yeni.append("")
        yeni.append("def _kapi_%s(F, N, O, %s):" % (ad, ", ".join(parametreler)))
        yeni.append('    fail = lambda k, m: F.append("[%s] %s" % (k, m))')
        yeni += L[bas - 1: son]               # <<< BIREBIR
        if ek:
            yeni.append("    return %s" % ek)
    yeni.append("")

    # --- 4) dokunulmayan kuyruk ---
    yeni += L[EK_BAS - 1:]

    metin = nl.join(yeni)

    # --- 5) kapilar: derlenir mi, fail() haritasi ayni mi ---
    compile(metin, "<bolme>", "exec")
    sonraki = fail_haritasi(metin)
    if onceki != sonraki:
        print("KIRMIZI: fail() haritasi DEGISTI.")
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
    print("  fail() : %d -> %d  (sira->kapi eslemesi AYNI)" % (len(onceki), len(sonraki)))
    print("  satir  : %d -> %d" % (len(L), len(yeni)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

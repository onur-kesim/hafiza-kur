#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C — `cmd_kur` BOLME URETECI (cmd_* sinifinin ILK bolmesi).

Kalip `fazC_bolucu_h11.py`dir. UC ONEMLI FARK var ve ucunu de `cmd_*` sinifinin
DOGASI dayatiyor:

1. 🔴 KANAL KAPISI YERINE **ETKI KAPISI**.
   Kapi fonksiyonlari hukmu `F/N/O` listelerine yazar; kanal kapisi "kullandigin
   listeyi imzada TASI" der. `cmd_kur`da oyle bir liste YOKTUR. Etkisi uc yerde
   gorunur ve UCU DE IMZADAN SEZILMEZ:
       DISK   diske yaziyor mu          (yaz · makedirs · copyfile · zincir_halka …)
       CIKTI  stdout'a basiyor mu       (print)
       OLUM   sureci oldurebiliyor mu   (`oldur` — DOGRUDAN ya da BIR SEVIYE DERIN)
   Uctu de AST ile OLCULUR ve uretilen docstring'e YAZILIR. Elle yazilmaz:
   **beyan uretilir, dolayisiyla yalan soyleyemez.** ("Belge de bir arayuzdur ve
   yalan soyleyebilir" dersinin dogrudan uygulamasi.)

2. 🔴 HUKUM HARITASI KAPISI YOK — `cmd_kur` hic `fail()` cagirmaz.
   Onun yerine esdegerlik `cmd_kur_bolme_mutanti.py`de **ETKI IMZASI** ile
   olculur: dokuz proje hali icin (exit, stdout, DISK AGACI MANIFESTOSU) uclusu
   bolme oncesi ve sonrasi BIREBIR AYNI olmalidir. Bu uretec o olcumu YAPMAZ;
   yalniz yapisal kapilari kosar. **Uretec kendi isini adjudike etmez.**

3. 🔴 AD KAPISI (yeni). Kapi bolmelerinde parcalar yalniz `F/N/O` ve birkac ad
   aliyordu; burada yedi parca arasinda `kok · ad · rc · y · yeni_kurulum`
   dolasiyor. Bir parametreyi imzaya koymayi unutmak, uretilen kodun ancak
   KOSTURULUNCA `NameError` vermesi demektir. Uretec her bolgenin SERBEST
   adlarini AST ile cikarir; imza + modul globalleri disinda kalan tek ad varsa
   YAZMAZ. Kosmadan once, uretim aninda yakalanir.

BOLGE HARITASI (yedi parca; sira BIREBIR korunur)
    A _kur_on_kontrol  kok cozumu + v1 izi taramasi        -> OLUM (dogrudan)
    B _kur_rc          ad · .hafizarc · rc · Y             -> DISK, OLUM (dolayli)
    C _kur_kilit       yol on kontrol · kilit · zincir sart-> DISK, OLUM (dolayli)
    D _kur_dizinler    dizin iskeleti                      -> DISK
    E _kur_dosyalar    dosya iskeleti (en buyuk bolge)     -> DISK
    F _kur_halka       arsiv dizini tazele + zincir halkasi-> DISK
    G _kur_rapor       dort satirlik rapor                 -> CIKTI

TEK RAPORCU KURALI: CIKTI ekseni YALNIZ BIR parcada olabilir. Ikinci bir parca
`print` ederse uretec KIRMIZI yanar. Gerekce H5 doktrini: "cikti nereden geliyor"
sorusunun iki cevabi olamaz.

INCE EBEVEYN KURALI: bolmeden sonra `cmd_kur`un GOVDESINDE dogrudan DISK/CIKTI/
OLUM cagrisi KALMAMALIDIR. Kalirsa ebeveyn hala is yapiyordur ve bolme yalancidir.

CIKIS KODU  0 yazildi · 1 KAPI KIRMIZI · 2 OLCULEMEDI
"""
import ast
import hashlib
import sys

KAYNAK = sys.argv[1] if len(sys.argv) > 1 else "skill/scripts/hafiza.py"
HEDEF = sys.argv[2] if len(sys.argv) > 2 else KAYNAK

BEKLENEN_SHA = "9b72160ae6e10bbe3e14f8095983fe1e64bf9ade2c19e8a112704f6aa2b2a7a0"

KUR_DEF = 1564          # def cmd_kur(a):
KUR_SONRASI = 1655      # bos satir, sonra def _arsiv_dizini_tazele

# (bas, son, dedent) — YORUM SATIRLARI BOLGEYE DAHILDIR: olculmus bulgular
# oralarda yaziyor ve bolmede kaybolmalari sessiz bir kayip olurdu.
# DEDENT = 0 ve bu H11'den FARKLI: orada bolgeler `if ks:` icinde (girinti 8)
# oldugu icin 4 dusuruluyordu. `cmd_kur` govdesi zaten girinti 4'te; dusurmek
# fonksiyon govdesini girinti 0'a indirip derlemeyi kirar (olculdu).
A = (1565, 1579, 0)     # kok + v1 izi
B = (1580, 1586, 0)     # ad · rc_p · yeni_kurulum · rc · y
C = (1587, 1602, 0)     # yol_on_kontrol · kilit_al · zincir_butunlugu_sart
D = (1603, 1607, 0)     # dizin iskeleti
E = (1608, 1641, 0)     # dosya iskeleti
F = (1642, 1649, 0)     # arsiv dizini tazele + zincir halkasi
G = (1650, 1654, 0)     # rapor

# (ad, imza, bolge, kuyruk)
PARCALAR = [
    ("_kur_on_kontrol", "def _kur_on_kontrol(a):", A, "    return kok"),
    ("_kur_rc", "def _kur_rc(a, kok):", B, "    return ad, yeni_kurulum, rc, y"),
    ("_kur_kilit", "def _kur_kilit(y, rc, yeni_kurulum):", C, None),
    ("_kur_dizinler", "def _kur_dizinler(kok, rc, y):", D, None),
    ("_kur_dosyalar", "def _kur_dosyalar(ad, rc, y):", E, None),
    ("_kur_halka", "def _kur_halka(y):", F, None),
    ("_kur_rapor", "def _kur_rapor(kok, rc, y):", G, None),
]

EBEVEYN = [
    "def cmd_kur(a):",
    "    kok = _kur_on_kontrol(a)",
    "    ad, yeni_kurulum, rc, y = _kur_rc(a, kok)",
    "    _kur_kilit(y, rc, yeni_kurulum)",
    "    _kur_dizinler(kok, rc, y)",
    "    _kur_dosyalar(ad, rc, y)",
    "    _kur_halka(y)",
    "    _kur_rapor(kok, rc, y)",
]

DISK_ADLARI = {"yaz", "makedirs", "copyfile", "zincir_halka", "kilit_al",
               "_beyan_yeni_satirlar", "_arsiv_dizini_tazele"}
CIKTI_ADLARI = {"print"}


def _cagri_adi(d):
    f = d.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def olum_verenler(kaynak):
    """Govdesinde `oldur(...)` GECEN modul duzeyi fonksiyonlar — DERIVE EDILIR.
    Elle liste tutmak bir beyandir ve bayatlar; burada kaynak kendi listesini verir."""
    agac = ast.parse(kaynak)
    out = set()
    for d in agac.body:
        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for x in ast.walk(d):
                if isinstance(x, ast.Call) and _cagri_adi(x) == "oldur":
                    out.add(d.name)
                    break
    return out


def etki(kaynak, bas, son, olumlu):
    """Bir bolgenin UC EKSENI. AST ile olculur, beyan edilmez."""
    agac = ast.parse(kaynak)
    eksen = set()
    for d in ast.walk(agac):
        if not isinstance(d, ast.Call) or not (bas <= getattr(d, "lineno", 0) <= son):
            continue
        ad = _cagri_adi(d)
        if ad in DISK_ADLARI:
            eksen.add("DISK")
        if ad in CIKTI_ADLARI:
            eksen.add("CIKTI")
        if ad == "oldur":
            eksen.add("OLUM")
        elif ad in olumlu:
            eksen.add("OLUM~")            # bir seviye derin
    return eksen


# Modul duzeyinde HER ZAMAN tanimli olan dunder'lar. Bunlar `ast` ile
# goruleMEZ (atama yok, import yok) ama isim cozumlemede vardirlar.
# Olculdu: bunlar olmadan AD KAPISI `_kur_rapor` icin `__file__` uzerinden
# SAHTE KIRMIZI verdi — ve sahte kirmizi gercek kirmiziyi degersizlestirir (Y-4).
MODUL_DUNDER = {"__file__", "__name__", "__doc__", "__package__", "__spec__",
                "__loader__", "__builtins__", "__debug__", "__path__"}


def _modul_globalleri(kaynak):
    agac = ast.parse(kaynak)
    try:
        g = set(vars(__builtins__)) if hasattr(__builtins__, "__dict__") else set(__builtins__)
    except TypeError:
        g = set(dir(__builtins__))
    g |= MODUL_DUNDER
    for d in agac.body:
        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            g.add(d.name)
        elif isinstance(d, (ast.Import, ast.ImportFrom)):
            for al in d.names:
                g.add((al.asname or al.name).split(".")[0])
        elif isinstance(d, ast.Assign):
            for t in d.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        g.add(n.id)
        elif isinstance(d, ast.AnnAssign) and isinstance(d.target, ast.Name):
            g.add(d.target.id)
    return g


def serbest_adlar(govde_kaynak):
    """Bir parca govdesinde OKUNAN ama icinde ATANMAYAN adlar."""
    agac = ast.parse(govde_kaynak)
    atanan, okunan = set(), set()
    for n in ast.walk(agac):
        if isinstance(n, ast.Name):
            (atanan if isinstance(n.ctx, (ast.Store, ast.Del)) else okunan).add(n.id)
        elif isinstance(n, ast.comprehension):
            for x in ast.walk(n.target):
                if isinstance(x, ast.Name):
                    atanan.add(x.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            for arg in list(getattr(n.args, "args", [])) + list(getattr(n.args, "kwonlyargs", [])):
                atanan.add(arg.arg)
    return okunan - atanan


def imza_adlari(imza):
    ic = imza.split("(", 1)[1].rstrip("):")
    return {p.strip().split("=")[0].strip() for p in ic.split(",") if p.strip()}


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

    # --- 1) YAPISAL DOGRULAMA — capalar ---
    assert L[KUR_DEF - 1] == "def cmd_kur(a):", L[KUR_DEF - 1]
    assert L[A[0] - 1].strip().startswith("kok = os.path.abspath("), L[A[0] - 1]
    assert L[B[0] - 1].strip().startswith("ad = a.ad or"), L[B[0] - 1]
    assert L[C[0] - 1].strip().startswith("# `kur` da yol tiplerini"), L[C[0] - 1]
    assert L[D[0] - 1].strip() == "" and L[D[0]].strip().startswith("for d in ["), L[D[0]]
    assert L[E[0] - 1].strip() == "" and L[E[0]].strip().startswith("if not os.path.isfile(y.canli)")
    assert L[F[0] - 1].strip() == "" and L[F[0]].strip().startswith("# arsiv dizini")
    assert L[G[0] - 1].strip() == "" and L[G[0]].strip().startswith('print("KURULDU:')
    assert L[G[1] - 1].strip().startswith('print("\\nSonraki:'), L[G[1] - 1]
    assert L[KUR_SONRASI - 1].strip() == "", "kuyruk bos degil"

    olumlu = olum_verenler(ham)
    globaller = _modul_globalleri(ham)

    # --- 2) ETKI KAPISI ---
    print("  %-18s %-22s %s" % ("parca", "ETKI (olculdu)", "kapi"))
    etkiler, ciktili = {}, []
    for ad, imza, bolge, _ in PARCALAR:
        e = etki(ham, bolge[0], bolge[1], olumlu)
        etkiler[ad] = e
        par = imza_adlari(imza)
        if "DISK" in e and not ({"y", "kok"} & par):
            print("KIRMIZI: %s DISK'e dokunuyor ama imzasinda ne `y` ne `kok` var: %s" % (ad, imza))
            return 1
        if "CIKTI" in e:
            ciktili.append(ad)
        print("  %-18s %-22s %s" % (ad, ",".join(sorted(e)) or "(SAF)", "tamam"))

    if len(ciktili) != 1:
        print("KIRMIZI: CIKTI ekseni tam BIR parcada olmali; bulunan: %s"
              % (", ".join(ciktili) or "hicbiri"))
        print("  ('cikti nereden geliyor' sorusunun iki cevabi olamaz — H5)")
        return 1

    # --- 3) AD KAPISI ---
    for ad, imza, bolge, kuyruk in PARCALAR:
        govde = "\n".join(tasi(L, bolge))
        try:
            serbest = serbest_adlar("if True:\n" + "\n".join("    " + s for s in govde.split("\n")))
        except SyntaxError as e:
            print("KIRMIZI: %s bolgesi tek basina ayristirilamiyor: %s" % (ad, e))
            return 1
        eksik = serbest - imza_adlari(imza) - globaller
        if eksik:
            print("KIRMIZI: %s bolgesi su adlari OKUYOR ama imzada/globalde YOK: %s"
                  % (ad, ", ".join(sorted(eksik))))
            print("  Bu, ancak KOSTURULUNCA NameError verirdi. Uretim aninda yakalandi.")
            return 1
    print("  ad kapisi: yedi parcanin serbest adlari imza+global icinde")

    # --- 4) yeni metin ---
    baslik = ["", "# ------------------------------------------- cmd_kur BOLMESI (FAZ C)",
              "# `cmd_kur` (91 satir, CC 27) YEDI parcaya bolundu; ince `cmd_kur` en sona konur.",
              "# Etki eksenleri ASAGIDA ELLE YAZILMADI — uretec her kosumda AST ile OLCUP",
              "# buraya yazar. Beyan uretilir, dolayisiyla bayatlayamaz.",
              "#"]
    for ad, _, _, _ in PARCALAR:
        baslik.append("#   %-18s %s" % (ad, ",".join(sorted(etkiler[ad])) or "(SAF)"))
    baslik += [
        "#",
        "#   DISK  diske yaziyor   CIKTI  stdout'a basiyor   OLUM  `oldur` (~ = bir",
        "#   seviye derin: govdesinde `oldur` gecen bir fonksiyonu cagiriyor)",
        "#",
        "# TEK RAPORCU: CIKTI ekseni yalniz `_kur_rapor`da. INCE EBEVEYN: bolmeden",
        "# sonra `cmd_kur` govdesinde dogrudan DISK/CIKTI/OLUM cagrisi YOKTUR.",
        "# Esdegerlik ETKI IMZASI ile olculur (faz0/cmd_kur_bolme_mutanti.py):",
        "# dokuz hal icin (exit, stdout, disk agaci) uclusu bolme oncesi=sonrasi.",
    ]

    yeni = L[: KUR_DEF - 1] + baslik + ["", ""]
    for ad, imza, bolge, kuyruk in PARCALAR:
        yeni.append(imza)
        yeni += tasi(L, bolge)
        if kuyruk:
            yeni.append(kuyruk)
        yeni += ["", ""]
    yeni += EBEVEYN
    yeni += L[KUR_SONRASI - 1:]
    metin = nl.join(yeni)

    # --- 5) derleme + INCE EBEVEYN KAPISI ---
    try:
        compile(metin, "<cmd_kur-bolme>", "exec")
    except SyntaxError as e:
        print("KIRMIZI: uretilen metin derlenmiyor: %s" % e)
        return 1

    agac = ast.parse(metin)
    ebeveyn = next((d for d in agac.body
                    if isinstance(d, ast.FunctionDef) and d.name == "cmd_kur"), None)
    if ebeveyn is None:
        print("KIRMIZI: uretilen metinde cmd_kur yok.")
        return 1
    kirli = set()
    for x in ast.walk(ebeveyn):
        if isinstance(x, ast.Call):
            ad = _cagri_adi(x)
            if ad in DISK_ADLARI:
                kirli.add("DISK:" + ad)
            if ad in CIKTI_ADLARI:
                kirli.add("CIKTI:" + ad)
            if ad == "oldur":
                kirli.add("OLUM:oldur")
    if kirli:
        print("KIRMIZI: ebeveyn hala dogrudan is yapiyor: %s" % ", ".join(sorted(kirli)))
        return 1
    print("  ince ebeveyn: cmd_kur govdesinde dogrudan DISK/CIKTI/OLUM cagrisi YOK")

    with open(HEDEF, "w", encoding="utf-8", newline="") as f:
        f.write(metin)
    print("YAZILDI: %s" % HEDEF)
    print("  satir  : %d -> %d" % (len(L), len(yeni)))
    print("  ESDEGERLIK BU URETECIN ISI DEGIL — faz0/cmd_kur_bolme_mutanti.py kos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

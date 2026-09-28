#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ISIR ESLESME MUTANTI (besli-paket/IS_EMRI_H1_ISIR_SIKB.md, 28 Eyl 2026, SIK B).

NEDEN VAR (olculdu: Cowork 28 Eyl, motor 559E830A; faz0/sabotaj.py)
  `isir`in eslesme kurali etiketi ONEKIYLE de kabul ediyordu: `[H1]` arayan bir
  mutant `[H1-KOVA]` satirini gorunce "isirdi" sayiliyordu. "satir KAYIP" fail()'i
  sokulunce ayni kaybi H1-KOVA da gordugu icin M-H1 yine ISIRDI diyordu (ORTUSEN
  TESPIT MASKELER) ve H1'in alti fail()'inin ALTISI da `isir` icin KAPSAMSIZDI.
  Duzeltme (Onur kilidi 28 Eyl: Soru 1 = A+B, Soru 2 = opsiyonel `siki`):
    A  `mutant()`/`mutant_git()` eslesmesi TAM etiket (onek dali kalkti)
    B  H1'in YEDI mutanti kendi EKSEN cumlesinden bir parca da ister (parca
       sozlugu `cmd_isir` icinde TEK yerde: `_h1_parca`)
    C  `_kapi_metni(kok, siki=False)`; yalniz eksen-6 mutanti (M-H1s) `siki=True`
  Bu betik uc duzeltmenin HER BIRINI ayri kolla olcer (her duzeltmeye AYRI mutant).

NE OLCER
  KOL O  STATIK OZ SINAMA (motor KOSULMAZ, ast.literal_eval ile okunur):
         (i)  `_h1_parca`nin her parcasi motordaki fail() cagrilarinin KAYNAK
              metinlerinden TAM BIRINE uyar (0 ya da 2+ = KIRMIZI) ve o cagri
              mutantin HEDEF ekseninin H1 fail()'idir. Eksen <-> fail() baglantisi
              faz0/h1_kapsam_mutanti.py'nin OLCULMUS eslemesinden alinir
              (`_h1_hedefleri`), burada yeniden yazilmaz.
         (ii) `sinamalar`da etiketi H1 olan her mutantin parcasi VAR, her parca
              anahtari bir `sinamalar` adidir; parcalar H1'in ALTI fail()'ini de
              orter; `siki` secenegi YALNIZ M-H1s'e verilmistir.
  KOL 0  NEGATIF KONTROL: temiz motor, kur+not+derle sablonu -> `isir` exit 0 ve
         H1'in yedi mutanti ISIRDI. Bu tutmazsa asagidaki kollar HICBIR SEY olcmez.
  KOL a  POZITIF KONTROL (maskeleme URETILIR): motor kopyasinda "satir KAYIP"
         fail()'i sabote edilir (sabotaj.py'nin KENDI fail_cagrilari/sabote_et'i;
         cagri METNINDEN bulunur, satir numarasindan DEGIL) VE eski kural geri
         konur (A ve B birlikte geri alinir) -> `isir` M-H1'i ISIRDI der.
  KOL a1 AYNI sabotaj, YALNIZ onek dali geri (B yerinde) -> M-H1/M-H1b KACTI.
  KOL a2 AYNI sabotaj, YALNIZ parca sarti kalkar (A yerinde) -> M-H1/M-H1b KACTI.
         (a1/a2: iki savunma BIRBIRINDEN BAGIMSIZ yeter; is emrinin lafzi "a"
         kolu — yalniz onek dali geri — a1'dir ve A+B kilidinde maskelemeyi
         URETEMEZ, cunku B ayakta. Maskelemeyi ureten kol ikisini birden geri alir.)
  KOL b  AYNI sabotaj, YENI kural -> M-H1 VE M-H1b KACTI.
  KOL c  `siki` GERCEKTEN kullaniliyor mu: M-H1s'in secenek tablosundan
         `siki=True` kaldirilir (sabotaj YOK) -> M-H1s KACTI ya da KURULAMADI
         (hangisi oldugu OLCULUP basilir). ISIRDI kalirsa parametre OLUdur.

NE OLCMEZ
  1. `mutant_git`teki onek dalinin kalkmasi: motorda tireli tek etiket H1-KOVA'dir
     ve `mutant_git` yalniz H12/H14 git kollarini sinar -> gozlenebilir fark YOK.
  2. Yeni eksen mutantlarinin (M-H1d/g/y/o/s) KOSEGENI: onu faz0/sabotaj.py
     (bayraksiz, `isir ile` sutunu) olcer; bu betik yalniz eslesme KURALINI olcer.
  3. H1-KOVA fail()'lerinin kapsami (bu turun disi).

CIKIS KODLARI
  0  KOL O temiz, KOL 0 temiz, a/a1/a2/b/c beklendigi gibi
  1  bir kol BEKLENMEDIK (oz sinama kirmizi, maskeleme uretilemedi, bir savunma
     tek basina yetmedi, M-H1s `siki`siz de ISIRDI ...)
  2  OLCULEMEDI (motor okunamadi, capa bulunamadi, sablon kurulamadi, `isir`
     cokti/zaman asimi) — sessiz PASS YOK

KULLANIM
  python faz0/isir_eslesme_mutanti.py [motor]
"""
import ast
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

# Mutant kimligi -> hedef H1 ekseni (numaralar faz0/h1_kapsam_mutanti.py'nin
# EKSEN_KAYNAK numaralaridir: 1 sahte duzeltme · 2 gerekcesiz · 3 YENI zaten var ·
# 4 okunamayan arsiv · 5 satir KAYIP · 6 beyansiz ekleme).
HEDEF_EKSEN = {"M-H1": 5, "M-H1b": 5, "M-H1d": 1, "M-H1g": 2,
               "M-H1y": 3, "M-H1o": 4, "M-H1s": 6}
SIKI_KIMLIK = "M-H1s"
SABOTAJ_KIMLIK = "M-H1"          # sabote edilen fail(): bu mutantin parcasiyla bulunur

# Metin capalari (motor kaynagi). Her biri kendi KAPSAMINDA TAM 1 kez gecmeli.
A_ESKI = 'yakalandi = (k != 0) and (("[%s]" % kapi) in c)'
A_YENI = 'yakalandi = (k != 0) and (("[%s]" % kapi) in c or ("[%s-" % kapi) in c)'
B_ESKI = 'parca_ok = (icerik_parcasi is None) or (icerik_parcasi in c)'
B_YENI = 'parca_ok = True'
C_ESKI = 'dict(siki=True)'
C_YENI = 'dict()'

_SATIR = re.compile(r"^\s*(M-\S+)\s.*?->\s*(ISIRDI|KACTI|KURULAMADI|UYGULANMAZ)", re.M)


class Olculemedi(Exception):
    """Kurulum/capa/kosum basarisiz — KOL HUKMU DEGILDIR."""


def kos(motor, *argv, kok=None, sure=240):
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                       timeout=sure)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# =============================================================== AST OKUMA
def _cmd_isir(agac):
    for d in agac.body:
        if isinstance(d, ast.FunctionDef) and d.name == "cmd_isir":
            return d
    raise Olculemedi("motorda `cmd_isir` bulunamadi")


def _atama(fn, ad):
    """cmd_isir GOVDESINDEKI (ic fonksiyonlara inmeden) `ad = ...` atamasinin degeri."""
    bulunan = [d.value for d in fn.body if isinstance(d, ast.Assign)
               and len(d.targets) == 1 and isinstance(d.targets[0], ast.Name)
               and d.targets[0].id == ad]
    if len(bulunan) != 1:
        raise Olculemedi("cmd_isir icinde `%s` atamasi %d kez (1 olmali)" % (ad, len(bulunan)))
    return bulunan[0]


def _ic_fonksiyon(fn, ad):
    bulunan = [d for d in fn.body if isinstance(d, ast.FunctionDef) and d.name == ad]
    if len(bulunan) != 1:
        raise Olculemedi("cmd_isir icinde `def %s` %d kez (1 olmali)" % (ad, len(bulunan)))
    return bulunan[0]


def motor_tablolari(kaynak):
    """Doner: parca {ad: parca}, sinamalar [(ad, kapi)], siki_adlar [ad]."""
    try:
        agac = ast.parse(kaynak)
    except SyntaxError as e:
        raise Olculemedi("motor ayristirilamadi: %s" % e)
    fn = _cmd_isir(agac)
    try:
        parca = ast.literal_eval(_atama(fn, "_h1_parca"))
    except ValueError as e:
        raise Olculemedi("`_h1_parca` bir sozluk LITERALI degil: %s" % e)
    if not isinstance(parca, dict) or not parca:
        raise Olculemedi("`_h1_parca` bos ya da sozluk degil")
    sin = _atama(fn, "sinamalar")
    if not isinstance(sin, ast.List):
        raise Olculemedi("`sinamalar` bir liste literali degil")
    sinamalar = []
    for e in sin.elts:
        if not (isinstance(e, ast.Tuple) and len(e.elts) >= 2
                and all(isinstance(x, ast.Constant) and isinstance(x.value, str)
                        for x in e.elts[:2])):
            raise Olculemedi("`sinamalar` ogesi (ad, kapi, fn) bicimi disinda (satir %d)"
                             % e.lineno)
        sinamalar.append((e.elts[0].value, e.elts[1].value))
    sec = _atama(fn, "_h1_secenek")
    if not isinstance(sec, ast.Dict):
        raise Olculemedi("`_h1_secenek` bir sozluk literali degil")
    siki_adlar = []
    for k, v in zip(sec.keys, sec.values):
        if not (isinstance(k, ast.Constant) and isinstance(v, ast.Call)):
            raise Olculemedi("`_h1_secenek` ogesi {ad: dict(...)} bicimi disinda")
        for kw in v.keywords:
            if kw.arg == "siki" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                siki_adlar.append(k.value)
    return parca, sinamalar, siki_adlar


def kimlik(ad):
    return ad.split()[0]


# ================================================================== KOL O
def kol_o(kaynak):
    """Doner: (bulgular, sabote edilecek fail() hedefi, parca sozlugu)."""
    import sabotaj                         # faz0/ sys.path[0]'dadir
    import h1_kapsam_mutanti
    parca, sinamalar, siki_adlar = motor_tablolari(kaynak)
    adlar = [a for a, _ in sinamalar]
    L = kaynak.split("\n")
    cagrilar = sabotaj.fail_cagrilari(kaynak)
    try:
        hedefler, _ = h1_kapsam_mutanti._h1_hedefleri(kaynak)
    except h1_kapsam_mutanti.Olculemedi as e:
        raise Olculemedi("H1 eksen eslemesi kurulamadi: %s" % e)
    b = []
    print("  motordaki fail() sayisi: %d · H1 fail(): %d · parca: %d"
          % (len(cagrilar), sum(1 for h in cagrilar if h["kapi"] == "H1"), len(parca)))
    h1_mutantlari = [a for a, k in sinamalar if k == "H1"]
    for a in h1_mutantlari:
        if a not in parca:
            b.append("etiketi H1 olan `%s` mutantinin PARCASI YOK" % a)
    for a in parca:
        if a not in adlar:
            b.append("parca anahtari `%s` hicbir `sinamalar` adi DEGIL (sessizce "
                     "uygulanmaz)" % a)
    ortulen = set()
    sabotaj_hedefi = None
    for a, p in sorted(parca.items(), key=lambda x: kimlik(x[0])):
        uyan = [h for h in cagrilar
                if p in "\n".join(L[h["lineno"] - 1:h["end_lineno"]])]
        eksen = HEDEF_EKSEN.get(kimlik(a))
        if eksen is None:
            b.append("`%s`: hedef ekseni bu betikte TANIMSIZ" % a)
            continue
        hedef = hedefler[eksen]
        tanim = ", ".join("#%02d sat %d [%s]" % (h["no"], h["lineno"], h["kapi"]) for h in uyan[:4])
        if len(uyan) > 4:
            tanim += " ... +%d" % (len(uyan) - 4)
        if len(uyan) != 1:
            b.append("`%s` parcasi %d fail()'e uyuyor (TAM 1 olmali): %r -> %s"
                     % (kimlik(a), len(uyan), p, tanim or "-"))
            continue
        h = uyan[0]
        if h["kapi"] != "H1" or h["lineno"] != hedef["lineno"]:
            b.append("`%s` parcasi YANLIS fail()'e uyuyor: %s (hedef eksen %d = #%02d sat %d)"
                     % (kimlik(a), tanim, eksen, hedef["no"], hedef["lineno"]))
            continue
        ortulen.add(h["lineno"])
        if kimlik(a) == SABOTAJ_KIMLIK:
            sabotaj_hedefi = h
        print("  %-6s eksen %d -> #%02d sat %-5d TAM 1 fail() : %r"
              % (kimlik(a), eksen, h["no"], h["lineno"], p))
    h1_hepsi = set(h["lineno"] for h in hedefler.values())
    if ortulen != h1_hepsi:
        b.append("parcalar H1'in alti fail()'ini ORTMUYOR: eksik satirlar %s"
                 % sorted(h1_hepsi - ortulen))
    if [kimlik(a) for a in siki_adlar] != [SIKI_KIMLIK]:
        b.append("`siki=True` alan mutantlar %s (YALNIZ %s olmali)"
                 % ([kimlik(a) for a in siki_adlar], SIKI_KIMLIK))
    if sabotaj_hedefi is None and not b:
        b.append("%s parcasinin fail()'i bulunamadi" % SABOTAJ_KIMLIK)
    return b, sabotaj_hedefi, parca


# ============================================================ MOTOR KOPYASI
def _kapsamda_degistir(kaynak, fonksiyon, eski, yeni):
    """`cmd_isir` (fonksiyon=None) ya da onun ic fonksiyonu `fonksiyon`un SATIR
    araliginda `eski`yi `yeni` ile degistirir; aralikta TAM 1 kez gecmeli."""
    agac = ast.parse(kaynak)
    fn = _cmd_isir(agac)
    if fonksiyon is not None:
        fn = _ic_fonksiyon(fn, fonksiyon)
    L = kaynak.split("\n")
    bas, son = fn.lineno - 1, fn.end_lineno
    parca = "\n".join(L[bas:son])
    n = parca.count(eski)
    if n != 1:
        raise Olculemedi("capa `%s` kapsaminda %d kez gecti (1 olmali): %r"
                         % (fonksiyon or "cmd_isir", n, eski))
    L[bas:son] = parca.replace(eski, yeni, 1).split("\n")
    return "\n".join(L)


def motor_turet(kaynak, sabotaj_hedefi, degisimler):
    import sabotaj
    s = kaynak
    if sabotaj_hedefi is not None:
        s = sabotaj.sabote_et(s, sabotaj_hedefi)
    for fonksiyon, eski, yeni in degisimler:
        s = _kapsamda_degistir(s, fonksiyon, eski, yeni)
    try:
        compile(s, "<isir_eslesme>", "exec")
    except SyntaxError as e:
        raise Olculemedi("turetilen motor derlenmiyor: %s" % e)
    return s


# ================================================================ KOSUM
def sablon_kur(motor, taban):
    kok = os.path.join(taban, "sablon")
    os.makedirs(kok)
    for argv in (("kur", "--ad", "IsirEslesme"),
                 ("not", "--konu=genel-durum", "--metin=isir eslesme sablonu ilk not"),
                 ("derle",)):
        k, c = kos(motor, *argv, kok=kok)
        if k != 0:
            raise Olculemedi("sablon: %s exit %d: %s" % (argv[0], k, c[-300:]))
    k, c = kos(motor, "kapi", kok=kok)
    if k != 0:
        raise Olculemedi("sablon: temiz motorda kapi exit %d (isir kosamaz)" % k)
    return kok


def isir_kos(motor_metni, sablon, taban, ad):
    """Turetilmis motoru yazar, sablonun KOPYASINDA `isir` kosar.
    Doner: (exit, {kimlik: hukum}, ham cikti)."""
    d = os.path.join(taban, ad)
    os.makedirs(d)
    mp = os.path.join(d, "hafiza.py")
    with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
        f.write(motor_metni)
    kok = os.path.join(d, "p")
    shutil.copytree(sablon, kok)
    try:
        k, c = kos(mp, "isir", kok=kok, sure=1200)
    except subprocess.TimeoutExpired:
        raise Olculemedi("%s: isir zaman asimi (1200 sn)" % ad)
    if "Traceback" in c:
        raise Olculemedi("%s: isir COKTU (Traceback): %s" % (ad, c[-300:]))
    hukum = {}
    for m in _SATIR.finditer(c):
        hukum.setdefault(m.group(1), m.group(2))
    if not hukum:
        raise Olculemedi("%s: isir ciktisinda mutant satiri yok (exit %d): %s"
                         % (ad, k, c[-300:]))
    return k, hukum, c


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN_MOTOR)
    print(CIZGI)
    print("ISIR ESLESME MUTANTI (SIK B: A tam etiket · B eksen parcasi · C siki)")
    print("motor: %s · platform: %s" % (motor, sys.platform))
    print(CIZGI)
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    # ---- KOL O -------------------------------------------------------------
    print("\n--- KOL O: statik oz sinama (parca -> TAM 1 fail(), hedef eksen) ---")
    try:
        bulgu_o, sab_hedef, parca = kol_o(kaynak)
    except (Olculemedi, ImportError) as e:
        print("SONUC: OLCULEMEDI — KOL O: %s" % e)
        return 2
    for x in bulgu_o:
        print("  ! %s" % x)
    if bulgu_o:
        print("\nSONUC: KIRMIZI — KOL O: %d bulgu (parca tablosu kendi sozlesmesini "
              "tutmuyor; dinamik kollar KOSULMADI)." % len(bulgu_o))
        return 1
    print("  KOL O -> TEMIZ (sabote edilecek fail(): #%02d sat %d, METINDEN bulundu)"
          % (sab_hedef["no"], sab_hedef["lineno"]))

    # ---- motor turevleri ---------------------------------------------------
    A = ("mutant", A_ESKI, A_YENI)
    B = ("mutant", B_ESKI, B_YENI)
    C = (None, C_ESKI, C_YENI)
    try:
        turevler = [
            ("KOL 0 ", "temiz motor (negatif kontrol)", motor_turet(kaynak, None, [])),
            ("KOL a ", "satir KAYIP sabote + ESKI kural (A ve B geri)",
             motor_turet(kaynak, sab_hedef, [A, B])),
            ("KOL a1", "satir KAYIP sabote + YALNIZ onek dali geri",
             motor_turet(kaynak, sab_hedef, [A])),
            ("KOL a2", "satir KAYIP sabote + YALNIZ parca sarti kalkti",
             motor_turet(kaynak, sab_hedef, [B])),
            ("KOL b ", "satir KAYIP sabote + YENI kural",
             motor_turet(kaynak, sab_hedef, [])),
            ("KOL c ", "M-H1s'ten siki=True kaldirildi (sabotaj YOK)",
             motor_turet(kaynak, None, [C])),
        ]
    except Olculemedi as e:
        print("SONUC: OLCULEMEDI — motor turetilemedi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="isir_eslesme_")
    try:
        try:
            sablon = sablon_kur(motor, taban)
        except (Olculemedi, subprocess.TimeoutExpired) as e:
            print("SONUC: OLCULEMEDI — %s" % e)
            return 2
        print("\n--- DINAMIK KOLLAR (kur+not+derle sablonu, her kol AYRI kopyada `isir`) ---")
        sonuc = {}
        with ThreadPoolExecutor(max_workers=3) as ex:
            isler = {ad.strip(): ex.submit(isir_kos, metin, sablon, taban,
                                           ad.strip().replace(" ", "_"))
                     for ad, _, metin in turevler}
            for ad, is_ in isler.items():
                try:
                    sonuc[ad] = is_.result()
                except Olculemedi as e:
                    sonuc[ad] = e
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    kirmizi, olculemeyen = 0, 0
    beklenen = {
        "KOL 0": ("H1'in yedi mutanti ISIRDI, exit 0",
                  lambda k, h: k == 0 and all(h.get(x) == "ISIRDI" for x in HEDEF_EKSEN)),
        "KOL a": ("M-H1 ISIRDI (maskeleme URETILDI)",
                  lambda k, h: h.get("M-H1") == "ISIRDI"),
        "KOL a1": ("M-H1 ve M-H1b KACTI (B tek basina yeter)",
                   lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL a2": ("M-H1 ve M-H1b KACTI (A tek basina yeter)",
                   lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL b": ("M-H1 ve M-H1b KACTI",
                  lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL c": ("M-H1s KACTI ya da KURULAMADI",
                  lambda k, h: h.get("M-H1s") in ("KACTI", "KURULAMADI")),
    }
    for ad, aciklama, _ in turevler:
        ad = ad.strip()
        r = sonuc[ad]
        if isinstance(r, Olculemedi):
            print("  %-6s %-46s -> OLCULEMEDI: %s" % (ad, aciklama, r))
            olculemeyen += 1
            continue
        k, h, _c = r
        ozet = " ".join("%s=%s" % (x, h.get(x, "-")) for x in sorted(HEDEF_EKSEN))
        tanim, olcut = beklenen[ad]
        tamam = olcut(k, h)
        print("  %-6s %-46s -> %s" % (ad, aciklama, "BEKLENDIGI GIBI" if tamam else "BEKLENMEDIK"))
        print("         isir exit %d · %s" % (k, ozet))
        print("         beklenen: %s" % tanim)
        if ad == "KOL c" and tamam:
            print("         OLCULDU: M-H1s `siki`siz -> %s" % h.get("M-H1s"))
        if not tamam:
            kirmizi += 1
    print()
    if kirmizi:
        print("SONUC: KIRMIZI — %d kol beklenmedik (kural/parca/siki sozlesmesi tutmuyor)."
              % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kol kosulamadi; sessiz PASS verilmez." % olculemeyen)
        return 2
    print("SONUC: YESIL — KOL O temiz; maskeleme eski kuralla URETILDI, A ve B ayri "
          "ayri yetiyor, yeni kuralda M-H1/M-H1b KACTI, `siki` parametresi CANLI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

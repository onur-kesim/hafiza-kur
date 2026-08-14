#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`cmd_kur` BOLME MUTANTI — parcalar arasi kenarlar OLCULUYOR mu?

Kapi bolmelerinin (`h1/h4/h10/h11/h12/h14`) sozlesmesiyle AYNI iskelet, ama
GOZLEM YUZEYI FARKLI ve fark bu betigin butun varlik sebebi:

    kapi bolmeleri : (exit, stdout)
    cmd_* bolmeleri: (exit, stdout, DISK AGACI MANIFESTOSU)   <- faz0/etki_imzasi.py

Gerekce olculdu (`faz0/cmd_etki_mutanti.py`, 14 Agu 2026): `cmd_kur`a yapilan
DORT sessiz-yazim sabotajinin DORDU DE `(exit, stdout)` yuzeyine gorunmez.
Kapi kalibini oldugu gibi kopyalamak KOR bir kapi uretmek olurdu.

UC SORU, AYRI AYRI OLCULUR
==========================
1. ESDEGERLIK — bolme oncesi ve sonrasi motorlar HER HALDE AYNI
   ucluyu uretiyor mu? Tek fark bile bolmenin davranis degistirdigi anlamina
   gelir ve betik durur. (Uretec bu olcumu YAPMAZ: uretici kendi isini
   adjudike edemez.)
2. HAL KAPISI — haller birbirinden AYRISIYOR mu? Iki hal ayni ucluyu
   uretiyorsa ayni dal iki kez olculuyordur ve mutant sonuclari yanlis okunur.
3. MUTANTLAR — ebeveyndeki her kenar/cagri koparildiginda FARK gorunuyor mu?

Her mutant icin ESKI (exit,stdout) ve YENI (+manifest) yuzeyler AYRI raporlanir.
"ESKI KOR · YENI ISIRDI" satirlari, yeni yuzeyin bu bolmede ne kazandirdiginin
OLCUSUDUR — beyani degil.

CIKIS KODU  0 hepsi isirdi · 1 kacan var / esdegerlik bozuk · 2 OLCULEMEDI
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
BOLUCU = os.path.join(KOK, "faz0", "fazC_bolucu_cmd_kur.py")
IMZA_MODUL = os.path.join(KOK, "faz0", "etki_imzasi.py")
CIZGI = "-" * 96

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi — bolmenin hukmu degil."""


def _imza_modulu():
    spec = importlib.util.spec_from_file_location("etki_imzasi", IMZA_MODUL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def stdout_normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    return _RE_TARIH.sub("<TARIH>", m)


def kos(motor, arglar, cwd):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300, cwd=cwd)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ------------------------------------------------------------------- HALLER
# Her hal `cmd_kur`un AYRI bir dalini calistirir; `oldur` yollari tek tek
# ayrilir cunku SURECI HANGI PARCANIN oldurdugu ETKI KAPISI'nin ana eksenidir.
# SAYI BURAYA YAZILMAZ — bir kez 'dokuz hal' yazildi, onuncu eklenince yalan
# oldu. Sayiyi `len(HALLER)` verir; beyan uretilir, elle tutulmaz.

def _git(kok):
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)


def _h_taze(motor, kok):
    _git(kok)


def _h_idempotent(motor, kok):
    _git(kok)
    rc, c = kos(motor, ["kur", "--ad", "KURMUT", "--kok", kok], kok)
    if rc != 0:
        raise Kurulamadi("on kurulum basarisiz: %s" % c.strip().split("\n")[-1][:100])


def _h_kok_yok(motor, kok):
    _git(kok)


def _h_v1_izi(motor, kok):
    _git(kok)
    d = os.path.join(kok, "arsiv", "hafiza")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "_ZINCIR.jsonl"), "w", encoding="utf-8").write("")
    open(os.path.join(d, "_KAYNAK.md"), "w", encoding="utf-8").write("# eski\n")


def _h_yol_ihlali(motor, kok):
    """`gunluk` DIZIN olmasi gereken yerde DOSYA var -> yol_on_kontrol oldurur."""
    _git(kok)
    open(os.path.join(kok, "gunluk"), "w", encoding="utf-8").write("dizin degil\n")


def _h_kilit_mesgul(motor, kok):
    _h_idempotent(motor, kok)
    p = os.path.join(kok, "arsiv", "hafiza", ".kilit")
    # BASKASININ kilidi: var olmayan bir pid ile. (Kendi pid'imiz olsaydi arac
    # kilidi bize ait sayardi — B-5'te olculen sahiplik davranisi.)
    open(p, "w", encoding="utf-8").write(json.dumps({"pid": 999999, "t": "2020-01-01T00:00:00"}))


def _h_bozuk_zincir(motor, kok):
    _h_idempotent(motor, kok)
    p = os.path.join(kok, "arsiv", "hafiza", "_ZINCIR.jsonl")
    open(p, "w", encoding="utf-8").write("")          # 0 bayta indir -> sart oldurmeli


def _h_arsiv_yok(motor, kok):
    """.hafizarc VAR ama arsiv dizini silinmis — 'kurulu ama cipasiz' hali."""
    _h_idempotent(motor, kok)
    shutil.rmtree(os.path.join(kok, "arsiv", "hafiza"))


def _h_rc_bozuk(motor, kok):
    _h_idempotent(motor, kok)
    p = os.path.join(kok, ".hafizarc")
    s = open(p, encoding="utf-8").read()
    s2 = re.sub(r'("tavan_kb"\s*:\s*)\d+', r'\1"cok"', s, count=1)
    if s2 == s:
        raise Kurulamadi("tavan_kb alani bulunamadi")
    open(p, "w", encoding="utf-8", newline="").write(s2)


def _arg_normal(kok):
    return ["kur", "--ad", "KURMUT", "--kok", kok]


def _arg_kok_yok(kok):
    return ["kur", "--ad", "KURMUT", "--kok", os.path.join(kok, "olmayan")]


def _arg_goreli(kok):
    # 🔴 GORELI --kok. Bu hal SONRADAN eklendi ve sebebi OLCUMDUR:
    # `M-8 DONUS kok` mutanti (ON KONTROL'un donusunu koparip `kok`u
    # `a.kok or os.getcwd()` ile yeniden hesaplamak) dokuz halin TAMAMINDA
    # KACIYORDU. Korluk ilan etmeden once "esdeger mutant mi?" diye soruldu:
    # EVET idi — cunku dokuz halin dokuzu da --kok'u MUTLAK yol veriyordu ve
    # `os.path.abspath` bir islem yapmiyordu. Yani kacis kapinin degil,
    # GIRDI KUMESININ eksigiydi. Goreli yol EKLENINCE mutant gercek oluyor.
    # Yan kazanc: goreli --kok bu ana kadar HIC olculmemisti.
    #
    # `--ad GORELI`: ayni ad verilseydi bu hal `h_taze` ile BIREBIR ayni ucluyu
    # uretirdi (abspath goreliyi mutlaka cevirdigi icin) ve HAL KAPISI
    # "haller ayrismiyor" derdi. O ozdeslik zaten `abspath`in calistiginin
    # kanitidir; haller ayrissin diye ad degistirildi.
    return ["kur", "--ad", "GORELI", "--kok", "."]


HALLER = [
    ("h_taze", _h_taze, _arg_normal, "ilk kurulum"),
    ("h_idempotent", _h_idempotent, _arg_normal, "ikinci kur: tazeleme dali"),
    ("h_kok_yok", _h_kok_yok, _arg_kok_yok, "kok yok -> ON KONTROL oldurur"),
    ("h_v1_izi", _h_v1_izi, _arg_normal, "v1 izi -> ON KONTROL oldurur"),
    ("h_yol_ihlali", _h_yol_ihlali, _arg_normal, "gunluk yerinde dosya -> KILIT bolgesi oldurur"),
    ("h_kilit_mesgul", _h_kilit_mesgul, _arg_normal, "baskasinin kilidi -> KILIT oldurur"),
    ("h_bozuk_zincir", _h_bozuk_zincir, _arg_normal, "0 baytlik zincir -> KILIT bolgesi oldurur"),
    ("h_arsiv_yok", _h_arsiv_yok, _arg_normal, "kurulu ama arsiv silinmis"),
    ("h_rc_bozuk", _h_rc_bozuk, _arg_normal, "tavan_kb metin -> RC bolgesi oldurur"),
    ("h_goreli_kok", _h_taze, _arg_goreli, "--kok=. (goreli) -> abspath calisiyor mu"),
]


# ----------------------------------------------------------------- MUTANTLAR
# Hedef dizgeler BOLUNMUS motorun EBEVEYNINDEDIR. Her biri bir KENARI ya da bir
# CAGRIYI koparir. Cogu SESSIZ olacak sekilde secildi: stdout ve exit ayni kalir,
# yalniz disk degisir — kapi kaliminin yuzeyi bunlara kordur.

MUTANTLAR = [
    ("M-1 CAGRI on_kontrol", "v1/kok korumasi hic kosmaz",
     [("    kok = _kur_on_kontrol(a)",
       "    kok = os.path.abspath(a.kok or os.getcwd())")]),
    ("M-2 KENAR yeni_kurulum", "KILIT'e hep True gider — zincir butunlugu sarti SUSAR",
     [("    _kur_kilit(y, rc, yeni_kurulum)", "    _kur_kilit(y, rc, True)")]),
    ("M-3 KENAR rc -> dizinler", "arsiv turleri bosalir — dizinler SESSIZCE acilmaz",
     [("    _kur_dizinler(kok, rc, y)",
       '    _kur_dizinler(kok, dict(rc, arsiv_turleri=[]), y)')]),
    ("M-4 KENAR ad -> dosyalar", "sabit ad — canli hafiza ve kural dosyasi SESSIZCE degisir",
     [('    _kur_dosyalar(ad, rc, y)', '    _kur_dosyalar("PROJE", rc, y)')]),
    ("M-5 CAGRI kilit", "kilit alinmaz, yol on kontrolu kosmaz",
     [("    _kur_kilit(y, rc, yeni_kurulum)", "    pass")]),
    ("M-6 CAGRI halka", "zincire halka YAZILMAZ — stdout ayni, denetim izi yok",
     [("    _kur_halka(y)", "    pass")]),
    ("M-7 KENAR kok -> rapor", "rapor yanlis kok basar",
     [('    _kur_rapor(kok, rc, y)', '    _kur_rapor(".", rc, y)')]),
    # M-8 yalnizca GORELI --kok halinde isirir: mutlak yolda `abspath` bir islem
    # yapmadigi icin ESDEGER MUTANT olur. Dokuz halle kaciyordu; onuncu hal
    # (h_goreli_kok) onu gercek mutanta cevirdi.
    ("M-8 DONUS kok", "ON KONTROL'un donusu kopar (abspath atlanir)",
     [("    kok = _kur_on_kontrol(a)", "    _kur_on_kontrol(a)\n    kok = a.kok or os.getcwd()")]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def kume_olc(motor, taban, im):
    out = {}
    for ad, hazir, arglar, _ in HALLER:
        kok = os.path.join(taban, ad)
        os.makedirs(kok, exist_ok=True)
        hazir(motor, kok)
        rc, c = kos(motor, arglar(kok), kok)
        try:
            manifest = im.imza(kok)
        except im.Olculemedi as e:
            raise Kurulamadi("imza alinamadi (%s): %s" % (ad, e))
        out[ad] = (rc, stdout_normalize(c, kok), im.ozet(manifest), manifest)
    return out


def eski_fark(a, b):
    return [ad for ad in a if (a[ad][0], a[ad][1]) != (b[ad][0], b[ad][1])]


def yeni_fark(a, b):
    return [ad for ad in a if (a[ad][0], a[ad][1], a[ad][2]) != (b[ad][0], b[ad][1], b[ad][2])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR,
                    help="BOLUNMUS motor (mutantlar buna uygulanir)")
    ap.add_argument("--once", default="",
                    help="BOLME ONCESI motor; verilirse ESDEGERLIK olculur")
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    for p, n in ((motor, "motor"), (IMZA_MODUL, "etki_imzasi.py")):
        if not os.path.isfile(p):
            print("OLCULEMEDI: %s yok: %s" % (n, p))
            return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok.")
        return 2
    im = _imza_modulu()
    kaynak = open(motor, encoding="utf-8").read()

    print(CIZGI)
    print("cmd_kur BOLME MUTANTI — kenarlar ve ETKI IMZASI")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="kurmut_")
    try:
        try:
            ref = kume_olc(motor, os.path.join(taban, "ref"), im)
            ref2 = kume_olc(motor, os.path.join(taban, "ref2"), im)
        except Kurulamadi as e:
            print("OLCULEMEDI: referans kol kurulamadi: %s" % e)
            return 2

        tk = yeni_fark(ref, ref2)
        print("  TEMIZ KOL (ayni motor 2 kez)   %s"
              % ("FARK YOK" if not tk else "FARK VAR: %s" % tk))
        if tk:
            for ad in tk:
                for yol, ne in im.fark(ref[ad][3], ref2[ad][3])[:4]:
                    print("     %-14s %-42s %s" % (ad, yol, ne))
            print("\nOLCULEMEDI: duzenek determinist degil.")
            return 2

        # --- 1) ESDEGERLIK ---
        if a.once:
            once = os.path.abspath(a.once)
            if not os.path.isfile(once):
                print("OLCULEMEDI: --once motoru yok: %s" % once)
                return 2
            # 🔴 DOSYA ADI KAPISI — olculdu 14 Agu 2026, SAHTE KIRMIZI uretti.
            # `cmd_kur`un son satiri `os.path.basename(__file__)` basar. Iki motor
            # farkli adlarla dururken (hafiza_ONCE.py / hafiza_SONRA.py) stdout
            # ZORUNLU olarak ayrisir ve esdegerlik kapisi "bolme davranis
            # degistirdi" der — oysa degisen ORTAMDIR, arac degil.
            # Bu, projenin "prob ORTAMI mi ARACI mi olcuyor" dersinin aynisi.
            # Cozum NORMALIZASYON DEGIL (o, adin gercekten degismesini de gizlerdi);
            # cozum LIKE-ILE-LIKE karsilastirmayi ZORUNLU kilmaktir:
            if os.path.basename(once) != os.path.basename(motor):
                print("OLCULEMEDI: iki motorun DOSYA ADI farkli (%s vs %s)."
                      % (os.path.basename(once), os.path.basename(motor)))
                print("  `cmd_kur` son satirinda kendi dosya adini BASAR; farkli adlar")
                print("  stdout'u zorunlu ayristirir ve SAHTE bir esdegerlik kirmizisi uretir.")
                print("  Ikisini de ayri dizinlere `hafiza.py` adiyla koyup tekrar kos.")
                return 2
            try:
                ref_once = kume_olc(once, os.path.join(taban, "once"), im)
            except Kurulamadi as e:
                print("OLCULEMEDI: bolme oncesi kol kurulamadi: %s" % e)
                return 2
            fk = yeni_fark(ref_once, ref)
            print("  ESDEGERLIK (bolme oncesi = sonrasi)   %s"
                  % ("FARK YOK — %d halin ucusu de AYNI" % len(HALLER) if not fk
                     else "🔴 FARK VAR: %s" % fk))
            if fk:
                for ad in fk:
                    e0, e1 = ref_once[ad], ref[ad]
                    if (e0[0], e0[1]) != (e1[0], e1[1]):
                        print("     %-14s exit %s->%s / stdout degisti" % (ad, e0[0], e1[0]))
                    for yol, ne in im.fark(e0[3], e1[3])[:4]:
                        print("     %-14s %-42s %s" % (ad, yol, ne))
                print("\nKIRMIZI: bolme DAVRANIS DEGISTIRDI. Mutant sonuclari okunmaz.")
                return 1
        else:
            print("  ESDEGERLIK                     OLCULMEDI (--once verilmedi)")

        # --- 2) HAL KAPISI ---
        imzalar = {(ref[ad][0], ref[ad][1], ref[ad][2]) for ad, _, _, _ in HALLER}
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), len(imzalar)))
        for ad, _, _, aciklama in HALLER:
            print("     %-16s exit %s · %-3d girdi · %s"
                  % (ad, ref[ad][0], len(ref[ad][3]), aciklama))
        if len(imzalar) < len(HALLER):
            print("\nOLCULEMEDI: haller ayrismiyor — ayni dal iki kez olculuyor.")
            return 2

        # --- 3) MUTANTLAR ---
        print(CIZGI)
        print("  %-24s %-11s %-11s %s" % ("mutant", "ESKI YUZEY", "YENI YUZEY", "iz"))
        print(CIZGI)
        kacan, kazanan = [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, "m_" + re.sub(r"\W+", "_", ad))
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yen = kume_olc(sab, os.path.join(d, "hal"), im)
            except Kurulamadi as e:
                print("  ?  %-24s OLCULEMEDI  %s" % (ad, e))
                return 2
            e_f, y_f = eski_fark(ref, yen), yeni_fark(ref, yen)
            if not y_f:
                kacan.append(ad)
            elif not e_f:
                kazanan.append(ad)
            print("  %s  %-24s %-11s %-11s %s"
                  % ("+" if y_f else "!", ad,
                     "ISIRDI" if e_f else "KOR", "ISIRDI" if y_f else "KOR",
                     (",".join(h.replace("h_", "") for h in y_f)[:34] or "-")))
            print("        %s" % aciklama)

        print(CIZGI)
        if kacan:
            print("KIRMIZI: %d mutant KACTI: %s" % (len(kacan), ", ".join(kacan)))
            print("  Kenar var, olcusu YOK. Esdeger mutant mi diye SOR; degilse korluk.")
            return 1
        print("HUKUM: %d mutantin hepsi ISIRDI (%d hal)." % (len(MUTANTLAR), len(HALLER)))
        print("  Bunlarin %d tanesinde ESKI yuzey KORDU — etki imzasi olmadan"
              % len(kazanan))
        print("  gorunmezlerdi: %s" % (", ".join(kazanan) or "hicbiri"))
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

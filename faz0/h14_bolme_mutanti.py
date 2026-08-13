#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H14 ALT-BOLME MUTANTI — `_kapi_h14`'un dort parcasi arasindaki kenarlar OLCULUYOR mu?

NEDEN AYRI BIR MUTANT
---------------------
`h1_bolme_mutanti.py` ile ayni gerekce: altin kume (`faz0/altin_kapi.json`)
"bugunku kod ayni davraniyor" der; "bir kenar yarin sessizce koparsa HERHANGI bir
olcum kirmizi olur mu" DEMEZ. H1 turunda bu fark OLCULDU: yedi kenar mutantindan
UCUNU altin kume hic gormedi.

H14 icin bosluk daha da genistir. H14'un konusu PROJE ZAMANI ile HAFIZA ZAMANI
arasindaki farktir; altin kumenin halleri taze kurulmus, hafizasi bugun yazilmis
projelerdir — yani H14 orada neredeyse hep ayni tek cumleyi ("hafiza projeyle
es") uretir. Bir siniflandirma kenari koparsa o cumle degismeyebilir.

Bu dosya kendi hallerini kurar: hafiza tarihi ile dosya tarihleri KASITLI olarak
ayrilir, ve git'in dort sinifi (izlenen-temiz · izlenen-kirli · izlenmeyen ·
.gitignore'lu) ayri ayri uyandirilir. Cunku H14'un git mantiginin VAR OLUS NEDENI
tam olarak bu dort sinifi ayirt etmektir (Fable Bulgu 9 ve §3.1).

IKI SUTUN HALINDE OLCER — ASIL SORU BUDUR
    KENDI KUMESI : bu betigin hallerinde fark var mi?
    ALTIN KUME   : `altin_cikti.py --karsilastir` ayni kusuru goruyor mu?

    Ikisi de ISIRIRSA  -> kenar zaten kapsamda; bu mutant KANIT olarak kalir.
    Yalniz kendi kumesi -> altin kume O SINIFA KOR; bu mutant GERCEK kapsam ekler.
    Ikisi de kacarsa   -> kenar HIC olculmuyor; bolme o noktada kanitsizdir.

    FARK VAR   -> ISIRDI      kenar olculuyor
    FARK YOK   -> KACTI       kenar icin KOR
    kurulamadi -> OLCULEMEDI  ARAC KUSURU (Y-4 dersi: sahte kirmizi uretme)

AYRICA — HAL KAPISI (bu betige ozgu)
    Temiz kolda her halin ciktisinda bir H14 satiri BULUNMALIDIR. Bulunmuyorsa
    hal H14'u hic ateslememis demektir; oyle bir kumede butun mutantlar "temiz"
    gorunur. Bu durumda betik OLCULEMEDI der ve 2 doner — sahte yesil uretmez.

KULLANIM
    python3 faz0/h14_bolme_mutanti.py
    python3 faz0/h14_bolme_mutanti.py --altin-atla     (hizli; ikinci sutun kosulmaz)

CIKIS KODU
    0  her mutant KENDI KUMESINDE ISIRDI
    1  en az bir mutant KACTI
    2  OLCULEMEDI / duzenek kurulamadi
"""
import argparse
import datetime as _dt
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI (olcum aracina da konur)
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
ALTIN_ARAC = os.path.join(KOK, "faz0", "altin_cikti.py")
ALTIN_KUME = os.path.join(KOK, "faz0", "altin_kapi.json")
CIZGI = "-" * 84

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")
_RE_GUN = re.compile(r"\b\d+ gun once\b")   # yalniz H12'nin notu; "40 gun geride" MASKELENMEZ

# Hafiza tarihi ile dosya tarihi arasina konan mesafe. `hafiza_gecikme_gun`
# varsayilani 2'dir; 40 gun her iki yonde de esigi RAHATCA asar, yani hukum
# esik yuvarlamasina degil kenarin kendisine baglidir.
GUN = 40


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun once", m)


# --------------------------------------------------------------- PROJE HALLERI
# Her hal H14'un FARKLI bir dalini ya da git sinifini uyandirir.
#   h_es      hafiza ile proje AYNI tarihte      -> "es" notu
#   h_geride  proje ilerledi, hafiza ilerlemedi  -> FAIL (kapinin var olus nedeni)
#   h_ileri   hafiza dosyalardan ILERIDE         -> FAIL (ters yon; ayri dal)
#   h_kirli   IZLENEN ama DEGISMIS dosya         -> mtime GERCEK calisma zamanidir
#   h_temiz   IZLENEN ve degismemis, mtime taze  -> ICERIK (commit) tarihi kullanilir
#   h_ignore  .gitignore'lu taze dosya           -> izlenmeyen; mtime ile olculur
#   h_kapali  hafiza_gecikme_gun = 0             -> kapi KAPALI (koruma dali)
HALLER = [
    ("h_es", "es"),
    ("h_geride", "geride"),
    ("h_ileri", "ileri"),
    ("h_kirli", "kirli"),
    ("h_temiz", "temiz"),
    ("h_ignore", "ignore"),
    ("h_kapali", "kapali"),
]

OLCUM_KOMUTLARI = [["kapi"]]

HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h14 mutanti icin ilk kayit"],
            ["derle"]]


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:120]))
    return r.stdout


def _eski_gun():
    return _dt.date.today() - _dt.timedelta(days=GUN)


def _eski_ts():
    # Gun ortasi: yerel saat/DST kaymasinin gun sinirini atlatmasini onler.
    g = _eski_gun()
    return _dt.datetime(g.year, g.month, g.day, 12, 0, 0).timestamp()


def _tarih_yaz(kok, gun):
    """'Son guncelleme' tarihini CANLI ve SNAPSHOT dosyalarinda ayni anda degistirir.

    Yalniz canliyi degistirmek H1'i (KAYIP satir) ates ediyordu; o gurultu
    hallerin ayirt ediciligini dusurmez ama okunmasini zorlastirir. Ikisini
    birden yazmak H14'un olctugu seyi degistirmez."""
    hedefler = [os.path.join(kok, "PROJE_HAFIZA.md"),
                os.path.join(kok, "arsiv", "hafiza", "_KAYNAK.md")]
    yazildi = 0
    for p in hedefler:
        if not os.path.isfile(p):
            continue
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r"(Son g[uü]ncelleme:\s*)(\d{4}-\d{2}-\d{2})",
                    r"\g<1>" + gun.isoformat(), s, count=1)
        if s2 != s:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(s2)
            yazildi += 1
    if not yazildi:
        raise Kurulamadi("'Son guncelleme' satiri bulunamadi — hal kurulamaz")


def _rc_yaz(kok, **anahtarlar):
    """`.hafizarc`'a anahtar yazar (yoksa EKLER).

    🔴 EKLEME SART: `kur` varsayilan degerdeki anahtarlari dosyaya YAZMAZ —
    olculdu, uretilen rc'de `hafiza_gecikme_gun` HIC yok (varsayilan 2 koddan
    gelir). Yalniz `re.sub` ile degistirmeye calisan bir kurulum bu yuzden
    sessizce hicbir sey yapmaz; bu betigin ilk kosumunda tam olarak bu oldu ve
    hal KURULAMADI hukmu verdi. Bu yuzden JSON olarak okunup yaziliyor."""
    import json
    p = os.path.join(kok, ".hafizarc")
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        raise Kurulamadi(".hafizarc okunamadi: %s" % e)
    d.update(anahtarlar)
    with open(p, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


# H14'un kendi disladigi dizinler; mtime'i onlarda degistirmenin anlami yok.
_HARIC = {".git", "node_modules", "__pycache__", ".venv", "arsiv", "gunluk", "dist", "build"}


def _mtime_ayarla(kok, ts, atla=()):
    for r0, d0, f0 in os.walk(kok):
        d0[:] = [d for d in d0 if d not in _HARIC]
        for f in f0:
            if f in atla:
                continue
            try:
                os.utime(os.path.join(r0, f), (ts, ts))
            except OSError:
                pass


def _commit_et(kok, gun):
    """Butun agaci `gun` tarihiyle commit'ler (izlenen-temiz sinifini var eder)."""
    iso = "%sT12:00:00" % gun.isoformat()
    ortam = dict(os.environ, GIT_AUTHOR_DATE=iso, GIT_COMMITTER_DATE=iso,
                 GIT_AUTHOR_NAME="h14mut", GIT_AUTHOR_EMAIL="h14@example.invalid",
                 GIT_COMMITTER_NAME="h14mut", GIT_COMMITTER_EMAIL="h14@example.invalid",
                 GIT_CONFIG_NOSYSTEM="1")
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban", env=ortam)


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H14MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))
    _rc_yaz(kok, bayatlik_gun=3600)
    eski, simdi = _eski_gun(), _dt.datetime.now().timestamp()
    kodp = os.path.join(kok, "kod.py")
    with open(kodp, "w", encoding="utf-8", newline="") as f:
        f.write("# h14 mutanti icin proje dosyasi\nDEGER = 1\n")

    if tip == "es":                       # hafiza ESKI, dosyalar da ESKI
        _tarih_yaz(kok, eski)
        _mtime_ayarla(kok, _eski_ts())
    elif tip == "geride":                 # hafiza ESKI, dosya TAZE
        _tarih_yaz(kok, eski)
        _mtime_ayarla(kok, _eski_ts(), atla=("kod.py",))
        os.utime(kodp, (simdi, simdi))
    elif tip == "ileri":                  # hafiza BUGUN, dosyalar ESKI
        _mtime_ayarla(kok, _eski_ts())
    elif tip == "kirli":                  # IZLENEN + DEGISMIS -> mtime gecerli
        _tarih_yaz(kok, eski)
        _commit_et(kok, eski)
        _mtime_ayarla(kok, _eski_ts())
        with open(kodp, "a", encoding="utf-8", newline="") as f:
            f.write("DEGER = 2   # commit'ten SONRA degisti\n")
        os.utime(kodp, (simdi, simdi))
    elif tip == "temiz":                  # IZLENEN + degismemis, mtime TAZE
        _tarih_yaz(kok, eski)
        _commit_et(kok, eski)
        _mtime_ayarla(kok, simdi)         # klon artefaktinin taklidi
    elif tip == "ignore":                 # .gitignore'lu TAZE dosya
        _tarih_yaz(kok, eski)
        with open(os.path.join(kok, ".gitignore"), "w", encoding="utf-8", newline="") as f:
            f.write("gizli.py\n")
        with open(os.path.join(kok, "gizli.py"), "w", encoding="utf-8", newline="") as f:
            f.write("# git'in gormedigi ama calisilan dosya\n")
        _commit_et(kok, eski)
        _mtime_ayarla(kok, _eski_ts(), atla=("gizli.py",))
        os.utime(os.path.join(kok, "gizli.py"), (simdi, simdi))
    elif tip == "kapali":                 # kapi bilincli KAPALI
        _tarih_yaz(kok, eski)
        _rc_yaz(kok, hafiza_gecikme_gun=0)
        _mtime_ayarla(kok, _eski_ts(), atla=("kod.py",))
        os.utime(kodp, (simdi, simdi))
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


def haller_kur(motor_temiz, taban):
    """Halleri BIR KEZ ve TEMIZ motorla kurar; {ad: kok} dondurur.

    🔴 NEDEN TEMIZ MOTOR (12 Agu 2026, H1 turunda olculdu): hal kurulumu `derle`
    icerir ve `derle` kapi FAIL verirse derlemeyi REDDEDER. Sabotajli motorla
    kurulan hal, kenar pekala olculebilirken OLCULEMEDI doner. Sabotaj OLCEN
    motordadir, olculen PROJEDE degil."""
    kokler = {}
    for ad, tip in HALLER:
        kokler[ad] = hal_kur(motor_temiz, ad, tip, taban)
    return kokler


def kume_olc(motor, kokler, hedef_taban):
    """Halleri kopyalayip verilen motorla olcer. {(hal, komut): (exit, cikti)}

    Kopya sart: kollar arasinda paylasilan agac bir kolun otekini kirletmesine
    acik olurdu; ayrica `copytree` mtime'lari KORUR (copy2) — H14'un olctugu sey
    tam olarak mtime oldugu icin bu bir ayrinti degil, on kosuldur."""
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        for komut in OLCUM_KOMUTLARI:
            rc, c = kos(motor, komut, kok)
            out[(ad, " ".join(komut))] = (rc, normalize(c, kok))
    return out


def farklari_bul(a, b):
    farklar = []
    for anahtar in sorted(set(a) | set(b)):
        x, y = a.get(anahtar), b.get(anahtar)
        if x is None or y is None:
            farklar.append((anahtar, "olcum EKSIK"))
        elif x[0] != y[0]:
            farklar.append((anahtar, "exit %s -> %s" % (x[0], y[0])))
        elif x[1] != y[1]:
            farklar.append((anahtar, "cikti degisti"))
    return farklar


def _h14_satiri(cikti):
    """Ciktidaki H14 satirini dondurur; FAIL satiri varsa ONCE onu.

    🔴 NEDEN ONCELIK: olculdu (13 Agu 2026, h_ileri hali) — motor `fark < -gecikme`
    oldugunda HEM `[H14] ... ILERIDE — tutarsiz` FAIL'ini HEM de `H14: hafiza
    projeyle es` notunu basiyor (ikinci kosul `if fark > gecikme / else` oldugu
    icin ters yon `else` dalina dusuyor). Ilk satiri alan bir okuyucu bu hali
    "es" saniyor. Bu bir DAVRANIS bulgusudur, bolmenin urunu degildir: bolme
    ONCESI motor da ayni ikisini basar (altin kume BIT-BIT ayni oldugu icin
    biliniyor) — burada yalniz GORUNUR kilindi, DUZELTILMEDI (refactor turunda
    davranis degistirilmez)."""
    satirlar = [s.strip() for s in cikti.split("\n")]
    for d in satirlar:
        if d.startswith("[H14]"):
            return d
    for d in satirlar:
        if d.startswith(("· H14", "? H14", "H14:")) or " H14:" in d[:12]:
            return d
    return None


# --------------------------------------------------------------------- MUTANTLAR
# Hedef dizgeler CAGRI satirlarini gosterir (TANIM satiri baska bicimdedir).
CAGRI_ADAY = "        adaylar = _h14_adaylar(kok, y)"
CAGRI_ENYENI = "        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, adaylar, git_var, kirli, izlenen)"
CAGRI_HUKUM = "        _h14_hukum(F, N, gecikme, t_son, en_yeni_t, en_yeni_f)"
KORUMA_KAPALI = "    if gecikme <= 0:"

MUTANTLAR = [
    ("M-H14a KENAR git_var", "GIT DURUMU -> EN YENI: git_var kenari kopar (hep False)",
     [(CAGRI_ENYENI, "        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, adaylar, False, kirli, izlenen)")]),
    ("M-H14b KENAR kirli", "GIT DURUMU -> EN YENI: kirli kumesi kopar (degismis dosya 'temiz' sayilir)",
     [(CAGRI_ENYENI, "        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, adaylar, git_var, set(), izlenen)")]),
    ("M-H14c KENAR izlenen", "GIT DURUMU -> EN YENI: izlenen kumesi kopar (her dosya mtime ile olculur)",
     [(CAGRI_ENYENI, "        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, adaylar, git_var, kirli, set())")]),
    ("M-H14d KENAR adaylar", "ADAY TARAMA -> EN YENI: aday listesi kopar (bos liste)",
     [(CAGRI_ENYENI, "        en_yeni_t, en_yeni_f = _h14_en_yeni(kok, [], git_var, kirli, izlenen)")]),
    ("M-H14e KENAR en_yeni", "EN YENI -> HUKUM: olculen tarih kopar (None)",
     [(CAGRI_HUKUM, "        _h14_hukum(F, N, gecikme, t_son, None, None)")]),
    ("M-H14f TOLERANS", "EN YENI -> HUKUM: gecikme tolerans kenari kopar (esik sonsuz — kapi sessizce kapanir)",
     [(CAGRI_HUKUM, "        _h14_hukum(F, N, 10 ** 6, t_son, en_yeni_t, en_yeni_f)")]),
    ("M-H14g KORUMA SOKME", "ince _kapi_h14: 'kapi KAPALI' dali silinir (gecikme=0 iken kapi yine de kosar)",
     [(KORUMA_KAPALI, "    if False:")]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:55]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def altin_isiriyor_mu(sabotajli):
    """`altin_cikti.py --karsilastir` bu sabotaji GORUYOR mu?

    (True, 'fark VAR') · (False, 'FARK YOK') · (None, sebep)"""
    if not (os.path.isfile(ALTIN_ARAC) and os.path.isfile(ALTIN_KUME)):
        return None, "altin arac/kume yok"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", ALTIN_ARAC,
                            "--motor", sabotajli, "--karsilastir", ALTIN_KUME],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900)
    except Exception as e:
        return None, "kosulamadi: %s" % e
    c = (r.stdout or "") + (r.stderr or "")
    if "FARK YOK" in c:
        return False, "FARK YOK"
    m = re.search(r"(\d+)\s+(?:olcumde|olcum)\s+FARK", c) or re.search(r"FARK.*?(\d+)", c)
    return True, ("fark VAR" + (" (%s)" % m.group(1) if m else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    ap.add_argument("--altin-atla", action="store_true",
                    help="ikinci sutunu (altin kume) kosma — hizli deneme")
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz.")
        return 2

    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("H14 ALT-BOLME MUTANTI — parcalar arasi kenarlar OLCULUYOR mu?")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h14mut_")
    try:
        try:
            kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
            referans = kume_olc(motor, kokler, os.path.join(taban, "ref"))
            ikinci = kume_olc(motor, kokler, os.path.join(taban, "ref2"))
        except Kurulamadi as e:
            print("OLCULEMEDI: referans/temiz kol kurulamadi: %s" % e)
            return 2
        tk = farklari_bul(referans, ikinci)
        print("  TEMIZ KOL (ayni motor 2 kez)   %s"
              % ("FARK YOK" if not tk else "FARK VAR: %s" % tk[:3]))
        if tk:
            print("\nOLCULEMEDI: duzenek determinist degil — mutant hukmu ANLAMSIZ.")
            return 2
        print("  referans olcum sayisi          %d" % len(referans))

        # HAL KAPISI: her hal H14'u ATESLEMELI. Ateslemeyen hal, butun mutantlari
        # sessizce "temiz" gosterir — kor kumenin ta kendisi.
        imzalar = {ad: referans[(ad, "kapi")] for ad, _ in HALLER}
        atessiz = [ad for ad, _ in HALLER if _h14_satiri(imzalar[ad][1]) is None]
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            print("     %-10s exit %s · %s" % (ad, e, (_h14_satiri(c) or "(H14 SATIRI YOK)")[:64]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H14'u hic ateslemedi: %s" % ", ".join(atessiz))
            print("  Bu kumede mutant hukmu ANLAMSIZ olurdu (sahte yesil).")
            return 2
        if tekil < 2:
            print("\nOLCULEMEDI: haller birbirinden ayrismiyor — kume korlestirici.")
            return 2
        print(CIZGI)
        print("  %-22s %-11s %-26s %s" % ("mutant", "KENDI", "iz", "ALTIN KUME"))
        print(CIZGI)

        isirdi, kacti, olculemedi, altin_kor = [], [], [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yeni = kume_olc(sab, kokler, os.path.join(d, "hal"))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-22s OLCULEMEDI  %s" % (ad, e))
                sys.stdout.flush()
                continue
            farklar = farklari_bul(referans, yeni)
            if a.altin_atla:
                alt_txt = "(atlandi)"
            else:
                alt, alt_sebep = altin_isiriyor_mu(sab)
                alt_txt = {True: "ISIRDI", False: "KOR (FARK YOK)", None: "OLCULEMEDI"}[alt]
                if alt is False:
                    altin_kor.append(ad)
                if alt is None:
                    alt_txt += " · " + alt_sebep
            if farklar:
                isirdi.append(ad)
                haller_izi = sorted({k[0] for k, _ in farklar})
                print("  +  %-22s ISIRDI      %-26s %s"
                      % (ad, "%d olcum: %s" % (len(farklar), ",".join(h[2:] for h in haller_izi)[:14]),
                         alt_txt))
            else:
                kacti.append(ad)
                print("  !  %-22s KACTI       %-26s %s" % (ad, "-", alt_txt))
                print("     -> kenar BU KUMEDE KOR: %s" % aciklama)
            sys.stdout.flush()
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if not a.altin_atla:
        if altin_kor:
            print("  ALTIN KUME %d mutanta KOR: %s" % (len(altin_kor), ", ".join(altin_kor)))
            print("  -> Bu mutant o kadar sinif icin GERCEK kapsam ekliyor;")
            print("     altin kume tek basina bolmeyi o noktalarda KANITLAMIYORDU.")
        else:
            print("  ALTIN KUME her mutanti gordu — bu mutant KANIT olarak kalir,")
            print("  yeni kapsam eklemez. (Bu da bir olcumdur, eksiklik degildir.)")
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kenar saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kumenin KOR oldugu kenar.")
        return 1
    print("  H14 bolmesinin her kenari olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

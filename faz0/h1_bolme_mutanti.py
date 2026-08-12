#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H1 ALT-BOLME MUTANTI — `_kapi_h1`'in bes parcasi arasindaki kenarlar OLCULUYOR mu?

NEDEN AYRI BIR MUTANT
---------------------
12 Agu 2026'da `_kapi_h1` bes parcaya bolundu ve kabul olcutu olarak altin kume
(`faz0/altin_kapi.json`, 22 olcum) BIT-BIT tuttu. Ama o olcut sunu kanitlar:
**bugunku kod ayni davraniyor.** Sunu KANITLAMAZ: bir kenar yarin sessizce
koparsa HERHANGI bir olcum kirmizi olur mu?

Altin kumenin 11 hali cogunlukla temiz/basit projedir. Bir KOVA kenari koparsa
o hallerin hicbirinde cikti degismeyebilir — yani kod dogru ama KANITSIZ kalir.
FAZ C'de tam olarak bu olculdu: `bl`/`ks` kenarlari koparildiginda altin
karsilastirma "FARK YOK" diyordu (bkz. fazC_bolme_mutanti.py basligi).

Bu dosya o boslugu H1 icin kapatir. Kendi hallerini kurar (altin referansa
DOKUNMAZ), referansi kosum aninda temiz motordan alir ve yedi kusuru tek tek
enjekte eder.

IKI SUTUN HALINDE OLCER — ASIL SORU BUDUR
    KENDI KUMESI : bu betigin hallerinde fark var mi?
    ALTIN KUME   : `altin_cikti.py --karsilastir` ayni kusuru goruyor mu?

    Ikisi de ISIRIRSA  -> kenar zaten kapsamda; bu mutant KANIT olarak kalir.
    Yalniz kendi kumesi -> altin kume O SINIFA KOR; bu mutant GERCEK kapsam ekler.
    Ikisi de kacarsa   -> kenar HIC olculmuyor; bolme o noktada kanitsizdir.

    FARK VAR   -> ISIRDI      kenar olculuyor
    FARK YOK   -> KACTI       kenar icin KOR
    kurulamadi -> OLCULEMEDI  ARAC KUSURU (Y-4 dersi: sahte kirmizi uretme)

KULLANIM
    python3 faz0/h1_bolme_mutanti.py
    python3 faz0/h1_bolme_mutanti.py --altin-atla     (hizli; ikinci sutun kosulmaz)

CIKIS KODU
    0  her mutant KENDI KUMESINDE ISIRDI
    1  en az bir mutant KACTI
    2  OLCULEMEDI / duzenek kurulamadi
"""
import argparse
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
_RE_GUN = re.compile(r"\b\d+ gun once\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun once", m)


# --------------------------------------------------------------- PROJE HALLERI
# Her hal H1'in FARKLI bir dalini uyandirmak icin vardir. Temiz proje tek basina
# YETMEZ: H1 saglikli projede sessizdir, dolayisiyla yalniz temiz halle olculen
# bir kenar mutanti KACAR (FAZ C'de h_arsiv hali tam bu yuzden eklenmisti).
HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h1 mutanti icin ilk kayit"],
            ["derle"]]

HALLER = [
    ("h_temiz", None),
    ("h_kayip", "canlidan_sil"),       # snapshot'ta var, canlida yok -> H1 KAYIP
    ("h_fazla", "canliya_ekle"),       # beyansiz satir            -> --siki FAZLA
    ("h_yeni_cakisma", "yeni_cakis"),  # _YENI_SATIRLAR'da snapshot satiri
    ("h_snapsiz", "snap_sil"),         # _KAYNAK.md yok            -> koruma dali
]

OLCUM_KOMUTLARI = [["kapi"], ["kapi", "--siki"]]


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _icerik_satiri(p):
    """Canlidan silinmeye/kopyalanmaya UYGUN ilk satir (baslik/isaret degil)."""
    for s in open(p, encoding="utf-8").read().splitlines():
        d = s.strip()
        if len(d) > 25 and not d.startswith(("#", ">", "|", "-", "<!--", "```")):
            return s
    return None


def hal_kur(motor, ad, ozel, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H1MUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))

    h = os.path.join(kok, "arsiv", "hafiza")
    canli = os.path.join(kok, "PROJE_HAFIZA.md")
    snap = os.path.join(h, "_KAYNAK.md")

    if ozel == "canlidan_sil":
        hedef = _icerik_satiri(snap)
        if hedef is None:
            raise Kurulamadi("snapshot'ta silinebilir icerik satiri yok")
        s = open(canli, encoding="utf-8").read()
        if hedef not in s:
            raise Kurulamadi("snapshot satiri canlida bulunamadi — hal kurulamaz")
        with open(canli, "w", encoding="utf-8", newline="") as f:
            f.write(s.replace(hedef + "\n", "", 1))
    elif ozel == "canliya_ekle":
        with open(canli, "a", encoding="utf-8", newline="") as f:
            f.write("\nBu satir hicbir deftere BEYAN EDILMEDI ve kovada da yoktur.\n")
    elif ozel == "yeni_cakis":
        hedef = _icerik_satiri(snap)
        if hedef is None:
            raise Kurulamadi("snapshot'ta kopyalanabilir satir yok")
        with open(os.path.join(h, "_YENI_SATIRLAR.txt"), "a",
                  encoding="utf-8", newline="") as f:
            f.write(hedef.strip() + "\n")
    elif ozel == "snap_sil":
        if not os.path.isfile(snap):
            raise Kurulamadi("_KAYNAK.md zaten yok")
        os.remove(snap)
    return kok


def haller_kur(motor_temiz, taban):
    """Halleri BIR KEZ ve TEMIZ motorla kurar; {ad: kok} dondurur.

    🔴 NEDEN TEMIZ MOTOR: olculdu 12 Agu 2026 — hal kurulumu `derle` icerir ve
    `derle` kapi FAIL verirse derlemeyi REDDEDER. Sabotajli motorla kurmaya
    calisildiginda `var`/`canliA` kenarlarini koparan iki mutant kurulum
    asamasinda coktu ve OLCULEMEDI dondu; oysa kenar pekala olculebilirdi.
    Sabotaj OLCEN motordadir, olculen PROJEDE degil — hal uretimi degiskenden
    ayrilir. Yan fayda: butun kollar BIT-BIT ayni proje agacini olcer."""
    kokler = {}
    for ad, ozel in HALLER:
        kokler[ad] = hal_kur(motor_temiz, ad, ozel, taban)
    return kokler


def kume_olc(motor, kokler, hedef_taban):
    """Halleri kopyalayip verilen motorla olcer. {(hal, komut): (exit, cikti)}

    Kopya sart: `kapi` bir olcum komutu olsa da yazma yapmadigi KANITLANMADI;
    kollar arasinda paylasilan agac bir kolun digerini kirletmesine acik olurdu."""
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


# --------------------------------------------------------------------- MUTANTLAR
# Hedef dizgeler CAGRI satirlarini gosterir (TANIM satiri baska bicimdedir).
CAGRI_FARK = "    _h1_fark(F, N, y, siki, bekle, var)"
CAGRI_KOVA = "    _h1_kova(F, y, snapL, duz, canliA)"
CAGRI_BEK = "        bek = _h1_kova_bek(kv, snapL, duz)"
KORUMA = "    if not os.path.isfile(y.snap):\n        return\n"

MUTANTLAR = [
    ("M-H1a KENAR bekle", "BEYAN -> FARK kenari kopar (bekle yerine bos cok-kume)",
     [(CAGRI_FARK, "    _h1_fark(F, N, y, siki, {}, var)")]),
    ("M-H1b KENAR var", "GERCEK -> FARK kenari kopar (var yerine bos cok-kume)",
     [(CAGRI_FARK, "    _h1_fark(F, N, y, siki, bekle, {})")]),
    ("M-H1c KENAR snapL", "BEYAN -> KOVA kenari kopar (snapL yerine bos liste)",
     [(CAGRI_KOVA, "    _h1_kova(F, y, [], duz, canliA)")]),
    ("M-H1d KENAR canliA", "GERCEK -> KOVA kenari kopar (canliA yerine bos liste)",
     [(CAGRI_KOVA, "    _h1_kova(F, y, snapL, duz, [])")]),
    ("M-H1e SAFLIK KENARI", "_h1_kova_bek atlanir; yalniz ek_canli kalir (CANLI kova taramasi duser)",
     [(CAGRI_BEK, '        bek = list(kv.get("ek_canli", []))')]),
    ("M-H1f KORUMA SOKME", "snapshot yoklugu korumasi silinir (ince _kapi_h1)",
     [(KORUMA, "")]),
    ("M-H1g SIRA", "FARK ile KOVA yer degistirir (cikti sirasi sozlesmedir)",
     [(CAGRI_FARK + "\n" + CAGRI_KOVA, CAGRI_KOVA + "\n" + CAGRI_FARK)]),
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

    (True, 'N olcumde fark') · (False, 'FARK YOK') · (None, sebep)"""
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
    print("H1 ALT-BOLME MUTANTI — parcalar arasi kenarlar OLCULUYOR mu?")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h1mut_")
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

        # HALLERIN AYIRT EDICILIGI: temiz motorda her hal FARKLI bir sey uretmeli.
        # Hepsi ayni ciktiysa kume tek hal kadar bilgi tasir ve mutantlar KACAR.
        imzalar = {ad: referans[(ad, "kapi")] for ad, _ in HALLER}
        tekil = len({(e, c) for e, c in imzalar.values()})
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), tekil))
        for ad, _ in HALLER:
            e, c = imzalar[ad]
            ilk = next((s.strip() for s in c.split("\n")
                        if s.strip().startswith(("SONUC", "[H1"))), "(hukum satiri yok)")
            print("     %-16s exit %s · %s" % (ad, e, ilk[:74]))
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
                print("  +  %-22s ISIRDI      %-26s %s"
                      % (ad, "%d olcumde fark" % len(farklar), alt_txt))
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
    print("  H1 bolmesinin her kenari olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ C — BOLME MUTANTI: bolmeye ozgu kusurlar OLCULUYOR mu?

NEDEN AYRI BIR MUTANT
---------------------
`faz0/altin_cikti.py` bir refactoring'in ciktisini bit-bit kiyaslar, ama neyi
GORDUGU kullandigi PROJE HALLERINE baglidir. Olculdu (11 Agu 2026): altin
kumenin bes hali H12'nin "CANLI BAYAT" dalina HIC UGRAMIYOR; dolayisiyla
`_kapi_h10 -> _kapi_h12` (bl) ve `_kapi_h11 -> _kapi_h12` (ks) kenarlari
koparildiginda altin karsilastirma "FARK YOK" diyordu. Yani o iki kenar icin
esdegerlik hukmu YOKTU — kod dogruydu ama KANITSIZDI.

Bu dosya o boslugu kapatir. Kendi hallerini kurar (altin referansa DOKUNMAZ),
temiz motordan referansi kosum aninda alir ve bolmeye ozgu alti kusuru tek tek
enjekte edip ciktinin DEGISMESINI bekler:

    * kapi SIRASI kayar                    (H15, H14'ten ONCE kosmali)
    * kapilar arasi tasinan veri kaybolur  (bl · ks · t_son)
    * toplayici bir kanali yutar           (_kapi_ekle icindeki N / O)

    FARK VAR   -> ISIRDI      kapi bu sinifi olcuyor
    FARK YOK   -> KACTI       kapi bu sinif icin KOR
    kurulamadi -> OLCULEMEDI  ARAC KUSURU (Y-4 dersi: sahte kirmizi uretme)

KULLANIM
    python3 faz0/fazC_bolme_mutanti.py
    python3 faz0/fazC_bolme_mutanti.py --karsilastir-motor /yol/eski_hafiza.py

Ikinci bicim bir DIFERANSIYEL olcumdur: iki motoru ayni haller uzerinde kosar
ve FARK YOK bekler. Faz C teslim edilirken bolme ONCESI motora karsi kosuldu.

CIKIS KODU
    0  her mutant ISIRDI (ya da diferansiyel: FARK YOK)
    1  en az bir mutant KACTI / diferansiyelde FARK VAR
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
CIZGI = "-" * 82

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")
_RE_GUN = re.compile(r"\b\d+ gun once\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin kor oldugu anlamina GELMEZ."""


def normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    m = _RE_TARIH.sub("<TARIH>", m)
    return _RE_GUN.sub("<GUN> gun once", m)


# --------------------------------------------------------------- PROJE HALLERI
# h_bl / h_ks BILEREK vardir: H12'nin "CANLI BAYAT" dali yalniz bir konuda
# CANLI BLOKTAN DAHA YENI bir kayit varken kosar; altin kumenin halleri o dala
# hic ugramaz. Tarih ELLE 2030'a cekilir — determinist, sabit, saate bagli degil.
GELECEK = "2030-01-01"

HALLER = [
    ("h_derlenmis", [["not", "--konu=genel-durum", "--metin=fazC mutanti icin ilk kayit"],
                     ["derle"]], None),
    ("h_bl", [["not", "--konu=genel-durum", "--metin=fazC mutanti icin ilk kayit"],
              ["derle"],
              ["not", "--konu=genel-durum", "--metin=fazC mutanti icin ikinci kayit"]], "fragman"),
    ("h_ks", [["not", "--konu=genel-durum", "--metin=fazC mutanti icin ilk kayit"],
              ["derle"],
              ["karar", "--baslik=Kenar kapisi", "--konu=genel-durum"]], "karar"),
    # h_kesilme: BIR KAPININ ICINDE once bulgu, sonra olumcul hata.
    # _KAYNAK.md kurcalanir  -> H0 "CIPA BOZULDU" bulgusu yazilir
    # _ZINCIR.jsonl UTF-8 degil -> AYNI kapida zincir_dogrula -> oldur()
    # Bu hal BILEREK vardir: bolmenin ilk (saf donuslu) bicimi bu halde H0
    # bulgusunu YUTUYORDU ve exit 1 -> exit 3 oluyordu. Olculdu 11 Agu 2026.
    ("h_kesilme", [["not", "--konu=genel-durum", "--metin=fazC mutanti icin ilk kayit"],
                   ["derle"]], "kesilme"),
    # h_arsiv: arsivde DIZINDE OLMAYAN bir dosya. H6 saglikli projede HICBIR
    # SEY basmaz (3 fail, 0 not) — yani H6 dagitimdan silinse fark GORUNMEZ.
    # Olculdu 11 Agu 2026: bu hal eklenmeden "kapi dusurme" mutanti KACIYORDU.
    ("h_arsiv", [["not", "--konu=genel-durum", "--metin=fazC mutanti icin ilk kayit"],
                 ["derle"]], "arsiv_fazlasi"),
]

OLCUM_KOMUTLARI = [["kapi"], ["kapi", "--siki"]]

# MUTLAK OLCUT — diferansiyele bagli DEGIL, kendi basina bir sozlesme maddesi.
# cmd_kapi'nin belgeledigi garanti: "ne olursa olsun O ANA KADAR TOPLANAN
# hukum basilir" ve "gercek bir kapi bulgusu VARSA 1 doner".
KESILME_BEKLENEN_METIN = "[H0] CIPA BOZULDU"
KESILME_BEKLENEN_EXIT = 1


def _tarihi_ilerlet(p):
    s = open(p, encoding="utf-8").read()
    yeni, n = re.subn(r"(?m)^tarih:.*$", "tarih: " + GELECEK, s, count=1)
    if n != 1:
        raise Kurulamadi("front-matter 'tarih:' satiri bulunamadi: %s" % os.path.basename(p))
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(yeni)


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def hal_kur(motor, ad, adimlar, ozel, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "FAZC"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in adimlar:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))
    if ozel == "fragman":
        d = os.path.join(kok, "gunluk")
        aday = sorted(f for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []
        if not aday:
            raise Kurulamadi("gunluk/ bos — bl hali kurulamadi")
        _tarihi_ilerlet(os.path.join(d, aday[0]))
    elif ozel == "karar":
        d = os.path.join(kok, "kararlar")
        # 0000-DIZIN.md URETILIR bir dosyadir; hedef ILK GERCEK ADR'dir.
        aday = sorted(f for f in os.listdir(d) if re.match(r"^0*[1-9]\d*-.*\.md$", f)) \
            if os.path.isdir(d) else []
        if not aday:
            raise Kurulamadi("kararlar/ icinde ADR yok — ks hali kurulamadi")
        _tarihi_ilerlet(os.path.join(d, aday[0]))
    elif ozel == "arsiv_fazlasi":
        h = os.path.join(kok, "arsiv", "hafiza")
        if not os.path.isdir(h):
            raise Kurulamadi("arsiv/hafiza yok — arsiv hali kurulamadi")
        with open(os.path.join(h, "HAFIZA_99.md"), "w", encoding="utf-8", newline="") as f:
            f.write("# ARSIV 99 (dizinde YOK)\n")
    elif ozel == "kesilme":
        h = os.path.join(kok, "arsiv", "hafiza")
        snap, zincir = os.path.join(h, "_KAYNAK.md"), os.path.join(h, "_ZINCIR.jsonl")
        if not (os.path.isfile(snap) and os.path.isfile(zincir)):
            raise Kurulamadi("_KAYNAK.md / _ZINCIR.jsonl yok — kesilme hali kurulamadi")
        with open(snap, "ab") as f:
            f.write(b"\n<!-- kurcalandi -->\n")
        with open(zincir, "ab") as f:
            f.write(b"\xff\xfe gecersiz\n")
    return kok


def kume_uret(motor, taban):
    """{(hal, komut): (exit, normallestirilmis cikti)}"""
    out = {}
    for ad, adimlar, ozel in HALLER:
        kok = hal_kur(motor, ad, adimlar, ozel, taban)
        for komut in OLCUM_KOMUTLARI:
            rc, c = kos(motor, komut, kok)
            out[(ad, " ".join(komut))] = (rc, normalize(c, kok))
    return out


def kesilme_sozlesmesi(motor, taban):
    """MUTLAK OLCUT: kapi-ici kesilmede o ana kadarki bulgu BASILIR ve exit 1 olur.

    Diferansiyele bagli degildir — referans motor olmasa da hukum verir.
    (True, '') ya da (False, sebep) dondurur; kurulamazsa Kurulamadi atar."""
    kok = hal_kur(motor, "sozlesme", HALLER[-1][1], "kesilme", taban)
    rc, c = kos(motor, ["kapi"], kok)
    eksik = []
    if KESILME_BEKLENEN_METIN not in c:
        eksik.append("bulgu KAYIP (%s yok)" % KESILME_BEKLENEN_METIN)
    if rc != KESILME_BEKLENEN_EXIT:
        eksik.append("exit %s (beklenen %s)" % (rc, KESILME_BEKLENEN_EXIT))
    return (not eksik), " · ".join(eksik)


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
# DIKKAT: hedef dizgeler CAGRI satirini gosterir. Ciplak imza dizgesi TANIM
# satirinda da gecer (2 kez) ve mutant kurulamaz; olculdu 11 Agu 2026.
MUTANTLAR = [
    ("M-C1 SIRA", "H15 ile H14 yer degistirir (cikti sirasi sozlesmedir)",
     [("    _kapi_h15(F, N, O, rc, y)\n    _kapi_h14(F, N, O, kok, rc, y, t_son)",
       "    _kapi_h14(F, N, O, kok, rc, y, t_son)\n    _kapi_h15(F, N, O, rc, y)")]),
    ("M-C2 KENAR t_son", "H12 -> H14 kenari kopar (t_son yerine None)",
     [("    _kapi_h14(F, N, O, kok, rc, y, t_son)",
       "    _kapi_h14(F, N, O, kok, rc, y, None)")]),
    ("M-C3 KENAR bl", "H10 -> H12 kenari kopar (bl yerine bos liste)",
     [("    t_son = _kapi_h12(F, N, O, rc, y, bl, ks)",
       "    t_son = _kapi_h12(F, N, O, rc, y, [], ks)")]),
    ("M-C4 KENAR ks", "H11 -> H12 kenari kopar (ks yerine bos liste)",
     [("    t_son = _kapi_h12(F, N, O, rc, y, bl, ks)",
       "    t_son = _kapi_h12(F, N, O, rc, y, bl, [])")]),
    ("M-C5 BULGU KAYBI", "H0'in bulgulari toplayiciya DEGIL cope yazilir",
     [("    _kapi_h0(F, N, O, y)\n", "    _kapi_h0([], [], [], y)\n")]),
    ("M-C6 KAPI DUSURME", "H6 dagitimdan tamamen silinir",
     [("    _kapi_h6(F, N, O, y)\n", "")]),
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


def diferansiyel(motor, referans_motor):
    print(CIZGI)
    print("DIFERANSIYEL — iki motor ayni haller uzerinde AYNI mi?")
    print("  motor    : %s" % motor)
    print("  referans : %s" % referans_motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="fazC_dif_")
    try:
        a = kume_uret(referans_motor, os.path.join(taban, "ref"))
        b = kume_uret(motor, os.path.join(taban, "yeni"))
        s_ok, s_sebep = kesilme_sozlesmesi(motor, os.path.join(taban, "soz"))
    except Kurulamadi as e:
        print("OLCULEMEDI: %s" % e)
        return 2
    finally:
        shutil.rmtree(taban, ignore_errors=True)
    farklar = farklari_bul(a, b)
    print("  olcum sayisi: %d" % len(a))
    print("  kesilme sozlesmesi: %s" % ("TUTUYOR" if s_ok else "BOZUK: " + s_sebep))
    if not s_ok:
        farklar.append((("sozlesme",), s_sebep))
    if farklar:
        for k, s in farklar:
            print("  FARK  %-28s %s" % (" ".join(k), s))
        print(CIZGI)
        print("FARK VAR — iki motor ayni davranmiyor.")
        return 1
    print(CIZGI)
    print("FARK YOK — H12'nin bl/ks dallari dahil, iki motorun ciktisi BIT-BIT ayni.")
    return 0


def mutant_turu(motor):
    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("FAZ C BOLME MUTANTI — bolmeye ozgu kusurlar OLCULUYOR mu?")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="fazC_ref_")
    try:
        try:
            referans = kume_uret(motor, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: referans kume kurulamadi: %s" % e)
            return 2
        # TEMIZ KOL: ayni motor iki kez -> FARK YOK (duzenek determinist mi?)
        try:
            ikinci = kume_uret(motor, os.path.join(taban, "temiz2"))
        except Kurulamadi as e:
            print("OLCULEMEDI: temiz kol kurulamadi: %s" % e)
            return 2
        tk = farklari_bul(referans, ikinci)
        print("  TEMIZ KOL (ayni motor 2 kez)   %s" % ("FARK YOK" if not tk else "FARK VAR: %s" % tk[:3]))
        if tk:
            print()
            print("OLCULEMEDI: duzenek determinist degil — mutant hukmu ANLAMSIZ.")
            return 2
        print("  referans olcum sayisi          %d" % len(referans))
        # MUTLAK OLCUT once TEMIZ motorda tutmali; tutmuyorsa mutant konusmaz.
        try:
            ok, sebep = kesilme_sozlesmesi(motor, os.path.join(taban, "soz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: kesilme sozlesmesi kurulamadi: %s" % e)
            return 2
        print("  KESILME SOZLESMESI (temiz)     %s" % ("TUTUYOR" if ok else "BOZUK: " + sebep))
        if not ok:
            print()
            print("KIRMIZI: kapi-ici kesilmede bulgu kayboluyor — bolme davranisi DEGISTIRDI.")
            return 1
        print(CIZGI)

        isirdi, kacti, olculemedi = [], [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yeni = kume_uret(sab, os.path.join(d, "hal"))
                s_ok, s_sebep = kesilme_sozlesmesi(sab, os.path.join(d, "soz"))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-22s OLCULEMEDI  %s" % (ad, e))
                sys.stdout.flush()
                continue
            farklar = farklari_bul(referans, yeni)
            if farklar or not s_ok:
                isirdi.append(ad)
                iz = "%d olcumde fark" % len(farklar) if farklar else ""
                if not s_ok:
                    iz = (iz + " · " if iz else "") + "sozlesme BOZULDU"
                print("  +  %-22s ISIRDI      %s · %s" % (ad, iz, aciklama))
            else:
                kacti.append(ad)
                print("  !  %-22s KACTI       %s" % (ad, aciklama))
                print("     -> kapi BU SINIF icin KOR; bolme o sinifta OLCULMEMISTIR.")
            sys.stdout.flush()
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = esdegerlik olcumunun KOR oldugu sinif.")
        return 1
    print("  Bolmeye ozgu her sinif olculuyor.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    ap.add_argument("--karsilastir-motor", dest="referans", default="",
                    help="diferansiyel mod: bu motora karsi FARK YOK bekle")
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz.")
        return 2
    if a.referans:
        ref = os.path.abspath(a.referans)
        if not os.path.isfile(ref):
            print("OLCULEMEDI: referans motor yok: %s" % ref)
            return 2
        return diferansiyel(motor, ref)
    return mutant_turu(motor)


if __name__ == "__main__":
    sys.exit(main())

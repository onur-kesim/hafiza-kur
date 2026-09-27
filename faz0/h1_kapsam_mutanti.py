#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — H1 KAPSAM MUTANTI (Cowork is emri "H1 KAPSAM", 27 Eyl 2026, SIK A kilidi).

NEDEN VAR (olculdu: faz0/sabotaj.py, motor 559E830A…)
  H1 urunun ANA VAADINI olcer ("hicbir satir kaybolmadi") ve altı `fail()`
  cagrisinin ALTISI da `isir` icin KAPSAMSIZDI: herhangi biri silinse `isir`in
  38/38'i fark etmezdi. Sebeplerden biri `isir`in KENDI eslesme kurali: mutant,
  kapi ciktisinda `[H1]` YA DA `[H1-` gorunce "isirdi" sayilir; ornegin "satir
  KAYIP" kapatilinca ayni kaybi `[H1-KOVA]` da gordugu icin M-H1 yine isirir
  (ortusen tespit korlugu MASKELER). Bu betik H1'in her EKSENINI ayri, kendi
  METNIYLE olcer. `isir` DEGISMEDI (motor bu turda dokunulmaz — SIK B ayri is).

ALTI KOL — her biri GERCEK bir butunluk ihlali uretir, `kapi --siki` kosar ve
bulgunun O EKSENIN bulgusu oldugunu (eksenin BASLIK satiri + enjekte edilen
icerik birlikte) dogrular. Yalniz "H1 kirmizi" YETMEZ; yalniz ayrinti satiri
da YETMEZ (sabotajda `fail()` kalkar ama `- KAYIP:` ayrinti satirlari basilmaya
devam eder — ayrintiya bakan kol KORDUR).
  K1  sahte duzeltme      : DUZELTME kaynagi snapshot'ta YOK (muhurlu beyan)
  K2  gerekcesiz duzeltme : gercek duzeltme, gerekce < 10 karakter (muhurlu)
  K3  kayip maskeleme     : snapshot'ta ZATEN olan satir 'YENI' diye beyan (muhurlu)
  K4  okunamayan arsiv    : HAFIZA_99.md gecersiz UTF-8 (dizine de yazilir, H6 temiz)
  K5  satir KAYIP         : snapshot satiri canlidan silinir
  K6  beyansiz ekleme     : canliya beyansiz satir (--siki)
Her kolun ihlal ONCESI hali (ortak sablon) bu alti eksenden HICBIRINI basmaz
(olculur: "kapinin senaryosu kapiyi kirmizi yakabilir" sinifi).
Yan kapi bulgusu RAPORLANIR, gizlenmez: K5 ayni kaybi `[H1-KOVA]` ile de
uretir (ayri kapi, alti eksenden biri DEGIL).

POZITIF KONTROL — 6x6 MATRIS (varsayilan kip, KALICI): H1'in alti `fail()`
cagrisi faz0/sabotaj.py'nin KENDI fonksiyonlariyla (fail_cagrilari/sabote_et)
TEK TEK devre disi birakilir ve alti kol yeniden kosulur. Beklenen KOSEGEN:
fail k kapaliyken YALNIZ kol k KACAR. Kosegende isirma = kol o fail'e BAGLI
DEGIL; kosegen disi kacis = ORTUSME — ikisi de adiyla raporlanir, KIRMIZI.

KIPLER VE CIKIS KODLARI
  python faz0/h1_kapsam_mutanti.py
      Oz sinama: repo motorunda alti kol + 6x6 matris.
      0 = 6/6 ISIRDI ve matris tam kosegen · 1 = kacan / ortusme / kosegen
      eksigi · 2 = OLCULEMEDI.
  python faz0/h1_kapsam_mutanti.py --motor <yol>
      EK OLCER kipi (faz0/sabotaj.py --ek-olcer): yalniz alti kol, verilen
      motorla. 0 = hepsi ISIRDI ("EK-OLCER: ISIRDI") · 1 = en az bir kol KACTI
      ("EK-OLCER: KACTI ...") · 2 = OLCULEMEDI. Cokme ASLA 1 vermez: sabotaj.py
      1'i ancak "EK-OLCER: KACTI" satiriyla birlikte KAPSAMLI sayar.

NE OLCMEZ
  H1'in ciktisi olmayan dallar (ornegin `--siki` OLMADAN fazla satir: N notu).
  isir'in kendi H1 korlugu bu betikle KAPANMAZ; sabotaj.py'nin `isir ile`
  sutunu o korlugu AYRICA ve DEGISMEDEN gosterir.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")
CANLI = "PROJE_HAFIZA.md"


class Olculemedi(Exception):
    """Sablon/kurulum basarisiz — KOL HUKMU DEGILDIR."""


def kos(motor, kok, *argv):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(argv) + ["--kok=" + kok],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"), timeout=240)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _oku(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def _yaz(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


# ================================================================= EKSENLER
# Her eksenin BASLIK deseni (genel — sablon temizligi bunlarla olculur) ve
# kolun kendi enjeksiyonuna bagli KANIT denetimi (asagida, kol tanimlarinda).
EKSEN_BASLIK = {
    1: re.compile(r"^\s*\[H1\] beyan edilen DUZELTME kaynagi snapshot'ta YOK", re.M),
    2: re.compile(r"^\s*\[H1\] duzeltme \S+ GEREKCESIZ", re.M),
    3: re.compile(r"^\s*\[H1\] 'YENI' diye beyan edilen satir snapshot'ta ZATEN VAR", re.M),
    4: re.compile(r"^\s*\[H1\] \d+ arsiv dosyasi OKUNAMADI", re.M),
    5: re.compile(r"^\s*\[H1\] \d+ satir KAYIP", re.M),
    6: re.compile(r"^\s*\[H1\] \d+ satir BEYANSIZ EKLENMIS", re.M),
}
# fail() cagrisinin kaynak metnini eksene baglayan ifade (6x6 matris icin)
EKSEN_KAYNAK = {1: "sahte duzeltme", 2: "GEREKCESIZ", 3: "ZATEN VAR",
                4: "OKUNAMADI", 5: "satir KAYIP", 6: "BEYANSIZ EKLENMIS"}

K1_SATIR = "- sahte duzeltme ile gelen satir (h1 kapsam kol 1)"
K2_SATIR = "- sonraki adim guncellendi (h1 kapsam kol 2)"
K6_SATIR = "- beyansiz eklenen satir (h1 kapsam kol 6)"


def _canli(kok):
    return os.path.join(kok, CANLI)


def _hdir(kok):
    return os.path.join(kok, "arsiv", "hafiza")


def _canliya_ekle(kok, satir):
    s = _oku(_canli(kok))
    _yaz(_canli(kok), s.rstrip("\n") + "\n" + satir + "\n")


def _duzeltme_yaz(kok, kayit):
    _yaz(os.path.join(_hdir(kok), "_DUZELTMELER.json"),
         json.dumps({"duzeltmeler": [kayit]}, ensure_ascii=False, indent=2) + "\n")


def _muhurle(motor, kok, ad):
    k, c = kos(motor, kok, "muhur", "h1 kapsam olcumu: %s" % ad)
    if k != 0:
        raise Olculemedi("muhur basarisiz (exit %d): %s" % (k, c[-200:]))


def _canli_satirlari(kok):
    return _oku(_canli(kok)).split("\n")


def _snapshot_icerik_satiri(kok):
    """Snapshot'ta ve canlida duran, blok isareti/baslik OLMAYAN ilk icerik satiri."""
    snap = _oku(os.path.join(_hdir(kok), "_KAYNAK.md")).split("\n")
    canli = set(_canli_satirlari(kok))
    for s in snap:
        t = s.strip()
        if (len(t) > 20 and not t.startswith(("#", ">", "<!--")) and s in canli
                and _canli_satirlari(kok).count(s) == 1):
            return s
    raise Olculemedi("snapshot'ta uygun icerik satiri yok")


def k1_ihlal(motor, kok):
    """Sahte duzeltme: kaynagi snapshot'ta OLMAYAN bir duzeltme beyan edilir ve
    muhurlenir; 'yeni' satiri canliya da konur ki KAYIP/FAZLA dogmasin."""
    _canliya_ekle(kok, K1_SATIR)
    _duzeltme_yaz(kok, {"satir": 999, "eski": "bu satir snapshot'ta hic yok (h1 kapsam kol 1)",
                        "yeni": K1_SATIR, "gerekce": "olcum icin sahte duzeltme beyani"})
    _muhurle(motor, kok, "kol 1")
    return lambda c: re.search(r"^\s*\[H1\] beyan edilen DUZELTME kaynagi snapshot'ta YOK "
                               r"\(satir 999\)", c, re.M)


def k2_ihlal(motor, kok):
    """Gercek bir duzeltme (canlida da yapilmis) GEREKCESIZ beyan edilir."""
    L = _canli_satirlari(kok)
    try:
        i = L.index("- (boş)")
    except ValueError:
        raise Olculemedi("sablonda '- (boş)' satiri yok")
    L[i] = K2_SATIR
    _yaz(_canli(kok), "\n".join(L))
    _duzeltme_yaz(kok, {"satir": i + 1, "eski": "- (boş)", "yeni": K2_SATIR, "gerekce": "kisa"})
    _muhurle(motor, kok, "kol 2")
    return lambda c: re.search(r"^\s*\[H1\] duzeltme %d GEREKCESIZ" % (i + 1), c, re.M)


def k3_ihlal(motor, kok):
    """Snapshot'ta ZATEN olan satir 'YENI' diye beyan edilir (kayip maskeleme);
    ikinci kopyasi canliya da konur ki sayim dengede kalsin."""
    s = _snapshot_icerik_satiri(kok)
    _canliya_ekle(kok, s)
    p = os.path.join(_hdir(kok), "_YENI_SATIRLAR.txt")
    _yaz(p, _oku(p) + s + "\n")
    _muhurle(motor, kok, "kol 3")
    parca = s.strip()[:40]
    return lambda c: any(EKSEN_BASLIK[3].match(x) and parca in x for x in c.split("\n"))


def k4_ihlal(motor, kok):
    """Arsiv dosyasi okunamaz (gecersiz UTF-8); dizin satiri da yazilir ki H6
    yan bulgu uretmesin."""
    with open(os.path.join(_hdir(kok), "HAFIZA_99.md"), "wb") as f:
        f.write(b"\xff\xfe bozuk arsiv \xfa\n")
    L = _canli_satirlari(kok)
    try:
        i = L.index("<!-- /v2-arsiv-dizini -->")
    except ValueError:
        raise Olculemedi("sablonda arsiv dizini alt blogu yok")
    L.insert(i, "- `arsiv/hafiza/HAFIZA_99.md` — 1 satır, 18 B")
    _yaz(_canli(kok), "\n".join(L))
    return lambda c: any(EKSEN_BASLIK[4].match(x) and "HAFIZA_99.md" in x for x in c.split("\n"))


def k5_ihlal(motor, kok):
    """Snapshot satiri canlidan silinir (beyansiz, arsive de gitmez)."""
    s = _snapshot_icerik_satiri(kok)
    L = _canli_satirlari(kok)
    L.remove(s)
    _yaz(_canli(kok), "\n".join(L))
    parca = s.strip()[:40]
    return lambda c: bool(EKSEN_BASLIK[5].search(c)) and ("- KAYIP: " + parca) in c


def k6_ihlal(motor, kok):
    """Canliya beyansiz satir eklenir; `--siki` bunu BEYANSIZ EKLENMIS saymali."""
    _canliya_ekle(kok, K6_SATIR)
    return lambda c: bool(EKSEN_BASLIK[6].search(c)) and ("- FAZLA: " + K6_SATIR) in c


KOLLAR = [
    (1, "K1 sahte duzeltme", k1_ihlal),
    (2, "K2 gerekcesiz duzeltme", k2_ihlal),
    (3, "K3 kayip maskeleme (YENI zaten var)", k3_ihlal),
    (4, "K4 okunamayan arsiv", k4_ihlal),
    (5, "K5 satir KAYIP", k5_ihlal),
    (6, "K6 beyansiz ekleme (--siki)", k6_ihlal),
]


# =================================================================== KOSUM

def sablon_kur(motor, taban):
    """kur + not + derle (faz0/sabotaj.py'nin sablonuyla ayni akis)."""
    kok = os.path.join(taban, "sablon")
    os.makedirs(kok)
    for argv in (("kur", "--ad", "H1Kapsam"),
                 ("not", "--konu=genel-durum", "--metin=h1 kapsam sablonu ilk not")):
        k, c = kos(motor, kok, *argv)
        if k != 0:
            raise Olculemedi("sablon: %s exit %d: %s" % (argv[0], k, c[-200:]))
    kos(motor, kok, "derle")          # derle'nin kapanis kapisi sabotajda FAIL verebilir
    if not os.path.isfile(os.path.join(_hdir(kok), "_KAYNAK.md")):
        raise Olculemedi("sablon: snapshot (_KAYNAK.md) yok")
    k, c = kos(motor, kok, "kapi", "--siki")
    kirli = [e for e, d in EKSEN_BASLIK.items() if d.search(c)]
    if kirli:
        raise Olculemedi("sablon IHLAL ONCESI eksen bulgusu basiyor %s — kol olcemez" % kirli)
    return kok


def kollari_kos(motor):
    """Doner: {eksen: (hukum, eksenler, yan_kapilar, aciklama)}; hukum ISIRDI/KACTI/OLCULEMEDI."""
    taban = tempfile.mkdtemp(prefix="h1_kapsam_")
    sonuc = {}
    try:
        sablon = sablon_kur(motor, taban)
        for eksen, ad, fn in KOLLAR:
            kok = os.path.join(taban, "kol%d" % eksen)
            shutil.copytree(sablon, kok)
            try:
                kanit = fn(motor, kok)
            except Olculemedi as e:
                sonuc[eksen] = ("OLCULEMEDI", [], [], str(e))
                continue
            k, c = kos(motor, kok, "kapi", "--siki")
            eksenler = [e for e, d in EKSEN_BASLIK.items() if d.search(c)]
            yan = sorted(set(re.findall(r"^\s*\[(H[^\]]*)\]", c, re.M)) - {"H1"})
            sonuc[eksen] = ("ISIRDI" if kanit(c) else "KACTI", eksenler, yan,
                            "" if kanit(c) else "eksen bulgusu YOK (kapi exit %d)" % k)
    finally:
        shutil.rmtree(taban, ignore_errors=True)
    return sonuc


def _h1_hedefleri(kaynak):
    """sabotaj.py'nin KENDI fail() bulucusuyla H1 cagrilari -> {eksen: hedef}."""
    import sabotaj                                     # faz0/ sys.path[0]'dadir
    L = kaynak.split("\n")
    out = {}
    for h in sabotaj.fail_cagrilari(kaynak):
        if h["kapi"] != "H1":
            continue
        metin = "\n".join(L[h["lineno"] - 1:h["end_lineno"]])
        eslesen = [e for e, ifade in EKSEN_KAYNAK.items() if ifade in metin]
        if len(eslesen) != 1 or eslesen[0] in out:
            raise Olculemedi("H1 fail() (satir %d) tek bir eksene baglanamadi: %s"
                             % (h["lineno"], eslesen))
        out[eslesen[0]] = h
    if sorted(out) != sorted(EKSEN_KAYNAK):
        raise Olculemedi("H1'de %d fail() bulundu, 6 eksen bekleniyordu: %s"
                         % (len(out), sorted(out)))
    return out, sabotaj.sabote_et


def ek_olcer_kipi(motor):
    print("=== H1 KAPSAM (EK OLCER kipi) === motor: %s" % motor)
    try:
        sonuc = kollari_kos(motor)
    except (Olculemedi, subprocess.TimeoutExpired) as e:
        print("EK-OLCER: OLCULEMEDI — %s" % e)
        return 2
    kacan = [e for e, r in sonuc.items() if r[0] == "KACTI"]
    olc = [e for e, r in sonuc.items() if r[0] == "OLCULEMEDI"]
    for eksen, ad, _ in KOLLAR:
        print("  %-38s -> %s %s" % (ad, sonuc[eksen][0], sonuc[eksen][3]))
    if kacan:
        print("EK-OLCER: KACTI %s" % ",".join("K%d" % e for e in kacan))
        return 1
    if olc:
        print("EK-OLCER: OLCULEMEDI %s" % ",".join("K%d" % e for e in olc))
        return 2
    print("EK-OLCER: ISIRDI 6/6")
    return 0


def oz_sinama(motor):
    print("=== H1 KAPSAM MUTANTI === motor: %s · platform: %s" % (motor, sys.platform))
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    kirmizi, olculemeyen = 0, 0
    try:
        temiz = kollari_kos(motor)
    except (Olculemedi, subprocess.TimeoutExpired) as e:
        print("SONUC: OLCULEMEDI — %s" % e)
        return 2
    print("\n--- ALTI KOL (temiz motor; ihlal ONCESI sablon alti eksenden hicbirini basmiyor) ---")
    for eksen, ad, _ in KOLLAR:
        h, eksenler, yan, ac = temiz[eksen]
        not_ = ""
        if eksenler and eksenler != [eksen]:
            not_ = "  ORTUSME: baska H1 eksenleri de yandi %s" % [e for e in eksenler if e != eksen]
            kirmizi += 1
        print("  %-38s -> %-10s eksen=%s yan kapi=%s%s %s"
              % (ad, h, eksenler or "-", yan or "-", not_, ac))
        if h == "KACTI":
            kirmizi += 1
        elif h == "OLCULEMEDI":
            olculemeyen += 1

    print("\n--- POZITIF KONTROL: 6x6 MATRIS (satir: devre disi fail · sutun: kol · K=KACTI) ---")
    try:
        hedefler, sabote_et = _h1_hedefleri(kaynak)
    except (Olculemedi, ImportError) as e:
        print("  OLCULEMEDI — %s" % e)
        return 2
    print("  %-34s %s" % ("devre disi fail()", "  ".join("K%d" % e for e, _, _ in KOLLAR)))
    for eksen in sorted(hedefler):
        h = hedefler[eksen]
        d = tempfile.mkdtemp(prefix="h1_kapsam_sab_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="\n") as f:
                f.write(sabote_et(kaynak, h))
            try:
                satir = kollari_kos(sahte)
            except (Olculemedi, subprocess.TimeoutExpired) as e:
                print("  #%02d sat %-5d (eksen %d)          OLCULEMEDI — %s"
                      % (h["no"], h["lineno"], eksen, e))
                olculemeyen += 1
                continue
        finally:
            shutil.rmtree(d, ignore_errors=True)
        hucre = []
        for e, _, _ in KOLLAR:
            r = satir[e][0]
            hucre.append({"KACTI": "K", "ISIRDI": ".", "OLCULEMEDI": "?"}[r])
        kacan = [e for e, _, _ in KOLLAR if satir[e][0] == "KACTI"]
        belirsiz = [e for e, _, _ in KOLLAR if satir[e][0] == "OLCULEMEDI"]
        yorum = []
        if eksen not in kacan:
            yorum.append("KOSEGEN EKSIK: K%d bu fail() kapaliyken de ISIRDI (baska yoldan)" % eksen)
            kirmizi += 1
        disi = [e for e in kacan if e != eksen]
        if disi:
            yorum.append("ORTUSME: %s de KACTI" % ",".join("K%d" % e for e in disi))
            kirmizi += 1
        if belirsiz:
            yorum.append("OLCULEMEDI: %s" % ",".join("K%d" % e for e in belirsiz))
            olculemeyen += 1
        print("  #%02d sat %-5d (eksen %d: %-16s)   %s   %s"
              % (h["no"], h["lineno"], eksen, EKSEN_KAYNAK[eksen][:16],
                 "   ".join(hucre), "; ".join(yorum) or "kosegen"))
    print()
    if kirmizi:
        print("SONUC: KIRMIZI — %d kalem (kacan kol / ortusme / kosegen eksigi)." % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem olculemedi; sessiz PASS verilmez." % olculemeyen)
        return 2
    print("SONUC: YESIL — alti kol ISIRDI, 6x6 matris TAM KOSEGEN (ortusme YOK).")
    return 0


def main():
    _cikti_kodlamasini_guvenceye_al()
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default="", help="EK OLCER kipi: yalniz alti kol, bu motorla")
    a = ap.parse_args()
    if a.motor:
        return ek_olcer_kipi(os.path.abspath(a.motor))
    return oz_sinama(os.path.abspath(VARSAYILAN_MOTOR))


if __name__ == "__main__":
    sys.exit(main())

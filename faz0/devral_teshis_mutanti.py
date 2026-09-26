#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — DEVRAL TESHIS MUTANTI (devral GIRIS KAPISI, KALEM 2 — 26 Eyl 2026).

NEDEN VAR (olculdu: Cowork, pallets/click; yerelde Windows'ta tekrarlandi)
  `devral --esle canli=PROJE_HAFIZA.md` ciktisinin TRIYAJ'i
      5. [H6] 'ARSIV DIZINI bolumu yok' ... CIKIS YOLU: hafiza.py bolum-kur
      6. [H17] '## GUNCEL DURUM bolumu YOK' ... CIKIS YOLU: hafiza.py bolum-kur
  basiyordu; oysa AYNI komutun yazdigi dosyada iki bolum de vardi ve onerilen
  cikis yolu kosulunca "0 bolum eklendi (zorunlu bolumlerin hepsi zaten var)"
  diyordu. Arac onarim komutu veriyor, onarim komutu "onarilacak sey yok" diyordu
  — yabancinin gordugu ILK cikti kendini yalanliyordu (sinif: OKUNMADAN HUKUM).
  Kok: iki madde KOSULSUZ basiliyordu. Duzeltme: her madde, yazim bittikten
  SONRA diskteki canli o bolumu GERCEKTEN tasimiyorsa basilir
  (`_devral_triyaj_bolum`, olcut H6/`bolum-kur` ile ayni `_bolum_araligi`).

NE OLCER — DORT KOL, YALNIZ MESAJ EKSENI. Her kolda iki kosul BIRDEN:
(i) TRIYAJ'in [H6]/[H17] maddeleri beklenen kume ile AYNI, (ii) ayni projede
`bolum-kur --dene`nin hukmuyle CELISMIYOR ([H6] <=> ARSIV DIZINI eklenecek,
[H17] <=> GUNCEL DURUM eklenecek) — is emri kabul 2.
  KOL-A  YENI canli (devral sablondan yazar)        -> madde YOK
  KOL-B  Momentum sinifi (baska basliklar, ikisi yok) -> [H6] + [H17]
  KOL-C  basliksiz canli (devral 7 bolumu KENDI ekler) -> madde YOK
  KOL-D  kismi (GUNCEL DURUM var, ARSIV DIZINI yok)   -> YALNIZ [H6]

MUTANTLAR (hafiza.py kaynagina textual sabotaj)
  M-1  teshis YAZMA ONCESI durumdan (devral'in once taradigi basliklar) —
       26 Eyl oncesi sinif: KOL-A ve KOL-C ISIRMALI
  M-2  madde hic basilmaz (susturma)                 -> KOL-B/KOL-D ISIRMALI
  M-3  iki madde TEK ortak kosula baglanir           -> KOL-D ISIRMALI

ORTUSME OLCUMU (is emri kabul 3)
  Bu kapi, KARDES kapinin (faz0/devral_politika_mutanti.py, POLITIKA ekseni)
  mutantlari altinda YESIL KALMALIDIR. CIFT MUTANT: M-1, kardesin P-1'i ile
  BIRLIKTE uygulandiginda da bu kapi ISIRMALIDIR.

NE OLCMEZ
  1. `.hafizarc` politikasi (kardes kapinin ekseni).
  2. TRIYAJ'in 1-4. maddeleri (sabit tavsiye metni; kosula bagli degil).
  3. `bolum-kur`un kendisi (faz0/bolum_kur_mutanti.py olcer).

CIKIS KODLARI
  0  dort kol temiz, her mutant ISIRDI, ortusme YOK
  1  bir kol KIRMIZI · bir mutant KACTI · ortusme VAR
  2  OLCULEMEDI (motor okunamadi, mutant/fikstur kurulamadi) — sessiz PASS yok

KULLANIM
  python faz0/devral_teshis_mutanti.py [motor]
  POZITIF KONTROL: duzeltmeden ONCEKI motorla KOL-A ve KOL-C KIRMIZI yanar,
  mutant capalari 0 kez gecer (olculdu, commit mesajinda).
"""
import io
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


class Kurulamadi(Exception):
    """Fikstur KURULUMU basarisiz (devral, bolum-kur) — KAPI HUKMU DEGILDIR."""


def kos(motor, *argv, kok=None):
    """`_kapi_metni` ile AYNI cagri kalibi: -X utf8 + PYTHONIOENCODING=utf-8."""
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ============================================================== FIKSTURLER
# Her kol: (ad, canli dosya adi, canli icerigi | None=YENI, beklenen madde kumesi)

_MOMENTUM = ("# Test Projesi\n\n"
             "## Kalici dersler (dilimden bagimsiz)\n- ornek ders\n\n"
             "## Bilinen sinirlar\n- ornek sinir\n")
_BASLIKSIZ = ("Bu dosya yalniz duz metin tutuyor.\n"
              "Hic markdown basligi yok.\n")
_KISMI = ("# Test Projesi\n\n"
          "## GÜNCEL DURUM\n- proje yuruyor\n\n"
          "## Bilinen sinirlar\n- ornek sinir\n")

KOLLAR = (
    ("KOL-A", "PROJE_HAFIZA.md", None, set(), "yeni canli: madde YOK"),
    ("KOL-B", "DURUM.md", _MOMENTUM, {"H6", "H17"}, "Momentum sinifi: [H6]+[H17]"),
    ("KOL-C", "DURUM.md", _BASLIKSIZ, set(), "basliksiz canli: madde YOK"),
    ("KOL-D", "DURUM.md", _KISMI, {"H6"}, "kismi: YALNIZ [H6]"),
)

_MADDE = re.compile(r"^\s+(\d+)\. \[(H6|H17)\] ", re.M)
_EKLENECEK = re.compile(r"^\s+\+ (## .+?)\s*$", re.M)
# bolum-kur hukmu -> TRIYAJ maddesi (motorun bu iki bolume verdigi etiketler)
_ESDEGER = {"## ARSIV DIZINI": "H6", "## GUNCEL DURUM": "H17"}


def triyaj_maddeleri(cikti):
    """Yalniz `=== TRIYAJ ===` sonrasini okur (kapi raporundaki [H6]/[H17]
    bulgulari TRIYAJ maddesi DEGILDIR). Doner: (etiket kumesi, numaralar)."""
    i = cikti.find("=== TRIYAJ ===")
    if i < 0:
        raise Kurulamadi("devral ciktisinda '=== TRIYAJ ===' yok")
    bolum = cikti[i:]
    m = _MADDE.findall(bolum)
    return set(e for _n, e in m), [int(n) for n, _e in m]


def bolum_kur_hukmu(motor, kok):
    """`bolum-kur --dene` (tek bayt yazmaz): EKLENECEK bolumlerin etiket kumesi."""
    k, c = kos(motor, "bolum-kur", "--dene", kok=kok)
    if k != 0:
        raise Kurulamadi("bolum-kur --dene basarisiz (exit %d): %s" % (k, c[-200:]))
    if "0 bolum eklendi" in c:
        return set()
    return set(_ESDEGER[b] for b in _EKLENECEK.findall(c) if b in _ESDEGER)


def kol_kos(motor, taban, kol):
    ad, dosya, icerik, beklenen, _ne = kol
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if icerik is not None:
        with io.open(os.path.join(kok, dosya), "w", encoding="utf-8", newline="\n") as f:
            f.write(icerik)
    k, c = kos(motor, "devral", "--esle", "canli=" + dosya, kok=kok)
    if k != 0:
        raise Kurulamadi("devral basarisiz (exit %d): %s" % (k, c[-300:]))
    maddeler, numaralar = triyaj_maddeleri(c)
    b = []
    if maddeler != beklenen:
        b.append("TRIYAJ maddeleri %s, beklenen %s (disk: %s)"
                 % (sorted(maddeler) or "YOK", sorted(beklenen) or "YOK", dosya))
    if numaralar and numaralar != list(range(numaralar[0], numaralar[0] + len(numaralar))):
        b.append("TRIYAJ numaralari ardisik DEGIL: %s" % numaralar)
    bk = bolum_kur_hukmu(motor, kok)
    if maddeler != bk:
        b.append("devral ile bolum-kur CELISIYOR: TRIYAJ %s · bolum-kur --dene %s"
                 % (sorted(maddeler) or "YOK", sorted(bk) or "0 bolum"))
    return b


# ================================================================= MUTANTLAR

def _degistir(s, eski, yeni, etiket):
    n = s.count(eski)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [%s]: %r\n"
                         % (n, etiket, eski[:70]))
        return None
    return s.replace(eski, yeni, 1)


def m1_yazma_oncesi(s):
    """Teshis, devral'in YAZMADAN ONCE taradigi basliklardan basilir (yeni ve
    basliksiz canlida bu liste bos) -> KOL-A/KOL-C ISIRMALI."""
    return _degistir(s, "    _devral_triyaj_bolum(kok, satirlar(canli_p), 5)\n",
                     "    _devral_triyaj_bolum(kok, basliklar, 5)"
                     "  # MUTANT M-1: yazma ONCESI durum\n", "M-1")


def m2_susturma(s):
    """Madde hic basilmaz -> KOL-B/KOL-D ISIRMALI (bolum gercekten yokken sessizlik)."""
    return _degistir(s,
                     "        if _bolum_araligi(L, bolum)[0] is not None:\n"
                     "            continue\n",
                     "        continue  # MUTANT M-2: madde SUSTURULDU\n", "M-2")


def m3_tek_kosul(s):
    """Iki madde TEK ortak kosula baglanir (biri eksikse ikisi de basilir) ->
    KOL-D ISIRMALI."""
    return _degistir(s,
                     "        if _bolum_araligi(L, bolum)[0] is not None:\n",
                     "        if all(_bolum_araligi(L, b0)[0] is not None"
                     " for b0, _m in _TRIYAJ_BOLUM_MADDELERI):  # MUTANT M-3\n", "M-3")


MUTANTLAR = [
    ("M-1  teshis YAZMA ONCESI durumdan", m1_yazma_oncesi),
    ("M-2  madde hic basilmaz (susturma)", m2_susturma),
    ("M-3  iki madde tek ortak kosul", m3_tek_kosul),
]


# ===================================================================== main

def hukum(motor):
    """Dort kolu kosar: ({ad: [bulgu] | None}, olculemeyen, [not])."""
    sonuc, olculemeyen, notlar = {}, 0, []
    for kol in KOLLAR:
        taban = tempfile.mkdtemp(prefix="devral_teshis_")
        try:
            sonuc[kol[0]] = kol_kos(motor, taban, kol)
        except Kurulamadi as e:
            sonuc[kol[0]] = None
            olculemeyen += 1
            notlar.append("%s OLCULEMEDI — %s" % (kol[0], e))
        finally:
            shutil.rmtree(taban, ignore_errors=True)
    return sonuc, olculemeyen, notlar


def _kirmizi(sonuc):
    return [ad for ad, b in sonuc.items() if b]


def _sahte_motor(kaynak, d):
    try:
        compile(kaynak, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(d, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(kaynak)
    return p, None


def _mutant_hukmu(kaynak, fonklar):
    bozuk = kaynak
    for fn in fonklar:
        bozuk = fn(bozuk) if bozuk is not None else None
    if bozuk is None or bozuk == kaynak:
        return None, "mutant KURULAMADI (capa)"
    d = tempfile.mkdtemp(prefix="devral_teshis_mut_")
    try:
        sahte, hata = _sahte_motor(bozuk, d)
        if sahte is None:
            return None, hata
        sonuc, olc, notlar = hukum(sahte)
        kir = _kirmizi(sonuc)
        if olc and not kir:
            return None, "; ".join(notlar)[:200]
        # kirmizi VARKEN olculemeyen kollar da ADIYLA doner — sessizce dusmez
        olcmeyen = [ad for ad, b in sonuc.items() if b is None]
        return kir, ("; OLCULEMEDI: %s" % ", ".join(olcmeyen)) if olcmeyen else ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _kardes_mutantlari():
    """POLITIKA ekseninin mutantlari (tek kaynak: kardes betik)."""
    try:
        import devral_politika_mutanti as kardes   # faz0/ sys.path[0]'dadir
    except ImportError as e:
        return None, str(e)
    return kardes.MUTANTLAR, None


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN_MOTOR)
    print("=== DEVRAL TESHIS MUTANTI (KALEM 2) === motor: %s · platform: %s"
          % (motor, sys.platform))
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    olculemeyen = 0
    sonuc, olc, notlar = hukum(motor)
    olculemeyen += olc
    for kol in KOLLAR:
        b = sonuc[kol[0]]
        durum = "OLCULEMEDI" if b is None else ("KIRMIZI" if b else "YESIL (%s)" % kol[4])
        print("  %-6s: %s" % (kol[0], durum))
        for x in b or []:
            print("      - %s" % x)
    for n in notlar:
        print("      ! %s" % n)
    kirmizi = len(_kirmizi(sonuc))

    print("\n--- MUTANT SINAMASI (kendi ekseni: MESAJ) ---")
    kacan = 0
    for ad, fn in MUTANTLAR:
        kir, aciklama = _mutant_hukmu(kaynak, [fn])
        if kir is None:
            print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
            olculemeyen += 1
        elif kir:
            print("  %-48s -> ISIRDI (%s%s)" % (ad, ", ".join(kir), aciklama))
        else:
            print("  %-48s -> KACTI (dort kol da KOR)" % ad)
            kacan += 1

    print("\n--- ORTUSME OLCUMU (kardes eksen: POLITIKA — bu kapi YESIL KALMALI) ---")
    ortusen, olculen = 0, 0
    kardes, hata = _kardes_mutantlari()
    if kardes is None:
        print("  kardes betik yuklenemedi: %s -> OLCULEMEDI" % hata)
        olculemeyen += 1
    else:
        for ad, fn in kardes:
            kir, aciklama = _mutant_hukmu(kaynak, [fn])
            if kir is None:
                print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
                olculemeyen += 1
                continue
            olculen += 1
            if kir:
                print("  %-48s -> ORTUSME: bu kapi da yandi (%s%s)"
                      % (ad, ", ".join(kir), aciklama))
                ortusen += 1
            else:
                print("  %-48s -> ayri eksen (bu kapi YESIL kaldi)" % ad)
        # CIFT MUTANT: POLITIKA duzeltmesi de sokulmusken bu kapi hala ISIRIYOR mu?
        ad = "CIFT  M-1 + kardes P-1 (politika duzeltmesi de yok)"
        kir, aciklama = _mutant_hukmu(kaynak, [m1_yazma_oncesi, kardes[0][1]])
        if kir is None:
            print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
            olculemeyen += 1
        elif kir:
            print("  %-48s -> ISIRDI (%s%s)" % (ad, ", ".join(kir), aciklama))
        else:
            print("  %-48s -> KACTI (tespit kardes duzeltmeye BAGLI)" % ad)
            kacan += 1
    print("  ortusme: %d / %d OLCULEN kardes mutant (toplam %d)"
          % (ortusen, olculen, len(kardes or [])))

    print()
    if kacan or ortusen:
        print("SONUC: KIRMIZI — %d mutant KACTI, %d ortusme." % (kacan, ortusen))
        return 1
    if kirmizi:
        print("SONUC: KIRMIZI — %d kol temiz motorda kirmizi (mutant sinamasindan ONCE)."
              % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem kosulamadi/kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    print("SONUC: YESIL — dort kol temiz, her mutant ISIRDI, ortusme YOK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

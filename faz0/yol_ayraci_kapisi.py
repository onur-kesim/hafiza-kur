#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — YOL AYRACI KAPISI + kendi mutantlari.

NEDEN VAR (olculdu 14 Agu 2026, GERCEK Windows kosumunda)
  `devral` bir gercek projede kosturuldu ve su satiri basti:
      Windows :   YEDEK: arsiv\\hafiza\\v2\\_DEVIR_ONCESI_2026-08-14.md
      Linux   :   YEDEK: arsiv/hafiza/v2/_DEVIR_ONCESI_2026-08-14.md
  AYNI kosumun H4 satirlari her iki platformda da duz bolu basiyordu; yani tek
  ciktinin icinde KARISIK ayrac vardi.

  Kok neden: `os.path.relpath` motorda 22 kez cagriliyordu; cevirim her cagri
  yerinde ELLE tekrarlaniyordu. 18'i kosulsuz (D-1 karari'ni ihlal ederek),
  4'u hic. Yani kusur bir dikkatsizlik degil, bir KACAK URETICISI idi.

  Bunu hicbir kapi olcmuyordu: `faz0/altin_cikti.py`'nin OLCUM_KOMUTLARI'si
  yalnizca `["kapi"]` ve `["kapi","--siki"]`. `not` · `devral` · `bloklastir`
  ciktisi altin kumenin TAMAMEN DISINDA. Ortusen tespit korlugu degil — TAM
  KORLUK: o uc komutun ciktisini olcen sifir kapi vardi.

NE OLCER — IKI AYRI EKSEN, IKI AYRI KAPI
  KAPI-1 (YAPI, depo metni)   : `hafiza.py`'de ciplak `os.path.relpath(` yalniz
                                `kok_goreli` ve `_rel` govdelerinde gecebilir.
                                Yeni bir kacak DOGDUGU anda kirmizi yanar.
  KAPI-2 (DAVRANIS, birim)    : `_rel`'in kendisi dogru mu?
                                H-a  Windows'ta ters bolu DUZ boluye cevrilir
                                H-b  POSIX'te ters bolu KORUNUR (D-1: '\\' orada
                                     dosya adinin MESRU parcasidir, ayrac degil)
                                H-c  relpath patlarsa cokmez

  Iki kapi ZORUNLUDUR ve biri otekinin yerine GECMEZ:
  KAPI-1 tek basina, `_rel`'in govdesi bozulursa KOR kalir (metin hala "_rel"
  diyor). KAPI-2 tek basina, 23. cagri yerinde yine elle yazilirsa KOR kalir
  (birim testi o cagriyi hic gormez). Ucuncu bir kapi gerekmez ama bu ikisinin
  ORTUSMEDIGI mutantlarla asagida KANITLANIR.

NE OLCMEZ (hukum degil, SINIR)
  1. Ciktinin TAMAMINI olcmez. `_rel`'den gecmeyen, elle kurulan bir yol
     dizesini gormez. Onu ancak altin kumeye `not`/`devral`/`bloklastir`
     eklenirse olcebiliriz — o AYRI bir istir ve yapilmadi.
  2. Gercek Windows'u olcmez; `ntpath`/`posixpath` ile SIMULE eder. Gercek
     hukum CI'nin windows-latest islerinden gelir. Prob CI'nin yerine GECMEZ.

CIKIS KODLARI
  0  iki kapi da yesil VE uc mutantin ucu de ISIRDI
  1  kapi kirmizi, ya da bir mutant KACTI (kapi kor)
  2  olculemedi (dosya yok, sozdizimi okunamadi) — sessiz PASS verilmez
"""
import io
import ntpath
import os
import posixpath
import re
import sys

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")

# `os.path.relpath(` cagrisinin MESRU olarak gecebilecegi tek iki govde.
# MUAFIYET LISTESI DEGILDIR: kural fonksiyon ADIYLA tanimli, elle bakim istemez.
MESRU_GOVDELER = ("kok_goreli", "_rel")

_DEF = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)


def govde_haritasi(s):
    """her ust-seviye def icin (ad, baslangic, bitis) — kaba ama yeterli."""
    m = [(x.group(1), x.start()) for x in _DEF.finditer(s)]
    out = []
    for i, (ad, b) in enumerate(m):
        son = m[i + 1][1] if i + 1 < len(m) else len(s)
        out.append((ad, b, son))
    return out


def kapi1_yapi(s):
    """ciplak os.path.relpath yalniz MESRU_GOVDELER icinde mi?"""
    harita = govde_haritasi(s)
    kacaklar = []
    for mm in re.finditer(r"os\.path\.relpath\(", s):
        i = mm.start()
        sahip = None
        for ad, b, e in harita:
            if b <= i < e:
                sahip = ad
                break
        if sahip not in MESRU_GOVDELER:
            kacaklar.append((s.count("\n", 0, i) + 1, sahip or "<modul>"))
    return kacaklar


def rel_govdesi(s):
    """`_rel` fonksiyonunun KAYNAK METNINI dondurur (import YOK — yan etki yok)."""
    i = s.find("\ndef _rel(")
    if i < 0:
        raise LookupError("_rel bulunamadi")
    j = s.find("\ndef ", i + 1)
    return s[i + 1:j if j > 0 else len(s)]


class _SahteOs(object):
    """os yerine gecen ince kabuk: sep ve path.relpath disinda bir sey vermez."""

    def __init__(self, sep, modul):
        self.sep = sep
        self.path = modul


def rel_yukle(kaynak, sep, modul):
    """_rel'i YALIN bir ad alaninda kur; `os` yerine sahte kabugu ver."""
    ns = {"os": _SahteOs(sep, modul)}
    exec(compile(rel_govdesi(kaynak), "<_rel>", "exec"), ns)
    return ns["_rel"]


def kapi2_davranis(s):
    """H-a · H-b · H-c — her hal TEK bir seyi olcer."""
    bulgu = []
    try:
        win = rel_yukle(s, "\\", ntpath)
        pos = rel_yukle(s, "/", posixpath)
    except (LookupError, SyntaxError) as e:
        return [("H-*", "ÖLÇÜLEMEDİ: %s" % e)]

    # H-a  Windows: ayrac CEVRILIR
    g = win(r"C:\p\arsiv\hafiza\v2\_DEVIR.md", r"C:\p")
    if g != "arsiv/hafiza/v2/_DEVIR.md":
        bulgu.append(("H-a", "Windows'ta ayrac cevrilmedi: %r" % g))

    # H-b  POSIX: ters bolu DOSYA ADININ PARCASI, KORUNUR (D-1)
    g = pos("/p/garip\\ad.md", "/p")
    if g != "garip\\ad.md":
        bulgu.append(("H-b", "POSIX'te mesru '\\\\' bozuldu (D-1 ihlali): %r" % g))

    # H-c  relpath patlarsa cokme, ham degeri dondur
    class _Patlak(object):
        sep = "\\"

        class path(object):
            @staticmethod
            def relpath(a, b):
                raise ValueError("farkli surucu")
    try:
        ns = {"os": _Patlak}
        exec(compile(rel_govdesi(s), "<_rel>", "exec"), ns)
        g = ns["_rel"]("D:\\x", "C:\\y")
        if g != "D:\\x":
            bulgu.append(("H-c", "hata halinde ham deger donmedi: %r" % g))
    except Exception as e:                                   # noqa: BLE001
        bulgu.append(("H-c", "hata halinde COKTU: %s" % e))
    return bulgu


# --------------------------------------------------------------- MUTANTLAR
# UC AYRI EKSEN. Ikisi ayni kapiyi ates ederse ORTUSEN TESPIT KORLUGU olur ve
# bir eksen olculmemis kalir; asagida hangi mutantin hangi kapiyi atesledigi
# BEKLENTI olarak yazilidir ve TUTMAZSA kirmizi yanar.
def m1_yapi_geri_al(s):
    """bir `_rel(` cagrisini ciplak `os.path.relpath(` yapar -> KAPI-1 isirmali."""
    i = s.find("\ndef _rel(")
    j = s.find("\ndef ", i + 1)
    sonra = s[j:].replace("_rel(", "os.path.relpath(", 1)
    return (s[:j] + sonra) if "_rel(" in s[j:] else None


def m2_cevirmiyor(s):
    """_rel ARTIK CEVIRMIYOR -> KAPI-2 H-a isirmali (H-b'yi ATESLEMEZ)."""
    return s.replace(
        '    return r.replace("\\\\", "/") if os.sep == "\\\\" else r',
        '    return r', 1)


def m3_fazla_ceviriyor(s):
    """_rel KOSULSUZ ceviriyor -> KAPI-2 H-b isirmali (H-a'yi ATESLEMEZ).

    D-1 ekseni. m2 ile ortusmez: m2 'hic cevirmiyor', m3 'her yerde ceviriyor'."""
    return s.replace(
        '    return r.replace("\\\\", "/") if os.sep == "\\\\" else r',
        '    return r.replace("\\\\", "/")', 1)


MUTANTLAR = [
    ("M-1 yapi kacagi geri geldi", m1_yapi_geri_al, "KAPI-1"),
    ("M-2 _rel cevirmiyor", m2_cevirmiyor, "KAPI-2/H-a"),
    ("M-3 _rel kosulsuz ceviriyor (D-1)", m3_fazla_ceviriyor, "KAPI-2/H-b"),
]


def hukum(s):
    k1 = kapi1_yapi(s)
    k2 = kapi2_davranis(s)
    return k1, k2


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: ÖLÇÜLEMEDİ — motor okunamadi: %s" % e)
        return 2

    print("=== YOL AYRACI KAPISI === motor: %s" % os.path.basename(yol))
    k1, k2 = hukum(s)
    print("  KAPI-1 YAPI     : %s" % ("YESIL (ciplak relpath yok)" if not k1 else
                                      "KIRMIZI — %d kacak" % len(k1)))
    for satir, sahip in k1:
        print("      ! satir %d, `%s` icinde" % (satir, sahip))
    print("  KAPI-2 DAVRANIS : %s" % ("YESIL (H-a · H-b · H-c gecti)" if not k2 else
                                      "KIRMIZI — %d hal" % len(k2)))
    for hal, ne in k2:
        print("      ! %s: %s" % (hal, ne))
    if k1 or k2:
        print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
        return 1

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    for ad, boz, beklenen in MUTANTLAR:
        bozuk = boz(s)
        if bozuk is None or bozuk == s:
            print("  %-38s KURULAMADI (mutant uygulanamadi)" % ad)
            kacan += 1
            continue
        b1, b2 = hukum(bozuk)
        ates = []
        if b1:
            ates.append("KAPI-1")
        for hal, _ in b2:
            ates.append("KAPI-2/" + hal)
        if beklenen in ates and len(set(ates)) == 1:
            print("  %-38s -> ISIRDI ✓  (%s)" % (ad, beklenen))
        elif beklenen in ates:
            print("  %-38s -> ISIRDI ama ORTUSTU: %s" % (ad, " + ".join(sorted(set(ates)))))
            kacan += 1
        else:
            print("  %-38s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                  % (ad, beklenen, " + ".join(ates) or "hicbiri"))
            kacan += 1

    if kacan:
        print("\nSONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi." % (kacan, len(MUTANTLAR)))
        return 1
    print("\nSONUC: YESIL — iki kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

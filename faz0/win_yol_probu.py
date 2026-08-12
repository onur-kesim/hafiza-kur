#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WIN YOL PROBU — _RE_KOK_YOLU deseni WINDOWS AYIRICISINDA yetiyor mu?

NEYI OLCER
  Altin kumedeki 22 referans ciktinin HER BIRINI Windows'un basacagi hale
  geri cevirir (kok = 'C:\\...\\hk', kok ALTINDAKI ayiricilar TERS BOLU),
  sonra normalize() kosar ve sonucun referansla BIT-BIT ayni olmasini bekler.

NEYI OLCMEZ (hukum degil, SINIR)
  1. WINDOWS'UN GERCEK METNINI olcmez. Yalniz kumede BUGUN duran cumlelerin
     ayirici kanonlastirmasini olcer. Windows farkli bir HATA SINIFI basarsa
     (ornek: dizin_yap bozmasinin PermissionError yerine NotADirectoryError
     vermesi) bu prob onu GORMEZ. O yalnizca CI'da olculur.
  2. Ayni gerekce ile: mesaj METNI degisirse prob sessiz kalir.

ONGORU DOGRULANDI (12 Agu 2026, CI run #22, commit 7d8e8bb)
  Bu prob commit'ten ONCE "desen Windows ayiricisinda YETIYOR" dedi. Ayni
  commit'in CI kosumunda `altin_cikti` isi windows-latest'te `continue-on-error`
  OLMADAN kostu ve YESIL dondu — yani 22 olcumun tamami gercek Windows'ta
  bit-bit tuttu. Ongoru TUTTU.
  Ayrica probun KAPSAMI DISINDA biraktigi ikinci risk de ayni kosumda kapandi:
  h8_kesilme_dizin (dizin_yap bozmasi) Windows'ta FARKLI BIR HATA SINIFI
  uretmedi. Probun soyleyemedigi seyi CI soyledi — ikisi ayri sorulardir ve
  bu ayrim korunmalidir. Prob CI'nin yerine GECMEZ; onu erkene ceker.

SABOTAJ KOLU (doktrin 1: olcmeyen kapinin hukmu yoktur)
  Desen bilinen BOZUK haline (kacis fazlasi) cevrilir. Prob KACTI demeli;
  demiyorsa prob KORDUR ve yesili anlamsizdir.

CIKIS KODLARI
  0  temiz kol GECTI ve sabotaj kolu ISIRDI
  1  temiz kol KALDI (desen Windows ayiricisinda yetmiyor)
  2  sabotaj kolu KACTI (prob kor) -> yesil anlamsiz
  3  arac kusuru
"""
import json
import os
import re
import sys

KOK_WIN = "C:\\Users\\CI\\AppData\\Local\\Temp\\hk_deneme"
KOK_NIX = "/tmp/hk_deneme"

# Bekleyen surumdeki desen (TEMIZ) ve bilinen BOZUK hali.
DESEN_TEMIZ = r"<KOK>([\\/][^\s:;,'\"]*)"
DESEN_BOZUK = r"<KOK>([\\/][^\\s:;,'\"]*)"   # kacis FAZLA -> sinif "ters bolu + s"


def normalize_gibi(metin, kok, desen):
    """altin_cikti.normalize()'in yol ile ilgili KISMI, desen disaridan verilir.
    SHA/TARIH/GUN normalizasyonu bu probun konusu degildir; referans zaten
    normalize edilmis oldugu icin o desenler idempotenttir."""
    m = metin.replace(kok, "<KOK>")
    m = m.replace(kok.replace("/", "\\"), "<KOK>")
    m = re.compile(desen).sub(lambda x: "<KOK>" + x.group(1).replace("\\", "/"), m)
    return m


_RE_KOK_ALTI = re.compile(r"<KOK>((?:/[^\s:;,'\"]+)+)")


def geri_cevir(ref, kok, ayirici):
    """Referans metni, kok'u <ayirici> ile basan bir platformun ciktisina cevirir."""
    def _alt(m):
        return kok + m.group(1).replace("/", ayirici)
    m = _RE_KOK_ALTI.sub(_alt, ref)
    return m.replace("<KOK>", kok)


def kol(kume, kok, ayirici, desen):
    kalan = []
    for r in kume:
        ref = r.get("cikti") or ""
        uretilen = geri_cevir(ref, kok, ayirici)
        geri = normalize_gibi(uretilen, kok, desen)
        if geri != ref:
            kalan.append((r.get("hal"), r.get("komut"), ref, geri))
    return kalan


def ilk_fark(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return "...%s|  BEKLENEN=%r  GELEN=%r" % (a[max(0, i - 34):i], a[i:i + 24], b[i:i + 24])
    return "uzunluk farki: %d vs %d" % (len(a), len(b))


def main():
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "altin_kapi.json")
    try:
        kume = json.load(open(yol, encoding="utf-8"))["kume"]
    except Exception as e:
        print("ARAC KUSURU: altin_kapi.json okunamadi: %s" % e)
        return 3

    kok_alti = sum(1 for r in kume if _RE_KOK_ALTI.search(r.get("cikti") or ""))
    print("=" * 78)
    print("WIN YOL PROBU — _RE_KOK_YOLU Windows ayiricisinda yetiyor mu?")
    print("  kume            : %d olcum" % len(kume))
    print("  kok ALTI yol iceren olcum: %d  <- probun GERCEK kapsami" % kok_alti)
    print("=" * 78)
    if kok_alti == 0:
        print("OLCULEMEDI: kumede kok ALTINDA yol basan tek bir olcum bile yok.")
        print("  Desen bu kumede OLU KOD; prob hukum veremez.")
        return 3

    # --- KONTROL KOLU: Linux ayiricisi. Prob kendi kendini yanlislamamali. ---
    nix = kol(kume, KOK_NIX, "/", DESEN_TEMIZ)
    print("  KONTROL (linux '/')          : %s" % ("GECTI" if not nix else "KALDI %d" % len(nix)))
    if nix:
        print("  ARAC KUSURU: prob kendi kontrol kolunda kaldi -> hukum verilemez.")
        print("   ", ilk_fark(nix[0][2], nix[0][3]))
        return 3

    # --- TEMIZ KOL: Windows ayiricisi, bekleyen desen. ---
    win = kol(kume, KOK_WIN, "\\", DESEN_TEMIZ)
    print("  TEMIZ  (windows '\\\\')        : %s" % ("GECTI" if not win else "KALDI %d olcumde" % len(win)))
    for hal, komut, ref, geri in win[:4]:
        print("     %s %s -> %s" % (hal, komut, ilk_fark(ref, geri)))

    # --- SABOTAJ KOLU: bilinen bozuk desen. Prob ISIRMALI. ---
    sab = kol(kume, KOK_WIN, "\\", DESEN_BOZUK)
    isirdi = len(sab) > 0
    print("  SABOTAJ (bozuk desen)        : %s" % ("ISIRDI (%d olcumde fark)" % len(sab) if isirdi else "KACTI"))
    if isirdi:
        hal, komut, ref, geri = sab[0]
        print("     ornek: %s %s -> %s" % (hal, komut, ilk_fark(ref, geri)))

    print("-" * 78)
    if not isirdi:
        print("SONUC: SABOTAJ KACTI — prob KOR. Yesil hukum ANLAMSIZ.")
        return 2
    if win:
        print("SONUC: TEMIZ KOL KALDI — desen Windows ayiricisinda YETMIYOR.")
        return 1
    print("SONUC: desen Windows ayiricisinda YETIYOR (bu kumedeki cumleler icin).")
    print("  SINIR: Windows'un FARKLI BIR METIN/HATA SINIFI basmasi bu probun")
    print("  KAPSAMI DISINDADIR ve yalniz CI kosumunda olculur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

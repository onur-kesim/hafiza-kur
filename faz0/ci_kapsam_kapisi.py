#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI KAPSAM KAPISI — her MUTANT BETIGININ CI'da bir ISI VAR MI?

NEDEN VAR (olculdu 14 Agu 2026): uc ayri commit bir CI isini MESAJINDA beyan
etti, dosya commit'e girmedi ve kimse fark etmedi.

    c0478f0  "CI: h1_kenar_mutanti uc platformda"    -> capraz.yml commit'te YOK
    2550eba  CI isi beyan edildi                     -> capraz.yml commit'te YOK
    5b1e80f  "CI: h12_kenar_mutanti"                 -> capraz.yml commit'te YOK

Uc kez ayni sinif = YONTEM kusuru. "Daha dikkatli ol" bir kapi degildir.

Hedef ENGELLEMEK degil GIZLENEMEZ KILMAK: bu kapi, deponun kendi checkout'undaki
`.github/workflows/capraz.yml` dosyasini okur. Mutant betigi commit'e girip
workflow girmediginde, ESKI workflow kosar, bu kapi yeni betigi gorur, karsilik
gelen `run:` satirini bulamaz ve KIRMIZI yanar. Yani hatanin kendisi kapiyi
tetikler.

KAPSAM: `faz0/*_mutanti.py` — TUM mutant betikleri.

Olcut MUAFIYETSIZLIKTIR: muafiyet listesi bir BEYANDIR, bayatlar ve kimse
bakmaz. Kapsam ancak muafiyet DOGURMADIGI surece genisletilir.

  · 14 Agu 2026, ilk surum: kapsam `*_bolme_mutanti.py` (7 dosya, 0 muafiyet).
    Daha genis bir kural ("faz0'daki tum olcum betikleri") IKI muafiyet
    dogurdugu icin (sabotaj.py, win_yol_probu.py) BILEREK secilmedi.
  · Ayni gun genisletildi: `*_mutanti.py`. OLCULDU — 13 dosyanin 13'u zaten CI
    isi tasiyor, yani muafiyet YINE DOGMUYOR. Genisleme bedava.
    Tetikleyen olay: `cmd_etki_mutanti.py` dar kapsamin DISINDA kaldi ve isi
    elle eklendi; kapi bunu goremezdi.

Kapsami bir daha genisletmek istersen olcut aynidir: once say, muafiyet
doguyorsa GENISLETME.

BOS KUME = OLCULEMEDI, YESIL DEGIL. Hicbir `*_mutanti.py` bulunmazsa kapi
exit 2 verir. Bir sey olcmeyen kapi "temiz" diyemez (doktrin 2).

CIKIS KODU  0 hepsinin isi VAR · 1 en az birinin isi YOK (KIRMIZI) · 2 OLCULEMEDI
"""
import argparse
import os
import re
import sys


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN_KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(".github", "workflows", "capraz.yml")
DESEN = re.compile(r".*_mutanti\.py$")
CIZGI = "-" * 78


def mutant_betikleri(kok):
    d = os.path.join(kok, "faz0")
    if not os.path.isdir(d):
        return None
    return sorted(f for f in os.listdir(d) if DESEN.match(f))


def calisan_satirlar(metin):
    """YORUM SATIRLARI SAYILMAZ. Bir dosya adinin yorumda gecmesi, o isin
    kostugunu KANITLAMAZ — bu projede beyan ile gercek tam olarak burada ayrilir."""
    return [s for s in metin.split("\n") if s.lstrip()[:1] != "#"]


def olc(kok):
    betikler = mutant_betikleri(kok)
    if betikler is None:
        return 2, "faz0/ dizini yok: %s" % kok, []
    wf = os.path.join(kok, WORKFLOW)
    if not os.path.isfile(wf):
        return 2, "workflow dosyasi yok: %s" % WORKFLOW, []
    try:
        with open(wf, encoding="utf-8", errors="replace") as f:
            metin = f.read()
    except OSError as e:
        return 2, "workflow okunamadi: %s" % e, []
    if not betikler:
        return 2, "hicbir faz0/*_mutanti.py bulunamadi — bu kapi HICBIR SEY olcmuyor", []

    govde = "\n".join(calisan_satirlar(metin))
    sonuc = [(b, ("faz0/" + b) in govde) for b in betikler]
    kacan = [b for b, var in sonuc if not var]
    return (1 if kacan else 0), "", sonuc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kok", default=VARSAYILAN_KOK)
    a = ap.parse_args()
    kok = os.path.abspath(a.kok)

    print(CIZGI)
    print("CI KAPSAM KAPISI — faz0/*_mutanti.py -> capraz.yml isi")
    print("kok: %s" % kok)
    print(CIZGI)

    # HUKMU `olc()` VERIR, `main()` yalnizca BASAR.
    # 14 Agu 2026: ilk surumde `main()` hukmu `sonuc`tan YENIDEN hesapliyordu ve
    # `olc()`in dondurdugu kod 0/1 ayriminda hic kullanilmiyordu. Kapinin kendi
    # mutanti (M-3) bunu ILK KOSUMDA yakaladi: `olc()`teki kodu bozmak hicbir
    # seyi degistirmiyordu, cunku o kod OLU'ydu. Hukmu tek yerde tut.
    kod, sebep, sonuc = olc(kok)
    if kod == 2:
        print("OLCULEMEDI: %s" % sebep)
        return kod
    for b, var in sonuc:
        print("  %s  %-28s %s" % ("+" if var else "!", b, "CI isi VAR" if var else "CI ISI YOK"))
    print(CIZGI)
    if kod == 1:
        kacan = [b for b, var in sonuc if not var]
        print("HUKUM: KIRMIZI — %d mutant betiginin CI isi YOK: %s"
              % (len(kacan), ", ".join(kacan)))
        print("  Betik depoda ama hic kosmuyor. `.github/workflows/capraz.yml`'e")
        print("  `run: python faz0/<ad>` tasiyan bir is ekle.")
        return kod
    print("HUKUM: %d mutant betiginin hepsinin CI isi VAR." % len(sonuc))
    return kod


if __name__ == "__main__":
    sys.exit(main())

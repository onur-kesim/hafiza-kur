#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — DURMA HUKMU AYRIMI MUTANTI (bir kapi + iki mutant) — BITTI md.8.

NEDEN VAR (olculdu 16 Agu 2026, 72 gercek public depo, salt okuma)
  `devral` `canli` bulamadigi icin durdugunda, HUKUM METNI iki tamamen farkli
  hali AYIRT ETMIYORDU:
    · flask       -> kokte hicbir hafiza adayi YOK           (envanter bos)
    · BookSwap    -> `memory-bank/` alti dosya TANINDI ama
                     hicbiri `canli` rolunde degil            (envanter dolu)
  Durma blogunun sha'si DORT ayri agacta (flask · BookSwap · axios ·
  hafiza-kur) BIREBIR AYNIYDI. Yani arac BILDIGI seyi hukmune koymuyordu:
  envanteri yukarida basiyor, sonra "TANINAN dosya YOK" diyordu. Kullanici
  bunu "aracim hafizami bulamadi" diye okur — oysa buldu, `canli` saymadi.
  Ayrica ayni mesajdaki 2. oneri ("Gercekten YENI defter ac") tam da CIFT
  DEFTERI onlemek icin durmus bir araca ikinci defteri actiriyordu.
  ⇒ md.8: hukum, envanterin BOS olup olmadigini AYIRT EDER. ADDITIVE — cikis
  kodu, durma kosulu ve md.7'nin coklu-`canli` kolu DEGISMEZ.

  🔴 POPULASYON NOTU: 22/22 `memory-bank/` deposunda `canli` YOKTUR
  (`MEMORY-BANK/*` -> `disarida`). Yani bu hal UC DURUM DEGIL, sektorun en
  yaygin hafiza konvansiyonunda VARSAYILAN haldir.

NE OLCER — TEK KAPI (kilit: "yalniz hukum ayrimi", Onur 16 Agu 2026)
  KAPI-1 (AYRIM) — iki senaryo, tek eksen
      S-BOS  : kokte yalniz `README.md` (hicbir rol atanmaz)
      S-DOLU : `memory-bank/` + alti dosya (alti `disarida` atamasi)
      Ikisinde de YAZAN kosum DURUR (cikis != 0, diske sifir bayt) ve iki
      durma blogu BIREBIR AYNI OLAMAZ. Ayniysa KIRMIZI.
      Karsilastirma yol-normalize edilir (kok yolu maskelenir), yoksa iki
      farkli dizin adi sahte bir "fark" uretir ve kapi KOR olur.

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. Hukum METNININ dogrulugu olculmez — yalniz AYRISTIGI olculur. "6 dosya"
     yerine "N dosya" yazsa bu kapi yesil kalir; sayinin dogrulugu ayri bir
     eksendir ve bu turda ACILMADI (kilit: tek eksen).
  2. Oneri SIRALAMASI ("YENI defter ac" tanninan dosya varken ilk sirada)
     bu turda KAPSAM DISI — ayri madde adayidir, kayda gecti.
  3. md.7'nin coklu-`canli` kolu bu kapinin ekseni degil; asagida OLCUM
     olarak basilir, KAPI olarak degil (hukum vermez).

CIKIS KODLARI
  0  kapi temiz VE 2/2 mutant ISIRDI
  1  kapi kirmizi ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi, git yok) — sessiz PASS yok
"""
import hashlib
import io
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
            pass


VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")

MB_DOSYALARI = ("activeContext.md", "productContext.md", "progress.md",
                "projectbrief.md", "systemPatterns.md", "techContext.md")


def _git_var():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except OSError:
        return False


def kur_senaryo(taban, ad, mb):
    """S-BOS ve S-DOLU. Ikisi de ayni `README.md`yi tasir: tek DEGISKEN
    `memory-bank/` dizinidir, boylece fark BASKA bir seyden gelemez."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with io.open(os.path.join(kok, "README.md"), "w", encoding="utf-8") as f:
        f.write("# proje\n")
    if mb:
        d = os.path.join(kok, "memory-bank")
        os.makedirs(d)
        for x in MB_DOSYALARI:
            with io.open(os.path.join(d, x), "w", encoding="utf-8") as f:
                f.write("# %s\n" % x)
    return kok


def kos(motor, kok, *ek):
    """stdout ve stderr AYRI yakalanir — BIRLESTIRILMEZ.

    🔴 OLCULDU (CI #61 ve #62, uc platformda birden; yerelde ASLA):
    `stderr=subprocess.STDOUT` ile birlestirmek bu kapiyi KOR EDIYORDU.
    Motor hukmu `oldur()` ile STDERR'e yazar (tamponsuz), envanteri
    `print()` ile STDOUT'a (boru arkasinda BLOK TAMPONLU). Boru arkasinda
    stderr ONCE bosalir, yani HATA blogunun ARDINA envanter satirlari duser.
    `cikti[find("HATA:"):]` o zaman envanteri de yutar — ve envanter
    senaryoya gore FARKLIDIR (s_bos 0 satir, s_dolu 6 `disarida` satiri).
    Sonuc: iki blok HEP farkli, mutantlar HEP kacar, kapi HEP yesil gorunur.
    Yerelde tampon sirasi tersti; kapi bu yuzden UC KEZ yesil dedi.
    Akislari ayirmak sinifi kokten kapatir: hukum yalniz stderr'den okunur.
    """
    p = subprocess.run([sys.executable, motor, "devral", "--kok=" + kok] + list(ek),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def durma_blogu(cikti, kok):
    """Hukum blogu = ilk `HATA:` satirindan sonu. Yol MASKELENIR.

    🔴 OLCULDU — CI #61 bu kapiyi KOR YAKALADI (uc platformda birden):
    yolu `kok` ile ESITLIK uzerinden maskelemek KIRILGANDIR. Motor `--kok`
    argumanina `os.path.abspath` uygular; bastigi yol gonderdigimden BIR
    KARAKTER farkli olabilir (kosucuda oldu, yerelde olmadi). O zaman
    maskeleme SESSIZCE basarisiz olur, iki senaryonun bloklari senaryo adi
    yuzunden HEP farkli kalir, karsilastirma HEP "ayri hukum" der ve kapi
    HEP YESIL gorunur — yani hicbir sey olcmez. Kanit: `--kok`a `/./`
    eklenince maskeleme tuttu mu = False, mutantlar KACTI.
    Artik yol ICERIGINE bakilmadan DESENLE silinir; ayrica maskelemenin
    gerceklestigi CAGIRAN tarafindan DOGRULANIR (`<KOK>` yoksa OLCULEMEDI).
    """
    i = cikti.find("HATA:")
    if i < 0:
        return None
    blok = cikti[i:]
    blok = re.sub(r'--kok="[^"]*"', '--kok="<KOK>"', blok)
    blok = blok.replace(kok, "<KOK>").replace(kok.replace(os.sep, "/"), "<KOK>")
    return re.sub(r"\s+", " ", blok).strip()


def diske_yazildi_mi(kok):
    for x in (".hafizarc", "PROJE_HAFIZA.md", "arsiv"):
        if os.path.exists(os.path.join(kok, x)):
            return x
    return None


def kapi_1(motor, taban):
    """AYRIM: envanteri BOS ve DOLU agac ayni hukmu basamaz."""
    b = []
    bloklar = {}
    for ad, mb in (("s_bos", False), ("s_dolu", True)):
        kok = kur_senaryo(taban, ad, mb)
        kod, _std, hata = kos(motor, kok)
        if kod == 0:
            b.append("%s: cikis 0 — durma kurali hic ateslenmedi" % ad)
            continue
        yazildi = diske_yazildi_mi(kok)
        if yazildi:
            b.append("%s: DURDU ama diske yazdi (%s)" % (ad, yazildi))
        blok = durma_blogu(hata, kok)
        if blok is None:
            b.append("%s: cikis %d ama `HATA:` blogu YOK" % (ad, kod))
        elif "taranan yuzey" in blok:
            # Hukum blogu ENVANTER satiri tasiyorsa akislar karismis demektir
            # (CI #61/#62'nin kok nedeni). Karsilastirma guvenilmez => KIRMIZI.
            b.append("%s: hukum blogu ENVANTER satiri tasiyor — akislar "
                     "karismis, karsilastirma guvenilmez" % ad)
            blok = None
        elif "<KOK>" not in blok:
            # Maskeleme tutmadiysa karsilastirma GUVENILMEZ. Sessizce "ayri
            # hukum" demek, kapiyi KOR birakmaktir (CI #61'in tam kusuru).
            b.append("%s: yol MASKELENEMEDI — karsilastirma guvenilmez, "
                     "kapi kor kalirdi" % ad)
            blok = None
        bloklar[ad] = blok
    if len(bloklar) == 2 and None not in bloklar.values():
        h = dict((k, hashlib.sha256(v.encode("utf-8")).hexdigest()[:8])
                 for k, v in bloklar.items())
        sys.stdout.write("      imza: s_bos %s · s_dolu %s\n"
                         % (h["s_bos"], h["s_dolu"]))
        if bloklar["s_bos"] == bloklar["s_dolu"]:
            b.append("AYRIM YOK — envanteri BOS ve DOLU agac BIREBIR AYNI "
                     "hukmu basiyor (md.8 kusuru)")
    return b


def hukum(motor, taban):
    return (kapi_1(motor, taban),)


# --------------------------------------------------------------- MUTANTLAR
# Iki mutant da AYNI kapiyi (KAPI-1) isirir; bu bilincli: kilit "tek eksen"
# dedi. Iki AYRI sabotaj kullanilir cunku tek sabotaj, kapinin yalnizca o
# sabotaji gormesi ihtimalini disarida birakmaz.
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n"
                         % (n, hedef[:60]))
        return False
    return True


def m1_ayrim_satiri_mesajdan_silinir(s):
    """Hukum metnindeki `  %s\\n` satiri kaldirilir = md.8 ONCESI hal.

    Bu, kusurun TA KENDISIDIR: iki hal ayni hukmu basar."""
    hedef = ('oldur("DEVIR DURDU — bu agacta `canli` rolunu ustlenen '
             'TANINAN dosya YOK.\\n"\n              "  %s\\n"\n')
    yeni = ('oldur("DEVIR DURDU — bu agacta `canli` rolunu ustlenen '
            'TANINAN dosya YOK.\\n"\n              "%.0s"\n')
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m2_ayrim_sabit_metne_cevrilir(s):
    """`_md8_ayrim` her iki dalda da AYNI sabit cumleye baglanir.

    Satir basilmaya devam eder ama BILGI TASIMAZ; kapi yine ISIRMALIDIR —
    "bir sey yazdim" ile "AYIRT ETTIM" ayni sey degildir."""
    hedef = '    _md8_ayrim = ("HIC dosya TANINMADI'
    yeni = ('    _md8_ayrim = "envanter yukarida."  # MUTANT: sabit\n'
            '    _yut = ("HIC dosya TANINMADI')
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


MUTANTLAR = [
    ("M-1 ayrim satiri mesajdan silinir", m1_ayrim_satiri_mesajdan_silinir, "KAPI-1"),
    ("M-2 ayrim sabit metne cevrilir", m2_ayrim_sabit_metne_cevrilir, "KAPI-1"),
]


def olcum_md7_kolu(motor, taban):
    """OLCUM (KAPI DEGIL): md.7'nin coklu-`canli` kolu bu degisiklikten
    etkilenmemeli. Hukum vermez — yalniz basar; hukum md.7'nin kendi
    aracinindir (`ayrisma_mutanti.py`) ve ORTUSME uretmemek icin buraya
    kapi olarak KONMAZ."""
    kok = os.path.join(taban, "olcum_coklu")
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for x in ("MEMORY.md", "PROJE_HAFIZA.md"):
        with io.open(os.path.join(kok, x), "w", encoding="utf-8") as f:
            f.write("x\n")
    kod, _std, hata = kos(motor, kok)
    coklu = "TANINAN 2 dosya var" in hata
    return kod, coklu


def main():
    _cikti_kodlamasini_guvenceye_al()
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    yol = os.path.abspath(yol)
    print("=== DURMA HUKMU AYRIMI MUTANTI === motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    if not _git_var():
        print("SONUC: ÖLÇÜLEMEDİ — `git` yok; senaryolar git'li agac ister.")
        return 2
    try:
        kaynak = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: ÖLÇÜLEMEDİ — motor okunamadi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="md8_temiz_")
    try:
        (b1,) = hukum(yol, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)
    if b1:
        print("  KAPI-1 AYRIM    : KIRMIZI")
        for x in b1:
            print("      - %s" % x)
    else:
        print("  KAPI-1 AYRIM    : YESIL (BOS ve DOLU envanter ayri hukum)")

    taban = tempfile.mkdtemp(prefix="md8_olcum_")
    try:
        kod7, coklu7 = olcum_md7_kolu(yol, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)
    print("  OLCUM md.7 kolu : cikis %d · kendi mesaji %s (KAPI DEGIL)"
          % (kod7, "VAR" if coklu7 else "YOK"))

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    olculemeyen = 0
    for ad, fn, kapi in MUTANTLAR:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  %-36s -> ÖLÇÜLEMEDİ (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        d = tempfile.mkdtemp(prefix="md8_mut_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            t2 = os.path.join(d, "senaryolar")
            os.makedirs(t2)
            (bm,) = hukum(sahte, t2)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if bm:
            print("  %-36s -> ISIRDI ✓  (%s)" % (ad, kapi))
        else:
            print("  %-36s -> KAÇTI ✗  (%s KOR)" % (ad, kapi))
            kacan += 1

    if olculemeyen:
        print("\nSONUC: ÖLÇÜLEMEDİ — %d mutant kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    if b1 or kacan:
        print("\nSONUC: KIRMIZI — kapi %s · kacan mutant %d"
              % ("KIRMIZI" if b1 else "temiz", kacan))
        return 1
    print("\nSONUC: YESIL — KAPI-1 temiz, %d/%d mutant ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

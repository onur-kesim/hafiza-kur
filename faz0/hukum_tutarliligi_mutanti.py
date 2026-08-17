#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — HUKUM IC TUTARLILIGI MUTANTI (bir kapi + iki mutant) — BITTI md.10.

NEDEN VAR (kaynak: md10-BRIEF.md, 17 Agu 2026, yedi gercek/sentetik agac + bir
kenar hali, salt okuma, cikis 2 / diske sifir bayt): durma hukmunun AYRIM
CUMLESI (`devir_durma_govdesi`, hal-2 dali) kapsam disi (`disarida`) dosyalari
"biri projenin gercek defteri OLABILIR" iddiasinin SAYISINA ve ROL LISTESINE
katiyordu — `%d` = `len(envanter)` (= ici + disi), rol listesi
`set(e[1] for e in envanter)`. Ekranda "7 dosya … (disarida, gunluk)" yazarken
aday olan sadece 1'di.

Bu GORUNURLUK kusuru DEGIL — md.9 gorunurlugu kapatti (sayi yazilir, ad
komutta). Bu bir HUKUM IC TUTARLILIGI kusuru: AYNI ekranda motor kendisiyle
CELISIYORDU — hal-3'te (hepsi disarida) "hicbiri onerilmez" derken, hal-2'de
disarida dosyalari "biri OLABILIR" kumesine katiyordu. Alt satirdaki kirpma
notu (md.9-c) kullaniciyi ARITMETIKLE kurtariyordu — bu bir hukum degil,
kullanicidan beklenen bir CIKARIM.

🔴 md.9 KAPISI (`gorunurluk_mutanti.py`) BU KUSURA KORDU — OLCULDU: iki motora
da (md.9 ONCESI ve md.10 ONCESI) BIT BIT AYNI cikti verdi (4/4 kapi temiz, 5/5
mutant isirdi). Sebep: KAPI-3 KAPSAM "gercek defteri OLABILIR" cumlesini
YALNIZ `s_disi` (0 kapsam ici) senaryosunda yasakliyor, karma agacta hic
bakmiyor; KAPI-4 KIRPMA yalniz kirpma notunun VARLIGINI olcuyor
(`"6" in blok and "listelenmedi" in blok`), ayrim cumlesinin SAYISINA
bakmiyor. ⇒ bu yeni kapi md.9 ile ORTUSMUYOR (orstusen tespit korlugu riski
yok); md.9'un kendi kapisi ayrica DOKUNULMADI (ADDITIVE, olculdu).

NE OLCER — TEK KAPI, IKI AYRI BULGU DIZESI (kilit: "yalniz ayrim sayisi/rolu",
Onur 17 Agu 2026)
  KAPI-1 AYRIM SAYISI — iki senaryo (tek senaryoda SABIT bir sayi yazan
  mutant kacabilirdi):
      s_karma_1 : kok `DURUM.md` + `memory-bank/` 6 dosya -> 1 ici / 6 disi
      s_karma_2 : kok `CLAUDE.md`+`DURUM.md` + `memory-bank/` 5 dosya
                  -> 2 ici / 5 disi
  Ayrim satiri DESENLE cekilir: `AMA (\\d+) dosya BASKA rollerde TANINDI
  \\(([^)]*)\\)`. Her senaryoda:
    bulgu (a) — yakalanan sayi != kapsam ICI sayisi
                ("ayrim sayisi KAPSAM DISI'yi da sayiyor")
    bulgu (b) — yakalanan rol listesinde `disarida` GECIYOR
                ("ayrim cumlesinin rol listesinde disarida GECIYOR")
  Desen HIC eslesmezse -> OLCULEMEDI (hal-2'ye hic girilmemis demektir,
  senaryo bozulmustur; sessiz PASS yok).

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. Kirpma notunu (md.9-c: "N dosya KAPSAM DISI … listelenmedi") BU KAPI
     OLCMEZ — o `gorunurluk_mutanti.py` KAPI-4'un isidir. Ayni seyi iki kapi
     olcerse mutant ikisini de olcuyor sanilir, oysa birini hic olcmuyor
     olabilir (kilit: tek eksen).
  2. Hal-1 ve hal-3 govde metninin BIREBIR korundugu bu kapinin ekseni degil
     (md.9'un ekseni); bu turda AYRICA olculmedi, yalniz gozle dogrulandi.
  3. `s_karma_2` senaryosunun kapi DISINDA motorla dogrulanmasi (md10-BRIEF
     §10) bu dosyayla KAPANDI — artik kapinin ICINDE kosuyor.

CIKIS KODLARI
  0  kapi temiz VE 2/2 mutant ISIRDI (her biri KENDI bulgusunu)
  1  kapi kirmizi ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi, git yok, desen
     eslesmedi) — sessiz PASS yok
"""
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

MB_ALTI = ("activeContext.md", "productContext.md", "progress.md",
           "projectbrief.md", "systemPatterns.md", "techContext.md")

AYRIM_DESENI = re.compile(r"AMA (\d+) dosya BASKA rollerde TANINDI \(([^)]*)\)")


def _git_var():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except OSError:
        return False


def kur_senaryo(taban, ad, durum=False, claude=False, mb_sayisi=0):
    """s_karma_1 / s_karma_2 — TEK DEGISKEN: kapsam ici/disi karisimi. Hepsi
    ayni README.md'yi tasir, boylece fark BASKA bir seyden gelemez."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with io.open(os.path.join(kok, "README.md"), "w", encoding="utf-8") as f:
        f.write("# proje\n")
    if durum:
        with io.open(os.path.join(kok, "DURUM.md"), "w", encoding="utf-8") as f:
            f.write("# durum\n")
    if claude:
        with io.open(os.path.join(kok, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write("# claude\n")
    if mb_sayisi:
        d = os.path.join(kok, "memory-bank")
        os.makedirs(d)
        for x in MB_ALTI[:mb_sayisi]:
            with io.open(os.path.join(d, x), "w", encoding="utf-8") as f:
                f.write("# %s\n" % x)
    return kok


def kos(motor, kok):
    """stdout ve stderr AYRI yakalanir — BIRLESTIRILMEZ (md.8 kapisini kor
    eden sinif, CI #61/#62). Boru YOK; cikis kodu dogrudan `p.returncode`den
    okunur (`| tail` sonrasi `$?` boruyu olcer kusuru burada olusamaz)."""
    p = subprocess.run([sys.executable, motor, "devral", "--kok=" + kok],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def durma_blogu(hata, kok):
    """Hukum blogu = ilk `HATA:` satirindan sonu. Yol DESENLE maskelenir
    (esitlik degil — esitlik tabanli maskeleme sessizce basarisiz olabilir,
    md.8'in bedeli odenmis dersi)."""
    i = hata.find("HATA:")
    if i < 0:
        return None
    blok = hata[i:]
    blok = re.sub(r'--kok="[^"]*"', '--kok="<KOK>"', blok)
    return blok.replace(kok, "<KOK>").replace(kok.replace(os.sep, "/"), "<KOK>")


def diske_yazildi_mi(kok):
    for x in (".hafizarc", "PROJE_HAFIZA.md", "arsiv"):
        if os.path.exists(os.path.join(kok, x)):
            return x
    return None


def _senaryo_olc(motor, taban, ad, beklenen_ici, **kur_kw):
    """Bir senaryoyu kosar, ayrim desenini cikarir. Donen:
    (kirmizi_bulgular, olculemedi_notlari) — ikisi de liste."""
    kirmizi, olculemedi = [], []
    kok = kur_senaryo(taban, ad, **kur_kw)
    kod, _std, hata = kos(motor, kok)
    if kod == 0:
        olculemedi.append("%s: cikis 0 — durma kurali hic ateslenmedi" % ad)
        return kirmizi, olculemedi
    yazildi = diske_yazildi_mi(kok)
    if yazildi:
        olculemedi.append("%s: DURDU ama diske yazdi (%s)" % (ad, yazildi))
    blok = durma_blogu(hata, kok)
    if blok is None:
        olculemedi.append("%s: cikis %d ama `HATA:` blogu YOK" % (ad, kod))
        return kirmizi, olculemedi
    if "<KOK>" not in blok:
        olculemedi.append("%s: yol MASKELENEMEDI — karsilastirma guvenilmez" % ad)
        return kirmizi, olculemedi
    m = AYRIM_DESENI.search(blok)
    if not m:
        olculemedi.append("%s: ayrim deseni HIC ESLESMEDI — hal-2'ye "
                          "girilmemis demektir, senaryo bozulmus" % ad)
        return kirmizi, olculemedi
    sayi, roller = int(m.group(1)), m.group(2)
    if sayi != beklenen_ici:
        kirmizi.append("%s: ayrim sayisi KAPSAM DISI'yi da sayiyor (%d, "
                       "beklenen %d)" % (ad, sayi, beklenen_ici))
    if "disarida" in roller:
        kirmizi.append("%s: ayrim cumlesinin rol listesinde `disarida` "
                       "GECIYOR (%r)" % (ad, roller))
    return kirmizi, olculemedi


def kapi_1_ayrim_sayisi(motor, taban):
    """AYRIM SAYISI: iki karma senaryo, her biri kendi bulgu cifti."""
    kirmizi, olculemedi = [], []
    for ad, beklenen_ici, kw in (
        ("s_karma_1", 1, {"durum": True, "mb_sayisi": 6}),
        ("s_karma_2", 2, {"durum": True, "claude": True, "mb_sayisi": 5}),
    ):
        k, o = _senaryo_olc(motor, taban, ad, beklenen_ici, **kw)
        kirmizi += k
        olculemedi += o
    return kirmizi, olculemedi


# --------------------------------------------------------------- MUTANTLAR
# Motorun KAYNAGINDA str.replace; her biri `_tek_yerde` ile doGrulanir.
# HER DUZELTMEYE AYRI MUTANT: M-a yalniz SAYI hesabini bozar (`len(ici)` ->
# `len(envanter)`), M-b yalniz ROL listesini bozar (`for e in ici` ->
# `for e in envanter`, join icinde). Biri digerinin bulgusunu da yakarsa
# kapi o ekseni AYRI OLCMUYOR demektir (esdeger mutant != korluk dersi).
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n"
                         % (n, hedef[:70]))
        return False
    return True


def m_a_sayi_bulasmasi(s):
    """M-a: `% (len(ici),` -> `% (len(envanter),` — sayi hesabi kapsam
    disini da sayar hale doner (md.10 ONCESI halin ta kendisi, sayi ekseni).
    bulgu (a)'yi isirmali, (b)'yi ISIRMAMALI (ROL listesine dokunmuyor)."""
    hedef = "                  % (len(ici),\n"
    yeni = "                  % (len(envanter),\n"
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m_b_rol_bulasmasi(s):
    """M-b: rol-listesi join'i `for e in ici` -> `for e in envanter` —
    kapsam disi rolleri (`disarida`) rol listesine geri katar (rol ekseni).
    bulgu (b)'yi isirmali, (a)'yi ISIRMAMALI (SAYI hesabina dokunmuyor)."""
    hedef = '                     ", ".join(sorted(set(e[1] for e in ici))))\n'
    yeni = '                     ", ".join(sorted(set(e[1] for e in envanter))))\n'
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


MUTANTLAR = [
    ("M-a sayi bulasmasi", m_a_sayi_bulasmasi, "bulgu (a) sayi"),
    ("M-b rol bulasmasi", m_b_rol_bulasmasi, "bulgu (b) rol"),
]


def main():
    _cikti_kodlamasini_guvenceye_al()
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    yol = os.path.abspath(yol)
    print("=== HUKUM IC TUTARLILIGI MUTANTI (1 kapi + 2 mutant) === motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    if not _git_var():
        print("SONUC: OLCULEMEDI — `git` yok; senaryolar git'li agac ister.")
        return 2
    try:
        kaynak = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="md10_temiz_")
    try:
        kirmizi, olculemedi = kapi_1_ayrim_sayisi(yol, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    if olculemedi:
        print("  KAPI-1 AYRIM SAYISI: OLCULEMEDI")
        for x in olculemedi:
            print("      - %s" % x)
        print("\nSONUC: OLCULEMEDI — kapinin kendi olcumu guvenilmez; "
              "sessiz PASS verilmez.")
        return 2
    if kirmizi:
        print("  KAPI-1 AYRIM SAYISI: KIRMIZI")
        for x in kirmizi:
            print("      - %s" % x)
    else:
        print("  KAPI-1 AYRIM SAYISI: YESIL (sayi/rol yalniz kapsam ICI'yi sayiyor)")

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    olculemeyen = 0
    for ad, fn, beklenen_bulgu in MUTANTLAR:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  %-24s -> OLCULEMEDI (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        d = tempfile.mkdtemp(prefix="md10_mut_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            t2 = os.path.join(d, "senaryolar")
            os.makedirs(t2)
            k_mut, o_mut = kapi_1_ayrim_sayisi(sahte, t2)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if o_mut:
            print("  %-24s -> OLCULEMEDI (mutantli kosum guvenilmez: %s)"
                  % (ad, o_mut[0]))
            olculemeyen += 1
            continue
        # Hangi eksenin yandigini AYRICA olc (harness "kirmizi yandi" ile
        # yetinmez, HANGI bulgunun yandigina bakar).
        yandi_sayi = any("ayrim sayisi" in b for b in k_mut)
        yandi_rol = any("rol listesinde" in b for b in k_mut)
        eksen = ("sayi" in beklenen_bulgu and yandi_sayi and not yandi_rol) or \
                ("rol" in beklenen_bulgu and yandi_rol and not yandi_sayi)
        if eksen:
            print("  %-24s -> ISIRDI (%s, TEK EKSEN — digeri temiz kaldi)"
                  % (ad, beklenen_bulgu))
        elif k_mut:
            print("  %-24s -> ISIRDI ama YANLIS EKSEN/FAZLA (beklenen: %s, "
                  "bulgular: %s)" % (ad, beklenen_bulgu, k_mut))
            kacan += 1
        else:
            print("  %-24s -> KACTI ✗ (beklenen %s KOR)" % (ad, beklenen_bulgu))
            kacan += 1

    if olculemeyen:
        print("\nSONUC: OLCULEMEDI — %d mutant/kosum guvenilmez; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    if kirmizi or kacan:
        print("\nSONUC: KIRMIZI — kapi %s · kacan/yanlis-eksen mutant %d"
              % ("KIRMIZI" if kirmizi else "temiz", kacan))
        return 1
    print("\nSONUC: YESIL — 1/1 kapi temiz, %d/%d mutant ISIRDI (her biri KENDI ekseninde)."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

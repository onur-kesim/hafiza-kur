#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B6 SATIR SAYISI MUTANTI (SIK β) — `_ilk_satir_isaretli`, cok satirli
`oldur()` mesajlarinda kayip satirlarin VARLIGINI hukumde isaretliyor mu?
(kalem5-tarama/IS_EMRI_B6_BETA.md, Onur kilidi 4 Eylul 2026)

NEDEN VAR (kalem5-tarama/OLCUM_RAPORU_B6.md, 4 Eylul 2026 — ISIRDI)
  `kapi_yalit()`nin OLCULEMEDI hukmu, `oldur()`un yazdigi TAM mesaji
  `.split("\n")[0]` ile hukum kanalinda (stdout, `O` listesi) TEK SATIRA
  dusuruyordu. OLCULDU: H8/UTF-8 vakasinda 4 satirlik/259 karakterlik bir
  mesajin 3 satiri (%81'i) — TANI ve COZUM — hukme HIC ULASMIYORDU; ne
  artefaktta, ne stdout borusunda, HICBIR YERDE gorunmuyordu (stderr
  DEVNULL'landiginda da ayni). Kaybolan yolun kuyrugu degil, COZUMUN
  KENDISIYDI.

  Duzeltme (SIK β — DOKTRININ "engellemek degil, gizlenemez kilmak"
  maddesine en yakin olan): `_ilk_satir_isaretli` cok satirli mesajlarda
  ilk satirin ardina "(+N satir: stderr)" ISARETI ekler. Kayip
  ENGELLENMEZ — hukum satiri hala TEK SATIRDIR, mesaj hala kirpilir —
  ama kaybin VARLIGI artik GIZLENEMEZ.

  🔴 EKSEN SATIR SAYISIDIR, YOL UZUNLUGU DEGIL: `yol_uzunlugu_mutanti.py`nin
  `--uzun-yol` kolu bu sinifi YAPISAL OLARAK GOREMEZ — yol uzunlugu mesajin
  SATIR SAYISINI degistirmez. Bu yuzden bu mutant AYRIDIR, o kola
  BAGLANMAZ, kendi CI adimini tasir.

  🔴 GUNCELLEME (5 Eylul 2026, Onur kilidi SIK A —
  kalem5-tarama/IS_EMRI_H9_STDERR_ISARET.md): `_kapi_h9`nin "git deposu
  OKUNAMADI" hukmu (o zaman `hafiza.py:3996`, motor buyudukce KAYDI —
  bugun `hafiza.py:4041`) AYNI kalibin bir uyesiydi: dubious-ownership
  vakasinda git 4 satirlik stderr yazar (`fatal: ...` + cozum komutu),
  motor yalniz ILK satiri basardi — cozum SESSIZCE kaybolurdu (OLCULDU:
  kalem5-tarama/OLCUM_RAPORU_H9_STDERR.md). O satir da `_ilk_satir_
  isaretli`'ye baglandi; asagidaki 4. ve 5. kollar (H9 POZITIF KONTROL /
  H9 MUTANT) bunu olcer. `hafiza.py:3370` (eski `:3325`, ayni kaydis) HALA
  KAPSAM DISIDIR — kardes kusur, AYRI dilim, AYRI kilit bekliyor; gercek
  vakasi bu dosyada HIC kosulmadi.

NE OLCER
  Sabotaj `_ilk_satir_isaretli`'yi isareti DUSUREN hale getirir (yani
  `satirlar[0].rstrip()` doner — kusurun kendisi, "TEK SATIRA dus" ile
  ESDEGERDIR). AYNI vaka, AYNI kum-havuzu tarifi (OLCUM_RAPORU_B6.md §2 /
  M-Y3 ile BIREBIR AYNI — kum havuzu PAYLASILMAZ, HER motora AYRI depo):
  git init+commit -> `kur` -> `korunan --dosya=NOTLAR.md` -> NOTLAR.md
  UTF-8 DISI bayta (`\xff\xfe`) cevrilir -> `kapi`.

    POZITIF KONTROL (ZORUNLU, uyari 8 — CI #85 dersi: `continue-on-error`
    tasiyan yesil KAPI DEGILDIR): sabotajSIZ motorda AYNI vaka kosulur;
    KEHANET: hukum satiri "(+3 satir: stderr)" isaretini TASIR (isaret
    VAR). Bu kontrol olmadan mutantin kirmizisi "kapi olcuyor" demek
    DEGILDIR.
    MUTANT: sabotajLI motorda AYNI vaka kosulur; KEHANET: isaret
    KAYBOLMALI (kusur GERI GELDI, mutant bunu ISIRIR/yakalar).

  Olculen: **stdout**'taki `O` listesi hukmu (satirda "(+3 satir: stderr)"
  geciyor mu). **`stderr` AYRI boruda tutulur, BIRLESTIRILMEZ** — hukmun
  yasadigi kanal budur (bkz. OLCUM_RAPORU_B6.md §4: stderr atilinca bile
  cozum stdout'ta HIC gorunmuyordu; bu mutant TAM O ayrimi olcer).

  🔴 `kapi`'nin KENDI exit kodu bu vakada H8'in OLCULEMEDI (O-tipi, F
  degil) uretmesi geregi TIPIK OLARAK sifirdan farklidir — sabotajli/
  sabotajsiz FARK ETMEKSIZIN (isaretin VARLIGI O-girdisinin sinifini
  degistirmez, yalniz METNINI degistirir). Bu YUZDEN kehanet `kapi`nin
  ham exit koduna DEGIL, hukum SATIRININ METNINE bakar — ayni ilke
  gitfile_korlugu_mutanti.py'nin 9. kolundaki "hukum SARI/SINIRLI, olculen
  TESHIS METNIDIR" ayrimiyla AYNIDIR.

  🔴 3. ve 4. KOL — H9 STDERR VAKASI (5 Eylul 2026 eklendi, ayni SABOTAJ
  yeniden kullanilir — B6'nin `_ilk_satir_isaretli` govdesi PAYLASILIR,
  cagri yeri farkli): git'in KENDI sahiplik denetimi
  `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` ile supheli hale getirilir (dosya
  sistemine DOKUNULMAZ, chown YOK, root/sudo GEREKMEZ — h9_kesme_
  mutanti.py'nin AYNI ilkesi). Git 4 satirlik bir `fatal: detected dubious
  ownership...` + cozum komutu stderr'i yazar; `_kapi_h9` bunu
  `"H9: git deposu OKUNAMADI%s"` seklinde basar. KEHANET (H8 ile AYNI
  desen, ama N SABITLENMEZ — `_ISARET_DESENI` ANY basamak sayisini
  kabul eder, cunku git'in TAM stderr bicimi surume gore degisebilir):
    H9 POZITIF KONTROL : sabotajsiz motorda hukum satiri `(+N satir:
                          stderr)` isaretini TASIR (isaret VAR).
    H9 MUTANT           : sabotajli motorda isaret KAYBOLMALI (kusur
                          GERI GELDI, ISIRMALI).
  `hafiza.py:3370`daki KARDES kusur (AYNI kaliptan, `kesildi = ...`)
  bu kollarin KAPSAMI DISINDADIR — ayri dilim, ayri kilit bekliyor.

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL —
motor degisirse `count()!=1` ARAC KUSURU verir, YANLIS yere yamanmaz.

CIKIS KODLARI (proje sozlesmesi)
  0  DORT kolun DORDU DE BEKLENDIGI GIBI (pozitif kontrol isaretli, mutant
     isaretsiz — H8 VE H9 vakalarinin ikisinde de)
  1  en az bir kol BEKLENMEDIK
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi)
"""
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
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []          # (ad, durum, ayrinti)

_ISARET = "(+3 satir: stderr)"   # bu vakada N HEP 3'tur (H8/UTF-8 mesaji 4 fiziksel satir)


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ
# `_ilk_satir_isaretli`'yi isareti DUSUREN hale getirir: cok satirli dalin
# SON DONUS satiri, isaret EKLEMEYEN "satirlar[0].rstrip()"e cevrilir —
# kusurun kendisiyle ESDEGER (eski `.split("\n")[0]` de yalniz ilk satiri
# donerdi).
_DUZELTILMIS = 'return "%s%s(+%d satir: stderr)" % (satirlar[0].rstrip(), _ILK_SATIR_ISARET_AYRAC, n)'
_SABOTAJLI = "return satirlar[0].rstrip()"


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (kalem5-tarama/IS_EMRI_B6_BETA.md, hafiza.py "
            "_ilk_satir_isaretli())." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=120, env=None):
    """`stdout` ve `stderr` AYRI doner — BIRLESTIRILMEZ (KALEM 3, uyari 5)."""
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if env:
        o.update(env)
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="b6-mut", GIT_AUTHOR_EMAIL="b6-mut@example.invalid",
    GIT_COMMITTER_NAME="b6-mut", GIT_COMMITTER_EMAIL="b6-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kum_havuzu_kur(motor, kok):
    """Uretim tarifi (OLCUM_RAPORU_B6.md §2, M-Y3'un kum havuzuyla BIREBIR
    AYNI — OLCULDU): git init+commit -> `kur` -> `korunan` (H8) -> NOTLAR.md
    UTF-8 DISI bayta cevrilir. Motora DOKUNMAZ, yalniz komut satirindan
    cagirir. KUM HAVUZU PAYLASILMAZ: her cagiran KENDI `kok`unu verir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "B6", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    notlar = os.path.join(kok, "NOTLAR.md")
    with open(notlar, "w", encoding="utf-8", newline="\n") as f:
        f.write("not\nBASLA\nkorunan icerik satiri\nBITIS\n")
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))
    rc, c, e = _kos(motor, ["korunan", "--kok=" + kok, "--dosya=NOTLAR.md",
                         "--bas=BASLA", "--son=BITIS",
                         "--gerekce=b6 satir sayisi mutanti icin korunan blok"])
    if rc != 0:
        raise AracKusuru("korunan basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    with open(notlar, "wb") as f:
        f.write(b"\xff\xfe")


def _olculemedi_satiri(stdout_metni):
    return next((s for s in stdout_metni.splitlines()
                 if "H8 (NOTLAR.md): OLCULEMEDI" in s), None)


def _sinama(taban, etiket, ad, motor, beklenen_isaretli):
    """`motor` (sabotajsiz/sabotajli) ile TAZE, AYRI bir kum havuzunda vaka
    kurulur, `kapi` kosulur. KEHANET: hukum satirinda `_ISARET`
    ("(+3 satir: stderr)") gecip gecmedigi. `stdout`/`stderr` AYRI okunur;
    yalniz stdout'a bakilir (KALEM 3: "olculen stdout'taki O listesi
    hukmu")."""
    alt = os.path.join(taban, etiket)
    os.makedirs(alt, exist_ok=True)
    kok = os.path.join(alt, "proje")
    try:
        _kum_havuzu_kur(motor, kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    rc, cout, cerr = _kos(motor, ["kapi", "--kok=" + kok])
    satir = _olculemedi_satiri(cout)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H8 OLCULEMEDI satiri stdout'ta bulunamadi (exit=%s)\n"
              "      ham stdout kuyrugu: %s\n"
              "      ham stderr kuyrugu: %s"
              % (rc, cout[-500:], cerr[-500:]))
        return
    isaretli = _ISARET in satir
    dogru = (isaretli == beklenen_isaretli)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "exit=%s | '%s' gecti mi=%s (beklenen: %s)\n      satir: %s"
          % (rc, _ISARET, "VAR" if isaretli else "yok",
             "VAR" if beklenen_isaretli else "yok", satir.strip()))


# --------------------------------------------------------------- H9 STDERR VAKASI
# (kalem5-tarama/IS_EMRI_H9_STDERR_ISARET.md, Onur kilidi 5 Eylul 2026 — SIK A)
# AYNI sabotaj (yukarida) yeniden kullanilir: `_ilk_satir_isaretli`nin govdesi
# H8 (`kapi_yalit`) VE H9 (`_kapi_h9`) cagri yerlerinin IKISI TARAFINDAN da
# paylasilir. Bu yuzden BURADA AYRI bir `_DUZELTILMIS`/`_SABOTAJLI` cifti YOK
# — `_sabotajli_motor()` her ikisini de ayni anda sabote eder.

_ISARET_DESENI = re.compile(r"\(\+\d+ satir: stderr\)")   # N sabitlenmez, OLCULUR
# (H8 vakasinda N hep 3'tur ama H9'un git stderr'i FARKLI sayida satir
# tasiyabilir — surume gore degisebilir; sabit sayi yazmak KALEM5_KESME_
# TARAMASI.md'nin "SAYI DEGIL FORMUL YAZ" dersini ihlal ederdi.)

_OLCUM_ORTAMI_SAHIPLIK = {
    "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1",   # tetikleyici (root/sudo GEREKMEZ)
    "GIT_CONFIG_NOSYSTEM": "1",               # kuresel/sistem `safe.directory`
    "GIT_CONFIG_GLOBAL": os.devnull,          # bagisikligi (h9_kesme_mutanti.py
    "GIT_CONFIG_SYSTEM": os.devnull,          # ile AYNI ilke)
}


def _h9_kum_havuzu_kur(motor, kok):
    """H9/dubious-ownership vakasi icin kum havuzu: git init -> `kur` (
    `.hafizarc` olmadan `kapi` YARIDA KESILIR, ISIR OLCULMEZ) -> commit.
    Git'in KENDI sahiplik denetimi `GIT_TEST_ASSUME_DIFFERENT_OWNER` ile
    devreye girer (dosya sistemine DOKUNULMAZ, chown YOK, root/sudo
    GEREKMEZ — h9_kesme_mutanti.py'nin AYNI ilkesi/gerekcesi)."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "H9", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))


def _h9_satiri(stdout_metni):
    return next((s for s in stdout_metni.splitlines()
                 if "H9: git deposu OKUNAMADI" in s), None)


def _sinama_h9(taban, etiket, ad, motor, beklenen_isaretli):
    """AYRI kum havuzu (paylasilmaz). `kapi`, git'in KENDI sahiplik denetimi
    supheli hale getirilerek (`GIT_TEST_ASSUME_DIFFERENT_OWNER=1`) kosulur.
    KEHANET: hukum satirinda `_ISARET_DESENI` ("(+N satir: stderr)", N
    SABITLENMEDEN) gecip gecmedigi. `stdout`/`stderr` AYRI okunur; yalniz
    stdout'a bakilir (H8 kollarindaki ayni ilke)."""
    alt = os.path.join(taban, etiket)
    os.makedirs(alt, exist_ok=True)
    kok = os.path.join(alt, "proje")
    try:
        _h9_kum_havuzu_kur(motor, kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    rc, cout, cerr = _kos(motor, ["kapi", "--kok=" + kok], env=dict(_OLCUM_ORTAMI_SAHIPLIK))
    satir = _h9_satiri(cout)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H9 OKUNAMADI satiri stdout'ta bulunamadi (exit=%s) — "
              "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ "
              "olabilir (surum/platform). Ham stdout kuyrugu: %s\n"
              "      ham stderr kuyrugu: %s"
              % (rc, cout[-500:], cerr[-500:]))
        return
    isaretli = _ISARET_DESENI.search(satir) is not None
    dogru = (isaretli == beklenen_isaretli)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "exit=%s | '(+N satir: stderr)' gecti mi=%s (beklenen: %s)\n      satir: %s"
          % (rc, "VAR" if isaretli else "yok",
             "VAR" if beklenen_isaretli else "yok", satir.strip()))


def main():
    print("=" * 82)
    print("B6 SATIR SAYISI MUTANTI — cok satirli oldur() mesaji hukumde isaretleniyor mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="b6km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        # POZITIF KONTROL ZORUNLU (uyari 8): sabotajsiz motorda isaret VAR mi.
        _sinama(taban, "pk",
               "POZITIF KONTROL: sabotajsiz motorda isaret VAR mi",
               MOTOR, True)

        sab_dizin = os.path.join(taban, "sab")
        os.makedirs(sab_dizin, exist_ok=True)
        try:
            motor_sab = _sabotajli_motor(sab_dizin)
        except AracKusuru as e:
            _kayit("MUTANT: sabotajli motorda isaret KAYBOLMALI (ISIRMALI)",
                  OLCULEMEDI, "sabotajli motor kurulamadi: %s" % e)
            _kayit("H9 MUTANT: sabotajli motorda isaret KAYBOLMALI (ISIRMALI, dubious-ownership)",
                  OLCULEMEDI, "sabotajli motor kurulamadi: %s" % e)
            motor_sab = None
        if motor_sab:
            _sinama(taban, "mut",
                   "MUTANT: sabotajli motorda isaret KAYBOLMALI (ISIRMALI)",
                   motor_sab, False)

        # --- H9 stderr vakasi (kalem5-tarama/IS_EMRI_H9_STDERR_ISARET.md, 5 Eylul 2026) ---
        _sinama_h9(taban, "h9pk",
                  "H9 POZITIF KONTROL: sabotajsiz motorda isaret VAR mi (dubious-ownership)",
                  MOTOR, True)
        if motor_sab:
            _sinama_h9(taban, "h9mut",
                      "H9 MUTANT: sabotajli motorda isaret KAYBOLMALI (ISIRMALI, dubious-ownership)",
                      motor_sab, False)

        print()
        for ad, durum, ayrinti in SONUC:
            print("  %-16s %s" % (durum, ad))
            print("  %-16s   %s" % ("", ayrinti))
        print(CIZGI)
        beklenmedik = sum(1 for _, d, _ in SONUC if d == BEKLENMEDIK)
        olculemedi = sum(1 for _, d, _ in SONUC if d == OLCULEMEDI)
        gibi = len(SONUC) - beklenmedik - olculemedi
        print("SONUC: %d/%d kol BEKLENDIGI GIBI - %d beklenmedik - %d olculemedi"
              % (gibi, len(SONUC), beklenmedik, olculemedi))
        if beklenmedik:
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

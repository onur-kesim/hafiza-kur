#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GITFILE KORLUGU MUTANTI — `_kapi_h9`, `.git` bir DOSYA (gitfile) oldugunda
SAGLIKLI bir depoyu "git YOK" diye mi raporluyor? (my4-epsilon/IS_EMRI_EPSILON.md
KALEM 2, Onur kilidi ONCE-MUTANT, 19 Agu 2026)

🔴 BU TUR DUZELTME YAPMAZ. Kalip `hukum_tutarliligi_mutanti.py`: kusuru
DUZELTMEDEN ONCE motorda KIRMIZI yanan bir kapi. Beklenen ILK SONUC exit 1'dir
— kusur ISIRIYOR, kanit budur.

NEDEN VAR (my4-epsilon/MY4_OLCUM_RAPORU.md §4, M-Y4 turunun YAN URUNU)
  `_kapi_h9`, git varligini `os.path.isdir(kok/".git")` ile sinar
  (`hafiza.py:3923`) — AYNI kontrol `hafiza.py:4405`de `git_var`
  (H14'un kirli/izlenen gorusu) icin de tekrarlanir. Ama modern git'te `.git`
  cogu zaman bir DIZIN degil, gitdir'e isaret eden bir METIN DOSYASIDIR
  ("gitfile"): `git worktree add`, `git init --separate-git-dir`, ve HER
  submodule calisma dizini bu sekli kullanir. Ucunde de depo TAMAMEN
  SAGLIKLIDIR (`git log` exit 0) ama `isdir()` False doner ⇒ motor "H9: git
  YOK" der. Hukum YANLIS **ve** `izlenmeli` zinciri (defterler git'te
  izleniyor mu?) HIC KOSMAZ — kapi sessizce "YESIL (SINIRLI)" kapanir.

  Bu, projenin ZATEN KAPATTIGI P-1 kusurunun ("commit'siz git deposu
  'okunamadi' diye YANLIS teshis edilmesin") IKIZIDIR ⇒ sinifin IKINCI
  ISIRIGI (ISLEYIS md.8: iki kez isirmayan olay kural olamaz — bu ISIRDI).

NE OLCER — BES KOL, IKI SINIF
  KUSUR KOLLARI (su an BEKLENMEDIK vermeli — kusur henuz duzeltilmedi):
    1. worktree          : `git worktree add` ile baglanan calisma agaci
    2. separate-git-dir   : `git init --separate-git-dir=<harici>`
    3. submodule          : bir submodule'un KENDI calisma dizini
    Her uc kolda da GERCEK vaka kurulur (sahte metin degil), defterler
    commit'lenir, `kapi` kosulur; KEHANET: ciktida "H9: git YOK" GECMEMELI.
    (Su an GECIYOR — kusur budur.)
  KONTROL KOLLARI (simdi de duzeltmeden sonra da BEKLENDIGI GIBI vermeli):
    4. git hic yok (salt dizin) : KEHANET: "H9: git YOK" GECMELI. Duzeltmenin
       asiri-tetiklemedigini (`.git` gercekten yoksa hala doğru "YOK" demeli)
       olcer.
    5. `git` PATH'te yok (`PATH=""` ile kosum) : KEHANET: yine "H9: git YOK".
       AYRI eksen — `.git` VAR (isdir=True) ama git BINARY'sinin KENDISI
       calistirilamiyor; hata YUTULMADAN yine dogru hukme dusuyor mu.
  🔴 4. VE 5. KOL SART (ortusen tespit korlugu, brief §2.2): bir duzeltme
  `rev-parse`e gecince "her yerde git var" demeye baslayabilir; bunu olcen
  TEK sey bu iki koldur — biri ayirdedir (dizin), digeri BINARY yoklugudur.

  6. KAYNAK KAPISI (Onur denetimi 19 Agu 2026 — my4-epsilon iki numarali is
     emri): Cowork bagimsiz denetiminde OLCTU: kusurun İKİ yeri var —
     `hafiza.py:3923` (H9) VE `hafiza.py:4405` (`git_var`, H14'un kirli/
     izlenen gorusu). Motorda YALNIZ 3923 duzeltilip 4405 birakilirsa
     yukaridaki BES kol 5/5 YESIL, exit 0 verir — YARIM DUZELTME KAPIDAN
     GECER, cunku hicbir kol 4405'in KENDI belirtisini olcmez. Bu, projenin
     kendi kuralinin ("her duzeltmeye AYRI mutant") ihlaliydi.
     6. kol bu BOSLUGU KAYNAK SEVIYESINDE kapatir: `hafiza.py` metninde
     `os.path.isdir(os.path.join(kok, ".git"))` deseni KAC KEZ geciyor?
     KEHANET: 0. OLCULDU (Onur denetimi): su anki motorda 2, yarim
     duzeltmede (yalniz 3923) 1, tam duzeltmede (3923+4405) 0 — desen ucunu
     da AYIRT EDIYOR. Yanlis-pozitif riski OLCULDU: motorda toplam
     `os.path.isdir(` cagrisi 30 (Onur denetimi tekrar sayidi; is emrindeki
     ilk beyan 20'ydi — TUTMADI, duzeltildi burada beyan edilir), ama TAM
     desene uyan YALNIZ bu 2'si; digerlerinin hicbiri `.git` sinamasi degil.
  7. DAVRANIS KOLU — H14 SESSIZ BASTIRMA (Onur denetimi 19 Agu 2026, Cowork'un
     ARADIGI AMA BULAMADIGI ayirici — bkz. asagidaki 🔴 not): worktree +
     ESKI TARIHLI commit'te git_var YANLIŞ FALSE dondugunde H14'un KENDI
     "[H14] hafiza tarihi proje dosyalarindan N gun ILERIDE — tutarsiz."
     FAIL'i SESSIZCE KAYBOLUYOR (duz depoda AYNI kurulumda GORUNUYOR).
     Yani kusur yalniz "git YOK" yanlis SINIFLAMASI degil, GERCEK bir H14
     bulgusunu da YUTUYOR. KEHANET: bu satir GECMELI (saglikli motorun
     davranisi). Su an GECMIYOR — BEKLENMEDIK.

🔴 4405'IN DAVRANISSAL BELIRTISI ARANDI VE BULUNDU (Onur denetimi 19 Agu
2026 — Cowork'un kendi ölçümünde bulamadığı ayrım): `_h14_git_durumu`nun
`git_var`i False donerse H14 TUM adaylari HAM mtime ile kiyaslar
(`_h14_en_yeni`); True donerse TAKIP EDILEN+TEMIZ dosyalar `git log -1
--format=%ct` (ICERIK tarihi) ile, geri kalani mtime ile kiyaslanir.
GERCEKTEN KOSULDU (Windows + WSL, N=1 ham cikti): ayni proje (kur + bir
IZLENEN dosya + ESKI TARIHLI commit `GIT_AUTHOR_DATE`), iki kol —
  duz depo   : `H14: hafiza projeyle es (en yeni degisiklik 2026-08-01, ...)`
               + `[H14] hafiza tarihi proje dosyalarindan 18 gun ILERIDE — tutarsiz.`
  worktree   : `H14: hafiza projeyle es (en yeni degisiklik 2026-08-19, ...)`
               (FAIL satiri YOK — git_var False, dosya mtime "simdi"ye
               dusuyor, gercek eski commit tarihi hic GORULMUYOR)
Cowork'un kendi denemesi (mtime tazeleme + tarih geri cekme, TEK SENARYODA)
bu ayrimi YAKALAYAMAMISTI; sebebi muhtemelen "hafiza tarihi" (`t_son`)
PROJE_HAFIZA.md ICERIGINDEN cozulup HER IKI kolda da ayni kaldigindan (dogru
gozlem), ama PROJE dosyasi tarafinin (`en_yeni_t`) ayni AYRIMA ugramasi icin
en az bir gercek IZLENEN dosyanin (`kur` cikisinin kendi disinda) var olmasi
GEREKIYORDU — o adim bu denetimde EKLENDI. ⇒ 7. kol BULUNDU ve eklendi.

DUZELTME TASARIMINA OLCULMUS UYARI (bu turda UYGULANMAZ — my4-epsilon/
IS_EMRI_EPSILON.md §2.4): dogru prob `git -C <kok> rev-parse --git-dir`,
AMA ust dizinlere YURUR — bir git deposunun ICINDEKI alt proje de "git var"
sayilir. Bir proje sinifini SARI'dan KIRMIZI'ya tasiyabilir (defterler
commit'siz kalirsa `izlenmeli` zinciri kirmizi yakar). Bu ayri bir tasarim
karari, Onur kilidi ister; bu dosyanin KAPSAMI DISINDA.

CAPA: motora KOD PARCACIGIYLA anchor atilir gerekirse (bu turda motor hic
DEGISMEZ, capa YOK — bu dosya yalniz OKUR).

CIKIS KODLARI (proje sozlesmesi)
  0  yedi kolun YEDISI DE BEKLENDIGI GIBI (kusur TAMAMEN DUZELTILMIS demektir)
  1  en az bir kol BEKLENMEDIK (BEKLENEN ILK SONUC — kusur henuz duzeltilmedi;
     su an 1·2·3·6·7 BEKLENMEDIK, 4·5 BEKLENDIGI GIBI ⇒ 2/7)
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU (kum havuzu kurulamadi)
"""
import datetime as _dt
import os
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

_KEHANET = "H9: git YOK"


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


def _kos(arglar, saniye=120, env=None, kok_calisma=None):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if env is not None:
        o = env
        o["PYTHONIOENCODING"] = o.get("PYTHONIOENCODING", "utf-8")
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", MOTOR] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace",
                           cwd=kok_calisma)
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    except OSError as e:
        return None, "ARAC KUSURU (subprocess baslatilamadi): %s" % e
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (" ".join(args), (r.stderr or r.stdout).strip()[:250]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="gitfile-mut", GIT_AUTHOR_EMAIL="gitfile-mut@example.invalid",
    GIT_COMMITTER_NAME="gitfile-mut", GIT_COMMITTER_EMAIL="gitfile-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kur_ve_commitle(kok, ad="GF"):
    """`kur` kosar, tum defterleri commit'ler. `kok` ONCEDEN git-init'lenmis
    olmalidir (bu fonksiyon init YAPMAZ — cagiran, senaryoya gore init'i
    KENDI secer: duz `git init`, `--separate-git-dir`, ya da submodule'un
    KENDI depo tarihi)."""
    rc, c = _kos(["kur", "--ad", ad, "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))


def _kapi_ham(kok, env=None):
    return _kos(["kapi", "--kok=" + kok], env=env)


def _sinama(taban, etiket, ad, kok_kurucu, beklenen_gecer):
    """`kok_kurucu(alt_taban) -> kok` kurar; `kapi` kosar; KEHANET
    (_KEHANET metninin gecip gecmemesi) `beklenen_gecer`le KARSILASTIRILIR.
    `etiket` KISA, dosya-adi-guvenli bir alt dizin adidir (`ad` insan-okur
    aciklamadir, dizin adina PARSE EDILMEZ — sondaki nokta/parantez Windows'ta
    gecersiz dizin adi uretirdi)."""
    alt = os.path.join(taban, etiket)
    os.makedirs(alt, exist_ok=True)
    try:
        kok, env = kok_kurucu(alt)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    rc, c = _kapi_ham(kok, env=env)
    if rc is None:
        _kayit(ad, OLCULEMEDI, "kapi kosturulamadi: %s" % c)
        return
    gecti = _KEHANET in c
    dogru = (gecti == beklenen_gecer)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "exit=%s | '%s' gecti mi=%s (beklenen: %s)\n      kok=%s"
          % (rc, _KEHANET, "VAR" if gecti else "yok",
             "VAR" if beklenen_gecer else "yok", kok))


# --------------------------------------------------------------- KOL KURUCULAR

def _kur_worktree(alt):
    ana = os.path.join(alt, "ana")
    os.makedirs(ana, exist_ok=True)
    _git(ana, "init", "-q")
    _kur_ve_commitle(ana)
    baglanan = os.path.join(alt, "baglanan")
    _git(ana, "worktree", "add", "-q", "-b", "dal-gf", baglanan,
        env=dict(os.environ, **_GIT_ORTAM))
    return baglanan, None


def _kur_ayri_gitdir(alt):
    kok = os.path.join(alt, "proje")
    harici = os.path.join(alt, "harici_gitdir")
    os.makedirs(kok, exist_ok=True)
    _git(alt, "init", "-q", "--separate-git-dir=" + harici, "proje")
    _kur_ve_commitle(kok)
    return kok, None


def _kur_submodule(alt):
    ic = os.path.join(alt, "ic_depo")
    os.makedirs(ic, exist_ok=True)
    _git(ic, "init", "-q")
    _kur_ve_commitle(ic, ad="ICDEPO")
    dis = os.path.join(alt, "dis_depo")
    os.makedirs(dis, exist_ok=True)
    _git(dis, "init", "-q")
    with open(os.path.join(dis, "PLASEHOLDER.txt"), "w", encoding="utf-8") as f:
        f.write("dis depo ilk commit\n")
    _git(dis, "add", "-A")
    _git(dis, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "dis taban",
        env=dict(os.environ, **_GIT_ORTAM))
    try:
        _git(dis, "-c", "protocol.file.allow=always", "submodule", "-q",
            "add", ic, "alt_modul")
    except AracKusuru:
        # CVE-2022-39253 sertlestirmesi bazi git surumlerinde salt bayrakla
        # yetinmeyebilir; file:// bicimini de dene (ikinci ve son deneme).
        _git(dis, "-c", "protocol.file.allow=always", "submodule", "-q",
            "add", "file://" + ic.replace("\\", "/"), "alt_modul")
    _git(dis, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "submodule eklendi",
        env=dict(os.environ, **_GIT_ORTAM))
    return os.path.join(dis, "alt_modul"), None


def _kur_git_yok(alt):
    kok = os.path.join(alt, "duz")
    os.makedirs(kok, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    return kok, None


def _kur_git_path_disi(alt):
    kok = os.path.join(alt, "proje")
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    _kur_ve_commitle(kok)
    # `git` KENDISI calistirilamasin diye PATH'i BOSALTIYORUZ — .git YINE VAR
    # (isdir=True), farkli eksen: git BINARY yok.
    yalitilmis = {"PYTHONIOENCODING": "utf-8", "PATH": "",
                  "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
    return kok, yalitilmis


# --------------------------------------------------------------- 6. KOL: KAYNAK

_ISDIR_DESEN = 'os.path.isdir(os.path.join(kok, ".git"))'


def sinama_kaynak_kapisi():
    """6. kol (Onur denetimi 19 Agu 2026): DAVRANIS DEGIL KAYNAK olcer —
    motor metninde `_ISDIR_DESEN` KAC KEZ geciyor? KEHANET: 0. Su an 2
    (3923 + 4405); YARIM duzeltmede (yalniz 3923) 1 kalir ve YINE
    BEKLENMEDIK'tir — yarim duzeltme bu kolu da GECEMEZ."""
    ad = "6. KAYNAK KAPISI (os.path.isdir(kok/.git) deseni KAC KEZ geciyor)"
    try:
        src = open(MOTOR, encoding="utf-8").read()
    except OSError as e:
        _kayit(ad, OLCULEMEDI, "motor okunamadi: %s" % e)
        return
    n = src.count(_ISDIR_DESEN)
    dogru = (n == 0)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "desen %r motorda %d kez geciyor (beklenen: 0). %s"
          % (_ISDIR_DESEN, n,
             "TAM DUZELTILMIS."
             if dogru else
             "3923 VE/veya 4405 hala eski deseni tasiyor."))


# --------------------------------------------------------------- 7. KOL: DAVRANIS

def _kur_worktree_eski_tarihli(alt):
    """7. kol icin: worktree + GERCEK bir IZLENEN dosya (kur'un kendi
    cikisi disinda — `_h14_adaylar` PROJE_HAFIZA.md/.hafizarc'i HARIC
    tutar, bu yuzden H14'un ayrisma URETMESI icin EN AZ bir baska izlenen
    dosya SART) + BUGUNDEN 30 gun ONCEYE backdate'lenmis commit (statik
    tarih YAZILMAZ — `hafiza_gecikme_gun` varsayilani 2 gun, 30 gun HER
    kosumda rahat asar)."""
    ana = os.path.join(alt, "ana")
    os.makedirs(ana, exist_ok=True)
    _git(ana, "init", "-q")
    rc, c = _kos(["kur", "--ad", "GF7", "--kok=" + ana])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    with open(os.path.join(ana, "uygulama.py"), "w", encoding="utf-8") as f:
        f.write("ornek kaynak kodu\n")
    _git(ana, "add", "-A")
    eski = (_dt.datetime.now() - _dt.timedelta(days=30)).strftime("%Y-%m-%dT12:00:00")
    ortam = dict(os.environ, **_GIT_ORTAM)
    ortam["GIT_AUTHOR_DATE"] = eski
    ortam["GIT_COMMITTER_DATE"] = eski
    _git(ana, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "eski taban", env=ortam)
    baglanan = os.path.join(alt, "baglanan")
    _git(ana, "worktree", "add", "-q", "-b", "dal-gf7", baglanan,
        env=dict(os.environ, **_GIT_ORTAM))
    return baglanan, None


def sinama_davranis_bastirma(taban):
    """7. kol (Onur denetimi 19 Agu 2026, Cowork'un aradigi ama BULAMADIGI
    ayirici — modul docstring'inde 🔴 not): worktree + eski tarihli
    commit'te H14'un GERCEK '[H14] hafiza tarihi ... ILERIDE' FAIL'i
    SESSIZCE mi kayboluyor? KEHANET: satir GECMELI (saglikli/duz depo
    davranisi — asagida ayrica dogrulanan N=1 ham cikti)."""
    ad = ("7. DAVRANIS KOLU: H14 'hafiza tarihi ... ILERIDE' FAIL'i worktree'de "
          "SESSIZCE kayboluyor mu")
    alt = os.path.join(taban, "dav")
    os.makedirs(alt, exist_ok=True)
    try:
        kok, env = _kur_worktree_eski_tarihli(alt)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    rc, c = _kapi_ham(kok, env=env)
    if rc is None:
        _kayit(ad, OLCULEMEDI, "kapi kosturulamadi: %s" % c)
        return
    satir = next((s for s in c.splitlines()
                  if "hafiza tarihi proje dosyalarindan" in s), None)
    gecti = satir is not None
    _kayit(ad, BEKLENDIGI_GIBI if gecti else BEKLENMEDIK,
          "exit=%s | '[H14] hafiza tarihi proje dosyalarindan ... ILERIDE' satiri "
          "gecti mi=%s (beklenen: VAR — saglikli motor bunu basar)\n      kok=%s%s"
          % (rc, "VAR" if gecti else "yok", kok,
             ("\n      satir: " + satir.strip()) if satir else ""))


def main():
    print("=" * 82)
    print("GITFILE KORLUGU MUTANTI — `.git` DOSYA oldugunda saglikli depo 'git YOK' mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s (BU TURDA DEGISMEDI)" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h16km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        _sinama(taban, "wt", "1. worktree (KUSUR KOLU)", _kur_worktree, False)
        _sinama(taban, "sgd", "2. separate-git-dir (KUSUR KOLU)", _kur_ayri_gitdir, False)
        _sinama(taban, "sub", "3. submodule (KUSUR KOLU)", _kur_submodule, False)
        _sinama(taban, "yok", "4. git hic yok (KONTROL)", _kur_git_yok, True)
        _sinama(taban, "yolsuz", "5. git PATH'te yok (KONTROL, AYRI EKSEN)", _kur_git_path_disi, True)
        sinama_kaynak_kapisi()
        sinama_davranis_bastirma(taban)
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
            print("  (BEKLENEN ILK SONUC budur: kusur henuz DUZELTILMEDI — bu tur ONCE-MUTANT.)")
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

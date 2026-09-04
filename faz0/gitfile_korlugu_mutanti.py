#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GITFILE KORLUGU MUTANTI — `_kapi_h9`, `.git` bir DOSYA (gitfile) oldugunda
SAGLIKLI bir depoyu "git YOK" diye mi raporluyor? (my4-epsilon/IS_EMRI_EPSILON.md
KALEM 2, Onur kilidi ONCE-MUTANT, 19 Agu 2026)

🔴 O TURDE DUZELTME YAPILMADI (asagidaki iki paragraf my4-epsilon turunun
KENDI kaydidir, tarihsel referans icin oldugu gibi birakildi): Kalip
`hukum_tutarliligi_mutanti.py`: kusuru DUZELTMEDEN ONCE motorda KIRMIZI
yanan bir kapi. Beklenen ILK SONUC exit 1'dir — kusur ISIRIYOR, kanit budur.

GUNCELLEME (20 Agu 2026, gitfile korlugu turu, Onur kilidi — IS_EMRI_GITFILE.md
KALEM 2): kusur bu turda GERCEKTEN DUZELTILDI — `_git_kokte_mi` adinda TEK
bir yardimci fonksiyon yazildi ve `_kapi_h9` ile `_h14_git_durumu`nun IKISI
de ona baglandi. Bu dosya artik ONCE-MUTANT degil — DUZELTILMIS motora karsi
kosulan SONRA-MUTANT/REGRESYON bataryasidir. my4-epsilon'un yedi koluna UC
YENI kol (8, 9, 10 — asagida NE OLCER) eklendi; BEKLENEN SONUC artik
**exit 0 · 10/10 kol BEKLENDIGI GIBI**'dir. Asagidaki "NEDEN VAR" ve "NE
OLCER" bolumlerindeki gecmis-zamanli anlatim BILEREKTIR — kusurun neden var
OLDUGUNU aciklar; kollarin KENDISI (kurulum kodu) DEGISMEDI, yalniz
BEKLENEN HUKUM DEGISTI (BEKLENMEDIK -> BEKLENDIGI GIBI).

NEDEN VAR (my4-epsilon/MY4_OLCUM_RAPORU.md §4, M-Y4 turunun YAN URUNU)
  `_kapi_h9`, git varligini `os.path.isdir(kok/".git")` ile SINARDI (bu
  fonksiyonun kendi govdesinde) — AYNI kontrol `_h14_git_durumu`de `git_var`
  (H14'un kirli/izlenen gorusu) icin de TEKRARLANIYORDU. Ama modern git'te
  `.git` cogu zaman bir DIZIN degil, gitdir'e isaret eden bir METIN
  DOSYASIDIR ("gitfile"): `git worktree add`, `git init --separate-git-dir`,
  ve HER submodule calisma dizini bu sekli kullanir. Ucunde de depo TAMAMEN
  SAGLIKLIDIR (`git log` exit 0) ama `isdir()` False doner ⇒ motor "H9: git
  YOK" der. Hukum YANLIS **ve** `izlenmeli` zinciri (defterler git'te
  izleniyor mu?) HIC KOSMAZ — kapi sessizce "YESIL (SINIRLI)" kapanir.

  Bu, projenin ZATEN KAPATTIGI P-1 kusurunun ("commit'siz git deposu
  'okunamadi' diye YANLIS teshis edilmesin") IKIZIDIR ⇒ sinifin IKINCI
  ISIRIGI (ISLEYIS md.8: iki kez isirmayan olay kural olamaz — bu ISIRDI).

NE OLCER — ON KOL, IKI SINIF (my4-epsilon'un yedi kolu + 20 Agu 2026'da
EKLENEN uc yeni kol)
  KUSUR KOLLARI (my4-epsilon turunde, duzeltmeden ONCE, BEKLENMEDIK
  veriyordu; DUZELTILMIS motorda BEKLENDIGI GIBI vermesi GEREKIR):
    1. worktree          : `git worktree add` ile baglanan calisma agaci
    2. separate-git-dir   : `git init --separate-git-dir=<harici>`
    3. submodule          : bir submodule'un KENDI calisma dizini
    Her uc kolda da GERCEK vaka kurulur (sahte metin degil), defterler
    commit'lenir, `kapi` kosulur; KEHANET: ciktida "H9: git YOK" GECMEMELI.
    (my4-epsilon turunde GECIYORDU — kusur buydu; DUZELTILMIS motorda
    GECMEMESI GEREKIR.)
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
     emri; GUNCELLEME 20 Agu 2026 — gitfile korlugu turu KALEM 2): Cowork
     bagimsiz denetiminde OLCTU: kusurun İKİ yeri var — `_kapi_h9` (H9) VE
     `_h14_git_durumu` (`git_var`, H14'un kirli/izlenen gorusu). Motorda
     YALNIZ birincisi duzeltilip ikincisi birakilsaydi yukaridaki BES kol
     5/5 YESIL, exit 0 verirdi — YARIM DUZELTME KAPIDAN GECERDI, cunku
     hicbir kol ikinci cagri yerinin KENDI belirtisini olcmuyordu. Bu,
     projenin kendi kuralinin ("her duzeltmeye AYRI mutant") ihlali olurdu.
     6. kol bu BOSLUGU KAYNAK SEVIYESINDE kapatir; TEK sayac degil UC sayac
     birden olculur (20 Agu 2026 guncellemesi — eski TEK sayacli hali
     helper'in ikinci cagri yerinden [`_h14_git_durumu`] de cagrildigini
     OLCMUYORDU): `hafiza.py` metninde eski desen
     `os.path.isdir(os.path.join(kok, ".git"))` KAC KEZ geciyor (KEHANET:
     0), `_git_kokte_mi(` KAC KEZ geciyor (KEHANET: TAM 3 — 1 tanim + 2
     cagri) ve helper'in KENDI icindeki
     `os.path.exists(os.path.join(kok, ".git"))` KAC KEZ geciyor (KEHANET:
     TAM 1). OLCULDU (Onur denetimi, 19 Agu 2026): eski motorda eski desen
     2, yarim duzeltmede (yalniz `_kapi_h9`) 1, tam duzeltmede 0 — desen
     ucunu de AYIRT EDIYOR; UC SAYAC birlikte, "helper tanimli ama ikinci
     cagri yerine hic baglanmamis" gibi YARIM bir duzeltmeyi de yakalar (o
     durumda `_git_kokte_mi(` 2 kalirdi, 3 degil). Yanlis-pozitif riski
     OLCULDU: motorda toplam `os.path.isdir(` cagrisi 30 (Onur denetimi
     tekrar sayidi; is emrindeki ilk beyan 20'ydi — TUTMADI, duzeltildi
     burada beyan edilir), ama TAM desene uyan YALNIZ bu 2'si; digerlerinin
     hicbiri `.git` sinamasi degil.
  7. DAVRANIS KOLU — H14 SESSIZ BASTIRMA (Onur denetimi 19 Agu 2026, Cowork'un
     ARADIGI AMA BULAMADIGI ayirici — bkz. asagidaki 🔴 not): worktree +
     ESKI TARIHLI commit'te git_var YANLIŞ FALSE dondugunde H14'un KENDI
     "[H14] hafiza tarihi proje dosyalarindan N gun ILERIDE — tutarsiz."
     FAIL'i SESSIZCE KAYBOLUYOR (duz depoda AYNI kurulumda GORUNUYOR).
     Yani kusur yalniz "git YOK" yanlis SINIFLAMASI degil, GERCEK bir H14
     bulgusunu da YUTUYOR. KEHANET: bu satir GECMELI (saglikli motorun
     davranisi). (my4-epsilon turunde GECMIYORDU — BEKLENMEDIK'ti;
     DUZELTILMIS motorda GECMESI GEREKIR.)

  YENI KOLLAR (20 Agu 2026 EKLENDI — gitfile korlugu turu, Onur kilidi,
  IS_EMRI_GITFILE.md KALEM 2; asagidaki uc kol DUZELTILMIS motora karsi
  kosulur, my4-epsilon'un yedisi gibi ONCE-MUTANT olarak yazilmadi):
    8. ALT DIZIN (uc alt-hal — commit'siz / commit'li / parent
       .gitignore'lu): bir git deposunun alt dizinindeki proje. KEHANET:
       ucunde de exit 0 VE ciktida "H9: git YOK" GECMELI. NIYE: SIK A
       (`--git-dir`, ust dizinlere yurur) bu 3 alt-halin 2'sinde exit 0'i
       exit 1'e tasiyip uc adet "[H9] git'te IZLENMIYOR" FAIL'i basiyordu
       (OLCULDU — bkz. gitfile-turu/OLCUM_RAPORU_GITFILE.md §3); bu kol o
       kapsam patlamasinin GERI GELMEDIGINI dogrular. DEVIR'in sart kostugu
       kol.
    9. BOZUK GITFILE + HAYALI GITDIR (iki alt-hal — `.git` DOSYA icerigi
       COP / gitfile var-olmayan bir gitdir'e isaret ediyor). KEHANET:
       "H9: git deposu OKUNAMADI" GECMELI, "H9: git YOK" GECMEMELI — hukum
       ikisinde de SARI/SINIRLI, olculen TESHIS METNIDIR, hukum degil. NIYE:
       bu D'yi SIK B'den ayiran TEK koldur; B burada "git YOK" der —
       kapatilmis P-1'in kardesi (yanlis teshis).
    10. GIT_DIR ORTAM DEGISKENI: kokte `.git` YOK, depo GIT_DIR +
        GIT_WORK_TREE ortam degiskenleriyle baglaniyor. KEHANET:
        "H9: git var" GECMELI. NIYE: D'yi SIK C'den (saf `exists`) ayiran
        TEK kol; bu kol olmasaydi "sadece exists" yarim duzeltmesi kapidan
        gecerdi.
  Bu uc kolla toplam ON kol olur; hepsi BEKLENDIGI GIBI verince exit 0.

🔴 `_h14_git_durumu`NUN DAVRANISSAL BELIRTISI ARANDI VE BULUNDU (Onur denetimi
19 Agu 2026 — Cowork'un kendi ölçümünde bulamadığı ayrım): `_h14_git_durumu`nun
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

DUZELTME TASARIMINA OLCULMUS UYARI (my4-epsilon/IS_EMRI_EPSILON.md §2.4'te
o turda UYGULANMADI): dogru prob `git -C <kok> rev-parse --git-dir`, AMA ust
dizinlere YURUR — bir git deposunun ICINDEKI alt proje de "git var" sayilir.
Bir proje sinifini SARI'dan KIRMIZI'ya tasiyabilir (defterler commit'siz
kalirsa `izlenmeli` zinciri kirmizi yakar). Bu ayri bir tasarim karari, Onur
kilidi isterdi.

GUNCELLEME (20 Agu 2026): gitfile korlugu turunde uygulanan gercek duzeltme
(`_git_kokte_mi`, uc kademeli) TAM OLARAK bu riski onlemek icin `--git-dir`
YERINE `--show-toplevel` + KOK ESITLIGI kullanir (bkz. skill/scripts/
hafiza.py, `_git_kokte_mi`). 8. kol (ALT DIZIN) bu secimin — SIK A DEGIL SIK
D'nin — dogrulugunu olcer.

CAPA: motora KOD PARCACIGIYLA anchor atilir gerekirse (my4-epsilon turunde
motor DEGISMEDI, capa YOK'tu — bu dosya yalniz OKUR. GUNCELLEME 20 Agu 2026:
gitfile korlugu turunde motor GERCEKTEN DEGISTI, ama capa YINE ATILMADI —
KALEM 3'teki `altin_cikti.py --karsilastir` ve `karmasiklik.py --ihlal` ayri
kapilar DEGISEN kaynagi zaten dogruluyor; bu dosyanin kendi govdesi
degismedigi surece ayrica capaya GEREK YOK).

CIKIS KODLARI (proje sozlesmesi)
  0  on kolun ONU DA BEKLENDIGI GIBI (kusur TAMAMEN DUZELTILMIS demektir —
     20 Agu 2026 gitfile korlugu turundan sonraki BEKLENEN durum budur)
  1  en az bir kol BEKLENMEDIK (my4-epsilon turunde — kusur duzeltilmeden
     ONCE — BEKLENEN ILK SONUC buydu: 1·2·3·6·7 BEKLENMEDIK, 4·5 BEKLENDIGI
     GIBI ⇒ 2/7. Motor DUZELTILDIKTEN sonra herhangi bir kolun BEKLENMEDIK
     kalmasi REGRESYONDUR — Onur'a donulur)
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
_HELPER_CAGRI_DESEN = '_git_kokte_mi('
_EXISTS_DESEN = 'os.path.exists(os.path.join(kok, ".git"))'


def sinama_kaynak_kapisi():
    """6. kol (Onur denetimi 19 Agu 2026; GUNCELLEME 20 Agu 2026 — gitfile
    korlugu turu KALEM 2): DAVRANIS DEGIL KAYNAK olcer. Eski hali TEK sayac
    olcuyordu (yalniz `_ISDIR_DESEN`in 0'a indigini) — bu, helper'in
    `_h14_git_durumu`den de (ikinci cagri yeri) cagrildigini OLCMUYORDU: bir
    duzeltme `_kapi_h9`'u guncelleyip `_h14_git_durumu`yu unutsa bile eski
    desen YINE 0 olurdu (unutulan cagri eski desen DEGIL, hala eski
    ISDIR/exists kombinasyonuysa farkli hikaye; ama helper'a hic
    BAGLANMAMIS bir cagri yeri de TEK sayacta gorunmez). GUNCEL hali UC
    sayacin UCUNU BIRDEN olcer:
      · eski desen `_ISDIR_DESEN`               -> KEHANET: 0
      · `_HELPER_CAGRI_DESEN`                    -> KEHANET: TAM 3 (1 tanim
        + 2 cagri: `_kapi_h9` VE `_h14_git_durumu`)
      · `_EXISTS_DESEN` (helper'in KENDI icinde) -> KEHANET: TAM 1
    UCU BIRDEN dogru olmadan kol BEKLENDIGI GIBI SAYILMAZ — `_HELPER_CAGRI_
    DESEN` sayaci 3'ten AZSA (ornegin 2) helper tanimli ama iki cagri
    yerinden biri hala baglanmamis demektir; bu YARIM duzeltmeyi eski TEK
    sayac YAKALAYAMAZDI (eski desen orada da 0'a duserdi), yeni UC sayac
    YAKALAR."""
    ad = ("6. KAYNAK KAPISI (uc sayac: eski desen · _git_kokte_mi( · "
          "exists(kok/.git))")
    try:
        src = open(MOTOR, encoding="utf-8").read()
    except OSError as e:
        _kayit(ad, OLCULEMEDI, "motor okunamadi: %s" % e)
        return
    n_eski = src.count(_ISDIR_DESEN)
    n_helper = src.count(_HELPER_CAGRI_DESEN)
    n_exists = src.count(_EXISTS_DESEN)
    dogru = (n_eski == 0 and n_helper == 3 and n_exists == 1)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "eski desen %r: %d kez (beklenen 0) · %r: %d kez (beklenen 3) · "
          "%r: %d kez (beklenen 1). %s"
          % (_ISDIR_DESEN, n_eski, _HELPER_CAGRI_DESEN, n_helper,
             _EXISTS_DESEN, n_exists,
             "TAM DUZELTILMIS VE HER IKI CAGRI YERI DE (_kapi_h9, "
             "_h14_git_durumu) HELPER'A BAGLANMIS."
             if dogru else
             "_kapi_h9 VE/veya _h14_git_durumu hala eski deseni tasiyor, "
             "ya da helper'a baglanan cagri sayisi beklenenden farkli."))


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


# --------------------------------------------------------------- 8. KOL: ALT DIZIN
# (20 Agu 2026 EKLENDI — gitfile korlugu turu KALEM 2, DEVIR'in sart kostugu kol)

def _kur_alt_dizin_commitsiz(alt):
    """8a: bir git deposunun (`dis`) alt dizininde bir proje (`proje` = test
    edilen `kok`); `proje` altindaki defterler HENUZ commit'lenmedi. `kok`in
    KENDISI hicbir zaman bir git KOKU DEGILDIR (`--show-toplevel` `dis`i
    doner, `proje`yi degil) ⇒ `_git_kokte_mi(kok)` HER ZAMAN False olmali —
    defterlerin commit durumu bu hukmu DEGISTIRMEMELI (kolun konusu budur)."""
    dis = os.path.join(alt, "dis")
    os.makedirs(dis, exist_ok=True)
    _git(dis, "init", "-q")
    with open(os.path.join(dis, "README.md"), "w", encoding="utf-8") as f:
        f.write("dis depo\n")
    _git(dis, "add", "-A")
    _git(dis, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "dis taban",
        env=dict(os.environ, **_GIT_ORTAM))
    proje = os.path.join(dis, "proje")
    os.makedirs(proje, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF8a", "--kok=" + proje])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    # BILEREKTIR: proje/ altindaki defterler DIS depoya commit'lenmiyor —
    # kolun adi ("commit'siz") budur.
    return proje, None


def _kur_alt_dizin_commitli(alt):
    """8b: ayni kurulum, ama `proje/` defterleri DIS depoya commit'leniyor."""
    dis = os.path.join(alt, "dis")
    os.makedirs(dis, exist_ok=True)
    _git(dis, "init", "-q")
    with open(os.path.join(dis, "README.md"), "w", encoding="utf-8") as f:
        f.write("dis depo\n")
    proje = os.path.join(dis, "proje")
    os.makedirs(proje, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF8b", "--kok=" + proje])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    _git(dis, "add", "-A")
    _git(dis, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "dis taban + proje",
        env=dict(os.environ, **_GIT_ORTAM))
    return proje, None


def _kur_alt_dizin_gitignore(alt):
    """8c: DIS depoda `proje/`nin bir kismini (canli hafiza dosyasi
    PROJE_HAFIZA.md) DISLAYAN bir `.gitignore` var. KEHANET degismez:
    `kok` (`proje/`) yine bir git KOKU DEGIL — `.gitignore`in kapsami
    `_git_kokte_mi` icin ILGISIZDIR, o yalniz `--show-toplevel`in `kok`e
    ESIT olup olmadigina bakar."""
    dis = os.path.join(alt, "dis")
    os.makedirs(dis, exist_ok=True)
    _git(dis, "init", "-q")
    with open(os.path.join(dis, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("proje/PROJE_HAFIZA.md\n")
    _git(dis, "add", "-A")
    _git(dis, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "dis taban + gitignore",
        env=dict(os.environ, **_GIT_ORTAM))
    proje = os.path.join(dis, "proje")
    os.makedirs(proje, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF8c", "--kok=" + proje])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    return proje, None


def sinama_alt_dizin(taban):
    """8. kol (DEVIR sarti — bkz. gitfile-turu/OLCUM_RAPORU_GITFILE.md §3):
    git deposunun ALT DIZININDEKI proje UC farkli defter-durumunda
    (commit'siz / commit'li / DIS `.gitignore`'lu) de HEP "H9: git YOK"
    vermeli VE exit 0 KALMALI. SIK A (`--git-dir`, ust dizinlere yurur) bu
    3 alt-halin 2'sinde exit 0'i exit 1'e tasiyip UC adet
    "[H9] git'te IZLENMIYOR" FAIL'i basiyordu (OLCULDU) — bu kol o kapsam
    patlamasinin GERI GELMEDIGINI dogrular. UC alt-halin HEPSI dogru
    OLMADAN kol BEKLENDIGI GIBI SAYILMAZ (tek bir _kayit'te toplanir —
    my4-epsilon'un 1-7. kollariyla ayni SONUC satir sayisini korumak icin:
    toplam ON kol, 13 degil)."""
    ad = "8. ALT DIZIN (git deposu icinde proje — commit'siz / commit'li / .gitignore'lu)"
    alt_hal = [
        ("alt-a", "commit'siz", _kur_alt_dizin_commitsiz),
        ("alt-b", "commit'li", _kur_alt_dizin_commitli),
        ("alt-c", "DIS .gitignore'lu", _kur_alt_dizin_gitignore),
    ]
    detaylar = []
    olculemedi = False
    hepsi_dogru = True
    for etiket, isim, kurucu in alt_hal:
        alt_dizin = os.path.join(taban, etiket)
        os.makedirs(alt_dizin, exist_ok=True)
        try:
            kok, env = kurucu(alt_dizin)
        except AracKusuru as e:
            olculemedi = True
            detaylar.append("%s: kum havuzu kurulamadi: %s" % (isim, e))
            continue
        rc, c = _kapi_ham(kok, env=env)
        if rc is None:
            olculemedi = True
            detaylar.append("%s: kapi kosturulamadi: %s" % (isim, c))
            continue
        gecti = _KEHANET in c
        dogru = gecti and (rc == 0)
        hepsi_dogru = hepsi_dogru and dogru
        detaylar.append(
            "%s: exit=%s (beklenen 0) | '%s' gecti mi=%s (beklenen: VAR)"
            % (isim, rc, _KEHANET, "VAR" if gecti else "yok"))
    if olculemedi:
        _kayit(ad, OLCULEMEDI, "\n      ".join(detaylar))
        return
    _kayit(ad, BEKLENDIGI_GIBI if hepsi_dogru else BEKLENMEDIK,
          "\n      ".join(detaylar))


# --------------------------------------------------------- 9. KOL: BOZUK GITFILE
# (20 Agu 2026 EKLENDI — gitfile korlugu turu KALEM 2, D'yi SIK B'den ayiran TEK kol)

_KEHANET_OKUNAMADI = "H9: git deposu OKUNAMADI"


def _kur_gitfile_cop(alt):
    """9a: `.git` bir DOSYA ama icerigi COP (gecerli bir gitfile degil)."""
    kok = os.path.join(alt, "proje")
    os.makedirs(kok, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF9a", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    with open(os.path.join(kok, ".git"), "w", encoding="utf-8") as f:
        f.write("bu gecerli bir gitfile degil — duz metin cop\n")
    return kok, None


def _kur_gitfile_hayalet(alt):
    """9b: `.git` DOSYASI var, ama isaret ettigi gitdir VAR OLMAYAN bir
    yol (hayalet gitdir)."""
    kok = os.path.join(alt, "proje")
    os.makedirs(kok, exist_ok=True)
    rc, c = _kos(["kur", "--ad", "GF9b", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    hayalet = os.path.join(alt, "hic_olmayan_gitdir")
    with open(os.path.join(kok, ".git"), "w", encoding="utf-8") as f:
        f.write("gitdir: %s\n" % hayalet.replace("\\", "/"))
    return kok, None


def sinama_bozuk_gitfile(taban):
    """9. kol: D'yi SIK B'den ayiran TEK kol. Iki alt-hal — (a) `.git`
    DOSYA icerigi COP, (b) gitfile HAYALET gitdir'e isaret ediyor. KEHANET
    IKISINDE DE: "H9: git deposu OKUNAMADI" GECMELI **ve** "H9: git YOK"
    GECMEMELI. Hukum ikisinde de SARI/SINIRLI — olculen TESHIS METNIDIR,
    PASS/FAIL degil. NIYE: SIK B burada "git YOK" derdi — kapatilmis P-1'in
    kardesi (yanlis teshis); C ve D "OKUNAMADI" der (dogru teshis)."""
    ad = "9. BOZUK GITFILE + HAYALI GITDIR (.git DOSYA/cop icerik · gitdir -> yok)"
    alt_hal = [
        ("gf-cop", ".git DOSYA, icerigi COP", _kur_gitfile_cop),
        ("gf-hayalet", "gitfile -> HAYALET gitdir", _kur_gitfile_hayalet),
    ]
    detaylar = []
    olculemedi = False
    hepsi_dogru = True
    for etiket, isim, kurucu in alt_hal:
        alt_dizin = os.path.join(taban, etiket)
        os.makedirs(alt_dizin, exist_ok=True)
        try:
            kok, env = kurucu(alt_dizin)
        except AracKusuru as e:
            olculemedi = True
            detaylar.append("%s: kum havuzu kurulamadi: %s" % (isim, e))
            continue
        rc, c = _kapi_ham(kok, env=env)
        if rc is None:
            olculemedi = True
            detaylar.append("%s: kapi kosturulamadi: %s" % (isim, c))
            continue
        okunamadi = _KEHANET_OKUNAMADI in c
        yanlis_git_yok = _KEHANET in c
        dogru = okunamadi and not yanlis_git_yok
        hepsi_dogru = hepsi_dogru and dogru
        detaylar.append(
            "%s: exit=%s | '%s' gecti mi=%s (beklenen: VAR) · '%s' gecti "
            "mi=%s (beklenen: yok)"
            % (isim, rc, _KEHANET_OKUNAMADI, "VAR" if okunamadi else "yok",
               _KEHANET, "VAR" if yanlis_git_yok else "yok"))
    if olculemedi:
        _kayit(ad, OLCULEMEDI, "\n      ".join(detaylar))
        return
    _kayit(ad, BEKLENDIGI_GIBI if hepsi_dogru else BEKLENMEDIK,
          "\n      ".join(detaylar))


# --------------------------------------------------------- 10. KOL: GIT_DIR ORTAM
# (20 Agu 2026 EKLENDI — gitfile korlugu turu KALEM 2, D'yi SIK C'den ayiran TEK kol)

_KEHANET_GIT_VAR = "H9: git var"


def _kur_git_dir_ortam(alt):
    """10. kol: kokte `.git` YOK; depo YALNIZ GIT_DIR + GIT_WORK_TREE ortam
    degiskenleriyle baglaniyor (worktree/submodule/separate-git-dir'in
    HICBIRINDE `kok` icinde bir gitfile/dizin YOKTUR — bu kolu onlardan
    ayiran budur). `_git_kokte_mi` 2. kademede (`kok/.git` var mi) BOS
    doner (yok cunku); 3. kademe (`--show-toplevel`) GIT_WORK_TREE
    sayesinde `kok`u dogru rapor etmeli."""
    kok = os.path.join(alt, "proje")
    gitdir = os.path.join(alt, "harici.git")
    os.makedirs(kok, exist_ok=True)
    _git(alt, "init", "-q", "--separate-git-dir=" + gitdir, "proje")
    _kur_ve_commitle(kok)
    # `--separate-git-dir` `proje/` icine bir GITFILE birakti (2. kolun
    # sinadigi durum budur) — 10. kol onu SILER: `kok`te HICBIR `.git` izi
    # kalmamali, TEK baglanti ortam degiskenleri olmali.
    os.remove(os.path.join(kok, ".git"))
    ortam = dict(os.environ, **_GIT_ORTAM)
    ortam["GIT_DIR"] = gitdir
    ortam["GIT_WORK_TREE"] = kok
    return kok, ortam


def sinama_git_dir_ortam(taban):
    """10. kol: D'yi SIK C'den (saf `exists`) ayiran TEK kol — bu kol
    olmasaydi "sadece exists" yarim duzeltmesi kapidan gecerdi (6. kolun
    dersinin aynisi, davranis duzeyinde). KEHANET: "H9: git var" GECMELI."""
    ad = ("10. GIT_DIR ORTAM DEGISKENI (kokte .git YOK, GIT_DIR+GIT_WORK_TREE "
          "ile baglanan depo)")
    alt_dizin = os.path.join(taban, "gitdirenv")
    os.makedirs(alt_dizin, exist_ok=True)
    try:
        kok, env = _kur_git_dir_ortam(alt_dizin)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    rc, c = _kapi_ham(kok, env=env)
    if rc is None:
        _kayit(ad, OLCULEMEDI, "kapi kosturulamadi: %s" % c)
        return
    gecti = _KEHANET_GIT_VAR in c
    _kayit(ad, BEKLENDIGI_GIBI if gecti else BEKLENMEDIK,
          "exit=%s | '%s' gecti mi=%s (beklenen: VAR)\n      kok=%s"
          % (rc, _KEHANET_GIT_VAR, "VAR" if gecti else "yok", kok))


def main():
    print("=" * 82)
    print("GITFILE KORLUGU MUTANTI — `.git` DOSYA oldugunda saglikli depo 'git YOK' mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s (20 Agu 2026 gitfile korlugu turunde DUZELTILDI —"
          " bu batarya artik SONRA-MUTANT/REGRESYON)" % MOTOR)
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
        sinama_alt_dizin(taban)
        sinama_bozuk_gitfile(taban)
        sinama_git_dir_ortam(taban)
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
            print("  (BEKLENEN SONUC 20 Agu 2026'dan sonra ON kolun ONU DA "
                  "BEKLENDIGI GIBI'dir — bir kol BEKLENMEDIK ise REGRESYON "
                  "demektir, Onur'a donulur.)")
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

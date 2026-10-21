#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H21 SESSIZLIK MUTANTI — `kapi` H21 hicbir dalda SESSIZ mi kaliyor, ve H9 depoyu/alt dizini "git YOK" diye yanlis mi teshis ediyor?
(besli-paket/IS_EMRI_H21_SESSIZLIK.md KALEM 1+2, 20 Eki 2026; hukum sinifi UYARI = Onur kilidi 18 Eki 23:31 aynen, cikis kodu DEGISMEZ)

NEDEN VAR (OLCULDU, Cowork 20 Eki 2026, Windows 11, motor 3085c1a1)
  S1 proje bir deponun ALT dizininde: `kur` `alt\\.gitattributes` yazdi ama `kapi` H21 satiri YOK ve H9 "git YOK" diyor (git VAR, depo VAR: yanlis teshis,
  P-1 sinifi). S2 depo degil: H21 sessiz. S3 depo, henuz commit yok, muhurlu dosyalar izlenmiyor, `.gitattributes` kaldirilmis: H21 sessiz — `acik` suzgeci
  yalniz IZLENEN yollara bakiyordu, koruma yoklugu ilk commit'e kadar gizleniyordu.
  BAGIMSIZ DOGRULAMA (iki tur, 5 salt-okunur ajan, 20 Eki) ek olarak buldu ve hepsi asagidaki hal/sabotajlara girdi: ustte HAYALET/BOZUK `.git` varken git "not a git
  repository" der -> motor "ust dizinlerde de yok" diyordu; ust deponun COMMIT'SIZ `.gitattributes`i (ARA dizin dahil; IC ICE depoda ilgisiz dis depo DEGIL) koruma sayiliyor,
  klon korumasiz kaliyor; `.gitignore`daki yollar "izlenmeyen" sayilip yanlis alarm veriyordu; uyari satirinin SAYILARI/YOLU hicbir yerde dogrulanmiyordu; OKUNAMADI dali ve
  KOKTE bozuk `.git` dali mutantsizdi; sembolik bag uzerinden verilen --kok ust depoyu goremiyordu (abspath); alt dizinde "korumasi OLCULDU" satiri klona tasinmayan
  kaynaklar icin ASIRI IDDIA idi (satir artik "calisma agacinda `text` unset" der ve sinirini soyler).

SECIM (rapora gerekce): alt dizinde `check-attr` GERCEKTEN OLCULUR (isin tercihi). Neden: motor `git -C <kok> check-attr/ls-files` ile kok'e GORELI yollar sorar; git ust
  deponun `.gitattributes`ini de hesaba katar; ikinci klon ust deponun klonudur ve `alt/.gitattributes` orada gecerlidir. Korumali alt dizin TEK bilgi satiri basar (koruma
  kaynagi ust depo olabilir; "ust depo X" yolu ve sayi gorunur olsun). Korumali KOK depo sessizdir (degismedi).

NE OLCER — haller BIR KEZ kurulur (kurulum yalniz `kur`/`git` kullanir; sabotajlar yalniz `kapi` yolundadir), her motor AYNI hallerde `kapi` ile yargilanir. HER halde cikis
kodu 0 (UYARI/OLCULEMEDI exit'i degistirmez; EKSIK_YOL'da eksik defter H10'u kirmizi yakabilir: 0|1):
    ALT_KORUMALI       deponun alt dizininde proje, `kur` + commit                 -> TEK bilgi satiri `· H21: alt dizin (ust depo X) — calisma agacinda `text` unset: N muhurlu yolun hepsi (...)`
    ALT_KORUMASIZ      ayni, `alt/.gitattributes` kaldirilmis + commit (S1)        -> TEK `· H21: ... bozabilir (alt dizin: ust depo X) — muhurlu N yol (izlenen N, izlenmeyen 0); N'inde ...`
    ALT_UST_KORUMA     ayni, ust depoda COMMIT'LI `* -text`, alt'ta yok             -> bilgi satiri (ust deponun korumasi SAYILIR)
    ALT_UST_KOMITSUZ   ust depodaki `* -text` COMMIT'SIZ                            -> TEK `· H21: <ust>/.gitattributes commit'lenmemis ...` (yol TAM dogru)
    ALT_ARA_KOMITSUZ   ust/ara/alt: ARA dizindeki `* -text` COMMIT'SIZ              -> ayni uyari, yol = ara/.gitattributes (ata dongusu ara dizinleri ATLAMAZ)
    ALT_ANA_ICINDE     dis depo B (commit'siz `.gitattributes`) icinde ic depo A, proje A/alt, A'da commit'li koruma -> bilgi satiri (ust = A); B'nin dosyasi ILGISIZ: uyari YOK
    ALT_BAGLI          `ALT_UST_KOMITSUZ` projesine SEMBOLIK BAG uzerinden --kok (POSIX / Windows yetkisi varsa) -> ayni uyari (ata yurumesi GERCEK yoldan baslar)
    ALT_KARISIK_KORUMALI korumali alt dizin + bir muhurlu yol izlenmiyor                -> bilgi satiri N = T (izlenmeyen de sayilir)
    ALT_IGNORE         ust depo `.gitignore: alt/`, alt'ta koruma yok                  -> `klona girecek muhurlu yol YOK · T yol .gitignore'da` (YANLIS ALARM yok)
    ALT_BOZUK_UST      ust dizinde `.git` = cop gitfile                             -> `H21: OLCULEMEDI (git deposu OKUNAMADI: ... ust dizinde .git var ...)`; H9 OKUNAMADI
    ALT_HAYALET        ust dizinde `.git` = var olmayan gitdir'e isaret              -> AYNI (git "not a git repository" der ama depo YOK degil: "ust dizinlerde de yok" DENMEZ)
    ALT_BOS_GIT        ust dizinde `.git` = BOS DIZIN (HEAD'siz)                    -> AYNI (git `.git`i gecersiz sayip yukari bakar ve "not a git repository (or any of the parent directories)" der; Linux/Win/macOS ORTAK: M-OKU-SINIF'in platformlar arasi kancasi)
    KOK_BOZUK_GIT      KOKTE `.git` = cop gitfile                                   -> `H21: OLCULEMEDI (git cikis 128/128: fatal: ...)` (check-attr hata dali; tani git'in stderr'ini tasir)
    DEPO_DEGIL         git deposu degil (S2)                                        -> TEK `· H21: OLCULEMEDI (git deposu degil) ...`; H9 "bu dizin bir git deposu degil"
    IZLENMEYEN         depo, hic commit yok, koruma yok (S3)                        -> `... (izlenen 0, izlenmeyen T); T'inde ...` (izlenme sarti YOK); H9 "HENUZ COMMIT YOK" aynen
    KARISIK            depo + commit, koruma yok, BIR muhurlu yol izlenmiyor         -> `(izlenen T-1, izlenmeyen 1)`
    EKSIK_YOL          hic commit yok, iki muhurlu politika dosyasi diskte YOK       -> `muhurlu T-2 yol (izlenen 0, izlenmeyen T-2)` (olmayan dosya SAYILMAZ)
    BINARY_YOK         git programi PATH'te yok, `.git` yok                          -> TEK `· H21: OLCULEMEDI (git calistirilamiyor, .git yok)`; H9 "git YOK (git programi PATH'te bulunamadi)"
    BINARY_YOK_UST     git programi yok, USTTE `.git` var                            -> `(git calistirilamiyor, ust dizinde .git var)`
    KOK_KORUMALI       kok depo, `kur` + commit (REFERANS)                          -> H21 SATIRI YOK; H9 "git var"
  SAGLAM motorda hepsi YESIL; sabotajlarin HER BIRI YALNIZ KENDI dalini bozar (kirilan (hal, kategori) kumesi beklenene TAM ESIT; kategori H21/H9/EXIT; motoru COKERTEN sabotaj
  EXIT kategorisi uretir = yanlis sebep, ISIRDI sayilmaz). Sembolik bag kurulamiyorsa (Windows yetkisi yok) ALT_BAGLI halleri ve M-UST-REAL ATLANIR (beyan edilir, sayilmaz).

NE OLCMEZ
  Gercek `dubious ownership` (baska kullaniciya ait depo): bu makinede kurulamaz; ayni OKUNAMADI dali cop/hayalet gitfile ile TETIKLENIR ve sabotajlanir. `_git_hali`nin TUTARSIZ dali
  dogal olarak URETILEMEZ (gitfile_korlugu_mutanti kol 1-3 metnini korur). `check-ignore` HATA dali (`_h21_yoksayilan` rc 128): yalniz POSIX'te sembolik bag ardindaki yolla ulasilir
  (`beyond a symbolic link`), halin kurulumu yaygin degil — OLCULMEZ, kodda "uyari AZALTILMAZ" (bos kume) ilkesiyle sabittir. `.git/info/attributes` ve `core.attributesFile` korumayi
  'var' gosterir ama klona TASINMAZ (kok depoda da boyle; belgeli sinir). Ilgisiz bir ust `.gitattributes` commit'siz ise (korumayi sagliyan o degil) uyari YINE verilir (gurultu, belgeli).

TEMP GUVENCESI: haller `tempfile.mkdtemp` altinda kurulur; TEMP'in ATALARINDA `.git` girdisi (dizin/gitfile) varsa "depo degil" halleri kurulamaz => OLCULEMEDI (exit 2), sahte KIRMIZI degil.

KULLANIM    python3 faz0/h21_sessizlik_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve tum mutantlar yalniz kendi dalinda KIRMIZI yakti · 1 saglam kirmizi/mutant KACTI ya da yanlis sebeple yakti · 2 OLCULEMEDI
"""
import os
import re
import shutil
import stat
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
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 84
HALLER = ["ALT_KORUMALI", "ALT_KORUMASIZ", "ALT_UST_KORUMA", "ALT_UST_KOMITSUZ", "ALT_ARA_KOMITSUZ", "ALT_ANA_ICINDE", "ALT_KARISIK_KORUMALI", "ALT_IGNORE",
          "ALT_BOZUK_UST", "ALT_HAYALET", "ALT_BOS_GIT", "KOK_BOZUK_GIT", "DEPO_DEGIL", "IZLENMEYEN", "KARISIK", "EKSIK_YOL", "BINARY_YOK", "BINARY_YOK_UST", "KOK_KORUMALI"]
ALT_BILGI = ["ALT_KORUMALI", "ALT_UST_KORUMA", "ALT_ANA_ICINDE", "ALT_KARISIK_KORUMALI", "ALT_IGNORE"]                 # korumali/ignore: bilgi satiri
KOMITSUZ_UYARI = ["ALT_UST_KOMITSUZ", "ALT_ARA_KOMITSUZ"]                                                          # (+ ALT_BAGLI): ust/ara `.gitattributes` commit'siz
ALT_OLCULEN = ["ALT_KORUMALI", "ALT_KORUMASIZ", "ALT_UST_KORUMA", "ALT_UST_KOMITSUZ", "ALT_ARA_KOMITSUZ", "ALT_ANA_ICINDE", "ALT_KARISIK_KORUMALI", "ALT_IGNORE"]
ALT_OKUNAMAYAN = ["ALT_BOZUK_UST", "ALT_HAYALET", "ALT_BOS_GIT"]
SINIF_ADAYLARI = ["ALT_HAYALET", "ALT_BOS_GIT"]       # M-OKU-SINIF: git bu hallerde "not a git repository" diyorsa (platforma gore DEGISIR: Win/macOS hayalet gitfile icin "gitfile does not point to a valid repository")
BINARY_HALLERI = ["BINARY_YOK", "BINARY_YOK_UST"]
CIKIS_IZIN = {"EKSIK_YOL": (0, 1)}                                                           # eksik defter H10'u kirmizi yakabilir


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin saglam/kor oldugu anlamina GELMEZ."""


def git_ortami(taban):
    g = os.path.join(taban, "gitconfig-global")
    if not os.path.isfile(g):
        with open(g, "w", encoding="utf-8", newline="\n") as f:
            f.write("[user]\n\tname = h21s\n\temail = h21s@example.invalid\n[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n")
    haric = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT")   # baska deponun ortami sizmasin
    ortam = dict((k, v) for k, v in os.environ.items() if k not in haric)
    return dict(ortam, GIT_CONFIG_GLOBAL=g, PYTHONIOENCODING="utf-8")


def git(ortam, kok, *args):
    r = subprocess.run(["git", "-C", kok] + list(args), env=ortam, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:140]))
    return r.stdout


def kos(motor, arglar, kok, ortam):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok], env=ortam, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _agaci_sil(yol):
    def _ac_ve_sil(fn, p, *_):
        try:
            os.chmod(p, stat.S_IWRITE)
            fn(p)
        except OSError:
            pass
    if sys.version_info >= (3, 12):
        shutil.rmtree(yol, onexc=_ac_ve_sil)
    else:
        shutil.rmtree(yol, onerror=_ac_ve_sil)


def kur(motor, ortam, kok, ga_sil=False):
    rc, c = kos(motor, ["kur", "--ad", "H21S"], kok, ortam)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s, exit %s): %s" % (os.path.basename(kok), rc, c.strip().split("\n")[-1][:140]))
    p = os.path.join(kok, ".gitattributes")
    if ga_sil and os.path.isfile(p):
        os.remove(p)


def komitle(ortam, repo):
    git(ortam, repo, "add", "-A")
    git(ortam, repo, "commit", "-q", "-m", "taban")


def yaz(yol, metin):
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)


def alt_dizin(motor, taban, ortam, ad, ust_ga=None, ust_gitignore=None, ga_sil=False, komitle_mi=True, ust_git=None, ara=None, ust_git_dizin=False):
    """Deponun ALT dizininde proje. -> (alt kok, ust depo kok). `ust_git`: ust dizindeki `.git`i bozuk bir DOSYAYLA degistirir (OKUNAMADI halleri).
    `ara`: proje `repo/<ara>/alt` altindadir (ara dizin). `ust_git_dizin`: ust `.git` BOS DIZIN olur (git bunu gecersiz sayip yukari bakar)."""
    repo = os.path.join(taban, ad)
    alt = os.path.join(repo, ara, "alt") if ara else os.path.join(repo, "alt")
    os.makedirs(alt)
    if ust_git_dizin:
        os.makedirs(os.path.join(repo, ".git"))
    elif ust_git is None:
        git(ortam, repo, "init", "-q")
    else:
        yaz(os.path.join(repo, ".git"), ust_git)
    if ust_gitignore is not None:
        yaz(os.path.join(repo, ".gitignore"), ust_gitignore)
    if ust_ga is not None and ust_git is None and not ust_git_dizin:
        yaz(os.path.join(repo, ".gitattributes"), ust_ga)
    kur(motor, ortam, alt, ga_sil=ga_sil)
    if ust_git is None and not ust_git_dizin and komitle_mi:
        komitle(ortam, repo)
    return alt, repo


def ata_git_izi(dizin):
    """`dizin`den yukari ilk `.git` girdisi (dizin YA DA gitfile) -> yol | None. TEMP guvencesi: rev-parse basarisiz olsa bile (bozuk ust `.git`) ata girdisi sezilir."""
    d = os.path.abspath(dizin)
    while True:
        p = os.path.join(d, ".git")
        if os.path.lexists(p):
            return p
        ust = os.path.dirname(d)
        if ust == d:
            return None
        d = ust


def haller_kur(motor, taban):
    """Halleri BIR KEZ kurar (saglam motorla). -> {hal: (kok, ust_depo|None)}, ortam, bos_yol. Sembolik bag kurulabiliyorsa ALT_BAGLI eklenir."""
    os.makedirs(taban, exist_ok=True)
    ortam = git_ortami(taban)
    iz = ata_git_izi(taban)
    if iz:
        raise Kurulamadi("gecici dizinin ATALARINDA `.git` girdisi var (%s) — 'depo degil' halleri kurulamaz; TMP/TEMP'i depo disina al" % iz)
    h = {}
    h["ALT_KORUMALI"] = alt_dizin(motor, taban, ortam, "alt_korumali")
    h["ALT_KORUMASIZ"] = alt_dizin(motor, taban, ortam, "alt_korumasiz", ga_sil=True)
    h["ALT_UST_KORUMA"] = alt_dizin(motor, taban, ortam, "alt_ust", ust_ga="* -text\n", ga_sil=True)
    alt, repo = alt_dizin(motor, taban, ortam, "alt_komitsuz", ga_sil=True)
    yaz(os.path.join(repo, ".gitattributes"), "* -text\n")                       # ust koruma var AMA COMMIT'SIZ
    h["ALT_UST_KOMITSUZ"] = (alt, repo)
    alt, repo = alt_dizin(motor, taban, ortam, "alt_ara", ga_sil=True, ara="ara")
    yaz(os.path.join(repo, "ara", ".gitattributes"), "* -text\n")                # ARA dizinde koruma var AMA COMMIT'SIZ
    h["ALT_ARA_KOMITSUZ"] = (alt, repo)
    dis = os.path.join(taban, "ana_dis")                                         # dis depo B: commit'siz `.gitattributes`, icinde ic depo A
    ic = os.path.join(dis, "ic")
    os.makedirs(os.path.join(ic, "alt"))
    git(ortam, dis, "init", "-q")
    yaz(os.path.join(dis, ".gitattributes"), "* -text\n")
    git(ortam, ic, "init", "-q")
    yaz(os.path.join(ic, ".gitattributes"), "* -text\n")                         # A'nin korumasi COMMIT'LI
    kur(motor, ortam, os.path.join(ic, "alt"), ga_sil=True)
    komitle(ortam, ic)
    h["ALT_ANA_ICINDE"] = (os.path.join(ic, "alt"), ic)
    alt, repo = alt_dizin(motor, taban, ortam, "alt_karisik", ust_ga="* -text\n", ga_sil=True)
    git(ortam, repo, "rm", "--cached", "-q", "alt/KONULAR.md")                   # korumali ama BIR muhurlu yol izlenmiyor
    h["ALT_KARISIK_KORUMALI"] = (alt, repo)
    h["ALT_IGNORE"] = alt_dizin(motor, taban, ortam, "alt_ignore", ust_gitignore="alt/\n", ga_sil=True)
    h["ALT_BOZUK_UST"] = alt_dizin(motor, taban, ortam, "alt_bozuk", ust_git="bu gecerli bir gitfile degil — duz metin cop\n")
    hayalet = os.path.join(taban, "hic_olmayan_gitdir").replace("\\", "/")
    h["ALT_HAYALET"] = alt_dizin(motor, taban, ortam, "alt_hayalet", ust_git="gitdir: %s\n" % hayalet)
    h["ALT_BOS_GIT"] = alt_dizin(motor, taban, ortam, "alt_bos_git", ust_git_dizin=True)
    k = os.path.join(taban, "kok_bozuk")
    os.makedirs(k)
    kur(motor, ortam, k)
    yaz(os.path.join(k, ".git"), "bu gecerli bir gitfile degil — duz metin cop\n")   # KOKTE bozuk `.git` (kur'dan SONRA)
    h["KOK_BOZUK_GIT"] = (k, None)
    k = os.path.join(taban, "depo_degil")
    os.makedirs(k)
    kur(motor, ortam, k)
    h["DEPO_DEGIL"] = (k, None)
    k = os.path.join(taban, "izlenmeyen")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k, ga_sil=True)                                            # hicbir sey izlenmiyor, koruma yok
    h["IZLENMEYEN"] = (k, None)
    k = os.path.join(taban, "karisik")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k, ga_sil=True)
    komitle(ortam, k)
    git(ortam, k, "rm", "--cached", "-q", "KONULAR.md")                          # BIR muhurlu yol izlenmiyor (diskte VAR)
    h["KARISIK"] = (k, None)
    k = os.path.join(taban, "eksik_yol")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k, ga_sil=True)
    os.remove(os.path.join(k, "KONULAR.md"))                                     # iki muhurlu politika dosyasi diskte YOK
    os.remove(os.path.join(k, "SAKLAMA_PLANI.md"))
    h["EKSIK_YOL"] = (k, None)
    k = os.path.join(taban, "binary_yok")
    os.makedirs(k)
    kur(motor, ortam, k)
    h["BINARY_YOK"] = (k, None)
    h["BINARY_YOK_UST"] = h["ALT_BOZUK_UST"]                                     # AYNI proje, git programi yok: ustte `.git` VAR
    k = os.path.join(taban, "kok")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k)
    komitle(ortam, k)
    h["KOK_KORUMALI"] = (k, None)
    bos_yol = os.path.join(taban, "bos-yol")
    os.makedirs(bos_yol, exist_ok=True)
    baglanti = os.path.join(taban, "bagli_lnk")                                  # sembolik bag uzerinden --kok (kurulamazsa ATLANIR)
    try:
        os.symlink(h["ALT_UST_KOMITSUZ"][0], baglanti, target_is_directory=True)
        h["ALT_BAGLI"] = (baglanti, h["ALT_UST_KOMITSUZ"][1])
        if "ALT_BAGLI" not in HALLER:
            HALLER.append("ALT_BAGLI")
    except (OSError, NotImplementedError, AttributeError):
        h["ALT_BAGLI"] = None
    return h, ortam, bos_yol


def gozle(motor, haller, ortam, bos_yol):
    """-> {hal: (exit, [H21 satirlari], [H9 satirlari])} — HER halde `kapi` kosar (kapi salt okunurdur)."""
    gozlem = {}
    for hal in [x for x in HALLER if haller.get(x)]:
        kok = haller[hal][0]
        e = dict(ortam, PATH=bos_yol) if hal in BINARY_HALLERI else ortam          # git calistirilamiyor: PATH git'siz bir dizine cevrilir
        rc, c = kos(motor, ["kapi"], kok, e)
        satirlar = [x.strip() for x in c.split("\n")]
        gozlem[hal] = (rc, [x for x in satirlar if "H21" in x], [x for x in satirlar if x.startswith(("? H9", "· H9"))])
    return gozlem


_UYARI = re.compile(r"^· H21: satir sonu cevrimi muhurlu dosyayi bozabilir(?: \(alt dizin: ust depo (?P<ust>.+?)\))? — "
                    r"muhurlu (?P<t>\d+) yol \(izlenen (?P<iz>\d+), izlenmeyen (?P<izm>\d+)\); (?P<acik>\d+)'inde `text` unset DEGIL")
_BILGI = re.compile(r"^· H21: alt dizin \(ust depo (?P<ust>.+?)\) — calisma agacinda `text` unset: (?P<n>\d+) muhurlu yolun hepsi"
                    r"(?: · (?P<ign>\d+) yol \.gitignore'da \(klona girmez\))? \(`\.git/info/attributes` ve `core\.attributesFile` klona TASINMAZ, OLCULMEZ\)$")
_BILGI0 = re.compile(r"^· H21: alt dizin \(ust depo (?P<ust>.+?)\) — klona girecek muhurlu yol YOK(?: · (?P<ign>\d+) yol \.gitignore'da \(klona girmez\))?$")
_KOMITSUZ = re.compile(r"^· H21: (?P<yol>.+?) commit'lenmemis \(izlenmiyor ya da HEAD'den farkli\) — `-text` korumasi KLONDA GORUNMEZ; `git add (?P<yol2>.+?)` ve commit")
_H9_KOK = re.compile(r"^\? H9: git deposunun KOKU degil \(ust depo: (?P<ust>.+?)\) — ")


def ayni_yol(a, b):
    n = lambda p: os.path.normcase(os.path.realpath(p))
    return n(a) == n(b)


def ihlaller(g, haller, t_ref=None):
    """-> [(hal, kategori, mesaj)] — bos liste = YESIL. kategori: EXIT · H21 · H9. Saglam/sabotajli motor AYNI fonksiyonla yargilanir.
    `t_ref`: SAGLAM motorun IZLENMEYEN halinden okunan muhurlu yol sayisi; sabotajli motorlarda verilir (sabotajin kendisi T'yi bozarsa diger hallere TASMASIN)."""
    out = []

    def ihlal(hal, kat, m):
        out.append((hal, kat, m))

    mevcut = [x for x in HALLER if haller.get(x)]
    for hal in mevcut:
        rc = g[hal][0]
        if rc not in CIKIS_IZIN.get(hal, (0,)):
            ihlal(hal, "EXIT", "kapi exit %s (UYARI/OLCULEMEDI exit'i DEGISTIRMEZ; %s beklenir)" % (rc, "|".join(map(str, CIKIS_IZIN.get(hal, (0,))))))
    mi = _UYARI.match(g["IZLENMEYEN"][1][0]) if len(g["IZLENMEYEN"][1]) == 1 else None
    t = t_ref if t_ref is not None else (int(mi.group("t")) if mi else None)
    # --- korumali / ignore: TEK bilgi satiri
    for hal in ALT_BILGI:
        s = g[hal][1]
        if hal == "ALT_IGNORE":
            m = _BILGI0.match(s[0]) if len(s) == 1 else None
            if not (m and ayni_yol(m.group("ust"), haller[hal][1]) and m.group("ign") and int(m.group("ign")) == (t or -1)):
                ihlal(hal, "H21", "tum muhurlu yollar .gitignore'da: `klona girecek muhurlu yol YOK · T yol .gitignore'da` beklenir (T=%s; ust depo yolu DOGRU): %r" % (t, s))
            continue
        m = _BILGI.match(s[0]) if len(s) == 1 else None
        if not (m and ayni_yol(m.group("ust"), haller[hal][1]) and t is not None and int(m.group("n")) == t and not m.group("ign")):
            ihlal(hal, "H21", "TEK `· H21: alt dizin (ust depo <ust>) — calisma agacinda `text` unset: T muhurlu yolun hepsi ...` bilgi satiri beklenir (T=%s; yol DOGRU; "
                              "izlenmeyen de sayilir): %r" % (t, s))
    # --- korumasiz alt dizin
    s = g["ALT_KORUMASIZ"][1]
    m = _UYARI.match(s[0]) if len(s) == 1 else None
    if not (m and m.group("ust") and ayni_yol(m.group("ust"), haller["ALT_KORUMASIZ"][1])
            and t is not None and int(m.group("t")) == t and int(m.group("iz")) == t and m.group("izm") == "0" and int(m.group("acik")) == t):
        ihlal("ALT_KORUMASIZ", "H21", "TEK `· H21: ... bozabilir (alt dizin: ust depo <ust>) — muhurlu T yol (izlenen T, izlenmeyen 0); T'inde ...` beklenir (ust yolu + SAYILAR): %r" % s)
    # --- ust/ara `.gitattributes` commit'siz: YOL tam dogru
    beklenen_yol = {"ALT_UST_KOMITSUZ": lambda r: os.path.join(r, ".gitattributes"), "ALT_ARA_KOMITSUZ": lambda r: os.path.join(r, "ara", ".gitattributes"),
                    "ALT_BAGLI": lambda r: os.path.join(r, ".gitattributes")}
    for hal in [x for x in KOMITSUZ_UYARI + ["ALT_BAGLI"] if haller.get(x)]:
        s = g[hal][1]
        m = _KOMITSUZ.match(s[0]) if len(s) == 1 else None
        if not (m and m.group("yol") == m.group("yol2") and ayni_yol(m.group("yol"), beklenen_yol[hal](haller[hal][1]))):
            ihlal(hal, "H21", "TEK `· H21: <TAM yol>/.gitattributes commit'lenmemis ...` beklenir (yol = %s): %r" % (beklenen_yol[hal](haller[hal][1]), s))
    # --- git yanitsiz
    for hal in ALT_OKUNAMAYAN:
        s = g[hal][1]
        if len(s) != 1 or not s[0].startswith("· H21: OLCULEMEDI (git deposu OKUNAMADI: ") or "ust dizinde .git var" not in s[0]:
            ihlal(hal, "H21", "TEK `· H21: OLCULEMEDI (git deposu OKUNAMADI: ... ust dizinde .git var ...)` beklenir (depo YOK degil, OKUNAMIYOR): %r" % s)
    s = g["KOK_BOZUK_GIT"][1]
    if len(s) != 1 or not s[0].startswith("· H21: OLCULEMEDI (git cikis ") or "fatal:" not in s[0]:
        ihlal("KOK_BOZUK_GIT", "H21", "TEK `· H21: OLCULEMEDI (git cikis a/b: fatal: ...)` beklenir (check-attr hata dali; git'in stderr'i tasinir): %r" % s)
    # --- depo degil / izlenmeyen / karisik / eksik / binary / referans
    s = g["DEPO_DEGIL"][1]
    if s != ["· H21: OLCULEMEDI (git deposu degil) — satir sonu korumasi olculemedi"]:
        ihlal("DEPO_DEGIL", "H21", "TEK `· H21: OLCULEMEDI (git deposu degil) ...` beklenir: %r" % s)
    s = g["IZLENMEYEN"][1]
    if not (mi and t is not None and t >= 5 and not mi.group("ust") and mi.group("iz") == "0" and int(mi.group("izm")) == t and int(mi.group("acik")) == t):
        ihlal("IZLENMEYEN", "H21", "TEK `· H21: ... muhurlu T yol (izlenen 0, izlenmeyen T); T'inde ...` beklenir (izlenme sarti YOK; T>=5): %r" % s)
    s = g["KARISIK"][1]
    m = _UYARI.match(s[0]) if len(s) == 1 else None
    if not (m and t is not None and not m.group("ust") and int(m.group("t")) == t and int(m.group("iz")) == t - 1 and m.group("izm") == "1"):
        ihlal("KARISIK", "H21", "TEK `· H21: ... muhurlu T yol (izlenen T-1, izlenmeyen 1); ...` beklenir (T=%s): %r" % (t, s))
    s = g["EKSIK_YOL"][1]
    m = _UYARI.match(s[0]) if len(s) == 1 else None
    if not (m and t is not None and not m.group("ust") and int(m.group("t")) == t - 2 and m.group("iz") == "0" and int(m.group("izm")) == t - 2):
        ihlal("EKSIK_YOL", "H21", "TEK `· H21: ... muhurlu T-2 yol (izlenen 0, izlenmeyen T-2); ...` beklenir (diskte OLMAYAN yol SAYILMAZ; T=%s): %r" % (t, s))
    s = g["BINARY_YOK"][1]
    if s != ["· H21: OLCULEMEDI (git calistirilamiyor, .git yok) — satir sonu korumasi olculemedi"]:
        ihlal("BINARY_YOK", "H21", "TEK `· H21: OLCULEMEDI (git calistirilamiyor, .git yok) ...` beklenir: %r" % s)
    s = g["BINARY_YOK_UST"][1]
    if s != ["· H21: OLCULEMEDI (git calistirilamiyor, ust dizinde .git var) — satir sonu korumasi olculemedi"]:
        ihlal("BINARY_YOK_UST", "H21", "TEK `· H21: OLCULEMEDI (git calistirilamiyor, ust dizinde .git var) ...` beklenir: %r" % s)
    if g["KOK_KORUMALI"][1]:
        ihlal("KOK_KORUMALI", "H21", "koruma OLCULDU ve VAR ama kok depoda H21 satiri basildi: %r" % g["KOK_KORUMALI"][1])
    # --- H9 satirlari
    for hal in [x for x in ALT_OLCULEN + ["ALT_BAGLI"] if haller.get(x)]:
        s9 = g[hal][2]
        m = _H9_KOK.match(s9[0]) if len(s9) == 1 else None
        if not (m and ayni_yol(m.group("ust"), haller[hal][1])):
            ihlal(hal, "H9", "H9 satiri `? H9: git deposunun KOKU degil (ust depo: <ust>) — ...` olmali (ust yolu DOGRU): %r" % s9)
    beklenen9 = {
        "ALT_BOZUK_UST": "? H9: git deposu OKUNAMADI: ",
        "ALT_HAYALET": "? H9: git deposu OKUNAMADI: ",
        "ALT_BOS_GIT": "? H9: git deposu OKUNAMADI: ",
        "KOK_BOZUK_GIT": "? H9: git deposu OKUNAMADI",
        "DEPO_DEGIL": "? H9: bu dizin bir git deposu degil (ust dizinlerde de yok)",
        "IZLENMEYEN": "? H9: git deposu var ama HENUZ COMMIT YOK",
        "EKSIK_YOL": "? H9: git deposu var ama HENUZ COMMIT YOK",
        "KARISIK": "· H9: git var",
        "BINARY_YOK": "? H9: git YOK (git programi PATH'te bulunamadi)",
        "BINARY_YOK_UST": "? H9: git YOK (git programi PATH'te bulunamadi)",
        "KOK_KORUMALI": "· H9: git var",
    }
    for hal, onek in beklenen9.items():
        s9 = g[hal][2]
        if len(s9) != 1 or not s9[0].startswith(onek):
            ihlal(hal, "H9", "H9 satiri %r ile baslamali: %r" % (onek, s9))
    return out


def P(halleri, kat):
    return {(h, kat) for h in halleri}


def git_cumlesi(ortam, kok):
    """`kok`te `git rev-parse --show-toplevel`in ilk stderr satiri (LC_ALL=C) — M-OKU-SINIF hangi halde `not a git repository` dalina GIRILDIGINI OLCER."""
    e = dict(ortam, LC_ALL="C", LANGUAGE="C")
    r = subprocess.run(["git", "-C", kok, "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=e, stdin=subprocess.DEVNULL, timeout=30)
    return ((r.stderr or "").strip().splitlines() or [""])[0]


def mutantlar(haller, sinif_halleri=None):
    """ad, aciklama, beklenen kirilan (hal, kategori) kumesi, gerek ('' | 'baglanti'), [(eski, yeni)]. `eski` motorda TAM 1 kez gecmelidir.
    ALT_BAGLI yalniz sembolik bag kurulabildiyse beklenene katilir."""
    bag = ["ALT_BAGLI"] if haller.get("ALT_BAGLI") else []
    return [
        ("M-S1 ALT DIZIN SESSIZE DONER", "alt dizin dalinda olcum yapilmaz", P(ALT_OLCULEN + bag, "H21"), "",
         [("    if hal == \"KOK_DEGIL\":\n        return True, ayr\n", "    if hal == \"KOK_DEGIL\":\n        return False, None   # MUTANT\n")]),
        ("M-S2 DEPO-DEGIL SESSIZE DONER", "depo degilse OLCULEMEDI satiri basilmaz", P(["DEPO_DEGIL"], "H21"), "",
         [("        N.append(\"H21: OLCULEMEDI (git deposu degil)", "        _x = (\"H21: OLCULEMEDI (git deposu degil)")]),
        ("M-S3 IZLENME SUZGECI GERI GELIR", "izlenmeyen yollar sayilmaz (koruma yoklugu ilk commit'e kadar gizlenir)",
         P(["IZLENMEYEN", "KARISIK", "EKSIK_YOL", "ALT_IGNORE", "ALT_KARISIK_KORUMALI"], "H21"), "",
         [("    var = [p for p in yollar if p in izlenen or os.path.lexists(os.path.join(kok, p))]\n",
           "    var = [p for p in yollar if p in izlenen]   # MUTANT\n")]),
        ("M-S3b VAR SUZGECI KALKAR", "diskte OLMAYAN muhurlu yollar da sayilir (sayi yalan soyler)", P(["EKSIK_YOL"], "H21"), "",
         [("    var = [p for p in yollar if p in izlenen or os.path.lexists(os.path.join(kok, p))]\n",
           "    var = list(yollar)   # MUTANT\n")]),
        ("M-S4 KORUMALI ALT DIZIN SESSIZ", "korumali alt dizinde bilgi satiri basilmaz", P(ALT_BILGI, "H21"), "",
         [("    if top:\n        ign = (", "    if False:   # MUTANT\n        ign = (")]),
        ("M-IGNORE GITIGNORE SUZGECI YOK", ".gitignore'daki yollar da sayilir (yanlis alarm)", P(["ALT_IGNORE"], "H21"), "",
         [("    yok = _h21_yoksayilan(kok, [p for p in var if p not in izlenen])\n", "    yok = set()   # MUTANT\n")]),
        ("M-UST-KOMITSUZ UST COMMIT DENETIMI YOK", "alt dizinde ust/ara deponun commit'siz `.gitattributes`i gorulmez", P(["ALT_UST_KOMITSUZ", "ALT_ARA_KOMITSUZ"] + bag, "H21"), "",
         [("        if not top or n(d) == n(top) or ust == d:\n", "        if True:   # MUTANT\n")]),
        ("M-UST-SINIR ATA YURUMESI SINIRSIZ", "ata dongusu ust deponun kokunde DURMAZ (ilgisiz dis depoya yanlis alarm)", P(["ALT_ANA_ICINDE"], "H21"), "",
         [("        if not top or n(d) == n(top) or ust == d:\n", "        if ust == d:   # MUTANT\n")]),
        ("M-UST-ARA ARA DIZIN ATLANIR", "ata dongusu ara dizinlere BAKMAZ (dogrudan ust depoya atlar)", P(["ALT_ARA_KOMITSUZ"], "H21"), "",
         [("        if not top or n(d) == n(top) or ust == d:\n            return None\n        d = ust\n",
           "        if not top or n(d) == n(top) or ust == d:\n            return None\n        d = top   # MUTANT\n")]),
        ("M-UST-REAL ABSPATH GERCEK YOL DEGIL", "ata yurumesi sembolik bagli --kok'ta gercek yoldan baslamaz", P(["ALT_BAGLI"], "H21"), "baglanti",
         [("    d = os.path.realpath(kok)\n    n = lambda p: os.path.normcase(os.path.realpath(p))\n    while True:\n        if _ga_commitsiz(d):\n",
           "    d = os.path.abspath(kok)   # MUTANT\n    n = lambda p: os.path.normcase(os.path.realpath(p))\n    while True:\n        if _ga_commitsiz(d):\n")]),
        ("M-SAYI IZLENEN SAYISI BOZULUR", "uyari satirinda `izlenen` hep 0", P(["ALT_KORUMASIZ", "KARISIK"], "H21"), "",
         [("        iz = len([p for p in var if p in izlenen])\n", "        iz = 0   # MUTANT\n")]),
        ("M-BILGI-SAYI BILGI SATIRI SAYISI BOZULUR", "bilgi satirinda N = len(izlenen) (izlenmeyen sayilmaz)", P(["ALT_KARISIK_KORUMALI"], "H21"), "",
         [("                \"(`.git/info/attributes` ve `core.attributesFile` klona TASINMAZ, OLCULMEZ)\" % (top, len(var), ign))\n",
           "                \"(`.git/info/attributes` ve `core.attributesFile` klona TASINMAZ, OLCULMEZ)\" % (top, len(izlenen), ign))   # MUTANT\n")]),
        ("M-UST-YOL UST DEPO YOLU YANLIS", "uyari `ust depo` yerine projenin kendi yolunu yazar", P(["ALT_KORUMASIZ"], "H21"), "",
         [("    nerede = (\" (alt dizin: ust depo %s)\" % top) if top else \"\"\n", "    nerede = (\" (alt dizin: ust depo %s)\" % kok) if top else \"\"\n")]),
        ("M-OLC-HATA CHECK-ATTR HATA SATIRI SUSAR", "olcum hata verince (kokte bozuk .git) H21 sessiz", P(["KOK_BOZUK_GIT"], "H21"), "",
         [("        N.append(\"H21: OLCULEMEDI (%s) — satir sonu korumasi olculemedi\" % izlenen)\n",
           "        _x = (\"H21: OLCULEMEDI (%s) — satir sonu korumasi olculemedi\" % izlenen)   # MUTANT\n")]),
        ("M-BIN-UST BINARY YOK USTTE .GIT AYRIMI KALKAR", "git yok ve ustte .git varken `.git yok` der", P(["BINARY_YOK_UST"], "H21"), "",
         [("(\"ust dizinde .git var\" if _ust_git_izi(kok) else \".git yok\")", "\".git yok\"")]),
        ("M-OKU-H21 OKUNAMADI SATIRI SUSAR", "git yanitsizsa H21 sessiz", P(ALT_OKUNAMAYAN, "H21"), "",
         [("    N.append(\"H21: OLCULEMEDI (git deposu OKUNAMADI: %s)", "    _x = (\"H21: OLCULEMEDI (git deposu OKUNAMADI: %s)")]),
        ("M-OKU-H9 OKUNAMADI ESKI CUMLEYE", "git yanitsizsa H9 `git YOK` der (yanlis teshis)", P(ALT_OKUNAMAYAN, "H9"), "",
         [("        return \"H9: git deposu OKUNAMADI: %s\" % ayr\n", "        return \"H9: git YOK\" + _H9_SONEK   # MUTANT\n")]),
        ("M-OKU-SINIF UST .GIT GOZETMENI KALKAR", "ustte `.git` VARKEN `not a git repository` => `depo yok` (git'in o cumleyi uretti hal/ler: platformdan OLCULUR)", P(sinif_halleri or [], "H21") | P(sinif_halleri or [], "H9"), "sinif",
         [(" and \"dubious ownership\" not in hata and iz is None:\n", " and \"dubious ownership\" not in hata:   # MUTANT\n")]),
        ("M-H9alt ALT DIZIN ESKI CUMLEYE", "kok degil dali `H9: git YOK` der (yanlis teshis)", P(ALT_OLCULEN + bag, "H9"), "",
         [("        return \"H9: git deposunun KOKU degil (ust depo: %s)%s\" % (ayr, _H9_SONEK)\n",
           "        return \"H9: git YOK\" + _H9_SONEK   # MUTANT\n")]),
        ("M-H9depo DEPO YOK ESKI CUMLEYE", "depo yok dali `H9: git YOK` der (yanlis teshis)", P(["DEPO_DEGIL"], "H9"), "",
         [("        return \"H9: bu dizin bir git deposu degil (ust dizinlerde de yok)\" + _H9_SONEK\n",
           "        return \"H9: git YOK\" + _H9_SONEK   # MUTANT\n")]),
        ("M-H9bin BINARY YOK DEPO CUMLESINE", "binary yok dali `depo degil` der (ayrim kaybolur)", P(BINARY_HALLERI, "H9"), "",
         [("    return \"H9: git YOK (git programi PATH'te bulunamadi)\" + _H9_SONEK\n",
           "    return \"H9: bu dizin bir git deposu degil (ust dizinlerde de yok)\" + _H9_SONEK   # MUTANT\n")]),
    ]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def main():
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_MOTOR
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz.")
        return 2
    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("H21 SESSIZLIK MUTANTI — H21 hicbir dalda sessiz degil, H9 ayri cumleler · platform: %s" % sys.platform)
    print("motor: %s" % motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="h21s_")
    try:
        try:
            haller, ortam, bos_yol = haller_kur(motor, os.path.join(taban, "haller"))
            g = gozle(motor, haller, ortam, bos_yol)
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        if not haller.get("ALT_BAGLI"):
            print("  (ATLANDI: sembolik bag kurulamadi — ALT_BAGLI halleri ve M-UST-REAL bu platformda sayilmaz)")
        mevcut = [x for x in HALLER if haller.get(x)]
        for hal in mevcut:
            rc, s21, s9 = g[hal]
            print("  %-20s exit %s · H21: %s" % (hal, rc, (s21[0][:88] if s21 else "(satir yok)")))
            print("  %-20s          H9 : %s" % ("", (s9[0][:88] if s9 else "(satir yok)")))
        temiz = ihlaller(g, haller)
        print("  SAGLAM MOTOR (%d hal)            %s" % (len(mevcut), "YESIL" if not temiz else "KIRMIZI"))
        for hal, kat, m in temiz:
            print("      ! %-20s [%s] %s" % (hal, kat, m[:170]))
        if temiz:
            print(CIZGI)
            print("SONUC: KIRMIZI — saglam motor kapiyi gecemedi.")
            return 1
        mt = _UYARI.match(g["IZLENMEYEN"][1][0]) if len(g["IZLENMEYEN"][1]) == 1 else None
        t_ref = int(mt.group("t")) if mt else None
        isirdi, kacti, olculemedi, atlandi = [], [], [], []
        sinif_olcum = {x: git_cumlesi(ortam, haller[x][0]) for x in SINIF_ADAYLARI if haller.get(x)}
        sinif_halleri = [x for x, c in sinif_olcum.items() if "not a git repository" in c.lower() and "dubious ownership" not in c]
        for x, c in sinif_olcum.items():
            print("  (M-OKU-SINIF kancasi %-12s git: %s%s)" % (x, c[:96], "" if x in sinif_halleri else "  => bu platformda `not a git repository` DEGIL, kanca disi"))
        liste = mutantlar(haller, sinif_halleri)
        for ad, aciklama, beklenen, gerek, degisim in liste:
            if gerek == "sinif" and not beklenen:
                olculemedi.append(ad)
                print("  ?  %-46s OLCULEMEDI  (platform: git `not a git repository` dalini hicbir halde uretmiyor — %s)" % (ad, " · ".join("%s: %s" % (x, sinif_olcum[x]) for x in SINIF_ADAYLARI)))
                continue
            if gerek == "baglanti" and not haller.get("ALT_BAGLI"):
                atlandi.append(ad)
                print("  -  %-46s ATLANDI     (sembolik bag kurulamadi)" % ad)
                continue
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisim, d)
                ih = ihlaller(gozle(sab, haller, ortam, bos_yol), haller, t_ref)
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-46s OLCULEMEDI  %s" % (ad, e))
                continue
            cift = {(h, k) for h, k, _ in ih}
            if cift == beklenen:
                isirdi.append(ad)
                print("  +  %-46s ISIRDI      yalniz kendi dali: %s" % (ad, ",".join("%s[%s]" % x for x in sorted(beklenen))))
            elif cift:
                kacti.append(ad)
                print("  !  %-46s YANLIS SEBEP/TASMA  kirilan: %s · beklenen: %s  (EXIT = motor cokmus olabilir)"
                      % (ad, ",".join("%s[%s]" % x for x in sorted(cift)), ",".join("%s[%s]" % x for x in sorted(beklenen))))
            else:
                kacti.append(ad)
                print("  !  %-46s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
            sys.stdout.flush()
    finally:
        _agaci_sil(taban)
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi - %d atlandi (toplam %d)" % (len(isirdi), len(kacti), len(olculemedi), len(atlandi), len(liste)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN/TASAN mutant = bu kapinin KOR ya da ORTUSEN oldugu yapi.")
        return 1
    print("  Saglam motor YESIL, %d sabotajin hepsi YALNIZ KENDI dalinda KIRMIZI%s: H21 hicbir dalda sessiz degil, H9 ayri cumleler."
          % (len(isirdi), (" (%d ATLANDI)" % len(atlandi)) if atlandi else ""))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

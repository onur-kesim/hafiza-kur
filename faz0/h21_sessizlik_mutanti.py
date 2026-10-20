#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H21 SESSIZLIK MUTANTI — `kapi` H21 hicbir dalda SESSIZ mi kaliyor, ve H9 alt dizini/depoyu "git YOK" diye yanlis mi teshis ediyor?
(besli-paket/IS_EMRI_H21_SESSIZLIK.md KALEM 1+2, 20 Eki 2026; hukum sinifi UYARI = Onur kilidi 18 Eki 23:31 aynen, cikis kodu DEGISMEZ)

NEDEN VAR (OLCULDU, Cowork 20 Eki 2026, Windows 11, motor 3085c1a1)
  S1 proje bir deponun ALT dizininde: `kur` `alt\\.gitattributes` yazdi ama `kapi` H21 satiri YOK ve H9 "git YOK" diyor (git VAR, depo VAR: yanlis teshis,
  P-1 sinifi). S2 depo degil: H21 sessiz. S3 depo, henuz commit yok, muhurlu dosyalar izlenmiyor, `.gitattributes` kaldirilmis: H21 sessiz — `acik` suzgeci
  yalniz IZLENEN yollara bakiyordu, koruma yoklugu ilk commit'e kadar gizleniyordu.

SECIM (rapora gerekce): alt dizinde `check-attr` GERCEKTEN OLCULUR (isin tercihi). Neden: motor `git -C <kok> check-attr/ls-files` ile kok'e GORELI
  yollar sorar; git ust deponun `.gitattributes`ini de hesaba katar; ikinci klon ust deponun klonudur ve `alt/.gitattributes` orada gecerlidir. OLCULEMEDI
  satiri cevabi ayni olurdu ama OLCULEBILEN seyi olcmemek olurdu.

NE OLCER — yedi HAL, her biri `kapi` ciktisindaki H21 ve H9 satirlariyla ve cikis koduyla yargilanir:
    ALT_KORUMALI   deponun alt dizininde proje, `kur` + commit              -> H21 SATIRI YOK (koruma OLCULDU, var); H9 "git deposunun KOKU degil (ust depo: ...)"
    ALT_KORUMASIZ  ayni, `alt/.gitattributes` kaldirilmis + commit (S1)     -> TEK `· H21: satir sonu cevrimi ... bozabilir (alt dizin: ust depo ...)`; H9 KOKU degil
    ALT_UST_KORUMA ayni, ust depoda `* -text`, alt'ta yok                   -> H21 SATIRI YOK (ust deponun korumasi SAYILIR); H9 KOKU degil
    DEPO_DEGIL     git deposu degil (S2)                                    -> TEK `· H21: OLCULEMEDI (git deposu degil) ...`; H9 "bu dizin bir git deposu degil"
    IZLENMEYEN     depo, hic commit yok, koruma yok, hicbir sey izlenmiyor (S3) -> TEK `· H21: ... izlenen 0, izlenmeyen N ...`; H9 "HENUZ COMMIT YOK" aynen
    BINARY_YOK     git programi PATH'te yok, `.git` yok                      -> TEK `· H21: OLCULEMEDI (git calistirilamiyor, .git yok)`; H9 "git YOK (git programi PATH'te bulunamadi)"
    KOK_KORUMALI   kok depo, `kur` + commit (REFERANS)                      -> H21 SATIRI YOK; H9 "git var"
  HER halde cikis kodu 0 (UYARI exit'i degistirmez). SAGLAM motorda hepsi YESIL; asagidaki alti sabotajin HER BIRI YALNIZ KENDI dalini bozar
  (kirilan hal kumesi hedefe TAM ESIT; kategori H21/H9 dogru; motoru COKERTEN sabotaj ISIRDI sayilmaz):
    M-S1   ALT DIZIN SESSIZE DONER        alt dizin dalinda olcum yapilmaz                  -> ALT_KORUMASIZ (H21)
    M-S2   DEPO-DEGIL SESSIZE DONER       depo degilse OLCULEMEDI satiri basilmaz          -> DEPO_DEGIL (H21)
    M-S3   IZLENME SUZGECI GERI GELIR     izlenmeyen yollar sayilmaz                        -> IZLENMEYEN (H21)
    M-H9alt  ALT DIZIN ESKI CUMLEYE       kok degil dali "H9: git YOK" der                  -> ALT_* (H9)
    M-H9depo DEPO YOK ESKI CUMLEYE        depo yok dali "H9: git YOK" der                   -> DEPO_DEGIL (H9)
    M-H9bin  BINARY YOK DEPO CUMLESINE    binary yok dali "depo degil" der                  -> BINARY_YOK (H9)

NE OLCMEZ
  `git` yanitsiz (dubious ownership vb.) dali: H21 `OLCULEMEDI (git deposu OKUNAMADI: ...)`, H9 `git deposu OKUNAMADI: ...` — halin kurulumu platforma bagli,
  burada OLCULMEZ (h9_kesme_mutanti H9 OKUNAMADI metnini zaten sinar). Saglam durumda H21'in pozitif satiri YOKTUR (korumali = sessiz): korumasiz
  OLCULEN durum uyarilir, korumali durum gurultu uretmez (KORUMALI/ALT_KORUMALI/ALT_UST_KORUMA/KOK_KORUMALI halleri bunu sabitler).

KULLANIM    python3 faz0/h21_sessizlik_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve alti mutantin HEPSI kendi halinde KIRMIZI yakti · 1 saglam kirmizi/mutant KACTI ya da yanlis sebeple yakti · 2 OLCULEMEDI
"""
import os
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
HALLER = ["ALT_KORUMALI", "ALT_KORUMASIZ", "ALT_UST_KORUMA", "DEPO_DEGIL", "IZLENMEYEN", "BINARY_YOK", "KOK_KORUMALI"]
ALT_HALLER = {"ALT_KORUMALI", "ALT_KORUMASIZ", "ALT_UST_KORUMA"}


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


def alt_dizin_projesi(motor, taban, ortam, ad, ust_ga=None, ga_sil=False):
    """Deponun ALT dizininde proje: -> alt kok. `ust_ga` verilirse ust deponun `.gitattributes`i."""
    repo = os.path.join(taban, ad)
    alt = os.path.join(repo, "alt")
    os.makedirs(alt)
    git(ortam, repo, "init", "-q")
    if ust_ga is not None:
        with open(os.path.join(repo, ".gitattributes"), "w", encoding="utf-8", newline="\n") as f:
            f.write(ust_ga)
    kur(motor, ortam, alt, ga_sil=ga_sil)
    komitle(ortam, repo)
    return alt


def gozle(motor, taban):
    """-> {hal: (exit, [H21 satirlari], [H9 satirlari])} — halleri kurar, `kapi` kosar."""
    os.makedirs(taban, exist_ok=True)
    ortam = git_ortami(taban)
    kokler = {}
    kokler["ALT_KORUMALI"] = alt_dizin_projesi(motor, taban, ortam, "alt_korumali")
    kokler["ALT_KORUMASIZ"] = alt_dizin_projesi(motor, taban, ortam, "alt_korumasiz", ga_sil=True)
    kokler["ALT_UST_KORUMA"] = alt_dizin_projesi(motor, taban, ortam, "alt_ust", ust_ga="* -text\n", ga_sil=True)
    k = os.path.join(taban, "depo_degil")
    os.makedirs(k)
    kur(motor, ortam, k)
    kokler["DEPO_DEGIL"] = k
    k = os.path.join(taban, "izlenmeyen")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k, ga_sil=True)                      # hicbir sey izlenmiyor, koruma yok
    kokler["IZLENMEYEN"] = k
    k = os.path.join(taban, "binary_yok")
    os.makedirs(k)
    kur(motor, ortam, k)
    kokler["BINARY_YOK"] = k
    k = os.path.join(taban, "kok")
    os.makedirs(k)
    git(ortam, k, "init", "-q")
    kur(motor, ortam, k)
    komitle(ortam, k)
    kokler["KOK_KORUMALI"] = k
    bos_yol = os.path.join(taban, "bos-yol")
    os.makedirs(bos_yol, exist_ok=True)
    gozlem = {}
    for hal, kok in kokler.items():
        e = ortam
        if hal == "BINARY_YOK":                            # git calistirilamiyor: PATH git'siz bir dizine cevrilir
            e = dict(ortam, PATH=bos_yol)
        rc, c = kos(motor, ["kapi"], kok, e)
        satirlar = [x.strip() for x in c.split("\n")]
        gozlem[hal] = (rc,
                       [x for x in satirlar if "H21" in x],
                       [x for x in satirlar if x.startswith(("? H9", "· H9"))])
    return gozlem


def ihlaller(g):
    """-> [(hal, kategori, mesaj)] — bos liste = YESIL. kategori: EXIT · H21 · H9. Saglam/sabotajli motor AYNI fonksiyonla yargilanir."""
    out = []
    for hal in HALLER:
        rc, s21, s9 = g[hal]
        if rc != 0:
            out.append((hal, "EXIT", "kapi exit %s (UYARI/OLCULEMEDI exit'i DEGISTIRMEZ; 0 beklenir)" % rc))
    for hal in ("ALT_KORUMALI", "ALT_UST_KORUMA", "KOK_KORUMALI"):
        if g[hal][1]:
            out.append((hal, "H21", "koruma OLCULDU ve VAR ama H21 satiri basildi: %r" % g[hal][1]))
    s = g["ALT_KORUMASIZ"][1]
    if len(s) != 1 or not s[0].startswith("· H21: satir sonu cevrimi muhurlu dosyayi bozabilir (alt dizin: ust depo "):
        out.append(("ALT_KORUMASIZ", "H21", "TEK `· H21: ... bozabilir (alt dizin: ust depo ...)` beklenir (alt dizinde OLCUM): %r" % s))
    s = g["DEPO_DEGIL"][1]
    if s != ["· H21: OLCULEMEDI (git deposu degil) — satir sonu korumasi olculemedi"]:
        out.append(("DEPO_DEGIL", "H21", "TEK `· H21: OLCULEMEDI (git deposu degil) ...` beklenir: %r" % s))
    s = g["IZLENMEYEN"][1]
    if len(s) != 1 or not s[0].startswith("· H21: satir sonu cevrimi muhurlu dosyayi bozabilir") or "izlenen 0, izlenmeyen" not in s[0]:
        out.append(("IZLENMEYEN", "H21", "TEK `· H21: ... izlenen 0, izlenmeyen N ...` beklenir (izlenme sarti YOK): %r" % s))
    s = g["BINARY_YOK"][1]
    if s != ["· H21: OLCULEMEDI (git calistirilamiyor, .git yok) — satir sonu korumasi olculemedi"]:
        out.append(("BINARY_YOK", "H21", "TEK `· H21: OLCULEMEDI (git calistirilamiyor, .git yok) ...` beklenir: %r" % s))
    beklenen9 = {
        "ALT_KORUMALI": "? H9: git deposunun KOKU degil (ust depo: ",
        "ALT_KORUMASIZ": "? H9: git deposunun KOKU degil (ust depo: ",
        "ALT_UST_KORUMA": "? H9: git deposunun KOKU degil (ust depo: ",
        "DEPO_DEGIL": "? H9: bu dizin bir git deposu degil (ust dizinlerde de yok)",
        "IZLENMEYEN": "? H9: git deposu var ama HENUZ COMMIT YOK",
        "BINARY_YOK": "? H9: git YOK (git programi PATH'te bulunamadi)",
        "KOK_KORUMALI": "· H9: git var",
    }
    for hal, onek in beklenen9.items():
        s9 = g[hal][2]
        if len(s9) != 1 or not s9[0].startswith(onek):
            out.append((hal, "H9", "H9 satiri %r ile baslamali: %r" % (onek, s9)))
    return out


# ad, aciklama, hedef hal(ler), kategori, [(eski, yeni)]. `eski` motorda TAM 1 kez gecmelidir.
MUTANTLAR = [
    ("M-S1 ALT DIZIN SESSIZE DONER", "alt dizin dalinda olcum yapilmaz", {"ALT_KORUMASIZ"}, "H21",
     [("        return True, \" (alt dizin: ust depo %s)\" % ayr\n", "        return False, \"\"   # MUTANT\n")]),
    ("M-S2 DEPO-DEGIL SESSIZE DONER", "depo degilse OLCULEMEDI satiri basilmaz", {"DEPO_DEGIL"}, "H21",
     [("        N.append(\"H21: OLCULEMEDI (git deposu degil)", "        _x = (\"H21: OLCULEMEDI (git deposu degil)")]),
    ("M-S3 IZLENME SUZGECI GERI GELIR", "izlenmeyen yollar sayilmaz (koruma yoklugu ilk commit'e kadar gizlenir)", {"IZLENMEYEN"}, "H21",
     [("    var = [p for p in yollar if p in izlenen or os.path.lexists(os.path.join(kok, p))]\n",
       "    var = [p for p in yollar if p in izlenen]   # MUTANT\n")]),
    ("M-H9alt ALT DIZIN ESKI CUMLEYE", "kok degil dali `H9: git YOK` der (yanlis teshis)", ALT_HALLER, "H9",
     [("        return \"H9: git deposunun KOKU degil (ust depo: %s)%s\" % (ayr, _H9_SONEK)\n",
       "        return \"H9: git YOK\" + _H9_SONEK   # MUTANT\n")]),
    ("M-H9depo DEPO YOK ESKI CUMLEYE", "depo yok dali `H9: git YOK` der (yanlis teshis)", {"DEPO_DEGIL"}, "H9",
     [("        return \"H9: bu dizin bir git deposu degil (ust dizinlerde de yok)\" + _H9_SONEK\n",
       "        return \"H9: git YOK\" + _H9_SONEK   # MUTANT\n")]),
    ("M-H9bin BINARY YOK DEPO CUMLESINE", "binary yok dali `depo degil` der (ayrim kaybolur)", {"BINARY_YOK"}, "H9",
     [("    return \"H9: git YOK%s%s\" % (\" (git programi PATH'te bulunamadi)\" if hal == \"BINARY_YOK\" else \"\", _H9_SONEK)\n",
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
    print("H21 SESSIZLIK MUTANTI — H21 hicbir dalda sessiz degil, H9 uc ayri cumle · platform: %s" % sys.platform)
    print("motor: %s" % motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="h21s_")
    try:
        try:
            g = gozle(motor, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        for hal in HALLER:
            rc, s21, s9 = g[hal]
            print("  %-15s exit %s · H21: %s" % (hal, rc, (s21[0][:96] if s21 else "(satir yok)")))
            print("  %-15s          H9 : %s" % ("", (s9[0][:96] if s9 else "(satir yok)")))
        temiz = ihlaller(g)
        print("  SAGLAM MOTOR (%d hal)            %s" % (len(HALLER), "YESIL" if not temiz else "KIRMIZI"))
        for hal, kat, m in temiz:
            print("      ! %-15s [%s] %s" % (hal, kat, m[:170]))
        if temiz:
            print(CIZGI)
            print("SONUC: KIRMIZI — saglam motor kapiyi gecemedi.")
            return 1
        isirdi, kacti, olculemedi = [], [], []
        for ad, aciklama, hedef, kategori, degisim in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisim, d)
                ih = ihlaller(gozle(sab, os.path.join(d, "hal")))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-36s OLCULEMEDI  %s" % (ad, e))
                continue
            cift = {(h, k) for h, k, _ in ih}
            beklenen = {(h, kategori) for h in hedef}
            if cift == beklenen:
                isirdi.append(ad)
                print("  +  %-36s ISIRDI      yalniz kendi dali: %s [%s]" % (ad, ",".join(sorted(hedef)), kategori))
            elif cift:
                kacti.append(ad)
                print("  !  %-36s YANLIS SEBEP/TASMA  kirilan: %s · beklenen: %s [%s]  (EXIT = motor cokmus olabilir)"
                      % (ad, ",".join("%s[%s]" % x for x in sorted(cift)), ",".join(sorted(hedef)), kategori))
            else:
                kacti.append(ad)
                print("  !  %-36s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
            sys.stdout.flush()
    finally:
        _agaci_sil(taban)
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)" % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN/TASAN mutant = bu kapinin KOR ya da ORTUSEN oldugu yapi.")
        return 1
    print("  Saglam motor YESIL, alti sabotajin hepsi YALNIZ KENDI dalinda KIRMIZI: H21 hicbir dalda sessiz degil, H9 uc ayri cumle.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

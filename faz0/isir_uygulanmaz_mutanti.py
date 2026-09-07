#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — isir UYGULANMAZ MUTANTI (KALEM 1, besli-paket/IS_EMRI_UYGULANMAZ.md).

NEDEN VAR (olculdu 7 Eyl 2026, A/B kontrolu: `64940f26` vs `fe01df60`,
besli-paket/OLCUM_RAPORU_7EYL_ISIR_GIT.md)
  `t_y42`'nin proje fabrikasi `yeni()` `git init` YAPMIYOR. Onceki turde (`isir`e
  `mutant_git` kolu eklenirken) git'siz projede M-H12g/M-H14g KURULAMIYORDU ve
  bu, mevcut `kurulamayan`/SINANMADI mekanizmasina dusuyordu — dogru gorunen ama
  YAN ETKISI OLCULMEMIS bir uygulama: git'i OLMAYAN HER projede `isir` artik 0
  donduremiyordu (`t_y42` 58/58 -> 56 gecti, 2 kaldi REGRESYONU; `readme_mutanti`
  bunu CI'da yakalardi).

  Duzeltme (IS_EMRI_UYGULANMAZ.md KALEM 1): YENI bir sinif — UYGULANMAZ.
  `mutant_git`, PROJEDE git OLMADIGI icin bir kolu kuramiyorsa `MutantUygulanmaz`
  firlatir; bu SINANMADI DEGILDIR — kapi korlugu da degildir, olcum ekseni bu
  projede yoktur. Cikis kodunu ETKILEMEZ, "kosulan mutant" sayisina GIRMEZ. Git
  VARKEN kurulum yine de bozulursa (ör. `.git` bozuk/gecersiz) davranis
  DEGISMEDI: SINANMADI + exit 2 BIREBIR korunur — UYGULANMAZ bir KACIS KAPISI
  DEGILDIR.

NE OLCER — DORT KOL
  KOL 1 (POZITIF KONTROL) — git'SIZ proje: kur->not->derle->isir -> exit 0,
      ciktida 'UYGULANMAZ' satiri VAR (M-H12g/M-H14g), SINANMADI sayisi bu iki
      kolu ICERMEZ (0).
  KOL 2 (GIT'Li KORUNUR) — AYNI akis git'Li bir projede -> 38/38 exit 0,
      M-H12g VE M-H14g ISIRDI.
  KOL 3 (SINANMADI KORUNUR) — git VAR (`.git` dizin olarak MEVCUT) ama GERCEK
      BIR DEPO DEGIL (bos dizin, ne HEAD ne objects/refs) -> `_git_kokte_mi`
      yine de True doner (doktrin: "icerigi COP ise bile True doner") ama
      gercek git komutlari (add/commit) BASARISIZ olur -> SINANMADI (>=2) +
      exit 2. UYGULANMAZ burada bir KACIS KAPISI OLMAMALI.
  KOL 4 (MUTANT) — UYGULANMAZ/SINANMADI ayrimi KAYNAKTAN sokulur (UYGULANMAZ
      da `kurulamayan`'a duser) -> KOL 1'in POZITIF KONTROLU (git'siz proje)
      artik exit 2 basar -> ISIRDI (kapinin var olmasi, ayrimin GERCEKTEN
      olculdugunun kanitidir).

CIKIS KODU  0 uc kol da temiz VE mutant ISIRDI · 1 en az bir kol BEKLENMEDIK
            / mutant KACTI · 2 OLCULEMEDI (git yok, motor okunamadi, kurulum
            basarisiz — kapi hukmu DEGIL)
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def kos(motor, arglar, kok, timeout=300):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _kur_ve_derle(motor, kok):
    """kur -> not -> derle. Uc adim da git'e BAKMAZ; git'siz/git'li/bozuk-git
    projede AYNI sekilde calismalidir (bu fonksiyonun KENDI on-kosulu)."""
    for adim in (["kur", "--ad", "UYGMUT"],
                 ["not", "--konu=genel-durum", "--metin=isir uygulanmaz mutanti ilk kayit"],
                 ["derle"]):
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s basarisiz: %s" % (adim[0], c.strip().split("\n")[-1][:160]))


def hal_git_yok(motor, kok):
    os.makedirs(kok, exist_ok=True)
    _kur_ve_derle(motor, kok)
    return kok


def hal_git_li(motor, kok):
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run(["git", "init", "-q", kok], capture_output=True)
    if r.returncode != 0:
        raise Kurulamadi("git init basarisiz")
    _kur_ve_derle(motor, kok)
    return kok


def hal_git_bozuk(motor, kok):
    """`.git` bir DIZIN olarak VAR (`_git_kokte_mi` bu yuzden True doner — bu,
    doktrinin KENDISIDIR: 'icerigi cop ise bile True doner') ama HEAD/objects/
    refs YOK — gercek bir depo DEGIL. Gercek git komutlari (add/commit) exit
    128 ('fatal: not a git repository') ile basarisiz olur (elle dogrulandi)."""
    os.makedirs(os.path.join(kok, ".git"), exist_ok=True)
    _kur_ve_derle(motor, kok)
    return kok


_UYGULANMAZ_SATIR = re.compile(r"^\s*M-H1[24]g.*->\s*UYGULANMAZ", re.M)
_ISIRDI_H12G = re.compile(r"^\s*M-H12g.*->\s*ISIRDI", re.M)
_ISIRDI_H14G = re.compile(r"^\s*M-H14g.*->\s*ISIRDI", re.M)
_SINANMADI_SAYI = re.compile(r"·\s*(\d+)\s+SINANMADI")
_KOSULAN_ORAN = re.compile(r"(\d+)/(\d+) kosulan mutant ISIRIYOR")


def _kol_olc(motor, kurucu, taban_ad, taban):
    kok = os.path.join(taban, taban_ad)
    kok = kurucu(motor, kok)
    return kos(motor, ["isir"], kok)


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok (bu batarya git'e SORDURMAYI olcer).")
        return 2

    print(CIZGI)
    print("ISIR UYGULANMAZ MUTANTI (KALEM 1) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="isir_uygulanmaz_")
    try:
        bulgu = []

        # ---- KOL 1: POZITIF KONTROL (git YOK) ------------------------------
        try:
            k1, c1 = _kol_olc(yol, hal_git_yok, "h1_git_yok", taban)
        except Kurulamadi as e:
            print("  KOL 1 (git YOK)   OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 1 (git YOK)      : isir exit=%d" % k1)
        if k1 != 0:
            bulgu.append("KOL 1: isir exit %d (0 bekleniyordu)" % k1)
        if not _UYGULANMAZ_SATIR.search(c1):
            bulgu.append("KOL 1: 'M-H1?g ... UYGULANMAZ' satiri YOK")
        m = _SINANMADI_SAYI.search(c1)
        if not m or int(m.group(1)) != 0:
            bulgu.append("KOL 1: SINANMADI sayisi 0 degil (%s) — UYGULANMAZ SINANMADI'ya "
                         "sizmis olabilir" % (m.group(1) if m else "YOK"))

        # ---- KOL 2: GIT'Li KORUNUR ------------------------------------------
        try:
            k2, c2 = _kol_olc(yol, hal_git_li, "h2_git_li", taban)
        except Kurulamadi as e:
            print("  KOL 2 (git VAR)   OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 2 (git VAR)      : isir exit=%d" % k2)
        if k2 != 0:
            bulgu.append("KOL 2: isir exit %d (0 bekleniyordu)" % k2)
        m = _KOSULAN_ORAN.search(c2)
        if not m or m.group(1) != "38" or m.group(2) != "38":
            bulgu.append("KOL 2: '38/38 kosulan mutant' degil (%s)" % (m.group(0) if m else "YOK"))
        if not _ISIRDI_H12G.search(c2):
            bulgu.append("KOL 2: M-H12g ISIRDI degil")
        if not _ISIRDI_H14G.search(c2):
            bulgu.append("KOL 2: M-H14g ISIRDI degil")

        # ---- KOL 3: SINANMADI KORUNUR (git BOZUK) ---------------------------
        try:
            k3, c3 = _kol_olc(yol, hal_git_bozuk, "h3_git_bozuk", taban)
        except Kurulamadi as e:
            print("  KOL 3 (git BOZUK) OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 3 (git BOZUK)    : isir exit=%d" % k3)
        if k3 != 2:
            bulgu.append("KOL 3: isir exit %d (2 bekleniyordu — SINANMADI korunmali)" % k3)
        m = _SINANMADI_SAYI.search(c3)
        if not m or int(m.group(1)) < 2:
            bulgu.append("KOL 3: SINANMADI sayisi < 2 (%s) — UYGULANMAZ bir KACIS KAPISI "
                         "olmus olabilir" % (m.group(1) if m else "YOK"))
        if _UYGULANMAZ_SATIR.search(c3):
            bulgu.append("KOL 3: git BOZUKKEN yanlislikla UYGULANMAZ basildi (SINANMADI olmaliydi)")

        for x in bulgu:
            print("      ! %s" % x)
        if bulgu:
            print("\nSONUC: KIRMIZI — temiz surumun kollari BEKLENMEDIK.")
            return 1

        # ---- KOL 4: MUTANT ----------------------------------------------------
        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        ANKOR = "            uygulanmaz.append((ad, kapi, str(e)))\n"
        n = s.count(ANKOR)
        if n != 1:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: capa %d yerde "
                  "gecti (1 olmali): %r" % (n, ANKOR.strip()))
            return 2
        yeni = s.replace(ANKOR, "            kurulamayan.append((ad, kapi, str(e)))  "
                                "# MUTANT: ayrim sokuldu\n", 1)
        try:
            compile(yeni, "<mutant>", "exec")
        except SyntaxError as e:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: "
                  "sabotajli motor derlenmiyor: %s" % e)
            return 2
        mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
        mp = os.path.join(mdir, "hafiza.py")
        with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
            f.write(yeni)
        try:
            km, cm = _kol_olc(mp, hal_git_yok, "hm_git_yok", taban)
        except Kurulamadi as e:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: %s" % e)
            return 2
        if km == 2:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   -> ISIRDI ✓  "
                  "(git'siz proje sabotajli motorda exit %d verdi, KOL 1 artik KIRMIZI)" % km)
            print(CIZGI)
            print("SONUC: YESIL — dort kol da BEKLENDIGI GIBI, mutant AYRI eksende ISIRDI.")
            return 0
        print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   -> KACTI ✗  "
              "(ayrim sokulunce de exit %d kaldi — KOL 1 bunu HIC OLCMUYOR)" % km)
        print(CIZGI)
        print("SONUC: KAPI KOR — mutant beklendigi gibi olculmedi.")
        return 1
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

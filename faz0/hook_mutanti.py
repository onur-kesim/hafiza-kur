#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HOOK MUTANTI — `hafiza.py hook --kur` ile kurulan pre-commit, kapi KIRMIZI
iken commit'i GERCEKTEN durduruyor mu?
(besli-paket/IS_EMRI.md KALEM 5, Onur kilidi 6 Eylul 2026)

NEDEN VAR (BELGE-KOD CELISKISI, olculdu 6 Eylul 2026)
  `SKILL.md` §1 tablosu KAPILI kademe icin "Zorlayici: Otomatik kapi + git hook"
  diyordu; §9 "Git hook bunu kismen zorlar, tamamen degil" diye ekliyordu;
  `references/sablonlar.md` elle kurulacak bir `pre-commit` sablonu veriyordu.
  Ama MOTORDA hook ureten hicbir kod YOKTU — olculdu: `hafiza.py` icinde "hook"
  gecen satir sayisi SIFIR. Yani belge bir otomatiklestirme VAAT EDIYOR, kod
  VERMIYORDU. Bu deponun kendi kapaginda tekrar eden sinif: "belge de bir
  arayuzdur ve yalan soyleyebilir".

  🔴 KURARKEN DIKKAT EDILEN IKI SEY (ikisi de bu projenin OLCULMUS dersi):
   (a) `.git` DIZIN SANILMAZ. hooks dizini `git rev-parse --git-path hooks` ile
       GIT'IN KENDISINE sordurulur. worktree / `--separate-git-dir` / submodule
       calisma agacinda `.git` bir METIN DOSYASIDIR (4 Eyl 2026 gitfile
       korlugu) ve `core.hooksPath` yalniz bu yolla dogru cozulur.
   (b) VAR OLAN HOOK EZILMEZ. Baskasinin hook'unu sessizce degistirmek, aracin
       "hicbir satir silinmez, tasinir" ilkesiyle carpisir.

NE OLCER (BES KOL)
  Sabotaj, yazilan hook govdesindeki `exit 1`i `exit 0`a cevirir: hook KOSAR,
  kirmiziyi BASAR, ama commit'i DURDURMAZ — "gorunurde calisan, fiilen etkisiz
  koruma" sinifi. (chmod'u dusuren bir sabotaj SECILMEDI: executable biti
  Windows'ta anlamsizdir, o mutant platforma gore FARKLI sey olcerdi.)

  1. POZITIF KONTROL : sabotajSIZ hook + KIRMIZI kapi -> `git commit` REDDEDILIR.
  2. MUTANT          : sabotajLI hook + AYNI vaka -> commit GECER (⇒ ISIRDI).
  3. HOOK KORUNUR    : var olan hook uzerine `hook --kur` -> DURUR ve dosyanin
                       SHA'si DEGISMEZ (ezme yok).
  4. YANLIS-POZITIF  : sabotajSIZ hook + YESIL kapi -> commit GECER. Hook her
                       commit'i durdursaydi koruma degil kilit olurdu.
  5. GITFILE         : `--separate-git-dir` ile kurulmus agacta hook, git'in
                       BILDIRDIGI hooks dizinine yazilir (`.git` bir METIN
                       DOSYASI oldugu halde). Elle `.git/hooks` kuran bir arac
                       burada HIC CALISMAYAN bir yere yazar ve fark etmez.

  🔴 PLATFORM SINIRI: 1. kol POZITIF KONTROLDUR. Bir platformda `sh` hook'lari
  hic kosmuyorsa commit reddedilmez; bu bir KUSUR degil ORTAM sinirdir ve kol
  OLCULEMEDI doner (BEKLENMEDIK degil) — "olculemeyene temiz denmez, ama
  olculemedi de FAIL degildir". O halde 2. kol da OLCULEMEDI'ye duser: pozitif
  kontrolu olmayan bir mutant, kendi basina hukum veremez.

CIKIS KODLARI: 0 bes kol da beklendigi gibi · 1 BEKLENMEDIK · 2 OLCULEMEDI ·
3 ARAC KUSURU
"""
import hashlib
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

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []

_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="hk-mut", GIT_AUTHOR_EMAIL="hk-mut@example.invalid",
    GIT_COMMITTER_NAME="hk-mut", GIT_COMMITTER_EMAIL="hk-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")

_DUZELTILMIS = '''  echo "HAFIZA KAPISI KIRMIZI — commit durduruldu."
  exit 1
}'''
_SABOTAJLI = '''  echo "HAFIZA KAPISI KIRMIZI — commit durduruldu."
  exit 0
}'''


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


def _sabotajli_motor(hedef):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru("sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse "
                         "SABOTAJ DA DEGISMELIDIR (hafiza.py HOOK_GOVDESI)." % n)
    with open(hedef, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return hedef


def _kos(motor, arglar, saniye=180):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI"
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, **_GIT_ORTAM))
    if not kw.get("hosgor") and r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def _kum_havuzu(motor, kok, ayri_gitdir=None):
    os.makedirs(kok, exist_ok=True)
    if ayri_gitdir:
        os.makedirs(ayri_gitdir, exist_ok=True)
        r = subprocess.run(["git", "init", "-q", "--separate-git-dir", ayri_gitdir, kok],
                           capture_output=True, text=True,
                           env=dict(os.environ, **_GIT_ORTAM))
        if r.returncode != 0:
            raise AracKusuru("git init --separate-git-dir: " + (r.stderr or "")[:200])
    else:
        _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "HK", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "ilk")
    return kok


def _kapiyi_kirmizi_yap(kok):
    """Canli hafizadan BASELINE bir satir silinir -> [H1] KAYIP."""
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    L = open(p, encoding="utf-8", newline="").read().splitlines(True)
    for i, s in enumerate(L):
        g = s.strip()
        if g and not g.startswith("#") and not g.startswith(">") and len(g) > 12:
            del L[i]
            break
    else:
        raise AracKusuru("silinecek anlamli satir bulunamadi")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def _kapi_kirmizi_mi(motor, kok):
    rc, _, _ = _kos(motor, ["kapi", "--kok=" + kok])
    return rc not in (0, None)


def _commit_dene(kok):
    """Bir dosya degistirilir ve commit DENENIR. Doner: (kabul_edildi, cikti)"""
    with open(os.path.join(kok, "deneme.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write("satir\n")
    _git(kok, "add", "-A")
    rc, c = _git(kok, "commit", "-m", "hook denemesi", hosgor=True)
    return rc == 0, c


# ------------------------------------------------------------------ KOLLAR
def _kol_kirmizi(motor, kok, ad, durmasi_bekleniyor):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "hook kurulamadi: %s" % (c + e).strip()[:120])
    _kapiyi_kirmizi_yap(kok)
    if not _kapi_kirmizi_mi(motor, kok):
        return _kayit(ad, OLCULEMEDI, "kapi KIRMIZI yapilamadi (senaryo kurulamadi)")
    kabul, cikti = _commit_dene(kok)
    if durmasi_bekleniyor:
        if not kabul:
            return _kayit(ad, BEKLENDIGI_GIBI, "commit REDDEDILDI (hook calisti)")
        return _kayit(ad, OLCULEMEDI,
                      "commit GECTI — bu ortamda `sh` hook'lari kosmuyor olabilir "
                      "(PLATFORM SINIRI, kusur hukmu VERILMEZ)")
    if kabul:
        return _kayit(ad, BEKLENDIGI_GIBI, "commit GECTI (kusur geri geldi ⇒ ISIRDI)")
    _kayit(ad, BEKLENMEDIK, "commit REDDEDILDI — sabotaja ragmen durdu")


def _kol_hook_korunur(motor, kok, ad):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "ilk hook kurulamadi")
    m = re.search(r"HOOK KURULDU: (.+)", c)
    if not m:
        return _kayit(ad, OLCULEMEDI, "hook yolu ciktidan cozulemedi")
    hedef = m.group(1).strip()
    with open(hedef, "a", encoding="utf-8", newline="\n") as f:
        f.write("# kullanicinin kendi satiri\n")
    once = _sha(hedef)
    rc2, c2, e2 = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    sonra = _sha(hedef)
    if rc2 != 0 and once == sonra:
        return _kayit(ad, BEKLENDIGI_GIBI, "DURDU (exit=%s) ve dosya DEGISMEDI" % rc2)
    _kayit(ad, BEKLENMEDIK,
           "exit=%s, dosya %s" % (rc2, "DEGISMEDI" if once == sonra else "EZILDI"))


def _kol_yesil(motor, kok, ad):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "hook kurulamadi")
    if _kapi_kirmizi_mi(motor, kok):
        return _kayit(ad, OLCULEMEDI, "kapi ZATEN kirmizi — yesil kol kurulamadi")
    kabul, cikti = _commit_dene(kok)
    if kabul:
        return _kayit(ad, BEKLENDIGI_GIBI, "yesil kapida commit GECTI")
    _kayit(ad, BEKLENMEDIK, "yesil kapida commit REDDEDILDI: %s" % cikti.strip()[:120])


def _kol_gitfile(motor, kok, gitdir, ad):
    _kum_havuzu(motor, kok, ayri_gitdir=gitdir)
    if os.path.isdir(os.path.join(kok, ".git")):
        return _kayit(ad, OLCULEMEDI, ".git DIZIN cikti — gitfile senaryosu kurulamadi")
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, BEKLENMEDIK, "gitfile agacinda hook kurulamadi: %s"
                      % (c + e).strip()[:120])
    m = re.search(r"HOOK KURULDU: (.+)", c)
    hedef = m.group(1).strip() if m else ""
    gercek = os.path.realpath(os.path.join(gitdir, "hooks", "pre-commit"))
    if hedef and os.path.realpath(hedef) == gercek and os.path.isfile(gercek):
        return _kayit(ad, BEKLENDIGI_GIBI, "hook AYRI gitdir'e yazildi")
    _kayit(ad, BEKLENMEDIK, "hook %r yazildi, beklenen %r" % (hedef, gercek))


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    if not shutil.which("git"):
        print("ARAC KUSURU: git yok")
        return 3
    gecici = tempfile.mkdtemp(prefix="hkm_")
    try:
        try:
            sab = _sabotajli_motor(os.path.join(gecici, "sab.py"))
            _kol_kirmizi(MOTOR, os.path.join(gecici, "a"), "1. POZITIF KONTROL", True)
            _kol_kirmizi(sab, os.path.join(gecici, "b"), "2. MUTANT", False)
            _kol_hook_korunur(MOTOR, os.path.join(gecici, "c"), "3. HOOK KORUNUR")
            _kol_yesil(MOTOR, os.path.join(gecici, "d"), "4. YANLIS-POZITIF")
            _kol_gitfile(MOTOR, os.path.join(gecici, "e"),
                         os.path.join(gecici, "e_gitdir"), "5. GITFILE")
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    print("=" * 82)
    print("HOOK MUTANTI — kurulan pre-commit kirmizi kapida commit'i durduruyor mu?")
    print("=" * 82)
    for ad, durum, ayrinti in SONUC:
        print("  %-22s %-16s %s" % (ad, durum, ayrinti))
    print(CIZGI)
    bek = sum(1 for _, d, _ in SONUC if d == BEKLENDIGI_GIBI)
    print("SONUC: %d/%d kol BEKLENDIGI GIBI" % (bek, len(SONUC)))
    if any(d == BEKLENMEDIK for _, d, _ in SONUC):
        return 1
    if any(d == OLCULEMEDI for _, d, _ in SONUC):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

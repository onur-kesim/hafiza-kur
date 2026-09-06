#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KAPSAM ZORLA MUTANTI — `--kapsam-zorla`, OLCULEMEDI varken cikis kodunu
gercekten degistiriyor mu; ve varsayilan davranisi BOZMADAN mi yapiyor?
(besli-paket/IS_EMRI.md KALEM 3, Onur kilidi 6 Eylul 2026)

NEDEN VAR (6 Eylul 2026 — OLCULDU)
  `kapi`nin hukum sozlesmesi: 0 yesil · 1 kirmizi · 2 kullanim hatasi ·
  3 olcum yapilamadi. Ama `YESIL (SINIRLI)` — yani "olculen her sey gecti,
  N SEY OLCULMEDI" — **0** donuyordu. Bu BILINCLI bir karardi (`SKILL.md` §9:
  beyanli gevseklik kapiyi kirmizi yakmaz) ve sonucu da orada yaziliydi:
      "`kapi && dagit` diyen bir CI, kapsami eksik bir projede dagitim yapar."
  Yani belge tuzagi ITIRAF ediyordu ama araci veren YOKTU: kullanicinin
  kapsami zorlamak icin cikti metnindeki `?` satirlarini elle ayiklamasi
  gerekiyordu — bir CI adiminda kirilgan is.

  Duzeltme YONU onemli: kapi KATILASTIRILMADI. Kacis yolu olmayan kapi kirilan
  kapidir (`SKILL.md` §9). Bunun yerine kapsam CI'da ZORLANABILIR kilindi:
  varsayilan davranis BIREBIR ayni kalir, yalniz `--kapsam-zorla` verilirse
  `O` listesi doluyken cikis kodu **5** olur.

  🔴 5 secildi: 0/1/2/3 `kapi`de DOLU, 4 `isir`in "temiz surum zaten FAIL"i.
  Sozlesme KIRILMIYOR, yalniz GENISLIYOR — mevcut hicbir kodun anlami degismez.

NE OLCER (BES KOL)
  Sabotaj bayragi ETKISIZ kilar (`if getattr(a, "kapsam_zorla", False):` ->
  `if False:`): kusurun kendisi, yani "kapsam eksikligi cikis koduna YANSIMAZ".

  1. POZITIF KONTROL : sabotajSIZ motor + commit'siz depo (H9 `?` uretir) +
                       `--kapsam-zorla` -> exit **5**.
  2. MUTANT          : sabotajLI motor + AYNI vaka -> exit **0** (kusur geri
                       geldi ⇒ ISIRDI).
  3. VARSAYILAN      : sabotajSIZ motor + AYNI vaka, bayrak YOK -> exit **0**.
                       Bayragi olmayan kullanicinin davranisi DEGISMEMELIDIR;
                       degisirse bu bir sozlesme kirilmasidir (minor artmali).
  4. YANLIS-POZITIF  : sabotajSIZ motor + KAPSAMI TAM proje (commit yapilmis)
                       + `--kapsam-zorla` -> exit **0**. Bayrak her yerde 5
                       dondururse hicbir sey olcmez, yalniz gurultu uretir.
  5. BEYANLI GEVSEKLIK: `.hafizarc`ta `kural_isaretleri` BOSALTILIR ve
                       `politika_gerekce` ile BEYAN EDILIR (H15 bunu `O`ya
                       yazar), sonra `muhur`lenir -> `--kapsam-zorla` exit **5**.
                       Bu kol IS EMRININ olcut (d)'sidir: ayni bayrak beyanli
                       gevsekligi de CI'da kirmizi yakmali. Yakmiyorsa "kapsam
                       zorlama" adi YANLIStir — yalniz git kapsamini zorluyordur.

  Olculen: `kapi`nin EXIT KODU (bu kalemin sozlesmesi cikis kodudur) ve 5.
  kolda ayrica hukum satirinin H15 beyanini tasidigi. stdout/stderr AYRI.

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI (proje sozlesmesi)
  0  BES kolun BESI DE BEKLENDIGI GIBI
  1  en az bir kol BEKLENMEDIK
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU
"""
import json
import os
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
    GIT_AUTHOR_NAME="kz-mut", GIT_AUTHOR_EMAIL="kz-mut@example.invalid",
    GIT_COMMITTER_NAME="kz-mut", GIT_COMMITTER_EMAIL="kz-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ
_DUZELTILMIS = '''        if getattr(a, "kapsam_zorla", False):'''
_SABOTAJLI = '''        if False:'''


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ DA "
            "DEGISMELIDIR (hafiza.py cmd_kapi, --kapsam-zorla dali)." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=180):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git(kok, *args):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, **_GIT_ORTAM))
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


def _kum_havuzu(motor, kok, commitli=False):
    """KUM HAVUZU PAYLASILMAZ — her kol KENDI kokunu alir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "KZ", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    if commitli:
        _git(kok, "add", "-A")
        _git(kok, "commit", "-q", "-m", "ilk")
    return kok


def _gevseklik_beyan_et(motor, kok):
    """`kural_isaretleri` BOSALTILIR ve `politika_gerekce` ile BEYAN EDILIR.
    H15 bunu `O`ya yazar (gevseklik gizlenemez, ITIRAF EDILIR). `.hafizarc`
    zincire bagli oldugu icin degisiklik `muhur` ile beyan edilir."""
    p = os.path.join(kok, ".hafizarc")
    d = json.loads(open(p, encoding="utf-8").read())
    d["kural_isaretleri"] = []
    d["politika_gerekce"] = {
        "kural_isaretleri": "bu kum havuzunda H7 bilincli olarak kapatildi (olcum)"}
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    rc, c, e = _kos(motor, ["muhur", "--kok=" + kok, "politika gerekcesi yazildi"])
    if rc != 0:
        raise AracKusuru("muhur basarisiz (exit=%s): %s" % (rc, (c + e)[-200:]))


# ------------------------------------------------------------------ KOLLAR
def _kol(motor, kok, ad, arglar, bekle, commitli=False, gevsek=False,
         metin_bekle=None):
    _kum_havuzu(motor, kok, commitli=commitli)
    if gevsek:
        _gevseklik_beyan_et(motor, kok)
    rc, c, e = _kos(motor, ["kapi", "--kok=" + kok] + list(arglar))
    if rc is None:
        return _kayit(ad, OLCULEMEDI, e)
    if rc != bekle:
        return _kayit(ad, BEKLENMEDIK, "exit=%s, beklenen %s" % (rc, bekle))
    if metin_bekle and metin_bekle not in c:
        return _kayit(ad, BEKLENMEDIK,
                      "exit dogru (%s) ama hukumde %r YOK" % (rc, metin_bekle))
    return _kayit(ad, BEKLENDIGI_GIBI,
                  "exit=%s (beklenen)%s" % (rc, " · beyan hukumde" if metin_bekle else ""))


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    gecici = tempfile.mkdtemp(prefix="kzm_")
    try:
        try:
            sab = _sabotajli_motor(gecici)
            _kol(MOTOR, os.path.join(gecici, "a"), "1. POZITIF KONTROL",
                 ["--kapsam-zorla"], 5)
            _kol(sab, os.path.join(gecici, "b"), "2. MUTANT",
                 ["--kapsam-zorla"], 0)
            _kol(MOTOR, os.path.join(gecici, "c"), "3. VARSAYILAN KORUNDU",
                 [], 0)
            _kol(MOTOR, os.path.join(gecici, "d"), "4. YANLIS-POZITIF",
                 ["--kapsam-zorla"], 0, commitli=True)
            _kol(MOTOR, os.path.join(gecici, "e"), "5. BEYANLI GEVSEKLIK",
                 ["--kapsam-zorla"], 5, commitli=True, gevsek=True,
                 metin_bekle="BEYANLA GEVSETILDI")
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    print("=" * 82)
    print("KAPSAM ZORLA MUTANTI — --kapsam-zorla cikis kodunu gercekten degistiriyor mu?")
    print("=" * 82)
    for ad, durum, ayrinti in SONUC:
        print("  %-24s %-16s %s" % (ad, durum, ayrinti))
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

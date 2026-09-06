#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KUR KORUMA MUTANTI — `kur`, BASKA bir aracin defterini taniyip DURUYOR mu?
(besli-paket/IS_EMRI.md KALEM 2, Onur kilidi 6 Eylul 2026)

NEDEN VAR (6 Eylul 2026 — OLCULDU, ISIRDI)
  `SKILL.md` §2 su uyariyi tasiyordu:
      "⛔ Mevcut hafiza sistemi olan bir projede `kur` KOSMA. Olculdu: zinciri
       kirar, ikinci cipa dogurur..."
  Ama KOD bunu zorlamiyordu. Eski `_kur_on_kontrol` YALNIZ hafiza-kur'un KENDI
  v1 izlerini ariyordu (`arsiv/hafiza/` altinda `_KAYNAK*.md`, `_ZINCIR.jsonl`,
  `HAFIZA_*.md`, `_KOVA.json`) — BASKA aracin defterini HIC gormuyordu.

  OLCUM: taze bir git deposuna `CLAUDE.md` + `DURUM.md` konuldu ve `kur`
  kosuldu. Sonuc: UYARI YOK, exit 0, yeni canli hafiza acildi ⇒ IKINCI DEFTER.
  (`CLAUDE.md`'ye dokunulmadi — SHA ayni kaldi; yani VERI kaybi degil DUZEN
  kaybi. Ama Is-Portfolyo denetcisinin cumlesi tam bunun icindi: "dokunmamak
  yetmez; ayrismayi olcen bir kapi olmadan iki defter, bir hafta icinde iki
  farkli gercek uretir.")

  Duzeltme: `_kur_yabanci_defter_kontrolu` — `devral`in KENDI iki fonksiyonunu
  (`_devir_adaylari` + `devir_rolu`) yeniden kullanir; IKINCI BIR TANIMA TABLOSU
  YAZILMAZ (iki tablo zamanla birbirinden ayrisir). Kacis: `--yine-de`, ve
  gecis `_ZINCIR.jsonl` halkasinin GEREKCESINE duser — kapatilmaz, GIZLENEMEZ.

NE OLCER (BES KOL)
  Sabotaj taramayi ETKISIZ kilar (`for rel in _devir_adaylari(kok)` ->
  `for rel in []`): kusurun kendisi, yani "yabanci defter GORULMUYOR" hali.

  1. POZITIF KONTROL : sabotajSIZ motor + CLAUDE.md'li agac -> `kur` DURUR
                       (exit != 0) ve canli hafiza ACILMAZ.
  2. MUTANT          : sabotajLI motor + AYNI agac -> `kur` GECER ve canli
                       hafiza ACILIR (kusur GERI GELDI ⇒ ISIRDI).
  3. YANLIS-POZITIF  : sabotajSIZ motor + BOS agac -> `kur` CALISIR. Koruma
                       yalniz yabanci defter varken durmali; her yerde
                       durursa arac kullanilamaz hale gelir.
  4. KACIS + IZ      : sabotajSIZ motor + CLAUDE.md'li agac + `--yine-de` ->
                       `kur` CALISIR **ve** `_ZINCIR.jsonl`de gecisin gerekcesi
                       GORUNUR. Beyanli gevseklik kullanilabilir ama gizlenemez;
                       iz YOKSA doktrin ihlal edilmis olur.
  5. IDEMPOTENT      : ZATEN KURULU projede (`.hafizarc` var) `kur` tekrar
                       kosulur -> CALISIR. Kontrol orada kosmamali; kosarsa
                       kendi kurulumumuz ikinci kosumda kilitlenirdi.

  Olculen: `kur`un exit kodu + canli hafizanin VARLIGI + zincir gerekcesi.
  `stdout`/`stderr` AYRI borulardadir, BIRLESTIRILMEZ.

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI (proje sozlesmesi)
  0  BES kolun BESI DE BEKLENDIGI GIBI
  1  en az bir kol BEKLENMEDIK
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi)
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
    GIT_AUTHOR_NAME="kk-mut", GIT_AUTHOR_EMAIL="kk-mut@example.invalid",
    GIT_COMMITTER_NAME="kk-mut", GIT_COMMITTER_EMAIL="kk-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ
_DUZELTILMIS = """    taninan = []
    for rel in _devir_adaylari(kok):
        rol = devir_rolu(rel)"""
_SABOTAJLI = """    taninan = []
    for rel in []:
        rol = devir_rolu(rel)"""


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ DA "
            "DEGISMELIDIR (hafiza.py _kur_yabanci_defter_kontrolu)." % n)
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


def _agac(kok, yabanci=True):
    """KUM HAVUZU PAYLASILMAZ — her kol KENDI kokunu alir."""
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run(["git", "-C", kok, "init", "-q"], capture_output=True,
                       text=True, env=dict(os.environ, **_GIT_ORTAM))
    if r.returncode != 0:
        raise AracKusuru("git init: " + (r.stderr or "")[:200])
    if yabanci:
        with open(os.path.join(kok, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# Kurallar\n\nBu proje boyle calisir.\n")
        with open(os.path.join(kok, "DURUM.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# Durum\n\nAktif is: X\n")
    return kok


def _canli_var(kok):
    return os.path.isfile(os.path.join(kok, "PROJE_HAFIZA.md"))


def _zincir_gerekceleri(kok):
    p = os.path.join(kok, "arsiv", "hafiza", "_ZINCIR.jsonl")
    if not os.path.isfile(p):
        return []
    out = []
    for satir in open(p, encoding="utf-8"):
        satir = satir.strip()
        if not satir:
            continue
        try:
            d = json.loads(satir)
        except ValueError:
            continue
        yuk = d.get("yuk") or {}
        out.append(str(yuk.get("gerekce", d.get("gerekce", ""))))
    return out


# ------------------------------------------------------------------ KOLLAR
def _kol_durmali(motor, kok, ad):
    _agac(kok, yabanci=True)
    rc, c, e = _kos(motor, ["kur", "--ad", "KK", "--kok=" + kok])
    if rc is None:
        return _kayit(ad, OLCULEMEDI, e)
    if rc != 0 and not _canli_var(kok):
        return _kayit(ad, BEKLENDIGI_GIBI, "kur DURDU (exit=%s), canli hafiza ACILMADI" % rc)
    _kayit(ad, BEKLENMEDIK,
           "kur exit=%s, canli hafiza %s — koruma ISLEMEDI"
           % (rc, "VAR" if _canli_var(kok) else "yok"))


def _kol_gecmeli(motor, kok, ad, ek=(), iz_bekle=False):
    _agac(kok, yabanci=True)
    rc, c, e = _kos(motor, ["kur", "--ad", "KK", "--kok=" + kok] + list(ek))
    if rc is None:
        return _kayit(ad, OLCULEMEDI, e)
    if rc != 0 or not _canli_var(kok):
        return _kayit(ad, BEKLENMEDIK,
                      "kur exit=%s, canli hafiza %s — GECMESI bekleniyordu"
                      % (rc, "VAR" if _canli_var(kok) else "yok"))
    if not iz_bekle:
        return _kayit(ad, BEKLENDIGI_GIBI, "kur GECTI (kusur geri geldi ⇒ ISIRDI)")
    izler = [g for g in _zincir_gerekceleri(kok) if "--yine-de" in g]
    if izler:
        return _kayit(ad, BEKLENDIGI_GIBI, "kur GECTI ve zincirde IZ var: %s" % izler[0][:60])
    _kayit(ad, BEKLENMEDIK, "kur GECTI ama zincirde `--yine-de` izi YOK (gizlendi)")


def _kol_bos_agac(motor, kok, ad):
    _agac(kok, yabanci=False)
    rc, c, e = _kos(motor, ["kur", "--ad", "KK", "--kok=" + kok])
    if rc == 0 and _canli_var(kok):
        return _kayit(ad, BEKLENDIGI_GIBI, "bos agacta kur CALISTI (yanlis-pozitif yok)")
    _kayit(ad, BEKLENMEDIK, "bos agacta kur exit=%s — koruma FAZLA GENIS" % rc)


def _kol_idempotent(motor, kok, ad):
    _agac(kok, yabanci=False)
    rc1, _, _ = _kos(motor, ["kur", "--ad", "KK", "--kok=" + kok])
    if rc1 != 0:
        return _kayit(ad, OLCULEMEDI, "ilk kur basarisiz (exit=%s)" % rc1)
    # kurulumdan SONRA yabanci defter EKLENIR: kontrol yine de kosmamali,
    # cunku .hafizarc var ve `kur` orada IDEMPOTENT TAZELEMEDIR.
    with open(os.path.join(kok, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# Kurallar\n")
    rc2, c, e = _kos(motor, ["kur", "--ad", "KK", "--kok=" + kok])
    if rc2 == 0:
        return _kayit(ad, BEKLENDIGI_GIBI, "kurulu projede kur TEKRAR calisti (exit=0)")
    _kayit(ad, BEKLENMEDIK,
           "kurulu projede kur exit=%s — idempotent tazeleme KILITLENDI: %s"
           % (rc2, (c + e).strip()[:120]))


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    gecici = tempfile.mkdtemp(prefix="kkm_")
    try:
        try:
            sab = _sabotajli_motor(gecici)
            _kol_durmali(MOTOR, os.path.join(gecici, "a"), "1. POZITIF KONTROL")
            _kol_gecmeli(sab, os.path.join(gecici, "b"), "2. MUTANT")
            _kol_bos_agac(MOTOR, os.path.join(gecici, "c"), "3. YANLIS-POZITIF")
            _kol_gecmeli(MOTOR, os.path.join(gecici, "d"), "4. KACIS + IZ",
                         ek=["--yine-de"], iz_bekle=True)
            _kol_idempotent(MOTOR, os.path.join(gecici, "e"), "5. IDEMPOTENT")
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    print("=" * 82)
    print("KUR KORUMA MUTANTI — yabanci defter varken `kur` duruyor mu?")
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

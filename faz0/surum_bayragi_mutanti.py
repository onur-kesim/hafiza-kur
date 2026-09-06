#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SURUM BAYRAGI MUTANTI — `hafiza.py surum` gercekten MOTORDAN mi okuyor,
yoksa bir yerde SABITLENMIS bir sayi mi basiyor?
(besli-paket/IS_EMRI.md KALEM 4, Onur kilidi 6 Eylul 2026)

NEDEN VAR
  `SKILL.md` §8 bu eksigi kendisi yazmisti: "Motorun surumunu soran bir bayrak
  henuz yok — bu bir eksiktir, olculdu." Ayni bolum sunu da soyluyordu:
  "Surum, satir sayisi ve SHA buraya YAZILMAZ — bayatlar. Bir kez yazildi ve
  bayatladi; kimse olcmedigi icin IKI SURUM boyunca gorulmedi."

  ⇒ Bu komutun TEK degeri, sayiyi BELGEDEN degil ARTEFAKTTAN uretmesidir. Eger
  bir gun cikti motordan KOPARSA (elle yazilmis bir sayiya donerse) komut,
  kapatmak icin var oldugu kusurun TA KENDISI olur: guven veren ama bayat bir
  sayi. Bu mutant tam o kopmayi olcer.

NE OLCER (DORT KOL — iki AYRI eksen, her eksende pozitif kontrol + mutant)
  EKSEN A (surum): sabotaj `print("hafiza.py %s" % SURUM)` satirini SABIT bir
  dizeye cevirir — cikti motordaki `SURUM` sabitinden KOPAR.
  EKSEN B (sha):   sabotaj `sha_dosya(os.path.abspath(__file__))` cagrisini
  SABIT bir dizeye cevirir — cikti dosyanin GERCEK icerigininden KOPAR.

  1. A-POZITIF : sabotajSIZ motorun bastigi surum, motor DOSYASINDAN regex ile
                 okunan `SURUM` sabitiyle BIREBIR AYNI.
  2. A-MUTANT  : sabotajLI motorda AYNI degil (kopus ⇒ ISIRDI).
  3. B-POZITIF : sabotajSIZ motorun bastigi sha256, o dosyanin `hashlib` ile
                 BAGIMSIZ hesaplanan sha256'siyla BIREBIR AYNI.
                 🔴 Bu bir CAPRAZ olcumdur: hesabi motorun kendi `sha_dosya`
                 fonksiyonu DEGIL, olcum araci yapar ("capa aracin kendi
                 ciktisindan guncellenmez" dersinin ayni kalibi).
  4. B-MUTANT  : sabotajLI motorda AYNI degil (kopus ⇒ ISIRDI).

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI: 0 dort kol da beklendigi gibi · 1 BEKLENMEDIK · 2 OLCULEMEDI ·
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

_A_DUZELTILMIS = '''    print("hafiza.py %s" % SURUM)'''
_A_SABOTAJLI = '''    print("hafiza.py 0.0.0-sabotaj")'''
_B_DUZELTILMIS = '''    print("sha256    %s" % sha_dosya(os.path.abspath(__file__)).upper())'''
_B_SABOTAJLI = '''    print("sha256    %s" % ("0" * 64))'''


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


def _sabotajli_motor(hedef, duzeltilmis, sabotajli, etiket):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(duzeltilmis)
    if n != 1:
        raise AracKusuru("%s sabotaj hedefi %d kez gecti (1 olmali). Motor "
                         "degistiyse SABOTAJ DA DEGISMELIDIR (hafiza.py cmd_surum)."
                         % (etiket, n))
    with open(hedef, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(duzeltilmis, sabotajli, 1))
    return hedef


def _kos(motor):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor, "surum"],
                           capture_output=True, timeout=60, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI"
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _surum_sabiti(yol):
    """Motor DOSYASINDAN okunur — motoru import ETMEDEN. Import etseydik
    olculen sey motorun kendi degeri olurdu, capraz olcum kaybolurdu."""
    m = re.search(r'^SURUM\s*=\s*"([^"]+)"', open(yol, encoding="utf-8").read(), re.M)
    if not m:
        raise AracKusuru("SURUM sabiti motorda bulunamadi: %s" % yol)
    return m.group(1)


def _sha_bagimsiz(yol):
    """BAGIMSIZ hesap: motorun `sha_dosya` fonksiyonu KULLANILMAZ."""
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for blok in iter(lambda: f.read(65536), b""):
            h.update(blok)
    return h.hexdigest().upper()


def _cikti_coz(c):
    surum = sha = None
    for satir in c.splitlines():
        p = satir.split(None, 1)
        if len(p) == 2 and p[0] == "hafiza.py":
            surum = p[1].strip()
        elif len(p) == 2 and p[0] == "sha256":
            sha = p[1].strip()
    return surum, sha


def _kol(motor, ad, eksen, esit_bekleniyor):
    rc, c, e = _kos(motor)
    if rc is None:
        return _kayit(ad, OLCULEMEDI, e)
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "surum exit=%s: %s" % (rc, (c + e)[-120:]))
    basilan_surum, basilan_sha = _cikti_coz(c)
    if eksen == "A":
        basilan, gercek = basilan_surum, _surum_sabiti(motor)
    else:
        basilan, gercek = basilan_sha, _sha_bagimsiz(motor)
    if basilan is None:
        return _kayit(ad, OLCULEMEDI, "cikti bicimi cozulemedi: %r" % c[:80])
    esit = (basilan == gercek)
    if esit == esit_bekleniyor:
        return _kayit(ad, BEKLENDIGI_GIBI,
                      "%s (beklenen)" % ("TUTUYOR" if esit else "KOPTU ⇒ ISIRDI"))
    _kayit(ad, BEKLENMEDIK, "basilan=%r gercek=%r" % (basilan, gercek[:24]))


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    gecici = tempfile.mkdtemp(prefix="sbm_")
    try:
        try:
            sab_a = _sabotajli_motor(os.path.join(gecici, "a.py"),
                                     _A_DUZELTILMIS, _A_SABOTAJLI, "EKSEN A")
            sab_b = _sabotajli_motor(os.path.join(gecici, "b.py"),
                                     _B_DUZELTILMIS, _B_SABOTAJLI, "EKSEN B")
            _kol(MOTOR, "1. A-POZITIF (surum)", "A", True)
            _kol(sab_a, "2. A-MUTANT  (surum)", "A", False)
            _kol(MOTOR, "3. B-POZITIF (sha)", "B", True)
            _kol(sab_b, "4. B-MUTANT  (sha)", "B", False)
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        shutil.rmtree(gecici, ignore_errors=True)

    print("=" * 82)
    print("SURUM BAYRAGI MUTANTI — `surum` motordan mi okuyor?")
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

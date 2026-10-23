#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SABLON GITSTATUS MUTANTI — `kur` ve `devral` KULLANICI projesinin canli dosyasina
"DEVRALAN MODELE ILK TALIMAT" olarak DUZ `git status` yaziyor mu?
(besli-paket/IS_EMRI_MOTOR_GITSTATUS.md KALEM 1, Onur kilidi 23 Eki 2026, sik A)

NEDEN VAR (OLCULDU)
  Baglı/paylasimli klasorde duz `git status` kalici `.git/index.lock` birakir (CLAUDE.md §4 mayini).
  `SAB_CANLI` sablonu (hafiza.py) bu komutu `kur`/`devral` ile HER yeni projenin canli dosyasina yaziyordu:
  mayin urun tarafindan yayiliyordu. SKILL belgeleri 069ba50'de duzeltilmisti, motor degil.
  Duzeltme: `git --no-optional-locks status --porcelain` (birebir lafiz; gerekce cumlesi EKLENMEZ).

NE OLCER (DORT KOL)
  Sabotaj sablon satirini DUZ `git status`a geri cevirir (kusurun kendisi).
  1. kur    · saglam motor  : canli dosyada `git --no-optional-locks status --porcelain` VAR, duz `git status` YOK.
  2. devral · saglam motor  : AYNI (SAB_CANLI'nin ikinci kullanim yolu).
  3. kur    · sabotajli     : saglam motorun kontrolu KIRMIZI olmali (ISIRDI).
  4. devral · sabotajli     : AYNI.
  Kol 1-2 bos gecmesin diye canli dosya BULUNMAZSA OLCULEMEDI (YESIL degil).

CIKIS KODLARI  0 dort kol beklendigi gibi · 1 BEKLENMEDIK (kacti / saglam kirmizi) · 2 OLCULEMEDI · 3 ARAC KUSURU
"""
import os
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82
DOGRU = "3. `git --no-optional-locks status --porcelain` temiz mi bak.\n"
ESKI = "3. `git status` temiz mi bak.\n"
BASLIK = "## DEVRALAN MODELE İLK TALİMAT"


class AracKusuru(Exception):
    pass


class Kurulamadi(Exception):
    pass


def _sabotajli_motor(hedef):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(DOGRU)
    if n != 1:
        raise AracKusuru("sabotaj hedefi %d kez gecti (1 olmali): motor degistiyse SABOTAJ DA DEGISMELIDIR" % n)
    p = os.path.join(hedef, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(DOGRU, ESKI, 1))
    return p


def _kos(motor, arglar, kok):
    o = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok], env=o, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *a):
    r = subprocess.run(["git", "-C", kok] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull))
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (a[0], (r.stderr or r.stdout).strip()[:140]))


def _canli_bul(kok):
    for yol, dizinler, dosyalar in os.walk(kok):
        dizinler[:] = [d for d in dizinler if d != ".git"]
        for f in dosyalar:
            if f.endswith(".md"):
                p = os.path.join(yol, f)
                with open(p, encoding="utf-8", errors="replace") as h:
                    if BASLIK in h.read():
                        return p
    return None


def _proje(motor, taban, ad, yol):
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if yol == "devral":
        with open(os.path.join(kok, "README.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# ornek\n")
        _git(kok, "init", "-q", ".")
        _git(kok, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "add", "-A")
        _git(kok, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "ilk")
        rc, c = _kos(motor, ["devral", "--esle", "canli=CANLI.md"], kok)
    else:
        rc, c = _kos(motor, ["kur", "--ad", "GS"], kok)
    if rc != 0:
        raise Kurulamadi("%s basarisiz (exit %d): %s" % (yol, rc, c.strip().split("\n")[-1][:140]))
    p = _canli_bul(kok)
    if not p:
        raise Kurulamadi("%s: canli dosya (%r basligi) BULUNAMADI — kontrol bos gecmesin" % (yol, BASLIK))
    return open(p, encoding="utf-8").read()


def _temiz_mi(icerik):
    """-> sorun listesi (bos = saglam)."""
    s = []
    if "3. `git --no-optional-locks status --porcelain` temiz mi bak." not in icerik:
        s.append("`--no-optional-locks status --porcelain` satiri YOK")
    if "`git status`" in icerik:
        s.append("DUZ `git status` var")
    return s


def main():
    taban = tempfile.mkdtemp(prefix="gsm_")
    sonuc = []
    try:
        try:
            os.makedirs(os.path.join(taban, "sab"))
            sab = _sabotajli_motor(os.path.join(taban, "sab"))
        except AracKusuru as e:
            print("ARAC KUSURU: %s" % e)
            return 3
        print(CIZGI)
        print("SABLON GITSTATUS MUTANTI — canli sablon duz `git status` yazmiyor · platform: %s" % sys.platform)
        print(CIZGI)
        for yol in ("kur", "devral"):
            for etiket, motor, beklenen_sorun in (("saglam", MOTOR, False), ("sabotajli", sab, True)):
                ad = "%s_%s" % (yol, etiket)
                try:
                    sorun = _temiz_mi(_proje(motor, taban, ad, yol))
                except Kurulamadi as e:
                    sonuc.append("OLCULEMEDI")
                    print("  ?  %-8s %-10s OLCULEMEDI  %s" % (yol, etiket, e))
                    continue
                if bool(sorun) == beklenen_sorun:
                    sonuc.append("TAMAM")
                    print("  +  %-8s %-10s %s" % (yol, etiket, ("ISIRDI: " + "; ".join(sorun)) if beklenen_sorun else "YESIL (satir dogru)"))
                else:
                    sonuc.append("BEKLENMEDIK")
                    print("  !  %-8s %-10s BEKLENMEDIK  %s" % (yol, etiket, ("KACTI: sabotajli motor kapiyi gecti") if beklenen_sorun else ("saglam motor KIRMIZI: " + "; ".join(sorun))))
        print(CIZGI)
        print("SONUC: %d tamam · %d beklenmedik · %d olculemedi (toplam %d)" % (sonuc.count("TAMAM"), sonuc.count("BEKLENMEDIK"), sonuc.count("OLCULEMEDI"), len(sonuc)))
        if "BEKLENMEDIK" in sonuc:
            return 1
        if "OLCULEMEDI" in sonuc:
            print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
            return 2
        print("  Saglam motor YESIL, sabotajli motor ISIRDI (kur + devral).")
        return 0
    finally:
        print("(taze gecici dizin: %s — SILINMEZ, iş emri KISIT: kendi betiklerinde silme yok)" % taban)


if __name__ == "__main__":
    sys.exit(main())

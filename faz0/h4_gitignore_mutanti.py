#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — H4 GITIGNORE MUTANTI (KALEM 2, besli-paket/IS_EMRI_DEVRAL.md).

NEDEN VAR (olculdu 6 Eyl 2026, Momentum kopyasi, git DAHIL)
  `_h4_havuz` git'in bildigini ELLE TAKLIT EDIYORDU: yalniz sabit
  `.git, node_modules, __pycache__, .venv` disliyordu. OLCULDU: `main.dart.js`
  agacta 7 yerde vardi ve H4 "OLU BAGLANTI — ayni adli baska dosya var ama yol
  tutmuyor" dedi; ama `.gitignore` okundugunda `.dart_tool/` VE derleme
  wwwroot'u ORADAYDI — yedi kopyanin YEDISI de git tarafindan yok sayiliyordu,
  hicbiri izlenmiyordu. Bu, kapali "gitfile korlugu"nun (`.git`i elle DIZIN
  sanmak) BIREBIR kardesi: cozum orada da burada da AYNI KALIP — "git'e sordur".

NE OLCER
  KAPI-A (POZITIF KONTROL + MUTANT EKSENI) — `.gitignore`'lu bir dizindeki
      kopya HAVUZA GIRMEZ: beyan edilen yol artik "hicbir yerde yok" (OLU,
      aciklamasiz), "yol tutmuyor" / "TASINMIS" DEGIL. Bu bir GEVSETME degil
      TERSINE DARALTMADIR (bulgu KAYBOLMUYOR, GEREKCESI dogruluyor).
  KAPI-B (GIT YOK KORUNUR) — git'siz agacta AYNI dizin duzeni eski (sabit
      liste) davranisini AYNEN uretir: kopya bulunur (TASINMIS/yol tutmuyor).
  KAPI-C (IZLENEN DOSYA KORUNUR) — `.gitignore`'da OLMAYAN, GERCEKTEN izlenen
      (commit'li) bir dosya havuzdan haric TUTULMAZ — kapi kor edilmiyor.

NE OLCMEZ
  KALEM 2-EK (beyan edilen yolun kendisi haric bir dizinde -> O/OLCULEMEDI)
  BURADA degil, `faz0/h4_bolme_mutanti.py`nin kapsadigi genel H4 kenarlarinin
  disinda AYRI bir eksen oldugu icin BU dosyada test EDILMEZ; o olcut kod
  incelemesiyle dogrulanir (bkz. IS_EMRI_DEVRAL.md KALEM 2-EK) ve mevcut H4
  bataryasindaki hicbir hali BOZMAZ (KALEM 0: additive).
  Performans (`check-ignore` toplu/tek surec) BURADA olculmez — davranissal
  DEGIL, uygulama detayidir; kod incelemesiyle dogrulanir.

CIKIS KODU  0 uc kapi da temiz VE mutant ISIRDI · 1 kapi kirmizi / mutant KACTI
            2 OLCULEMEDI (git yok, motor okunamadi, senaryo kurulamadi)
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

HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h4 gitignore mutanti icin ilk kayit"],
            ["derle"]]

_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="h4gitmut", GIT_AUTHOR_EMAIL="h4git@example.invalid",
                GIT_COMMITTER_NAME="h4gitmut", GIT_COMMITTER_EMAIL="h4git@example.invalid",
                GIT_CONFIG_NOSYSTEM="1")


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args):
    return subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                          env=_GIT_ENV, check=False)


def _commit_et(kok, mesaj="taban"):
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", mesaj)


def _dosya(kok, rel, icerik):
    p = os.path.join(kok, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(icerik)


def _ekle(kok, satirlar):
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write("\n" + "\n".join(satirlar) + "\n")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    if tip != "git_yok":
        subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H4GITMUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))

    if tip == "ignore_olu":
        # Momentum vakasinin KUCUK OLCEGI: '.dart_tool/'/wwwroot yerine 'build/'.
        # build/web/main.dart.js YOKSAYILIR (.gitignore); beyan `web/main.dart.js`
        # dizin BILESENI "web" ile ORTAK oldugu icin ESKI kodda TASINMIS/yol
        # tutmuyor sayilirdi — git'e sorulunca kopya havuza HIC GIRMEMELI.
        _dosya(kok, ".gitignore", "build/\n")
        _dosya(kok, "build/web/main.dart.js", "// derleme artefakti\n")
        _ekle(kok, ["Dosya: `web/main.dart.js`."])
    elif tip == "git_yok":
        # git init YOK (yukarida atlandi). Ayni dizin duzeni ama SABIT liste
        # 'build'u haric TUTMAZ -> kopya BULUNMALI (eski davranis BIREBIR).
        _dosya(kok, "build/web/main.dart.js", "// derleme artefakti\n")
        _ekle(kok, ["Dosya: `web/main.dart.js`."])
    elif tip == "izlenen":
        # .gitignore'da OLMAYAN, GERCEKTEN commit'li bir dosya: `arsiv/` altinda
        # oldugu icin zaten TASINMIS sayilir — git-yoksayma DEGISIKLIGI bunu
        # haric TUTMAMALI (kapi kor edilmiyor).
        _dosya(kok, "arsiv/belgeler/rapor.md", "# eski rapor\n")
        _commit_et(kok)
        _ekle(kok, ["Rapor burada: `belgeler/rapor.md`."])
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


HALLER = [
    ("h_ignore_olu", "ignore_olu"),
    ("h_git_yok", "git_yok"),
    ("h_izlenen", "izlenen"),
]


def haller_kur(motor_temiz, taban):
    return {ad: hal_kur(motor_temiz, ad, tip, taban) for ad, tip in HALLER}


def kume_olc(motor, kokler, hedef_taban):
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        rc, c = kos(motor, ["kapi"], kok)
        out[ad] = (rc, c)
    return out


def _h4_satiri(cikti):
    for d in [s.strip() for s in cikti.split("\n")]:
        if d.startswith("[H4]") or d[:12].find("H4:") >= 0:
            return d
    return None


def _siniflandirma(satir):
    if not satir:
        return "YOK"
    if "hicbir yerde yok" in satir:
        return "OLU_ACIKLAMASIZ"
    if "TASINMIS" in satir:
        return "TASINMIS"
    if "yol tutmuyor" in satir:
        return "YOL_TUTMUYOR"
    return "DIGER"


def hukum(motor, taban):
    """Uc hal icin (kod, H4 satiri, siniflandirma) doner. `taban` HER cagriya
    OZEL (mkdtemp) olmalidir — iki ayri motor (temiz/mutant) ayni dizin
    agacini PAYLASMAZ."""
    kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
    olcum = kume_olc(motor, kokler, os.path.join(taban, "olc"))
    out = {}
    for ad, tip in HALLER:
        kod, cikti = olcum[ad]
        satir = _h4_satiri(cikti)
        out[ad] = (kod, satir, _siniflandirma(satir))
    return out


# --------------------------------------------------------------------- MUTANT
# `_h4_havuz`in tek cagri yeri (`havuz = _h4_havuz(kok)`) ve imzasi
# (`_h4_havuz(kok)`) FAZ C bolme mutantlarinin (h4_bolme_mutanti.py,
# fazC_bolucu_h4.py) capasidir ve DEGISTIRILMEZ. KALEM 2'nin sorgusu
# `_h4_havuz` GOVDESI icindedir; mutant o govdedeki TEK satiri hedefler.
ANKOR = "    haric_git = _h4_git_yoksayilanlar(kok)\n"
YENI = "    haric_git = set()      # MUTANT: git'e hic sorulmuyor\n"


def sokulmus_motor(kaynak, hedef_dizin):
    n = kaynak.count(ANKOR)
    if n != 1:
        return None, "capa %d yerde gecti (1 olmali): %r" % (n, ANKOR.strip())
    metin = kaynak.replace(ANKOR, YENI, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(hedef_dizin, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p, None


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
    print("H4 GITIGNORE MUTANTI (KALEM 2) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h4_gitignore_")
    try:
        try:
            h = hukum(yol, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2

        b = []
        kod, satir, sinif = h["h_ignore_olu"]
        print("  KAPI-A .gitignore'lu kopya : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if kod == 0:
            b.append("KAPI-A: kapi YESIL — beklenen [H4] OLU bulgusu YOK")
        elif sinif != "OLU_ACIKLAMASIZ":
            b.append("KAPI-A: siniflandirma %r (beklenen OLU_ACIKLAMASIZ — 'hicbir yerde yok')" % sinif)

        kod, satir, sinif = h["h_git_yok"]
        print("  KAPI-B git yok             : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if sinif == "OLU_ACIKLAMASIZ":
            b.append("KAPI-B: git YOKKEN de 'hicbir yerde yok' — sabit liste davranisi BOZULDU")
        elif sinif not in ("TASINMIS", "YOL_TUTMUYOR"):
            b.append("KAPI-B: siniflandirma %r (beklenen TASINMIS/YOL_TUTMUYOR — eski davranis)" % sinif)

        kod, satir, sinif = h["h_izlenen"]
        print("  KAPI-C izlenen dosya       : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if sinif != "TASINMIS":
            b.append("KAPI-C: izlenen dosya TASINMIS bulunmadi (%r) — kapi KOR edilmis olabilir" % sinif)

        for x in b:
            print("      ! %s" % x)
        if b:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
        sab, hata = sokulmus_motor(s, mdir)
        if sab is None:
            print("  M-1 git sorgusu sokulur           OLCULEMEDI: %s" % hata)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        mh = hukum(sab, os.path.join(taban, "mutant"))
        mkod, msatir, msinif = mh["h_ignore_olu"]
        if msinif != "OLU_ACIKLAMASIZ":
            print("  M-1 git sorgusu sokulur           -> ISIRDI ✓  (kopya geri geldi: %s)"
                  % (msatir or "(H4 satiri YOK)"))
            print(CIZGI)
            print("SONUC: YESIL — kapilar temiz, mutant AYRI eksende ISIRDI.")
            return 0
        print("  M-1 git sorgusu sokulur           -> KACTI ✗  (sorgu sokulunce de ayni "
              "hukum cikti — kapi bunu HIC OLCMUYOR)")
        print(CIZGI)
        print("SONUC: KAPI KOR — mutant beklendigi gibi olculmedi.")
        return 1
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

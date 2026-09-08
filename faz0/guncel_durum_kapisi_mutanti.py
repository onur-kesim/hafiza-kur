#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — GUNCEL DURUM KAPISI MUTANTI (besli-paket/IS_EMRI_GUNCEL_DURUM_KAPISI.md).

NEDEN VAR (olculdu 8 Eyl 2026, besli-paket/OLCUM_RAPORU_8EYL_DENEME_KAPANIS.md,
Momentum kopyasinda GERCEKTEN OLCULDU)
  Momentum kopyasinda dort gercek `not` yazildi, dordu de exit 0 verdi ve
  "FRAGMAN: gunluk/...md" dedi. Ardindan `derle`:
      ATLANDI (bolum yok: ## GUNCEL DURUM): ...  (x4)
      DERLENDI: 0 fragman islendi ve arsive tasindi.
  `derle` exit 0. Ve `kapi`:
      SONUC: YESIL — olculen her sey gecti.        exit 0
  Kullanici dort not yazdi, arac "kaydedildi" dedi, hicbiri canli deftere
  girmedi, kapi "her sey gecti" dedi. Aracin var olma sebebi kayit tutmak.

  Kok sebep: `devral` `zorunlu_bolumler`i PROJEDE ONCEDEN VAROLAN basliklardan
  turetir (KALEM 1, 6 Eyl 2026 kilidi: "diskteki gercek ustundur" — DEGISTIRILMEZ).
  Momentum'un DURUM.md'sinde `## GUNCEL DURUM` hic yoktu, dolayisiyla H3 onu
  "zorunlu" saymadi ve HIC anmadi. `derle` de hedef bolum yoksa fragmani
  sessizce ATLAYIP exit 0 doner. Iki katman birlikte, bir yapilandirma
  eksigini TAMAMEN gorunmez kilar.

NE OLCER — UC KOL, UC AYRI EKSEN (Onur kilidi: K1+K3 -> "kapi her zaman bulgu
versin" (`devral`a DOKUNULMAZ) · K2 -> "`derle` exit 2 = OLCULEMEDI")
  KAPI-1 (KALEM 1, `_kapi_h17`) — `## GUNCEL DURUM` YOK, henuz HIC not
      yazilmamis taze bir kurulumda BILE: `kapi` bulgu URETIR (fragman sarti
      YOK), cikti bolumu ADLANDIRIR. Fixture Momentum'un kurulum-sonrasi
      haliyle BIREBIR ayni sinif: `devral --esle` ile mevcut basliklardan
      turetilmis bir proje (H3 bunu HIC anmaz, H17 KOSULSUZ anar).
      MUTANT (M-A): bu olcumu sokan mutant (H17 kosulu HER ZAMAN False) ISIRIR.
  KAPI-2 (KALEM 2, `derle`) — bolum YOK + fragman VAR: `derle` exit 2 doner,
      "ATLANDI" satirlari AYNEN basilir, fragmanlar gunluk/'te DURUR (SILINMEZ,
      arsive TASINMAZ).
      MUTANT (M-B): exit'i 0'a donduren mutant ISIRIR.
  KAPI-3 (KONTROL KOLU, yanlis pozitif ekseni AYRI olculur — ortusen tespit
      korlugune dusulmez) — bolum VAR: `kapi` bu eksende TEMIZ (H17 hic
      konusmaz), `derle` exit 0, fragman islenip arsive TASINIR.
      MUTANT (M-C): KALEM 1'in bulgusunu KOSULSUZ ureten mutant (H17 kosulu
      HER ZAMAN True) — bolum VARKEN de FIRE eder — ISIRIR.

NE OLCMEZ
  K4 (H6 arsiv blogu icerik korlugu) BU DOSYADA DEGIL — Onur kilidiyle AYRI
  is emrine ertelendi (SIRADAKI). `devral`in KENDI davranisi (basligi
  eklememesi) burada DOGRU/DEGISMEZ kabul edilir, sinanmaz — sinanan KAPININ
  bunu YAKALAMASIdir.

CIKIS KODU  0 uc kol da temiz VE uc mutant da ISIRDI · 1 en az bir kol
            BEKLENMEDIK / mutant KACTI · 2 OLCULEMEDI (git yok, motor
            okunamadi, kurulum basarisiz — kapi hukmu DEGIL)
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

_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="gdkmut", GIT_AUTHOR_EMAIL="gdk@example.invalid",
                GIT_COMMITTER_NAME="gdkmut", GIT_COMMITTER_EMAIL="gdk@example.invalid",
                GIT_CONFIG_NOSYSTEM="1")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def kos(motor, arglar, kok, timeout=120):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args):
    return subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                          env=_GIT_ENV, check=False)


def hal_bolum_yok(motor, kok):
    """Momentum'un kurulum-sonrasi hali: mevcut projenin DURUM.md'sinde
    '## GUNCEL DURUM' HIC YOK; `devral --esle` bunu ONCEDEN VAROLAN
    basliklardan turetir ('devral DEGISMEZ' kilidi, KALEM 1 6 Eyl 2026) —
    H3 bu yuzden bolumu HIC anmaz, kapsam H17'nin KOSULSUZLUGUNU sinar."""
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run(["git", "init", "-q", kok], capture_output=True)
    if r.returncode != 0:
        raise Kurulamadi("git init basarisiz")
    durum = os.path.join(kok, "DURUM.md")
    with open(durum, "w", encoding="utf-8", newline="\n") as f:
        f.write("# DURUM.md\n\n## Kalici dersler\n- ders 1\n\n"
                "## DILIM 3 - ISBIRLIGI\n- calisma\n\n## Bilinen sinirlar\n- sinir 1\n")
    _git(kok, "add", "-A")
    rc_commit = subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false",
                                "commit", "-q", "-m", "ilk"],
                               capture_output=True, env=_GIT_ENV)
    if rc_commit.returncode != 0:
        raise Kurulamadi("git commit basarisiz")
    rc, c = kos(motor, ["devral", "--esle=canli=DURUM.md", "--ad", "GDKMUT"], kok)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    return kok


def hal_bolum_var(motor, kok):
    """KONTROL KOLU (KAPI-3): normal `kur` — '## GUNCEL DURUM' VARSAYILAN
    sablonda zaten vardir, HICBIR SEY elle eklenmez/silinmez."""
    os.makedirs(kok, exist_ok=True)
    rc, c = kos(motor, ["kur", "--ad", "GDKMUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    return kok


_H17_IMZA = "GUNCEL DURUM"           # bulgu metninde bolumu ADLANDIRAN ortak parca
_H17_ETIKET = "[H17]"


def _h17_var_mi(cikti):
    return _H17_ETIKET in cikti and _H17_IMZA in cikti


def kapi1_bolum_yok_taze(motor, taban):
    """KAPI-1: HENUZ HIC not yazilmamis, bolum yok -> kapi bulgu URETMELI
    (fragman sarti YOK — KABUL OLCUTU 3)."""
    kok = hal_bolum_yok(motor, os.path.join(taban, "k1"))
    return kos(motor, ["kapi"], kok)


def kapi2_bolum_yok_fragman_var(motor, taban):
    """KAPI-2: bolum yok + fragman VAR -> `derle` exit 2, ATLANDI satirlari
    basilir, fragman gunluk/'te KALIR (SILINMEZ/tasinmiaz)."""
    kok = hal_bolum_yok(motor, os.path.join(taban, "k2"))
    rc0, c0 = kos(motor, ["not", "--konu=genel-durum",
                          "--metin=guncel durum kapisi mutanti icin ilk kayit"], kok)
    if rc0 != 0:
        raise Kurulamadi("not basarisiz: %s" % c0.strip().split("\n")[-1][:160])
    rc, c = kos(motor, ["derle"], kok)
    return rc, c, kok


def kapi3_bolum_var(motor, taban):
    """KAPI-3 KONTROL KOLU: bolum VAR -> `derle` exit 0, fragman islenip
    arsive tasinir; H17 hic konusmaz (yanlis pozitif yok)."""
    kok = hal_bolum_var(motor, os.path.join(taban, "k3"))
    rc0, c0 = kos(motor, ["not", "--konu=genel-durum",
                          "--metin=guncel durum kapisi mutanti kontrol kolu"], kok)
    if rc0 != 0:
        raise Kurulamadi("not basarisiz: %s" % c0.strip().split("\n")[-1][:160])
    rc, c = kos(motor, ["derle"], kok)
    return rc, c


# --------------------------------------------------------------------- MUTANT
# M-A/M-C AYNI satiri hedefler (`_kapi_h17`'nin kosulu) ama TERS yonlerde
# bozar: M-A hic ATESLEMEZ (False), M-C KOSULSUZ ateşler (True). `_kapi_h17`nin
# GOVDESI (imzasi degil) hedeflenir; `_kapi_govde`deki cagri yeri BU MUTANTLARIN
# HICBIRINDE degismez.
ANKOR_H17_KOSUL = ('    if not any(bas_eslesir(s, "## GUNCEL DURUM") for s in satirlar(y.canli) '
                   'if s.startswith("#")):\n')
YENI_MA = '    if False:      # MUTANT: H17 sokuldu\n'
YENI_MC = '    if True:       # MUTANT: H17 kosulsuz FIRE eder\n'

# M-B: KAPI-2'nin exit 2'sini SOKAR (bolum yok + fragman VAR dali).
ANKOR_MB = ("    kod, cikti = _kapi_kos(kok)\n"
           "    print(cikti.strip())\n"
           "    if not _bolum_var:\n")
YENI_MB = ("    kod, cikti = _kapi_kos(kok)\n"
          "    print(cikti.strip())\n"
          "    if False:      # MUTANT: KALEM 2 exit 2'si sokuldu\n")


def _sabotajli_yaz(kaynak, ankor, yeni, hedef_dizin, ad):
    n = kaynak.count(ankor)
    if n != 1:
        return None, "capa %d yerde gecti (1 olmali): %r" % (n, ankor.strip())
    metin = kaynak.replace(ankor, yeni, 1)
    try:
        compile(metin, "<%s>" % ad, "exec")
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
        print("SONUC: OLCULEMEDI — git yok (bu batarya `devral --esle` icin git ister).")
        return 2

    print(CIZGI)
    print("GUNCEL DURUM KAPISI MUTANTI — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="guncel_durum_kapisi_")
    try:
        b = []

        # ---- KAPI-1 ----------------------------------------------------
        try:
            k1, c1 = kapi1_bolum_yok_taze(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-1 bolum YOK (taze)   OLCULEMEDI: %s" % e)
            return 2
        var1 = _h17_var_mi(c1)
        print("  KAPI-1 bolum YOK (taze)   : kapi exit=%s · [H17] VAR=%s" % (k1, var1))
        if k1 == 0:
            b.append("KAPI-1: kapi exit 0 — bolum yokken YESIL olmamali")
        if not var1:
            b.append("KAPI-1: [H17] bulgusu (bolumu ADLANDIRAN) ciktida YOK")

        # ---- KAPI-2 ----------------------------------------------------
        try:
            k2, c2, kok2 = kapi2_bolum_yok_fragman_var(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-2 bolum YOK+fragman  OLCULEMEDI: %s" % e)
            return 2
        atlandi_var = "ATLANDI" in c2
        gunluk2 = os.path.join(kok2, "gunluk")   # y.gunluk (BEKLEYEN, henuz arsivlenmemis)
        fragman_kaldi = os.path.isdir(gunluk2) and any(
            f.endswith(".md") for f in os.listdir(gunluk2))
        print("  KAPI-2 bolum YOK+fragman  : derle exit=%s · ATLANDI=%s · fragman gunluk'te KALDI=%s"
              % (k2, atlandi_var, fragman_kaldi))
        if k2 != 2:
            b.append("KAPI-2: derle exit %s (2 bekleniyordu — isir'in 'OLCULEMEDI' dili)" % k2)
        if not atlandi_var:
            b.append("KAPI-2: 'ATLANDI' satiri ciktida YOK")
        if not fragman_kaldi:
            b.append("KAPI-2: fragman gunluk/'te KALMADI — SILINMIS/tasinmis olabilir")

        # ---- KAPI-3 (KONTROL KOLU) --------------------------------------
        try:
            k3, c3 = kapi3_bolum_var(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-3 bolum VAR (kontrol) OLCULEMEDI: %s" % e)
            return 2
        var3 = _h17_var_mi(c3)
        islendi3 = "DERLENDI: 1 fragman islendi" in c3
        print("  KAPI-3 bolum VAR (kontrol): derle exit=%s · [H17] VAR=%s · 1 fragman islendi=%s"
              % (k3, var3, islendi3))
        if k3 != 0:
            b.append("KAPI-3: derle exit %s (0 bekleniyordu — bolum VARKEN bugunku davranis)" % k3)
        if var3:
            b.append("KAPI-3: [H17] bolum VARKEN de FIRE etti (yanlis pozitif)")
        if not islendi3:
            b.append("KAPI-3: fragman islenmedi (bolum VARKEN 1 fragman islenmeli)")

        for x in b:
            print("      ! %s" % x)
        if b:
            print("\nSONUC: KIRMIZI — temiz surumun kollari BEKLENMEDIK.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = []

        # ---- M-A ---------------------------------------------------------
        mdirA = tempfile.mkdtemp(prefix="mutantA_", dir=taban)
        sabA, hataA = _sabotajli_yaz(s, ANKOR_H17_KOSUL, YENI_MA, mdirA, "mutantA")
        if sabA is None:
            print("  M-A H17 kosulu sokulur (False)   OLCULEMEDI: %s" % hataA)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kA, cA = kapi1_bolum_yok_taze(sabA, os.path.join(taban, "tA"))
        except Kurulamadi as e:
            print("  M-A H17 kosulu sokulur (False)   OLCULEMEDI: %s" % e)
            return 2
        if not _h17_var_mi(cA):
            print("  M-A H17 kosulu sokulur (False)   -> ISIRDI ✓  (bolum YOKKEN [H17] "
                  "ARTIK cikmiyor)")
        else:
            print("  M-A H17 kosulu sokulur (False)   -> KACTI ✗  ([H17] hala cikiyor — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-A")

        # ---- M-B ---------------------------------------------------------
        mdirB = tempfile.mkdtemp(prefix="mutantB_", dir=taban)
        sabB, hataB = _sabotajli_yaz(s, ANKOR_MB, YENI_MB, mdirB, "mutantB")
        if sabB is None:
            print("  M-B derle exit 2'si sokulur      OLCULEMEDI: %s" % hataB)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kB, cB, _ = kapi2_bolum_yok_fragman_var(sabB, os.path.join(taban, "tB"))
        except Kurulamadi as e:
            print("  M-B derle exit 2'si sokulur      OLCULEMEDI: %s" % e)
            return 2
        if kB != 2:
            print("  M-B derle exit 2'si sokulur      -> ISIRDI ✓  (exit artik %s — "
                  "'OLCULEMEDI' sozlesmesi kayboldu)" % kB)
        else:
            print("  M-B derle exit 2'si sokulur      -> KACTI ✗  (exit hala 2 — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-B")

        # ---- M-C ---------------------------------------------------------
        mdirC = tempfile.mkdtemp(prefix="mutantC_", dir=taban)
        sabC, hataC = _sabotajli_yaz(s, ANKOR_H17_KOSUL, YENI_MC, mdirC, "mutantC")
        if sabC is None:
            print("  M-C H17 kosulsuz FIRE eder (True) OLCULEMEDI: %s" % hataC)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kC, cC = kapi3_bolum_var(sabC, os.path.join(taban, "tC"))
        except Kurulamadi as e:
            print("  M-C H17 kosulsuz FIRE eder (True) OLCULEMEDI: %s" % e)
            return 2
        if _h17_var_mi(cC):
            print("  M-C H17 kosulsuz FIRE eder (True) -> ISIRDI ✓  (bolum VARKEN de "
                  "[H17] cikti — yanlis pozitif ekseni olculuyor)")
        else:
            print("  M-C H17 kosulsuz FIRE eder (True) -> KACTI ✗  ([H17] hala sessiz — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-C")

        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %s beklendigi gibi olculmedi." % ", ".join(kacan))
            return 1
        print("SONUC: YESIL — uc kol da temiz, uc mutant da AYRI eksende ISIRDI.")
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

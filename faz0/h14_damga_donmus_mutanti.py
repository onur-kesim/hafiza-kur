#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — H14 DAMGA DONMUS MUTANTI (KALEM 3, besli-paket/IS_EMRI_DEVRAL.md).

NEDEN VAR (olculdu 6 Eyl 2026, Uygulama - Tuzak Avcisi kopyasi, git DAHIL —
bu is emrinin EN PAHALI bulgusu)
  `kapi` git'li bir kopyada sunu dedi:
      [H12] canli hafiza 43 gundur guncellenmemis (tavan 30 gun)
      [H14] PROJE ILERLEDI, HAFIZA ILERLEMEDI: ... -> Calisildi ama kayit birakilmadi.
  Git ise ayni gun IKI kez hafiza defterine commit oldugunu gosteriyordu. "Kayit
  birakilmadi" cumlesi YANLISTIR ve motorun OLCMEDIGI bir seyi IDDIA EDER.
  Kok: `_kapi_h14` proje tarafini git'e SORAR (`_h14_en_yeni`), hafiza tarafini
  ise yalniz BEYAN edilen `> Son guncelleme:` satirindan (`t_son`) okur — git
  elinin altindayken hafiza defterlerine dokunan SON COMMIT'e (`t_git`) HIC
  BAKMAZ. Bu projede damga YAPISAL olarak DONUK (eski `hafiza_gate` satir 4
  degisince H1 KAYIP verip FAIL ediyordu) — yani H12/H14 SONSUZA DEK yanlis-
  kirmizi yanar, ikisi de TEK NOKTADAN (t_son) duser.

🔴 HUKUM GEVSEMEZ: bu KALEM bir MUAFIYET DEGIL, bir DOGRULUK DUZELTMESIDIR.
  Git mtime'i damganin YERINE GECMEZ; iki halde de (damga gercekten bayat /
  damga donmus) kapi FAIL verir, exit hala 1. Degisen yalniz HANGI CUMLENIN
  basildigidir — "kayit birakilmadi" (yanlis teshis) yerine "tarih damgasi
  donmus" (dogru teshis + duzeltme yolu).

NE OLCER
  KAPI-A (POZITIF KONTROL) — hafiza defterleri (canli+arsiv) damgadan (t_son)
      SONRA commit'lenmis: H14 YENI cumleyi ("HAFIZA YAZILDI, TARIH DAMGASI
      DONMUS") basar, H12 de YENI sozu ("beyan edilen tarih ... yenilenmemis")
      kullanir — AYNI agacta (H12 KOLU). Kapi HALA FAIL, exit 1.
  KAPI-B (GERCEK GERILEME KORUNUR) — defterler damgadan SONRA hic
      commit'lenmemis: eski cumle ("PROJE ILERLEDI, HAFIZA ILERLEMEDI: ...
      Calisildi ama kayit birakilmadi.") AYNEN kalir — gercek "kayit
      birakilmadi" hali yumusatilmaz.
  KAPI-C (GIT YOK KORUNUR) — git'siz agacta cikti BAYT-BIREBIR eski hali:
      yeni cumle hic gorunmez, davranis KALEM 3 ONCESIYLE AYNI.

NE OLCMEZ
  `hafiza_gecikme_gun=0` (kapi bilincli KAPALI) hali — bu dal KALEM 3'ten
  ONCE de sonra da AYNI davranir (`h14_bolme_mutanti.py`nin `h_kapali` koluyla
  zaten kapsamda), burada tekrarlanmaz.

CIKIS KODU  0 uc kapi da temiz VE mutant ISIRDI · 1 kapi kirmizi / mutant KACTI
            2 OLCULEMEDI (git yok, motor okunamadi, senaryo kurulamadi)
"""
import datetime as _dt
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

# Damga (t_son) ile bugun arasindaki mesafe: hem H12 tavanini (30) hem H14
# gecikmesini (2) RAHATCA asar — hukum esik yuvarlamasina degil kenarin
# kendisine baglidir (h14_bolme_mutanti.py'nin GUN sabitiyle ayni gerekce).
GUN_DAMGA = 40
GUN_ARSIV = 3     # damgadan SONRA hafiza defterine dokunan commit
GUN_PROJE = 5     # proje dosyasinin (kod.py) en yeni degisikligi

HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h14 damga donmus mutanti icin ilk kayit"],
            ["derle"]]

_GIT_ENV_TABAN = dict(os.environ, GIT_AUTHOR_NAME="h14dmut", GIT_AUTHOR_EMAIL="h14d@example.invalid",
                      GIT_COMMITTER_NAME="h14dmut", GIT_COMMITTER_EMAIL="h14d@example.invalid",
                      GIT_CONFIG_NOSYSTEM="1")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:160]))
    return r.stdout


def _gun(delta):
    return _dt.date.today() - _dt.timedelta(days=delta)


def _iso_ogle(gun):
    return "%sT12:00:00" % gun.isoformat()


def _commit_et(kok, delta_gun, mesaj):
    iso = _iso_ogle(_gun(delta_gun))
    ortam = dict(_GIT_ENV_TABAN, GIT_AUTHOR_DATE=iso, GIT_COMMITTER_DATE=iso)
    _git(kok, "add", "-A")
    r = subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", mesaj],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ortam)
    if r.returncode != 0:
        raise Kurulamadi("git commit: %s" % (r.stderr or r.stdout).strip()[:160])


def _tarih_yaz(kok, gun):
    """'Son guncelleme' tarihini CANLI ve SNAPSHOT dosyalarinda ayni anda
    degistirir (yalniz canliyi degistirmek H0 CIPA BOZULDU ates eder)."""
    hedefler = [os.path.join(kok, "PROJE_HAFIZA.md"),
                os.path.join(kok, "arsiv", "hafiza", "_KAYNAK.md")]
    yazildi = 0
    for p in hedefler:
        if not os.path.isfile(p):
            continue
        s = open(p, encoding="utf-8").read()
        s2 = re.sub(r"(Son g[uü]ncelleme:\s*)(\d{4}-\d{2}-\d{2})",
                    r"\g<1>" + gun.isoformat(), s, count=1)
        if s2 != s:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(s2)
            yazildi += 1
    if not yazildi:
        raise Kurulamadi("'Son guncelleme' satiri bulunamadi — hal kurulamaz")


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    if tip != "git_yok":
        subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H14DMUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:160]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:160]))

    # Damgayi GUN_DAMGA gun geriye cek (hem H12 tavanini hem H14 gecikmesini asar).
    _tarih_yaz(kok, _gun(GUN_DAMGA))
    kodp = os.path.join(kok, "kod.py")
    with open(kodp, "w", encoding="utf-8", newline="") as f:
        f.write("# h14 damga donmus mutanti icin proje dosyasi\nDEGER = 1\n")

    if tip == "git_yok":
        # git YOK: sadece mtime ile proje ilerlemesini kur.
        os.utime(kodp, None)
        eski_ts = _dt.datetime(*_gun(GUN_DAMGA).timetuple()[:3], 12, 0, 0).timestamp()
        proje_ts = _dt.datetime(*_gun(GUN_PROJE).timetuple()[:3], 12, 0, 0).timestamp()
        for r0, d0, f0 in os.walk(kok):
            d0[:] = [d for d in d0 if d not in (".git", "node_modules", "__pycache__", ".venv")]
            for f in f0:
                p0 = os.path.join(r0, f)
                try:
                    os.utime(p0, (eski_ts, eski_ts))
                except OSError:
                    pass
        os.utime(kodp, (proje_ts, proje_ts))
        return kok

    # git VAR: tum agac damga gunune commit'lenir (canli+arsiv+kod.py birlikte).
    _commit_et(kok, GUN_DAMGA, "taban (damga gunu)")

    if tip == "donmus":
        # KALEM 3 POZITIF KONTROL: hafiza defteri (arsiv altina yeni dosya)
        # damgadan SONRA (GUN_ARSIV < GUN_DAMGA) commit'lenir — 'Son guncelleme'
        # SATIRI guncellenMEDEN. Bu, gercek projede olculen "kayit BIRAKILDI,
        # damga DONDU" halinin ta kendisidir.
        ars_dosya = os.path.join(kok, "arsiv", "hafiza", "HAFIZA_02.md")
        with open(ars_dosya, "w", encoding="utf-8", newline="") as f:
            f.write("# ARSIV 02 — h14 damga donmus mutanti\n> kayit birakildi.\n")
        _commit_et(kok, GUN_ARSIV, "HAFIZA: oturum kayit gunlugu (damga guncellenmedi)")
    elif tip == "gercek_geri":
        # KAPI-B: hafiza defterleri damgadan SONRA HIC commit'lenmedi — sadece
        # proje dosyasi ilerledi. Gercek "kayit birakilmadi" hali.
        pass
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)

    # Proje dosyasi (kod.py) GUN_PROJE gunu KIRLI (izlenen+degismis) olarak
    # ilerler -> `_h14_en_yeni` mtime'ini DOGRUDAN kullanir (h14_bolme_mutanti.py
    # ile ayni "kirli" kalibi).
    with open(kodp, "a", encoding="utf-8", newline="") as f:
        f.write("DEGER = 2   # damgadan SONRA degisti\n")
    proje_ts = _dt.datetime(*_gun(GUN_PROJE).timetuple()[:3], 12, 0, 0).timestamp()
    os.utime(kodp, (proje_ts, proje_ts))
    return kok


HALLER = [
    ("h_donmus", "donmus"),
    ("h_gercek_geri", "gercek_geri"),
    ("h_git_yok", "git_yok"),
]


def haller_kur(motor, taban):
    return {ad: hal_kur(motor, ad, tip, taban) for ad, tip in HALLER}


def kume_olc(motor, kokler, hedef_taban):
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        rc, c = kos(motor, ["kapi"], kok)
        out[ad] = (rc, c)
    return out


def _satir(cikti, etiket):
    for s in [x.strip() for x in cikti.split("\n")]:
        if s.startswith("[%s]" % etiket) or (etiket + ":") in s[:16]:
            return s
    return None


DONMUS_IMZA = "TARIH DAMGASI DONMUS"
ESKI_IMZA = "Calisildi ama kayit birakilmadi"
H12_YENI_SOZ = "beyan edilen tarih"
H12_ESKI_SOZ = "canli hafiza"


def hukum(motor, taban):
    kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
    olcum = kume_olc(motor, kokler, os.path.join(taban, "olc"))
    out = {}
    for ad, tip in HALLER:
        kod, cikti = olcum[ad]
        out[ad] = {
            "kod": kod, "cikti": cikti,
            "h14": _satir(cikti, "H14"),
            "h12": _satir(cikti, "H12"),
        }
    return out


# --------------------------------------------------------------------- MUTANT
# MUTANT: H12'de hesaplanip H14'e yan-kanaldan tasinan git sorgusu SOKULUR ->
# `_H14_T_GIT_SON` HER ZAMAN None kalir -> hem H12 hem H14 ESKI cumleye duser.
ANKOR = "    _H14_T_GIT_SON[0] = _h12_hafiza_git_tarihi(y, rc) if t_son else None\n"
YENI = "    _H14_T_GIT_SON[0] = None      # MUTANT: git sorgusu sokuldu\n"


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
    print("H14 DAMGA DONMUS MUTANTI (KALEM 3) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h14_damga_donmus_")
    try:
        try:
            h = hukum(yol, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2

        b = []
        # ---- KAPI-A POZITIF KONTROL --------------------------------------
        r = h["h_donmus"]
        print("  KAPI-A damga donmus  : kod=%s" % r["kod"])
        print("      H14: %s" % (r["h14"] or "(YOK)"))
        print("      H12: %s" % (r["h12"] or "(YOK)"))
        if r["kod"] != 1:
            b.append("KAPI-A: kapi exit %s (1 bekleniyordu — HUKUM GEVSEMEMELI)" % r["kod"])
        if DONMUS_IMZA not in r["cikti"]:
            b.append("KAPI-A: H14 YENI cumleyi ('%s') basmiyor" % DONMUS_IMZA)
        if ESKI_IMZA in r["cikti"]:
            b.append("KAPI-A: H14 hala ESKI cumleyi basiyor (yanlis teshis surdu)")
        if not r["h12"] or H12_YENI_SOZ not in r["h12"]:
            b.append("KAPI-A (H12 KOLU): H12 YENI sozu ('%s') kullanmiyor" % H12_YENI_SOZ)

        # ---- KAPI-B GERCEK GERILEME KORUNUR -------------------------------
        r = h["h_gercek_geri"]
        print("  KAPI-B gercek gerileme: kod=%s" % r["kod"])
        print("      H14: %s" % (r["h14"] or "(YOK)"))
        if r["kod"] != 1:
            b.append("KAPI-B: kapi exit %s (1 bekleniyordu)" % r["kod"])
        if ESKI_IMZA not in r["cikti"]:
            b.append("KAPI-B: gercek gerilemede ESKI cumle ('%s') KAYBOLDU" % ESKI_IMZA)
        if DONMUS_IMZA in r["cikti"]:
            b.append("KAPI-B: gercek gerileme YANLISLIKLA 'damga donmus' sanildi")

        # ---- KAPI-C GIT YOK KORUNUR ---------------------------------------
        r = h["h_git_yok"]
        print("  KAPI-C git yok        : kod=%s" % r["kod"])
        print("      H14: %s" % (r["h14"] or "(YOK)"))
        print("      H12: %s" % (r["h12"] or "(YOK)"))
        if r["kod"] != 1:
            b.append("KAPI-C: kapi exit %s (1 bekleniyordu)" % r["kod"])
        if DONMUS_IMZA in r["cikti"]:
            b.append("KAPI-C: git YOKKEN 'damga donmus' cumlesi CIKTI — bireBir korunmadi")
        if r["h12"] and H12_YENI_SOZ in r["h12"]:
            b.append("KAPI-C: git YOKKEN H12 YENI sozu kullandi — bireBir korunmadi")

        for x in b:
            print("      ! %s" % x)
        if b:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
        sab, hata = sokulmus_motor(s, mdir)
        if sab is None:
            print("  M-1 git sorgusu sokulur            OLCULEMEDI: %s" % hata)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            mh = hukum(sab, os.path.join(taban, "mutant"))
        except Kurulamadi as e:
            print("  M-1 git sorgusu sokulur            OLCULEMEDI: %s" % e)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant hali kurulamadi.")
            return 2
        r = mh["h_donmus"]
        if ESKI_IMZA in r["cikti"] and DONMUS_IMZA not in r["cikti"]:
            print("  M-1 git sorgusu sokulur            -> ISIRDI ✓  (ESKI cumle geri geldi: %s)"
                  % r["h14"])
            print(CIZGI)
            print("SONUC: YESIL — kapilar temiz, mutant AYRI eksende ISIRDI.")
            return 0
        print("  M-1 git sorgusu sokulur            -> KACTI ✗  (sorgu sokulunce de YENI "
              "cumle CIKTI — kapi bunu HIC OLCMUYOR): %s" % (r["h14"] or "(YOK)"))
        print(CIZGI)
        print("SONUC: KAPI KOR — mutant beklendigi gibi olculmedi.")
        return 1
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

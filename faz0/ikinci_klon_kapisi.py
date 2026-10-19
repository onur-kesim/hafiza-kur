#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IKINCI KLON KAPISI — `core.autocrlf=true` altinda taze klonda `kapi` YESIL kaliyor mu?
(besli-paket/IS_EMRI_GITATTRIBUTES_MUHUR.md KALEM 3, 18 Eki 2026)

NEDEN VAR (OLCULDU 18 Eki 2026, Windows 11, `core.autocrlf=true`, hafiza.py 6EA0A2ED)
  proje-sablonu'ndan klon + `devral` + `not` + `derle` + commit -> ayni makinede `kapi` YESIL.
  AYNI depo ikinci kez klonlandi (Windows varsayilani) -> `kapi` exit 1, FAIL 10:
      [H0] CIPA BOZULDU: _KAYNAK.md SHA ... != _CIPA.json ...
      9x `defter MUHURSUZ degismis`
  Sebep: hafiza.py defterleri BAYT-TAM hash'ler (`sha_dosya` "rb"); git `autocrlf=true` checkout'ta
  LF'i CRLF'e cevirir; muhurlu dosyalarin SHA'si degisir. Hicbir tahrif yokken, HER Windows
  kullanicisinda, HER ikinci klonda. Sinif UCUNCU kez isirdi (DURUM.md `.gitkeep`/autocrlf siniri).
  Cozum: `kur`/`devral` `.gitattributes`'a muhurlu kume icin `-text` blogu yazar (KALEM 1).

NE OLCER (gercek ikinci klon — simulasyon degil)
  1. gecici proje: `git init` -> `kur` -> `not` -> `derle` -> commit            (kurulum)
  2. AYNI makinede `kapi` exit 0                                               (POZITIF KONTROL)
  3. `git clone` ikinci kopya -> `kapi` exit 0                                 (HUKUM)
  Kurulum ya da pozitif kontrol kirmizi ise OLCULEMEDI (exit 2): ikinci klonun kirmizisi o zaman
  autocrlf'e YAZILAMAZ. NEGATIF KONTROL: klonda `core.autocrlf=true` GERCEKTEN CRLF uretmediyse (ayar
  etkisiz) hukum YOK (OLCULEMEDI): vakum YESIL sahte guvence olurdu.
  `core.autocrlf=true` TEK AYARDIR ve ELLE kurulur: `GIT_CONFIG_GLOBAL` ile gecici bir "global" dosyaya
  yazilir (CI'da `git config --global core.autocrlf true` ile ayni etki; yerelde kullanicinin GERCEK
  global ayarina DOKUNULMAZ). Sistem ayari (runner'in ne dedigi) ezilir: sonuc runner'a bagli degildir.

  `--ad-alani <dizin>`: arsiv dizini FARKLI ad alaninda (`.hafizarc hafiza_dizini`) kurulur — `kur`, `.hafizarc`i degistir, dizini
  tasi, `.gitattributes`i sil, `kur`u tekrarla (idempotent tazeleme): blok SABIT liste degil ad alanindan TUREMIS olmali.

KULLANIM   python3 faz0/ikinci_klon_kapisi.py [--motor yol/hafiza.py] [--ad-alani kayit/hafiza]
CIKIS KODU 0 ikinci klonda kapi YESIL · 1 KIRMIZI (ham cikti basilir) · 2 OLCULEMEDI
"""
import argparse
import json
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
HAZIRLIK = [["kur", "--ad", "IKIKLON"],
            ["not", "--konu=genel-durum", "--tur=durum", "--metin=ikinci klon kapisi icin ilk kayit"],
            ["derle"]]


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Ikinci klonun hukmu YOK demektir (sahte yesil/kirmizi uretme)."""


def git_ortami(taban):
    """`core.autocrlf=true` TEK ayar; gercek global config'e dokunulmaz."""
    g = os.path.join(taban, "gitconfig-global")
    with open(g, "w", encoding="utf-8", newline="\n") as f:
        f.write("[core]\n\tautocrlf = true\n[user]\n\tname = ikiklon\n\temail = ikiklon@example.invalid\n"
                "[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n")
    haric = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT")      # baska deponun/komutun ortami sizmasin
    ortam = dict((k, v) for k, v in os.environ.items() if k not in haric)
    return dict(ortam, GIT_CONFIG_GLOBAL=g, PYTHONIOENCODING="utf-8")


def git(ortam, *args, cwd=None):
    r = subprocess.run(["git"] + list(args), cwd=cwd, env=ortam, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:160]))
    return r.stdout


def kos(motor, arglar, kok, ortam):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok], env=ortam,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _agaci_sil(yol):
    """Windows'ta git nesneleri SALT-OKUNURDUR; `ignore_errors=True` onlari birakir."""
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


def _crlf_sayisi(kok):
    """Teshis (hukum DEGIL): izlenen dosyalarda CRLF iceren dosya sayisi."""
    n = 0
    for r0, d0, f0 in os.walk(kok):
        d0[:] = [d for d in d0 if d != ".git"]
        for f in f0:
            try:
                with open(os.path.join(r0, f), "rb") as fh:
                    if b"\r\n" in fh.read():
                        n += 1
            except OSError:
                pass
    return n


def ad_alanina_tasi(motor, proje, ortam, yeni):
    """`.hafizarc hafiza_dizini`ni degistirir, arsiv dizinini tasir, `.gitattributes`i siler ve `kur`u tekrarlar (idempotent tazeleme)."""
    rcp = os.path.join(proje, ".hafizarc")
    with open(rcp, encoding="utf-8") as f:
        d = json.load(f)
    eski = d.get("hafiza_dizini", "arsiv/hafiza")
    d["hafiza_dizini"] = yeni
    with open(rcp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    hedef = os.path.join(proje, *yeni.split("/"))
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    shutil.move(os.path.join(proje, *eski.split("/")), hedef)
    ga = os.path.join(proje, ".gitattributes")
    if os.path.isfile(ga):
        os.remove(ga)
    rc, c = kos(motor, ["kur"], proje, ortam)
    if rc != 0:
        raise Kurulamadi("ad alani degisimi sonrasi `kur` basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))


def olc(motor, taban, ad_alani=None):
    """-> (hukum, ayrinti dict). hukum: 'YESIL' | 'KIRMIZI'. Kurulamazsa Kurulamadi firlatir."""
    ortam = git_ortami(taban)
    proje, klon = os.path.join(taban, "proje"), os.path.join(taban, "klon")
    os.makedirs(proje)
    git(ortam, "init", "-q", proje)
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, proje, ortam)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (exit %s): %s" % (adim[0], rc, c.strip().split("\n")[-1][:140]))
    if ad_alani:
        ad_alanina_tasi(motor, proje, ortam, ad_alani)
    git(ortam, "add", "-A", cwd=proje)
    git(ortam, "commit", "-q", "-m", "ikinci klon kapisi: taban", cwd=proje)
    rc0, c0 = kos(motor, ["kapi"], proje, ortam)
    if rc0 != 0:
        raise Kurulamadi("POZITIF KONTROL kirmizi: ILK projede `kapi` exit %s (ikinci klonun kirmizisi "
                         "autocrlf'e yazilamaz):\n%s" % (rc0, "\n".join(c0.strip().split("\n")[-12:])))
    git(ortam, "clone", "-q", proje, klon)
    crlf_p, crlf_k = _crlf_sayisi(proje), _crlf_sayisi(klon)
    if crlf_k <= crlf_p:
        # NEGATIF KONTROL: `core.autocrlf=true` klonda GERCEKTEN CRLF uretmediyse (eski git GIT_CONFIG_GLOBAL'i yok sayar, ayar ezilmis olabilir)
        # YESIL vakumdur: korumayi degil ayarin etkisizligini olcmus oluruz.
        raise Kurulamadi("core.autocrlf=true klonda CRLF URETMEDI (proje %d, klon %d CRLF'li dosya): ayar etkisiz — hukum YOK" % (crlf_p, crlf_k))
    rc1, c1 = kos(motor, ["kapi"], klon, ortam)
    return ("YESIL" if rc1 == 0 else "KIRMIZI"), {"exit": rc1, "cikti": c1, "crlf_proje": crlf_p, "crlf_klon": crlf_k}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    ap.add_argument("--ad-alani", default=None, help="arsiv dizini ad alani (ornek: kayit/hafiza); varsayilan arsiv/hafiza")
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — ikinci klon kurulamaz.")
        return 2
    print(CIZGI)
    print("IKINCI KLON KAPISI — core.autocrlf=true, gercek ikinci klonda `kapi` — platform: %s" % sys.platform)
    print("motor: %s%s" % (motor, (" · ad alani: " + a.ad_alani) if a.ad_alani else ""))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="ikiklon_")
    try:
        try:
            hukum, d = olc(motor, taban, a.ad_alani)
        except Kurulamadi as e:
            print("OLCULEMEDI: %s" % e)
            return 2
        except (OSError, subprocess.SubprocessError) as e:
            print("OLCULEMEDI: arac hatasi (%s: %s)" % (type(e).__name__, e))
            return 2
        print("  proje (ilk) `kapi`            exit 0  (pozitif kontrol)")
        print("  CRLF iceren dosya             proje %d · klon %d   (teshis; hukum DEGIL)" % (d["crlf_proje"], d["crlf_klon"]))
        print("  ikinci klon `kapi`            exit %s" % d["exit"])
        if hukum == "KIRMIZI":
            bulgular = [s.rstrip() for s in d["cikti"].split("\n")
                        if s.lstrip().startswith("[H") or "SONUC" in s]
            for s in bulgular[:14]:
                print("      " + s[:150])
            if len(bulgular) > 14:
                print("      ... (%d satir daha)" % (len(bulgular) - 14))
            print(CIZGI)
            print("SONUC: KIRMIZI — taze ikinci klonda `kapi` exit %s (autocrlf=true: muhurlu dosyalar bozuldu)" % d["exit"])
            return 1
        print(CIZGI)
        print("SONUC: YESIL — ikinci klonda `kapi` exit 0 (core.autocrlf=true)")
        return 0
    finally:
        _agaci_sil(taban)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — GITKEEP MUTANTI (B2, besli-paket/IS_EMRI_KUTUDAN_B1B2.md, Onur kilidi 4 Eki 2026).

NEDEN VAR (olculdu 4 Eki 2026, Momentum kopyasi, OLCUM_RAPORU_04EKIM_DENEME_V7.md §2 B2)
  `derle` fragmanlari arsive tasiyinca `gunluk/` bos kaliyor, ADR yoksa `kararlar/` bos. Git bos dizin
  TASIMAZ: kurulu + commit'li projeyi `git clone` eden ikinci makine / yeni oturum ilk acilista `kapi`
  KIRMIZI goruyor (`[H16] kararlar YOK` · `[H16] gunluk YOK`). CI (189/189) bunu GORMEDI: hicbir CI
  fixture'i kur -> commit -> KLON -> kapi zincirini kosmuyordu. Duzeltme: `kur` (taze kurulum) ve `devral`
  H16'nin denetledigi DORT dizinin (kararlar · gunluk · gunluk_ars · hafiza dizini) HER BIRINE bos `.gitkeep`
  yazar; idempotent, var olana dokunmaz. MEVCUT kurulu projede `kapi` eksik `.gitkeep`i bulgu YAPMAZ ve
  tekrar `kur` onu ONARMAZ (onarmak AYRI karar — bu pakette YOK).

NE OLCER — YEDI KOL (her biri temiz motorda YESIL olmali)
  KOL 1 (KUR AKISI) — kur -> not -> derle -> git commit -> `git clone` -> klonda `kapi`: dort `.gitkeep` git'te
      IZLENIYOR (0 bayt) ve klonda `[H16]` bulgusu YOK, `SONUC: YESIL`, exit 0.
  KOL 2 (DEVRAL AKISI) — Momentum SEKLI (CLAUDE.md + DURUM.md; devral --esle -> bolum-kur -> not -> derle -> commit
      -> klon -> kapi): ayni uc beklenti.
  KOL 3 (GERIYE UYUM) — taze kur'dan sonra dort `.gitkeep` SILINIR (mevcut kurulu proje gibi): (a) `kapi` YESIL,
      eksik `.gitkeep` bulgu DEGIL; (b) ikinci `kur` (idempotent tazeleme) `.gitkeep` YAZMAZ.
  KOL 4 (VAR OLANA DOKUNMA) — `kararlar/.gitkeep` kullanici icerigiyle ONCEDEN var: taze `kur` onu EZMEZ, diger
      uc dizine bos `.gitkeep` yazar.
  KOL 5 (YARIM KURULUM YOK) — `gunluk/` yazilamaz (chmod 555) iken taze `kur`: `.gitkeep` best-effort, kurulum TAM
      (`.hafizarc` + zincir + cipa), exit 0, stderr'de UYARI; tekrar `kur` "VERI KAYBI" diye REDDETMEZ (OLCULDU:
      erken/fatal yazim `.hafizarc` yazilmis YARIM kurulum birakiyordu). YALNIZ POSIX non-root (Windows'ta dizin
      chmod'u etkisiz, root izni asar) — aksi halde UYGULANMAZ, kapi korlugu degildir.
  KOL 6 (H4 HAVUZU) — `.gitkeep` bir dosya ADI sayilmaz: GERCEKTEN olmayan `.gitkeep` hedefli markdown linki
      (`[x](arsiv/olmayan/.gitkeep)`) `[H4] OLU BAGLANTI` KALIR. Havuza girerse "ayni adla baska yerde var" diye
      TASINMIS sayilir ve FAIL -> YESIL olur (OLCULDU).
  KOL 7 (H12 GIT TARIHI) — bayat damga + ESKI tarihli commit; sonra YALNIZ `arsiv/hafiza/.gitkeep` degisip BUGUN
      commit'lenir: H12 cumlesi `canli hafiza N gundur guncellenmemis` KALIR; `defterler git'te ... commit'lenmis`
      YANLIS teshisine donusmez (`y.h` bir DIZIN pathspec'i; `.gitkeep` icindedir — OLCULDU).
  Klon, `git -c core.autocrlf=false clone` ile yapilir: Windows'un varsayilani (`autocrlf=true`) checkout'ta CRLF
  uretir ve `.gitkeep` olsa bile `kapi` H0'da KIRMIZI olur (OLCULDU) — bu ayri bir sinif; mutant H16'yi olcmeli.

ON SABOTAJ (her duzeltmeye AYRI; her biri BEKLENEN kolu — ve yalniz onu — KIRMIZI yakmali)
  M-1 yazim kapanir (hic `.gitkeep` yazilmaz)     -> KOL 1, 2, 4 (+5 POSIX'te) KIRMIZI (klonda `[H16] ... YOK` GERI GELIR)
  M-2 `kur` cagri yeri kapanir                    -> KOL 1, 4 (+5 POSIX'te) KIRMIZI (devral akisi YESIL kalir)
  M-3 `devral` cagri yeri kapanir                 -> KOL 2 KIRMIZI (kur akisi YESIL kalir)
  M-4 tekrar `kur` da yazar (onarim)              -> KOL 3 KIRMIZI (geriye uyum bozulur)
  M-5 `xb` -> `wb` (var olani ezer)               -> KOL 4 KIRMIZI
  M-6 `kapi` eksik `.gitkeep`i bulgu yapar        -> KOL 3 KIRMIZI
  M-7 hafiza dizini dortlunun disinda kalir       -> KOL 1, 2, 4 KIRMIZI (H16 onu klonda GOZLEMEZ: dizin hep dolu —
                                                     bu kol MULK kontroluyle isirir)
  M-8 yazim hatasi FATAL olur (UYARI kalkar)      -> KOL 5 KIRMIZI (UYGULANMAZ ise bu sabotaj da UYGULANMAZ)
  M-9 H4 havuzu `.gitkeep`i ad sayar              -> KOL 6 KIRMIZI
  M-10 H12 git tarihi `.gitkeep`i defter sayar    -> KOL 7 KIRMIZI

CIKIS KODU  0 temiz kollar YESIL VE her sabotaj beklenen kolu kirmizi yakti · 1 temiz kol KIRMIZI ya da sabotaj
            KACTI/yanlis kolu yakti · 2 OLCULEMEDI (git yok, motor okunamadi, capa tutmadi, kurulum basarisiz)
"""
import concurrent.futures
import datetime
import io
import os
import re
import shutil
import stat
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

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
DORT = ["kararlar", "gunluk", "arsiv/hafiza/gunluk", "arsiv/hafiza"]     # H16'nin dort dizini (hafiza dizini: arsiv/hafiza)
GITKEEP = ".gitkeep"
KULLANICI_ICERIK = "KULLANICI-ICERIGI-EZILMEMELI"


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapi hukmu DEGIL."""


def kos(motor, arglar, kok, timeout=300):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def git(kok, *arg):
    r = subprocess.run(["git", "-C", kok] + list(arg), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _yaz_satirlar(yol, satirlar):
    with io.open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(satirlar) + "\n")


def _adim(motor, arglar, kok, tolere=False):
    rc, c = kos(motor, arglar, kok)
    if rc != 0 and not tolere:
        raise Kurulamadi("%s basarisiz (exit %d): %s" % (arglar[0], rc, c.strip().split("\n")[-1][:160]))
    return rc, c


def _commit(kok):
    for arg in (["init", "-q"], ["add", "-A"],
                ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                 "commit", "-q", "-m", "gitkeep mutanti fixture"]):
        rc, c = git(kok, *arg)
        if rc != 0:
            raise Kurulamadi("git %s basarisiz: %s" % (arg[-1] if arg[0] != "-c" else "commit", c.strip()[:120]))


def _kur_fixture(motor, kok, onceden=None):
    """kur -> not -> derle (derle `gunluk/`u BOSALTIR: B2'nin mekanizmasi). `onceden`: kur'dan ONCE yapilacak is."""
    os.makedirs(kok, exist_ok=True)
    if onceden:
        onceden(kok)
    _adim(motor, ["kur", "--ad", "GKMUT"], kok)
    _adim(motor, ["not", "--konu=genel-durum", "--metin=gitkeep mutanti ilk kayit"], kok)
    _adim(motor, ["derle"], kok, tolere=True)       # kapi kirmizi donerse exit 1; hukmu klon kapisi verir
    return kok


def _devral_fixture(motor, kok):
    """Momentum SEKLI: yalniz CLAUDE.md + DURUM.md; canli rolu otomatik taninmaz -> `--esle` ile kilitlenir."""
    os.makedirs(kok, exist_ok=True)
    bugun = datetime.date.today().isoformat()
    _yaz_satirlar(os.path.join(kok, "CLAUDE.md"),
                  ["# GK fixture - PROJE ESASLARI", "", "## Kurallar",
                   "- birinci ornek kural satiri uzun ve benzersizdir"])
    _yaz_satirlar(os.path.join(kok, "DURUM.md"),
                  ["# GK fixture - DURUM", "> Son guncelleme: " + bugun, "", "## Genel",
                   "- birinci ornek durum satiri uzun ve benzersizdir", "",
                   "## Bilinen sinirlar", "- birinci ornek sinir satiri uzun ve benzersizdir"])
    for arglar in (["devral", "--esle", "canli=DURUM.md,kural=CLAUDE.md", "--ad", "GKDEV"],
                   ["bolum-kur"],
                   ["not", "--konu=genel-durum", "--tur=durum", "--metin=gitkeep mutanti ilk kayit"],
                   ["derle"]):
        _adim(motor, arglar, kok, tolere=(arglar[0] in ("devral", "bolum-kur", "derle")))
    return kok


def _klon_olc(motor, kaynak, klon):
    """commit'li `kaynak`i KLONLA, klonda `kapi` kos. Doner: (izlenen .gitkeep listesi, bayt hepsi 0 mu,
    kapi exit, [H16] satirlari, SONUC satiri)."""
    _commit(kaynak)
    rc, ls = git(kaynak, "ls-files")
    izlenen = sorted(s.strip() for s in ls.splitlines() if s.strip().endswith(GITKEEP))
    sifir = all(os.path.getsize(os.path.join(kaynak, *s.split("/"))) == 0 for s in izlenen if os.path.isfile(os.path.join(kaynak, *s.split("/"))))
    r = subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", kaynak, klon],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise Kurulamadi("git clone basarisiz: %s" % (r.stderr or "").strip()[:120])
    k, c = kos(motor, ["kapi"], klon)
    h16 = [s.strip() for s in c.splitlines() if "[H16]" in s]
    sonuc = next((s.strip() for s in c.splitlines() if s.startswith("SONUC")), "SONUC satiri YOK")
    return izlenen, sifir, k, h16, sonuc


def _klon_yesil(sonuc_tuple):
    izlenen, sifir, k, h16, sonuc = sonuc_tuple
    return izlenen == sorted(d + "/" + GITKEEP for d in DORT) and sifir and k == 0 and not h16 and "YESIL" in sonuc


def kol1(motor, taban):
    kaynak = _kur_fixture(motor, os.path.join(taban, "k1"))
    return _klon_olc(motor, kaynak, os.path.join(taban, "k1_klon"))


def kol2(motor, taban):
    kaynak = _devral_fixture(motor, os.path.join(taban, "k2"))
    return _klon_olc(motor, kaynak, os.path.join(taban, "k2_klon"))


def kol3(motor, taban):
    """GERIYE UYUM: dort `.gitkeep` silinir; (a) kapi YESIL (b) ikinci kur yazmaz. Doner (a_ok, b_ok, ayrinti)."""
    kok = _kur_fixture(motor, os.path.join(taban, "k3"))
    silinen = 0
    for d in DORT:
        p = os.path.join(kok, *d.split("/"), GITKEEP)
        if os.path.isfile(p):          # yazici KAPALI bir motorda zaten yok: proje zaten 'mevcut kurulu' seklindedir
            os.remove(p)
            silinen += 1
    k, c = kos(motor, ["kapi"], kok)
    a_ok = k == 0 and "YESIL" in c and GITKEEP not in c
    _adim(motor, ["kur", "--ad", "GKMUT"], kok)
    yazilan = [d for d in DORT if os.path.lexists(os.path.join(kok, *d.split("/"), GITKEEP))]
    b_ok = not yazilan
    return a_ok, b_ok, ("silinen=%d .gitkeep · kapi exit=%d · tekrar kur sonrasi yazilan .gitkeep=%s"
                        % (silinen, k, yazilan or "yok"))


def kol4(motor, taban):
    """VAR OLANA DOKUNMA: kararlar/.gitkeep kullanici icerigiyle onceden var -> ezilmez, diger uc dizine bos yazilir."""
    def onceden(kok):
        os.makedirs(os.path.join(kok, "kararlar"))
        with io.open(os.path.join(kok, "kararlar", GITKEEP), "w", encoding="utf-8", newline="\n") as f:
            f.write(KULLANICI_ICERIK)
    kok = _kur_fixture(motor, os.path.join(taban, "k4"), onceden)
    p0 = os.path.join(kok, "kararlar", GITKEEP)
    icerik = io.open(p0, encoding="utf-8", newline="").read() if os.path.isfile(p0) else None
    digerleri = [d for d in DORT if d != "kararlar"]
    bos = all(os.path.isfile(os.path.join(kok, *d.split("/"), GITKEEP))
              and os.path.getsize(os.path.join(kok, *d.split("/"), GITKEEP)) == 0 for d in digerleri)
    return icerik == KULLANICI_ICERIK and bos, "kararlar/.gitkeep icerigi=%r · diger uc bos yazildi=%s" % (icerik, bos)


def kol6(motor, taban):
    """H4 HAVUZU: `.gitkeep` bir dosya ADI sayilmaz — GERCEKTEN olmayan `.gitkeep` hedefli markdown linki OLU kalir.
    (Havuza girerse 'ayni adla baska yerde var' diye TASINMIS sayilir: FAIL -> YESIL, OLCULDU.)"""
    kok = os.path.join(taban, "k6")
    os.makedirs(kok)
    _adim(motor, ["kur", "--ad", "GKMUT"], kok)
    _adim(motor, ["not", "--konu=genel-durum", "--metin=bkz [yok](arsiv/olmayan/.gitkeep) isaretli baglanti"], kok)
    _adim(motor, ["derle"], kok, tolere=True)       # H4 bulgusu yuzunden exit 1 donebilir; hukmu asagidaki kapi verir
    k, c = kos(motor, ["kapi"], kok)
    h4 = [s.strip() for s in c.splitlines() if "H4" in s]
    olu = k == 1 and any("[H4] OLU BAGLANTI" in s and "arsiv/olmayan/.gitkeep" in s for s in h4)
    return olu, "kapi exit=%d · %s" % (k, "; ".join(x[:90] for x in h4[:2]) or "H4 satiri YOK")


def _commit_tarihli(kok, mesaj, tarih=None):
    """`git add -A` + commit; `tarih` (YYYY-MM-DD) verilirse commit o tarihle atilir (yazar + islemci)."""
    ortam = dict(os.environ)
    if tarih:
        ortam["GIT_AUTHOR_DATE"] = ortam["GIT_COMMITTER_DATE"] = tarih + "T12:00:00"
    for arg in (["add", "-A"],
                ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                 "commit", "-q", "-m", mesaj]):
        r = subprocess.run(["git", "-C", kok] + arg, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=ortam)
        if r.returncode != 0:
            raise Kurulamadi("git %s basarisiz: %s" % (arg[-1] if arg[0] != "-c" else "commit", (r.stderr or "").strip()[:120]))


def kol7(motor, taban):
    """H12 GIT TARIHI: yalniz `.gitkeep`e dokunan SONRAKI bir commit 'defterlere dokunan son commit' SAYILMAZ —
    H12 cumlesi YANLIS teshise ('defterler git'te ... commit'lenmis') donusmez. Bayat damga + ESKI tarihli commit; sonra
    YALNIZ `arsiv/hafiza/.gitkeep` degisir ve BUGUN commit'lenir. (`y.h` bir DIZIN pathspec'idir: `.gitkeep` icindedir.)"""
    kok = os.path.join(taban, "k7")
    os.makedirs(kok)
    rc, c = git(kok, "init", "-q")
    if rc != 0:
        raise Kurulamadi("git init basarisiz: %s" % c.strip()[:120])
    _adim(motor, ["kur", "--ad", "GKMUT"], kok)
    _adim(motor, ["not", "--konu=genel-durum", "--metin=gitkeep mutanti ilk kayit"], kok)
    _adim(motor, ["derle"], kok, tolere=True)
    eski = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()
    cp = os.path.join(kok, "PROJE_HAFIZA.md")
    s = io.open(cp, encoding="utf-8", newline="").read()
    yeni, n = re.subn(r"(Son guncelleme:\s*)\d{4}-\d{2}-\d{2}", r"\g<1>" + eski, s, count=1)
    if n != 1:
        raise Kurulamadi("KOL 7: canlida 'Son guncelleme: <tarih>' damgasi bulunamadi")
    io.open(cp, "w", encoding="utf-8", newline="").write(yeni)
    _commit_tarihli(kok, "eski tarihli kurulum", eski)
    with io.open(os.path.join(kok, "arsiv", "hafiza", GITKEEP), "w", encoding="utf-8", newline="\n") as f:
        f.write("x")                                   # yalniz `.gitkeep` degisir -> BUGUN commit'lenir
    _commit_tarihli(kok, "yalniz .gitkeep degisti")
    k, c = kos(motor, ["kapi"], kok)
    h12 = [x.strip() for x in c.splitlines() if "[H12]" in x]
    ok = any("guncellenmemis" in x for x in h12) and not any("commit'lenmis" in x for x in h12)
    return ok, "kapi exit=%d · %s" % (k, "; ".join(x[:110] for x in h12[:2]) or "H12 satiri YOK")


def kol5_uygulanabilir():
    """Dizin yazma izni: Windows'ta chmod dizinde etkisiz, root izin engelini asar -> KOL 5 UYGULANMAZ."""
    return os.name != "nt" and not (hasattr(os, "geteuid") and os.geteuid() == 0)


def kol5(motor, taban):
    """YARIM KURULUM YOK: `gunluk/` yazilamazken taze `kur` — `.gitkeep` best-effort, kurulum TAM, tekrar kur reddetmez.
    Doner (ok, ayrinti). Dizin izni her kosulda geri verilir (harness temizligi)."""
    kok = os.path.join(taban, "k5")
    gk = os.path.join(kok, "gunluk")
    os.makedirs(gk)
    os.chmod(gk, 0o555)
    try:
        try:
            with open(os.path.join(gk, "_on_kosul"), "xb"):
                pass
        except OSError:
            pass
        else:
            raise Kurulamadi("KOL 5 on-kosul: chmod 555 dizin YAZILABILDI (izin engeli etkisiz)")
        rc, c = kos(motor, ["kur", "--ad", "GKMUT"], kok)
        uyari = "UYARI: .gitkeep yazilamadi" in c
        tam = all(os.path.isfile(os.path.join(kok, *p.split("/")))
                  for p in (".hafizarc", "arsiv/hafiza/_ZINCIR.jsonl", "arsiv/hafiza/_CIPA.json"))
        digeri = os.path.isfile(os.path.join(kok, "kararlar", GITKEEP))
        rc2, c2 = kos(motor, ["kur", "--ad", "GKMUT"], kok)
        return (rc == 0 and uyari and tam and digeri and rc2 == 0,
                "kur exit=%d · UYARI=%s · kurulum tam=%s · yazilabilen dizine .gitkeep=%s · tekrar kur exit=%d%s"
                % (rc, uyari, tam, digeri, rc2, "" if rc == 0 else " · " + c.strip().split("\n")[-1][:70]))
    finally:
        os.chmod(gk, 0o755)


def tum_kollar(motor, taban):
    """Bes kolu bir motorda kos. Doner {kol: (yesil_mi | None=UYGULANMAZ, ayrinti)}."""
    out = {}
    for ad, fn in (("KOL 1", kol1), ("KOL 2", kol2)):
        t = fn(motor, os.path.join(taban, ad.replace(" ", "")))
        out[ad] = (_klon_yesil(t), "izlenen=%d .gitkeep · klon kapi exit=%d · %s%s"
                   % (len(t[0]), t[2], t[4][:40], (" · " + "; ".join(t[3])[:70]) if t[3] else ""))
    a_ok, b_ok, ay = kol3(motor, os.path.join(taban, "KOL3"))
    out["KOL 3"] = (a_ok and b_ok, ("a=%s b=%s · " % ("YESIL" if a_ok else "KIRMIZI", "YESIL" if b_ok else "KIRMIZI")) + ay)
    ok4, ay4 = kol4(motor, os.path.join(taban, "KOL4"))
    out["KOL 4"] = (ok4, ay4)
    if kol5_uygulanabilir():
        out["KOL 5"] = kol5(motor, os.path.join(taban, "KOL5"))
    else:
        out["KOL 5"] = (None, "UYGULANMAZ (Windows ya da root: dizin izin engeli olusturulamaz)")
    out["KOL 6"] = kol6(motor, os.path.join(taban, "KOL6"))
    out["KOL 7"] = kol7(motor, os.path.join(taban, "KOL7"))
    return out


# ---------------------------------------------------------------------------------------------------
# SABOTAJLAR — hedef dizge motorda TAM 1 kez gecmeli (degilse OLCULEMEDI: motor degistiyse SABOTAJ DA DEGISMELI)
# ---------------------------------------------------------------------------------------------------
SABOTAJLAR = [
    ("M-1 yazim kapanir (hic .gitkeep yazilmaz)",
     '            with open(os.path.join(d, ".gitkeep"), "xb"):\n                pass\n', '            pass\n',
     {"KOL 1", "KOL 2", "KOL 4", "KOL 5"}),
    ("M-2 kur cagri yeri kapanir",
     '        zincir_halka(y, "GENESIS", "kurulum" + ek)\n        _gitkeep_yaz(y)\n',
     '        zincir_halka(y, "GENESIS", "kurulum" + ek)\n', {"KOL 1", "KOL 4", "KOL 5"}),
    ("M-3 devral cagri yeri kapanir",
     '    print("  cipa + defterler + zincir kuruldu (%s)" % hdir_rel)\n    _gitkeep_yaz(y)\n',
     '    print("  cipa + defterler + zincir kuruldu (%s)" % hdir_rel)\n', {"KOL 2"}),
    ("M-4 tekrar kur da yazar (onarim)",
     '        zincir_halka(y, "KURULUM", "hafiza.py kur (idempotent tazeleme)" + ek)\n',
     '        _gitkeep_yaz(y)\n        zincir_halka(y, "KURULUM", "hafiza.py kur (idempotent tazeleme)" + ek)\n', {"KOL 3"}),
    ("M-5 'xb' -> 'wb' (var olani ezer)",
     '            with open(os.path.join(d, ".gitkeep"), "xb"):\n', '            with open(os.path.join(d, ".gitkeep"), "wb"):\n',
     {"KOL 4"}),
    ("M-6 kapi eksik .gitkeep'i bulgu yapar",
     '        if not os.path.lexists(d):\n            fail("H16", "%s YOK: %s" % (ad, d))\n',
     '        if not os.path.lexists(d):\n            fail("H16", "%s YOK: %s" % (ad, d))\n'
     '        elif not os.path.lexists(os.path.join(d, ".gitkeep")):\n'
     '            fail("H16", "%s .gitkeep YOK: %s" % (ad, d))\n', {"KOL 3"}),
    # H16 klonda hafiza dizini icin .gitkeep'i GOZLEMEZ (dizin her zaman defter dosyalariyla dolu ve izlenir) —
    # bu kol klon hukmuyle degil, dort `.gitkeep`in IZLENDIGI MULK kontroluyle isirir.
    ("M-7 hafiza dizini dortlunun disinda kalir",
     '    for d in (y.kararlar, y.gunluk, y.gunluk_ars, y.h):\n', '    for d in (y.kararlar, y.gunluk, y.gunluk_ars):\n',
     {"KOL 1", "KOL 2", "KOL 4"}),
    ("M-8 yazim hatasi FATAL olur (UYARI kalkar)",
     '        except OSError as e:\n'
     '            print("UYARI: .gitkeep yazilamadi (%s): %s — taze klonda [H16] bu dizin icin YOK cikabilir"\n'
     '                  % (_rel(d, y.kok), e), file=sys.stderr)\n',
     '        except OSError:\n            raise\n', {"KOL 5"}),
    ("M-9 H4 havuzu .gitkeep'i ad sayar",
     '            if f == ".gitkeep":\n                continue\n', '            pass\n', {"KOL 6"}),
    ("M-10 H12 git tarihi .gitkeep'i defter sayar",
     '    yollar += [":(exclude,glob)**/.gitkeep"]\n', '    pass\n', {"KOL 7"}),
]


def _sabotajli_motor(kaynak, ankor, yerine, taban, ad):
    n = kaynak.count(ankor)
    if n != 1:
        raise Kurulamadi("%s: capa motorda %d kez gecti (1 olmali): %r" % (ad, n, ankor.strip()[:70]))
    yeni = kaynak.replace(ankor, yerine, 1)
    try:
        compile(yeni, "<mutant-%s>" % ad[:3], "exec")
    except SyntaxError as e:
        raise Kurulamadi("%s: sabotajli motor derlenmiyor: %s" % (ad, e))
    d = tempfile.mkdtemp(prefix="gkm_", dir=taban)
    p = os.path.join(d, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(yeni)
    return p


def _sil(yol):
    """Harness'in KENDI gecici dizinini SIL (salt-okunur git objeleri dahil; Windows)."""
    def onar(fonk, p, *_):
        try:
            os.chmod(p, stat.S_IRWXU)
            fonk(p)
        except OSError:
            pass
    shutil.rmtree(yol, **({"onexc": onar} if sys.version_info >= (3, 12) else {"onerror": onar}))


def main():
    yol = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN)
    try:
        kaynak = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok (bu mutant kur -> commit -> KLON zincirini olcer).")
        return 2
    print(CIZGI)
    print("GITKEEP MUTANTI (B2) — motor: %s · platform: %s" % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="gkmut_")
    try:
        try:
            motorlar = [("temiz", yol, set())]
            for ad, ankor, yerine, beklenen in SABOTAJLAR:
                motorlar.append((ad, _sabotajli_motor(kaynak, ankor, yerine, taban, ad), beklenen))

            def kos_hepsi(item):
                ad, motor, _ = item
                d = os.path.join(taban, "v%d" % motorlar.index(item))
                os.makedirs(d)
                return tum_kollar(motor, d)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
                sonuclar = list(ex.map(kos_hepsi, motorlar))
        except Kurulamadi as e:
            print("SONUC: OLCULEMEDI — %s" % e)
            return 2
        except subprocess.TimeoutExpired as e:
            print("SONUC: OLCULEMEDI — zaman asimi (%s sn)" % e.timeout)
            return 2

        kacan = []
        temiz = sonuclar[0]
        uygulanmaz = sorted(k for k, (ok, _) in temiz.items() if ok is None)
        print("  TEMIZ MOTOR (olculen kollar YESIL olmali):")
        for kol in sorted(temiz):
            ok, ay = temiz[kol]
            print("    %s  %-5s %s" % ("~" if ok is None else ("+" if ok else "!"), kol, ay))
            if ok is False:
                kacan.append("temiz/" + kol)
        if kacan:
            print(CIZGI)
            print("SONUC: KIRMIZI — temiz motorda kol(lar) BEKLENMEDIK: %s" % ", ".join(kacan))
            return 1
        print("\n  SABOTAJLAR (her biri BEKLENEN kolu — ve yalniz onu — KIRMIZI yakmali):")
        isiran = uygulanmaz_sabotaj = 0
        for (ad, motor, beklenen), s in zip(motorlar[1:], sonuclar[1:]):
            beklenen_olculen = set(beklenen) - set(uygulanmaz)
            if not beklenen_olculen:
                uygulanmaz_sabotaj += 1
                print("    %-46s -> UYGULANMAZ  (beklenen kol %s bu ortamda olculemez)"
                      % (ad, ", ".join(sorted(beklenen))))
                continue
            kirmizi = {k for k, (ok, _) in s.items() if ok is False}
            isirdi = kirmizi == beklenen_olculen
            print("    %-46s -> %s  (kirmizi: %s · beklenen: %s)"
                  % (ad, "ISIRDI ✓" if isirdi else "KACTI ✗", ", ".join(sorted(kirmizi)) or "HICBIRI",
                     ", ".join(sorted(beklenen_olculen))))
            for k in sorted(kirmizi):          # KANIT: kirmizi yanan kolun ham ayrintisi (ISIRDI da olsa)
                print("        ! %s %s" % (k, s[k][1][:150]))
            if isirdi:
                isiran += 1
            else:
                kacan.append(ad)
        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — sabotaj beklenen kolu yakmadi: %s" % ", ".join(kacan))
            return 1
        print("SONUC: YESIL — %d kol temiz motorda YESIL (%d UYGULANMAZ), %d sabotajin %d'i BEKLENEN kolu yakti (%d UYGULANMAZ)."
              % (len(temiz) - len(uygulanmaz), len(uygulanmaz), len(SABOTAJLAR), isiran, uygulanmaz_sabotaj))
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

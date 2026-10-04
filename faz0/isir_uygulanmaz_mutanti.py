#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — isir UYGULANMAZ MUTANTI (KALEM 1, besli-paket/IS_EMRI_UYGULANMAZ.md).

NEDEN VAR (olculdu 7 Eyl 2026, A/B kontrolu: `64940f26` vs `fe01df60`,
besli-paket/OLCUM_RAPORU_7EYL_ISIR_GIT.md)
  `t_y42`'nin proje fabrikasi `yeni()` `git init` YAPMIYOR. Onceki turde (`isir`e
  `mutant_git` kolu eklenirken) git'siz projede M-H12g/M-H14g KURULAMIYORDU ve
  bu, mevcut `kurulamayan`/SINANMADI mekanizmasina dusuyordu — dogru gorunen ama
  YAN ETKISI OLCULMEMIS bir uygulama: git'i OLMAYAN HER projede `isir` artik 0
  donduremiyordu (`t_y42` 58/58 -> 56 gecti, 2 kaldi REGRESYONU; `readme_mutanti`
  bunu CI'da yakalardi).

  Duzeltme (IS_EMRI_UYGULANMAZ.md KALEM 1): YENI bir sinif — UYGULANMAZ.
  `mutant_git`, PROJEDE git OLMADIGI icin bir kolu kuramiyorsa `MutantUygulanmaz`
  firlatir; bu SINANMADI DEGILDIR — kapi korlugu da degildir, olcum ekseni bu
  projede yoktur. Cikis kodunu ETKILEMEZ, "kosulan mutant" sayisina GIRMEZ. Git
  VARKEN kurulum yine de bozulursa (ör. `.git` bozuk/gecersiz) davranis
  DEGISMEDI: SINANMADI + exit 2 BIREBIR korunur — UYGULANMAZ bir KACIS KAPISI
  DEGILDIR.

NE OLCER — DORT KOL
  KOL 1 (POZITIF KONTROL) — git'SIZ proje: kur->not->derle->isir -> exit 0,
      ciktida TAM UC 'UYGULANMAZ' satiri VAR (M-H12g/M-H14g/M-H9 — M-H9 TEK TANIK
      turunda, IS_EMRI_TEK_TANIK_ISIR.md, eklendi), SINANMADI sayisi bu kollari
      ICERMEZ (0).
  KOL 2 (GIT'Li KORUNUR) — AYNI akis git'Li bir projede -> 81/81 exit 0,
      M-H12g, M-H14g VE M-H9 ISIRDI.
  KOL 3 (SINANMADI KORUNUR) — git VAR (`.git` dizin olarak MEVCUT) ama GERCEK
      BIR DEPO DEGIL (bos dizin, ne HEAD ne objects/refs) -> `_git_kokte_mi`
      yine de True doner (doktrin: "icerigi COP ise bile True doner") ama
      gercek git komutlari (add/commit) BASARISIZ olur -> SINANMADI (>=2) +
      exit 2. UYGULANMAZ burada bir KACIS KAPISI OLMAMALI.
  KOL 4 (MUTANT) — UYGULANMAZ/SINANMADI ayrimi KAYNAKTAN sokulur (UYGULANMAZ
      da `kurulamayan`'a duser) -> KOL 1'in POZITIF KONTROLU (git'siz proje)
      artik exit 2 basar -> ISIRDI (kapinin var olmasi, ayrimin GERCEKTEN
      olculdugunun kanitidir).

W1 — GECICI DIZIN SIZINTISI (Onur kilidi 4 Eki 2026, besli-paket/IS_EMRI_WIN_TEMP_SIZINTI.md) · DORT KOL DAHA
  Olculdu: `isir`in gecici kopyalari `shutil.rmtree(..., ignore_errors=True)` ile siliniyordu; Windows'ta
  salt-okunur git objeleri (0444), POSIX'te yazilamaz alt dizin silinemez ve hata YUTULUR: tek bir
  `hook_mutanti.py` kosumu 9 artik, %TEMP%'te 9.179 birikmis. Motor artik tek yardimciyi (`_gecici_sil`)
  kullanir: hata gelince girdiyi yazilabilir yapip yeniden dener, yine olmazsa stderr'e TEK satir
  `GECICI DIZIN SILINEMEDI: <yol>` (stdout'a YAZMAZ, cikis kodu sozlesmesi degismez). Her kol IZOLE
  `TMPDIR/TEMP/TMP` ile sayar (makinedeki baska artik karismaz).
  KOL 5 (UCTAN UCA) — git'li proje + `.git` icinde kilitli dizin/salt-okunur dosya (Windows'ta ayrica
      commit'lerin salt-okunur objeleri): `isir` exit 0, 81/81, izole TMP'de artik 0, stderr'de uyari YOK.
  KOL 6 (ONARIM + UYARI, surec ici) — motor `importlib` ile yuklenir; salt-okunur dosyali + yazilamaz
      alt dizinli agac `_gecici_sil` ile TAMAMEN silinir (ses yok); `os.chmod` etkisizlestirilince agac KALIR,
      stderr'e TEK uyari satiri, stdout bos. (Linux'ta root ise B kolu OLCULEMEDI: root izni asar.)
  KOL 7 (CAGRI YERLERI, statik) — motorda `rmtree(..., ignore_errors=True)` cagrisi YOK; `_gecici_sil(`
      cagrisi TAM 5 (mutant, mutant_git, komut_sinamasi, k_devir, _skill_kur_yerlestir).
  KOL 8 (MUTANTLAR, her duzeltmeye AYRI) — M-2 yardimci `ignore_errors=True`ya geri doner: KOL 6 artik KALIR
      diye ISIRIR VE uctan uca isir de izole TMP'de artik BIRAKIR (KOL 5 kor degil) · M-3 uyari satiri sokulur:
      KOL 6 sessizligi gorur · M-4 bir cagri yeri eski satira doner: KOL 7 gorur.

CIKIS KODU  0 tum kollar temiz VE mutantlar ISIRDI · 1 en az bir kol BEKLENMEDIK
            / mutant KACTI · 2 OLCULEMEDI (git yok, motor okunamadi, kurulum
            basarisiz — kapi hukmu DEGIL)
"""
import ast
import io
import json
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

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def kos(motor, arglar, kok, timeout=300):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _kur_ve_derle(motor, kok):
    """kur -> not -> derle. Uc adim da git'e BAKMAZ; git'siz/git'li/bozuk-git
    projede AYNI sekilde calismalidir (bu fonksiyonun KENDI on-kosulu)."""
    for adim in (["kur", "--ad", "UYGMUT"],
                 ["not", "--konu=genel-durum", "--metin=isir uygulanmaz mutanti ilk kayit"],
                 ["derle"]):
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s basarisiz: %s" % (adim[0], c.strip().split("\n")[-1][:160]))


def hal_git_yok(motor, kok):
    os.makedirs(kok, exist_ok=True)
    _kur_ve_derle(motor, kok)
    return kok


def hal_git_li(motor, kok):
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run(["git", "init", "-q", kok], capture_output=True)
    if r.returncode != 0:
        raise Kurulamadi("git init basarisiz")
    _kur_ve_derle(motor, kok)
    return kok


def hal_git_bozuk(motor, kok):
    """`.git` bir DIZIN olarak VAR (`_git_kokte_mi` bu yuzden True doner — bu,
    doktrinin KENDISIDIR: 'icerigi cop ise bile True doner') ama HEAD/objects/
    refs YOK — gercek bir depo DEGIL. Gercek git komutlari (add/commit) exit
    128 ('fatal: not a git repository') ile basarisiz olur (elle dogrulandi)."""
    os.makedirs(os.path.join(kok, ".git"), exist_ok=True)
    _kur_ve_derle(motor, kok)
    return kok


_UYGULANMAZ_SATIR = re.compile(r"^\s*M-H(?:1[24]g|9)\s.*->\s*UYGULANMAZ", re.M)
_ISIRDI_H12G = re.compile(r"^\s*M-H12g.*->\s*ISIRDI", re.M)
_ISIRDI_H14G = re.compile(r"^\s*M-H14g.*->\s*ISIRDI", re.M)
_ISIRDI_H9 = re.compile(r"^\s*M-H9\s.*->\s*ISIRDI", re.M)
_SINANMADI_SAYI = re.compile(r"·\s*(\d+)\s+SINANMADI")
_KOSULAN_ORAN = re.compile(r"(\d+)/(\d+) kosulan mutant ISIRIYOR")


def _kol_olc(motor, kurucu, taban_ad, taban):
    kok = os.path.join(taban, taban_ad)
    kok = kurucu(motor, kok)
    return kos(motor, ["isir"], kok)


# ---------------------------------------------------------------------------------------------------
# W1 — GECICI DIZIN TEMIZLIGI (motorun `_gecici_sil` yardimcisi)
# ---------------------------------------------------------------------------------------------------
_UYARI = "GECICI DIZIN SILINEMEDI: "
# MUTANT capalari — motorda TAM 1 kez gecmeli (degilse OLCULEMEDI: motor degistiyse SABOTAJ DA DEGISMELI)
_ANKOR_YARDIMCI = ('    shutil.rmtree(yol, **({"onexc": onar} if sys.version_info >= (3, 12) '
                   'else {"onerror": onar}))\n')
_ANKOR_UYARI = '        print("GECICI DIZIN SILINEMEDI: %s" % yol, file=sys.stderr)\n'
_ANKOR_CAGRI = ("            return (etiketli and parca_ok), k, c\n"
                "        finally:\n"
                "            _gecici_sil(tmp)\n")

# Surec ici sinama (motor importlib ile yuklenir). Kaynakta ters bolu YOK (arac tuzagi).
_COCUK = '''
import contextlib, importlib.util, io, json, os, stat, sys
motor, kok = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("hafiza_w1", motor)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def agac(ad):
    d = os.path.join(kok, ad)
    os.makedirs(os.path.join(d, "kilitli_dizin"))
    f1 = os.path.join(d, "salt_okunur.txt")
    with open(f1, "w") as f:
        f.write("x")
    os.chmod(f1, stat.S_IREAD)
    f2 = os.path.join(d, "kilitli_dizin", "ic.txt")
    with open(f2, "w") as f:
        f.write("y")
    os.chmod(os.path.join(d, "kilitli_dizin"), stat.S_IREAD | stat.S_IEXEC)
    return d
def calistir(yol):
    o, e = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
        m._gecici_sil(yol)
    return o.getvalue(), e.getvalue()
a = agac("a")
oa, ea = calistir(a)
b = agac("b")
gercek = os.chmod
os.chmod = lambda *x, **k: None
try:
    ob, eb = calistir(b)
finally:
    os.chmod = gercek
print(json.dumps({"a_kalan": os.path.lexists(a), "a_out": oa, "a_err": ea,
                  "b_kalan": os.path.lexists(b), "b_out": ob, "b_err": eb,
                  "root": hasattr(os, "geteuid") and os.geteuid() == 0}))
'''


def _sil(yol):
    """Harness'in KENDI gecici dizinini SIL (salt-okunur dosya / kilitli dizin dahil). Motordan BAGIMSIZ
    kopya (harness temizligi sinanan koda dayanmasin). Kokun USTUNE ve sembolik baglantiya chmod YOK."""
    yol = os.path.normpath(yol)

    def onar(fonk, p, *_):
        hedef = [p] if not os.path.islink(p) else []
        if os.path.dirname(p).startswith(yol):
            hedef.append(os.path.dirname(p))
        for h in hedef:
            try:
                os.chmod(h, stat.S_IRWXU)
            except OSError:
                pass
        try:
            fonk(p)
        except OSError:
            pass
    shutil.rmtree(yol, **({"onexc": onar} if sys.version_info >= (3, 12) else {"onerror": onar}))
    if os.path.lexists(yol):
        print("GECICI DIZIN SILINEMEDI: %s" % yol, file=sys.stderr)


def hal_git_li_kilitli(motor, kok):
    """KOL 2'nin git'li projesi + `.git` ICINDE kilitli dizin (POSIX: yazilamaz) ve salt-okunur dosya
    (Windows: salt-okunur bit). `mutant_git` `.git`i kopyalar -> temizlik basarisiz olursa artik kalir."""
    hal_git_li(motor, kok)
    d = os.path.join(kok, ".git", "kilitli_dizin")
    os.makedirs(d)
    f = os.path.join(d, "ic.txt")
    with open(f, "w") as fh:
        fh.write("kilitli")
    os.chmod(f, stat.S_IREAD)
    os.chmod(d, stat.S_IREAD | stat.S_IEXEC)
    return kok


def _kos_izole(motor, kok, izole, timeout=900):
    """`isir`i IZOLE TMPDIR/TEMP/TMP ile kosar; (exit, cikti, izole dizindeki girdiler)."""
    os.makedirs(izole, exist_ok=True)
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8", TMPDIR=izole, TEMP=izole, TMP=izole)
    r = subprocess.run([sys.executable, "-X", "utf8", motor, "isir", "--kok", kok],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or ""), sorted(os.listdir(izole))


def _kol5(motor, taban, ad):
    """UCTAN UCA: kilitli fixture + izole TMP -> (bulgular, ozet)."""
    kok = hal_git_li_kilitli(motor, os.path.join(taban, ad))
    k, c, girdiler = _kos_izole(motor, kok, os.path.join(taban, ad + "t"))
    artik = [g for g in girdiler if g.startswith("hafiza_isir_")]
    m = _KOSULAN_ORAN.search(c)
    if k != 0 or not m or m.group(1) != "81":
        for x in [x for x in c.splitlines() if "KURULAMADI" in x][:6]:      # TANI: hangi mutant dustu
            print("      · %s" % x.strip()[:170])
    return k, m, artik, girdiler, (_UYARI in c)


def _kol6(motor, taban, ad):
    """SUREC ICI: onarim + uyari yolu. Doner (bulgular, olculemedi_sebebi)."""
    d = tempfile.mkdtemp(prefix="w1k6_", dir=taban)
    cp = os.path.join(d, "cocuk.py")
    with io.open(cp, "w", encoding="utf-8", newline="\n") as f:
        f.write(_COCUK)
    r = subprocess.run([sys.executable, "-X", "utf8", cp, motor, os.path.join(d, "i")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=300)
    try:
        o = json.loads((r.stdout or "").strip().split("\n")[-1])
    except (ValueError, IndexError):
        raise Kurulamadi("%s: cocuk surec ciktisi okunamadi: %s" % (ad, ((r.stderr or "") + (r.stdout or ""))[-200:]))
    if o["root"]:
        return [], "root olarak kosuyor — izin engeli asilir, onarim/uyari yolu OLCULEMEZ"
    hat = []
    if o["a_kalan"]:
        hat.append("onarim yolu agaci SILEMEDI (salt-okunur/kilitli dizin kaldi)")
    if o["a_out"] or o["a_err"]:
        hat.append("onarilabilir silmede SES var: %r" % (o["a_out"] + o["a_err"])[:80])
    satir = [x for x in o["b_err"].splitlines() if x.strip()]
    if not o["b_kalan"]:
        hat.append("kurtarilamayan agac silinmis (kurulum etkisiz?)")
    if o["b_out"]:
        hat.append("uyari STDOUT'a yazildi: %r" % o["b_out"][:80])
    if len(satir) != 1 or not satir[0].startswith(_UYARI):
        hat.append("stderr'de TAM BIR '%s...' satiri yok: %r" % (_UYARI, o["b_err"][:100]))
    return hat, None


def _kol7(kaynak):
    """STATIK: (rmtree(ignore_errors=True) cagri sayisi, `_gecici_sil(` cagri sayisi)."""
    ig = cagri = 0
    for n in ast.walk(ast.parse(kaynak)):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        if (isinstance(f, ast.Attribute) and f.attr == "rmtree"
                and any(k.arg == "ignore_errors" and isinstance(k.value, ast.Constant)
                        and k.value.value is True for k in n.keywords)):
            ig += 1
        if isinstance(f, ast.Name) and f.id == "_gecici_sil":
            cagri += 1
    return ig, cagri


def _mutant_yaz(s, ankor, yerine, taban, ad):
    n = s.count(ankor)
    if n != 1:
        raise Kurulamadi("%s: capa %d yerde gecti (1 olmali): %r" % (ad, n, ankor.strip()[:70]))
    yeni = s.replace(ankor, yerine, 1)
    compile(yeni, "<mutant-%s>" % ad, "exec")
    d = tempfile.mkdtemp(prefix="w1m_", dir=taban)
    p = os.path.join(d, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(yeni)
    return p


def _w1_kollari(yol, s, taban):
    """KOL 5-8. Doner: (kod, kacanlar): kod None = tamam, 1 = BEKLENMEDIK/KACTI, 2 = OLCULEMEDI."""
    print("\n--- W1 GECICI DIZIN TEMIZLIGI (izole TMPDIR/TEMP/TMP; makinedeki baska artik karismaz) ---")
    kacan = []
    try:
        # KOL 5 — uctan uca, temiz motor
        k5, m5, artik5, girdi5, uyari5 = _kol5(yol, taban, "k5")      # kisa ad: Windows 260 sinirina pay
        print("  KOL 5 (uctan uca)    : isir exit=%d · %s · izole TMP'de hafiza_isir_* artik=%d (toplam girdi %d)"
              % (k5, m5.group(0) if m5 else "oran YOK", len(artik5), len(girdi5)))
        for x, ok in (("isir exit 0 degil (%d)" % k5, k5 == 0),
                      ("81/81 degil (%s)" % (m5.group(0) if m5 else "YOK"),
                       bool(m5) and m5.group(1) == "81" == m5.group(2)),
                      ("izole TMP'de ARTIK var: %s" % ", ".join(artik5[:4]), not artik5),
                      ("temiz motor 'GECICI DIZIN SILINEMEDI' uyarisi basti", not uyari5)):
            if not ok:
                print("      ! KOL 5: %s" % x)
                kacan.append("KOL 5")
        # KOL 6 — surec ici onarim + uyari
        hat6, olc6 = _kol6(yol, taban, "KOL 6")
        if olc6:
            print("  KOL 6 (onarim+uyari) OLCULEMEDI: %s" % olc6)
            return 2, kacan
        print("  KOL 6 (onarim+uyari) : %s" % ("temiz" if not hat6 else "BEKLENMEDIK"))
        for x in hat6:
            print("      ! KOL 6: %s" % x)
            kacan.append("KOL 6")
        # KOL 7 — statik
        ig7, cagri7 = _kol7(s)
        print("  KOL 7 (cagri yerleri): rmtree(ignore_errors=True)=%d (0 olmali) · _gecici_sil( cagrisi=%d (5 olmali)"
              % (ig7, cagri7))
        if ig7 != 0 or cagri7 != 5:
            print("      ! KOL 7: cagri yerleri BEKLENEN degil")
            kacan.append("KOL 7")
        if kacan:
            return 1, kacan
        # KOL 8 — mutantlar
        print("\n  KOL 8 (W1 MUTANTLARI — kapinin var olmasi ISIRDIGI anlamina gelmez):")
        # M-2: yardimci ignore_errors=True'ya geri doner -> KOL 6 + uctan uca isir
        mp = _mutant_yaz(s, _ANKOR_YARDIMCI, "    shutil.rmtree(yol, ignore_errors=True)\n", taban, "M-2")
        hat2, _ = _kol6(mp, taban, "M-2 / KOL 6")
        k2, m2, artik2, girdi2, _u = _kol5(mp, taban, "m2")
        bit2 = bool(hat2) and bool(artik2)
        print("  M-2 yardimci ignore_errors=True'ya doner  -> %s  (KOL 6: %s · uctan uca izole TMP artik=%d)"
              % ("ISIRDI ✓" if bit2 else "KACTI ✗", "yakaladi" if hat2 else "GORMEDI", len(artik2)))
        if not bit2:
            kacan.append("M-2")
        # M-3: uyari satiri sokulur -> KOL 6 sessizligi gorur
        mp = _mutant_yaz(s, _ANKOR_UYARI, "        pass\n", taban, "M-3")
        hat3, _ = _kol6(mp, taban, "M-3 / KOL 6")
        print("  M-3 uyari satiri sokulur                  -> %s  (KOL 6: %s)"
              % ("ISIRDI ✓" if hat3 else "KACTI ✗", "yakaladi" if hat3 else "GORMEDI"))
        if not hat3:
            kacan.append("M-3")
        # M-4: bir cagri yeri eski satira doner -> KOL 7
        mp = _mutant_yaz(s, _ANKOR_CAGRI, _ANKOR_CAGRI.replace("_gecici_sil(tmp)", "shutil.rmtree(tmp, ignore_errors=True)"),
                         taban, "M-4")
        with io.open(mp, encoding="utf-8", newline="") as f:
            ig4, cagri4 = _kol7(f.read())
        bit4 = ig4 != 0 or cagri4 != 5
        print("  M-4 bir cagri yeri eski satira doner      -> %s  (KOL 7: ignore_errors=%d · _gecici_sil(=%d)"
              % ("ISIRDI ✓" if bit4 else "KACTI ✗", ig4, cagri4))
        if not bit4:
            kacan.append("M-4")
    except Kurulamadi as e:
        print("  W1 kollari OLCULEMEDI: %s" % e)
        return 2, kacan
    return (1 if kacan else None), kacan


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
    print("ISIR UYGULANMAZ MUTANTI (KALEM 1) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="isir_uygulanmaz_")
    try:
        bulgu = []

        # ---- KOL 1: POZITIF KONTROL (git YOK) ------------------------------
        try:
            k1, c1 = _kol_olc(yol, hal_git_yok, "h1_git_yok", taban)
        except Kurulamadi as e:
            print("  KOL 1 (git YOK)   OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 1 (git YOK)      : isir exit=%d" % k1)
        if k1 != 0:
            bulgu.append("KOL 1: isir exit %d (0 bekleniyordu)" % k1)
        n_u = len(_UYGULANMAZ_SATIR.findall(c1))
        if n_u != 3:
            bulgu.append("KOL 1: UYGULANMAZ satiri %d (M-H12g/M-H14g/M-H9 = 3 bekleniyordu)" % n_u)
        m = _SINANMADI_SAYI.search(c1)
        if not m or int(m.group(1)) != 0:
            bulgu.append("KOL 1: SINANMADI sayisi 0 degil (%s) — UYGULANMAZ SINANMADI'ya "
                         "sizmis olabilir" % (m.group(1) if m else "YOK"))

        # ---- KOL 2: GIT'Li KORUNUR ------------------------------------------
        try:
            k2, c2 = _kol_olc(yol, hal_git_li, "h2_git_li", taban)
        except Kurulamadi as e:
            print("  KOL 2 (git VAR)   OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 2 (git VAR)      : isir exit=%d" % k2)
        if k2 != 0:
            bulgu.append("KOL 2: isir exit %d (0 bekleniyordu)" % k2)
        m = _KOSULAN_ORAN.search(c2)
        if not m or m.group(1) != "81" or m.group(2) != "81":
            bulgu.append("KOL 2: '81/81 kosulan mutant' degil (%s)" % (m.group(0) if m else "YOK"))
        if not _ISIRDI_H9.search(c2):
            bulgu.append("KOL 2: M-H9 ISIRDI degil")
        if not _ISIRDI_H12G.search(c2):
            bulgu.append("KOL 2: M-H12g ISIRDI degil")
        if not _ISIRDI_H14G.search(c2):
            bulgu.append("KOL 2: M-H14g ISIRDI degil")

        # ---- KOL 3: SINANMADI KORUNUR (git BOZUK) ---------------------------
        try:
            k3, c3 = _kol_olc(yol, hal_git_bozuk, "h3_git_bozuk", taban)
        except Kurulamadi as e:
            print("  KOL 3 (git BOZUK) OLCULEMEDI: %s" % e)
            return 2
        print("  KOL 3 (git BOZUK)    : isir exit=%d" % k3)
        if k3 != 2:
            bulgu.append("KOL 3: isir exit %d (2 bekleniyordu — SINANMADI korunmali)" % k3)
        m = _SINANMADI_SAYI.search(c3)
        if not m or int(m.group(1)) < 2:
            bulgu.append("KOL 3: SINANMADI sayisi < 2 (%s) — UYGULANMAZ bir KACIS KAPISI "
                         "olmus olabilir" % (m.group(1) if m else "YOK"))
        if _UYGULANMAZ_SATIR.search(c3):
            bulgu.append("KOL 3: git BOZUKKEN yanlislikla UYGULANMAZ basildi (SINANMADI olmaliydi)")

        for x in bulgu:
            print("      ! %s" % x)
        if bulgu:
            print("\nSONUC: KIRMIZI — temiz surumun kollari BEKLENMEDIK.")
            return 1

        # ---- KOL 4: MUTANT ----------------------------------------------------
        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        ANKOR = "            uygulanmaz.append((ad, kapi, str(e)))\n"
        n = s.count(ANKOR)
        if n != 1:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: capa %d yerde "
                  "gecti (1 olmali): %r" % (n, ANKOR.strip()))
            return 2
        yeni = s.replace(ANKOR, "            kurulamayan.append((ad, kapi, str(e)))  "
                                "# MUTANT: ayrim sokuldu\n", 1)
        try:
            compile(yeni, "<mutant>", "exec")
        except SyntaxError as e:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: "
                  "sabotajli motor derlenmiyor: %s" % e)
            return 2
        mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
        mp = os.path.join(mdir, "hafiza.py")
        with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
            f.write(yeni)
        try:
            km, cm = _kol_olc(mp, hal_git_yok, "hm_git_yok", taban)
        except Kurulamadi as e:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   OLCULEMEDI: %s" % e)
            return 2
        kacan = []
        if km == 2:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   -> ISIRDI ✓  "
                  "(git'siz proje sabotajli motorda exit %d verdi, KOL 1 artik KIRMIZI)" % km)
        else:
            print("  M-1 UYGULANMAZ/SINANMADI ayrimi sokulur   -> KACTI ✗  "
                  "(ayrim sokulunce de exit %d kaldi — KOL 1 bunu HIC OLCMUYOR)" % km)
            kacan.append("M-1")

        # ---- KOL 5-8: W1 gecici dizin temizligi -----------------------------------
        kod, w1_kacan = _w1_kollari(yol, s, taban)
        if kod == 2:
            return 2
        kacan += w1_kacan
        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — kol/mutant beklendigi gibi olculmedi: %s" % ", ".join(kacan))
            return 1
        print("SONUC: YESIL — sekiz kol da BEKLENDIGI GIBI, mutantlar AYRI eksenlerde ISIRDI.")
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

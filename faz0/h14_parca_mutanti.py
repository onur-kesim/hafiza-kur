#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — H14 PARCA MUTANTI (besli-paket/IS_EMRI_H14_KOMUT_SATIRI.md, 6 Eki 2026, Onur kilidi sik (a)).

NEDEN VAR (olculdu, mozilla/fxa kopyasi, 8.335 izlenen dosya, yollarin toplami ~509.000 kr)
  `kapi` exit 3 `FileNotFoundError: [WinError 206]` verdi: `_h14_en_yeni` git'e butun temiz yollari TEK komut
  satirinda (400 yol'luk obeklerle) gonderiyordu; Windows komut satiri ~32.767 karakter. Duzeltme: yollar girdi
  SIRASIYLA parcalanir, her parcada karakter toplami (+1 ayrac) <= `_GIT_YOL_BUTCE` (8.000), sonuc parcalarin EN
  BUYUK `%ct`'si (`_git_son_ct`). Bu betik o duzeltmeyi uc EKSENDE sinar.

NEDEN AYRI BETIK (yeni `capraz.yml` isi): bu kollar motoru KUTUPHANE olarak ice alir (`_git_son_ct`e girdi SIRASI ve
  yol UZUNLUKLARI elle verilir; git cagrilari kaydedilir) — `kapi`yi altprosesle kosan mevcut H14 betikleri girdi sirasini
  (`os.walk`: NTFS sirali, Linux keyfi) KONTROL EDEMEZ ve "tam butce" siniri komut satirindan gorunmez. Gercek git deposu
  kullanilir; tarihler `GIT_COMMITTER_DATE` ile sabittir; beklentiler FIKSTURDEN elle yazilidir (motor sabitinden degil:
  paylasilan kural = paylasilan korluk).

UC KOL (her biri AYRI etiketli eksen)
  H14-PARCA-MAX    >=3 parcaya bolunecek kadar yol (450 x 71 kr); EN YENI commit'i alan dosya SON parcada ->
                   sonuc = o dosyanin tarihi (PMAX-TARIH), parca sayisi >= 3 (PMAX-PARCA), HER git cagrisinda yol
                   toplami <= 8.000 (PMAX-BUTCE). Sabotaj: yalniz ilk parcanin sonucu alinir.
  H14-PARCA-SINIR  butceye TAM esit (100 yol x 80 = 8.000) ve +1 asan (8.001) yol kumesi: ikisinde de dogru tarih
                   (PSINIR-TARIH); esit kume TEK cagri, +1 kume IKI cagri (son yol 1 kr uzun) (PSINIR-SAYI). Sabotaj: `>` -> `>=` (esit kume
                   bolunur: SAYI ekseni isirir, TARIH eksenine DOKUNMAZ — bolme maksimumu degistirmez) ve ayrac sayilmaz
                   (+1 kume bolunmez: SAYI).
  H14-WIN-UZUN     YALNIZ WINDOWS'ta isirir (beyanli): toplam yol uzunlugu > 32.767 (kisa izole TEMP, tek yol < 260) olan
                   gercek bir projede `kapi` exit != 3 ve `H14:` satiri basili (PWIN). Sabotaj: butce sonsuz (tek cagri) ->
                   Windows'ta exit 3. Linux/macOS'ta sinir YOK: kol `OLCULEMEDI: bu platformda sinir yok` BEYAN eder
                   (sessiz YESIL degil; hukum `YESIL (SINIRLI)`).

ORTUSME (raporlanir, gizlenmez): PARCA-MAX sabotaji ve WIN-UZUN sabotaji (`butce sonsuz`) ayni "tek cagri" davranisini
  gorebilir — her sabotajin tum kollarda atesledigi etiketler basilir; kendi ekseni disindakiler ORTUSME'dir.

CIKIS KODU  0 tum kollar temiz + olculebilen her sabotaj ISIRDI · 1 kol BEKLENMEDIK / sabotaj KACTI ·
            2 OLCULEMEDI (git yok, capa uymadi, duzenek kurulamadi)
"""
import datetime as _dt
import importlib.util
import io
import os
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
            pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
BUTCE = 8000            # BILEREK motordan okunmaz: beklenti fiksturden/elle (paylasilan kural = paylasilan korluk)
ESKI = "2020-01-01T12:00:00"
YENI = "2021-06-15T12:00:00"


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def _ts(iso):
    return int(_dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=_dt.timezone.utc).timestamp())


def _git(kok, *args, tarih=None):
    ortam = dict(os.environ, GIT_AUTHOR_NAME="h14p", GIT_AUTHOR_EMAIL="h14p@example.invalid",
                 GIT_COMMITTER_NAME="h14p", GIT_COMMITTER_EMAIL="h14p@example.invalid", GIT_CONFIG_NOSYSTEM="1")
    if tarih:
        ortam["GIT_AUTHOR_DATE"] = ortam["GIT_COMMITTER_DATE"] = tarih + " +0000"
    return subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"] + list(args),
                          capture_output=True, env=ortam)


def _yaz(yol, metin):
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    with io.open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)


def _sil(yol):
    def onar(fonk, p, *_):
        try:
            os.chmod(p, stat.S_IRWXU)
            fonk(p)
        except OSError:
            return
    if sys.version_info >= (3, 12):
        shutil.rmtree(yol, onexc=onar)
    else:
        shutil.rmtree(yol, onerror=onar)


def yukle(motor, ad):
    """Motoru KUTUPHANE olarak yukler (her sabotajli kopya ayri modul adi)."""
    spec = importlib.util.spec_from_file_location(ad, motor)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def kayitli(fonk):
    """`fonk()`i calistirir; `git log -1 --format=%ct` cagrilarini (argv) KAYDEDER, GERCEK git'e aynen iletir."""
    gercek = subprocess.run
    cagrilar = []

    def sar(argv, *a, **k):
        if isinstance(argv, list) and "--format=%ct" in argv and "log" in argv:
            cagrilar.append(list(argv))
        return gercek(argv, *a, **k)
    subprocess.run = sar
    try:
        return fonk(), cagrilar
    finally:
        subprocess.run = gercek


def _cagri_yollari(argv):
    return argv[argv.index("--") + 1:]


def _depo(taban, ad, yollar, yeni_dosya):
    """git deposu: `yollar` ESKI tarihle, ardindan `yeni_dosya` YENI tarihle commit'lenir. DONER kok."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    for y in yollar:
        _yaz(os.path.join(kok, *y.split("/")), "ilk\n")
    _git(kok, "add", "-A")
    if _git(kok, "commit", "-q", "-m", "ilk", tarih=ESKI).returncode != 0:
        raise Kurulamadi("git commit (eski) basarisiz")
    _yaz(os.path.join(kok, *yeni_dosya.split("/")), "yeni\n")
    _git(kok, "add", "-A")
    if _git(kok, "commit", "-q", "-m", "yeni", tarih=YENI).returncode != 0:
        raise Kurulamadi("git commit (yeni) basarisiz")
    return kok


def _yollar_max(n=450):
    """n yol, her biri 71 kr (`veri/` + ad): sirali; SON yol = en yeni commit'i alacak dosya."""
    return ["veri/d%04d_%s.txt" % (i, "x" * 55) for i in range(n)]


def kol_max(h, taban):
    """H14-PARCA-MAX (PMAX-TARIH · PMAX-PARCA · PMAX-BUTCE)."""
    b = []
    yollar = _yollar_max()
    kok = _depo(taban, "pmax", yollar, yollar[-1])
    ct, cagrilar = kayitli(lambda: h._git_son_ct(kok, yollar))
    if ct != _ts(YENI):
        b.append(("PMAX-TARIH", "sonuc %r (beklenen SON parcadaki dosyanin tarihi %d = %s)" % (ct, _ts(YENI), YENI)))
    if len(cagrilar) < 3:
        b.append(("PMAX-PARCA", "git cagrisi %d (>=3 parca bekleniyordu: 450 yol x 71 kr)" % len(cagrilar)))
    asan = [sum(len(y) + 1 for y in _cagri_yollari(c)) for c in cagrilar if
            sum(len(y) + 1 for y in _cagri_yollari(c)) > BUTCE]
    if asan:
        b.append(("PMAX-BUTCE", "parca(lar) butceyi (%d) asti: %r" % (BUTCE, asan)))
    return b


def _yollar_esit(ekstra):
    """100 yol x 80 kr (79 + 1 ayrac) = TAM 8.000; `ekstra` True ise SON yol 1 kr uzar (80 kr -> 81) -> 8.001."""
    yollar = ["veri/e%03d_%s.txt" % (i, "y" * (79 - len("veri/e000_") - len(".txt"))) for i in range(100)]
    assert all(len(y) == 79 for y in yollar), [len(y) for y in yollar][:3]
    if ekstra:
        yollar[-1] = yollar[-1][:-4] + "y.txt"
    return yollar


def kol_sinir(h, taban):
    """H14-PARCA-SINIR (PSINIR-TARIH · PSINIR-SAYI): butceye TAM esit -> 1 cagri; +1 -> 2 cagri; ikisinde de tarih dogru."""
    b = []
    for ad, ekstra, beklenen in (("psesit", False, 1), ("psarti", True, 2)):
        yollar = _yollar_esit(ekstra)
        kok = _depo(taban, ad, yollar, yollar[-1])
        ct, cagrilar = kayitli(lambda: h._git_son_ct(kok, yollar))
        if ct != _ts(YENI):
            b.append(("PSINIR-TARIH", "%s: sonuc %r (beklenen %d)" % (ad, ct, _ts(YENI))))
        if len(cagrilar) != beklenen:
            b.append(("PSINIR-SAYI", "%s: git cagrisi %d (beklenen %d; toplam %d kr, butce %d)"
                      % (ad, len(cagrilar), beklenen, sum(len(y) + 1 for y in yollar), BUTCE)))
    return b


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
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(metin)
    return p, None


def hepsi(motor, taban, ad):
    """UC kolun (WIN yalniz Windows'ta) bulgulari -> [(etiket, mesaj)]; WIN olculemezse etiket `OLCULEMEDI-WIN`."""
    h = yukle(motor, ad)
    return kol_max(h, taban) + kol_sinir(h, taban)


# (ad, etiket, ankor, yeni): ankor motorda TAM 1 kez gecmeli (aksi OLCULEMEDI).
SABOTAJLAR = (
    ("M-PM1 yalniz ILK parcanin sonucu alinir", "PMAX-TARIH",
     "            if en is None or ct > en:\n                en = ct\n",
     "            if en is None:      # MUTANT\n                en = ct\n"),
    ("M-PS1 butce karsilastirmasi `>` -> `>=` (esit kume bolunur)", "PSINIR-SAYI",
     "        if parca and toplam + len(yol) + 1 > butce:\n",
     "        if parca and toplam + len(yol) + 1 >= butce:      # MUTANT\n"),
    ("M-PS2 ayrac SAYILMAZ (+1 kume bolunmez)", "PSINIR-SAYI",
     "        if parca and toplam + len(yol) + 1 > butce:\n",
     "        if parca and toplam + len(yol) > butce:      # MUTANT\n"),
)


def main():
    yol = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN)
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok.")
        return 2
    print(CIZGI)
    print("H14 PARCA MUTANTI — motor: %s · platform: %s" % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="h14p_")
    try:
        try:
            temiz = hepsi(yol, os.path.join(taban, "t"), "h14p_temiz")
        except Kurulamadi as e:
            print("SONUC: OLCULEMEDI — duzenek kurulamadi (arac kusuru, kapi kor DEGIL): %s" % e)
            return 2
        kotu = temiz
        olcul = []
        print("  H14-PARCA-MAX / PARCA-SINIR : %s" % ("TEMIZ" if not kotu else "BEKLENMEDIK"))
        for et, m in kotu:
            print("      ! %s: %s" % (et, m))
        if kotu:
            print("\nSONUC: KIRMIZI — temiz motorun kollari BEKLENMEDIK.")
            return 1
        print("\n--- SABOTAJLAR (her biri KENDI ekseninde ISIRMALI; ortusme raporlanir) ---")
        kacan, olculemeyen = [], []
        for sira, (ad, etiket, ankor, yeni) in enumerate(SABOTAJLAR, 1):
            d = tempfile.mkdtemp(prefix="m%d_" % sira, dir=taban)
            sab, hata = _sabotajli_yaz(s, ankor, yeni, d, "m%d" % sira)
            if sab is None:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, hata))
                return 2
            try:
                atesler = {e for e, _ in hepsi(sab, os.path.join(d, "t"), "h14p_m%d" % sira)}
            except Kurulamadi as e:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, e))
                return 2
            if etiket in atesler:
                ort = sorted(atesler - {etiket})
                print("  %-58s -> ISIRDI ✓  (%s%s)" % (ad, etiket, ("; ortusme: " + ", ".join(ort)) if ort else ""))
            else:
                print("  %-58s -> KACTI ✗  (%s ekseni sabotajda da TEMIZ; atesleyen: %s)"
                      % (ad, etiket, ", ".join(sorted(atesler)) or "hicbiri"))
                kacan.append(ad)
        print(CIZGI)
        if kacan:
            print("SONUC: KIRMIZI — KACTI: %s" % "; ".join(kacan))
            return 1
        if olculemeyen:
            print("SONUC: YESIL (SINIRLI) — olculebilen her sabotaj ISIRDI; %d OLCULEMEDI (Windows'a ozgu, yukarida)."
                  % len(olculemeyen))
        else:
            print("SONUC: YESIL — uc kol temiz, %d sabotaj AYRI eksende ISIRDI." % len(SABOTAJLAR))
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

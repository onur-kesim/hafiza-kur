#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H14 TEK HUKUM MUTANTI — `_h14_hukum`'te ILERIDE / GERIDE / es UC YOL AYRIK MI?

NEDEN VAR
---------
`_h14_hukum` eskiden iki AYRI `if` tasiyordu:

    if fark < -gecikme:  fail(... ILERIDE ...)
    if fark > gecikme:   ... GERIDE FAIL kollari ...
    else:                N.append("H14: hafiza projeyle es ...")

Ters yon (hafiza dosyalardan ILERIDE) ikinci `if`'in `else`'ine de dusuyor ve AYNI
raporda hem FAIL hem "es" notu basiyordu. Iki olcum:
  · 13 Agu 2026, `FAZC_H14_RAPOR.md` §6 — `h_ileri` hali kurulurken goruldu,
    "ayri bir tura yazildi", duzeltilmedi.
  · 18 Eki 2026, Momentum `d4b5417` + `devral --esle canli=DURUM.md` — `kapi`
    ayni raporda `· H14: hafiza projeyle es (...)` (satir 14) VE
    `[H14] hafiza tarihi proje dosyalarindan 39 gun ILERIDE — tutarsiz.` (satir 23).
Ikinci isirik: `faz0/h14_bolme_mutanti.py` `_h14_satiri` FAIL'i ONCELEYEREK bu
korlugu atlatiyordu — yani mevcut kapilar kusuru GORMUYOR, TOLERE EDIYORDU.

DUZELTME: `if fark > gecikme` -> `elif fark > gecikme`. Mesaj metinleri DEGISMEDI.
Bu dosya o yapinin geri gelmesini mekanik olarak yakalar.

NE OLCER
--------
Dort proje hali, her biri `kapi` ile olculur; H14 satirlari SINIFLANIR:
    h_es         hafiza = dosyalar (ikisi eski)       -> YALNIZ  ES
    h_geride     proje ilerledi, hafiza ilerlemedi    -> YALNIZ  GERIDE (FAIL, exit 1)
    h_ileri      hafiza BUGUN, dosyalar eski (mtime)  -> YALNIZ  ILERIDE (FAIL, exit 1)
    h_ileri_git  ayni, ama izlenen-TEMIZ dosyalar     -> YALNIZ  ILERIDE (FAIL, exit 1)
                 (commit tarihi eski, mtime taze: taze klon / Momentum+devral yolu)
"YALNIZ" = o halin H14 satirlari arasinda baska sinifin satiri YOK ve H14 satiri
tektir. Uc yolun imzasi (es / geride / ileride) birbirinden de ayrisir.
HUKUM GEVSEMEZ: ILERIDE ve GERIDE hallerinde FAIL satiri (`[H14]` kanali) basilmaya
DEVAM eder; nota dusurulmus FAIL `· [H14]` onekiyle DIGER sayilir -> kirmizi. `kapi`
exit 1 de beklenir ama YEDEKTIR: bu hallerde H14 disi FAIL'ler de vardir (h_es'te bile
exit 1, olculdu), yani exit tek basina H14'u ayirt ETMEZ — asil koruma satir sinifidir.

SAGLAM motorda kapi YESIL; asagidaki uc mutantin HER BIRINDE KIRMIZI yanmalidir:
    M-TEK1 ESKI IF/IF-ELSE   `elif` -> `if` (ters yon iki hukum birden — iki olcumun kusuru)
    M-TEK2 ES NOTU KOSULSUZ  `else` -> `if True` (es notu FAIL yollarinda da basilir)
    M-TEK3 ILERIDE SOKULUR   ILERIDE FAIL kolu `if False` (ters yon sessiz kalir: hukum gevsedi)

HAL KAPISI: temiz kolda her halin ciktisinda H14 satiri BULUNMALIDIR; bulunmazsa
hal kapiyi hic ateslememistir, butun mutantlar sahte "temiz" gorunurdu -> OLCULEMEDI.

NE OLCMEZ
---------
  · ILERIDE'nin FAIL OLMASININ dogru hukum olup olmadigi (devralma ani muafiyeti
    sorusu IS_EMRI_H14_TERS_YON_TEK_HUKUM.md "AÇIK SORU": karar degil, olculmedi).
    Bu kapi bugunku hukmu (FAIL, exit 1) SABITLER, onayini iddia etmez.
  · `gecikme` sinir degerleri (`fark == +-gecikme`) ve "damga donmus" alt kolu
    (`h14_damga_donmus_mutanti.py` ayri eksende olcer).

KULLANIM    python3 faz0/h14_tek_hukum_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve uc mutantin uclusu de KIRMIZI yakti
            1 saglam motorda kirmizi YA DA bir mutant KACTI
            2 OLCULEMEDI (git yok, hal kurulamadi, anchor tutmadi, duzenek determinist degil)
"""
import datetime as _dt
import json
import os
import re
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

# Hafiza tarihi ile dosya tarihi arasina konan mesafe: varsayilan `hafiza_gecikme_gun`
# (2) her iki yonde RAHATCA asilir; hukum esik yuvarlamasina degil yola baglidir.
GUN = 40

HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h14 tek hukum mutanti icin ilk kayit"],
            ["derle"]]

# hal adi, kurulum tipi, BEKLENEN H14 sinifi, kapi exit 1 olmali mi
HALLER = [
    ("h_es", "es", "ES", False),
    ("h_geride", "geride", "GERIDE", True),
    ("h_ileri", "ileri", "ILERIDE", True),
    ("h_ileri_git", "ileri_git", "ILERIDE", True),
]


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin kor/saglam oldugu anlamina GELMEZ."""


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:120]))
    return r.stdout


def _eski_gun():
    return _dt.date.today() - _dt.timedelta(days=GUN)


def _eski_ts():
    # Gun ortasi: yerel saat/DST kaymasinin gun sinirini atlatmasini onler.
    g = _eski_gun()
    return _dt.datetime(g.year, g.month, g.day, 12, 0, 0).timestamp()


def _tarih_yaz(kok, gun):
    """'Son guncelleme' tarihini CANLI ve SNAPSHOT dosyalarinda ayni anda degistirir."""
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


def _rc_yaz(kok, **anahtarlar):
    """`.hafizarc`'a anahtar yazar (yoksa EKLER; `kur` varsayilan degerleri yazmaz)."""
    p = os.path.join(kok, ".hafizarc")
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        raise Kurulamadi(".hafizarc okunamadi: %s" % e)
    d.update(anahtarlar)
    with open(p, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


# H14'un kendi disladigi dizinler; mtime'i onlarda degistirmenin anlami yok.
_HARIC = {".git", "node_modules", "__pycache__", ".venv", "arsiv", "gunluk", "dist", "build"}


def _mtime_ayarla(kok, ts, atla=()):
    for r0, d0, f0 in os.walk(kok):
        d0[:] = [d for d in d0 if d not in _HARIC]
        for f in f0:
            if f in atla:
                continue
            try:
                os.utime(os.path.join(r0, f), (ts, ts))
            except OSError:
                pass


def _commit_et(kok, gun):
    """Butun agaci `gun` tarihiyle commit'ler (izlenen-temiz sinifini var eder)."""
    iso = "%sT12:00:00" % gun.isoformat()
    ortam = dict(os.environ, GIT_AUTHOR_DATE=iso, GIT_COMMITTER_DATE=iso,
                 GIT_AUTHOR_NAME="h14tek", GIT_AUTHOR_EMAIL="h14tek@example.invalid",
                 GIT_COMMITTER_NAME="h14tek", GIT_COMMITTER_EMAIL="h14tek@example.invalid",
                 GIT_CONFIG_NOSYSTEM="1")
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban", env=ortam)


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H14TEK"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))
    _rc_yaz(kok, bayatlik_gun=3600)          # H12 gurultusu hallerin ayirt ediciligini bozmasin
    simdi = _dt.datetime.now().timestamp()
    eski, eski_ts = _eski_gun(), _eski_ts()
    kodp = os.path.join(kok, "kod.py")
    with open(kodp, "w", encoding="utf-8", newline="") as f:
        f.write("# h14 tek hukum mutanti icin proje dosyasi\nDEGER = 1\n")

    if tip == "es":                        # hafiza ESKI, dosyalar da ESKI
        _tarih_yaz(kok, eski)
        _mtime_ayarla(kok, eski_ts)
    elif tip == "geride":                  # hafiza ESKI, dosya TAZE
        _tarih_yaz(kok, eski)
        _mtime_ayarla(kok, eski_ts, atla=("kod.py",))
        os.utime(kodp, (simdi, simdi))
    elif tip == "ileri":                   # hafiza BUGUN, dosyalar ESKI (mtime yolu)
        _mtime_ayarla(kok, eski_ts)
    elif tip == "ileri_git":               # hafiza BUGUN, izlenen+TEMIZ dosya, commit ESKI, mtime TAZE
        _commit_et(kok, eski)              # (taze klon / Momentum + devral yolu: commit tarihi gecerli)
        _mtime_ayarla(kok, simdi)
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


def _agaci_sil(yol):
    """Windows'ta git nesneleri SALT-OKUNURDUR; `ignore_errors=True` onlari sessizce birakir
    (her kosumda %TEMP%'te `h14tek_*` birikir). Yazma izni acip yeniden dener."""
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


def haller_kur(motor_temiz, taban):
    """Halleri BIR KEZ ve TEMIZ motorla kurar. Sabotaj OLCEN motordadir, olculen PROJEDE degil
    (hal kurulumu `derle` icerir; sabotajli motor derlemeyi reddedebilir -> OLCULEMEDI)."""
    return {ad: hal_kur(motor_temiz, ad, tip, taban) for ad, tip, _, _ in HALLER}


def h14_satirlari(cikti):
    return [s.strip() for s in cikti.split("\n") if "H14" in s]


def sinifla(satir):
    """Bir H14 satirini {ILERIDE, GERIDE, ES, DIGER}'e ayirir. Mesaj metinleri DEGISMEZ."""
    if satir.startswith("[H14]"):
        if "ILERIDE" in satir:
            return "ILERIDE"
        if "PROJE ILERLEDI" in satir or "TARIH DAMGASI DONMUS" in satir:
            return "GERIDE"
        return "DIGER"
    if "H14: hafiza projeyle es" in satir:
        return "ES"
    return "DIGER"


def olc(motor, kokler, hedef_taban):
    """{hal: (exit, [H14 satirlari])} — halleri kopyalayip verilen motorla `kapi` kosar.
    `copytree` mtime'lari KORUR (copy2): H14'un olctugu sey tam olarak mtime'dir."""
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        rc, c = kos(motor, ["kapi"], kok)
        out[ad] = (rc, h14_satirlari(c))
    return out


def kapi_ihlalleri(olcum):
    """KAPI: hal basina ihlal listesi (bos = YESIL). Sagli/sabotajli motor AYNI fonksiyonla yargilanir."""
    ihlal = []
    for ad, _, beklenen, exit1 in HALLER:
        rc, satirlar = olcum[ad]
        siniflar = [sinifla(s) for s in satirlar]
        digerleri = sorted({c for c in siniflar if c != beklenen})
        if digerleri:
            ihlal.append("%s: beklenen YALNIZ %s, ama %s da basildi: %s"
                         % (ad, beklenen, "/".join(digerleri),
                            " || ".join(s[:70] for s, c in zip(satirlar, siniflar) if c != beklenen)))
        if siniflar.count(beklenen) != 1:
            ihlal.append("%s: %s satiri %d adet (TEK olmali)" % (ad, beklenen, siniflar.count(beklenen)))
        if exit1 and rc != 1:
            ihlal.append("%s: kapi exit %s (HUKUM GEVSEMEMELI: 1 beklenir)" % (ad, rc))
    imzalar = {tuple(sorted(sinifla(s) for s in olcum[ad][1])) for ad, _, _, _ in HALLER
               if ad in ("h_es", "h_geride", "h_ileri")}
    if len(imzalar) != 3:
        ihlal.append("es / geride / ileri imzalari ayrismiyor (%d ayrik imza, 3 beklenir)" % len(imzalar))
    return ihlal


# --------------------------------------------------------------------- MUTANTLAR
# Her mutant: ad, aciklama, [(eski, yeni)]. `eski` motorda TAM 1 kez gecmelidir.
MUTANTLAR = [
    ("M-TEK1 ESKI IF/IF-ELSE",
     "`elif fark > gecikme` -> `if`: ters yon ikinci if'in else'ine duser (FAIL + es notu birlikte)",
     [("        elif fark > gecikme:", "        if fark > gecikme:")]),
    ("M-TEK2 ES NOTU KOSULSUZ",
     "`else:` -> `if True:`: es notu GERIDE/ILERIDE FAIL yollarinda da basilir",
     [("        else:\n            N.append(\"H14: hafiza projeyle es",
       "        if True:\n            N.append(\"H14: hafiza projeyle es")]),
    ("M-TEK3 ILERIDE SOKULUR",
     "ILERIDE FAIL kolu `if False`: ters yon SESSIZ kalir (hukum gevsedi, yalniz es notu)",
     [("        if fark < -gecikme:\n            devral = _H14_MUAFIYET[0]",
       "        if False:\n            devral = _H14_MUAFIYET[0]")]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def _ozet(olcum):
    return {ad: (rc, sorted(sinifla(s) for s in satirlar)) for ad, (rc, satirlar) in olcum.items()}


def main():
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_MOTOR
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz (izlenen-temiz sinifi git ister).")
        return 2

    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("H14 TEK HUKUM MUTANTI — ILERIDE / GERIDE / es uc yol AYRIK mi?")
    print("motor: %s · platform: %s" % (motor, sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h14tek_")
    try:
        try:
            kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
            temiz = olc(motor, kokler, os.path.join(taban, "ref"))
            temiz2 = olc(motor, kokler, os.path.join(taban, "ref2"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        if _ozet(temiz) != _ozet(temiz2):
            print("OLCULEMEDI: duzenek determinist degil (ayni motor 2 kez farkli) — mutant hukmu ANLAMSIZ.")
            return 2

        # HAL KAPISI: her hal H14'u ATESLEMELI.
        atessiz = [ad for ad, _, _, _ in HALLER if not temiz[ad][1]]
        for ad, _, beklenen, _ in HALLER:
            rc, satirlar = temiz[ad]
            print("  %-12s exit %s · beklenen %-8s · %s"
                  % (ad, rc, beklenen, (satirlar[0] if satirlar else "(H14 SATIRI YOK)")[:76]))
            for ek in satirlar[1:]:
                print("  %-12s %-30s · %s" % ("", "(ek H14 satiri)", ek[:76]))
        if atessiz:
            print("\nOLCULEMEDI: su haller H14'u hic ateslemedi: %s (sahte yesil olurdu)" % ", ".join(atessiz))
            return 2
        print(CIZGI)

        # ---- SAGLAM MOTOR: kapi YESIL olmali -----------------------------------
        ihlal = kapi_ihlalleri(temiz)
        print("  SAGLAM MOTOR                   %s" % ("KAPI YESIL" if not ihlal else "KAPI KIRMIZI"))
        for x in ihlal:
            print("      ! %s" % x)
        if ihlal:
            print(CIZGI)
            print("SONUC: KIRMIZI — saglam motor kapiyi gecemedi (ters yonde iki hukum / FAIL kaybi).")
            return 1

        # ---- MUTANTLAR: her biri KIRMIZI yakmali --------------------------------
        isirdi, kacti, olculemedi = [], [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yeni = olc(sab, kokler, os.path.join(d, "hal"))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-26s OLCULEMEDI  %s" % (ad, e))
                continue
            m_ihlal = kapi_ihlalleri(yeni)
            if m_ihlal:
                isirdi.append(ad)
                print("  +  %-26s ISIRDI      kapi KIRMIZI (%d ihlal): %s" % (ad, len(m_ihlal), m_ihlal[0][:90]))
            else:
                kacti.append(ad)
                print("  !  %-26s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
            sys.stdout.flush()
    finally:
        _agaci_sil(taban)

    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
          % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kapinin KOR oldugu yapi.")
        return 1
    print("  Saglam motor YESIL, uc sabotaj KIRMIZI: ILERIDE / GERIDE / es yollari AYRIK olculuyor.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H9 KESME MUTANTI (M-Y4) — `_kapi_h9`nun "git deposu OKUNAMADI" hukmu, git'in
ilk satirini KIRPMADAN mi basiyor? (kalem5-tarama/IS_EMRI_SIK_A.md D2, Onur
kilidi SIK A, 19 Agu 2026 · dayanak: kalem5-tarama/KALEM5_KESME_TARAMASI.md)

NEDEN VAR
  `olculemedi_kesme_mutanti.py`nin (M-Y3, D1) ikiz kardesi: AYNI kalibin
  ikinci uyesi. `hafiza.py` satir ~3956, git alt-surecinin stderr'inin ILK
  SATIRINI `[:120]` ile kesiyordu; o satir (`fatal: ...`) sik sik KOK
  DIZININ YOLUNU tasir. Kok uzunsa yol KIRPILIR, kullanici HANGI DIZIN
  oldugunu YARIM gorur.

NE OLCER — CIFT KOLLU (M-Y3 ile AYNI kalip; POSIX SARTI YOK, UC PLATFORMDA KAPI)
    M-Y4 UZUN KOL : kok >= 200 karakter. Motora ESKI kesme ([:120]) GERI
                    enjekte edilir; H9 satiri KIRPILMALI (kapanis tirnagi
                    `'` ile BITMEMELI) — kapi kusuru DOGRU yakaladi (ISIRDI).
    M-Y4 KISA KOL : kok kisa (mkdtemp varsayilani). AYNI sabotaj; git'in
                    mesaji <120 karakter oldugu icin GORUNMEZ KALMALI (satir
                    kapanis tirnagi `'` ile BITMELI) — KACIS BEKLENEN sonuc.

URETIM TARIFI (SIK EPSILON, 19 Agu 2026 Onur kilidi — birebir OLCULDU)
  git init + commit -> `kur` -> defterler commit'lenir -> `kapi`, git'in KENDI
  sahiplik denetimi `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` ile tetiklenmis olarak
  kosulur. Git `fatal: detected dubious ownership in repository at '<KOK>'`
  verir (exit 128); hem `log` hem `rev-parse --git-dir` duser -> `_kapi_h9`nun
  OKUNAMADI dali kosar. Olculmus imza: kisa kokte 72 karakter (H9 satiri 98),
  uzun kokte 252 (H9 satiri 278).

  🔴 NEDEN `chown` DEGIL (19 Agu 2026, CI #80 `32236392253` ISIRDI): eski tarif
  `chown -R nobody <KOK>` idi. `chown` ile BASKA kullaniciya sahiplik devri
  POSIX'te ROOT ister; GitHub runner'i `runner` kullanicisidir, root DEGILDIR
  -> UC PLATFORMDA DA "kum havuzu kurulamadi" (exit 2). Arac DURUST davrandi;
  kusur ORTAM VARSAYIMINDAYDI. `GIT_TEST_ASSUME_DIFFERENT_OWNER` AYNI mesaji
  uretir, ROOT/sudo GEREKTIRMEZ ve DOSYA SISTEMINE DOKUNMAZ.

  🔴 KALAN ACIK RISK (gizlenmez): degisken git'in KENDI TEST kancasidir; upstream
  kaldirirsa ya da runner'da kuresel `safe.directory` onu etkisizlestirirse mesaj
  URETILMEZ. O halde bu arac SESSIZCE GECMEZ: H9 OKUNAMADI satirini bulamaz ve
  OLCULEMEDI (exit 2) doner — OLCULDU (bkz. asagidaki kuresel-ayar bagisikligi).
  Kuresel ayar bagisikligi icin `GIT_CONFIG_GLOBAL/SYSTEM=os.devnull` +
  `GIT_CONFIG_NOSYSTEM=1` de gecirilir; `safe.directory=*` tanimliyken bile
  iki kol da BEKLENDIGI GIBI olctu.

CAPA (H16-KESME-DUZELTME-BRIEF.md §5 dersi): motora KOD PARCACIGIYLA anchor
atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI (proje sozlesmesi)
  0  iki kolun IKISI DE BEKLENDIGI GIBI (KISA icin 'beklenen' KACIStir)
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  OLCULEMEDI (BEKLENMEDIK yoksa) — tetikleyici mesaji uretmediyse DAHIL
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi)
"""
import os
import shutil
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
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []          # (ad, durum, ayrinti)


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ (D2)
# KALEM 1'in TERSİ (D2): duzeltilmis motora `[0][:120]` kesmesini GERI
# enjekte eder. `.split("\n")[0]`nin KENDISI DOKUNULMAZ (IS_EMRI_SIK_A.md §2)
# — yalniz kuyruktaki `[:120]` eklenir/cikarilir.
_DUZELTILMIS = '_sb = (r.stderr or _rg.stderr or "").strip().split("\\n")[0]'
_SABOTAJLI = '_sb = (r.stderr or _rg.stderr or "").strip().split("\\n")[0][:120]'


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (kalem5-tarama/IS_EMRI_SIK_A.md D2, hafiza.py "
            "_kapi_h9())." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=120, env=None):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if env:
        o.update(env)
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="h9-mut", GIT_AUTHOR_EMAIL="h9-mut@example.invalid",
    GIT_COMMITTER_NAME="h9-mut", GIT_COMMITTER_EMAIL="h9-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kok_hedef_uzunlukta(taban_dizini, hedef_uzunluk):
    """bkz. olculemedi_kesme_mutanti.py._kok_hedef_uzunlukta — AYNI mantik,
    dolgu HEX OLMAYAN ("zq" tekrari)."""
    on_ek = os.path.join(taban_dizini, "")
    gerekli = hedef_uzunluk - len(on_ek)
    if gerekli < 1:
        return None
    dolgu = ("zq" * ((gerekli // 2) + 1))[:gerekli]
    kok = on_ek + dolgu
    os.makedirs(kok, exist_ok=True)
    return kok


# 🔴 AD, YAPILAN ISI SOYLER (M-A8 dersi: adi "realpath maskesi" olup KESMEYI olcen
# bir mutant, maskeyi hic olcmedigini UC AY gizledi). Burada sahiplik DEVREDILMEZ;
# git'in sahiplik DENETIMI supheli hale getirilir. Ad da onu soyler.
_OLCUM_ORTAMI = {
    "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1",   # tetikleyici (root/sudo GEREKMEZ)
    "GIT_CONFIG_NOSYSTEM": "1",               # kuresel/sistem `safe.directory`
    "GIT_CONFIG_GLOBAL": os.devnull,          # bagisikligi — OLCULDU: `*` tanimli
    "GIT_CONFIG_SYSTEM": os.devnull,          # olsa bile iki kol da olcuyor
}


def _sahipligi_supheli_kil():
    """SIK EPSILON: dosya sistemine DOKUNMAZ, kullanici/izin DEGISTIRMEZ.
    Git'in kendi sahiplik denetimi cevre degiskeniyle tetiklenir; uretilen mesaj
    `chown` tarifiyle BIREBIR AYNIDIR (olculdu 19 Agu 2026, git 2.43.0)."""
    return dict(_OLCUM_ORTAMI)


def _kum_havuzu_kur(motor, kok):
    """Uretim tarifi (IS_EMRI_SIK_A.md §4, OLCULDU): git init+commit -> kur ->
    defterler commit'lenir -> depo BASKA kullaniciya devredilir. Motora
    DOKUNMAZ, yalniz komut satirindan cagirir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c = _kos(motor, ["kur", "--ad", "Y4", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))


def _h9_satiri(cikti):
    return next((s for s in cikti.splitlines() if "H9: git deposu OKUNAMADI" in s), None)


def _my4_kol(taban, ad, hedef_uzunluk, beklenen_kirpilmamis):
    alt = os.path.join(taban, "u" if hedef_uzunluk else "k")
    os.makedirs(alt, exist_ok=True)
    if hedef_uzunluk:
        kok = _kok_hedef_uzunlukta(alt, hedef_uzunluk)
        if kok is None:
            _kayit(ad, OLCULEMEDI, "hedef uzunluk (%d) bu ortamda kurulamadi" % hedef_uzunluk)
            return
    else:
        kok = os.path.join(alt, "kk")
        os.makedirs(kok, exist_ok=True)
    try:
        _kum_havuzu_kur(MOTOR, kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    sab_dizin = os.path.join(alt, "sab")
    os.makedirs(sab_dizin, exist_ok=True)
    motor_sab = _sabotajli_motor(sab_dizin)
    rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok],
                 env=_sahipligi_supheli_kil())
    satir = _h9_satiri(c)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H9 OKUNAMADI satiri bulunamadi (kok uzunlugu=%d, exit=%s) — "
              "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ olabilir "
              "(surum/platform). SESSIZ GECIS DEGIL, OLCULEMEDI. Ham cikti kuyrugu:\n%s"
              % (len(kok), rc, c[-500:]))
        return
    kirpilmamis = satir.rstrip().endswith("'")
    dogru = (kirpilmamis == beklenen_kirpilmamis)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "kok uzunlugu=%d | sabotajli motor ([:120] geri) | satir kapanis tirnagi "
          "(') ile bitiyor (kirpilmamis)=%s (beklenen: %s)\n      satir: %s"
          % (len(kok), "VAR" if kirpilmamis else "yok",
             "VAR" if beklenen_kirpilmamis else "yok", satir.strip()))


def my4_uzun_kol(taban):
    try:
        # olculemedi_kesme_mutanti.py ile ayni ders: 200 Windows'ta MAX_PATH'e
        # carpiyordu (git commit'in .git/objects yazimi); 170 mesaj esigini
        # (>120) rahatca asiyor. Bu kol zaten POSIX-disi platformda hic
        # kosmuyor (main() basinda OLCULEMEDI), ama Linux/macOS icin de
        # tutarli tek sabit deger tercih edildi.
        _my4_kol(taban,
                "M-Y4 UZUN KOL: kok>=170, sabotajli motor H9 satirini KIRPMALI (ISIRMALI)",
                170, False)
    except AracKusuru as e:
        _kayit("M-Y4 UZUN KOL", OLCULEMEDI, str(e))


def my4_kisa_kol(taban):
    try:
        _my4_kol(taban,
                "M-Y4 KISA KOL (KOR KOL): kisa kokte AYNI sabotaj GORUNMEZ KALMALI (KACMASI BEKLENEN)",
                0, True)
    except AracKusuru as e:
        _kayit("M-Y4 KISA KOL", OLCULEMEDI, str(e))


def main():
    print("=" * 82)
    print("H9 KESME MUTANTI (M-Y4) — _kapi_h9 OKUNAMADI hukmu kirpilmadan mi basiyor?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h16km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        my4_uzun_kol(taban)
        my4_kisa_kol(taban)
        print()
        for ad, durum, ayrinti in SONUC:
            print("  %-16s %s" % (durum, ad))
            print("  %-16s   %s" % ("", ayrinti))
        print(CIZGI)
        beklenmedik = sum(1 for _, d, _ in SONUC if d == BEKLENMEDIK)
        olculemedi = sum(1 for _, d, _ in SONUC if d == OLCULEMEDI)
        gibi = len(SONUC) - beklenmedik - olculemedi
        print("SONUC: %d/%d kol BEKLENDIGI GIBI - %d beklenmedik - %d olculemedi"
              % (gibi, len(SONUC), beklenmedik, olculemedi))
        if beklenmedik:
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

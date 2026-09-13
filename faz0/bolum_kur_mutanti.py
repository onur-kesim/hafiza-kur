#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — BOLUM KUR MUTANTI (besli-paket/IS_EMRI_BOLUM_KUR.md, KALEM 1).

NEDEN VAR (olculdu, kod yazilmadan ONCE — gercek Momentum kopyasinda)
  `devral`, diskte ZATEN `## ` basligi olan bir projede `zorunlu_bolumler`i
  MEVCUT basliklardan turetir (6 Eyl kilidi "diskteki gercek ustundur") ve
  EKSIK basligi FORCE EKLEMEZ. Bir proje `## GUNCEL DURUM` hic tasimadan
  devralinirsa (OLCULDU: gercek Momentum kopyasi, `devral --esle canli=
  DURUM.md` sonrasi `.hafizarc`'ta `zorunlu_bolumler` 3 oge tasiyordu, hicbiri
  GUNCEL DURUM degildi) `not`/`derle` dongusu HIC BASLAYAMAZ: `derle` hedef
  bulamayip fragmani sessizce ATLAR ("0 fragman islendi"), `kapi` [H17] ve
  [H6] ile KOSULSUZ kirmizi kalir. `devral` KENDISI degismez (dokunulmazlar
  listesi); cozum AYRI, ACIK bir komuttur: `hafiza.py bolum-kur`.

  REDDEDILEN ALTERNATIF (kod yazilmadan once OLCULUP dogrulandi): adaylari
  `rc["zorunlu_bolumler"]`den turetmek. O liste `devral` aninda MEVCUT
  basliklardan turetildigi icin, tam da duzeltilmesi gereken Momentum sinifi
  projede `## GUNCEL DURUM` HIC icermiyordu — o listeden turetilen bir komut
  BU PROJEDE HICBIR SEY EKLEMEZ (M-3 bunu sinar).

NE OLCER — UC KAPI (hepsi GERCEK subprocess ile, senaryo "Momentum SINIFI":
existing `## ` basliklari olan, `## GUNCEL DURUM`u OLMAYAN bir canli defter,
`devral --esle` ile devralinir)
  KAPI-1  bolum-kur -> not -> derle  => derle fragmani ISLER (0 DEGIL),
          kapi ciktisinda [H17] ve [H6] YOK
  KAPI-2  bolumler ZATEN varken bolum-kur (ikinci kosum) => '0 bolum eklendi',
          canli dosyada HICBIR BAYT degismez
  KAPI-3  POZITIF KONTROL: taze `kur` projesinde bolum-kur => hicbir sey
          eklemez (kur ZATEN yazmisti), canli dosya degismez, tam tur YESIL

NE OLCMEZ
  1. `devral`in kendi davranisi (DOKUNULMAZ, ayri kapinin konusu degil).
  2. K4 — H6'nin ICERIK korlugu (bu kapi yalniz BOLUM YOKLUGU kolunu olcer).

CIKIS KODLARI
  0  uc kapi de temiz VE M-1/M-2/M-3 ucu de ISIRDI
  1  bir kapi KIRMIZI ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor okunamadi, kurulum basarisiz, git yok) — kirmizi/kacan YOK
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
            pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")


class Kurulamadi(Exception):
    """Test KURULUMU basarisiz (git yok, devral/kur/not basarisiz) — KAPI HUKMU DEGILDIR."""


def kos(motor, *argv, kok=None):
    """`_komut`/`_kapi_kos` ile AYNI cagri kalibi (hafiza.py): -X utf8 +
    PYTHONIOENCODING=utf-8 — Windows'ta cp1254 cocugu bozmasin."""
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ======================================================== MOMENTUM SINIFI

_MOMENTUM_SINIFI_CANLI = (
    "# Test Projesi\n\n"
    "## Kalici dersler (dilimden bagimsiz)\n"
    "- ornek ders\n\n"
    "## Bilinen sinirlar\n"
    "- ornek sinir\n"
)


def _momentum_sinifi_kur(taban, ad, motor):
    """`devral`in `zorunlu_bolumler`i MEVCUT basliklardan turettigi, `##
    GUNCEL DURUM`u İCERMEYEN sinifi taklit eder: canlida BASKA basliklar olan
    bir proje, `devral --esle` ile devralinir. GERCEK Momentum kopyasinin
    OLCULEN yapisiyla AYNI sinif (iki `## ` basligi, GUNCEL DURUM YOK)."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with io.open(os.path.join(kok, "DURUM.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(_MOMENTUM_SINIFI_CANLI)
    k, c = kos(motor, "devral", "--esle", "canli=DURUM.md", kok=kok)
    if k != 0:
        raise Kurulamadi("devral basarisiz (exit %d): %s" % (k, c[:300]))
    return kok


# ============================================================== KAPI-1/2/3

_H_ETIKET = re.compile(r"^\s*\[(H\d+)\]", re.M)


def kapi_1(motor, taban):
    """bolum-kur -> not -> derle: derle fragmani ISLEMELI, [H17]/[H6] SUSMALI."""
    kok = _momentum_sinifi_kur(taban, "kapi1", motor)
    k, c = kos(motor, "bolum-kur", kok=kok)
    if k != 0:
        raise Kurulamadi("bolum-kur basarisiz (exit %d): %s" % (k, c[:300]))
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=kapi-1 dogrulama notu", kok=kok)
    if k != 0:
        raise Kurulamadi("not basarisiz (exit %d): %s" % (k, c[:300]))
    k, c = kos(motor, "derle", kok=kok)
    bulgular = []
    if "DERLENDI: 0 fragman" in c:
        bulgular.append("derle fragmani ISLEMEDI ('0 fragman islendi' -- bolum-kur hedefi "
                         "ACMAMIS olabilir): %s" % c[:300])
    elif "DERLENDI:" not in c:
        bulgular.append("derle beklenmeyen cikti (exit %d): %s" % (k, c[:300]))
    k, c = kos(motor, "kapi", kok=kok)
    etiketler = set(_H_ETIKET.findall(c))
    if "H17" in etiketler:
        bulgular.append("[H17] HALA cikiyor (bolum-kur sonrasi): %s" % c[:400])
    if "H6" in etiketler:
        bulgular.append("[H6] HALA cikiyor (bolum-kur sonrasi): %s" % c[:400])
    return bulgular


def kapi_2(motor, taban):
    """Bolumler ZATEN varken (ikinci kosum) bolum-kur: '0 bolum eklendi',
    canli dosyada HICBIR BAYT degismez."""
    kok = _momentum_sinifi_kur(taban, "kapi2", motor)
    k, c = kos(motor, "bolum-kur", kok=kok)
    if k != 0:
        raise Kurulamadi("ilk bolum-kur basarisiz (exit %d): %s" % (k, c[:300]))
    canli = os.path.join(kok, "DURUM.md")
    onceki = io.open(canli, "rb").read()
    k, c = kos(motor, "bolum-kur", kok=kok)   # IKINCI kosum -- hepsi ZATEN var
    bulgular = []
    if k != 0:
        bulgular.append("ikinci bolum-kur basarisiz (exit %d): %s" % (k, c[:300]))
    if "0 bolum eklendi" not in c:
        bulgular.append("ikinci kosumda '0 bolum eklendi' BASILMADI: %s" % c[:300])
    sonraki = io.open(canli, "rb").read()
    if sonraki != onceki:
        bulgular.append("ikinci kosumda canli dosya DEGISTI (bayt-ayni OLMALIYDI) — "
                         "%d -> %d bayt" % (len(onceki), len(sonraki)))
    return bulgular


def kapi_3(motor, taban):
    """POZITIF KONTROL: taze `kur` projesi zaten 7 zorunlu bolumu tasir;
    bolum-kur hicbir sey EKLEMEMELI, tam tur YESIL KALMALI (duzeltme `kur`
    yolunu BOZMAMALI)."""
    kok = os.path.join(taban, "kapi3")
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    k, c = kos(motor, "kur", "--ad=kapi3", kok=kok)
    if k != 0:
        raise Kurulamadi("kur basarisiz (exit %d): %s" % (k, c[:300]))
    canli = os.path.join(kok, "PROJE_HAFIZA.md")
    onceki = io.open(canli, "rb").read()
    k, c = kos(motor, "bolum-kur", kok=kok)
    bulgular = []
    if k != 0:
        bulgular.append("bolum-kur basarisiz (exit %d): %s" % (k, c[:300]))
    if "0 bolum eklendi" not in c:
        bulgular.append("kur SONRASI bolum-kur BIR SEY EKLEDI (beklenen: 0 -- `kur` yolu "
                         "BOZULDU): %s" % c[:300])
    sonraki = io.open(canli, "rb").read()
    if sonraki != onceki:
        bulgular.append("kur SONRASI bolum-kur canli dosyayi DEGISTIRDI (bayt-ayni OLMALIYDI)")
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=kapi-3 dogrulama notu", kok=kok)
    if k != 0:
        bulgular.append("not basarisiz (exit %d): %s" % (k, c[:200]))
    k, c = kos(motor, "derle", kok=kok)
    if k != 0:
        bulgular.append("derle basarisiz (exit %d): %s" % (k, c[:300]))
    k, c = kos(motor, "kapi", kok=kok)
    if k != 0:
        bulgular.append("kapi KIRMIZI (kur yolunda REGRESYON): %s" % c[:400])
    return bulgular


# ================================================================ MUTANTLAR

def _degistir(s, eski, yeni, etiket):
    n = s.count(eski)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [%s]: %r\n"
                         % (n, etiket, eski[:70]))
        return None
    return s.replace(eski, yeni, 1)


_M1_ESKI = (
    "    L = L[:i0] + ek + L[i0:]\n"
    "    yaz(y.canli, \"\\n\".join(L))\n"
)
_M1_YENI = (
    "    L = L[:i0] + ek + L[i0:]\n"
    "    pass  # MUTANT: bolum ekleme dali SOKULDU (yaz() hic cagrilmiyor)\n"
)


def m1_ekleme_dali_sokulur(s):
    """Bolum ekleme dali (asil `yaz()` cagrisi) SOKULUR -> komut 'EKLENDI'
    der ama hicbir sey yazmaz -> KAPI-1 ISIRMALI (derle hala fragmani atlar)."""
    return _degistir(s, _M1_ESKI, _M1_YENI, "M-1")


_M2_ESKI = '    eksik = [b for b in _BOLUM_KUR_ADAYLARI if _bolum_araligi(L, b)[0] is None]\n'
_M2_YENI = '    eksik = list(_BOLUM_KUR_ADAYLARI)  # MUTANT: "yalniz eksik" kosulu KALDIRILDI\n'


def m2_yalniz_eksik_kosulu_kaldirilir(s):
    """'Yalniz EKSIK olani ekle' kosulu kaldirilir -> var olan bolumler de
    HER KOSUMDA yeniden eklenir -> KAPI-2 ISIRMALI (ikinci kosum bayt
    degistirir, '0 bolum eklendi' hic basilmaz)."""
    return _degistir(s, _M2_ESKI, _M2_YENI, "M-2")


_M3_ESKI = '    eksik = [b for b in _BOLUM_KUR_ADAYLARI if _bolum_araligi(L, b)[0] is None]\n'
_M3_YENI = ('    eksik = [b for b in rc["zorunlu_bolumler"] if _bolum_araligi(L, b)[0] is None]'
            '  # MUTANT: REDDEDILEN turetim\n')


def m3_reddedilen_turetim(s):
    """Aday listesi `rc["zorunlu_bolumler"]`den turetilir (is emrinin
    REDDETTIGI alternatif) -> Momentum sinifi fiksturde o liste GUNCEL
    DURUM'u hic icermedigi icin HICBIR SEY eklenmez -> KAPI-1 ISIRMALI."""
    return _degistir(s, _M3_ESKI, _M3_YENI, "M-3")


MUTANTLAR = [
    ("M-1  bolum ekleme dali sokulur", m1_ekleme_dali_sokulur, "KAPI-1"),
    ("M-2  'yalniz eksik' kosulu kaldirilir", m2_yalniz_eksik_kosulu_kaldirilir, "KAPI-2"),
    ("M-3  REDDEDILEN turetim (rc['zorunlu_bolumler'])", m3_reddedilen_turetim, "KAPI-1"),
]


# ===================================================================== main

def _git_var():
    return shutil.which("git") is not None


def _kapi_calistir(fn, motor):
    taban = tempfile.mkdtemp(prefix="bolumkur_kapi_")
    try:
        return fn(motor, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN_MOTOR)
    print("=== BOLUM KUR MUTANTI === motor: %s · platform: %s" % (motor, sys.platform))

    if not _git_var():
        print("SONUC: OLCULEMEDI — git yok; senaryolar git'li agac ister.")
        return 2
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    olculemeyen = 0
    kirmizi = 0

    for ad, fn in (("KAPI-1", kapi_1), ("KAPI-2", kapi_2), ("KAPI-3", kapi_3)):
        try:
            b = _kapi_calistir(fn, motor)
            print("  %-8s: %s" % (ad, "KIRMIZI" if b else "YESIL"))
            for x in b:
                print("      - %s" % x)
            if b:
                kirmizi += 1
        except Kurulamadi as e:
            print("  %-8s: OLCULEMEDI — %s" % (ad, e))
            olculemeyen += 1

    print("\n--- MUTANT SINAMASI (hafiza.py kaynagina textual sabotaj) ---")
    kacan = 0
    _KAPILAR = {"KAPI-1": kapi_1, "KAPI-2": kapi_2, "KAPI-3": kapi_3}
    for ad, fn, kapi_etiket in MUTANTLAR:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  %-46s -> OLCULEMEDI (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        d = tempfile.mkdtemp(prefix="bolumkur_mut_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            try:
                b_mut = _kapi_calistir(_KAPILAR[kapi_etiket], sahte)
            except Kurulamadi as e:
                print("  %-46s -> OLCULEMEDI (kurulum: %s)" % (ad, e))
                olculemeyen += 1
                continue
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if b_mut:
            print("  %-46s -> ISIRDI (%s)" % (ad, kapi_etiket))
        else:
            print("  %-46s -> KACTI (%s KOR)" % (ad, kapi_etiket))
            kacan += 1

    print()
    if kacan:
        print("SONUC: KIRMIZI — %d mutant KACTI (kapi kor)." % kacan)
        return 1
    if kirmizi:
        print("SONUC: KIRMIZI — %d kapi kendisi kirmizi (mutant sinamasindan ONCE)." % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem kosulamadi/kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    print("SONUC: YESIL — uc kapi de temiz, her mutant ISIRDI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

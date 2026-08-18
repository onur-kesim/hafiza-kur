#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YOL UZUNLUGU MUTANTI — `altin_cikti.py --uzun-yol` kolu KESILDI[:160]
REGRESYONUNU yakaliyor mu? (H16-KESME-DUZELTME-BRIEF.md KALEM 3)

NEDEN BU DOSYA VAR
  H16-KOK-SEBEP-RAPORU.md: CI #76'nin UC kirmizisinin TEK kok sebebi
  `hafiza.py:3326`'daki sabit `kesildi[:160]` kesmesiydi — symlink'le,
  `realpath`le, `normalize()` ile ILGISI YOKTU; belirleyici degisken kok
  dizininin KARAKTER UZUNLUGUYDU. Kusur AYLARDIR oradaydi ve BUTUN faz0
  bataryasi onu goremedi, cunku hepsi KISA `/tmp` altinda kosuyordu. CI'in
  onu yakalamasi KAZA eseriydi (symlink kolu yolu tesadufen esigin ustune
  cikardi) — kaza, kapi degildir.

  "Her duzeltmeye AYRI mutant" gereginin bu duzeltmedeki karsiligi budur.
  `altin_cikti.py`'nin YENI `--uzun-yol` kolunun KENDISI bu dosyanin konusu
  DEGIL — bu dosya o kolun ISIRDIGINI kanitlar: motora KESME GERI enjekte
  edilirse uzun-yol kolu bunu YAKALIYOR mu, ayni sabotaj KISA yolda GERCEKTEN
  KOR mu (bu korluk CI #76'yi aylarca gorunmez kildi — simdi olculuyor), esik
  (98/99) duzeltme sonrasi GERCEKTEN kapandi mi, duzeltme kisa yoldaki altin
  kumeyi BOZMUYOR mu.

DORT KOL — her biri AYRI bir korumayi olcer
  M-Y1 KESME GERI : DUZELTILMIS motora `kesildi[:160]` GERI enjekte edilir;
                     `--uzun-yol` kolu bunu YAKALAMALI (FARK VAR = kapi dogru
                     calisiyor, ISIRDI).
  M-Y2 KOR KOL     : AYNI sabotajli motor, KISA `/tmp` ile (--uzun-yol YOK)
                     kosulur; FARK YOK CIKMALI. Bu KACIS BEKLENEN ve ISTENEN
                     sonuctur — kisa yol bu sinifa YAPISAL OLARAK KORDUR;
                     🔴 EN ONEMLI KOL: bir kolun ISIRMASI kadar, ayni kolun
                     YANLIS ORTAMDA KACMASI da olculmelidir — yoksa bir
                     sonraki turda biri uzun-yol kolunu kisa `/tmp`'e cevirir
                     ve kapi sessizce kor olur (DURUM.md: "OLCUMU KOSTUM, ONU
                     KORUYAN KAPIYI KOSMADIM").
  M-Y3 ESIK        : DUZELTILMIS (sabotajsiz) motorla kok TAM 98 VE TAM 99
                     karakter uzunlugunda tek tek kurulur (H16-KOK-SEBEP-
                     RAPORU.md §2'nin birebir eşiği); ikisi de KIRPILMAMIS
                     mesaj basmali — esik artik YOK, cunku kesme kaldirildi.
  M-Y4 TEMIZ KOL   : DUZELTILMIS motor, KISA `/tmp`, `--uzun-yol` YOK; altin
                     kume BIT-BIT bozulmamis olmali (kabul olcutu (a)'nin bu
                     dosya icindeki tekrari).

🔴 KUM HAVUZU ADLARI: ne olculen kelimeyi ("yol"/"uzunluk"/"kesme") ne de
`normalize()`nin `<SHA>` desenine (16+ hex karakter) benzeyen bir dizgeyi
tasir — ikisi de ayri ayri OLCULDU KUSURLAR (YAPI_KAPISI_TASARIM ADR §3.1:
senaryo dizin adi kendi olcumune SIZDI; H16-KOK-SEBEP-RAPORU §2b: "ddd…"
dolgusu `<SHA>` sanildi). Dolgu harfleri HEX OLMAYAN ve NOTR ("zq" tekrari).

CIKIS KODLARI (proje sozlesmesi)
  0  dort kolun DORDU DE BEKLENDIGI GIBI (M-Y2 icin 'beklenen' KACIStir)
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kurulum coktu)
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
ARAC = os.path.join(KOK, "faz0", "altin_cikti.py")
REFERANS = os.path.join(KOK, "faz0", "altin_kapi.json")
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


# --------------------------------------------------------------- SABOTAJ (M-Y1/M-Y2)
# KALEM 1'in TERSİ: duzeltilmis motora kesmeyi GERI enjekte eder. Iki dize de
# hafiza.py:3326'nin BUGUNKU (duzeltilmis) ve DUN (sabotajli) haliyle BIREBIR
# eslesir — motor degisirse bu sabotaj da degismelidir (ESKI_TAM kalibiyle
# ayni ders, altin_olcut_mutanti.py'den).
_DUZELTILMIS = 'F.append("[KAPI] OLCUM YARIDA KESILDI: %s" % kesildi)'
_SABOTAJLI = 'F.append("[KAPI] OLCUM YARIDA KESILDI: %s" % kesildi[:160])'


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (H16-KESME-DUZELTME-BRIEF.md KALEM 1 satiri, "
            "hafiza.py:3326)." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _altin_cikti_kos(arglar, saniye=300):
    """`altin_cikti.py`yi verilen ek argumanlarla kosar; ham (returncode, cikti)
    doner. stdout/stderr AYRI okunur, sonra PYTHON icinde birlestirilir —
    `stderr=STDOUT` YASAK; boru yok, `returncode` DOGRUDAN kullanilir."""
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", ARAC] + arglar,
                           capture_output=True, timeout=saniye,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def my1_kesme_geri(taban):
    ad = "M-Y1 KESME GERI: --uzun-yol kolu, motora GERI enjekte edilen kesmeyi YAKALIYOR mu"
    sab_dizin = os.path.join(taban, "y1")
    os.makedirs(sab_dizin)
    motor = _sabotajli_motor(sab_dizin)
    rc, c = _altin_cikti_kos(["--karsilastir", REFERANS, "--motor", motor, "--uzun-yol"])
    if rc is None:
        _kayit(ad, OLCULEMEDI, c)
        return motor
    fark_var = rc == 1 and "davranis DEGISTI" in c
    _kayit(ad, BEKLENDIGI_GIBI if fark_var else BEKLENMEDIK,
          "sabotajli motor (kesme GERI) + --uzun-yol | exit=%s 'davranis DEGISTI'=%s "
          "(beklenen: 1/VAR -> ISIRDI: kapi kesmeyi YAKALADI)"
          % (rc, "VAR" if fark_var else "yok"))
    return motor


def my2_kor_kol(taban, sabotajli_motor):
    ad = ("M-Y2 KOR KOL (EN ONEMLI KOL): AYNI sabotaj, KISA /tmp ile kosulunca "
          "KACAR mi (BEKLENEN: evet)")
    if sabotajli_motor is None:
        _kayit(ad, OLCULEMEDI, "M-Y1 sabotajli motor uretemedi, bu kol atlandi")
        return
    rc, c = _altin_cikti_kos(["--karsilastir", REFERANS, "--motor", sabotajli_motor])
    if rc is None:
        _kayit(ad, OLCULEMEDI, c)
        return
    fark_yok = rc == 0 and "FARK YOK" in c
    _kayit(ad, BEKLENDIGI_GIBI if fark_yok else BEKLENMEDIK,
          "AYNI sabotajli motor + KISA /tmp, --uzun-yol YOK | exit=%s 'FARK YOK'=%s "
          "(BEKLENEN: 0/VAR -> KACTI: kisa yol bu sinifa YAPISAL OLARAK KORDUR; "
          "CI #76'yi aylarca gormeyen sey TAM budur, simdi olculuyor)"
          % (rc, "VAR" if fark_yok else "yok"))


# --------------------------------------------------------------- ESIK (M-Y3)
# H16-KOK-SEBEP-RAPORU.md §2'nin BIREBIR eşiği: onek 46 + kok + "/PROJE_HAFIZA.md"
# (16) = kok + 62. kesildi[:160] kok=98'de (uzunluk tam 160) HENUZ kesmez,
# kok=99'da (uzunluk 161) kesiyordu. Duzeltme sonrasi ikisi de KIRPILMAMIS
# basmali — esik artik yoktur, ama TARIHI sinir NOKTA NOKTA dogrulanir.

def _hedef_uzunlukta_kok(taban_dizini, hedef_uzunluk):
    on_ek = os.path.join(taban_dizini, "")   # taban + platform ayiricisi
    gerekli = hedef_uzunluk - len(on_ek)
    if gerekli < 1:
        raise AracKusuru("taban_dizini (%d) hedef uzunluktan (%d) zaten uzun"
                         % (len(on_ek), hedef_uzunluk))
    dolgu = ("zq" * ((gerekli // 2) + 1))[:gerekli]     # hex olmayan, notr dolgu
    kok = on_ek + dolgu
    if len(kok) != hedef_uzunluk:
        raise AracKusuru("kok uzunlugu hesap hatasi: %d != %d" % (len(kok), hedef_uzunluk))
    return kok


def _kur_ve_dizin_yap(kok):
    """h8_kesilme_dizin'in AYNISI (altin_cikti.py `_boz_dizin_yap`): kur, sonra
    PROJE_HAFIZA.md'yi dizine cevirir — ayni kesilme SINIFI, motora DOKUNMAZ."""
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run([sys.executable, "-X", "utf8", MOTOR, "kur", "--ad", "ESIK",
                        "--kok=" + kok], capture_output=True, timeout=120,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s"
                         % (r.returncode, ((r.stdout or "") + (r.stderr or ""))[-300:]))
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    os.remove(p)
    os.makedirs(p)


def _kapi_ham(kok, saniye=120):
    r = subprocess.run([sys.executable, "-X", "utf8", MOTOR, "kapi", "--kok=" + kok],
                       capture_output=True, timeout=saniye,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def my3_esik(taban):
    ad = "M-Y3 ESIK: duzeltme sonrasi kok=98 VE kok=99 ikisi de KIRPILMAMIS mesaj basar"
    kollar = []
    hepsi_tam = True
    for hedef in (98, 99):
        alt_taban = os.path.join(taban, "y3k%d" % hedef)
        os.makedirs(alt_taban)
        kok = _hedef_uzunlukta_kok(alt_taban, hedef)
        _kur_ve_dizin_yap(kok)
        rc, c = _kapi_ham(kok)
        satir = next((s for s in c.splitlines() if "OLCUM YARIDA KESILDI" in s), None)
        kuyruk_a = kok + os.sep + "PROJE_HAFIZA.md"
        kuyruk_b = kok.replace("\\", "/") + "/PROJE_HAFIZA.md"
        tam = satir is not None and (kuyruk_a in satir or kuyruk_b in satir)
        hepsi_tam = hepsi_tam and tam
        kollar.append("kok_uzunlugu=%d exit=%s kirpilmamis=%s"
                      % (len(kok), rc, "VAR" if tam else "YOK"))
    _kayit(ad, BEKLENDIGI_GIBI if hepsi_tam else BEKLENMEDIK,
          " | ".join(kollar) + " (beklenen: ikisi de kirpilmamis=VAR)")


def my4_temiz_kol(taban):
    ad = "M-Y4 TEMIZ KOL: duzeltilmis motor + KISA /tmp -> altin kume BIT-BIT BOZULMADI"
    rc, c = _altin_cikti_kos(["--karsilastir", REFERANS])
    if rc is None:
        _kayit(ad, OLCULEMEDI, c)
        return
    fark_yok = rc == 0 and "FARK YOK" in c
    _kayit(ad, BEKLENDIGI_GIBI if fark_yok else BEKLENMEDIK,
          "kisa /tmp, --uzun-yol YOK, --motor VARSAYILAN (duzeltilmis) | exit=%s "
          "'FARK YOK'=%s (beklenen: 0/VAR — kabul olcutu (a)'nin tekrari)"
          % (rc, "VAR" if fark_yok else "yok"))


def main():
    print("=" * 82)
    print("YOL UZUNLUGU MUTANTI — --uzun-yol kolu KESILME REGRESYONUNU yakaliyor mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  arac     : %s" % ARAC)
    print("  motor    : %s" % MOTOR)
    print("  referans : %s" % REFERANS)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h16km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        try:
            motor_sab = my1_kesme_geri(taban)
            my2_kor_kol(taban, motor_sab)
            my3_esik(taban)
            my4_temiz_kol(taban)
        except AracKusuru as e:
            print("\nARAC KUSURU: %s" % e)
            return 3
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

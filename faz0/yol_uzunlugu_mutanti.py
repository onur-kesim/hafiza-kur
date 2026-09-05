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
  M-Y3 ESIK        : DUZELTILMIS (sabotajsiz) motorla kok TAM kritik_kok VE
                     TAM kritik_kok+1 karakter uzunlugunda tek tek kurulur
                     (H16-KOK-SEBEP-RAPORU.md §2'nin TARIHI esigi — degeri
                     ARTIK SABIT DEGIL, formulden TURETILIR, bkz. asagidaki
                     ESIK bolumu); ikisi de KIRPILMAMIS mesaj basmali —
                     kesme kaldirildigindan bu YANA esik YOKTUR, ama TARIHI
                     sinir NOKTA NOKTA dogrulanmaya devam eder.
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
import re
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
# 🔴 IS_EMRI_3370_VE_ASIMETRI.md KALEM 2 (Onur kilidi 5 Eylul 2026): eski yorum
# "onek 46 + kok + '/PROJE_HAFIZA.md' (16) = kok + 62" idi — bu SABIT, hafiza.py:
# 3370'in B6 isaretine (`_ilk_satir_isaretli`) devredilmesiyle ESKIDI: `kesildi`
# artik (bu vakada SON_HATA[0] COK SATIRLI oldugu icin) " (+N satir: stderr)"
# isareti TASIYOR, iliski `len(kesildi) = kok + sabit` hala AFFINE ama SABIT
# DEGISTI. Sabit BURADA YAZILMAZ — `_kritik_kok_turet()` CANLI olcer (esik
# `_SABOTAJLI`den okunur, sabit iki FARKLI referans kok'ta olculup AFFINE
# oldugu DOGRULANIR). `kesildi[:160]` (esik) kritik_kok'ta (uzunluk tam esik)
# HENUZ kesmez, kritik_kok+1'de (uzunluk esik+1) keserdi — DUZELTME sonrasi
# ikisi de KIRPILMAMIS basmali (kesme YOK artik), ama TARIHI sinir NOKTA
# NOKTA dogrulanmaya devam eder; sinir isaretle KAYDIGI icin ESKI 98/99
# ARTIK sinirda DEGIL — sessizce daha az olcen bir kol olurdu (bkz. dosya
# basi KALEM 2 gerekcesi).

_KESILDI_ONEK = "[KAPI] OLCUM YARIDA KESILDI: "


def _sabotaj_esigi():
    """`_SABOTAJLI` dizgesinden kesme esigini (bugun 160) OKUR — sabit
    YAZILMAZ, sabotaj degisirse bu da otomatik degisir (h9_kesme_mutanti.py/
    olculemedi_kesme_mutanti.py'nin ayni adli fonksiyonuyla AYNI ilke: kod
    parcaciginin KENDISINDEN oku, ayri bir sabit YAZMA)."""
    m = re.search(r"\[:(\d+)\]", _SABOTAJLI)
    if not m:
        raise AracKusuru("sabotaj esigi _SABOTAJLI dizgesinden okunamadi (desen degisti mi?)")
    return int(m.group(1))


def _kesildi_govdesi(satir):
    """M-Y3 hukum satirindaki, ISARETIN GERCEKTEN eklendigi parca —
    `_KESILDI_ONEK`den SONRAKI kisim. `startswith` DEGIL `split`: basili
    satir baska metinle GIRINTILI olabilir, satir ONEKLE BASLAMAZ — yalniz
    ICERIR (h9_kesme_mutanti.py'nin `_h9_mesaj_govdesi`siyle AYNI ilke).
    Ayrac bulunamazsa None doner — cagiran SESSIZCE satira DUSMEZ."""
    parca = satir.split(_KESILDI_ONEK, 1)
    return parca[1] if len(parca) == 2 else None


def _kesildi_uzunlugu_olc(hedef_kok_uzunlugu, ust_taban):
    """DUZELTILMIS (gercek, sabotajsiz) motorla TEK bir referans kok icin
    `kesildi`nin (isaretiyle BIRLIKTE) uzunlugunu CANLI olcer — TAHMIN
    EDILMEZ. Kum havuzu bu olcum icin AYRI acilir (paylasilmaz)."""
    alt = os.path.join(ust_taban, "esikolc%d" % hedef_kok_uzunlugu)
    os.makedirs(alt)
    kok = _hedef_uzunlukta_kok(alt, hedef_kok_uzunlugu)
    _kur_ve_dizin_yap(kok)
    rc, c = _kapi_ham(kok)
    satir = next((s for s in c.splitlines() if "OLCUM YARIDA KESILDI" in s), None)
    if satir is None:
        raise AracKusuru("referans kok=%d icin OLCUM YARIDA KESILDI satiri bulunamadi (exit=%s)"
                         % (hedef_kok_uzunlugu, rc))
    govde = _kesildi_govdesi(satir)
    if govde is None:
        raise AracKusuru("'%s' ayraci referans satirda bulunamadi: %s"
                         % (_KESILDI_ONEK, satir.strip()))
    return len(govde.rstrip())


def _kritik_kok_turet(taban):
    """KALEM 2 (IS_EMRI_3370_VE_ASIMETRI.md, Onur kilidi 5 Eylul 2026): eski
    sabit 98/99'u SABIT YAZMAK yerine kritik kok'u FORMULDEN turetir.
    `hafiza.py:3370`nin `_ilk_satir_isaretli`ye devredilmesinden beri
    `len(kesildi) = kok + sabit` iliskisindeki SABIT degisti (eski deger
    ~62'ydi — BU FONKSIYON yeni degeri KENDI olcer, hicbir yerden kopyalamaz).
    Iliskinin GERCEKTEN affine (kok'tan BAGIMSIZ sabit fark) oldugu IKI
    FARKLI, esikten UZAK referans kok uzunlugunda dogrulanir; degilse
    AracKusuru (formul varsayimi kirilmis demektir — YANLIS bir sabitle
    SESSIZCE devam EDILMEZ)."""
    esik = _sabotaj_esigi()
    a_kok, b_kok = 150, 200   # herhangi iki FARKLI, guvenli (beklenen kritik
                              # bolgeden acikca uzak) referans deger
    len_a = _kesildi_uzunlugu_olc(a_kok, taban)
    len_b = _kesildi_uzunlugu_olc(b_kok, taban)
    fark_a = len_a - a_kok
    fark_b = len_b - b_kok
    if fark_a != fark_b:
        raise AracKusuru(
            "kesildi uzunlugu ile kok uzunlugu arasindaki iliski AFFINE degil "
            "(kok=%d->fark=%d, kok=%d->fark=%d) — formul varsayimi (mesaj=kok+sabit) "
            "KIRILDI, kritik kok TURETILEMEDI" % (a_kok, fark_a, b_kok, fark_b))
    return esik - fark_a, esik, fark_a


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
    ad = ("M-Y3 ESIK: duzeltme sonrasi kritik_kok VE kritik_kok+1 ikisi de "
          "KIRPILMAMIS mesaj basar")
    kritik_kok, esik, sabit_fark = _kritik_kok_turet(taban)
    kollar = []
    hepsi_tam = True
    for hedef in (kritik_kok, kritik_kok + 1):
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
          "kritik_kok=%d (esik=%d - sabit_fark=%d, FORMULDEN TURETILDI, sabit YAZILMADI) | "
          % (kritik_kok, esik, sabit_fark)
          + " | ".join(kollar) + " (beklenen: ikisi de kirpilmamis=VAR)")


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

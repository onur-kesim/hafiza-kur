#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H4 CIPLAK AD MUTANTI — `_h4_siniflandir`, canli hafizanin SADECE ADIYLA
(dizin BEYAN ETMEDEN) andigi bir dosyayi haksiz yere OLU mu sayiyor?
(besli-paket/IS_EMRI_H4.md, Onur kilidi 6 Eylul 2026 — Cowork'un gercek
projede (Uygulama - Tuzak Avcisi kopyasi) olctugu kusur)

NEDEN VAR — GERCEK PROJEDE OLCULDU
  hafiza-kur ilk kez gercek bir projede kosturuldugunda H4 kapisi 13 bulgu
  verdi; 11'i GURULTUYDU (%85). Sekiz vakanin sekizi de agacta TAM BIR yerde
  duruyordu (ornek: `QA_STRATEGI.md` -> `belgeler/QA_STRATEGI.md`), ama canli
  hafiza dosyayi yalniz ADIYLA anmisti (dizin beyan ETMEDEN). Eski kod
  `beyan_dizin` bos oldugunda "yol tutmuyor" hukmu VEREMEZ hale gelmesi
  gerekirken tam tersini yapiyordu: "tutulacak bir yol yok" -> `iyi=None` ->
  OLU. Oysa "yol tutmuyor" demek icin tutulacak bir yolun BEYAN EDILMIS
  OLMASI gerekir — hic beyan edilmemis bir yol icin bu hukum ANLAMSIZDIR.

  Duzeltme `_h4_siniflandir`e CIPLAK AD KOLU ekler: `iyi` bulunamamis VE
  beyan hicbir dizin bileseni TASIMIYOR VE agacta TAM BIR aday VARSA, dosya
  BULUNMUS sayilir — OLU degil. Hukum kanalinda "TASINMIS" ile AYNI kelime
  KULLANILMAZ (dosya taşınmadı, yalniz adiyla anildi); bu mutant ikisinin
  AYRI kelimelerle raporlandigini da sinar.

BES KOL — YALNIZ BIRI MUTANTTIR, UCU "KAPI GEVSEMEDI" KANITIDIR
  1. POZITIF KONTROL : sabotajsiz motor, ciplak ad + TEK eslesme -> OLU
                        DEGIL, ayri etiketli not VAR ("CIPLAK ADLA ANILDI").
  2. MUTANT          : AYNI vaka, sabotajli motorda OLU GERI GELIR (ISIRIR)
                        — kusurun kendisi budur.
  3. HIC YOK KORUNUR : ciplak ad + 0 eslesme -> IKI motorda da OLU (yeni kol
                        BU VAKAYA HIC GIRMEZ, `len(adaylar)==1` sarti
                        saglanmaz).
  4. COK ESLESME KORUNUR (Fable Bulgu 7) : ciplak ad + 2 eslesme -> IKI
                        motorda da OLU. Fable Bulgu 7'nin gerekcesi ("yalniz
                        basename eslesmesi tasinmis saymak README.md/
                        config.json gibi YAYGIN adlarda kapiyi silahsizlandirir")
                        burada da GECERLI — "yaygin" = BIRDEN COK yerde
                        bulunan; yeni kol YALNIZ TAM BIR eslesmede acilir.
  5. DIZINLI BEYAN KORUNUR : beyan bir dizin bileseni tasiyor (`www/index.html`)
                        ama dosya BASKA bir dizinde bulundu
                        (`magaza_rafi/site/index.html`) -> IKI motorda da OLU.
                        Bu vaka GERCEK projeden BIREBIR alindi — duzeltmeden
                        SONRA da orada OLU kalmisti.

  Kum havuzu PAYLASILMAZ (her kol/vaka KENDI kokunde kurulur, kendi ayri
  sabotajli motor kopyasini kullanir). Olculen: `kapi`nin STDOUT'undaki H4
  hukum satirlarinin METNI; stderr AYRI boruda tutulur, BIRLESTIRILMEZ.

CAPA: motora KOD PARCACIGIYLA anchor atilir, satir NUMARASIYLA DEGIL — motor
degisirse `count()!=1` ARAC KUSURU verir, YANLIS yere yamanmaz.

CIKIS KODLARI (proje sozlesmesi)
  0  bes kolun besi de BEKLENDIGI GIBI
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  en az bir kol OLCULEMEDI (BEKLENMEDIK yoksa)
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


# --------------------------------------------------------------- SABOTAJ
# IS_EMRI_H4.md KALEM (a): yeni CIPLAK AD kolunun KOSULUNU dusurur — kusurun
# KENDISI budur. Iki dize de hafiza.py'nin BUGUNKU (duzeltilmis) haliyle
# BIREBIR eslesir — motor degisirse bu sabotaj da degismelidir.
_DUZELTILMIS = "ciplak_tek = (not beyan_dizin and len(adaylar) == 1)"
_SABOTAJLI = "ciplak_tek = False"


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (besli-paket/IS_EMRI_H4.md, hafiza.py "
            "_h4_siniflandir())." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, kok, saniye=120):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok=" + kok],
                       capture_output=True, timeout=saniye,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _kur(motor, kok):
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, out, err = _kos(motor, ["kur", "--ad", "H4CIPLAK"], kok)
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (out + err)[-300:]))


def _vaka_kur(motor, kok, beyan, dosyalar):
    """`beyan`: canli hafizaya backtick'li referans olarak eklenecek yol metni.
    `dosyalar`: {goreli_yol: icerik} — agacta GERCEKTEN olusturulacak dosyalar
    (bos sozluk = agacta HICBIR eslesme, vaka 3 icin)."""
    _kur(motor, kok)
    for rel, icerik in dosyalar.items():
        p = os.path.join(kok, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(icerik)
    canli = os.path.join(kok, "PROJE_HAFIZA.md")
    with open(canli, "a", encoding="utf-8", newline="\n") as f:
        f.write("\nDokuman: `%s` referansi.\n" % beyan)


def _h4_stdout_satirlari(stdout_metni):
    """`kapi`nin STDOUT'undaki H4 hukum satirlari — stderr AYRI boruda tutulur,
    BIRLESTIRILMEZ (is emri §3: olculen kapi'nin stdout H4 hukum satirlarinin
    METNIDIR)."""
    return [s for s in stdout_metni.splitlines() if "H4:" in s or "[H4]" in s]


def _olu_mu(satirlar, ad):
    return any("[H4]" in s and ("OLU BAGLANTI: %s" % ad) in s for s in satirlar)


def _ciplak_adla_anildi_mi(satirlar, ad):
    return any("CIPLAK ADLA ANILDI" in s and ("'%s'" % ad) in s for s in satirlar)


def vaka1_pozitif_kontrol(taban):
    ad = ("1. POZITIF KONTROL: ciplak ad + TEK eslesme -> sabotajsiz motorda "
          "OLU DEGIL, ayri etiketli not VAR")
    kok = os.path.join(taban, "v1")
    try:
        _vaka_kur(MOTOR, kok, "RAPOR_TEK.md", {"belgeler/RAPOR_TEK.md": "# rapor\n"})
        rc, out, err = _kos(MOTOR, ["kapi"], kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    satirlar = _h4_stdout_satirlari(out)
    ciplak_var = _ciplak_adla_anildi_mi(satirlar, "RAPOR_TEK.md")
    olu_var = _olu_mu(satirlar, "RAPOR_TEK.md")
    dogru = ciplak_var and not olu_var
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "sabotajsiz motor | 'CIPLAK ADLA ANILDI' notu=%s | '[H4] OLU BAGLANTI'=%s "
          "(beklenen: VAR / yok)\n      H4 satirlari: %s"
          % ("VAR" if ciplak_var else "yok", "VAR" if olu_var else "yok",
             " | ".join(s.strip() for s in satirlar) or "(hicbiri)"))


def vaka2_mutant(taban):
    ad = "2. MUTANT: AYNI vaka, sabotajli motorda OLU GERI GELIR (ISIRMALI)"
    kok = os.path.join(taban, "v2")
    sab_dizin = os.path.join(taban, "v2_sab")
    os.makedirs(sab_dizin, exist_ok=True)
    try:
        _vaka_kur(MOTOR, kok, "RAPOR_TEK.md", {"belgeler/RAPOR_TEK.md": "# rapor\n"})
        motor_sab = _sabotajli_motor(sab_dizin)
        rc, out, err = _kos(motor_sab, ["kapi"], kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    satirlar = _h4_stdout_satirlari(out)
    olu_var = _olu_mu(satirlar, "RAPOR_TEK.md")
    _kayit(ad, BEKLENDIGI_GIBI if olu_var else BEKLENMEDIK,
          "sabotajli motor (ciplak_tek daima False) | '[H4] OLU BAGLANTI'=%s "
          "(beklenen: VAR -> kusur GERI GELDI, ISIRDI)\n      H4 satirlari: %s"
          % ("VAR" if olu_var else "yok",
             " | ".join(s.strip() for s in satirlar) or "(hicbiri)"))


def vaka3_hic_yok(taban):
    ad = "3. HIC YOK KORUNUR: ciplak ad + 0 eslesme -> IKI motorda da OLU"
    kok_temiz = os.path.join(taban, "v3_temiz")
    kok_sab = os.path.join(taban, "v3_sab")
    sab_dizin = os.path.join(taban, "v3_sabmotor")
    os.makedirs(sab_dizin, exist_ok=True)
    try:
        _vaka_kur(MOTOR, kok_temiz, "YOK_HICBIRYERDE.md", {})
        _vaka_kur(MOTOR, kok_sab, "YOK_HICBIRYERDE.md", {})
        motor_sab = _sabotajli_motor(sab_dizin)
        rc_t, out_t, _ = _kos(MOTOR, ["kapi"], kok_temiz)
        rc_s, out_s, _ = _kos(motor_sab, ["kapi"], kok_sab)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    olu_temiz = _olu_mu(_h4_stdout_satirlari(out_t), "YOK_HICBIRYERDE.md")
    olu_sab = _olu_mu(_h4_stdout_satirlari(out_s), "YOK_HICBIRYERDE.md")
    dogru = olu_temiz and olu_sab
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "duzeltilmis motor OLU=%s | sabotajli motor OLU=%s (beklenen: ikisi de "
          "VAR — Fable Bulgu 7 (c): 0 eslesme yeni kola hic GIRMEZ)"
          % ("VAR" if olu_temiz else "yok", "VAR" if olu_sab else "yok"))


def vaka4_cok_eslesme(taban):
    ad = ("4. COK ESLESME KORUNUR (Fable Bulgu 7): ciplak ad + 2 eslesme -> "
          "IKI motorda da OLU")
    dosyalar = {"klasor_a/COK_YERDE.md": "# a\n", "klasor_b/COK_YERDE.md": "# b\n"}
    kok_temiz = os.path.join(taban, "v4_temiz")
    kok_sab = os.path.join(taban, "v4_sab")
    sab_dizin = os.path.join(taban, "v4_sabmotor")
    os.makedirs(sab_dizin, exist_ok=True)
    try:
        _vaka_kur(MOTOR, kok_temiz, "COK_YERDE.md", dosyalar)
        _vaka_kur(MOTOR, kok_sab, "COK_YERDE.md", dosyalar)
        motor_sab = _sabotajli_motor(sab_dizin)
        rc_t, out_t, _ = _kos(MOTOR, ["kapi"], kok_temiz)
        rc_s, out_s, _ = _kos(motor_sab, ["kapi"], kok_sab)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    olu_temiz = _olu_mu(_h4_stdout_satirlari(out_t), "COK_YERDE.md")
    olu_sab = _olu_mu(_h4_stdout_satirlari(out_s), "COK_YERDE.md")
    dogru = olu_temiz and olu_sab
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "duzeltilmis motor OLU=%s | sabotajli motor OLU=%s (beklenen: ikisi de "
          "VAR — yaygin adlar kapiyi SILAHSIZLANDIRMAZ)"
          % ("VAR" if olu_temiz else "yok", "VAR" if olu_sab else "yok"))


def vaka5_dizinli_beyan(taban):
    ad = ("5. DIZINLI BEYAN KORUNUR (gercek projeden BIREBIR): beyan dizinli, "
          "dosya BASKA dizinde bulundu -> IKI motorda da OLU")
    dosyalar = {"magaza_rafi/site/index.html": "<html></html>\n"}
    kok_temiz = os.path.join(taban, "v5_temiz")
    kok_sab = os.path.join(taban, "v5_sab")
    sab_dizin = os.path.join(taban, "v5_sabmotor")
    os.makedirs(sab_dizin, exist_ok=True)
    try:
        _vaka_kur(MOTOR, kok_temiz, "www/index.html", dosyalar)
        _vaka_kur(MOTOR, kok_sab, "www/index.html", dosyalar)
        motor_sab = _sabotajli_motor(sab_dizin)
        rc_t, out_t, _ = _kos(MOTOR, ["kapi"], kok_temiz)
        rc_s, out_s, _ = _kos(motor_sab, ["kapi"], kok_sab)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    olu_temiz = _olu_mu(_h4_stdout_satirlari(out_t), "www/index.html")
    olu_sab = _olu_mu(_h4_stdout_satirlari(out_s), "www/index.html")
    dogru = olu_temiz and olu_sab
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "duzeltilmis motor OLU=%s | sabotajli motor OLU=%s (beklenen: ikisi de "
          "VAR — dizinli beyan yeni kolu hic ATESLEMEZ)"
          % ("VAR" if olu_temiz else "yok", "VAR" if olu_sab else "yok"))


def main():
    print("=" * 82)
    print("H4 CIPLAK AD MUTANTI — canli hafizanin SADECE ADIYLA andigi dosya haksiz OLU mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h4cad_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        try:
            vaka1_pozitif_kontrol(taban)
            vaka2_mutant(taban)
            vaka3_hic_yok(taban)
            vaka4_cok_eslesme(taban)
            vaka5_dizinli_beyan(taban)
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — PAKETTEN KOSUM (BITTI maddesi 4 ve maddesi 2(ii)).

NEDEN VAR (olculdu 14 Agu 2026)
  Bugune kadarki BUTUN kosumlar depodaki `skill/scripts/hafiza.py` ile yapildi.
  PAKETTEN ACILMIS motor HIC kosmadi. Iki BITTI maddesi tam olarak bunu istiyor:
     madde 4     : ".skill paketini kurup taze bir projede 5 dakikada
                    calistirabilir (KURULUM BELGESIYLE)"
     madde 2(ii) : ".skill taze bir projede GERCEK Windows'ta kurulup
                    kur->kapi->isir kosuyor"
  Ve olculdu: `capraz.yml`de `paketle`/`.skill` icin SIFIR esleme vardi.

  🔴 BU ARACIN ILK SURUMUNUN KUSURU (14 Agu, CI #45 yesilken bulundu):
     Arac motoru PAKET DIZININDEN kosturuyordu. Oysa `SKILL.md` §2 "Sifirdan
     kurulum" DORT adim tarif ediyor ve BIRINCISI "motoru projeye kopyala ->
     <proje>/araclar/hafiza/hafiza.py". Yani arac, BELGENIN tarif ettigi akisi
     degil KENDI akisini olcuyordu; madde 4'un "(kurulum belgesiyle)" sarti
     OLCULMEMIS kaliyordu. CI yesildi ve bunu HIC gostermiyordu.
     Duzeltme: belgenin akisi izlenir VE belgenin kendisi kapiya baglanir.

NE OLCER — IKI AYRI EKSEN
  KAPI-1 BELGE : kostugum adimlarin HER BIRI, PAKETTEKI `SKILL.md`in "Sifirdan
                 kurulum" blokunda geciyor mu? Belge kayarsa (ornegin komut adi
                 degisirse) kapi KIRMIZI yanar. Boylece "belge de bir arayuzdur
                 ve yalan soyleyebilir" dersi BEYAN olmaktan cikip OLCUM olur.
                 Depodaki degil PAKETTEKI SKILL.md okunur — kullaniciya giden o.
  KAPI-2 CANLI : belgenin akisiyla (once motoru projeye kopyala) TAZE projede
                 `kur` -> `kapi` -> `isir`; cikis kodlari SOZLESMEYE vurulur ve
                 toplam sure 300 sn olcutune (madde 4: "5 dakikada").

  Ortusmezler: belge dogru olup motor cokebilir (KAPI-2), ya da motor calisip
  belge baska bir komut tarif ediyor olabilir (KAPI-1). Biri otekinin yerine gecmez.

CIKIS KODU SOZLESMESI — `hafiza.py` sat. 4845'ten OKUNDU, uydurulmadi
  kur   : 0 beklenir.
  kapi  : 0 beklenir ("YESIL (SINIRLI)" de 0'dir; taze projede H9 OLCULEMEDI).
  isir  : 0 = hepsi isirdi · 1 = KAPI KOR · 2 = olculemeyen mutant · 4 = temiz surum FAIL.
          TAZE bir projede 2 SAGLIKLIDIR ve KABUL EDILIR: M-H1b kurulamaz cunku
          henuz `derle` kosmadi. Motorun kendi yorumu da budur (sat. 4839-4844:
          "`isir && ...` diyen CI sarmalayicisi onu basarisiz etiketliyordu").
          1 ve 4 KIRMIZIDIR. `|| true` ile hepsini yutmak SAHTE YESIL uretir.

KOR OLMADIGININ OLCUMU (doktrin 1: olculmeyen kapinin hukmu yoktur)
  A. SOZLESME SINIFLANDIRMASI: sentetik 0/1/2/4 kodlari siniflandiriciya verilir;
     1 ve 4 KIRMIZI, 0 ve 2 YESIL cikmali. Saf mantik, ucuz, kesin.
  B. CANLI MOTOR: kurulmus motora sozdizimi hatasi enjekte edilir, `kur` yeniden
     kosar; SIFIRDAN FARKLI donmeli. Arac cikis kodlarini GERCEKTEN okuyor mu?
  C. BELGE MUTANTI: paketteki `SKILL.md`in kurulum blokundaki `kapi` komutu
     bellekte `denetle` yapilir; KAPI-1 KIRMIZI yanmali. Belge kapisi kor mu?

NE OLCMEZ (hukum degil, SINIR)
  1. Belgenin ANLAMINI olcmez, GECTIGINI olcer: SKILL.md blokunda komut satiri
     var mi. Belge yanlis SIRAYLA anlatirsa bunu gormez.
  2. `derle` sonrasi ikinci bir `isir` (yani isir=0 hali) olculmez.
  3. Paketin ICERIGI olculmez — o `paketle.sh`in iki kapisi + `faz0/paket_mutanti.py`.
  4. `devral` yolu olculmez; bu arac yalnizca "Sifirdan kurulum"u kosar.

CIKIS KODLARI
  0  iki kapi da temiz VE uc korluk olcumu de gecti
  1  bir kapi kirmizi (belge kaymis / komut sozlesmeyi bozmus / sure asilmis / kor)
  2  olculemedi (paket yok, acilamadi, SKILL.md blogu bulunamadi)
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile


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
VARSAYILAN = os.path.join(KOK, "hafiza-kur.skill")
SURE_OLCUTU = 300.0                      # madde 4: "5 dakikada"

# Belgenin (`SKILL.md` §2 "Sifirdan kurulum") tarif ettigi motor yolu.
BELGE_MOTOR_YOLU = ("araclar", "hafiza", "hafiza.py")

# (ad, ek argumanlar, kabul edilen cikis kodlari, BELGEDE ARANACAK desen)
ZINCIR = (
    ("kur", ["--ad", "Paket Denemesi"], (0,), "hafiza.py kur --kok="),
    ("kapi", [], (0,), "hafiza.py kapi --kok="),
    ("isir", [], (0, 2), "hafiza.py isir --kok="),
)
ISIR_NOTU = {0: "hepsi isirdi", 1: "KAPI KOR", 2: "olculemeyen mutant (taze projede SAGLIKLI)",
             4: "temiz surum zaten FAIL"}

_BASLIK = re.compile(r"^#+\s*S[iı]f[iı]rdan kurulum\s*$", re.M | re.I)


def kurulum_blogu(skill_md):
    """`SKILL.md`in "Sifirdan kurulum" basligindan sonraki ilk cit blogu.

    Bulunamazsa None doner -> OLCULEMEDI. Sessiz PASS verilmez."""
    m = _BASLIK.search(skill_md)
    if not m:
        return None
    kalan = skill_md[m.end():]
    i = kalan.find("```")
    if i < 0:
        return None
    j = kalan.find("```", i + 3)
    if j < 0:
        return None
    return kalan[i + 3:j]


_YOL = re.compile(r"([\w./<>\\-]*)hafiza\.py")


def kapi1_belge(blok):
    """Kostugum her adim belgede geciyor mu? IKI SORU, ikisi de gerekli.

    (a) KOMUT: kostugum uc komut satiri blokta geciyor mu?
    (b) YOL  : bloktaki HER `hafiza.py` referansi `araclar/hafiza/` altinda mi?
        (b) olmadan belge KENDI ICINDE tutarsiz olabilir — 1. adim motoru
        `<proje>/bin/`e koydurup komutlar `araclar/hafiza/`dan kosabilir. Bu
        SABOTAJ PROBUYLA olculdu (S-6): yalniz "gecti mi" sorusu KACIRIYORDU."""
    bulgu = []
    kopyala = "/".join(BELGE_MOTOR_YOLU)
    dizin = kopyala[:-len("hafiza.py")]                # "araclar/hafiza/"
    for ad, _, _, desen in ZINCIR:
        if desen not in blok:
            bulgu.append("belgede `%s` GECMIYOR (arac bu komutu kosuyor)" % desen)
    yollar = [m.group(1) for m in _YOL.finditer(blok)]
    if not yollar:
        bulgu.append("belgede hic `hafiza.py` referansi YOK")
    for y in sorted(set(yollar)):
        if not y.endswith(dizin):
            bulgu.append("belgedeki motor yolu `%shafiza.py` beklenen `%s` DEGIL" % (y, kopyala))
    return bulgu


def kabul_mu(komut, kod):
    for ad, _, kabul, _ in ZINCIR:
        if ad == komut:
            return kod in kabul
    return False


def kos(motor, komut, ek, proje):
    b = time.time()
    p = subprocess.run([sys.executable, motor, komut, "--kok", proje] + ek,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, time.time() - b, p.stdout.decode("utf-8", "replace")


def main():
    paket = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    if not os.path.isfile(paket):
        print("SONUC: ÖLÇÜLEMEDİ — paket yok: %s" % paket)
        return 2

    print("=== PAKETTEN KOSUM === paket: %s (%d B) · platform: %s"
          % (os.path.basename(paket), os.path.getsize(paket), sys.platform))

    gecici = tempfile.mkdtemp(prefix="paketten-kos-")
    try:
        acik = os.path.join(gecici, "paket")
        proje = os.path.join(gecici, "taze-proje")
        os.makedirs(proje)
        try:
            with zipfile.ZipFile(paket) as z:
                z.extractall(acik)
                sayi = len([a for a in z.namelist() if not a.endswith("/")])
        except Exception as e:                                # noqa: BLE001
            print("SONUC: ÖLÇÜLEMEDİ — paket acilamadi: %s" % e)
            return 2

        kaynak_motor = os.path.join(acik, "scripts", "hafiza.py")
        skill_md = os.path.join(acik, "SKILL.md")
        if not os.path.isfile(kaynak_motor) or not os.path.isfile(skill_md):
            print("  ACILDI          : %d dosya" % sayi)
            print("SONUC: KIRMIZI — pakette scripts/hafiza.py ya da SKILL.md YOK.")
            return 1
        ham = open(kaynak_motor, "rb").read()
        print("  ACILDI          : %d dosya · motor %d B · SHA %s…"
              % (sayi, len(ham), hashlib.sha256(ham).hexdigest().upper()[:16]))

        # ---- KAPI-1 BELGE (paketteki SKILL.md okunur) -----------------------
        with open(skill_md, encoding="utf-8", newline="") as f:
            metin = f.read()
        blok = kurulum_blogu(metin)
        if blok is None:
            print("  KAPI-1 BELGE    : ÖLÇÜLEMEDİ — SKILL.md'de 'Sifirdan kurulum' blogu yok")
            print("\nSONUC: ÖLÇÜLEMEDİ — belge blogu bulunamadi; sessiz PASS verilmez.")
            return 2
        k1 = kapi1_belge(blok)
        print("  KAPI-1 BELGE    : %s (%d satirlik blok)"
              % ("YESIL (4 adimin 4'u belgede)" if not k1 else "KIRMIZI — %d eksik" % len(k1),
                 blok.count("\n")))
        for x in k1:
            print("      ! %s" % x)

        # ---- KAPI-2 CANLI (BELGENIN AKISI: once motoru projeye kopyala) -----
        hedef = os.path.join(proje, *BELGE_MOTOR_YOLU)
        os.makedirs(os.path.dirname(hedef), exist_ok=True)
        shutil.copy2(kaynak_motor, hedef)
        print("  BELGE ADIM 1    : motor projeye kopyalandi -> %s"
              % "/".join(BELGE_MOTOR_YOLU))

        k2 = []
        toplam = 0.0
        for komut, ek, kabul, _ in ZINCIR:
            kod, sure, _c = kos(hedef, komut, ek, proje)
            toplam += sure
            not_ = (" — SOZLESME: %s" % ISIR_NOTU.get(kod, "BILINMEYEN KOD")) if komut == "isir" else ""
            print("  %-15s : exit %-2s %s (%.1f sn · kabul %s)%s"
                  % (komut, kod, "✓" if kod in kabul else "✗", sure,
                     "/".join(str(x) for x in kabul), not_))
            if kod not in kabul:
                k2.append("%s sozlesmeyi bozdu: exit %s" % (komut, kod))
        print("  TOPLAM SURE     : %.1f sn  (olcut: <%.0f sn — madde 4)" % (toplam, SURE_OLCUTU))
        if toplam >= SURE_OLCUTU:
            k2.append("sure olcutu asildi: %.1f sn" % toplam)

        # ---- KOR OLMADIGININ OLCUMU ----------------------------------------
        kor = []
        yanlis = [k for k in (1, 4) if kabul_mu("isir", k)] + \
                 [k for k in (0, 2) if not kabul_mu("isir", k)]
        if yanlis:
            kor.append("A) sozlesme siniflandirmasi YANLIS: %s" % yanlis)

        proje2 = os.path.join(gecici, "taze-proje-2")
        os.makedirs(proje2)
        with open(hedef, "ab") as f:
            f.write(b"\nbu satir sozdizimi hatasidir(\n")
        kod2, _, _ = kos(hedef, "kur", ["--ad", "Bozuk"], proje2)
        if kod2 == 0:
            kor.append("B) bozuk motorla `kur` yine exit 0 dondu — cikis kodu OKUNMUYOR")

        # C) belge mutantlari — IKI AYRI EKSEN (komut adi · motor yolu)
        belge_mutantlari = (
            ("C1 komut", blok.replace("hafiza.py kapi --kok=", "hafiza.py denetle --kok=", 1)),
            ("C2 yol", blok.replace("/".join(BELGE_MOTOR_YOLU), "bin/hafiza.py")),
        )
        c_hali = []
        for ad, bozuk in belge_mutantlari:
            if bozuk == blok:
                kor.append("C) %s mutanti KURULAMADI (desen blokta yok)" % ad)
                c_hali.append("%s KURULAMADI" % ad)
            elif not kapi1_belge(bozuk):
                kor.append("C) %s mutanti KACTI — KAPI-1 bu kaymayi GORMUYOR" % ad)
                c_hali.append("%s KACTI" % ad)
            else:
                c_hali.append("%s ISIRDI ✓" % ad)
        print("  KOR DEGIL       : A) siniflandirma %s · B) bozuk motorla kur -> exit %s %s · "
              "C) belge mutantlari: %s"
              % ("4/4 ✓" if not yanlis else "KIRMIZI", kod2, "✓" if kod2 else "✗",
                 " · ".join(c_hali)))

        for x in k2 + kor:
            print("      ! %s" % x)
        if k1 or k2 or kor:
            print("\nSONUC: KIRMIZI — paket kurulumu olcutu KARSILAMADI.")
            return 1
        print("\nSONUC: YESIL — BELGENIN akisiyla, paketten acilmis motor TAZE projede "
              "kur→kapi→isir kosdu (%.1f sn, %s)." % (toplam, sys.platform))
        return 0
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — PAKETTEN KOSUM (BITTI maddesi 4 ve maddesi 2(ii)).

NEDEN VAR (olculdu 14 Agu 2026)
  Bugune kadarki BUTUN kosumlar depodaki `skill/scripts/hafiza.py` ile yapildi.
  PAKETTEN ACILMIS motor HIC kosmadi — ne Linux'ta ne Windows'ta. Oysa iki BITTI
  maddesi tam olarak bunu istiyor:
     madde 4     : ".skill paketini kurup taze bir projede 5 dakikada calistirabilir"
     madde 2(ii) : ".skill taze bir projede GERCEK Windows'ta kurulup kur->kapi->isir kosuyor"
  Ve olculdu: `capraz.yml`de `paketle`/`.skill` icin SIFIR esleme vardi.

NE OLCER
  1. Paket acilir (stdlib `zipfile`; hedefte `unzip` GEREKMEZ — Windows kolu bu
     yuzden calisir), TAZE bir dizine.
  2. TAZE bir proje dizininde, ACILMIS motorla: `kur` -> `kapi` -> `isir`.
  3. Her komutun cikis kodu SOZLESMEYE gore yorumlanir (asagida).
  4. Toplam duvar-saati suresi olculur ve 300 sn olcutune vurulur (madde 4).

CIKIS KODU SOZLESMESI — `hafiza.py` sat. 4845'ten OKUNDU, uydurulmadi
  kur   : 0 beklenir.
  kapi  : 0 beklenir ("YESIL (SINIRLI)" de 0'dir; taze projede H9 OLCULEMEDI).
  isir  : 0 = hepsi isirdi · 1 = KAPI KOR · 2 = olculemeyen mutant · 4 = temiz surum FAIL.
          TAZE bir projede 2 SAGLIKLIDIR ve KABUL EDILIR: M-H1b kurulamaz cunku
          henuz `derle` kosmadi. Motorun kendi yorumu da budur (sat. 4839-4844:
          "`isir && ...` diyen CI sarmalayicisi onu basarisiz etiketliyordu").
          1 ve 4 KIRMIZIDIR. `|| true` ile hepsini yutmak SAHTE YESIL uretir —
          bu araciin varlik sebebi tam olarak o tuzagi kapatmaktir.

KOR OLMADIGININ OLCUMU (doktrin 1: olculmeyen kapinin hukmu yoktur)
  A. SOZLESME SINIFLANDIRMASI: 0/1/2/4 sentetik kodlari siniflandiriciya verilir;
     1 ve 4 KIRMIZI, 0 ve 2 YESIL cikmali. Saf mantik, ucuz, kesin.
  B. CANLI: acilmis motora sozdizimi hatasi enjekte edilir ve `kur` yeniden kosar;
     SIFIRDAN FARKLI donmelidir. Bu, araciin cikis kodlarini gercekten OKUDUGUNU
     olcer (her zaman yesil basan bir arac buradan kirmizi yanar).

NE OLCMEZ (hukum degil, SINIR)
  1. Kurulum BELGESININ dogrulugunu olcmez (madde 4 "kurulum belgesiyle" der);
     bu arac komutlari SKILL.md'den degil sabit listeden kosar.
  2. `derle` sonrasi ikinci bir `isir` (yani isir=0 hali) olculmez.
  3. Paketin ICERIGINI olcmez — o `paketle.sh`in iki kapisi ve `faz0/paket_mutanti.py`.

CIKIS KODLARI
  0  paket acildi, uc komut da sozlesmeye uydu, sure olcutu tuttu, kor degil
  1  bir komut sozlesmeyi bozdu / sure asildi / kor oldugu olculdu
  2  olculemedi (paket yok, acilamadi) — sessiz PASS verilmez
"""
import hashlib
import os
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

# (ad, ek argumanlar, kabul edilen cikis kodlari)
ZINCIR = (
    ("kur", ["--ad", "Paket Denemesi"], (0,)),
    ("kapi", [], (0,)),
    ("isir", [], (0, 2)),
)
ISIR_NOTU = {0: "hepsi isirdi", 1: "KAPI KOR", 2: "olculemeyen mutant (taze projede SAGLIKLI)",
             4: "temiz surum zaten FAIL"}


def kabul_mu(komut, kod):
    for ad, _, kabul in ZINCIR:
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

    boyut = os.path.getsize(paket)
    print("=== PAKETTEN KOSUM === paket: %s (%d B) · platform: %s"
          % (os.path.basename(paket), boyut, sys.platform))

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

        motor = os.path.join(acik, "scripts", "hafiza.py")
        if not os.path.isfile(motor):
            print("  ACILDI          : %d dosya" % sayi)
            print("SONUC: KIRMIZI — pakette scripts/hafiza.py YOK.")
            return 1
        ham = open(motor, "rb").read()
        print("  ACILDI          : %d dosya · motor %d B · SHA %s…"
              % (sayi, len(ham), hashlib.sha256(ham).hexdigest().upper()[:16]))

        bulgu = []
        toplam = 0.0
        for komut, ek, kabul in ZINCIR:
            kod, sure, _ = kos(motor, komut, ek, proje)
            toplam += sure
            not_ = ""
            if komut == "isir":
                not_ = " — SOZLESME: %s" % ISIR_NOTU.get(kod, "BILINMEYEN KOD")
            damga = "✓" if kod in kabul else "✗"
            print("  %-15s : exit %-2s %s (%.1f sn · kabul %s)%s"
                  % (komut, kod, damga, sure, "/".join(str(x) for x in kabul), not_))
            if kod not in kabul:
                bulgu.append("%s sozlesmeyi bozdu: exit %s" % (komut, kod))

        print("  TOPLAM SURE     : %.1f sn  (olcut: <%.0f sn — madde 4)" % (toplam, SURE_OLCUTU))
        if toplam >= SURE_OLCUTU:
            bulgu.append("sure olcutu asildi: %.1f sn" % toplam)

        # --- KOR OLMADIGININ OLCUMU -------------------------------------------
        kor = []
        yanlis = [k for k in (1, 4) if kabul_mu("isir", k)] + \
                 [k for k in (0, 2) if not kabul_mu("isir", k)]
        if yanlis:
            kor.append("sozlesme siniflandirmasi YANLIS: %s" % yanlis)
        proje2 = os.path.join(gecici, "taze-proje-2")
        os.makedirs(proje2)
        with open(motor, "ab") as f:
            f.write(b"\nbu satir sozdizimi hatasidir(\n")
        kod2, _, _ = kos(motor, "kur", ["--ad", "Bozuk"], proje2)
        if kod2 == 0:
            kor.append("bozuk motorla `kur` yine exit 0 dondu — arac cikis kodunu OKUMUYOR")
        print("  KOR DEGIL       : sozlesme siniflandirmasi %s · bozuk motorla kur -> exit %s %s"
              % ("4/4 ✓" if not yanlis else "KIRMIZI", kod2, "✓" if kod2 else "✗"))

        for x in bulgu + kor:
            print("      ! %s" % x)
        if bulgu or kor:
            print("\nSONUC: KIRMIZI — paket kurulumu olcutu KARSILAMADI.")
            return 1
        print("\nSONUC: YESIL — paketten acilmis motor TAZE projede kur→kapi→isir kosdu "
              "(%.1f sn, %s)." % (toplam, sys.platform))
        return 0
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

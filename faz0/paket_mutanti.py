#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — PAKET MUTANTI (`paketle.sh`in iki kapisi gercekten isiriyor mu?).

NEDEN VAR (olculdu 14 Agu 2026)
  `paketle.sh` bir SHA256 kapisi OLDUGUNU soyluyordu ama kapi OLUYDU:
  kontrol `[ -n "$BEYAN" ]` ile korunuyordu ve `SKILL.md`de 64'luk hex SIFIRDI
  (olculdu: `grep -coE '[0-9A-F]{64}' skill/SKILL.md` -> 0), yani `if` HIC
  girilmiyordu. Ustelik `SKILL.md` sat. 245-249 SHA yazmamayi OLCULMUS bir
  dersle savunuyor ("bayatlar; iki surum boyunca gorulmedi") — yani betigin
  BASLIGI ile belgenin KARARI carpisiyordu ve kod sessizce belgenin tarafini
  tutuyordu. Sinif IKINCI kez isirdi (1: LISANS, 10 Agu): "SKILL.md beyani ile
  paketin gercegi tutmuyor, kimse olcmuyor."

  Ayrica olculdu: `capraz.yml`de `paketle` ve `.skill` icin SIFIR esleme —
  paketleme, madde 4'un ve madde 2(ii)'nin dayandigi TEK yuzey, hic kosmuyordu.

NE OLCER — IKI AYRI EKSEN (kapilar `paketle.sh`in icinde yasar, burasi ISIRMAYI olcer)
  KAPI-1 MOTOR BIT-BIT : zip'ten geri cikarilan `scripts/hafiza.py` kaynakla ayni mi
  KAPI-2 ENVANTER      : `skill/` altindaki filtre-disi her dosya pakette var mi
                         (ve pakette FAZLA dosya yok mu)

  Iki kapi ORTUSMEZ ve biri otekinin yerine GECMEZ: motor bit-bit dogru olup
  `references/` tumden dusebilir (LISANS sinifi); ya da butun dosyalar yerinde
  olup motorun baytlari satir-sonu cevrimiyle bozulabilir (`.gitattributes`
  `* -text` dersinin paketleme karsiligi).

MUTANTLAR — ikisi de GERCEK arizadir, uydurma degil
  M-1 `zip -l` (satir-sonu cevrimi)  -> KAPI-1 isirmali, KAPI-2 yesil kalmali
      Olculdu: hafiza.py 259.228 -> 264.431 bayt (5.203 satirin LF'i CRLF oldu).
  M-2 `-x 'references/*'`            -> KAPI-2 isirmali, KAPI-1 yesil kalmali
      Olculdu: alti `references/*.md` paketten duser, motor saglam kalir.

NE OLCMEZ (hukum degil, SINIR)
  1. Paketin KURULUP KOSTUGUNU olcmez — o `faz0/paketten_kos.py`in isidir.
  2. `zip` yoksa OLCULEMEDI der (exit 2), sessiz PASS vermez. Bu yuzden CI'da
     ubuntu kolunda kosar; windows kolu paketi ARTEFAKT olarak alir (gercek
     kullanicinin yaptigi da budur: paket bir kez uretilir, baska yerde kurulur).
  3. `paketle.sh`in kendi `set -eu` disi yollari (ornegin `zip` yarida olurse)
     olculmedi.

CIKIS KODLARI
  0  temiz agac iki kapidan da gecti VE 2/2 mutant AYRI eksende ISIRDI
  1  temiz agac kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  olculemedi (zip yok, dosya yok) — sessiz PASS verilmez
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

_K1 = re.compile(r"^KAPI-1 MOTOR BIT-BIT\s*:\s*(\w+)", re.M)
_K2 = re.compile(r"^KAPI-2 ENVANTER\s*:\s*(\w+)", re.M)


def kum_havuzu(hedef):
    """`skill/` + `paketle.sh`i yalin bir dizine kopyalar (depo kirletilmez)."""
    shutil.copytree(os.path.join(KOK, "skill"), os.path.join(hedef, "skill"))
    shutil.copy2(os.path.join(KOK, "paketle.sh"), os.path.join(hedef, "paketle.sh"))
    os.chmod(os.path.join(hedef, "paketle.sh"), 0o755)


def kos(dizin):
    """`paketle.sh`i kosar; (cikis_kodu, KAPI-1 hali, KAPI-2 hali, ham cikti)."""
    p = subprocess.run(["bash", "paketle.sh"], cwd=dizin,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    c = p.stdout.decode("utf-8", "replace")
    m1, m2 = _K1.search(c), _K2.search(c)
    return p.returncode, (m1.group(1) if m1 else None), (m2.group(1) if m2 else None), c


def m1_satir_sonu(s):
    """zip'e -l eklenir: metin dosyalarinin LF'i CRLF olur -> KAPI-1 isirmali."""
    yeni = s.replace("zip -q -r -X ", "zip -q -r -X -l ", 1)
    return yeni if yeni != s else None


def m2_referanslar_dusuyor(s):
    """referans dosyalari filtreye takilir -> KAPI-2 isirmali."""
    hedef = "-x '*/__pycache__/*'"
    yeni = s.replace(hedef, hedef + " -x 'references/*'", 1)
    return yeni if yeni != s else None


MUTANTLAR = [
    ("M-1 zip -l (satir-sonu cevrimi)", m1_satir_sonu, "KAPI-1"),
    ("M-2 references/* paketten duser", m2_referanslar_dusuyor, "KAPI-2"),
]


def main():
    if shutil.which("zip") is None:
        print("SONUC: ÖLÇÜLEMEDİ — `zip` komutu yok; bu platformda paketleme olculemez.")
        return 2
    if not os.path.isfile(os.path.join(KOK, "paketle.sh")):
        print("SONUC: ÖLÇÜLEMEDİ — paketle.sh yok.")
        return 2

    print("=== PAKET MUTANTI === kok: %s" % os.path.basename(KOK))
    gecici = tempfile.mkdtemp(prefix="paket-mutanti-")
    try:
        temiz = os.path.join(gecici, "temiz")
        os.makedirs(temiz)
        kum_havuzu(temiz)
        rc, k1, k2, ham = kos(temiz)
        print("  TEMIZ AGAC      : exit=%s · KAPI-1=%s · KAPI-2=%s" % (rc, k1, k2))
        if rc != 0 or k1 != "YESIL" or k2 != "YESIL":
            print("\n--- paketle.sh ciktisi ---\n%s" % ham.strip())
            print("\nSONUC: KIRMIZI — temiz agac kendi kapisini gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = 0
        for ad, boz, beklenen in MUTANTLAR:
            d = os.path.join(gecici, ad.split()[0])
            os.makedirs(d)
            kum_havuzu(d)
            yol = os.path.join(d, "paketle.sh")
            with open(yol, encoding="utf-8", newline="") as f:
                s = f.read()
            bozuk = boz(s)
            if bozuk is None:
                print("  %-34s KURULAMADI (mutant uygulanamadi)" % ad)
                kacan += 1
                continue
            with open(yol, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            rc, k1, k2, _ = kos(d)
            ates = [a for a, h in (("KAPI-1", k1), ("KAPI-2", k2)) if h == "KIRMIZI"]
            if rc == 0:
                print("  %-34s -> KACTI ✗  (paket exit 0 ile URETILDI)" % ad)
                kacan += 1
            elif ates == [beklenen]:
                print("  %-34s -> ISIRDI ✓  (%s · exit %s)" % (ad, beklenen, rc))
            elif beklenen in ates:
                print("  %-34s -> ISIRDI ama ORTUSTU: %s" % (ad, " + ".join(ates)))
                kacan += 1
            else:
                print("  %-34s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                      % (ad, beklenen, " + ".join(ates) or "hicbiri"))
                kacan += 1

        if kacan:
            print("\nSONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
                  % (kacan, len(MUTANTLAR)))
            return 1
        print("\nSONUC: YESIL — iki kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
              % (len(MUTANTLAR), len(MUTANTLAR)))
        return 0
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

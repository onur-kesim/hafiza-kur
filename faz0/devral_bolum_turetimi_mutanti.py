#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — DEVIR BOLUM TURETIMI MUTANTI (KALEM 1, besli-paket/IS_EMRI_DEVRAL.md).

NEDEN VAR (olculdu 6 Eyl 2026, Momentum kopyasinda, diske DOKUNULMADI)
  `SKILL.md` §2 der ki: "`devral` yapilandirmayi diskteki GERCEKTEN turetir."
  OLCULDU — `rc["zorunlu_bolumler"]` diskten (canlidaki mevcut `## ` basliklarindan)
  turetiliyordu AMA canli DOSYAYA eksik bolum yazan dongu hala sabit
  `VARSAYILAN_RC["zorunlu_bolumler"]`i kullaniyordu. Sonuc: Momentum'un KENDI
  basliklari (`## Kalici dersler ...`, `## DILIM 3 — ISBIRLIGI`, ...) tasiyan
  bir `DURUM.md`ye devral kosulunca, motorun SABIT VARSAYILANININ YEDI bolumu
  (ARSIV DIZINI DAHIL) BOS ICERIK olarak yazildi ve dosya GERCEKTEN 8186 ->
  8537 bayt oldu (bu aracin kurdugu senaryoyla dogrulandi). Carpici kanit:
  hafiza-kur'un KENDI `DURUM.md`si de o bolumlerin HICBIRINE sahip degil —
  arac, kendi belgesinde kullanmadigi bir sablonu devraldigi projeye dayatiyordu.

NE OLCER
  KAPI-A (POZITIF KONTROL) — kendi basliklari olan bir canliya `devral`:
      (a) o basliklar `.hafizarc > zorunlu_bolumler`e GECER,
      (b) motorun 6 SABIT varsayilan bolumunden HICBIRI BOS ICERIK olarak
          canli dosyaya EKLENMEZ — (c) `## ARSIV DIZINI` de bu kurala TABIDIR:
          basliklar ZATEN VARSA o da force EKLENMEZ ("diskteki gercek,
          varsayilana yeglenir" ilkesi (a) burada da gecerlidir; GERCEK
          Momentum olcumu bunu DOGRULAR — dosya YALNIZ cipa satiri kadar buyur),
      dosya SADECE `> Son guncelleme:` cipa satiri kadar BUYUR.
  KAPI-B (BOS CANLI KORUNUR) — canlida HIC '## ' basligi yoksa (d): eski
      davranis BIREBIR korunur — VARSAYILAN_RC'nin 7 bolumu de eklenir; bu
      kolda `## ARSIV DIZINI`nin (motorun URETTIGI blok) gerekcesi (c) rapor
      satirinda AYRICA gorunur.
  KAPI-C (H3 ANLAMLI KALIYOR) — KAPI-A'nin turettigi bir bolum SONRADAN
      SILINIRSE `kapi` H3 kirmizi yakar: turetim kapiyi silahsizlandirmiyor.

NE OLCMEZ
  `tavan_kb` turetimi (KAPSAM DISI, IS_EMRI_DEVRAL.md — Onur'a birakildi).
  `arsiv_turleri`/`kural_evi_bolumleri` turetimi (zaten dogru, bu aracin konusu
  degil — olculdugu yer BASKA).

CIKIS KODU  0 uc kapi da temiz VE mutant ISIRDI · 1 kapi kirmizi / mutant KACTI
            2 OLCULEMEDI (motor okunamadi, senaryo kurulamadi)
"""
import io
import json
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
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

KENDI_BASLIKLAR = ["## GUNCEL ILERLEME", "## BILINEN SINIRLAR"]
SABIT_6 = ["## GUNCEL DURUM", "## SONRAKI ADIM", "## ACIK KARARLAR",
           "## SABIT CERCEVE", "## KIRMIZI CIZGILER", "## KARAR GUNLUGU"]

S_A_CANLI = ("# Proje Y\n"
             "\n"
             "## GUNCEL ILERLEME\n"
             "Birinci bolum icerigi — kullanici yazdi.\n"
             "\n"
             "## BILINEN SINIRLAR\n"
             "Ikinci bolum icerigi — kullanici yazdi.\n")

# KAPI-B: hic '## ' basligi YOK — duz nesir, taze/eski proje hali.
S_B_CANLI = ("Bu dosya sadece duz metin tutuyor.\n"
             "Hic markdown basligi yok.\n")


def kur_proje(taban, dosyalar):
    kok = tempfile.mkdtemp(prefix="devral_bolum_", dir=taban)
    for rel, icerik in dosyalar.items():
        p = os.path.join(kok, *rel.split("/"))
        d = os.path.dirname(p)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with io.open(p, "w", encoding="utf-8", newline="") as f:
            f.write(icerik)
    return kok


def kos(motor, kok, komut, *ek):
    p = subprocess.Popen([sys.executable, motor, komut, "--kok=" + kok] + list(ek),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cikti = p.communicate()[0].decode("utf-8", "replace")
    return p.returncode, cikti


def _rc_oku(kok):
    p = os.path.join(kok, ".hafizarc")
    if not os.path.isfile(p):
        return None
    try:
        return json.loads(io.open(p, encoding="utf-8").read())
    except Exception:                                  # noqa: BLE001
        return None


# ------------------------------------------------------------------- KAPI-A
def kapi_a(motor, taban):
    """POZITIF KONTROL: kendi basliklari olan canliya devral -> basliklar
    RC'ye gecer VE bos icerik bolumu EKLENMEZ — '## ARSIV DIZINI' DAHIL
    (Momentum'da GERCEKTEN olculdu: basliklar varsa motor HICBIR SEY force
    eklemez; ekleseydi 'diskteki gercek, varsayilana yeglenir' ilkesi (a)
    ARSIV DIZINI'nda bile ihlal edilirdi). Dosya SADECE '> Son guncelleme:'
    cipa satiri kadar buyumelidir."""
    b = []
    kok = kur_proje(taban, {"DURUM.md": S_A_CANLI, "CLAUDE.md": "# kurallar\n"})
    onceki_bayt = len(S_A_CANLI.encode("utf-8"))
    kod, cikti = kos(motor, kok, "devral", "--esle", "canli=DURUM.md")
    if kod != 0:
        b.append("devral cikis %d (0 bekleniyordu): %s"
                 % (kod, cikti.strip().split("\n")[-1][:160]))
        return b, kok
    rc = _rc_oku(kok)
    if rc is None:
        b.append(".hafizarc yazilmadi/okunamadi")
        return b, kok
    zb = rc.get("zorunlu_bolumler") or []
    for h in KENDI_BASLIKLAR:
        if h not in zb:
            b.append("(a) .hafizarc.zorunlu_bolumler KENDI basligi ICERMIYOR: %s" % h)
    for h in SABIT_6:
        if h in zb:
            b.append("(a) .hafizarc.zorunlu_bolumler SABIT VARSAYILANI tasiyor "
                     "(diskten turetilmedi): %s" % h)
    canli = io.open(os.path.join(kok, "DURUM.md"), encoding="utf-8", newline="").read()
    for h in SABIT_6:
        if h in canli:
            b.append("(b) canli dosyaya BOS ICERIK bolumu EKLENDI: %s" % h)
    if "ARSIV DIZINI" in canli.upper():
        b.append("(c) '## ARSIV DIZINI' basliklar VARKEN de force EKLENDI — "
                 "(a) 'diskteki gercek ustundur' ilkesi burada da gecerli olmali")
    yeni_bayt = len(io.open(os.path.join(kok, "DURUM.md"), "rb").read())
    fark = yeni_bayt - onceki_bayt
    cipa_satiri = len(("> Son guncelleme: %s\n" % "2026-09-06").encode("utf-8"))
    if fark > cipa_satiri + 5:          # kucuk tolerans (satir sonu/tarih uzunlugu)
        b.append("dosya cipa satirindan COK DAHA FAZLA buyudu: +%d bayt "
                 "(Momentum regresyonu: 'yalniz cipa satiri kadar' beklenir)" % fark)
    return b, kok


# ------------------------------------------------------------------- KAPI-B
def kapi_b(motor, taban):
    """(d) canlida hic '## ' basligi yoksa eski davranis BIREBIR korunur:
    VARSAYILAN_RC'nin 7 bolumu de eklenir (taze/bos proje hali degismez)."""
    b = []
    kok = kur_proje(taban, {"DURUM.md": S_B_CANLI, "CLAUDE.md": "# kurallar\n"})
    kod, cikti = kos(motor, kok, "devral", "--esle", "canli=DURUM.md")
    if kod != 0:
        b.append("devral cikis %d (0 bekleniyordu): %s"
                 % (kod, cikti.strip().split("\n")[-1][:160]))
        return b
    rc = _rc_oku(kok)
    if rc is None:
        b.append(".hafizarc yazilmadi/okunamadi")
        return b
    zb = set(rc.get("zorunlu_bolumler") or [])
    VARSAYILAN_7 = ["## GUNCEL DURUM", "## SONRAKI ADIM", "## ACIK KARARLAR",
                    "## SABIT CERCEVE", "## KIRMIZI CIZGILER", "## KARAR GUNLUGU",
                    "## ARSIV DIZINI"]
    for h in VARSAYILAN_7:
        if h not in zb:
            b.append("basliksiz canlida VARSAYILAN bolum EKSIK (regresyon): %s" % h)
    canli = io.open(os.path.join(kok, "DURUM.md"), encoding="utf-8", newline="").read()
    for h in VARSAYILAN_7:
        if h not in canli:
            b.append("basliksiz canlida VARSAYILAN bolum DOSYAYA yazilmadi (regresyon): %s" % h)
    # (c) bu koldaki '## ARSIV DIZINI' motorun URETTIGI bloktur; gerekcesi
    # rapor satirinda GORUNUR olmalidir (diger 6 sabit bolumden AYRI vurgu).
    if "arsiv dizini" not in cikti.lower():
        b.append("(c) basliksiz koldaki '## ARSIV DIZINI' eklemesinin GEREKCESI "
                 "rapor satirinda GORUNMUYOR")
    return b


# ------------------------------------------------------------------- KAPI-C
def kapi_c(motor, taban):
    """H3 ANLAMLI KALIYOR: KAPI-A'nin turettigi bir bolum sonradan SILINIRSE
    `kapi` H3 kirmizi yakar — turetim kapiyi silahsizlandirmiyor."""
    b = []
    bulgu_a, kok = kapi_a(motor, taban)
    if bulgu_a:
        b.append("H3 kolu KAPI-A uzerine kuruluyor ama KAPI-A zaten kirmizi — atlanamaz")
        return b
    canli_p = os.path.join(kok, "DURUM.md")
    metin = io.open(canli_p, encoding="utf-8", newline="").read()
    L = [s for s in metin.split("\n") if s.rstrip() != "## BILINEN SINIRLAR"]
    with io.open(canli_p, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L))
    kod, cikti = kos(motor, kok, "kapi")
    if kod == 0:
        b.append("turetilen bolum SILINDIKTEN SONRA `kapi` hala YESIL — H3 silahsizlandi")
    elif "[H3]" not in cikti or "BILINEN SINIRLAR" not in cikti:
        b.append("`kapi` kirmizi ama [H3] 'BILINEN SINIRLAR' bulgusu GORUNMUYOR: %s"
                 % cikti.strip().split("\n")[-1][:160])
    return b


def hukum(motor, taban):
    a, _ = kapi_a(motor, taban)
    return a, kapi_b(motor, taban), kapi_c(motor, taban)


# --------------------------------------------------------------- MUTANT
# MUTANT: KALEM 1'in duzeltmesi sokulur -> eksik-bolum dongusu yeniden KOSULSUZ
# VARSAYILAN_RC'yi kullanir. KAPI-A'nin (b) ayagi (bos icerik bolumu eklenmedi)
# ISIRMALIDIR: bes SABIT bolum yeniden BOS ICERIK olarak canliya yazilir.
ANKOR = ('    _bolum_adaylari = [] if basliklar else list(VARSAYILAN_RC["zorunlu_bolumler"])\n'
         '    _eklenen_bolum = []\n'
         '    for _b in _bolum_adaylari:\n')
YENI = ('    _eklenen_bolum = []\n'
        '    for _b in VARSAYILAN_RC["zorunlu_bolumler"]:\n')


def sokulmus_motor(kaynak, hedef_dizin):
    n = kaynak.count(ANKOR)
    if n != 1:
        return None, "capa %d yerde gecti (1 olmali): %r" % (n, ANKOR[:60])
    metin = kaynak.replace(ANKOR, YENI, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(hedef_dizin, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p, None


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    print(CIZGI)
    print("DEVIR BOLUM TURETIMI MUTANTI (KALEM 1) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="devral_bolum_turetimi_")
    try:
        a, bb, c = hukum(yol, taban)
        for ad, bulgu, ne in (("KAPI-A POZITIF KONTROL", a,
                                "basliklar turetildi + bos bolum yok + ARSIV DIZINI istisnasi"),
                              ("KAPI-B BOS CANLI      ", bb,
                                "basliksiz canlida varsayilan davranis BIREBIR"),
                              ("KAPI-C H3 ANLAMLI     ", c,
                                "turetilen bolum silinince H3 kirmizi yaniyor")):
            print("  %s: %s" % (ad, "YESIL (%s)" % ne if not bulgu
                                else "KIRMIZI — %d bulgu" % len(bulgu)))
            for x in bulgu:
                print("      ! %s" % x)
        if a or bb or c:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
        sab, hata = sokulmus_motor(s, mdir)
        if sab is None:
            print("  M-1 turetim sokulur              OLCULEMEDI: %s" % hata)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        ma, _ = kapi_a(sab, taban)
        if ma:
            print("  M-1 turetim sokulur              -> ISIRDI ✓  (KAPI-A: %s)"
                  % "; ".join(ma[:2]))
            print(CIZGI)
            print("SONUC: YESIL — kapilar temiz, mutant AYRI eksende ISIRDI.")
            return 0
        print("  M-1 turetim sokulur              -> KACTI ✗  (duzeltmeden onceki davranis "
              "geri geldiginde hicbir kapi bunu YAKALAMIYOR)")
        print(CIZGI)
        print("SONUC: KAPI KOR — mutant beklendigi gibi olculmedi.")
        return 1
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

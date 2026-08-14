#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — README KANIT BLOGU KAPISI (BITTI maddesi 5).

NEDEN VAR (olculdu 14 Agu 2026)
  Madde 5: "25 Agu yazisinin okuru, depoya gelip README ile sistemi kendi basina
  deneyebilir." Okurun yapacagi sey README'nin "Kanitini kendin kos" blogudur ve
  o blok SAYISAL BEYANLAR tasiyor:
      python3 hafiza.py isir --kok=deneme   # taze projede: 34/34 + 2 SINANMADI, exit 2
      python3 hafiza.py isir --kok=deneme   # derle sonrasi: 36/36, exit 0
  Bu beyanlari HICBIR kapi olcmuyordu. Ustelik ikincisi (`derle` sonrasi isir=0)
  `DURUM.md`in "olculmuyor" diye yazdigi bosluğun ta kendisiydi: README onu IDDIA
  ediyor, hicbir sey dogrulamiyordu. Bir okur yanlis sayiyla karsilassa projenin
  TEK vaadi (olculebilirlik) onun gozunde daha ilk dakikada duserdi.

  Ayni gun iki kez isiran sinif: "belge de bir arayuzdur ve yalan soyleyebilir"
  (`paketle.sh` basligi · `SKILL.md` kurulum akisi). Bu, ucuncu kapisidir.

NE OLCER — UC AYRI EKSEN
  KAPI-1 BEYAN     : blok AYIKLANABILIR beyan tasiyor mu? Her `python3 hafiza.py`
                     satirinin yorumundan `exit N` cikarilabiliyor mu, ve en az
                     iki `isir` beyani var mi? (README olculebilir olmaktan
                     cikarsa — yorumlar silinirse — kapi KIRMIZI yanar.)
  KAPI-2 GERCEK    : blok KOSULUR ve her beyan GERCEKLE karsilastirilir. Beklenen
                     degerler BLOKTAN OKUNUR, araca YAZILMAZ — "sayi yazilmaz,
                     URETILIR" dersi. README'deki sayi degisirse kapi onu izler;
                     README yanlis sayi yazarsa KIRMIZI yanar.
  KAPI-3 SOZLESME  : README'nin "Cikis kodlari" paragrafindaki `isir` kod KUMESI,
                     motorun kendi bastigi `CIKIS KODLARI:` satiriyla ayni mi.

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. `t_y3.py` / `t_y42.py` blokta gecer ama BURADA kosulmaz. 🔴 DIKKAT — ilk
     surum burada "`kanit` isi onlari zaten continue-on-error'SIZ kosuyor" YAZDI;
     OLCULDU ve YANLISTI: `kanit` isinin HER IKI adimi da `continue-on-error: true`
     tasiyor, yani kirmizilari YUTULUYOR. Dolayisiyla README'nin "20 senaryo" ve
     "58 senaryo" beyanlari SU AN HICBIR KAPIYLA olculmuyor. Bu bir SINIRDIR,
     hukum degil; atlandiklari CIKTIDA yazilir — sessiz atlama YOK.
     (Karar bekliyor: bu araca alinsinlar mi, yoksa `kanit`teki bilincli
     `continue-on-error` mi kaldirilsin.)
  2. Blokta TANIMADIGI bir satir gorurse ARAC DURUR (OLCULEMEDI). README'ye yeni
     bir adim eklenip kapinin onu sessizce yok saymasi, tam da bu araciin
     onlemek icin var oldugu sey.
  3. Blok depo kokunde degil, `skill/scripts`in GECICI bir kopyasinda kosar
     (depo kirletilmesin). Komutlar ve goreli yollar birebir aynidir.
  4. README'nin ANLATIMINI olcmez (sira, dil, aciklik) — yalnizca olculebilir
     beyanlarini.

CIKIS KODLARI
  0  uc kapi da temiz VE 4/4 mutant AYRI eksende ISIRDI
  1  bir kapi kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  olculemedi (README yok, blok yok, taninmayan satir, git yok)
"""
import os
import re
import shlex
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
README = os.path.join(KOK, "README.md")

_BASLIK = re.compile(r"^#+\s*Kan[iı]t[iı]n?[iı]? kendin ko[sş]\s*$", re.M | re.I)
_EXIT = re.compile(r"exit\s+(\d+)")
_ORAN = re.compile(r"(\d+)\s*/\s*(\d+)")
_SINANMADI = re.compile(r"(\d+)\s+SINANMADI")
# motorun kendi hukum satiri
_SONUC = re.compile(r"(\d+)/(\d+) kosulan mutant ISIRIYOR · (\d+) SINANMADI")
_MOTOR_KOD = re.compile(r"CIKIS KODLARI:\s*(.+)")
_KOD = re.compile(r"(\d+)")
# README'nin "Cikis kodlari" paragrafi
_README_ISIR = re.compile(r"`isir`\s*:(.+?)\.", re.S)


def blok_bul(metin):
    """"Kanitini kendin kos" basligindan sonraki ILK cit blogu."""
    m = _BASLIK.search(metin)
    if not m:
        return None
    kalan = metin[m.end():]
    i = kalan.find("```")
    if i < 0:
        return None
    j = kalan.find("```", i + 3)
    if j < 0:
        return None
    govde = kalan[i + 3:j]
    return govde.split("\n", 1)[1] if govde.startswith("bash") else govde


def satirlari_coz(blok):
    """Blogun her satirini (tur, komut, beyan) olarak cozer.

    Taninmayan satir -> ('BILINMEYEN', ham, None). Cagiran yer DURUR."""
    out = []
    for ham in blok.split("\n"):
        s = ham.strip()
        if not s:
            continue
        komut, _, yorum = s.partition("#")
        komut = komut.strip()
        beyan = None
        if yorum.strip():
            e = _EXIT.search(yorum)
            o = _ORAN.search(yorum)
            sn = _SINANMADI.search(yorum)
            beyan = {"ham": yorum.strip(),
                     "exit": int(e.group(1)) if e else None,
                     "oran": (int(o.group(1)), int(o.group(2))) if o else None,
                     "sinanmadi": int(sn.group(1)) if sn else None}
        if komut.startswith("cd "):
            out.append(("CD", komut, beyan))
        elif komut.startswith("mkdir "):
            out.append(("MKDIR", komut, beyan))
        elif "git init" in komut:
            out.append(("GIT", komut, beyan))
        elif re.match(r"python3?\s+hafiza\.py\s", komut):
            out.append(("MOTOR", komut, beyan))
        elif re.match(r"python3?\s+t_y\d+\.py", komut):
            out.append(("KANIT", komut, beyan))
        else:
            out.append(("BILINMEYEN", komut, beyan))
    return out


# ------------------------------------------------------------------- KAPI-1
def kapi1_beyan(adimlar):
    """Blok AYIKLANABILIR beyan tasiyor mu?"""
    bulgu = []
    motor = [(k, b) for t, k, b in adimlar if t == "MOTOR"]
    if not motor:
        bulgu.append("blokta hic `hafiza.py` komutu YOK")
    isirlar = [(k, b) for k, b in motor if " isir " in k + " "]
    beyanli = [b for k, b in isirlar if b and b.get("exit") is not None]
    if len(beyanli) < 2:
        bulgu.append("`isir` icin AYIKLANABILIR `exit N` beyani %d < 2 — README olculebilir "
                     "olmaktan cikti" % len(beyanli))
    for k, b in isirlar:
        if b and b.get("exit") is not None and b.get("oran") is None:
            bulgu.append("beyanda `exit` var ama mutant orani (N/M) YOK: %s" % b["ham"])
    return bulgu


# ------------------------------------------------------------------- KAPI-3
def kapi3_sozlesme(metin, isir_ciktisi):
    """README'nin ilan ettigi `isir` kod kumesi motorunkiyle ayni mi?"""
    m = _README_ISIR.search(metin)
    if not m:
        return ["README'de `isir` cikis kodu paragrafi bulunamadi"]
    belge = set(int(x) for x in _KOD.findall(m.group(1)))
    mm = _MOTOR_KOD.search(isir_ciktisi)
    if not mm:
        return ["motor `CIKIS KODLARI:` satirini basmadi — karsilastirilamaz"]
    gercek = set(int(x) for x in _KOD.findall(mm.group(1)))
    if belge != gercek:
        return ["README %s diyor, motor %s basiyor (fark: %s)"
                % (sorted(belge), sorted(gercek), sorted(belge ^ gercek))]
    return []


# --------------------------------------------------------------- KAPI-2 (canli)
def kapi2_gercek(adimlar, kaynak_scripts):
    """Blogu KOSAR ve her beyani gercekle karsilastirir. (bulgu, atlanan, son_isir)"""
    bulgu, atlanan, son = [], [], ""
    gecici = tempfile.mkdtemp(prefix="readme-kapisi-")
    try:
        calisma = os.path.join(gecici, "scripts")
        shutil.copytree(kaynak_scripts, calisma,
                        ignore=shutil.ignore_patterns("__pycache__", "deneme"))
        cwd = calisma
        for tur, komut, beyan in adimlar:
            if tur == "CD":
                continue                       # blok zaten `skill/scripts`e giriyor
            if tur == "MKDIR":
                os.makedirs(os.path.join(cwd, komut.split()[-1]), exist_ok=True)
                continue
            if tur == "GIT":
                hedef = os.path.join(cwd, komut.split()[-1])
                os.makedirs(hedef, exist_ok=True)
                p = subprocess.run(["git", "init", "-q", hedef],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if p.returncode != 0:
                    bulgu.append("`git init` basarisiz: %s"
                                 % p.stdout.decode("utf-8", "replace")[:120])
                continue
            if tur == "KANIT":
                atlanan.append(komut)          # `kanit` isi zaten kosuyor
                continue
            # shlex SART: `--metin="ilk not"` ve `--ad "Deneme"` duz split ile bozulur
            # (olculdu: bozuk arguman -> her komut exit 2, arac README'yi suclardi).
            arg = shlex.split(komut)[2:]       # "python3 hafiza.py" sonrasi
            p = subprocess.run([sys.executable, "hafiza.py"] + arg, cwd=cwd,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            c = p.stdout.decode("utf-8", "replace")
            if " isir " in komut + " ":
                son = c
            if not beyan:
                if p.returncode != 0:
                    bulgu.append("`%s` beyansiz ama exit %d dondu" % (komut, p.returncode))
                continue
            if beyan["exit"] is not None and p.returncode != beyan["exit"]:
                bulgu.append("`%s`: README `exit %d` diyor, GERCEK exit %d"
                             % (komut, beyan["exit"], p.returncode))
            m = _SONUC.search(c)
            if beyan["oran"] is not None:
                if not m:
                    bulgu.append("`%s`: README %d/%d diyor ama motor SONUC satirini basmadi"
                                 % (komut, beyan["oran"][0], beyan["oran"][1]))
                elif (int(m.group(1)), int(m.group(2))) != beyan["oran"]:
                    bulgu.append("`%s`: README %d/%d diyor, GERCEK %s/%s"
                                 % (komut, beyan["oran"][0], beyan["oran"][1],
                                    m.group(1), m.group(2)))
            if beyan["sinanmadi"] is not None and m and int(m.group(3)) != beyan["sinanmadi"]:
                bulgu.append("`%s`: README %d SINANMADI diyor, GERCEK %s"
                             % (komut, beyan["sinanmadi"], m.group(3)))
        return bulgu, atlanan, son
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


# --------------------------------------------------------------- MUTANTLAR
def m1_beyan_silinir(s):
    """`exit 2` beyani yorumdan silinir -> KAPI-1 isirmali (KAPI-2 o beyani olcmez)."""
    yeni = s.replace("# taze projede: 34/34 + 2 SINANMADI, exit 2",
                     "# taze projede", 1)
    return yeni if yeni != s else None


def m2_oran_bozulur(s):
    """README yanlis mutant orani yazar -> KAPI-2 isirmali."""
    yeni = s.replace("34/34 + 2 SINANMADI", "33/33 + 2 SINANMADI", 1)
    return yeni if yeni != s else None


def m3_cikis_kodu_bozulur(s):
    """README yanlis cikis kodu yazar -> KAPI-2 isirmali (oranlar dogru kalir)."""
    yeni = s.replace("# derle sonrası: 36/36, exit 0", "# derle sonrası: 36/36, exit 3", 1)
    return yeni if yeni != s else None


def m4_sozlesme_eksilir(s):
    """README `isir` sozlesmesinden bir kod duser -> KAPI-3 isirmali."""
    yeni = s.replace("`2` ölçülemeyen mutant · `4` temiz sürüm zaten FAIL",
                     "`2` ölçülemeyen mutant", 1)
    return yeni if yeni != s else None


MUTANTLAR = [
    ("M-1 beyan yorumdan silindi", m1_beyan_silinir, "KAPI-1"),
    ("M-2 README yanlis oran yaziyor", m2_oran_bozulur, "KAPI-2"),
    ("M-3 README yanlis cikis kodu", m3_cikis_kodu_bozulur, "KAPI-2"),
    ("M-4 sozlesmeden kod dustu", m4_sozlesme_eksilir, "KAPI-3"),
]


def hukum(metin, kaynak_scripts):
    """(k1, k2, k3, atlanan) — blok cozulemezse None doner (OLCULEMEDI)."""
    blok = blok_bul(metin)
    if blok is None:
        return None
    adimlar = satirlari_coz(blok)
    bilinmeyen = [k for t, k, _ in adimlar if t == "BILINMEYEN"]
    if bilinmeyen:
        return ("BILINMEYEN", bilinmeyen)
    k1 = kapi1_beyan(adimlar)
    k2, atlanan, son = kapi2_gercek(adimlar, kaynak_scripts)
    k3 = kapi3_sozlesme(metin, son)
    return (k1, k2, k3, atlanan)


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else README
    kaynak = os.path.join(KOK, "skill", "scripts")
    if not os.path.isfile(yol):
        print("SONUC: ÖLÇÜLEMEDİ — README yok: %s" % yol)
        return 2
    if shutil.which("git") is None:
        print("SONUC: ÖLÇÜLEMEDİ — `git` yok; blok `git init` istiyor.")
        return 2
    with open(yol, encoding="utf-8", newline="") as f:
        metin = f.read()

    print("=== README KANIT BLOGU KAPISI === %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    h = hukum(metin, kaynak)
    if h is None:
        print("SONUC: ÖLÇÜLEMEDİ — 'Kanitini kendin kos' blogu bulunamadi.")
        return 2
    if h[0] == "BILINMEYEN":
        print("  BLOK            : TANIMADIGIM SATIR VAR — sessiz atlama YOK")
        for k in h[1]:
            print("      ? %s" % k)
        print("\nSONUC: ÖLÇÜLEMEDİ — blok cozulemedi; araca yeni satir turu ogretilmeli.")
        return 2
    k1, k2, k3, atlanan = h
    print("  KAPI-1 BEYAN    : %s" % ("YESIL (beyanlar ayiklanabiliyor)" if not k1
                                      else "KIRMIZI — %d bulgu" % len(k1)))
    for x in k1:
        print("      ! %s" % x)
    print("  KAPI-2 GERCEK   : %s" % ("YESIL (README'nin her sayisi GERCEKLE tuttu)" if not k2
                                      else "KIRMIZI — %d bulgu" % len(k2)))
    for x in k2:
        print("      ! %s" % x)
    print("  KAPI-3 SOZLESME : %s" % ("YESIL (README ile motor ayni kod kumesi)" if not k3
                                      else "KIRMIZI — %d bulgu" % len(k3)))
    for x in k3:
        print("      ! %s" % x)
    for k in atlanan:
        print("  ATLANDI (sessiz DEGIL): `%s` — `kanit` isi kosuyor AMA "
              "`continue-on-error: true` ile (kirmizisi yutulur) → bu beyan OLCULMUYOR" % k)
    if k1 or k2 or k3:
        print("\nSONUC: KIRMIZI — README'nin beyani gercekle TUTMUYOR.")
        return 1

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    for ad, boz, beklenen in MUTANTLAR:
        bozuk = boz(metin)
        if bozuk is None:
            print("  %-34s KURULAMADI (desen README'de yok)" % ad)
            kacan += 1
            continue
        b = hukum(bozuk, kaynak)
        if b is None or b[0] == "BILINMEYEN":
            print("  %-34s -> BLOK COZULEMEDI (mutant kapiyi degil ayirici yi bozdu)" % ad)
            kacan += 1
            continue
        ates = [a for a, v in (("KAPI-1", b[0]), ("KAPI-2", b[1]), ("KAPI-3", b[2])) if v]
        if ates == [beklenen]:
            print("  %-34s -> ISIRDI ✓  (%s)" % (ad, beklenen))
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
    print("\nSONUC: YESIL — uc kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACILIS GOCU MUTANTI — `derle`, ESKI motorla kurulmus projenin `acilis-protokolu` blogundaki duz `git status` satirini
yeni lafza goc ettiriyor mu, ve YALNIZ onu mu?
(besli-paket/IS_EMRI_ACILIS_SATIR_GOCU.md, Onur kilidi sik A, 23 Eki 2026)

NEDEN VAR (OLCULDU, RAPOR_MOTOR_GITSTATUS_23EKIM KALEM 1)
  Sablon duzeltmesi (`SAB_CANLI`) yalniz YENI projeleri korudu: eski motorla kurulmus projenin canli dosyasindaki
  `3. `git status` temiz mi bak.` satiri (baglı klasorde kalici `.git/index.lock` mayini) `kur`/`derle`/`devral` sonrasi KALIYORDU.
  `derle` artik sahip="hafiza-kur" `acilis-protokolu` blogunda YALNIZ birebir bu satiri `3. `git --no-optional-locks status --porcelain`
  temiz mi bak.` yapar (muhasebe: mevcut motor-blok yolu — eski blok arsive, `guncel` damgasi, tek NOT satiri). Baska satira dokunmaz.

FIXTURE GERCEK ESKI KURULUMDAN GELIR: `git show d05d91c3:skill/scripts/hafiza.py` (SHA256 135eb72c0e16…) ile `kur`. Obje yoksa (sig klon)
  ya da SHA tutmazsa OLCULEMEDI (exit 2) — elle yazilmis canli dosya TEK BASINA YETMEZ, sessiz yesil YOK.

VAKALAR (hepsi ayri proje; kapi motoru = sinanan motor; `kur` HER ZAMAN eski motorla)
  A GOC          eski satir -> yeni; blogun KALAN satirlari ayni; eski blok arsive 1 kez; TEK NOT satiri; `kapi` exit'i taze kurulumla AYNI
  B IDEMPOTENT   ikinci `derle` (yeni parca ile) acilis blogunu BYTE degistirmez ve arsive ikinci kez yazmaz
  C KULLANICI    kullanicinin degistirdigi satir (`... git status` ve `git log` bak.`) ayni kalir, arsive yazilmaz
  D EK SATIR     kullanicinin bloga ekledigi satir korunur, yalniz 3. satir degisir
  E SAHIP        sahip="hafiza-kur" olmayan blokta satir DEGISMEZ
  F KALICI KURAL kalici-kural isaretli (ASLA) blok DEGISMEZ + ATLANDI notu
  G BLOK DISI    eski satirin BLOK DISINDAKI kopyasina dokunulmaz
MUTANTLAR (M-G1..M-G6; kirilan vaka kumesi beklenene TAM ESIT olmali)
  M-G1 goc kapali {A,D,F: goc / ATLANDI notu beklenen vakalar} · M-G2 blok esitleme (govde sablondan) {D} · M-G3 sahiplik suzgeci yok {E}
  M-G4 birebir degil icerir {C,G: ikisi de blokta kullanici satiri tasir}
  M-G5 idempotent degil (ayni-icerik kisa devresi kalkar) {B} · M-G6 KALICI KURAL suzgeci yok {F}

CIKIS KODLARI  0 saglam YESIL ve 6 mutant ISIRDI · 1 saglam kirmizi / mutant KACTI / yanlis vaka · 2 OLCULEMEDI · 3 ARAC KUSURU
Betik kendi gecici dizinini SILMEZ (taze mkdtemp).
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 84
ESKI_SHA = "d05d91c3"
ESKI_SHA256 = "135eb72c0e16a5cfa85dd7de3d4beab70d122e038a1c812b7eeac3360a1c32bd"
ESKI = "3. `git status` temiz mi bak."
YENI = "3. `git --no-optional-locks status --porcelain` temiz mi bak."
KULLANICI = "3. `git status` ve `git log` bak."
EK = "8. Benim notum burada."
KURAL = "9. ASLA push etme."
BLOK_BAS = re.compile(r'^<!-- blok konu="acilis-protokolu"[^>]*-->$')
VAKALAR = ["A", "B", "C", "D", "E", "F", "G"]


class AracKusuru(Exception):
    pass


class Kurulamadi(Exception):
    pass


def _git(kok, *a, ham=False):
    r = subprocess.run(["git", "-C", kok] + list(a), capture_output=True,
                       env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull))
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (a[0], r.stderr.decode("utf-8", "replace").strip()[:140]))
    return r.stdout if ham else r.stdout.decode("utf-8", "replace")


def eski_motor_yaz(hedef):
    try:
        b = _git(KOK, "show", "%s:skill/scripts/hafiza.py" % ESKI_SHA, ham=True)
    except Kurulamadi as e:
        raise Kurulamadi("eski motor okunamadi (sig klon? `fetch-depth: 0` gerekir): %s" % e)
    if hashlib.sha256(b).hexdigest() != ESKI_SHA256:
        raise Kurulamadi("eski motor SHA256 tutmuyor (%s != %s)" % (hashlib.sha256(b).hexdigest()[:12], ESKI_SHA256[:12]))
    p = os.path.join(hedef, "eski_hafiza.py")
    with open(p, "wb") as f:
        f.write(b)
    return p


def sabotajli_motor(hedef, degisimler):
    metin = open(MOTOR, encoding="utf-8").read()
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise AracKusuru("sabotaj hedefi %d kez gecti (1 olmali): %r" % (n, eski[:70]))
        metin = metin.replace(eski, yeni, 1)
    compile(metin, "<mutant>", "exec")
    p = os.path.join(hedef, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def kos(motor, arglar, kok):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def canli_yol(kok):
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    if not os.path.isfile(p):
        raise Kurulamadi("canli dosya yok: %s" % p)
    return p


def satirlar(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def yaz(p, L):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L))


def blok(L):
    """acilis-protokolu blogu -> (bas_idx, son_idx) | None."""
    for i, s in enumerate(L):
        if BLOK_BAS.match(s):
            for j in range(i + 1, len(L)):
                if L[j].startswith("<!-- /blok -->"):
                    return i, j
    return None


def arsiv_metni(kok):
    t = ""
    for yol, dizinler, dosyalar in os.walk(os.path.join(kok, "arsiv")):
        dizinler.sort()
        for f in sorted(dosyalar):
            if f.endswith(".md"):
                with open(os.path.join(yol, f), encoding="utf-8", errors="replace") as h:
                    t += h.read()
    return t


def emekli_sayisi(kok):
    return arsiv_metni(kok).count("konu 'acilis-protokolu' guncellendi")


def eski_kurulum(eski, taban, ad):
    """GERCEK eski motorla kurulmus proje (git init + `kur`)."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    _git(kok, "init", "-q", ".")
    rc, c = kos(eski, ["kur", "--ad", "GOC"], kok)
    if rc != 0:
        raise Kurulamadi("eski `kur` basarisiz (%s, exit %d): %s" % (ad, rc, c.strip().split("\n")[-1][:140]))
    p = canli_yol(kok)
    L = satirlar(p)
    b = blok(L)
    if not b or ESKI not in L[b[0] + 1:b[1]]:
        raise Kurulamadi("eski kurulumun acilis blogunda ESKI satir yok — fixture gecersiz")
    return kok, p


def tur(motor, kok, konu="genel-durum"):
    rc, c = kos(motor, ["not", "--konu", konu, "--tur", "durum", "--metin", "gocu olcum"], kok)
    if rc != 0:
        raise Kurulamadi("`not` basarisiz (exit %d): %s" % (rc, c.strip().split("\n")[-1][:140]))


def derle(motor, kok):
    rc, c = kos(motor, ["derle"], kok)
    if rc not in (0, 1):      # 1 = derleme YAPILDI ama sonraki kapi FAIL (ornek: ASLA'li blok H7); vaka iddialari yazilan dosyalara bakar
        raise Kurulamadi("`derle` basarisiz (exit %d): %s" % (rc, c.strip().split("\n")[-1][:140]))
    return c


def vaka(ad, motor, eski, taban):
    """-> kirilan iddialar listesi (bos = saglam)."""
    ih = []
    kok, p = eski_kurulum(eski, taban, "v_" + ad)
    L0 = satirlar(p)
    b0 = blok(L0)
    govde0 = L0[b0[0] + 1:b0[1]]
    if ad in ("C", "D", "E", "F", "G"):
        L = list(L0)
        if ad == "C":
            L[b0[0] + 1 + govde0.index(ESKI)] = KULLANICI
        elif ad == "D":
            L.insert(b0[1], EK)
        elif ad == "E":
            L[b0[0]] = L[b0[0]].replace('sahip="hafiza-kur"', 'sahip="proje"')
        elif ad == "F":
            L.insert(b0[1], KURAL)
        elif ad == "G":
            L[b0[0] + 1 + govde0.index(ESKI)] = KULLANICI                       # blok icindeki satir kullanicinin
            L += ["", "## NOT", ESKI]                                           # ESKI satir blok DISINDA
        yaz(p, L)
        L0 = satirlar(p)
        b0 = blok(L0)
        govde0 = L0[b0[0] + 1:b0[1]]
    tur(motor, kok)
    cikti = derle(motor, kok)
    L1 = satirlar(p)
    b1 = blok(L1)
    govde1 = L1[b1[0] + 1:b1[1]]
    emekli = emekli_sayisi(kok)
    if ad == "A":
        beklenen = [YENI if s == ESKI else s for s in govde0]
        if govde1 != beklenen:
            ih.append("A: blok govdesi yalniz 3. satir degismeli (beklenen %r, bulunan %r)" % (beklenen[2:3], govde1[2:3] if len(govde1) > 2 else govde1))
        if emekli != 1:
            ih.append("A: eski blok arsive TAM 1 kez yazilmali (bulunan %d)" % emekli)
        if cikti.count("'acilis-protokolu' blogu guncellendi (motor, tek satir: git status -> --no-optional-locks)") != 1:
            ih.append("A: TEK NOT satiri beklenir")
        # kapi exit: taze (yeni motorla kurulmus) proje ile AYNI islemden sonra ayni exit
        kok2 = os.path.join(taban, "v_A_taze")
        os.makedirs(kok2)
        _git(kok2, "init", "-q", ".")
        rc, c = kos(MOTOR, ["kur", "--ad", "GOC"], kok2)
        if rc != 0:
            raise Kurulamadi("taze `kur` basarisiz: %s" % c.strip().split("\n")[-1][:120])
        tur(MOTOR, kok2)
        derle(MOTOR, kok2)
        rc_ref, _ = kos(MOTOR, ["kapi"], kok2)
        rc_goc, _ = kos(motor, ["kapi"], kok)
        if rc_goc != rc_ref:
            ih.append("A: kapi exit goc sonrasi %d, taze kurulumda %d (AYNI olmali)" % (rc_goc, rc_ref))
    elif ad == "B":
        blok_once = "\n".join(L1[b1[0]:b1[1] + 1])
        emekli_once = emekli
        tur(motor, kok, konu="acik-kararlar")
        derle(motor, kok)
        L2 = satirlar(p)
        b2 = blok(L2)
        blok_sonra = "\n".join(L2[b2[0]:b2[1] + 1])
        if blok_sonra != blok_once:
            ih.append("B: ikinci derle acilis blogunu degistirdi")
        if emekli_sayisi(kok) != emekli_once:
            ih.append("B: ikinci derle arsive acilis blogunu yeniden yazdi (%d -> %d)" % (emekli_once, emekli_sayisi(kok)))
    elif ad in ("C", "E", "F"):
        if govde1 != govde0 or L1[b1[0]] != L0[b0[0]]:
            ih.append("%s: blok DEGISMEMELI" % ad)
        if emekli != 0:
            ih.append("%s: arsive acilis blogu yazilmamali (bulunan %d)" % (ad, emekli))
        if ad == "F" and "ATLANDI (konu 'acilis-protokolu' blogunda KALICI KURAL" not in cikti:
            ih.append("F: ATLANDI notu beklenir")
    elif ad == "D":
        beklenen = [YENI if s == ESKI else s for s in govde0]
        if govde1 != beklenen:
            ih.append("D: kullanicinin ekledigi satir korunmali, yalniz 3. satir degismeli")
    elif ad == "G":
        if ESKI not in L1[b1[1] + 1:]:
            ih.append("G: blok DISINDAKI eski satir degismemeli")
        if govde1 != govde0:
            ih.append("G: blok degismemeli")
    return ih


def tum_vakalar(motor, eski, taban, ek=""):
    kirilan = {}
    for ad in VAKALAR:
        kirilan[ad] = vaka(ad, motor, eski, os.path.join(taban, ek + ad))
    return kirilan


GOVDE_SABLON = ('["1. Bu dosyayı baştan sona oku. Sohbet geçmişini hafıza sayma.", "2. `hafiza.py kapi` koş. YEŞİL görmeden işe BAŞLAMA.", _ACILIS_YENI, '
                '"4. SONRAKİ ADIM\'daki ilk işten devam et.", "5. Kod/içerik yazmadan ÖNCE tasarımı işaretlenebilir şıklarla sun; kapsamı onaylat.", '
                '"6. Her büyük adım sonunda `hafiza.py not` ile fragman yaz (checkpoint).", "7. Oturum kapanırken: `hafiza.py derle` → `hafiza.py kapi` → devir notu."]')

MUTANTLAR = [
    ("M-G1 GOC KAPALI", "eski projede satir kalir (D: ek satirli blokta da goc beklenir; F: ATLANDI notu beklenir -> esitle hic cagrilmaz)", {"A", "D", "F"},
     [("    L = _acilis_satir_goc(y, rc, L, ertele, eklenen)   # eski kurulum gocu: tek satir (sik A)\n", "    pass   # MUTANT\n")]),
    ("M-G2 BLOK ESITLEME", "govde sablondan: kullanicinin bloga ekledigi satir silinir", {"D"},
     [("    govde = [_ACILIS_YENI if s == _ACILIS_ESKI else s for s in mevcut]\n", "    govde = %s   # MUTANT\n" % GOVDE_SABLON)]),
    ("M-G3 SAHIPLIK SUZGECI YOK", "sahip=hafiza-kur olmayan blokta satir degisir", {"E"},
     [("    if bul == \"BOZUK\" or (bul and bul[2].get(\"sahip\") != \"hafiza-kur\"):\n        return L\n", "    if bul == \"BOZUK\":   # MUTANT\n        return L\n")]),
    ("M-G4 BIREBIR DEGIL ICERIR", "`git status` iceren her satir degisir (kullanicinin satiri dahil; G de blok icinde kullanici satiri tasir)", {"C", "G"},
     [("    eskili = _ACILIS_ESKI in mevcut\n", "    eskili = any(\"git status\" in x for x in mevcut)   # MUTANT\n"),
      ("    govde = [_ACILIS_YENI if s == _ACILIS_ESKI else s for s in mevcut]\n", "    govde = [_ACILIS_YENI if \"git status\" in s else s for s in mevcut]   # MUTANT\n")]),
    ("M-G5 IDEMPOTENT DEGIL", "ayni-icerik kisa devresi kalkar: ikinci derle arsive yazar", {"B"},
     [("    if bul and govde is not None and _motor_blok_ayni(L, bul, govde):\n        return L\n", "    pass   # MUTANT\n")]),
    ("M-G6 KALICI KURAL SUZGECI YOK", "isaretli blok degisir", {"F"},
     [("    if bul and _motor_blok_kuralli(rc, L, bul):\n        print(\"ATLANDI", "    if False:   # MUTANT\n        print(\"ATLANDI")]),
]


def main():
    taban = tempfile.mkdtemp(prefix="agm_")
    print(CIZGI)
    print("ACILIS GOCU MUTANTI — derle eski kurulumda YALNIZ birebir `git status` satirini goc ettirir · platform: %s" % sys.platform)
    print(CIZGI)
    try:
        eski = eski_motor_yaz(taban)
        saglam = tum_vakalar(MOTOR, eski, taban, "s_")
    except Kurulamadi as e:
        print("OLCULEMEDI: %s" % e)
        return 2
    kotu = {k: v for k, v in saglam.items() if v}
    for ad in VAKALAR:
        print("  %s %-2s %s" % ("+" if not saglam[ad] else "!", ad, "YESIL" if not saglam[ad] else "; ".join(saglam[ad])))
    print("  SAGLAM MOTOR (%d vaka)  %s" % (len(VAKALAR), "YESIL" if not kotu else "KIRMIZI"))
    if kotu:
        print(CIZGI)
        print("SONUC: KIRMIZI — saglam motor vakalari gecemedi.")
        return 1
    isirdi, kacti, olculemedi = [], [], []
    for n, (ad, aciklama, beklenen, degisim) in enumerate(MUTANTLAR):
        d = os.path.join(taban, "m%d" % n)
        os.makedirs(d)
        try:
            sab = sabotajli_motor(d, degisim)
            kir = tum_vakalar(sab, eski, d, "t_")
        except AracKusuru as e:
            print("ARAC KUSURU: %s" % e)
            return 3
        except (Kurulamadi, subprocess.SubprocessError, OSError) as e:
            olculemedi.append(ad)
            print("  ?  %-34s OLCULEMEDI  %s" % (ad, e))
            continue
        except SystemExit:
            raise
        kirilan = {k for k, v in kir.items() if v}
        if kirilan == beklenen:
            isirdi.append(ad)
            print("  +  %-34s ISIRDI      yalniz kendi vakasi: %s" % (ad, ",".join(sorted(kirilan))))
        elif not kirilan:
            kacti.append(ad)
            print("  !  %-34s KACTI       hicbir vaka kirilmadi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
        else:
            kacti.append(ad)
            print("  !  %-34s YANLIS SEBEP/TASMA  kirilan: %s · beklenen: %s" % (ad, ",".join(sorted(kirilan)), ",".join(sorted(beklenen))))
        sys.stdout.flush()
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)" % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    print("(gecici dizin: %s — SILINMEZ)" % taban)
    if kacti:
        return 1
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    print("  Saglam motor YESIL, 6 sabotajin hepsi YALNIZ KENDI vakasinda KIRMIZI: eski projede satir goc eder, baska satira dokunmaz, idempotent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

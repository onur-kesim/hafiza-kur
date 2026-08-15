#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — DEVIR KESFI MUTANTI (uc kapi + uc mutant, ORTUSMESIZ).

NEDEN VAR (olculdu 15 Agu 2026, BITTI md.6)
  `devral`in kesif ayagi YALNIZ `*HAFIZA.md`/`MEMORY.md` taniyordu. `CLAUDE.md`,
  `AGENTS.md`, `DURUM.md`, `memory-bank/`, `.cursor/rules/` GORUNMUYORDU; hicbiri
  eslesmeyince kesif sessizce `PROJE_HAFIZA.md`ye dusup BOS bir defter aciyor ve
  projenin GERCEK hafizasini yok sayiyordu — CIFT DEFTER tam olarak boyle dogar.
  `devral` yolunun bugune kadar TEK canli olcumu vardi (gercek Windows, 421 MB,
  exit 0); yani bu yol pratikte OLCULMUYORDU.

NE OLCER — UC AYRI YUZEY, UC AYRI SENARYO
  Senaryolar KASITLI olarak AYRILDI: bir kapinin senaryosu otekinin ekseninde
  degisiklik uretmesin diye. "ORTUSEN TESPIT KORLUGU MASKELER" — iki kapi ayni
  mutanti yakalarsa, mutant ikisini de olcuyor SANILIR, oysa birini hic olcmuyor
  olabilir. Ortusme burada ARANIR ve bulunursa KIRMIZI yanar.

  KAPI-A (ROL TANIMA) — senaryo: on bes dosya, TANINMAYAN HICBIR SEY YOK
      Kilitli on iki desenin her biri BEKLENEN ROLUYLE listelenmeli
      (canli · kural_evi · gunluk · disarida). Eksik ya da yanlis rol -> KIRMIZI.
      Bu senaryoda taninmayan dosya YOKTUR => KAPI-B'nin eksenine dokunmaz.

  KAPI-B (OLCULEMEDI) — senaryo: `PROJE_HAFIZA.md` + `TASARIM.md` + `olaylar.jsonl`
      Taninmayan her KOK `.md`/`.jsonl` icin "OLCULEMEDI — tanimadim: <ad>"
      satiri basilmali (sessiz atlama YOK), ve TANINAN dosya o listeye
      DUSMEMELI. Senaryoda `CLAUDE.md` YOKTUR => M-1'in ekseninden yalitiktir.
      `.jsonl` yarisi CANLIDIR: adaptorde `.*\\.JSONL$` gibi bir YAKALA-HEPSI
      deseni olsaydi hicbir `.jsonl` asla "taninmayan" olamaz ve olcutun o
      yarisi OLU MANTIK olurdu.

  KAPI-C (DURMA KURALI) — iki kollu, ayni eksen
      C1 ZARAR ESIGI : `CLAUDE.md` + `DURUM.md` (canli YOK) -> `devral` cikis != 0,
                       DISKE TEK BAYT yazilmamis (.hafizarc yok, PROJE_HAFIZA.md
                       yok, arsiv/ yok) ve mesaj `--esle` istiyor.
      C2 ADDITIVE    : `PROJE_HAFIZA.md` + `CLAUDE.md` -> `devral` cikis 0.
                       Durma kurali MEVCUT projeleri etkilemez; bu kol kuralin
                       ASIRI ateslenmedigini olcer.

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. `--esle`nin HATA yollari (bilinmeyen rol, agac disi yol, ayni rol iki kez)
     bu araca GIRMEDI: `cli_yol_coz` gecidi ayri bir yuzeydir ve kendi kapisi
     vardir. Burada yalniz `--esle canli=` ile durma kuralinin ACILDIGI olculur.
  2. `indeks` rolunun tabloda deseni YOKTUR (yalniz `--esle` ile atanir); bu arac
     o rolu OLCMEZ, cunku olculecek bir desen yok.
  3. Bu arac `devral`in YAZIM ayagini (cipa, zincir, yedek, triyaj) olcmez —
     C2'de yalniz CIKIS KODUNA bakar. Yazim ayagi ortak bataryanin isidir.
  4. Gercek Windows'ta yol ayraci davranisi CI'nin windows isindedir.

CIKIS KODLARI
  0  uc kapi da temiz VE 3/3 mutant AYRI eksende ISIRDI
  1  bir kapi kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi) — sessiz PASS verilmez
"""
import io
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

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

# ------------------------------------------------------------------ senaryolar
# (goreli yol, icerik) — icerik ONEMSIZ; kesif ADLARA bakar.
S_A = [
    ("PROJE_HAFIZA.md", "# H\n\n## GUNCEL DURUM\n"),
    ("MEMORY.md", "x\n"),
    ("ESKI_HAFIZA.md", "x\n"),
    ("CLAUDE.md", "x\n"),
    ("AGENTS.md", "x\n"),
    ("GEMINI.md", "x\n"),
    (".cursorrules", "x\n"),
    (".cursor/rules/010-stil.mdc", "x\n"),
    (".github/copilot-instructions.md", "x\n"),
    ("DURUM.md", "x\n"),
    ("BORCLAR.md", "x\n"),
    ("_ZINCIR.jsonl", "{}\n"),
    ("PROJE_RADAR.jsonl", "{}\n"),
    ("memory-bank/activeContext.md", "x\n"),
    ("memory-bank/progress.md", "x\n"),
]
BEKLENEN_ROL = {
    "PROJE_HAFIZA.md": "canli", "MEMORY.md": "canli", "ESKI_HAFIZA.md": "canli",
    "CLAUDE.md": "kural_evi", "AGENTS.md": "kural_evi", "GEMINI.md": "kural_evi",
    ".cursorrules": "kural_evi", ".cursor/rules/010-stil.mdc": "kural_evi",
    ".github/copilot-instructions.md": "kural_evi",
    "DURUM.md": "gunluk", "BORCLAR.md": "gunluk",
    "_ZINCIR.jsonl": "gunluk", "PROJE_RADAR.jsonl": "gunluk",
    "memory-bank/activeContext.md": "disarida", "memory-bank/progress.md": "disarida",
}

S_B = [("PROJE_HAFIZA.md", "# H\n\n## GUNCEL DURUM\n"),
       ("TASARIM.md", "x\n"), ("olaylar.jsonl", "{}\n")]
B_TANINMAYAN = ("TASARIM.md", "olaylar.jsonl")
B_TANINAN = ("PROJE_HAFIZA.md",)

S_C1 = [("CLAUDE.md", "x\n"), ("DURUM.md", "x\n")]
S_C2 = [("PROJE_HAFIZA.md", "# H\n\n## GUNCEL DURUM\n"), ("CLAUDE.md", "x\n")]

_ROL = re.compile(r"^ {2}(canli|kural_evi|gunluk|indeks|disarida) *: *(\S+)")
_TANIMADIM = re.compile(r"OLCULEMEDI\b.*tanimadim: *(\S+)")


def kur_senaryo(taban, dosyalar):
    kok = tempfile.mkdtemp(prefix="devir_", dir=taban)
    for rel, icerik in dosyalar:
        p = os.path.join(kok, *rel.split("/"))
        d = os.path.dirname(p)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with io.open(p, "w", encoding="utf-8", newline="") as f:
            f.write(icerik)
    return kok


def kos(motor, kok, *ek):
    p = subprocess.Popen([sys.executable, motor, "devral", "--kok=" + kok] + list(ek),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cikti = p.communicate()[0].decode("utf-8", "replace")
    return p.returncode, cikti


def roller(cikti):
    out = {}
    for s in cikti.split("\n"):
        m = _ROL.match(s.rstrip("\r"))
        if m:
            out[m.group(2)] = m.group(1)
    return out


def tanimadiklari(cikti):
    return set(m.group(1) for m in (_TANIMADIM.search(s) for s in cikti.split("\n")) if m)


# ------------------------------------------------------------------- KAPI-A
def kapi_a(motor, taban):
    kok = kur_senaryo(taban, S_A)
    kod, cikti = kos(motor, kok, "--kesif")
    b = []
    if kod != 0:
        b.append("`--kesif` cikis %d (0 bekleniyordu)" % kod)
    goru = roller(cikti)
    for rel, beklenen in sorted(BEKLENEN_ROL.items()):
        gelen = goru.get(rel)
        if gelen is None:
            b.append("%s HIC listelenmedi" % rel)
        elif gelen != beklenen:
            b.append("%s rolu %r (beklenen %r)" % (rel, gelen, beklenen))
    return b


# ------------------------------------------------------------------- KAPI-B
def kapi_b(motor, taban):
    kok = kur_senaryo(taban, S_B)
    kod, cikti = kos(motor, kok, "--kesif")
    b = []
    if kod != 0:
        b.append("`--kesif` cikis %d (0 bekleniyordu)" % kod)
    goru = tanimadiklari(cikti)
    for rel in B_TANINMAYAN:
        if rel not in goru:
            b.append("%s icin OLCULEMEDI satiri YOK (sessiz atlama)" % rel)
    for rel in B_TANINAN:
        if rel in goru:
            b.append("%s TANINAN oldugu halde OLCULEMEDI'ye dustu" % rel)
    return b


# ------------------------------------------------------------------- KAPI-C
def _yazildi_mi(kok):
    return sorted(x for x in (".hafizarc", "PROJE_HAFIZA.md", "arsiv", "gunluk", "kararlar")
                  if os.path.exists(os.path.join(kok, x)))


def kapi_c(motor, taban):
    b = []
    # --- C1 ZARAR ESIGI: canli YOK -> DUR, hicbir sey yazma
    kok = kur_senaryo(taban, S_C1)
    kod, cikti = kos(motor, kok)
    if kod == 0:
        b.append("C1: canli YOKKEN cikis 0 — motor gene defter acti")
    if "--esle" not in cikti:
        b.append("C1: mesaj `--esle` istemiyor (kullaniciya cikis yolu verilmedi)")
    art = _yazildi_mi(kok)
    if art:
        b.append("C1: DURMASINA RAGMEN yazdi: %s" % ", ".join(art))
    # --- C1b: `--esle canli=` kilidi durmayi ACAR
    kok = kur_senaryo(taban, S_C1)
    kod, cikti = kos(motor, kok, "--esle", "canli=DURUM.md")
    if kod != 0:
        b.append("C1b: `--esle canli=DURUM.md` ile de DURDU (cikis %d) — kilit acmiyor" % kod)
    # --- C2 ADDITIVE: taninan canli VARSA bugunku akis
    kok = kur_senaryo(taban, S_C2)
    kod, cikti = kos(motor, kok)
    if kod != 0:
        b.append("C2: taninan `canli` VARKEN cikis %d — durma kurali ASIRI atesliyor "
                 "(mevcut projeler kirilir)" % kod)
    return b


def hukum(motor, taban):
    return kapi_a(motor, taban), kapi_b(motor, taban), kapi_c(motor, taban)


# --------------------------------------------------------------- MUTANTLAR
# 🔴 OLCULDU 15 Agu 2026, ILK KOSUM: M-3'un capasi (`    if not adaylar:`) motorda
#    UC YERDE geciyordu ve `str.replace(..., 1)` mutanti YANLIS FONKSIYONA kurdu.
#    Metin degisti, `bozuk != s` oldu, arac mutanti "kuruldu" saydi ve KACTI dedi.
#    Bu bir mutant kusuru degil, KAPI KORLUGU URETEN bir arac kusurudur: "uygulandi"
#    ile "DOGRU YERE uygulandi" ayni sey degildir. Artik capa TEK YERDE olmak
#    ZORUNDA; degilse mutant KURULAMADI sayilir (= kirmizi), sessizce gecmez.
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n"
                         % (n, hedef[:60]))
        return False
    return True


def m1_tablodan_claude_silinir(s):
    """Adaptor tablosundan `CLAUDE.md` satiri silinir -> KAPI-A isirmali.

    Ekseni: ROL TANIMA. KAPI-B'nin senaryosunda `CLAUDE.md` YOKTUR, KAPI-C'de
    `canli` zaten yoktur/vardir (durma hukmu degismez) => ortusmez."""
    L = s.split("\n")
    hedef = [x for x in L if r"^CLAUDE\.MD$" in x]
    if len(hedef) != 1:
        sys.stdout.write("      ! adaptor tablosunda CLAUDE.md satiri %d yerde "
                         "(1 olmali)\n" % len(hedef))
        return None
    return "\n".join(x for x in L if x != hedef[0])


def m2_olculemedi_bastirilir(s):
    """OLCULEMEDI satirlari bastirilir (sessiz atlama geri gelir) -> KAPI-B isirmali.

    Ekseni: GORUNURLUK. KAPI-A'nin senaryosunda taninmayan dosya YOKTUR ve
    KAPI-C cikis koduna bakar => ortusmez."""
    hedef = "    for rel in olculemedi:\n"
    yeni = "    for rel in olculemedi[:0]:      # MUTANT: sessiz atlama\n"
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m3_durma_kosuluna_ve_eklenir(s):
    """Durma kosuluna `and olculemedi` eklenir -> KAPI-C isirmali.

    Bu, olcut (c)'nin ILK (VE'li) yaziminin ta kendisidir ve OLCULDU: DELIK.
    `CLAUDE.md` + `DURUM.md` tasiyan gercek bir projede her iki dosya da
    TANINDIGI icin `olculemedi` BOS kalir, kosul atesleneMEZ ve motor gene BOS
    defter acar. Ekseni: DURMA. KAPI-A ve KAPI-B `--kesif` ile kosar (durma
    yolunu hic yurumez) => ortusmez."""
    # CAPA `if not adaylar:` TEK BASINA YETMEZ — motorda uc yerde geciyor
    # (olculdu). Durma blogunun KENDI mesajiyla birlikte capalanir.
    hedef = '    if not adaylar:\n        oldur("DEVIR DURDU'
    yeni = ('    if not adaylar and olculemedi:      # MUTANT: VE\'li ilk yazim\n'
            '        oldur("DEVIR DURDU')
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


MUTANTLAR = [
    ("M-1 tablodan CLAUDE.md silinir", m1_tablodan_claude_silinir, "KAPI-A"),
    ("M-2 OLCULEMEDI bastirilir", m2_olculemedi_bastirilir, "KAPI-B"),
    ("M-3 durma kosuluna VE eklenir", m3_durma_kosuluna_ve_eklenir, "KAPI-C"),
]


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    print(CIZGI)
    print("DEVIR KESFI MUTANTI — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="devir_kesif_")
    try:
        a, b, c = hukum(yol, taban)
        for ad, bulgu, ne in (("KAPI-A ROL TANIMA ", a, "%d desen dogru rolde" % len(BEKLENEN_ROL)),
                              ("KAPI-B OLCULEMEDI ", b, "sessiz atlama yok"),
                              ("KAPI-C DURMA      ", c, "C1 durdu+yazmadi · C1b kilit acti · C2 additive")):
            print("  %s: %s" % (ad, "YESIL (%s)" % ne if not bulgu
                                else "KIRMIZI — %d bulgu" % len(bulgu)))
            for x in bulgu:
                print("      ! %s" % x)
        if a or b or c:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = 0
        for ad, boz, beklenen in MUTANTLAR:
            bozuk = boz(s)
            if bozuk is None or bozuk == s:
                print("  %-34s KURULAMADI (mutant uygulanamadi)" % ad)
                kacan += 1
                continue
            mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
            mp = os.path.join(mdir, "hafiza.py")
            with io.open(mp, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            ma, mb, mc = hukum(mp, taban)
            ates = ([x for x, v in (("KAPI-A", ma), ("KAPI-B", mb), ("KAPI-C", mc)) if v])
            if ates == [beklenen]:
                print("  %-34s -> ISIRDI ✓  (%s)" % (ad, beklenen))
            elif beklenen in ates:
                print("  %-34s -> ISIRDI ama ORTUSTU: %s" % (ad, " + ".join(ates)))
                kacan += 1
            else:
                print("  %-34s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                      % (ad, beklenen, " + ".join(ates) or "hicbiri"))
                kacan += 1
        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
                  % (kacan, len(MUTANTLAR)))
            return 1
        print("SONUC: YESIL — uc kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
              % (len(MUTANTLAR), len(MUTANTLAR)))
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

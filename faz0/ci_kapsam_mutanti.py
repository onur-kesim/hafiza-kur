#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI KAPSAM KAPISININ MUTANTI — kapi gercekten ISIRIYOR mu?

Kapinin var olmasi isirdigi anlamina gelmez (doktrin 1). Bu betik IKI SORUYU
ayri ayri olcer:

  A) GIRDI SENARYOLARI — depo hali sabote edilir, kapi dogru hukmu vermeli.
     S-2 tam olarak yasanan hali yeniden uretir: mutant betigi var, CI isi yok.

  B) KAPI MUTANTLARI — kapinin KENDI kodu sabote edilir; her mutant icin
     "hangi senaryo bunu yakalar" ONCEDEN yazilidir. Yakalayan senaryo yoksa
     o kod parcasi KOR bir suslemedir ve silinmelidir.

  Ikisi ayri sorudur: (A) kapinin dis dunyayi olcup olcmedigini, (B) kapinin
  hicbir parcasinin bos yere durmadigini gosterir. Yalnizca (A) kosulursa
  "kapi calisiyor" denir ama icindeki olu kod gorunmez.

CIKIS KODU  0 hepsi beklendigi gibi · 1 en az biri KACTI · 2 OLCULEMEDI
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAPI = os.path.join(KOK, "faz0", "ci_kapsam_kapisi.py")
WF = os.path.join(".github", "workflows", "capraz.yml")
CIZGI = "-" * 78


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi — kapinin hukmu degil."""


def kos(kapi, kok):
    r = subprocess.run([sys.executable, "-X", "utf8", kapi, "--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def iskelet_kur(taban):
    """Gercek depodan MINIMUM iskelet: faz0'daki bolme mutantlarinin ADLARI
    (icerik gerekmez, kapi ada bakar) + gercek capraz.yml."""
    kok = os.path.join(taban, "depo")
    os.makedirs(os.path.join(kok, "faz0"))
    os.makedirs(os.path.join(kok, ".github", "workflows"))
    kaynak_faz0 = os.path.join(KOK, "faz0")
    adlar = sorted(f for f in os.listdir(kaynak_faz0) if f.endswith("_bolme_mutanti.py"))
    if not adlar:
        raise Kurulamadi("kaynak depoda hic *_bolme_mutanti.py yok")
    for ad in adlar:
        open(os.path.join(kok, "faz0", ad), "w", encoding="utf-8").write("# yer tutucu\n")
    kaynak_wf = os.path.join(KOK, WF)
    if not os.path.isfile(kaynak_wf):
        raise Kurulamadi("kaynak depoda %s yok" % WF)
    shutil.copyfile(kaynak_wf, os.path.join(kok, WF))
    return kok, adlar


def wf_oku(kok):
    return open(os.path.join(kok, WF), encoding="utf-8").read()


def wf_yaz(kok, metin):
    open(os.path.join(kok, WF), "w", encoding="utf-8", newline="\n").write(metin)


# ----------------------------------------------------------- GIRDI SENARYOLARI
# (ad, aciklama, hazirlik(kok, adlar), beklenen_exit)

def _s1_is_silindi(kok, adlar):
    hedef = adlar[-1]
    metin = wf_oku(kok)
    yeni = "\n".join(s for s in metin.split("\n") if ("faz0/" + hedef) not in s)
    if yeni == metin:
        raise Kurulamadi("workflow'da faz0/%s satiri zaten yok" % hedef)
    wf_yaz(kok, yeni)
    return hedef


def _s2_yeni_mutant_is_yok(kok, adlar):
    # YASANAN HAL: betik commit'e girdi, workflow girmedi.
    yeni = "h11_bolme_mutanti.py"
    open(os.path.join(kok, "faz0", yeni), "w", encoding="utf-8").write("# yer tutucu\n")
    return yeni


def _s3_yalniz_yorumda(kok, adlar):
    # Is silinir ama dosya adi bir YORUM satirinda birakilir.
    hedef = _s1_is_silindi(kok, adlar)
    wf_yaz(kok, wf_oku(kok) + "\n  #     ileride: python faz0/%s eklenecek\n" % hedef)
    return hedef


def _s4_temiz(kok, adlar):
    return "-"


def _s5_hic_mutant_yok(kok, adlar):
    for ad in adlar:
        os.remove(os.path.join(kok, "faz0", ad))
    return "-"


def _s6_workflow_yok(kok, adlar):
    os.remove(os.path.join(kok, WF))
    return "-"


SENARYOLAR = [
    ("S-1 IS SILINDI", "bir bolme mutantinin `run:` satiri kaldirildi", _s1_is_silindi, 1),
    ("S-2 YENI MUTANT, IS YOK", "YASANAN HAL: betik var, CI isi yok", _s2_yeni_mutant_is_yok, 1),
    ("S-3 YALNIZ YORUMDA", "is yok ama ad bir YORUM satirinda geciyor", _s3_yalniz_yorumda, 1),
    ("S-4 TEMIZ", "dokunulmamis depo — yalanci kirmizi yakmamali", _s4_temiz, 0),
    ("S-5 HIC MUTANT YOK", "olcecek bir sey yok -> OLCULEMEDI, YESIL DEGIL", _s5_hic_mutant_yok, 2),
    ("S-6 WORKFLOW YOK", "capraz.yml yok -> OLCULEMEDI", _s6_workflow_yok, 2),
]

# ------------------------------------------------------------- KAPI MUTANTLARI
# Her mutant, KENDISINI YAKALAMASI BEKLENEN senaryoyla birlikte yazilir.
# Yakalayan yoksa o satir kapida bos duruyordur.

KAPI_MUTANTLARI = [
    ("M-1 YORUM FILTRESI", "yorum satirlari da sayilir olsun",
     [('    return [s for s in metin.split("\\n") if s.lstrip()[:1] != "#"]',
       '    return metin.split("\\n")')],
     "S-3 YALNIZ YORUMDA"),
    ("M-2 BOS KUME KONTROLU", "bos kumede OLCULEMEDI yerine YESIL",
     [('    if not betikler:\n        return 2, "hicbir faz0/*_bolme_mutanti.py bulunamadi'
       ' — bu kapi HICBIR SEY olcmuyor", []',
       '    if not betikler:\n        return 0, "", []')],
     "S-5 HIC MUTANT YOK"),
    ("M-3 KIRMIZI CIKIS KODU", "kacan varken yine de 0 don",
     [("    return (1 if kacan else 0), \"\", sonuc",
       "    return 0, \"\", sonuc")],
     "S-1 IS SILINDI"),
]


def sabotajli_kapi(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli kapi derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "ci_kapsam_kapisi.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def senaryo_kur(taban, ad, hazirlik):
    kok, adlar = iskelet_kur(os.path.join(taban, re.sub(r"\W+", "_", ad)))
    hazirlik(kok, adlar)
    return kok


def main():
    if not os.path.isfile(KAPI):
        print("OLCULEMEDI: kapi yok: %s" % KAPI)
        return 2
    kaynak = open(KAPI, encoding="utf-8").read()

    print(CIZGI)
    print("CI KAPSAM KAPISI MUTANTI")
    print("kapi: %s" % KAPI)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="cikapsam_")
    kokler, kacan = {}, []
    try:
        # ---- A) GIRDI SENARYOLARI -----------------------------------------
        print("A) GIRDI SENARYOLARI — temiz kapi dogru hukmu veriyor mu")
        for ad, aciklama, hazirlik, beklenen in SENARYOLAR:
            try:
                kok = senaryo_kur(taban, ad, hazirlik)
            except Kurulamadi as e:
                print("  ?  %-24s OLCULEMEDI  %s" % (ad, e))
                return 2
            kokler[ad] = kok
            rc, _ = kos(KAPI, kok)
            ok = rc == beklenen
            if not ok:
                kacan.append("%s (beklenen exit %d, cikan %d)" % (ad, beklenen, rc))
            print("  %s  %-24s exit %d (beklenen %d)   %s"
                  % ("+" if ok else "!", ad, rc, beklenen, aciklama))

        # ---- B) KAPI MUTANTLARI -------------------------------------------
        print(CIZGI)
        print("B) KAPI MUTANTLARI — kapinin her parcasi ISIRIYOR mu")
        for ad, aciklama, degisimler, yakalayan in KAPI_MUTANTLARI:
            d = os.path.join(taban, "mut_" + re.sub(r"\W+", "_", ad))
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_kapi(kaynak, degisimler, d)
            except Kurulamadi as e:
                print("  ?  %-24s OLCULEMEDI  %s" % (ad, e))
                return 2
            beklenen = dict((s[0], s[3]) for s in SENARYOLAR)[yakalayan]
            rc, _ = kos(sab, kokler[yakalayan])
            isirdi = rc != beklenen
            if not isirdi:
                kacan.append("%s (yakalamasi beklenen: %s)" % (ad, yakalayan))
            print("  %s  %-24s %-11s %s -> exit %d (temizde %d)   %s"
                  % ("+" if isirdi else "!", ad, "ISIRDI" if isirdi else "KACTI",
                     yakalayan, rc, beklenen, aciklama))

        print(CIZGI)
        if kacan:
            print("HUKUM: KIRMIZI — %d olcum beklendigi gibi cikmadi:" % len(kacan))
            for k in kacan:
                print("    %s" % k)
            return 1
        print("HUKUM: %d senaryo + %d kapi mutanti, hepsi beklendigi gibi."
              % (len(SENARYOLAR), len(KAPI_MUTANTLARI)))
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OTURUM SAGLIGI MUTANTI — olcerin kendisi ISIRIYOR mu?

"Olculmeyen kapinin hukmu YOKTUR" (doktrin 1). `oturum_sagligi.py` bir kapidir:
esik asildiginda HUKUM DEGISTIRMELI ve olculemeyeni YESIL SAYMAMALI. Bu dosya
alti kusuru tek tek enjekte eder; altisi da ISIRMALIDIR.

DUZENEK: gercek transcript kullanilmaz — SENTETIK jsonl uretilir (bilinen
sayilar). Boylece hukum, makinenin o anki oturumuna degil YALNIZ araca baglidir.
Bu ayrim FazA'nin 7. dersidir: bir prob ORTAMI mi olcuyor ARACI mi.

CIKIS KODU   0 hepsi isirdi · 1 en az biri kacti · 2 OLCULEMEDI
"""
import json
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARAC = os.path.join(KOK, "araclar", "oturum_sagligi.py")
CIZGI = "-" * 84


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()


def transcript_yaz(yol, cikti, girdi=0, cache_y=0, cache_o=0, bozuk=0):
    """Tek usage kaydiyla sentetik transcript. Sayilar TAM olarak istenendir."""
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "x"}}) + "\n")
        for _ in range(bozuk):
            f.write("{bu satir bozuk\n")
        f.write(json.dumps({"message": {"usage": {
            "input_tokens": girdi, "output_tokens": cikti,
            "cache_creation_input_tokens": cache_y,
            "cache_read_input_tokens": cache_o}}}) + "\n")


def kos(arac, *args):
    r = subprocess.run([sys.executable, "-X", "utf8", arac] + list(args),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# (ad, aciklama, [(eski, yeni)])
MUTANTLAR = [
    ("M-S1 SARI ESIGI", "SARI esigi 400k'dan 4M'a cikar — asilan esik gorunmez olur",
     [("ESIKLER = [(400_000,", "ESIKLER = [(4_000_000,")]),
    ("M-S2 KIRMIZI ESIGI", "KIRMIZI esigi 650k'dan 65M'a cikar — DUR hukmu hic verilmez",
     [("(650_000, \"TURUNCU\", 3)", "(65_000_000, \"TURUNCU\", 3)")]),
    ("M-S3 FORMUL", "varsayilan formule cache okumasi eklenir — sayi ~100x sisirilir",
     [('"girdi+cikti": ("input", "output"),',
       '"girdi+cikti": ("input", "output", "cache_okumasi"),')]),
    ("M-S4 OLCULEMEDI SOKME", "transcript yoksa OLCULEMEDI yerine YESIL basar (koruma sokme)",
     [('print("OLCULEMEDI: transcript bulunamadi (%s)" % (yol or "arama bos dondu"))\n'
       '        print("  arananlar: %s" % " · ".join(ARAMA))\n        return 2',
       'print("YESIL (transcript yok)")\n        return 0')]),
    ("M-S5 CIKIS KODU", "KIRMIZI hukmu basilir ama cikis kodu 0 doner — sozlesme kirilir",
     [('(float("inf"), "KIRMIZI", 4)', '(float("inf"), "KIRMIZI", 0)')]),
    ("M-S6 SESSIZ ATLAMA", "bozuk satir sayaci susturulur — eksik olcum gorunmez olur",
     [("                atlanan += 1", "                pass")]),
]

# (ad, transcript kw, arac argumanlari, beklenen hukum parcasi, beklenen exit)
HALLER = [
    ("h_yesil", dict(cikti=100_000), (), "YESIL", 0),
    ("h_sari", dict(cikti=450_000), (), "SARI", 1),
    ("h_turuncu", dict(cikti=550_000), (), "TURUNCU", 3),
    ("h_kirmizi", dict(cikti=700_000), (), "KIRMIZI", 4),
    ("h_cache_yuku", dict(cikti=10_000, cache_o=9_000_000), (), "YESIL", 0),
    ("h_bozuk_satir", dict(cikti=1_000, bozuk=3), (), "YESIL", 0),
]


def kume_olc(arac, taban):
    """{hal: (exit, normalize edilmis cikti)} — yol adi normalize edilir."""
    out = {}
    for ad, kw, ek, _, _ in HALLER:
        t = os.path.join(taban, ad + ".jsonl")
        transcript_yaz(t, **kw)
        rc, c = kos(arac, "--transcript", t, *ek)
        out[ad] = (rc, c.replace(t, "<T>").replace(taban, "<TABAN>"))
    # transcript YOKLUGU da bir haldir: koruma dali ancak boyle uyanir.
    yok = os.path.join(taban, "olmayan.jsonl")
    rc, c = kos(arac, "--transcript", yok)
    out["h_transcript_yok"] = (rc, c.replace(yok, "<T>").replace(taban, "<TABAN>"))
    return out


def main():
    if not os.path.isfile(ARAC):
        print("OLCULEMEDI: arac yok: %s" % ARAC)
        return 2
    kaynak = open(ARAC, encoding="utf-8").read()
    taban = tempfile.mkdtemp(prefix="sagmut_")
    print(CIZGI)
    print("OTURUM SAGLIGI MUTANTI — olcerin kendisi isiriyor mu?")
    print(CIZGI)
    try:
        referans = kume_olc(ARAC, taban)
        ikinci = kume_olc(ARAC, taban)
        if referans != ikinci:
            print("OLCULEMEDI: duzenek determinist degil.")
            return 2
        # HAL KAPISI: temiz kolda beklenen hukum GERCEKTEN cikmali; cikmiyorsa
        # kume yanlis kurulmustur ve butun mutantlar sahte 'temiz' gorunur.
        for ad, _, _, bek_h, bek_e in HALLER:
            rc, c = referans[ad]
            if bek_h not in c or rc != bek_e:
                print("OLCULEMEDI: hal %s beklenen hukmu vermedi "
                      "(beklenen %s/exit %d, gorulen exit %d)" % (ad, bek_h, bek_e, rc))
                print("   " + c.strip().replace("\n", "\n   ")[:400])
                return 2
        if referans["h_transcript_yok"][0] != 2:
            print("OLCULEMEDI: transcript yoklugu 2 dondurmedi — taban kol zaten bozuk.")
            return 2
        print("  temiz kol: 7 hal, 7 hukum beklendigi gibi (YESIL/SARI/TURUNCU/KIRMIZI"
              " + cache yuku + bozuk satir + transcript yok)")
        print(CIZGI)
        isirdi, kacti = [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            metin = kaynak
            hatali = False
            for eski, yeni in degisimler:
                if metin.count(eski) != 1:
                    print("  ?  %-22s OLCULEMEDI  hedef dizge %d kez gecti"
                          % (ad, metin.count(eski)))
                    hatali = True
                    break
                metin = metin.replace(eski, yeni, 1)
            if hatali:
                return 2
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            sab = os.path.join(d, "oturum_sagligi.py")
            with open(sab, "w", encoding="utf-8", newline="\n") as f:
                f.write(metin)
            try:
                compile(metin, "<mutant>", "exec")
            except SyntaxError as e:
                print("  ?  %-22s OLCULEMEDI  derlenmiyor: %s" % (ad, e))
                return 2
            yeni_olcum = kume_olc(sab, taban)
            farkli = [h for h in referans if referans[h] != yeni_olcum[h]]
            if farkli:
                isirdi.append(ad)
                print("  +  %-22s ISIRDI      %d halde fark: %s"
                      % (ad, len(farkli), ",".join(h[2:] for h in sorted(farkli))[:38]))
            else:
                kacti.append(ad)
                print("  !  %-22s KACTI       -> %s" % (ad, aciklama))
            sys.stdout.flush()
    finally:
        import shutil
        shutil.rmtree(taban, ignore_errors=True)
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti (toplam %d)" % (len(isirdi), len(kacti), len(MUTANTLAR)))
    if kacti:
        print("  KACAN mutant = olcerin KOR oldugu sinif.")
        return 1
    print("  Olcerin her maddesi olculuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

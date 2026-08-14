#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETKI IMZASI HARNESS'ININ MUTANTI — yeni yuzey MASRAFINI HAK EDIYOR MU?

Bu betik `cmd_kur`u BOLMEZ. Once harness'in kendisini olcer; bolme ondan sonra
gelir. Gerekce projenin kendi dersi: bir prob ORTAMI mi ARACI mi olcuyor ayrimi.
Harness bolmeden SONRA yazilsaydi, bir mutant isirdiginda BOLMEYI mi yoksa
KOMUTU mu olctugu belirsiz kalirdi. Once bolunmemis komuta karsi yazilir ve
isirdigi kanitlanir; ancak ondan sonra bolme yapilir.

OLCULEN IDDIA (tek cumle):
    `(exit, stdout)` yuzeyi ETKILI komutlarda KORDUR, etki imzasi bu korlugu
    kapatir — ve bu bir iddia degil, her mutant icin AYRI AYRI olculur.

Her mutant icin IKI yuzey birden hesaplanir:
    ESKI YUZEY  = (exit, stdout)                      <- kapi kalibinin yuzeyi
    YENI YUZEY  = (exit, stdout, DISK AGACI IMZASI)   <- etki imzasi

Dort hucre mumkun ve DORDU DE anlamlidir:
    ESKI ISIRDI  · YENI ISIRDI   -> yeni yuzey bu mutant icin GEREKSIZ
    ESKI KOR     · YENI ISIRDI   -> 🔴 YENI YUZEY KAZANDI (harness'in varlik sebebi)
    ESKI ISIRDI  · YENI KOR      -> IMKANSIZ; cikarsa harness BOZUK (yeni yuzey
                                     eskiyi kapsar). Bu betik bunu ayrica olcer.
    ESKI KOR     · YENI KOR      -> ikisi de kor: gercek bir bosluk ya da
                                     esdeger mutant. Ayirt etmek okuyucunun isi.

Eger HICBIR mutantta "ESKI KOR · YENI ISIRDI" cikmazsa, etki imzasi bu komut icin
masrafini HAK ETMIYOR demektir ve betik bunu KIRMIZI yazar. Harness'in degeri
beyan edilmez, OLCULUR.

CIKIS KODU  0 yeni yuzey kazandi · 1 kazanmadi ya da harness bozuk · 2 OLCULEMEDI
"""
import argparse
import importlib.util
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
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
IMZA_MODUL = os.path.join(KOK, "faz0", "etki_imzasi.py")
CIZGI = "-" * 92

_RE_SHA = re.compile(r"\b[0-9A-Fa-f]{16,}\b")
_RE_TARIH = re.compile(r"\b20\d\d-\d\d-\d\d\b")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi."""


def _imza_modulu():
    spec = importlib.util.spec_from_file_location("etki_imzasi", IMZA_MODUL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def stdout_normalize(metin, kok):
    m = metin.replace(kok, "<KOK>").replace(kok.replace("/", "\\"), "<KOK>")
    m = _RE_SHA.sub("<SHA>", m)
    return _RE_TARIH.sub("<TARIH>", m)


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300, cwd=kok)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# --------------------------------------------------------------------- HALLER
# Her hal `cmd_kur`un AYRI bir dalini calistirir. HAL KAPISI: iki hal ayni
# (exit, stdout, imza) uclusunu uretirse dal ayrismiyor demektir -> OLCULEMEDI.

def _h_taze(kok):
    """ilk kurulum: .hafizarc yok, arsiv yok"""
    return ["kur", "--ad", "ETKI", "--kok", kok]


def _h_idempotent(kok, motor=None):
    """ikinci kez kur: tazeleme dali (zincir_butunlugu_sart + KURULUM halkasi)"""
    return ["kur", "--ad", "ETKI", "--kok", kok]


def _h_v1_izi(kok):
    """v1 izi var, .hafizarc yok -> oldur (yazmadan cikmali)"""
    return ["kur", "--ad", "ETKI", "--kok", kok]


def _h_kok_yok(kok):
    return ["kur", "--ad", "ETKI", "--kok", os.path.join(kok, "olmayan-dizin")]


def _hazir_taze(motor, kok):
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)


def _hazir_idempotent(motor, kok):
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "ETKI", "--kok", kok], kok)
    if rc != 0:
        raise Kurulamadi("on kurulum basarisiz: %s" % c.strip().split("\n")[-1][:100])


def _hazir_v1_izi(motor, kok):
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    d = os.path.join(kok, "arsiv", "hafiza")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "_ZINCIR.jsonl"), "w", encoding="utf-8").write("")
    open(os.path.join(d, "_KAYNAK.md"), "w", encoding="utf-8").write("# eski\n")


def _hazir_kok_yok(motor, kok):
    subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)


HALLER = [
    ("h_taze", _hazir_taze, _h_taze, "ilk kurulum"),
    ("h_idempotent", _hazir_idempotent, _h_idempotent, "ikinci kur: tazeleme dali"),
    ("h_v1_izi", _hazir_v1_izi, _h_v1_izi, "v1 izi var -> oldur"),
    ("h_kok_yok", _hazir_kok_yok, _h_kok_yok, "kok yok -> oldur"),
]


# ------------------------------------------------------------------- MUTANTLAR
# Hepsi SESSIZ YAZIM sinifindandir: stdout ve exit AYNI kalmasi BEKLENIR,
# diskteki agac degisir. Kapi kaliби bunlara yapisal olarak kordur.

MUTANTLAR = [
    ("S-1 KOVA filtresi",
     "`anlamli(s)` filtresi dusuyor — _KOVA.json fazla satir tasiyor",
     [('        kv = {"satirlar": {str(i + 1): "CANLI" for i, s in enumerate(L) if anlamli(s)}}',
       '        kv = {"satirlar": {str(i + 1): "CANLI" for i, s in enumerate(L)}}')]),
    ("S-2 arsiv dizini eksik",
     "arsiv turlerinin ILKI atlaniyor — bir dizin hic olusmuyor",
     [('    for t in rc["arsiv_turleri"]:\n        os.makedirs(os.path.join(kok, "arsiv", t), exist_ok=True)',
       '    for t in rc["arsiv_turleri"][1:]:\n        os.makedirs(os.path.join(kok, "arsiv", t), exist_ok=True)')]),
    ("S-3 DUZELTMELER bicimi",
     "_DUZELTMELER.json bicimi degisiyor (ayni anlam, farkli bayt)",
     [("""    for p, ilk in [(y.duzelt, '{\\n  "duzeltmeler": []\\n}\\n'),""",
       """    for p, ilk in [(y.duzelt, '{"duzeltmeler": []}\\n'),""")]),
    ("S-4 kural dosyasi metni",
     "CLAUDE.md protokol metni degisiyor — kimse stdout'ta gormez",
     [('                     "> BUDAMA TESTİ: bir satırı silmek modelin hata yapmasına yol açmıyorsa, KES.\\n" % ad)',
       '                     "> BUDAMA TESTI: kes.\\n" % ad)')]),
    # 🔴 BILINEN KOR NOKTANIN OLCUMU — bu mutantin KACMASI BEKLENIR.
    # `etki_imzasi.py` `halka`/`onceki` alanlarini normalize eder (zamandan
    # tureyen hash'ler). Bedeli: YALNIZCA halka hash'ini bozan bir kusur bu
    # yuzeye gorunmez. Kor nokta varsayilmadi, OLCULDU: asagidaki mutant
    # raporda "IKISI DE KOR" satiri olarak GORUNUR ve orada durur.
    # Kapatmanin dogru yolu zincir dogrulamasini AYRI bir kapiyla olcmektir.
    ("S-5 HALKA hash'i (kor nokta)",
     "halka hash'i bozuluyor, girdilerine dokunulmuyor — normalize edildigi icin GORUNMEZ",
     [('    kayit["halka"] = sha(onceki + json.dumps({k: v for k, v in kayit.items() if k != "halka"},\n'
       '                                             sort_keys=True, ensure_ascii=False))',
       '    kayit["halka"] = sha(onceki + json.dumps({k: v for k, v in kayit.items() if k != "halka"},\n'
       '                                             sort_keys=True, ensure_ascii=False))[::-1]')]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def kume_olc(motor, taban, im_modul):
    """Her hal icin (exit, normalize stdout, disk imzasi) ucer."""
    out = {}
    for ad, hazir, arglar, _ in HALLER:
        kok = os.path.join(taban, ad)
        os.makedirs(kok, exist_ok=True)
        hazir(motor, kok)
        rc, c = kos(motor, arglar(kok), kok)
        try:
            im = im_modul.imza(kok)
        except im_modul.Olculemedi as e:
            raise Kurulamadi("imza alinamadi (%s): %s" % (ad, e))
        out[ad] = (rc, stdout_normalize(c, kok), im_modul.ozet(im), im)
    return out


def eski_fark(a, b):
    return [ad for ad in a if (a[ad][0], a[ad][1]) != (b[ad][0], b[ad][1])]


def yeni_fark(a, b):
    return [ad for ad in a if (a[ad][0], a[ad][1], a[ad][2]) != (b[ad][0], b[ad][1], b[ad][2])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default=VARSAYILAN_MOTOR)
    a = ap.parse_args()
    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not os.path.isfile(IMZA_MODUL):
        print("OLCULEMEDI: etki_imzasi.py yok: %s" % IMZA_MODUL)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok.")
        return 2
    im_modul = _imza_modulu()
    kaynak = open(motor, encoding="utf-8").read()

    print(CIZGI)
    print("ETKI IMZASI HARNESS MUTANTI — yeni yuzey masrafini hak ediyor mu?")
    print("motor: %s" % motor)
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="etkimut_")
    try:
        try:
            ref = kume_olc(motor, os.path.join(taban, "ref"), im_modul)
            ref2 = kume_olc(motor, os.path.join(taban, "ref2"), im_modul)
        except Kurulamadi as e:
            print("OLCULEMEDI: referans kol kurulamadi: %s" % e)
            return 2

        # --- TEMIZ KOL: harness'in KENDISI determinist mi? ---
        tk_eski, tk_yeni = eski_fark(ref, ref2), yeni_fark(ref, ref2)
        print("  TEMIZ KOL (ayni motor 2 kez)   eski yuzey: %s · yeni yuzey: %s"
              % ("FARK YOK" if not tk_eski else "FARK VAR %s" % tk_eski,
                 "FARK YOK" if not tk_yeni else "FARK VAR %s" % tk_yeni))
        if tk_yeni:
            print("\nOLCULEMEDI: etki imzasi determinist DEGIL. Normalize edilmemis")
            print("  degisken bir alan var. Farkli haller: %s" % tk_yeni)
            for ad in tk_yeni:
                for yol, ne in im_modul.fark(ref[ad][3], ref2[ad][3])[:5]:
                    print("    %-14s %-40s %s" % (ad, yol, ne))
            return 2

        # --- HAL KAPISI: haller ayrisiyor mu? ---
        imzalar = {(ref[ad][0], ref[ad][1], ref[ad][2]) for ad, _, _, _ in HALLER}
        print("  hal sayisi / ayrik imza        %d / %d" % (len(HALLER), len(imzalar)))
        for ad, _, _, aciklama in HALLER:
            print("     %-14s exit %s · %-3d girdi · %s"
                  % (ad, ref[ad][0], len(ref[ad][3]), aciklama))
        if len(imzalar) < len(HALLER):
            print("\nOLCULEMEDI: haller ayrismiyor — ayni dal iki kez olculuyor.")
            return 2

        print(CIZGI)
        print("  %-24s %-12s %-12s %s" % ("mutant (SESSIZ YAZIM)", "ESKI YUZEY", "YENI YUZEY", "hukum"))
        print(CIZGI)

        kazanan, bozuk, ikisi_de_kor = [], [], []
        for ad, aciklama, degisimler in MUTANTLAR:
            d = os.path.join(taban, "m_" + re.sub(r"\W+", "_", ad))
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisimler, d)
                yen = kume_olc(sab, os.path.join(d, "hal"), im_modul)
            except Kurulamadi as e:
                print("  ?  %-24s OLCULEMEDI   %s" % (ad, e))
                return 2
            e_f, y_f = eski_fark(ref, yen), yeni_fark(ref, yen)
            e_txt = "ISIRDI" if e_f else "KOR"
            y_txt = "ISIRDI" if y_f else "KOR"
            if e_f and not y_f:
                hukum = "🔴 HARNESS BOZUK (yeni yuzey eskiyi KAPSAMALI)"
                bozuk.append(ad)
            elif not e_f and y_f:
                hukum = "YENI YUZEY KAZANDI (%s)" % ",".join(y_f)
                kazanan.append(ad)
            elif e_f and y_f:
                hukum = "ikisi de gordu — yeni yuzey bu mutant icin gereksiz"
            else:
                hukum = "IKISI DE KOR"
                ikisi_de_kor.append(ad)
            print("  %s  %-24s %-12s %-12s %s"
                  % ("+" if y_f else "!", ad, e_txt, y_txt, hukum))
            if y_f:
                for yol, ne in im_modul.fark(ref[y_f[0]][3], yen[y_f[0]][3])[:3]:
                    print("        %-46s %s" % (yol, ne))

        print(CIZGI)
        if bozuk:
            print("KIRMIZI: harness BOZUK — %s mutantinda eski yuzey gordu, yeni gormedi."
                  % ", ".join(bozuk))
            print("  Yeni yuzey eskiyi KAPSAR; bu imkansiz olmali.")
            return 1
        if ikisi_de_kor:
            print("  IKISI DE KOR: %s  (gercek bosluk mu, esdeger mutant mi — ayirt et)"
                  % ", ".join(ikisi_de_kor))
        if not kazanan:
            print("KIRMIZI: hicbir mutantta yeni yuzey KAZANMADI.")
            print("  Etki imzasi bu komut icin masrafini HAK ETMIYOR. Ya mutantlar")
            print("  yeterince sessiz degil, ya da yuzey genislemesi gereksiz.")
            return 1
        print("HUKUM: etki imzasi %d/%d mutantta KAZANDI — `(exit, stdout)` yuzeyinin"
              % (len(kazanan), len(MUTANTLAR)))
        print("  ETKILI komutlarda kor oldugu OLCULDU, iddia edilmedi.")
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

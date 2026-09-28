#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAZ 0 — OTOMATIK SABOTAJ / KAPSAM ENVANTERI URETECI

Fable 5, 4. tur denetimi §3.6:
  "Sabotaj olceklenmiyor: elle yapiliyor ve yalniz YENI testlere uygulanmis.
   Olceklenmesi zor degil ... tam katalog bir gecelik isidir ve KAPSAM
   ENVANTERINI OTOMATIK URETIR."
ve §9:
  "Sen bu yontemi biliyorsun ve YENI testlere uygulamissin; ESKILERE
   uygulamamissin. Asil bosluk orada."

NE YAPAR
--------
`hafiza.py` icindeki HER `fail(...)` cagrisini (bugun 60 adet) TEK TEK devre disi
birakir ve her seferinde `isir` kosar:

  * Devre disi birakinca EN AZ BIR mutant "KACTI" diyorsa
        -> o fail() KAPSAMLI: onu olcen bir mutant var.            [KAPSAMLI]
  * Devre disi birakinca HICBIR SEY degismiyorsa (isir yine 53/53)
        -> o fail() KAPSAMSIZ: hicbir mutant onu olcmuyor.         [KAPSAMSIZ]
           Yarin o satir silinse `isir` FARK ETMEZ. Kapsam envanteri budur.
  * Sabotajli surum cokuyorsa                                      [OLCULEMEDI]

Yani bu betik "kor kapi protokolu"nu kapilarin KENDISINE degil, kapilarin
KANITLARINA uygular: bir mutantin var olmasi, dogru sinifi olctugu anlamina gelmez.

ONEMLI: `hafiza.py` DEGISTIRILMEZ. Salt-okunur girdidir; her sabotaj gecici bir
KOPYA uzerinde yapilir ve kopya sonunda silinir.

KULLANIM
--------
    python3 faz0/sabotaj.py --motor skill/scripts/hafiza.py [--is 4] [--json rapor.json]
    python3 faz0/sabotaj.py --motor skill/scripts/hafiza.py --sadece 5      # hizli deneme

CIKIS KODU
----------
    0  her fail() kapsamli (hicbir kor nokta yok)
    1  en az bir KAPSAMSIZ fail() var  (v2.4.1'de beklenen)
    2  OLCULEMEDI / kurulum hatasi

EK OLCER (`--ek-olcer <betik>`, 27 Eyl 2026 — "H1 KAPSAM" is emri, SIK A kilidi)
-------------------------------------------------------------------------------
Bayraksiz kosum BIREBIR eskisidir (hukum/sebep/cikti/JSON/cikis kodu). Bayrakla,
her sabotajli motor `isir`e EK olarak `<betik> --motor <sabotajli motor>` ile de
kosulur ve AYRI bir sutun uretir. Sozlesme:
    exit 0                                   -> KAPSAMSIZ (sabotaj KACMADI)
    exit 1 + "EK-OLCER: KACTI" + Traceback YOK -> KAPSAMLI  (en az bir kol KACTI)
    diger / cokme / zaman asimi               -> OLCULEMEDI (cokme ASLA KAPSAMLI sayilmaz)
Olcer once SABOTAJSIZ motorla kosulur: orada "KACTI" diyen olcer yalan soyluyordur
(her sabotaji KAPSAMLI sayardi) -> OLCULEMEDI, kosum durur.
Rapor UC sayiyi AYRI basar: `isir ile X/N · ek ile Y/N · birlesim Z/N`. `isir`
sutunu birlesime KATLANMAZ ve cikis kodu YALNIZ `isir` sutunundan turer:
kullanicinin kendi projesinde kosabildigi kanit `isir`dir.
"""
import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed

CIZGI = "-" * 78


# ---------------------------------------------------------------------------
# 1) fail() cagri yerlerini AST ile bul  (regex DEGIL: cok satirli cagrilar var)
# ---------------------------------------------------------------------------
def fail_cagrilari(kaynak):
    """[(no, lineno, col, end_lineno, end_col, etiket)] dondurur."""
    agac = ast.parse(kaynak)
    bulunan = []
    for d in ast.walk(agac):
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "fail":
            etiket = "?"
            if d.args and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str):
                etiket = d.args[0].value
            bulunan.append(
                {
                    "lineno": d.lineno,
                    "col": d.col_offset,
                    "end_lineno": d.end_lineno,
                    "end_col": d.end_col_offset,
                    "kapi": etiket,
                }
            )
    bulunan.sort(key=lambda x: (x["lineno"], x["col"]))
    for i, b in enumerate(bulunan):
        b["no"] = i + 1
    return bulunan


def sabote_et(kaynak, hedef):
    """Tek bir fail(...) cagrisini `None` ile degistir. Kaynagi DEGISTIRMEZ."""
    satirlar = kaynak.split("\n")
    bas_i, son_i = hedef["lineno"] - 1, hedef["end_lineno"] - 1
    if bas_i == son_i:
        s = satirlar[bas_i]
        satirlar[bas_i] = s[: hedef["col"]] + "None" + s[hedef["end_col"] :]
    else:
        bas = satirlar[bas_i][: hedef["col"]] + "None"
        son = satirlar[son_i][hedef["end_col"] :]
        satirlar[bas_i] = bas + son
        # aradaki satirlari sil (sondan basa)
        del satirlar[bas_i + 1 : son_i + 1]
    yeni = "\n".join(satirlar)
    compile(yeni, "<sabotaj>", "exec")   # sozdizimi bozulduysa burada patlar
    return yeni


# ---------------------------------------------------------------------------
# 2) Tek bir sabotajı koş
# ---------------------------------------------------------------------------
def ek_olcer_hukmu(ek_olcer, motor):
    """EK OLCER sozlesmesi (bkz. modul belgesi). Cokme ASLA KAPSAMLI sayilmaz."""
    if not motor or not os.path.isfile(motor):
        return {"ek_hukum": "OLCULEMEDI", "ek_sebep": "sabotajli motor yazilamadi",
                "ek_exit": None}
    try:
        p = subprocess.run([sys.executable, ek_olcer, "--motor", motor],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    except subprocess.TimeoutExpired:
        return {"ek_hukum": "OLCULEMEDI", "ek_sebep": "ek olcer zaman asimi (600 sn)",
                "ek_exit": None}
    cikti = (p.stdout or "") + (p.stderr or "")
    cokme = "Traceback" in cikti
    kacti = re.search(r"^EK-OLCER: KACTI\b(.*)$", cikti, re.M)
    if p.returncode == 1 and kacti and not cokme:
        return {"ek_hukum": "KAPSAMLI", "ek_sebep": "ek olcer KACTI:%s" % kacti.group(1),
                "ek_exit": 1}
    if p.returncode == 0 and not cokme:
        return {"ek_hukum": "KAPSAMSIZ", "ek_sebep": "ek olcer fark etmedi (exit 0)",
                "ek_exit": 0}
    return {"ek_hukum": "OLCULEMEDI",
            "ek_sebep": "ek olcer exit %s%s" % (p.returncode, " + Traceback" if cokme else ""),
            "ek_exit": p.returncode}


def birlesim_hukmu(isir_hukum, ek_hukum):
    if "KAPSAMLI" in (isir_hukum, ek_hukum):
        return "KAPSAMLI"
    if "OLCULEMEDI" in (isir_hukum, ek_hukum):
        return "OLCULEMEDI"
    return "KAPSAMSIZ"


def tek_kosum(args):
    """`isir` hukmu (BIREBIR eskisi) + istenirse EK OLCER sutunu. Ek olcer,
    sabotajli motor gecici dizin silinmeden ONCE kosulur."""
    kaynak, hedef, sablon_proje = args[:3]
    ek_olcer = args[3] if len(args) > 3 else ""
    gecici = tempfile.mkdtemp(prefix="sabotaj_%03d_" % hedef["no"])
    try:
        sonuc = _isir_kosumu(kaynak, hedef, sablon_proje, gecici)
        if ek_olcer:
            sonuc.update(ek_olcer_hukmu(ek_olcer, os.path.join(gecici, "hafiza.py")))
            sonuc["birlesim"] = birlesim_hukmu(sonuc["hukum"], sonuc["ek_hukum"])
        return sonuc
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def _isir_kosumu(kaynak, hedef, sablon_proje, gecici):
    """Tek sabotajin `isir` hukmu — 27 Eyl oncesi `tek_kosum` govdesinin BIREBIR
    kendisi (girinti disinda); gecici dizini artik cagiran siler."""
    try:
        bozuk = sabote_et(kaynak, hedef)
    except SyntaxError as e:
        return {**hedef, "hukum": "OLCULEMEDI", "sebep": "sozdizimi: %s" % e,
                "kacan": 0, "exit": None, "kacanlar": []}

    motor = os.path.join(gecici, "hafiza.py")
    with open(motor, "w", encoding="utf-8", newline="\n") as f:
        f.write(bozuk)

    proje = os.path.join(gecici, "p")
    shutil.copytree(sablon_proje, proje, symlinks=True)

    try:
        p = subprocess.run(
            [sys.executable, motor, "isir", "--kok", proje],
            capture_output=True, text=True, timeout=300,
        )
    except subprocess.TimeoutExpired:
        return {**hedef, "hukum": "OLCULEMEDI", "sebep": "zaman asimi (300 sn)",
                "kacan": 0, "exit": None, "kacanlar": []}

    cikti = (p.stdout or "") + (p.stderr or "")
    kacanlar = sorted(set(re.findall(r"(M-[A-Z0-9a-z_]+)\s+.*?KACTI", cikti)))
    if not kacanlar:
        kacanlar = sorted(set(m for m in re.findall(r"^\s*(M-\S+).*KACTI", cikti, re.M)))
    kacan = len(kacanlar)

    if "Traceback" in cikti:
        hukum, sebep = "OLCULEMEDI", "sabotajli surum cokuyor"
    elif kacan > 0:
        hukum, sebep = "KAPSAMLI", "%d mutant KACTI" % kacan
    else:
        hukum, sebep = "KAPSAMSIZ", "hicbir mutant fark etmedi (isir exit=%s)" % p.returncode

    return {**hedef, "hukum": hukum, "sebep": sebep, "kacan": kacan,
            "exit": p.returncode, "kacanlar": kacanlar}


# ---------------------------------------------------------------------------
# 3) Sablon proje: `derle` kosulmus olmali (yoksa M-H1b / M-DEVIR kurulamaz)
# ---------------------------------------------------------------------------
def sablon_hazirla(motor, kok):
    os.makedirs(kok, exist_ok=True)
    subprocess.run(["git", "init", "-q", kok], check=False,
                   capture_output=True)
    ad = [sys.executable, motor]
    subprocess.run(ad + ["kur", "--kok", kok, "--ad", "Sabotaj"],
                   capture_output=True, check=False)
    subprocess.run(ad + ["not", "--kok", kok, "--konu=genel-durum",
                         "--metin=sabotaj sablonu icin ilk not"],
                   capture_output=True, check=False)
    subprocess.run(ad + ["derle", "--kok", kok], capture_output=True, check=False)
    p = subprocess.run(ad + ["isir", "--kok", kok], capture_output=True, text=True, check=False)
    ozet = ""
    for s in (p.stdout or "").split("\n"):
        if s.startswith("SONUC:"):
            ozet = s.strip()
    return p.returncode, ozet


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI (ek sutun '·' '—' basar)
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    _cikti_kodlamasini_guvenceye_al()
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor", default="skill/scripts/hafiza.py")
    ap.add_argument("--is", dest="isci", type=int, default=4, help="paralel isci sayisi")
    ap.add_argument("--sadece", type=int, default=0, help="yalniz ilk N fail() (hizli deneme)")
    ap.add_argument("--json", default="", help="raporu bu dosyaya JSON olarak yaz")
    ap.add_argument("--ek-olcer", dest="ek_olcer", default="",
                    help="isir'e EK olarak her sabotajli motorla kosulan olcer betigi "
                         "(ayri sutun; cikis kodunu ETKILEMEZ)")
    a = ap.parse_args()

    motor = os.path.abspath(a.motor)
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    kaynak = open(motor, encoding="utf-8").read()
    # BAGLAM: bir kapsam raporu HANGI MOTORA ait oldugunu soylemek ZORUNDADIR.
    # Olculdu (10 Agu 2026): eski bir rapor yalnizca YOL tasiyordu; o yol artik yok
    # olan bir klonu gosteriyordu ve sayilar hangi baytlara ait bilinmiyordu.
    # "Sayi baglamsiz beyan edilmez" — yol degisir, SHA degismez.
    motor_sha = hashlib.sha256(open(motor, "rb").read()).hexdigest().upper()

    hedefler = fail_cagrilari(kaynak)
    if a.sadece:
        hedefler = hedefler[: a.sadece]

    print(CIZGI)
    print("OTOMATIK SABOTAJ — kapsam envanteri")
    print("motor      : %s" % motor)
    print("motor SHA  : %s" % motor_sha)
    print("fail() sayi: %d  (kosulacak: %d)" % (len(fail_cagrilari(kaynak)), len(hedefler)))
    print(CIZGI)

    kok = tempfile.mkdtemp(prefix="sabotaj_sablon_")
    proje = os.path.join(kok, "sablon")
    rc, ozet = sablon_hazirla(motor, proje)
    print("SABLON (sabotajsiz temel kosum): exit=%s" % rc)
    print("  %s" % ozet)
    if rc != 0:
        print("OLCULEMEDI: temel kosum zaten temiz degil; sabotaj anlamsiz.")
        shutil.rmtree(kok, ignore_errors=True)
        return 2
    ek = os.path.abspath(a.ek_olcer) if a.ek_olcer else ""
    ek_temiz = None
    if ek:
        if not os.path.isfile(ek):
            print("OLCULEMEDI: ek olcer yok: %s" % ek)
            shutil.rmtree(kok, ignore_errors=True)
            return 2
        ek_temiz = ek_olcer_hukmu(ek, motor)
        print("EK OLCER   : %s (SHA %s)" % (ek, hashlib.sha256(open(ek, "rb").read()).hexdigest()[:16].upper()))
        print("  sabotajsiz motorla: %s — %s" % (ek_temiz["ek_hukum"], ek_temiz["ek_sebep"]))
        if ek_temiz["ek_hukum"] == "KAPSAMLI":
            print("OLCULEMEDI: ek olcer SABOTAJSIZ motorda 'KACTI' diyor — yalan soyleyen olcer "
                  "her sabotaji KAPSAMLI sayardi.")
            shutil.rmtree(kok, ignore_errors=True)
            return 2
    print(CIZGI)

    sonuclar = []
    try:
        with ProcessPoolExecutor(max_workers=a.isci) as ex:
            isler = {ex.submit(tek_kosum, (kaynak, h, proje, ek) if ek else (kaynak, h, proje)): h
                     for h in hedefler}
            for fut in as_completed(isler):
                r = fut.result()
                sonuclar.append(r)
                im = {"KAPSAMLI": "+", "KAPSAMSIZ": "!", "OLCULEMEDI": "?"}[r["hukum"]]
                if ek:
                    print("  %s  #%02d  satir %-5d  %-8s %-11s | ek: %-10s %s"
                          % (im, r["no"], r["lineno"], r["kapi"], r["hukum"], r["ek_hukum"],
                             ",".join(r["kacanlar"][:4]) or r["sebep"]))
                else:
                    print("  %s  #%02d  satir %-5d  %-8s %-11s %s"
                          % (im, r["no"], r["lineno"], r["kapi"], r["hukum"],
                             ",".join(r["kacanlar"][:4]) or r["sebep"]))
                sys.stdout.flush()
    finally:
        shutil.rmtree(kok, ignore_errors=True)

    sonuclar.sort(key=lambda x: x["no"])
    kapsamli = [r for r in sonuclar if r["hukum"] == "KAPSAMLI"]
    kapsamsiz = [r for r in sonuclar if r["hukum"] == "KAPSAMSIZ"]
    olculemedi = [r for r in sonuclar if r["hukum"] == "OLCULEMEDI"]

    print(CIZGI)
    print("KAPSAM ENVANTERI")
    print("  KAPSAMLI   : %d" % len(kapsamli))
    print("  KAPSAMSIZ  : %d   <-- bu satirlar silinse `isir` FARK ETMEZ" % len(kapsamsiz))
    print("  OLCULEMEDI : %d" % len(olculemedi))
    if kapsamsiz:
        print()
        print("  KAPSAMSIZ fail() cagrilari (kapi -> satir):")
        for r in kapsamsiz:
            print("    %-8s satir %d" % (r["kapi"], r["lineno"]))
    print(CIZGI)
    ek_ozet = None
    if ek:
        n = len(sonuclar)
        say = lambda alan, h: sum(1 for r in sonuclar if r[alan] == h)
        ek_ozet = {"toplam": n,
                   "isir_kapsamli": len(kapsamli),
                   "ek_kapsamli": say("ek_hukum", "KAPSAMLI"),
                   "ek_kapsamsiz": say("ek_hukum", "KAPSAMSIZ"),
                   "ek_olculemedi": say("ek_hukum", "OLCULEMEDI"),
                   "birlesim_kapsamli": say("birlesim", "KAPSAMLI")}
        print("UC SUTUN (isir sutunu birlesime KATLANMAZ; cikis kodu yalniz isir'den):")
        print("  isir ile %d/%d · ek ile %d/%d · birlesim %d/%d"
              % (ek_ozet["isir_kapsamli"], n, ek_ozet["ek_kapsamli"], n,
                 ek_ozet["birlesim_kapsamli"], n))
        print("  ek sutunu: KAPSAMLI %d · KAPSAMSIZ %d · OLCULEMEDI %d"
              % (ek_ozet["ek_kapsamli"], ek_ozet["ek_kapsamsiz"], ek_ozet["ek_olculemedi"]))
        yalniz_ek = [r for r in sonuclar if r["ek_hukum"] == "KAPSAMLI" and r["hukum"] != "KAPSAMLI"]
        if yalniz_ek:
            print("  YALNIZ ek olcerle kapsanan (isir'de KOR kalan) fail() cagrilari:")
            for r in yalniz_ek:
                print("    #%02d %-8s satir %d  (%s)" % (r["no"], r["kapi"], r["lineno"], r["ek_sebep"]))
        print(CIZGI)

    if a.json:
        # H16-BRIEF §3.1 (17 Agu 2026): `motor` alani bir YOL yaziyordu; yol
        # tasinabilir/kopyalanabilir/silinebilir, kimlik degildir. OLCULDU:
        # eski bir raporun `motor` yolu artik yok olan bir kopyayi gosteriyordu
        # ve sayilarin HANGI baytlara ait oldugu dosya ADINDAKI kisa SHA'dan
        # baska hicbir yerden anlasilamiyordu. `motor` artik SHA256 tasir; yol
        # (hata ayiklama icin faydali) `motor_yolu` altina TASINDI, kaybolmadi.
        rapor = {"motor": motor_sha, "motor_yolu": motor,
                 "fail_sayisi": len(fail_cagrilari(kaynak)),
                 "sonuclar": sonuclar}
        if ek:           # bayraksiz JSON BIREBIR eskisi kalir (yalniz bayrakla alan eklenir)
            rapor["ek_olcer"] = {"yol": ek,
                                 "sha": hashlib.sha256(open(ek, "rb").read()).hexdigest().upper(),
                                 "sabotajsiz_motorla": ek_temiz, "ozet": ek_ozet}
        with open(a.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rapor, f, ensure_ascii=False, indent=2)
        print("JSON rapor: %s" % a.json)

    if olculemedi and not kapsamsiz:
        print("HUKUM: OLCULEMEDI kalemler var — 'tam kapsamli' DEMEK YASAK.")
        return 2
    if kapsamsiz:
        print("HUKUM: %d KOR NOKTA var." % len(kapsamsiz))
        return 1
    print("HUKUM: her fail() en az bir mutantla kapsanmis.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

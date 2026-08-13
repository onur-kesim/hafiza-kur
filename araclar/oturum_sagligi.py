#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OTURUM SAGLIGI — bir Claude oturumunun KULLANDIGI token'i olcer.

NE OLCER, NE OLCMEZ
-------------------
Bu arac **yalnizca KULLANILANI** olcer. TAVANI olcmez, dolayisiyla **YUZDE
BASMAZ** — bir yuzde, bilinmeyen bir paydaya bolunmus bir uydurmadir. Cikti
mutlak sayidir.

🔴 FORMUL BIR POLITIKA KARARIDIR, OLCUM DEGILDIR.
Transcript dort ayri sayi tasir (girdi · cikti · cache YAZIMI · cache OKUMASI) ve
"kullanilan token" bunlarin hangi toplami oldugu bir TERCIHTIR. Bu yuzden arac
DORDUNU DE AYRI AYRI basar; esik yalnizca secilen formule uygulanir ve secilen
formul her ciktida ADIYLA yazilir. Formulu gizleyen bir arac, esigi de gizler.

Varsayilan `girdi+cikti`dir. Gerekce olculebilirdir, keyfi degil: 13 Agu 2026'da
bir oturum 469.417 ile SARI raporlandi; cache alanlari dahil edildiginde ayni
sinifta bir oturum milyonlari asiyor (olculdu: tek oturumda cache okumasi
22.521.379). 469.417'yi SARI araliginda tutan tek okuma cache HARIC olanidir.
Bu bir CIKARIMDIR ve boyle isaretlenmistir; formulu degistirmek isteyen
`--formul` ile degistirir, arac itiraz etmez ama HANGI formulle konustugunu
her seferinde yazar.

ESIKLER (politika; 5 Agu 2026'da kilitlendi — tavan iddiasi DEGILDIR)
    x < 400.000            YESIL     serbest
    400.000 <= x < 500.000 SARI      hafiza checkpoint'i
    500.000 <= x < 650.000 TURUNCU   yeni buyuk is yok, mevcut isi bitir
    x >= 650.000           KIRMIZI   DUR, devret

CIKIS KODU (proje sozlesmesi: 2 = OLCULEMEDI, PASS DEGIL)
    0 YESIL · 1 SARI · 3 TURUNCU · 4 KIRMIZI · 2 OLCULEMEDI

KULLANIM
    python3 araclar/oturum_sagligi.py                      # en yeni transcript
    python3 araclar/oturum_sagligi.py --transcript X.jsonl
    python3 araclar/oturum_sagligi.py --formul girdi+cikti --json
"""
import argparse
import glob
import json
import os
import sys

ESIKLER = [(400_000, "YESIL", 0), (500_000, "SARI", 1),
           (650_000, "TURUNCU", 3), (float("inf"), "KIRMIZI", 4)]

FORMULLER = {
    "girdi+cikti": ("input", "output"),
    "cache-haric": ("input", "output", "cache_yazimi"),
    "hepsi": ("input", "output", "cache_yazimi", "cache_okumasi"),
    "cikti": ("output",),
}

ARAMA = [os.path.expanduser("~/.claude/projects/*/*.jsonl"),
         "/root/.claude/projects/*/*.jsonl"]


def transcript_bul():
    adaylar = []
    for desen in ARAMA:
        adaylar.extend(glob.glob(desen))
    if not adaylar:
        return None
    return max(adaylar, key=os.path.getmtime)


def bilesenler(yol):
    """{bilesen: toplam} · (okunan_satir, atlanan_satir).

    Atlanan satir SAYILIR ve basilir: sessizce yutulan bir satir, eksik olculmus
    bir toplamdir ve bunu okuyanin gormesi gerekir."""
    t = {"input": 0, "output": 0, "cache_yazimi": 0, "cache_okumasi": 0}
    okunan, atlanan, kayit = 0, 0, 0
    with open(yol, encoding="utf-8", errors="replace") as f:
        for satir in f:
            satir = satir.strip()
            if not satir:
                continue
            okunan += 1
            try:
                o = json.loads(satir)
            except ValueError:
                atlanan += 1
                continue
            u = None
            if isinstance(o, dict):
                m = o.get("message")
                if isinstance(m, dict) and isinstance(m.get("usage"), dict):
                    u = m["usage"]
                elif isinstance(o.get("usage"), dict):
                    u = o["usage"]
            if not u:
                continue
            kayit += 1
            t["input"] += u.get("input_tokens") or 0
            t["output"] += u.get("output_tokens") or 0
            t["cache_yazimi"] += u.get("cache_creation_input_tokens") or 0
            t["cache_okumasi"] += u.get("cache_read_input_tokens") or 0
    return t, okunan, atlanan, kayit


def hukum(x):
    for sinir, ad, kod in ESIKLER:
        if x < sinir:
            return ad, kod
    return "KIRMIZI", 4                      # ulasilamaz; sozlesme yine de yazili


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript")
    ap.add_argument("--formul", default="girdi+cikti", choices=sorted(FORMULLER))
    ap.add_argument("--json", action="store_true", dest="js")
    a = ap.parse_args(argv)

    yol = a.transcript or transcript_bul()
    if not yol or not os.path.isfile(yol):
        # 🔴 KORUMA: bulunamayan transcript YESIL DEGILDIR. Olculemeyen bir sayi
        # hukum vermez; cagiran taraf bunu TURUNCU gibi ele almalidir.
        print("OLCULEMEDI: transcript bulunamadi (%s)" % (yol or "arama bos dondu"))
        print("  arananlar: %s" % " · ".join(ARAMA))
        return 2
    try:
        t, okunan, atlanan, kayit = bilesenler(yol)
    except OSError as e:
        print("OLCULEMEDI: transcript okunamadi: %s" % e)
        return 2
    if kayit == 0:
        print("OLCULEMEDI: dosyada tek bir usage kaydi yok: %s" % yol)
        return 2

    x = sum(t[k] for k in FORMULLER[a.formul])
    ad, kod = hukum(x)
    if a.js:
        print(json.dumps({"transcript": yol, "formul": a.formul, "kullanilan": x,
                          "hukum": ad, "bilesenler": t, "usage_kaydi": kayit,
                          "atlanan_satir": atlanan}, ensure_ascii=False, indent=2))
        return kod
    print("OTURUM SAGLIGI — %s" % yol)
    print("  usage kaydi %d · okunan satir %d · ATLANAN (bozuk) satir %d"
          % (kayit, okunan, atlanan))
    for k in ("input", "output", "cache_yazimi", "cache_okumasi"):
        print("    %-14s %12s" % (k, "{:,}".format(t[k]).replace(",", ".")))
    print("  formul      %s  ->  %s" % (a.formul, " + ".join(FORMULLER[a.formul])))
    print("  KULLANILAN  %s" % "{:,}".format(x).replace(",", "."))
    print("  HUKUM       %s   (esikler: 400k / 500k / 650k · tavan OLCULMEDI, yuzde YOK)"
          % ad)
    return kod


if __name__ == "__main__":
    sys.exit(main())

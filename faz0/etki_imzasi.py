#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETKI IMZASI — ETKILI komutlar icin gozlem yuzeyi.

NEDEN VAR
=========
Kapi mutantlarinin gozlem yuzeyi `(exit, stdout)`tir ve bu SALT-OKUNUR `kapi`
komutu icin dogrudur. `cmd_kur` / `cmd_derle` / `cmd_devral` / `cmd_bloklastir` /
`cmd_emekli` ise ETKILI komutlardir: dosya yazar, tasir, kilit alir, zincire halka
atar. Kopan bir kenar AYNI stdout'u basip DISKTE FARKLI BIR AGAC birakabilir —
ve `(exit, stdout)` yuzeyi buna YAPISAL OLARAK KORDUR. Kapi kalibini oldugu gibi
kopyalamak, kor bir kapi uretmek olurdu.

Bu modul o yuzeyi genisletir:

    ETKI IMZASI = (exit, stdout) + DISK AGACI MANIFESTOSU

Manifesto: her yol icin (goreli yol, tip, deger). Tip D/F/L. Deger dosyalarda
icerigin sha256'si, baglantilarda hedef, dizinlerde bos.

NORMALIZASYON — OLCULDU, TAHMIN EDILMEDI (14 Agu 2026)
======================================================
Iki bagimsiz `kur` kosumu (farkli kok, 2 saniye arayla) karsilastirildi. Degisen
alanlar OLCULEREK bulundu, tahmin edilmedi — ve olcum IKI ADIMDA dogruyu verdi:

    1) `_ZINCIR.jsonl` icindeki  "t": "2026-08-14T07:59:45"  damgasi
    2) ayni satirdaki  "halka"  (ve cok halkali zincirde "onceki") — bunlar
       `t`'yi de kapsayan bir hash'tir, yani zaman degisince TUREV olarak degisir

Baska HICBIR sey degismedi: `_CIPA.json`, `yuk` icindeki dosya SHA'lari, tarihler,
dosya adlari, dizin yapisi, hatta kok yolu (hicbir dosyaya gomulu degil).

Normalizasyon bu UC alanla SINIRLIDIR: `<ZAMAN>`, `<HALKA>`, `<ONCEKI>`.

🔴 DOSYA SHA'LARI NORMALIZE EDILMEZ. Kapi mutantlari stdout'ta `<SHA>` yapar
cunku orada SHA gurultudur. BURADA SHA SINYALDIR: `_CIPA.json`in `sha` alani ve
`_ZINCIR.jsonl`in `yuk` alani bu aracin tum kanit degeridir. Normalize etseydik
cipa bozulmasi ve icerik tahrifi GORUNMEZ olurdu — harness'i tam da olcmesi
gereken sinifa kor yapardik. Normalizasyon ne kadar genisse yuzey o kadar kordur:
OLCULEN kadarini normalize et, bir fazlasini DEGIL.

🔴 BUNUN BEDELI BIR KOR NOKTADIR VE GIZLENMIYOR: yalnizca `halka`/`onceki`
hash'ini bozan (girdilerine dokunmayan) bir kusur bu yuzeye GORUNMEZ. Kor nokta
KABUL EDILMEDI, OLCULDU: `cmd_etki_mutanti.py` icindeki `S-5 HALKA hash'i` mutanti
tam olarak bunu yapar ve raporda "IKISI DE KOR" satiri olarak GORUNUR. Hedef
engellemek degil, GIZLENEMEZ KILMAK. Kapatmak icin dogru yol zincir dogrulamasini
ayri bir kapiyla olcmektir — bu harness'in isi degildir.

⚠️ ILK OLCUM YANILTTI. Iki kosum ARD ARDA yapilinca FARK YOK cikti ve "tam
determinist" gorundu — ikisi de ayni SANIYEYE dustugu icin. Degisen niceligi
KESMEYEN bir determinizm olcumu HICBIR SEY olcmez. 2 saniye ara konunca gercek
gorundu; ve `halka` ancak o zaman ortaya cikti.

GUN SINIRI KAPISI
=================
Dosyalarda `bugun()` tarihi var. Referans ve mutant kosumlari gece yarisini
gecerse imzalar TARIH yuzunden ayrisir ve bu SAHTE bir fark olur. Bu yuzden
`imza()` tarihi basta ve sonda okur; degismisse hukum `OLCULEMEDI`dir.

BILINEN KOR NOKTA (v1, gizlenmiyor)
===================================
Dosya IZINLERI (mode) imzaya GIRMIYOR. Gerekce: umask ve platform farki gurultu
uretir, Windows'ta zaten anlamsizdir. Sonuc: yalnizca izin bitlerini degistiren
bir kusur bu yuzeye GORUNMEZ. Bu bir eksiklik olarak KAYITLIDIR; kapatilirsa
once mutantla olculmelidir.

CIKIS KODU  0 imza uretildi · 2 OLCULEMEDI (kok yok / gun siniri asildi)
"""
import argparse
import datetime as _dt
import hashlib
import os
import re
import sys


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

ATLA = {".git"}
RE_ZAMAN = re.compile(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
# `halka` ve `onceki` ZAMANI kapsayan hash'lerdir; zaman degisince turev olarak
# degisirler. Alan ADIYLA hedeflenir — "her 64 haneli hex" gibi genis bir kalip
# `yuk` icindeki DOSYA SHA'larini da yutardi ve harness'i asil sinyaline kor
# yapardi. Dar hedefle: yalniz bu iki alanin DEGERI.
RE_HALKA = re.compile(rb'("halka":\s*")[0-9A-Fa-f]{16,}(")')
RE_ONCEKI = re.compile(rb'("onceki":\s*")[0-9A-Fa-f]{16,}(")')


class Olculemedi(Exception):
    """Imza uretilemedi — 'temiz' DEGIL, ayri bir hukum."""


def normalize(ham):
    """UC kalip, hepsi OLCULEREK secildi: zaman damgasi ve ondan TUREYEN iki hash.
    Dosya SHA'larina DOKUNULMAZ — onlar sinyaldir, gurultu degil."""
    m = RE_ZAMAN.sub(b"<ZAMAN>", ham)
    m = RE_HALKA.sub(rb"\1<HALKA>\2", m)
    return RE_ONCEKI.sub(rb"\1<ONCEKI>\2", m)


def _deger(p):
    with open(p, "rb") as f:
        return hashlib.sha256(normalize(f.read())).hexdigest()


def imza(kok):
    """(goreli yol, tip, deger) uclulerinin SIRALI listesi."""
    kok = os.path.abspath(kok)
    if not os.path.isdir(kok):
        raise Olculemedi("kok yok ya da dizin degil: %s" % kok)
    t0 = _dt.date.today()
    out = []
    for dizin, altlar, dosyalar in os.walk(kok):
        altlar[:] = sorted(d for d in altlar if d not in ATLA)
        for d in altlar:
            p = os.path.join(dizin, d)
            rel = os.path.relpath(p, kok).replace(os.sep, "/")
            if os.path.islink(p):
                out.append((rel, "L", os.readlink(p).replace(os.sep, "/")))
            else:
                out.append((rel, "D", ""))
        for f in sorted(dosyalar):
            p = os.path.join(dizin, f)
            rel = os.path.relpath(p, kok).replace(os.sep, "/")
            try:
                if os.path.islink(p):
                    out.append((rel, "L", os.readlink(p).replace(os.sep, "/")))
                elif os.path.isfile(p):
                    out.append((rel, "F", _deger(p)))
                else:
                    out.append((rel, "?", ""))
            except OSError as e:
                out.append((rel, "!", "okunamadi: %s" % e.__class__.__name__))
    if _dt.date.today() != t0:
        raise Olculemedi("GUN SINIRI asildi (%s -> %s) — imza karsilastirilamaz"
                         % (t0, _dt.date.today()))
    out.sort()
    return out


def ozet(im):
    h = hashlib.sha256()
    for rel, tip, deger in im:
        h.update(("%s\x00%s\x00%s\x00" % (rel, tip, deger)).encode("utf-8"))
    return h.hexdigest()


def fark(a, b):
    """Iki imza arasindaki farklar: (yol, 'YOK->VAR' | 'VAR->YOK' | 'DEGISTI')."""
    ha, hb = {r: (t, d) for r, t, d in a}, {r: (t, d) for r, t, d in b}
    farklar = []
    for r in sorted(set(ha) | set(hb)):
        x, y = ha.get(r), hb.get(r)
        if x is None:
            farklar.append((r, "YOK->VAR"))
        elif y is None:
            farklar.append((r, "VAR->YOK"))
        elif x != y:
            farklar.append((r, "DEGISTI" if x[0] == y[0] else "TIP %s->%s" % (x[0], y[0])))
    return farklar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kok")
    ap.add_argument("--ozet", action="store_true", help="yalniz tek satirlik ozet SHA")
    a = ap.parse_args()
    try:
        im = imza(a.kok)
    except Olculemedi as e:
        print("OLCULEMEDI: %s" % e)
        return 2
    if a.ozet:
        print("%s  %d girdi" % (ozet(im), len(im)))
        return 0
    for rel, tip, deger in im:
        print("%s %-44s %s" % (tip, rel, deger))
    print("-" * 78)
    print("OZET %s  ·  %d girdi" % (ozet(im), len(im)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

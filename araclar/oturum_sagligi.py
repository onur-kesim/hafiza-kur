#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OTURUM SAGLIGI — bir Claude oturumunun BAGLAM DOLULUGUNU (N) olcer.

N TANIMI (global anayasa §3, birebir)
  Transcript'te `type == "assistant"` olan, `isSidechain` dogru OLMAYAN ve `message.usage` tasiyan kayitlarin
  SONUNCUSU. N = input_tokens + cache_read_input_tokens + cache_creation_input_tokens (eksik alan 0).
  output_tokens DAHIL DEGIL. Toplama YOK: N harcanan toplam degil, son ana-dongu mesajinin bagliminin
  doluluguudur (anayasadaki jq komutunun son satiriyla ayni sey).

BU DOSYA YALNIZ N BASAR. Renk, hukum, yuzde ve esikler global anayasa §3'te yasar; bu dosya onlari TASIMAZ
(tek kaynak — denetim/2026-10-03_oturum-sagligi-anayasa-tek-kaynak.md). Sebep OLCULMUSTU: ayni politika iki
yerde yaziliydi ve bayatladi; ustelik arac anayasadakinden FARKLI bir buyuklugu (kumulatif toplam, sidechain
dahil) olcuyordu.

TRANSCRIPT SECIMI
  `--transcript` verilirse o. Verilmezse ortamda `CLAUDE_CODE_SESSION_ID` varsa YALNIZ `<kimlik>.jsonl`
  (`~/.claude/projects/*/`); bulunamazsa baska oturuma DUSULMEZ, OLCULEMEDI doner. Kimlik yoksa en yeni
  `*.jsonl` (anayasa komutuyla ayni mantik).

CIKTI   stdout'a YALNIZ N (tek satir, tam sayi, ayracsiz). `--json` ek alanlari basar; renk alani YOK.
CIKIS   0 olculdu · 2 OLCULEMEDI (stdout'a hicbir sayi basilmaz, stderr'e `OLCULEMEDI: <sebep>`).
BOZUK SATIR  sayilir; `atlanan_satir > 0` ise stderr'e tek satir yazilir, N yine basilir (anayasa jq'su bozuk
  satirda coker; arac gizlemez, soyler).

KULLANIM
    python3 araclar/oturum_sagligi.py                      # bu oturumun (ya da en yeni) transcript'i
    python3 araclar/oturum_sagligi.py --transcript X.jsonl
    python3 araclar/oturum_sagligi.py --json
"""
import argparse
import glob
import json
import os
import sys

ARAMA = [os.path.join(os.path.expanduser("~"), ".claude", "projects", "*", "{AD}.jsonl"),
         "/root/.claude/projects/*/{AD}.jsonl"]


def transcript_bul(kimlik):
    """Yol | None. Kimlik VARSA yalniz `<kimlik>.jsonl` aranir (yoksa None: baska oturum OLCULMEZ); yoksa en yeni."""
    ad = glob.escape(kimlik) if kimlik else "*"
    adaylar = []
    for desen in ARAMA:
        adaylar.extend(glob.glob(desen.replace("{AD}", ad)))
    return max(adaylar, key=os.path.getmtime) if adaylar else None


def _say(v):
    """Alan tam sayiysa kendisi, degilse (eksik/null/bicim disi) 0 — anayasa jq'sundaki `// 0` karsiligi."""
    return v if isinstance(v, int) and not isinstance(v, bool) else 0


def son_kayit(yol):
    """(son nitelikli usage | None, nitelikli kayit sayisi, atlanan bozuk satir).

    Nitelikli = assistant + ana dongu (isSidechain null/false) + `message.usage` bir nesne. Bozuk JSON satiri
    SAYILIR: sessizce yutulan satir eksik bir olcumdur ve bunu okuyanin gormesi gerekir."""
    son, kayit, atlanan = None, 0, 0
    with open(yol, encoding="utf-8", errors="replace") as f:
        for satir in f:
            satir = satir.strip()
            if not satir:
                continue
            try:
                o = json.loads(satir)
            except ValueError:
                atlanan += 1
                continue
            if not isinstance(o, dict) or o.get("type") != "assistant":
                continue
            ana_dongu = o.get("isSidechain") is None or o.get("isSidechain") is False
            if not ana_dongu:
                continue
            m = o.get("message")
            u = m.get("usage") if isinstance(m, dict) else None
            if not isinstance(u, dict):
                continue
            kayit += 1
            son = u
    return son, kayit, atlanan


def baglam(u):
    """(N, input, cache_read, cache_creation). output_tokens DAHIL DEGIL (anayasa §3)."""
    i = _say(u.get("input_tokens"))
    o = _say(u.get("cache_read_input_tokens"))
    y = _say(u.get("cache_creation_input_tokens"))
    return i + o + y, i, o, y


def olculemedi(sebep):
    sys.stderr.write("OLCULEMEDI: %s\n" % sebep)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(description="Oturumun baglam doluluguunu (N) basar; renk/esik global anayasa §3'tedir.")
    ap.add_argument("--transcript", help="olculecek transcript (verilmezse oturum kimligi / en yeni)")
    ap.add_argument("--json", action="store_true", dest="js", help="N'yi bilesenleriyle JSON olarak bas")
    a = ap.parse_args(argv)

    kimlik = os.environ.get("CLAUDE_CODE_SESSION_ID") or None
    aranan = "oturum kimligi %s" % kimlik if kimlik else "en yeni transcript"
    yol = a.transcript or transcript_bul(kimlik)
    if not yol or not os.path.isfile(yol):
        return olculemedi("transcript bulunamadi: %s" % (yol or aranan))
    try:
        son, kayit, atlanan = son_kayit(yol)
    except OSError as e:
        return olculemedi("transcript okunamadi: %s" % e)
    if son is None:
        return olculemedi("nitelikli kayit yok (assistant + ana dongu + usage): %s" % yol)

    n, girdi, okuma, yazim = baglam(son)
    if atlanan:
        sys.stderr.write("UYARI: %d bozuk JSON satiri sayildi ve atlandi (anayasa jq'su bu satirda coker; arac atlar ve soyler)\n"
                         % atlanan)
    if a.js:
        print(json.dumps({"transcript": yol, "N": n, "input": girdi, "cache_read": okuma,
                          "cache_creation": yazim, "kayit": kayit, "atlanan_satir": atlanan},
                         ensure_ascii=False, indent=2))
    else:
        print(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())

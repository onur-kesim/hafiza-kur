#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ACIKLAMA SINIRI MUTANTI (besli-paket/IS_EMRI_URUN_HAZIRLIK.md KALEM 2, 30 Eyl 2026).

NEDEN VAR (olculdu 30 Eyl 2026 — claude.ai'ye GERCEK yukleme, OLCUM_30EYL_TANITIM_ONCESI_URUN.md §6)
  claude.ai bir skill'in aciklamasini KAYITTA 500. KARAKTERDE SESSIZCE KIRPIYOR: 713 karakterlik
  aciklama kayittan sonra tam 500. karakterde, kelime ortasinda bitti; uyari yok, hata yok.
  Kaybolan 213 karakter otomatik tetik KOSULUYDU (`... bulunmadiginda DEVREYE GIR`) ve oturum
  protokoluydu — Cowork'te GORUNMEZ. (Destek belgesindeki "200 karakter" siniri UYGULANMIYOR: ayni
  yuklemede olculdu.) Bu, projenin doktrininin tam karsiti bir kusurdur: GIZLENEN KAYIP.
  Claude Code'un siniri ayridir (1.536) ve bu kapidan ETKILENMEZ; TEK aciklama kalir.

KAPI (motorun `paket` komutunun uretim-sonrasi olcumunun (v) ayagi — `hafiza.py` `_paket_aciklama_ayagi`)
  SKILL.md on-maddesindeki `description` > 500 KARAKTER ise paket URETILMEZ (exit 1, dosya YOK).
  Okunamayan aciklama da KIRMIZIDIR: olculemeyen sey temiz sayilmaz.

NE OLCER — SINIR IKI TARAFTAN, UC YAML BICIMINDE
  S-0          depodaki GERCEK SKILL.md: BAGIMSIZ sayim <= 500 ve `paket` exit 0
  S-500 x3     tam 500 karakter -> exit 0 (katlanmis `>-` cok satir · tirnakli tek satir · duz tek satir)
  S-501 x3     tam 501 karakter -> exit 1, paket YOK, mesaj 501 ve 500'u anar
  S-500B       500 KARAKTER ama 500 BAYTTAN COK (Turkce harfli) -> exit 0: KARAKTER sayilir, bayt degil
  S-YOK        `description` okunamiyor -> exit 1 (olculemeyen temiz sayilmaz)
  S-CIFT       `description` IKI KEZ var (ilki kisa, ikincisi 501) -> exit 1: hangisinin gecerli
               oldugu ayristiriciya gore degisir (PyYAML sonuncuyu alir); ilkini alip YESIL demek
               sessiz kayip olurdu

MUTANTLAR (motor KOPYASINDA dizge sabotaji; hedef dizge TAM 1 kez gecmeli — h14_bolme dersi)
  M-A1 sinir 500 -> 501            -> S-501 satirlari YESIL kalir (yakalanmali)
  M-A2 sinir 500 -> 499            -> S-500 satirlari KIRMIZI olur
  M-A3 KARAKTER yerine BAYT sayar  -> S-500B KIRMIZI olur
  M-A4 okunamayan aciklama GECER   -> S-YOK YESIL kalir
  M-A5 kapi komple sokulur         -> S-501 satirlari YESIL kalir
  M-A6 yinelenen anahtarda ILKINI alir -> S-CIFT YESIL kalir
POZITIF KONTROL: temiz motorda TUM vakalar beklenen hukmu vermeli; vermezse mutant hukmu ANLAMSIZDIR.

NE OLCMEZ (hukum degil, SINIR)
  1. claude.ai'nin SAYIMINI (UTF-16 birimi mi, karakter mi) dogrudan olcmez: bu dosyanin tum
     karakterleri BMP'dedir ve ikisi ayni sayidir. BMP-disi (emoji) bir aciklama icin sayim
     OLCULMEDI.
  2. Motorun YAML ayristiricisi tam YAML DEGILDIR: blok skalar (`>`/`>-`/`|`/`|-`), tirnakli ve duz
     TEK satir desteklenir; baska her sey "okunamadi" = KIRMIZI. Bu bir SINIRDIR ve kapiyi
     gevsetmez, sikilastirir.

CIKIS KODLARI
  0  pozitif kontrol temiz VE tum mutantlar ISIRDI
  1  temiz motor beklenenden saptı, ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor/SKILL.md yok, vaka kurulamadi)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap


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
SKILL = os.path.join(KOK, "skill")
SINIR = 500
ASCII_SOZLUK = ["hafiza", "duzen", "kurar", "isletir", "karar", "gunlugu", "arsiv", "kapi", "olcer"]
TURKCE_SOZLUK = ["hafıza", "düzeni", "işletir", "şişti", "çıkış", "öğrenme", "ğüşçö", "ölçülmeyene"]


class Olculemedi(Exception):
    """Duzenegin KENDISI kurulamadi — kapi hukmu DEGIL."""


def metin(n, sozluk):
    """Tam n KARAKTERLIK, tek bosluklu, ne basta ne sonda bosluk; YAML'e zararsiz bir metin."""
    kelimeler, uz, i = [], 0, 0
    while True:
        k = sozluk[i % len(sozluk)]
        i += 1
        ek = len(k) + (1 if kelimeler else 0)
        if uz + ek > n:
            break
        kelimeler.append(k)
        uz += ek
    if not kelimeler:
        raise Olculemedi("metin(%d) kurulamadi" % n)
    kelimeler[-1] += sozluk[0][0] * (n - uz)
    s = " ".join(kelimeler)
    if len(s) != n or s != s.strip():
        raise Olculemedi("metin(%d) uzunlugu tutmadi: %d" % (n, len(s)))
    return s


def on_madde(bicim, aciklama):
    """SKILL.md on-maddesi: `katlanmis` (>- cok satir) · `tirnakli` · `duz` · `yok` (description satiri yok)."""
    if bicim == "katlanmis":
        satirlar = textwrap.wrap(aciklama, width=78, break_long_words=False, break_on_hyphens=False)
        govde = "description: >-\n" + "".join("  %s\n" % x for x in satirlar)
    elif bicim == "tirnakli":
        govde = 'description: "%s"\n' % aciklama
    elif bicim == "duz":
        govde = "description: %s\n" % aciklama
    elif bicim == "cift":
        govde = "description: kisa bir aciklama" + chr(10) + 'description: "%s"' % aciklama + chr(10)
    else:
        govde = "aciklama_degil: bir sey\n"
    return "---\nname: hafiza-kur\n%s---\n\n# Deneme\n" % govde


def bagimsiz_uzunluk(md):
    """Motordan BAGIMSIZ sayim (yalniz `>-` ya da tek satir): katlanmis satirlar tek bosluk ile
    birlestirilir. Baska bicimde None = OLCULEMEDI. PyYAML varsa capraz dogrulanir."""
    m = re.match(r"---\n(.*?)\n---\n", md.replace("\r\n", "\n"), re.S)
    if not m:
        return None
    satirlar = m.group(1).split("\n")
    for i, s in enumerate(satirlar):
        g = re.match(r"description:\s*(.*)$", s)
        if not g:
            continue
        ilk = g.group(1).strip()
        if ilk == ">-":
            parca = []
            for t in satirlar[i + 1:]:
                if t[:1] not in (" ", "\t"):
                    break
                parca.append(t.strip())
            deger = " ".join(parca)
        else:
            deger = ilk
        try:
            import yaml                                     # yalniz capraz dogrulama (gelistirme araci)
            y = yaml.safe_load(m.group(1)).get("description")
            if isinstance(y, str) and y.rstrip("\n") != deger:
                return None
        except ImportError:
            pass
        return len(deger)
    return None


def skill_kopyasi(hedef, motor_metni=None):
    shutil.copytree(SKILL, hedef, ignore=shutil.ignore_patterns("__pycache__", "deneme", ".*"))
    if motor_metni is not None:
        with open(os.path.join(hedef, "scripts", "hafiza.py"), "w", encoding="utf-8", newline="") as f:
            f.write(motor_metni)


def paket_kos(skill_dizini, cikti):
    """Kopya skill dizinindeki motorun `paket` komutunu kosar; (exit, ham cikti)."""
    p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(skill_dizini, "scripts", "hafiza.py"),
                        "paket", "--cikti", cikti], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


# ---------------------------------------------------------------------------- VAKALAR
def vakalar():
    """(ad, SKILL.md metni | None = depodaki gercek, beklenen exit, cikti icinde aranacaklar)"""
    v = [("S-0 depodaki gercek SKILL.md", None, 0, ())]
    for bicim in ("katlanmis", "tirnakli", "duz"):
        v.append(("S-500 %s" % bicim, on_madde(bicim, metin(500, ASCII_SOZLUK)), 0, ()))
        v.append(("S-501 %s" % bicim, on_madde(bicim, metin(501, ASCII_SOZLUK)), 1,
                  ("501", "500", "PAKET OLCUMU TUTMADI")))
    t = metin(500, TURKCE_SOZLUK)
    if len(t.encode("utf-8")) <= 500:
        raise Olculemedi("S-500B metni 500 baytin ustunde degil: bayt sayimi ayirt EDEMEZ")
    v.append(("S-500B coklu bayt (500 krk, %d bayt)" % len(t.encode("utf-8")), on_madde("katlanmis", t), 0, ()))
    v.append(("S-YOK aciklama okunamiyor", on_madde("yok", ""), 1, ("OKUNAMADI",)))
    v.append(("S-CIFT yinelenen description", on_madde("cift", metin(501, ASCII_SOZLUK)), 1, ("OKUNAMADI",)))
    return v


def batarya(taban, motor_metni, etiket):
    """Tum vakalari (motor_metni None = temiz) kosar. [(ad, durum, ayrinti)]; durum TAMAM | SAPTI."""
    sonuc = []
    for i, (ad, md, beklenen, aranan) in enumerate(vakalar()):
        d = os.path.join(taban, "%s-%d" % (etiket, i))
        skill_kopyasi(d, motor_metni)
        if md is not None:
            with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(md)
        cikti = os.path.join(taban, "%s-%d.skill" % (etiket, i))
        kod, ham = paket_kos(d, cikti)
        hata = []
        if kod != beklenen:
            hata.append("exit %d (%d bekleniyordu)" % (kod, beklenen))
        if beklenen == 0 and not os.path.isfile(cikti):
            hata.append("paket URETILMEDI")
        if beklenen != 0 and os.path.exists(cikti):
            hata.append("paket BIRAKILDI")
        hata += ["cikti `%s` anmiyor" % x for x in aranan if x not in ham]
        if md is None:                                        # S-0: bagimsiz sayim
            with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8", newline="") as f:
                n = bagimsiz_uzunluk(f.read())
            if n is None or n > SINIR:
                hata.append("gercek SKILL.md aciklamasi bagimsiz sayimla %s (<= %d bekleniyordu)" % (n, SINIR))
        sonuc.append((ad, "SAPTI" if hata else "TAMAM", "; ".join(hata)))
    return sonuc


# ---------------------------------------------------------------------------- MUTANTLAR
# (ad, aciklama, eski, yeni, hangi vaka(lar) SAPMALI)
MUTANTLAR = [
    ("M-A1", "sinir 500 -> 501", "_PAKET_ACIKLAMA_SINIRI = 500\n", "_PAKET_ACIKLAMA_SINIRI = 501\n", "S-501"),
    ("M-A2", "sinir 500 -> 499", "_PAKET_ACIKLAMA_SINIRI = 500\n", "_PAKET_ACIKLAMA_SINIRI = 499\n", "S-500 "),
    ("M-A3", "KARAKTER yerine BAYT sayar", "    if len(a) > _PAKET_ACIKLAMA_SINIRI:\n",
     '    if len(a.encode("utf-8")) > _PAKET_ACIKLAMA_SINIRI:\n', "S-500B"),
    ("M-A4", "okunamayan aciklama GECER", '        return "(v) SKILL.md on-maddesinden',
     '        return None; "(v) SKILL.md on-maddesinden', "S-YOK"),
    ("M-A5", "kapi komple sokulur", "def _paket_aciklama_ayagi(skill_md_bayt):\n",
     "def _paket_aciklama_ayagi(skill_md_bayt):\n    return None\n", "S-501"),
    ("M-A6", "yinelenen anahtarda ILKINI alir", "    if len(bulunan) != 1:\n", "    if not bulunan:\n", "S-CIFT"),
]


def bir_kez(m, eski):
    n = m.count(eski)
    if n != 1:
        raise Olculemedi("hedef dizge motorda %d kez geciyor (1 olmali): %r" % (n, eski[:60]))


def main():
    motor = os.path.join(SKILL, "scripts", "hafiza.py")
    if not (os.path.isfile(motor) and os.path.isfile(os.path.join(SKILL, "SKILL.md"))):
        print("SONUC: ÖLÇÜLEMEDİ — skill/ ya da motor yok.")
        return 2
    with open(motor, encoding="utf-8", newline="") as f:
        temiz_metin = f.read()
    print("=== ACIKLAMA SINIRI MUTANTI === sinir: %d karakter · platform: %s" % (SINIR, sys.platform))
    taban = tempfile.mkdtemp(prefix="aciklama-siniri-")
    try:
        try:
            temiz = batarya(taban, None, "temiz")
        except Olculemedi as e:
            print("SONUC: ÖLÇÜLEMEDİ — vaka kurulamadi: %s" % e)
            return 2
        for ad, durum, ayr in temiz:
            print("  %-42s %-6s %s" % (ad, durum, ayr))
        if any(d != "TAMAM" for _, d, _ in temiz):
            print("\nSONUC: KIRMIZI — temiz motor beklenen hukmu VERMEDI (mutant hukumleri ANLAMSIZ, koşulmadı).")
            return 1
        print("  POZITIF KONTROL : %d vaka, hepsi beklenen hukmu verdi (500 yesil · 501 kirmizi · okunamayan kirmizi)"
              % len(temiz))

        print("\n--- MUTANT SINAMASI (sinir iki taraftan) ---")
        kacan, olculemedi = [], []
        for ad, acik, eski, yeni, sapmali in MUTANTLAR:
            try:
                bir_kez(temiz_metin, eski)
                sab = temiz_metin.replace(eski, yeni, 1)
                compile(sab, "<mutant>", "exec")
                sonuc = batarya(taban, sab, ad)
            except (Olculemedi, SyntaxError) as e:
                olculemedi.append(ad)
                print("  %-5s %-28s OLCULEMEDI: %s" % (ad, acik, e))
                continue
            sapanlar = [a for a, d, _ in sonuc if d == "SAPTI"]
            if any(a.startswith(sapmali) for a in sapanlar):
                print("  %-5s %-28s -> ISIRDI ✓  (sapan vaka: %s)" % (ad, acik, "; ".join(sapanlar)))
            else:
                kacan.append(ad)
                print("  %-5s %-28s -> KACTI ✗  (beklenen %s sapmadi; sapan: %s)"
                      % (ad, acik, sapmali, "; ".join(sapanlar) or "hicbiri"))
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    if olculemedi:
        print("\nSONUC: ÖLÇÜLEMEDİ — %d mutant kurulamadi: %s" % (len(olculemedi), ", ".join(olculemedi)))
        return 2
    if kacan:
        print("\nSONUC: KAPI KOR — %d/%d mutant KACTI: %s" % (len(kacan), len(MUTANTLAR), ", ".join(kacan)))
        return 1
    print("\nSONUC: YESIL — sinir iki taraftan olculdu (500 yesil · 501 kirmizi), %d/%d mutant ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

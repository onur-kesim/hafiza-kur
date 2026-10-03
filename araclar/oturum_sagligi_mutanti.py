#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OTURUM SAGLIGI MUTANTI — olcerin kendisi ISIRIYOR mu?

`araclar/oturum_sagligi.py` global anayasa §3'teki N'yi basar (son ana-dongu assistant kaydinin
input + cache_read + cache_creation degeri). Bu dosya aracin DOGRU sayiyi basip basmadigini ve olculemeyeni
sayiyla gizlemedigini, her kusuru AYRI bir mutantla enjekte ederek olcer.

DUZENEK: gercek transcript kullanilmaz — SENTETIK jsonl uretilir. BEKLENEN N her fixture icin ELLE YAZILI
SABITTIR (asagidaki tablo); araca sorulmaz, araca bakilarak turetilmez. Cikti yalniz araca baglidir, makinenin
o anki oturumuna degil: ortamdan CLAUDE_CODE_SESSION_ID silinir, HOME gecici dizine cevrilir.

FIXTURELER   F1 duz 3 mesaj · F2 SON kayit sidechain · F3 son kayit usage'siz · F4 cache_read eksik/null alan ·
             F5 bozuk satir ortada · F6 iki transcript, ortam degiskeni ESKISINI gosteriyor · F7 bos usage nesnesi ·
             F8 `--transcript` oturum kimligine ONCELIKLI · F9 kimlik yok, en yeni mtime ·
             F10 assistant-disi kayit usage tasiyor (tip filtresi)
OLCULEMEDI   O1 transcript yok · O2 nitelikli kayit yok · O3 kimlik var ama dosyasi yok (baska oturuma DUSULMEZ)
MUTANTLAR    her biri KENDI ekseninde, ayri ayri sayilir; hedef hal(ler) BEKLENEN degeri vermemeli:
  M-S1 sidechain filtresi sokulur (F2) · M-S2 kumulatif toplama doner (F1) · M-S3 cache_read duser (F1) ·
  M-S4 output eklenir (F1) · M-S5 ilk kayit alinir, son degil (F1) · M-S6 transcript yokken sayi basar, exit 0 (O1) ·
  M-S7 bozuk satir sayaci susar (F5) · M-S8 oturum kimligi yok sayilir (F6) ·
  M-S10 tip filtresi sokulur (F10; bagimsiz dogrulayicinin buldugu yanlis-olumlu sinifi, ek mutant) ·
  M-S9 renk/esik tablosu kaynaga GERI GIRER: yalniz KAYNAK TARAMASI isirir (fixture'lar degismez; tarama
  sozcukleri asagidaki TEK satirdadir, sayi aranmaz — sayi yazmak zaten yasak)
TEMIZ KOL KOLLARI  aracin icine degil, temiz kolun KENDI hukmune sabotaj (git yok, sabit sabotaj):
  M-S11 yol basan arac -> temiz kol HATALI + exit 1 verir, OLCULEMEDI/exit 2 DEGIL (iki bicim: TAM yol · yolun son
        iki parcasi; sonuc metinleri `[:40]` ile kesildigi icin yalniz ikincisi kok uzunlugundan bagimsiz isirir) ·
  M-S12 hukmu t2 kosusunda degisen arac -> OLCULEMEDI + exit 2 (determinizm bekcisi yasiyor; M-S11 duzeltmesinin
        pozitif kontrolu: karsilastirma METINDEN HUKME indi, gevsetilen kontrol hala isiriyor mu)
DETERMINIZM  temiz kol iki kosu (t1/t2) yapar; karsilastirilan sey hal -> sapma VAR/YOK'tur, sonuc METNI degil —
             metin kosuya ozgu gecici yolu tasiyabilir ve yol basan bir arac regresyonu sahte OLCULEMEDI olurdu
CAPRAZ       `jq` varsa her fixture'da anayasadaki jq suzgeci == arac N (POSIX'te F6 icin anayasanin TAM komutu);
             jq yoksa satir `OLCULEMEDI (jq yok)` der, temiz DEMEZ. F5'te jq bozuk satirda COKER (anayasa komutunun
             bilinen siniri): orada esitlik beklenmez, jq'nun cokmesi ve aracin N'yi yine basmasi BEKLENEN sapmadir.

CIKIS KODU   0 hepsi isirdi, temiz kolda 0 yanlis-pozitif · 1 en az bir mutant KACTI ya da temiz kol sapti ·
             2 OLCULEMEDI (arac yok, duzenek determinist degil)
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARAC = os.path.join(KOK, "araclar", "oturum_sagligi.py")
CIZGI = "-" * 84
JSON_ALANLARI = {"transcript", "N", "input", "cache_read", "cache_creation", "kayit", "atlanan_satir"}

# --- M-S9: kaynak taramasi (renk/esik sozcukleri TEK yerde) ---
TARAMA_SOZCUKLERI = ("ESIK", "YESIL", "SARI", "TURUNCU", "KIRMIZI")

# --- anayasa §3 jq suzgeci (birebir) ---
ANAYASA_JQ = ('select(type=="object" and .type=="assistant" and (.isSidechain|not) and .message.usage!=null)'
              '|.message.usage|((.input_tokens//0)+(.cache_read_input_tokens//0)+(.cache_creation_input_tokens//0))')
ANAYASA_KOMUT = ('f=$(ls -t ~/.claude/projects/*/${CLAUDE_CODE_SESSION_ID:-*}.jsonl | head -1); '
                 'jq -r "$ANAYASA_JQ" $f | tail -1')


def _cikti_kodlamasini_guvenceye_al():          # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()


# ------------------------------------------------------------------ fixture uretimi
def asistan(i=None, cr=None, cc=None, out=None, yan=False, usage=True, ham=None):
    u = dict(ham) if ham is not None else {}
    for k, v in (("input_tokens", i), ("cache_read_input_tokens", cr),
                 ("cache_creation_input_tokens", cc), ("output_tokens", out)):
        if v is not None:
            u[k] = v
    m = {"role": "assistant", "content": "x"}
    if usage:
        m["usage"] = u
    k = {"type": "assistant", "message": m}
    if yan:
        k["isSidechain"] = True
    return json.dumps(k)


KULLANICI = json.dumps({"type": "user", "message": {"content": "x"}})
ARAC_SONUCU = json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "content": "y"}]}})
BOZUK = "{bu satir bozuk"
SISTEM_KAYDI = json.dumps({"type": "system", "message": {"usage": {
    "input_tokens": 1000000, "cache_read_input_tokens": 1000000, "cache_creation_input_tokens": 1000000}}})

# (ad, aciklama, satirlar, BEKLENEN N, input, cache_read, cache_creation, kayit, atlanan_satir) — ELLE YAZILI
FIXTURELER = [
    ("F1", "duz 3 mesaj", [KULLANICI, asistan(10, 100, 1000, 5), asistan(20, 200, 2000, 7), asistan(30, 300, 3000, 9)],
     3330, 30, 300, 3000, 3, 0),
    ("F2", "SON kayit sidechain", [KULLANICI, asistan(11, 111, 1111, 1), asistan(9, 900000, 5, 2, yan=True)],
     1233, 11, 111, 1111, 1, 0),
    ("F3", "son kayit usage'siz", [asistan(5, 50, 500, 1), KULLANICI, asistan(usage=False), ARAC_SONUCU],
     555, 5, 50, 500, 1, 0),
    ("F4", "cache_read eksik/null alan", [asistan(1, 1000, 10, 3),
                                          asistan(7, None, 70, 999, ham={"cache_read_input_tokens": None})],
     77, 7, 0, 70, 2, 0),
    ("F5", "bozuk satir ortada", [asistan(3, 30, 300, 1), BOZUK, asistan(4, 40, 400, 2)],
     444, 4, 40, 400, 2, 1),
    ("F7", "bos usage nesnesi", [asistan(8, 80, 800, 1), asistan(ham={})],
     0, 0, 0, 0, 2, 0),
    ("F10", "assistant-disi kayit usage tasiyor", [asistan(6, 60, 600, 1), SISTEM_KAYDI],
     666, 6, 60, 600, 1, 0),
]
# F6/F8/F9: iki transcript (A eski, B yeni); (ad, aciklama, kimlik, args, N, input, cache_read, cache_creation)
KIMLIK_A, KIMLIK_B = "aaaaaaaa-1111", "bbbbbbbb-2222"
SATIR_A, SATIR_B = [asistan(1, 10, 100, 5)], [asistan(2, 20, 200, 5)]
IKILI = [
    ("F6", "kimlik ESKI transcript'i gosteriyor", KIMLIK_A, (), 111, 1, 10, 100),
    ("F8", "--transcript kimlige ONCELIKLI", KIMLIK_A, ("--transcript", "{B}"), 222, 2, 20, 200),
    ("F9", "kimlik yok: en yeni mtime", None, (), 222, 2, 20, 200),
]
OLCULEMEDI_HALLERI = ["O1", "O2", "O3"]


KOK_TRANSCRIPT_VAR = bool(glob.glob("/root/.claude/projects/*/*.jsonl"))   # arac /root'u da arar: F9 izole EDILEMEZ


def kos(arac, args, ortam):
    env = dict(os.environ)
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    env.update(ortam)
    r = subprocess.run([sys.executable, "-X", "utf8", arac] + list(args), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120, env=env)
    return r.returncode, r.stdout or "", r.stderr or ""


def duzenek_kur(taban):
    """Fixture dosyalari + iki transcriptli sahte HOME. {ad: yol} ve ortam sozlugu doner."""
    os.makedirs(taban, exist_ok=True)
    yollar = {}
    for ad, _a, satirlar, *_ in FIXTURELER:
        yollar[ad] = os.path.join(taban, ad + ".jsonl")
        with open(yollar[ad], "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(satirlar) + "\n")
    yollar["O2"] = os.path.join(taban, "O2.jsonl")
    with open(yollar["O2"], "w", encoding="utf-8", newline="\n") as f:
        f.write(KULLANICI + "\n" + ARAC_SONUCU + "\n")
    home = os.path.join(taban, "ev")
    for proje, kimlik, satirlar, yas in (("proje1", KIMLIK_A, SATIR_A, 1000), ("proje2", KIMLIK_B, SATIR_B, 0)):
        d = os.path.join(home, ".claude", "projects", proje)
        os.makedirs(d)
        p = os.path.join(d, kimlik + ".jsonl")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(satirlar) + "\n")
        t = time.time() - yas
        os.utime(p, (t, t))
        yollar[kimlik] = p
    return yollar, {"HOME": home, "USERPROFILE": home}


def sayi_hatasi(ad, rc, out, err, n, atl=0):
    """Tek calistirmanin stdout/stderr/exit sozlesmesini BEKLENEN n'ye karsi olcer; sapma listesi."""
    h = []
    if rc != 0:
        h.append("%s exit %d (0 bekleniyordu)" % (ad, rc))
    elif not re.fullmatch(r"\d+\n", out):
        h.append("%s stdout YALNIZ tek satir tam sayi degil: %r" % (ad, out[:40]))
    elif int(out) != n:
        h.append("%s N=%s (beklenen %d)" % (ad, out.strip(), n))
    if atl and not re.search(r"UYARI: %d bozuk" % atl, err):
        h.append("%s stderr'de bozuk-satir uyarisi YOK" % ad)
    if not atl and err.strip():
        h.append("%s stderr bos olmaliydi: %r" % (ad, err[:40]))
    return h


def json_hatasi(ad, rc, out, bek):
    """`--json` alanlari: tam kume (renk alani YOK) ve elle yazili degerler. bek = (N, girdi, okuma, yazim, kayit, atl)."""
    try:
        d = json.loads(out)
    except ValueError:
        return ["%s --json cikti JSON degil (exit %d)" % (ad, rc)]
    h = []
    if set(d) != JSON_ALANLARI:
        h.append("%s --json alan kumesi %s" % (ad, sorted(set(d) ^ JSON_ALANLARI)))
    got = (d.get("N"), d.get("input"), d.get("cache_read"), d.get("cache_creation"), d.get("kayit"), d.get("atlanan_satir"))
    if got != bek:
        h.append("%s --json %s (beklenen %s)" % (ad, got, bek))
    return h


def olculemedi_hatasi(ad, rc, out, err):
    h = []
    if rc != 2:
        h.append("%s exit %d (2 bekleniyordu)" % (ad, rc))
    if re.search(r"\d", out):
        h.append("%s stdout'a SAYI basti: %r" % (ad, out[:40]))
    if not err.startswith("OLCULEMEDI:"):
        h.append("%s stderr 'OLCULEMEDI:' ile baslamiyor: %r" % (ad, err[:50]))
    return h


def haller_olc(arac, taban):
    """{hal: [sapma, ...]} — BEKLENEN degerler yukaridaki ELLE YAZILI tablolardandir."""
    yollar, ev = duzenek_kur(taban)
    sonuc = {}
    for ad, _a, _s, n, g, o, y, kayit, atl in FIXTURELER:
        rc, out, err = kos(arac, ["--transcript", yollar[ad]], ev)
        h = sayi_hatasi(ad, rc, out, err, n, atl)
        rc, out, err = kos(arac, ["--transcript", yollar[ad], "--json"], ev)
        sonuc[ad] = h + json_hatasi(ad, rc, out, (n, g, o, y, kayit, atl))
    for ad, _a, kimlik, args, n, g, o, y in IKILI:
        if ad == "F9" and KOK_TRANSCRIPT_VAR:
            sonuc[ad] = []          # ATLANDI (main'de SINIRLI diye bildirilir)
            continue
        ortam = dict(ev, **({"CLAUDE_CODE_SESSION_ID": kimlik} if kimlik else {}))
        args = [yollar[KIMLIK_B] if x == "{B}" else x for x in args]
        rc, out, err = kos(arac, args, ortam)
        h = sayi_hatasi(ad, rc, out, err, n)
        rc, out, err = kos(arac, args + ["--json"], ortam)
        sonuc[ad] = h + json_hatasi(ad, rc, out, (n, g, o, y, 1, 0))
    rc, out, err = kos(arac, ["--transcript", os.path.join(taban, "olmayan.jsonl")], ev)
    sonuc["O1"] = olculemedi_hatasi("O1", rc, out, err)
    rc, out, err = kos(arac, ["--transcript", yollar["O2"]], ev)
    sonuc["O2"] = olculemedi_hatasi("O2", rc, out, err)
    rc, out, err = kos(arac, [], dict(ev, CLAUDE_CODE_SESSION_ID="yok-boyle-bir-kimlik"))
    sonuc["O3"] = olculemedi_hatasi("O3", rc, out, err)
    return sonuc


def kaynak_tarama(metin):
    return sorted(s for s in TARAMA_SOZCUKLERI if s in metin)


def hukmu_ayrisan(bir, iki):
    """Hukmu (sapma VAR/YOK) iki kosumda AYRISAN haller. Sonuc METINLERI karsilastirilmaz: metin `%r` ile ve `[:40]`
    kesmesiyle kosuya ozgu gecici yolu (`t1`/`t2`) tasiyabilir; yol basan her arac regresyonu HATALI yerine sahte
    OLCULEMEDI olurdu. Normalize etmek yerine hukme inmek, yolun HER bicimine (ham · repr · json · realpath · kesik)
    dayanir; mutant hukumleri de yalniz bu VAR/YOK'tan okunur."""
    return sorted(h for h in set(bir) | set(iki) if (h in bir) != (h in iki) or bool(bir.get(h)) != bool(iki.get(h)))


def temiz_kol(arac, kaynak, taban):
    """Temiz kol HUKMU: (kod, satirlar). kod 0 temiz · 1 HATALI · 2 OLCULEMEDI; `satirlar` sirasiyla basilacak metin.
    main (gercek arac) ve M-S11 (yol sabotaji kolu) AYNI fonksiyonu kosar: kolun hukmu gercek kolun hukmuyle ayni koddan gelir."""
    bir = haller_olc(arac, os.path.join(taban, "t1"))
    iki = haller_olc(arac, os.path.join(taban, "t2"))
    ayrisan = hukmu_ayrisan(bir, iki)
    if ayrisan:
        return 2, ["OLCULEMEDI: duzenek determinist degil — hukmu iki kosumda ayrisan hal: %s." % ",".join(ayrisan)]
    sapan = {h: s for h, s in bir.items() if s}
    taramada = kaynak_tarama(kaynak)
    satirlar = ["  temiz kol: %d hal (%d fixture + %d olculemedi hali) · BEKLENEN N elle yazili · yanlis-pozitif: %d"
                % (len(bir), len(bir) - len(OLCULEMEDI_HALLERI), len(OLCULEMEDI_HALLERI), len(sapan))]
    if sapan or taramada:
        for h, s in sorted(sapan.items()):
            satirlar.append("  ! %s: %s" % (h, "; ".join(s)[:300]))
        if taramada:
            satirlar.append("  ! kaynak taramasi temiz degil: %s" % ", ".join(taramada))
        satirlar.append("\nSONUC: HATALI — temiz aracta yanlis-pozitif; mutant hukumleri anlamsiz.")
        return 1, satirlar
    satirlar.append("  kaynak taramasi: temiz (renk/esik sozcugu yok)")
    if KOK_TRANSCRIPT_VAR:
        satirlar.append("  F9: ATLANDI (SINIRLI) — /root/.claude altinda transcript var; arac /root'u da arar, en-yeni-mtime hali izole edilemez")
    return 0, satirlar


def temiz_kol_kolu(kaynak, sabotajlar, bekleneni, onek):
    """M-S11/M-S12: (isirdi | None, ayrinti). None = sabotaj kurulamadi (OLCULEMEDI). Isirdi = HER bicimde temiz kol
    `bekleneni` (exit kodu) ve `onek` ile baslayan hukum satirini verdi; baska kod ya da satir KACTI'dir.
    Her sabotaj KENDI mkdtemp kokunde kosar: t1/t2 gercek temiz kolla AYNI derinlikte (`<kok>/t1`). Tabana gomulu
    (`<taban>/M-S11a/t1`) kurulsaydi yol bir seviye uzar ve (a) hicbir platformda `[:40]` penceresine ulasmazdi."""
    ayrinti, isirdi = [], True
    for harf, _aciklama, yeni in sabotajlar:
        metin, hata = mutant_metni(kaynak, [(PRINT_N, yeni)])
        if hata:
            return None, "%s: %s" % (harf, hata)
        kok = tempfile.mkdtemp(prefix="sagmut_")
        try:
            sab = os.path.join(kok, "oturum_sagligi.py")
            with open(sab, "w", encoding="utf-8", newline="\n") as f:
                f.write(metin)
            kod, satirlar = temiz_kol(sab, metin, kok)
        finally:
            shutil.rmtree(kok, ignore_errors=True)
        tuttu = kod == bekleneni and any(s.lstrip("\n").startswith(onek) for s in satirlar)
        isirdi = isirdi and tuttu
        ayrinti.append("%s: exit %d %s%s" % (harf, kod, HUKUM_ADI.get(kod, "?"),
                                           "" if tuttu else " (%s + exit %d bekleniyordu)" % (HUKUM_ADI[bekleneni], bekleneni)))
    return isirdi, " · ".join(ayrinti)


# ------------------------------------------------------------------ mutantlar
# (ad, aciklama, [(eski, yeni)], hedef haller) — `eski` aracta TAM 1 kez gecmeli
SON_U = "            son = u\n"
DONUS = "    return i + o + y, i, o, y\n"
MUTANTLAR = [
    ("M-S1", "sidechain filtresi sokulur (son kayit sidechain ise o alinir)",
     [('            ana_dongu = o.get("isSidechain") is None or o.get("isSidechain") is False\n',
       "            ana_dongu = True\n")], ["F2"]),
    ("M-S2", "kumulatif toplama doner (son kayit degil, hepsinin toplami)",
     [(SON_U, '            son = {k: (son or {}).get(k, 0) + _say(u.get(k)) for k in '
              '("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")}\n')], ["F1"]),
    ("M-S3", "cache_read N'den duser", [(DONUS, "    return i + y, i, o, y\n")], ["F1"]),
    ("M-S4", "output_tokens N'ye eklenir",
     [(DONUS, '    return i + o + y + _say(u.get("output_tokens")), i, o, y\n')], ["F1"]),
    ("M-S5", "ILK kayit alinir (son degil)", [(SON_U, "            son = u if son is None else son\n")], ["F1"]),
    ("M-S6", "transcript yokken sayi basar ve exit 0 doner",
     [('        return olculemedi("transcript bulunamadi: %s" % (yol or aranan))\n',
       "        print(0)\n        return 0\n")], ["O1"]),
    ("M-S7", "bozuk satir sayaci susar (eksik olcum gorunmez)",
     [("                atlanan += 1\n", "                pass\n")], ["F5"]),
    ("M-S8", "oturum kimligi yok sayilir (en yeni mtime)",
     [('    ad = glob.escape(kimlik) if kimlik else "*"\n', '    ad = "*"\n')], ["F6"]),
]
MUTANTLAR.append(
    ("M-S10", "tip filtresi sokulur (assistant-disi kayit usage tasiyorsa o alinir)",
     [('            if not isinstance(o, dict) or o.get("type") != "assistant":' + chr(10),
       "            if not isinstance(o, dict):" + chr(10))], ["F10"]))
# M-S9 kaynak mutanti: tabloyu aracin SONUNA ekler (davranis degismez); yalniz tarama gorur
M_S9 = ("M-S9", "renk/esik tablosu kaynaga GERI GIRER (davranis ayni, yalniz KAYNAK TARAMASI gorur)")
# TEMIZ KOL KOLLARI (M-S11, M-S12): aracin ICINE degil, temiz kolun KENDI hukmune sabotaj. Sabittir: git yok, eski
# surume bagimlilik yok. Her sabotaj `print(n)` satirini degistirir; (ad, aciklama, [(harf, aciklama, yeni satir)],
# BEKLENEN kod, hukum satirinin on eki).
#   M-S11  yol basan arac -> HATALI + exit 1 (OLCULEMEDI/exit 2 DEGIL). Iki bicim: (a) eski aracin basligi gibi TAM yol;
#          (b) yolun yalniz son iki parcasi. Sonuc metinleri `[:40]` ile kesildiginden TAM yol ancak kisa kokte (Linux
#          /tmp) penceredeki t1/t2 farkina ulasir; (b) kok uzunlugundan BAGIMSIZ ulasir (yol uzunlugu bir olcum eksenidir).
#   M-S12  hukmu t2 kosusunda DEGISEN arac -> OLCULEMEDI + exit 2: M-S11'in duzeltmesi karsilastirmayi METINDEN
#          HUKME indirdi; bekci YASIYOR mu (gevsetilen kontrolun hala isirdigi) pozitif kontroluyle olculur.
PRINT_N = "        print(n)\n"
TEMIZ_KOL_KOLLARI = [
    ("M-S11", "yol basan arac HATALI + exit 1 vermeli",
     [("a", "TAM yol (eski aracin basligi gibi)", '        print("OTURUM SAGLIGI: %s" % yol)\n' + PRINT_N),
      ("b", "yolun yalniz SON IKI parcasi (kok uzunlugundan bagimsiz)",
       '        print("%s/%s" % (os.path.basename(os.path.dirname(yol)), os.path.basename(yol)))\n' + PRINT_N)],
     1, "SONUC: HATALI"),
    ("M-S12", "hukmu kosuya gore degisen arac OLCULEMEDI + exit 2 vermeli (determinizm bekcisi yasiyor)",
     [("t2", "yalniz t2 kosusunda N yanlis", '        print(n + int((os.sep + "t2" + os.sep) in yol))\n')],
     2, "OLCULEMEDI: duzenek determinist degil"),
]
HUKUM_ADI = {0: "TEMIZ", 1: "HATALI", 2: "OLCULEMEDI"}


def mutant_metni(kaynak, degisimler):
    metin = kaynak
    for eski, yeni in degisimler:
        if metin.count(eski) != 1:
            return None, "hedef dizge %d kez gecti" % metin.count(eski)
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "derlenmiyor: %s" % e
    return metin, None


# ------------------------------------------------------------------ jq capraz kontrolu
def jq_var():
    return shutil.which("jq") is not None


def jq_n(yol):
    """Anayasa suzgeci: (exit, son satir | None)."""
    r = subprocess.run(["jq", "-r", ANAYASA_JQ, yol], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=60)
    satirlar = [x for x in (r.stdout or "").splitlines() if x.strip()]
    return r.returncode, (satirlar[-1] if satirlar else None)


def capraz_kontrol(arac, taban):
    """(satirlar, sapma_var, olculemedi_var). jq yoksa temiz DENMEZ: olculemedi_var."""
    if not jq_var():
        return ["  jq: OLCULEMEDI (jq yok) — anayasa jq'su ile capraz kontrol yapilamadi, temiz denmez"], False, True
    yollar, ev = duzenek_kur(taban)
    satirlar, sapma = [], False
    for ad, _a, _s, n, *_r, atl in FIXTURELER:
        rc, out, _e = kos(arac, ["--transcript", yollar[ad]], ev)
        jrc, jn = jq_n(yollar[ad])
        if atl:    # bozuk satir: jq COKER (anayasa komutunun bilinen siniri); arac N'yi basar ve uyarir
            ok = jrc != 0 and rc == 0 and out.strip() == str(n)
            satirlar.append("  %s: jq bozuk satirda cokuyor (exit %d, son satir %s) · arac %s + uyari -> BEKLENEN sapma %s"
                            % (ad, jrc, jn, out.strip(), "tamam" if ok else "BEKLENMEDIK"))
        else:
            ok = jrc == 0 and jn == out.strip() == str(n)
            satirlar.append("  %s: jq %s == arac %s -> %s" % (ad, jn, out.strip(), "ESIT" if ok else "FARKLI"))
        sapma = sapma or not ok
    if os.name == "nt":
        satirlar.append("  F6: OLCULEMEDI (anayasa komutu POSIX kabugu ister; Windows'ta yalniz jq suzgeci karsilastirildi)")
        return satirlar, sapma, True
    bash = shutil.which("bash")
    if not bash:
        satirlar.append("  F6: OLCULEMEDI (bash yok)")
        return satirlar, sapma, True
    r = subprocess.run([bash, "-c", ANAYASA_KOMUT], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=60, env=dict(os.environ, **ev, CLAUDE_CODE_SESSION_ID=KIMLIK_A, ANAYASA_JQ=ANAYASA_JQ))
    rc, out, _e = kos(arac, [], dict(ev, CLAUDE_CODE_SESSION_ID=KIMLIK_A))
    ok = r.stdout.strip() == out.strip() == "111"
    satirlar.append("  F6: anayasanin TAM komutu %s == arac %s -> %s" % (r.stdout.strip(), out.strip(), "ESIT" if ok else "FARKLI"))
    return satirlar, sapma or not ok, False


def main():
    if not os.path.isfile(ARAC):
        print("OLCULEMEDI: arac yok: %s" % ARAC)
        return 2
    kaynak = open(ARAC, encoding="utf-8", newline="").read()
    taban = tempfile.mkdtemp(prefix="sagmut_")
    print(CIZGI)
    print("OTURUM SAGLIGI MUTANTI — olcerin kendisi isiriyor mu?")
    print(CIZGI)
    try:
        kod, temiz = temiz_kol(ARAC, kaynak, taban)
        print("\n".join(temiz))
        if kod:
            return kod
        satirlar, jq_sapma, jq_olculemedi = capraz_kontrol(ARAC, os.path.join(taban, "t3"))
        print("  jq capraz kontrol:")
        print("\n".join(satirlar))
        if jq_sapma:
            print("\nSONUC: HATALI — arac N'si anayasa jq'sundan FARKLI.")
            return 1
        print(CIZGI)
        isirdi, kacti = [], []
        for ad, aciklama, degisimler, hedef in MUTANTLAR:
            metin, hata = mutant_metni(kaynak, degisimler)
            if hata:
                print("  ?  %-5s OLCULEMEDI  %s" % (ad, hata))
                return 2
            d = os.path.join(taban, ad)
            os.makedirs(d)
            sab = os.path.join(d, "oturum_sagligi.py")
            with open(sab, "w", encoding="utf-8", newline="\n") as f:
                f.write(metin)
            yeni = haller_olc(sab, os.path.join(d, "t"))
            sapma = sorted(h for h, s in yeni.items() if s)
            if all(h in sapma for h in hedef):
                isirdi.append(ad)
                print("  +  %-5s ISIRDI  hedef %-3s · sapan hal: %s" % (ad, ",".join(hedef), ",".join(sapma)))
            else:
                kacti.append(ad)
                print("  !  %-5s KACTI   hedef %s sapmadi (sapan: %s) -> %s" % (ad, ",".join(hedef), ",".join(sapma) or "yok", aciklama))
            sys.stdout.flush()
        # M-S9: kaynak mutanti
        ad9, acik9 = M_S9
        metin9 = kaynak + "\n_TABLO = %r\n" % (TARAMA_SOZCUKLERI,)
        compile(metin9, "<mutant>", "exec")
        d = os.path.join(taban, ad9)
        os.makedirs(d)
        sab9 = os.path.join(d, "oturum_sagligi.py")
        with open(sab9, "w", encoding="utf-8", newline="\n") as f:
            f.write(metin9)
        davranis = sorted(h for h, s in haller_olc(sab9, os.path.join(d, "t")).items() if s)
        bulunan = kaynak_tarama(metin9)
        if bulunan and not davranis:
            isirdi.append(ad9)
            print("  +  %-5s ISIRDI  hedef KAYNAK TARAMASI · bulunan: %s · fixture sapmasi: yok (ayri eksen)"
                  % (ad9, ",".join(bulunan)))
        else:
            kacti.append(ad9)
            print("  !  %-5s KACTI   tarama bulunan=%s fixture sapmasi=%s -> %s" % (ad9, bulunan or "yok", davranis or "yok", acik9))
        # M-S11/M-S12: temiz kolun KENDI hukmune sabotaj (yol basan arac · hukmu degisen arac)
        for ad, aciklama, sabotajlar, bekleneni, onek in TEMIZ_KOL_KOLLARI:
            isirdi_kol, ayrinti = temiz_kol_kolu(kaynak, sabotajlar, bekleneni, onek)
            if isirdi_kol is None:
                print("  ?  %-5s OLCULEMEDI  %s" % (ad, ayrinti))
                return 2
            if isirdi_kol:
                isirdi.append(ad)
                print("  +  %-5s ISIRDI  hedef TEMIZ KOL HUKMU · %s" % (ad, ayrinti))
            else:
                kacti.append(ad)
                print("  !  %-5s KACTI   hedef TEMIZ KOL HUKMU · %s -> %s" % (ad, ayrinti, aciklama))
            sys.stdout.flush()
    finally:
        shutil.rmtree(taban, ignore_errors=True)
    print(CIZGI)
    toplam = len(MUTANTLAR) + 1 + len(TEMIZ_KOL_KOLLARI)
    print("SONUC: %d isirdi - %d kacti (toplam %d)%s" % (len(isirdi), len(kacti), toplam,
                                                      " · jq capraz kontrol OLCULEMEDI (SINIRLI)" if jq_olculemedi else ""))
    if kacti:
        print("  KACAN mutant = olcerin KOR oldugu sinif.")
        return 1
    print("  Olcerin her maddesi olculuyor" + (" (jq capraz kontrolu HARIC: baska ortamda kosar)." if jq_olculemedi else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())

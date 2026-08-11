#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALTIN OLCUT MUTANTI — altin_cikti.py'nin UC duzeltmesi ISIRIYOR MU?

NEDEN BU DOSYA VAR
  CI #17 ve #18'de `Altin cikti / kapi esdegerligi (windows-latest)` isi kirmizi
  yandi; ubuntu ve macos yesildi. Artefakt (`altin-windows-latest/altin-fark.txt`)
  elle okundu ve sunu gosterdi (olculdu 11 Agu 2026):

      10 olcumun 10'unda  CIKTI DEGISTI
      hicbirinde          EXIT DEGISTI  YOK
      hepsinde tek satir  "(satir farki bulunamadi — bosluk/satir sonu farki olabilir)"
      hukum               "SONUC: 10 FARK — davranis DEGISTI." (exit 1)

  Yani arac bir fark GORDU ama ADLANDIRAMADI ve buna ragmen "davranis DEGISTI"
  dedi. Bu bir URUN hukmu DEGILDI: bolme (Faz C) o platformda hic olculmemisti ve
  ubuntu/macos bit-bit ayni cikiyordu. Arac KENDI kusurunu URUN regresyonu diye
  raporluyordu — tam Y-4 sinifi ("olcemedigini ARAC KUSURU diye mi raporluyor?").

  UC DUZELTME YAPILDI, ve DOKTRIN 1 aciktir: "olculmeyen kapinin hukmu YOKTUR".
  Bir OLCUT duzeltmesi de bir kapidir; isirdigi KANITLANMALIDIR.

    DUZELTME-1  kos(): `-X utf8` + `text=True, encoding="utf-8", errors="replace"`
                Cocugun ciktisi universal newline ile okunur; \\r\\n -> \\n.
                🔴 CIPLAK `text=True` COZUM DEGILDIR: kodlama ACIK verilmezse
                cozme, ust surecin VARSAYILAN kodlamasina baglanir. `LC_ALL=C`
                TEK BASINA bunu tetiklemez — PEP 540 UTF-8 kipini kendiliginden
                acar (olculdu 11 Agu 2026: `LC_ALL=C` -> utf8_mode=1). Tetikleyen
                hal `LC_ALL=C PYTHONUTF8=0`: orada ciplak `text=True` ham
                traceback'li `UnicodeDecodeError` verir ve exit 1 = "FARK VAR"
                olarak raporlanir. Teslim gunundeki ham-bayt `.decode(...)` hali
                bu sinifa ZATEN bagisikti; yani bu ayak MEVCUT bir kusuru
                kapatmaz, `text=True`'nun GETIRECEGI kusuru onler.
    DUZELTME-2  Satir duzeyinde ADLANDIRILAMAYAN fark artik OLCULEMEDI (exit 2)
                hukmudur; gorunmez karakterin SINIFI ve repr penceresi basilir.
                Neden gerekli: `splitlines()` yalniz \\r'yi degil \\x0b · \\x0c ·
                \\u2028 · \\x85 gibi TUM satir siniri karakterlerini yutar;
                universal newline ise yalniz \\r\\n'i cevirir. DUZELTME-1 sinifin
                TAMAMINI kapatmaz — M-A2 tam bu bosluktadir.
                🔴 Tabloya YALNIZ satir siniri karakterleri girer. NBSP · BOM ·
                SEKME · BOSLUK · ZWSP satir listesini DEGISTIRIR, dolayisiyla
                ADLANDIRILABILIR bir satir farki uretir ve teshise HIC ULASMAZ
                (olculdu: satir_farki("a b", "a\\xa0b") -> adlandirildi=True).
    DUZELTME-3  Referansin SEKLI kapida sinanir (_kume_sekli_dogrula): eksik alan
                ya da yanlis tur ARAC KUSURU (exit 3) olur, ham traceback + exit 1
                olmaz. M-A7 bunu olcer.

  Duzeltmelerin katkisi YALNIZ satir-sonu ceviren bir ortamda gorunur. POSIX'te
  eski olcut de "FARK YOK" der; yani duzeltme burada KENDI KORLUGUNU tekrarlar.
  Bu yuzden mutant ORTAMI URETIR (asagi bak).

ORTAM URETIMI — motora DOKUNULMAZ
  `sitecustomize.py` + `PYTHONPATH` ile COCUK SURECIN satir sonu kipi degistirilir:
      CRLF kolu        : sys.stdout.reconfigure(newline="\\r\\n")
      DIKEY SEKME kolu : write() sarmalayicisi \\n -> \\x0b
  Enjeksiyon yalniz `hafiza.py` cagrisinda devreye girer; olcum aracinin kendi
  ciktisi bozulmaz (aksi halde mutant kendi grep'ini olcerdi).
  Olculdu: motorun Y-2 korumasi (`reconfigure(encoding=…, errors=…)`) newline
  ayarini SIFIRLAMAZ — yani enjeksiyon motorun korumasindan SONRA da ayakta.

  🔴 URETILEN ORTAM GERCEK WINDOWS DEGILDIR. Burada olculen sey "hafiza.py
  Windows'ta ne basar" DEGIL, "yeni olcut, eski olcutun goremedigini goruyor mu"
  ve "gordugunu ADLANDIRABILIYOR mu"dur. Windows'un kendi hukmu CI'da olculur;
  bu dosya onun YERINE GECMEZ.

YEDI MUTANT — her biri AYRI bir korumayi olcer
  M-A1 SATIR SONU (CRLF)   : eski olcut yanlis hukum verir, yeni olcut FARK YOK der.
  M-A2 SATIR SINIRI (\\x0b) : DUZELTME-1'in kapatMADIGI sinif — yeni olcut
                             OLCULEMEDI der ve SINIFI ADLANDIRIR.
  M-A3 GERCEK FARK         : yeni siniflandirma gorunur bir regresyonu
                             OLCULEMEDI'ye CEVIRMIYOR (yutma kontrolu).
  M-A4 TEMIZ KOL           : duzeltme altin kumeyi BOZMUYOR — referansi yeniden
                             kaydetmek GEREKMIYOR.
  M-A5 KAPI DUSURME        : DUZELTME-2'nin HUKMU sokulurse GORUNUYOR mu.
  M-A6 IZ KILIDI           : DUZELTME-2'nin TESHISI sokulurse hukum AYNI kalir
                             (exit 2) ama artefakt sinifi ADLANDIRAMAZ. Hukum ile
                             iz AYRI iki korumadir; ayri ayri olculur.
  M-A7 BOZUK REFERANS      : DUZELTME-3. Bagimsiz denetci teslimden ONCE buldu:
                             sekli bozuk bir referans dosyasi farklari_bul icinde
                             KeyError/TypeError atip HAM TRACEBACK ile exit 1
                             veriyordu — yani ARAC KUSURU yine "davranis DEGISTI"
                             diye okunuyordu. Duzeltilen kusurun BASKA KAPIDAN
                             donusu. Artik sekil kapida sinanir: exit 3.

CIKIS KODLARI (proje sozlesmesi)
  0 olculen her mutant ISIRDI · 1 en az biri KACTI · 2 OLCULEMEDI · 3 ARAC KUSURU
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI (olcum araci da korunur)
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
ARAC = os.path.join(KOK, "faz0", "altin_cikti.py")
REFERANS = os.path.join(KOK, "faz0", "altin_kapi.json")
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")

ISIRDI = "ISIRDI"
KACTI = "KACTI"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []

# Motora enjekte edilen NOT DEGISIKLIGI — altin_cikti.py'nin --kendini-sina
# sabotajiyla AYNI hedef. M-A3'te "gerçek, GORUNUR fark" uretmek icin kullanilir.
SAB_ESKI = 'N.append("H13: %d seri tanimli" % len(seriler))'
SAB_YENI = 'N.append("H13: %d seri tanimlandi" % len(seriler))'


class AracKusuru(Exception):
    pass


def _degistir(metin, eski, yeni, etiket):
    """Tek eslesme + SATIR SINIRI guvencesi (fazA/fazB/fazC ile ayni ders:
    girintili bir desen satirin ORTASINA eslesirse yamalanmis kopya ARACI degil
    YAMAYI olcer)."""
    n = metin.count(eski)
    if n != 1:
        raise AracKusuru("%s: hedef metin %d kez gecti (1 olmali). Kaynak "
                         "degistiyse MUTANT DA DEGISMELIDIR." % (etiket, n))
    i = metin.index(eski)
    if eski[:1] in (" ", "\t") and i != 0 and metin[i - 1] != "\n":
        raise AracKusuru("%s: desen girinti tasiyor ama eslesme SATIR BASINDA "
                         "degil (alt-dize eslesmesi)." % etiket)
    return metin.replace(eski, yeni, 1)


# --------------------------------------------------- ESKI OLCUTU GERI GETIREN YAMALAR

def yama_eski_kos(m):
    """DUZELTME-1'i geri alir: cocugun ciktisi ham bayt olarak decode edilir,
    `\\r` KORUNUR ve `-X utf8` verilmez (teslim gunundeki hal)."""
    return _degistir(
        m,
        '        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok=" + kok],\n'
        '                           capture_output=True, timeout=saniye, env=o,\n'
        '                           text=True, encoding="utf-8", errors="replace")\n'
        '    except subprocess.TimeoutExpired:\n'
        '        return None, "ZAMAN ASIMI (%d sn)" % saniye\n'
        '    return r.returncode, (r.stdout or "") + (r.stderr or "")\n',
        '        r = subprocess.run([sys.executable, motor] + arglar + ["--kok=" + kok],\n'
        '                           capture_output=True, timeout=saniye, env=o)\n'
        '    except subprocess.TimeoutExpired:\n'
        '        return None, "ZAMAN ASIMI (%d sn)" % saniye\n'
        '    return r.returncode, (r.stdout or b"").decode("utf-8", "replace") + \\\n'
        '                         (r.stderr or b"").decode("utf-8", "replace")\n',
        "mutant/eski-kos")


ESKI_YEDEK = '"      (satir farki bulunamadi — bosluk/satir sonu farki olabilir)"'


def yama_eski_teshis(m):
    """DUZELTME-2'nin IZ ayagini geri alir: gorunmez karakterin SINIFI ve repr
    penceresi yerine teslim gunundeki yedek cumle basilir. Hukum (exit) aynidir;
    kaybolan sey ARTEFAKTIN ADLANDIRMA GUCUDUR — CI #17/#18'de tam bu kayboldu."""
    return _degistir(
        m,
        "    return gorunmez_teshis(eski, yeni), False\n",
        "    return %s, False   # MUTANT: TESHIS SOKULU\n" % ESKI_YEDEK,
        "mutant/eski-teshis")


def yama_eski_hukum(m):
    """DUZELTME-2'nin HUKUM ayagini geri alir: adlandirilamayan fark yine
    'davranis DEGISTI' (exit 1) diye raporlanir."""
    return _degistir(
        m,
        '    adsiz = [f for f in farklar if f[2] == "ADLANDIRILAMADI"]\n',
        '    adsiz = []   # MUTANT: HUKUM SOKULU\n',
        "mutant/eski-hukum")


def yama_eski_sekil(m):
    """DUZELTME-3'u geri alir: referansin SEKLI sinanmaz. Bozuk bir referans
    farklari_bul icinde KeyError/TypeError atar -> HAM TRACEBACK + exit 1."""
    return _degistir(
        m,
        '        _kume_sekli_dogrula(altin)\n'
        '    except (OSError, ValueError, KeyError, TypeError) as e:\n',
        '    except (OSError, ValueError, KeyError) as e:\n',
        "mutant/eski-sekil")


# Teslim gunundeki (commit 8e3993f) aracin ciktisini birebir ureten yama kumesi.
ESKI_TAM = [yama_eski_kos, yama_eski_teshis, yama_eski_hukum, yama_eski_sekil]


# --------------------------------------------------------------- ORTAM URETIMI

SC_CRLF = '''\
# MUTANT ORTAMI: cocuk surecin satir sonu kipi Windows metin kipi gibi davranir.
# Yalniz MOTOR cagrisinda devreye girer — olcum aracinin kendi ciktisi bozulmaz.
import sys
if any(str(a).endswith("hafiza.py") for a in sys.argv):
    for _a in (sys.stdout, sys.stderr):
        try: _a.reconfigure(newline="\\r\\n")
        except Exception: pass
'''

SC_SINIR = """\
# MUTANT ORTAMI: satir siniri karakteri \\n yerine %(ad)s.
# universal newline BUNU CEVIRMEZ -> DUZELTME-1 bu sinifi KAPATMAZ.
# splitlines() ise onu da satir siniri sayar -> satir farki GORUNMEZ.
import sys
if any(str(a).endswith("hafiza.py") for a in sys.argv):
    class _W:
        def __init__(s, t): s._t = t
        def write(s, x): return s._t.write(x.replace("\\n", %(kacis)s))
        def __getattr__(s, n): return getattr(s._t, n)
    sys.stdout = _W(sys.stdout); sys.stderr = _W(sys.stderr)
"""

# CPython str.splitlines() sinir kumesinden IKI uye. \x0b universal newline'in
# CEVIRMEDIGI klasik hal; \x85 (NEL) ise altin_cikti'nin _SINIR_ADI tablosunda
# olmasi gereken ama ilk teslimde EKSIK OLAN uye — denetci bu bosluğu buldu, o
# yuzden mutant artik IKISINI de olcer. Tek karakterle olculen bir tablo, tablonun
# geri kalanini "olculdu" sanmaya yol acar (ortusen tespit korlugu).
SINIR_HALLERI = [
    ("\\x0b", '"\\x0b"', "DIKEY SEKME (VT)"),
    ("\\x85", '"\\x85"', "SONRAKI SATIR (NEL, U+0085)"),
]
SC_VT = SC_SINIR % {"ad": "\\x0b (dikey sekme)", "kacis": '"\\x0b"'}


def ortam_kur(taban, ad, kaynak):
    d = os.path.join(taban, "ortam_" + ad)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "sitecustomize.py"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(kaynak)
    return d


# --------------------------------------------------------------- AGAC + KOSUM

def agac_kur(taban, ad, yamalar, motor_sabotaji=False, referansi_boz=False):
    """Yamalanmis ARAC + (istege gore sabotajli) motor ile calisir bir agac.
    Referans altin kume varsayilan olarak DOKUNULMADAN kopyalanir."""
    kok = os.path.join(taban, ad)
    os.makedirs(os.path.join(kok, "faz0"))
    os.makedirs(os.path.join(kok, "skill", "scripts"))

    mm = open(MOTOR, encoding="utf-8").read()
    if motor_sabotaji:
        mm = _degistir(mm, SAB_ESKI, SAB_YENI, "mutant/motor-not-degisikligi")
    with open(os.path.join(kok, "skill", "scripts", "hafiza.py"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(mm)

    hedef_ref = os.path.join(kok, "faz0", "altin_kapi.json")
    if referansi_boz:
        # M-A7 ORTAMI: gecerli JSON, BOZUK SEKIL. Kesik indirme / birlestirme
        # catismasi / elle duzenleme hepsi bu hali uretir. Ilk kaydin "exit"
        # alani silinir — farklari_bul icinde KeyError, yani HAM TRACEBACK adayi.
        d = json.load(open(REFERANS, encoding="utf-8"))
        del d["kume"][0]["exit"]
        with open(hedef_ref, "w", encoding="utf-8", newline="\n") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    else:
        shutil.copy2(REFERANS, hedef_ref)

    metin = open(ARAC, encoding="utf-8").read()
    for y in yamalar:
        metin = y(metin)
    try:
        ast.parse(metin)
    except SyntaxError as e:
        raise AracKusuru("yamalanmis arac PARSE EDILEMIYOR (satir %s: %s)"
                         % (e.lineno, e.msg))
    hedef = os.path.join(kok, "faz0", "altin_cikti.py")
    with open(hedef, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return hedef


def kos(arac, ortam_dizini=None, saniye=900):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if ortam_dizini:
        onceki = o.get("PYTHONPATH")
        o["PYTHONPATH"] = ortam_dizini + (os.pathsep + onceki if onceki else "")
    ref = os.path.join(os.path.dirname(arac), "altin_kapi.json")
    try:
        r = subprocess.run([sys.executable, arac, "--karsilastir", ref],
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def imza(cikti):
    """Ciktinin OLGU imzasi (sebep degil): sayilabilir isaretler."""
    return {
        "fark_yok": "FARK YOK" in cikti,
        "adsiz": cikti.count("(satir farki bulunamadi"),
        "gorunmez": cikti.count("GORUNMEZ FARK"),
        "sinif": next((s.split("sinif:")[1].split("·")[0].strip()
                       for s in cikti.splitlines() if "GORUNMEZ FARK" in s), None),
        "adlandirildi": cikti.count("        ALTIN: "),
        "olculemedi": "OLCULEMEDI:" in cikti,
        "davranis_degisti": "davranis DEGISTI" in cikti,
        "exit_farki": "EXIT DEGISTI" in cikti,
        "traceback": "Traceback (most recent call last)" in cikti,
    }


def kayit(ad, hukum, ayrinti):
    SONUC.append((ad, hukum, ayrinti))


# --------------------------------------------------------------- MUTANTLAR

def ma1_satir_sonu(taban):
    ad = "M-A1 SATIR SONU (CRLF): yeni olcut, eski olcutun yanlis hukmunu duzeltiyor"
    ortam = ortam_kur(taban, "crlf", SC_CRLF)
    eski = agac_kur(taban, "a1_eski", ESKI_TAM)
    yeni = agac_kur(taban, "a1_yeni", [])
    e_rc, e_c = kos(eski, ortam)
    y_rc, y_c = kos(yeni, ortam)
    if e_rc is None or y_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (eski=%s yeni=%s)" % (e_rc, y_rc))
        return
    ei, yi = imza(e_c), imza(y_c)
    # ESKI: exit 1 + adlandirilamayan fark + "davranis DEGISTI" (YANLIS HUKUM)
    # YENI: exit 0 + FARK YOK (duzeltme-1 sinifi kapatti)
    tamam = (e_rc == 1 and ei["adsiz"] == 10 and ei["davranis_degisti"]
             and y_rc == 0 and yi["fark_yok"] and not yi["traceback"])
    kayit(ad, ISIRDI if tamam else KACTI,
          "CRLF ortami | ESKI: exit=%s adsiz-fark=%s 'davranis DEGISTI'=%s "
          "| YENI: exit=%s 'FARK YOK'=%s (beklenen: 1/10/VAR -> 0/VAR)"
          % (e_rc, ei["adsiz"], "VAR" if ei["davranis_degisti"] else "yok",
             y_rc, "VAR" if yi["fark_yok"] else "yok"))


def ma2_satir_siniri(taban):
    ad = ("M-A2 SATIR SINIRI (\\x0b + \\x85): DUZELTME-1'in KAPATMADIGI sinifi "
          "DUZELTME-2 adlandiriyor")
    izler = []
    tamam = True
    for kacis_ad, kacis, beklenen_sinif in SINIR_HALLERI:
        etiket = kacis_ad.replace("\\", "")
        ortam = ortam_kur(taban, "sinir_" + etiket,
                          SC_SINIR % {"ad": kacis_ad, "kacis": kacis})
        eski = agac_kur(taban, "a2_eski_" + etiket, ESKI_TAM)
        yeni = agac_kur(taban, "a2_yeni_" + etiket, [])
        e_rc, e_c = kos(eski, ortam)
        y_rc, y_c = kos(yeni, ortam)
        if e_rc is None or y_rc is None:
            kayit(ad, OLCULEMEDI, "%s: zaman asimi (eski=%s yeni=%s)"
                  % (kacis_ad, e_rc, y_rc))
            return
        ei, yi = imza(e_c), imza(y_c)
        # YENI: exit 2 (OLCULEMEDI) + sinif ADLANDIRILMIS. exit 0 OLMAMALI —
        # universal newline bu karakteri cevirmez; cevirseydi mutant KENDI
        # hedefini olcemez ve o durumda da KACTI demeli.
        ok = (e_rc == 1 and ei["adsiz"] == 10 and ei["davranis_degisti"]
              and y_rc == 2 and yi["olculemedi"] and yi["gorunmez"] == 10
              and yi["sinif"] == beklenen_sinif and not yi["traceback"])
        tamam = tamam and ok
        izler.append("%s: ESKI exit=%s adsiz=%s -> YENI exit=%s teshis=%s sinif=%r %s"
                     % (kacis_ad, e_rc, ei["adsiz"], y_rc, yi["gorunmez"],
                        yi["sinif"], "OK" if ok else "BEKLENEN=%r" % beklenen_sinif))
    kayit(ad, ISIRDI if tamam else KACTI,
          "beklenen her kolda: 1/10 -> 2/10/<sinif adi> | " + " | ".join(izler))


def ma3_gercek_fark(taban):
    ad = "M-A3 GERCEK FARK: yeni siniflandirma gorunur regresyonu YUTMUYOR"
    yeni = agac_kur(taban, "a3_yeni", [], motor_sabotaji=True)
    rc, c = kos(yeni)          # TEMIZ ortam — yalniz motor sabotajli
    if rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    i = imza(c)
    # Gorunur bir not degisikligi: exit 1 + satir ADLANDIRILMIS + OLCULEMEDI YOK.
    tamam = (rc == 1 and i["davranis_degisti"] and i["adlandirildi"] >= 10
             and not i["olculemedi"] and i["gorunmez"] == 0)
    kayit(ad, ISIRDI if tamam else KACTI,
          "TEMIZ ortam + motorda NOT DEGISIKLIGI | exit=%s 'davranis DEGISTI'=%s "
          "adlandirilan-satir=%s OLCULEMEDI=%s gorunmez=%s "
          "(beklenen: 1/VAR/>=10/yok/0)"
          % (rc, "VAR" if i["davranis_degisti"] else "yok", i["adlandirildi"],
             "VAR" if i["olculemedi"] else "yok", i["gorunmez"]))


def ma4_temiz_kol(taban):
    ad = "M-A4 TEMIZ KOL: duzeltme altin kumeyi BOZMUYOR (referans yeniden kaydedilmez)"
    yeni = agac_kur(taban, "a4_yeni", [])
    rc, c = kos(yeni)
    if rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    i = imza(c)
    tamam = (rc == 0 and i["fark_yok"] and not i["traceback"])
    kayit(ad, ISIRDI if tamam else KACTI,
          "TEMIZ ortam + DOKUNULMAMIS motor | exit=%s 'FARK YOK'=%s traceback=%s "
          "(beklenen: 0/VAR/yok)"
          % (rc, "VAR" if i["fark_yok"] else "yok", "VAR" if i["traceback"] else "yok"))


def ma6_iz_kilidi(taban):
    ad = "M-A6 IZ KILIDI: teshis sokulurse hukum AYNI kalir ama IZ kaybolur"
    ortam = ortam_kur(taban, "vt", SC_VT)
    sokuk = agac_kur(taban, "a6_sokuk", [yama_eski_teshis])   # hukum YERINDE
    tam = agac_kur(taban, "a6_tam", [])
    s_rc, s_c = kos(sokuk, ortam)
    t_rc, t_c = kos(tam, ortam)
    if s_rc is None or t_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (sokuk=%s tam=%s)" % (s_rc, t_rc))
        return
    si, ti = imza(s_c), imza(t_c)
    # Iki kol AYNI hukmu verir (exit 2). Ayrisan sey yalniz IZ: SINIF adi.
    # Bu, "bir hukum izsiz verilebiliyorsa artefakt teshis edemez" dersidir —
    # CI #9'un teshisi tam bu iz olmadigi icin bir tur gecikmisti.
    beklenen = SINIR_HALLERI[0][2]        # tek kaynak: tablo degisirse mutant da degisir
    tamam = (t_rc == 2 and s_rc == 2
             and ti["sinif"] == beklenen and si["sinif"] is None
             and si["adsiz"] == 10 and not si["traceback"])
    kayit(ad, ISIRDI if tamam else KACTI,
          "DIKEY SEKME ortami | TAM: exit=%s sinif=%r | SOKUK: exit=%s sinif=%r "
          "eski-yedek-cumle=%s (beklenen: 2/%r -> 2/None/10; hukum AYNI "
          "kalmali, yoksa mutant hukmu degil izi olcemez)"
          % (t_rc, ti["sinif"], s_rc, si["sinif"], si["adsiz"], beklenen))


def ma5_kapi_dusurme(taban):
    ad = "M-A5 KAPI DUSURME: DUZELTME-2'nin HUKMU sokulurse GORUNUYOR mu (ADDITIVE kilidi)"
    ortam = ortam_kur(taban, "vt", SC_VT)
    sokuk = agac_kur(taban, "a5_sokuk", [yama_eski_hukum])   # kos() ve teshis YERINDE
    tam = agac_kur(taban, "a5_tam", [])
    s_rc, s_c = kos(sokuk, ortam)
    t_rc, t_c = kos(tam, ortam)
    if s_rc is None or t_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (sokuk=%s tam=%s)" % (s_rc, t_rc))
        return
    si, ti = imza(s_c), imza(t_c)
    tamam = (t_rc == 2 and ti["olculemedi"] and s_rc == 1
             and si["davranis_degisti"] and not si["olculemedi"])
    kayit(ad, ISIRDI if tamam else KACTI,
          "DIKEY SEKME ortami | TAM: exit=%s OLCULEMEDI=%s | SOKUK: exit=%s "
          "'davranis DEGISTI'=%s (beklenen: 2/VAR -> 1/VAR; ayni cikarsa kapi KOR)"
          % (t_rc, "VAR" if ti["olculemedi"] else "yok", s_rc,
             "VAR" if si["davranis_degisti"] else "yok"))


def ma7_bozuk_referans(taban):
    ad = "M-A7 BOZUK REFERANS: sekil kusuru ARAC KUSURU (exit 3), URUN hukmu DEGIL"
    eski = agac_kur(taban, "a7_eski", ESKI_TAM, referansi_boz=True)
    yeni = agac_kur(taban, "a7_yeni", [], referansi_boz=True)
    e_rc, e_c = kos(eski)
    y_rc, y_c = kos(yeni)
    if e_rc is None or y_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (eski=%s yeni=%s)" % (e_rc, y_rc))
        return
    ei, yi = imza(e_c), imza(y_c)
    # ESKI: ham traceback + exit 1 (= "davranis DEGISTI", YANLIS URUN HUKMU).
    # YENI: exit 3 + ARAC KUSURU, traceback YOK.
    tamam = (e_rc == 1 and ei["traceback"]
             and y_rc == 3 and "ARAC KUSURU" in y_c and not yi["traceback"])
    kayit(ad, ISIRDI if tamam else KACTI,
          "referansin ilk kaydindan 'exit' alani SILINDI | ESKI: exit=%s "
          "ham-traceback=%s | YENI: exit=%s ARAC-KUSURU=%s ham-traceback=%s "
          "(beklenen: 1/VAR -> 3/VAR/yok)"
          % (e_rc, "VAR" if ei["traceback"] else "yok", y_rc,
             "VAR" if "ARAC KUSURU" in y_c else "YOK",
             "VAR" if yi["traceback"] else "yok"))


def main():
    print("=" * 82)
    print("ALTIN OLCUT MUTANTI — altin_cikti.py'nin uc duzeltmesi ISIRIYOR mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  arac     : %s" % ARAC)
    print("  referans : %s" % REFERANS)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="altin_olcut_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        for f in (ma1_satir_sonu, ma2_satir_siniri, ma3_gercek_fark,
                  ma4_temiz_kol, ma5_kapi_dusurme, ma6_iz_kilidi,
                  ma7_bozuk_referans):
            try:
                f(taban)
            except AracKusuru as e:
                print("\nARAC KUSURU: %s" % e)
                return 3
        print()
        say = {ISIRDI: 0, KACTI: 0, OLCULEMEDI: 0}
        for ad, hukum, ayrinti in SONUC:
            say[hukum] += 1
            print("  %-10s %s" % (hukum, ad))
            print("  %-10s   %s" % ("", ayrinti))
        print()
        print("OLCUMUN SINIRI (hukum degil):")
        print("  - URETILEN ORTAM GERCEK WINDOWS DEGILDIR. Cocugun satir sonu kipi")
        print("    enjekte edilmistir; Windows'un kendi hukmu CI'da olculur.")
        print("  - CI #17/#18 artefaktinin imzasi (10 fark · EXIT farki YOK · 10")
        print("    adlandirilamayan) M-A1/M-A2'nin ESKI kolunun imzasiyla ayni.")
        print("    Bu, SINIFI olcer; artefakt hangi KARAKTER oldugunu adlandirmaz —")
        print("    cunku adlandiramamak kusurun kendisidir. DUZELTME-2 indikten")
        print("    sonraki ilk Windows kosumu o karakteri BASACAK.")
        print("  - Bu mutant yalniz `--karsilastir` olcutunu olcer. `--kendini-sina`")
        print("    KAPSAM DISIDIR ve bu sinifa YAPISAL OLARAK kordur: iki kolu da")
        print("    kosum-aninda uretir, ortama sistematik fark ikisinde de bulunup")
        print("    birbirini goturur (olculdu: temiz · CRLF · \\x0b ortamlarinin")
        print("    ucunde de 'toplam fark kaydi: 10 · ISIRDI · exit 0').")
        print("    Bu yuzden --kendini-sina'ya TOPLAM FARK KAPISI KONMADI: kor olurdu.")
        print("-" * 82)
        print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
              % (say[ISIRDI], say[KACTI], say[OLCULEMEDI], len(SONUC)))
        if say[KACTI]:
            return 1
        if say[OLCULEMEDI]:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

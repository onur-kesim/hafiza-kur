#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ISIR ESLESME MUTANTI (besli-paket/IS_EMRI_H1_ISIR_SIKB.md, 28 Eyl 2026, SIK B).

NEDEN VAR (olculdu: Cowork 28 Eyl, motor 559E830A; faz0/sabotaj.py)
  `isir`in eslesme kurali etiketi ONEKIYLE de kabul ediyordu: `[H1]` arayan bir
  mutant `[H1-KOVA]` satirini gorunce "isirdi" sayiliyordu. "satir KAYIP" fail()'i
  sokulunce ayni kaybi H1-KOVA da gordugu icin M-H1 yine ISIRDI diyordu (ORTUSEN
  TESPIT MASKELER) ve H1'in alti fail()'inin ALTISI da `isir` icin KAPSAMSIZDI.
  Duzeltme (Onur kilidi 28 Eyl: Soru 1 = A+B, Soru 2 = opsiyonel `siki`):
    A  `mutant()`/`mutant_git()` eslesmesi TAM etiket (onek dali kalkti)
    B  H1'in YEDI mutanti kendi EKSEN cumlesinden bir parca da ister (parca
       sozlugu `cmd_isir` icinde TEK yerde; H11 turunda (IS_EMRI_H11_ISIR.md,
       28 Eyl 2026) adi `_eksen_parca` oldu ve H11'in ON BIR mutantini da tasir)
    C  `_kapi_metni(kok, siki=False)`; yalniz eksen-6 mutanti (M-H1s) `siki=True`
  Bu betik uc duzeltmenin HER BIRINI ayri kolla olcer (her duzeltmeye AYRI mutant).

NE OLCER
  KOL O  STATIK OZ SINAMA (motor KOSULMAZ, ast.literal_eval ile okunur):
         (i)  `_eksen_parca`nin her parcasi motordaki fail() SABLONLARINDAN TAM
              BIRINE uyar (0 ya da 2+ = KIRMIZI) ve o cagri mutantin HEDEF
              ekseninin fail()'idir. H1: eksen <-> fail() baglantisi
              faz0/h1_kapsam_mutanti.py'nin OLCULMUS eslemesinden alinir
              (`_h1_hedefleri`). H11: hedef, fail()'in KONUMUDUR — durdugu H11
              alt-fonksiyonu ve o fonksiyondaki SIRASI (`H11_HEDEF`); parca
              metninden bagimsizdir.
              SABLON ESLEMESI (IS_EMRI_H11_ISIR.md EK-1 a): fail()'in ikinci
              argumani AST'ten sablona cevrilir (sabit metin · `%` bicimi ·
              `+` birlesimi · f-string · kosullu ifade -> iki sablon; baska her
              ifade TEK yer tutucu). Parca, sablonun bir CIKTISININ alt dizesi
              olabiliyorsa ve sablonun EN AZ BIR sabit karakterini iceriyorsa
              "uyar". Yer tutucu TEK SOZCUKTUR (bosluksuz; %d ailesi rakam).
              Gerekce (olculdu 28 Eyl): lafzi `.+?` ile "yerine-gecen 9999 yok"
              parcasi `%s: yerini-aldigi %s yok` sablonuna da uyar (ikinci %s
              = "yerine-gecen 9999") — oysa o %s isdigit()'ten gecmis bir
              sayidir; H11'in %s degerleri dosya adi ([a-z0-9-]+.md) ve sayidir.
         (ii) `sinamalar`da etiketi H1 ya da H11 olan her mutantin parcasi VAR,
              her parca anahtari bir `sinamalar` adidir; parcalar H1'in ALTI ve
              H11'in ON BIR fail()'ini de orter; `siki` secenegi YALNIZ M-H1s'e
              verilmistir.
  KOL 0  NEGATIF KONTROL: temiz motor, kur+not+derle sablonu -> `isir` exit 0 ve
         H1'in yedi, H11'in on bir mutanti ISIRDI. Bu tutmazsa asagidaki kollar
         HICBIR SEY olcmez.
  KOL a  POZITIF KONTROL (maskeleme URETILIR): motor kopyasinda "satir KAYIP"
         fail()'i sabote edilir (sabotaj.py'nin KENDI fail_cagrilari/sabote_et'i;
         cagri METNINDEN bulunur, satir numarasindan DEGIL) VE eski kural geri
         konur (A ve B birlikte geri alinir) -> `isir` M-H1'i ISIRDI der.
  KOL a1 AYNI sabotaj, YALNIZ onek dali geri (B yerinde) -> M-H1/M-H1b KACTI.
  KOL a2 AYNI sabotaj, YALNIZ parca sarti kalkar (A yerinde) -> M-H1/M-H1b KACTI.
         (a1/a2: iki savunma BIRBIRINDEN BAGIMSIZ yeter; is emrinin lafzi "a"
         kolu — yalniz onek dali geri — a1'dir ve A+B kilidinde maskelemeyi
         URETEMEZ, cunku B ayakta. Maskelemeyi ureten kol ikisini birden geri alir.)
  KOL b  AYNI sabotaj, YENI kural -> M-H1 VE M-H1b KACTI.
  KOL c  `siki` GERCEKTEN kullaniliyor mu: M-H1s'in secenek tablosundan
         `siki=True` kaldirilir (sabotaj YOK) -> M-H1s KACTI ya da KURULAMADI
         (hangisi oldugu OLCULUP basilir). ISIRDI kalirsa parametre OLUdur.

NE OLCMEZ
  1. `mutant_git`teki onek dalinin kalkmasi: motorda tireli tek etiket H1-KOVA'dir
     ve `mutant_git` yalniz H12/H14 git kollarini sinar -> gozlenebilir fark YOK.
  2. Yeni eksen mutantlarinin (M-H1d/g/y/o/s, M-H11t/v/ys/yy/tk/yd/as/ay/lo/ly)
     KOSEGENI: onu faz0/sabotaj.py (bayraksiz, `isir ile` sutunu) olcer; bu betik
     yalniz eslesme KURALINI ve parca tablosunu olcer.
  3. H1-KOVA fail()'lerinin kapsami (bu turun disi).
  4. Mesaji TUMUYLE bir degiskenden gelen fail() (ör. `fail("H0", h)`): sabit
     karakteri yoktur, hicbir parca ona "uyamaz" — KOL O onu GOREMEZ. Bosluk
     iceren yer tutucu degerleri (serbest metin) de modellenmez (yukaridaki
     gerekce); parca o metne denk gelirse KOL O bunu yakalamaz.

CIKIS KODLARI
  0  KOL O temiz, KOL 0 temiz, a/a1/a2/b/c beklendigi gibi
  1  bir kol BEKLENMEDIK (oz sinama kirmizi, maskeleme uretilemedi, bir savunma
     tek basina yetmedi, M-H1s `siki`siz de ISIRDI ...)
  2  OLCULEMEDI (motor okunamadi, capa bulunamadi, sablon kurulamadi, `isir`
     cokti/zaman asimi) — sessiz PASS YOK

KULLANIM
  python faz0/isir_eslesme_mutanti.py [motor]
"""
import ast
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

# Mutant kimligi -> hedef H1 ekseni (numaralar faz0/h1_kapsam_mutanti.py'nin
# EKSEN_KAYNAK numaralaridir: 1 sahte duzeltme · 2 gerekcesiz · 3 YENI zaten var ·
# 4 okunamayan arsiv · 5 satir KAYIP · 6 beyansiz ekleme).
HEDEF_EKSEN = {"M-H1": 5, "M-H1b": 5, "M-H1d": 1, "M-H1g": 2,
               "M-H1y": 3, "M-H1o": 4, "M-H1s": 6}
# H11 turu (besli-paket/IS_EMRI_H11_ISIR.md, 28 Eyl 2026): mutant kimligi -> hedef
# fail()'in KONUMU = (durdugu H11 alt-fonksiyonu, o fonksiyondaki H11 fail() SIRASI,
# 1'den). Motorun H11 ALT-BOLMESI (FAZ C) yorumundaki dort parca; parca METNINDEN
# bagimsizdir — kapi govdesinde bir fail() yer degistirirse KOL O KIRMIZI yanar.
H11_HEDEF = {"M-H11t": ("_h11_numara", 1), "M-H11": ("_h11_numara", 2),
             "M-H11v": ("_h11_govde", 1),
             "M-H11ys": ("_h11_baglanti", 1), "M-H11yy": ("_h11_baglanti", 2),
             "M-H11tk": ("_h11_baglanti", 3), "M-H11yd": ("_h11_baglanti", 4),
             "M-H11as": ("_h11_baglanti", 5), "M-H11ay": ("_h11_baglanti", 6),
             "M-H11lo": ("_h11_canli_link", 1), "M-H11ly": ("_h11_canli_link", 2)}
# H6/H8/H16 turu (besli-paket/IS_EMRI_H8_H6_H16_ISIR.md, 29 Eyl 2026): AYNI
# gerekce H11 ile PAYLASILIR — H16'nin uc fail() cagrisi DORT dizin
# (kararlar/gunluk/gunluk_ars/h) icin TEK yerden AYNI sablonu basar (dizin adi
# kaynakta bir DEGISKENDIR, literal degil); icerik-esleme TEK BASINA hangi
# dizini kastettigini ayirt edemez. Hedef bu yuzden KONUMDUR (H6/H8 de,
# tutarlilik ve saglamlik icin, AYNI yontemle -- parca metninden BAGIMSIZ --
# dogrulanir; H11'in kendisiyle AYNI dongude, bkz. `kol_o`).
H6_HEDEF = {"M-H6y": ("_kapi_govde", 1),
            "M-H6b": ("_kapi_h6", 1), "M-H6": ("_kapi_h6", 2), "M-H6t": ("_kapi_h6", 3)}
H8_HEDEF = {"M-H8y": ("_kapi_h8", 1), "M-H8o": ("_kapi_h8", 2), "M-H8b": ("_kapi_h8", 3),
            "M-H8m": ("_kapi_h8", 4), "M-H8g": ("_kapi_h8", 5), "M-H8": ("_kapi_h8", 6)}
H16_HEDEF = {"M-H16y": ("_kapi_h16", 1), "M-H16d": ("_kapi_h16", 2), "M-H16k": ("_kapi_h16", 3)}
POZISYON_GRUPLARI = (("H11", H11_HEDEF), ("H6", H6_HEDEF), ("H8", H8_HEDEF), ("H16", H16_HEDEF))
TABLO = "_eksen_parca"           # cmd_isir icindeki TEK parca tablosunun adi
SIKI_KIMLIK = "M-H1s"
SABOTAJ_KIMLIK = "M-H1"          # sabote edilen fail(): bu mutantin parcasiyla bulunur
# EK-1 (besli-paket/IS_EMRI_H8_H6_H16_ISIR.md): junction dali AYRICA kolla
# olculur — symlink'i zorla basarisiz kil, junction'a dustu mu / #66 ISIRDI mi.
# TEK TANIK turu (besli-paket/IS_EMRI_TEK_TANIK_ISIR.md, 29 Eyl 2026): kapisinin
# DIGER mutantlari parcasiz kalir (mevcut mutantlar birebir) => bu grup icin
# "kapinin tum fail()'leri ortulmeli" sarti YOK; her parca TAM 1 fail()'e uymali
# ve o fail()'in KONUMU (etiket, fonksiyon, o etikete gore sirasi) beklenenle
# ayni olmali. M-H9'un parcasi `_eksen_parca`da degil, `sinamalar_git`
# tuple'inin 4. ogesindedir (mutant_git kalibi).
TEK_TANIK_HEDEF = {"M-Hcy": ("H-", "_kapi_govde", 1), "M-H0k": ("H0", "_kapi_h0", 1),
                   "M-H10t": ("H10", "_h10_sozluk", 1), "M-H12c": ("H12", "_h12_sapma_hukmu", 1),
                   "M-H14e": ("H14", "_h14_hukum", 1), "M-H9": ("H9", "_kapi_h9", 1),
                   # KALAN 12 KOR NOKTA (besli-paket/IS_EMRI_KALAN12_KOR_NOKTA.md, 3 Eki 2026): AYNI
                   # sozlesme (tamamlik istenmez; her parca [etiket] altinda TAM 1 fail()'e uyar ve o
                   # fail() beklenen KONUMDA durur). Etiket icindeki sira, ust fonksiyondaki fail()
                   # cagrilarinin kaynak sirasidir (1'den): ayni etiketli kardes fail()'ler (H0 3906/3911,
                   # H1-KOVA 4065/4086/4095, H13 5016/5022/5030) yalniz KONUMLA ayirt edilir.
                   "M-H0x": ("H0", "_kapi_h0", 2), "M-H1kv": ("H1-KOVA", "_h1_kova", 1),
                   "M-H1ks": ("H1-KOVA", "_h1_kova", 3), "M-H4k": ("H4", "_h4_hukum", 2),
                   "M-H5r": ("H5", "_kapi_h5", 1), "M-H10g": ("H10", "_h10_cit", 2),
                   "M-H12s": ("H12", "_h12_tazelik", 4), "M-H13s": ("H13", "_kapi_h13", 2),
                   "M-H13p": ("H13", "_kapi_h13", 3), "M-H2d": ("H2", "_kapi_h15", 1),
                   "M-H17b": ("H17", "_kapi_h17", 1), "M-HLINK": ("H-LINK", "_kapi_govde", 1)}
JUNCTION_KIMLIK = "M-H16k"
JUNCTION_FONKSIYON = "m_h16k"
JUNCTION_ESKI = "os.symlink(dis, d, target_is_directory=True)"
JUNCTION_YENI = "raise OSError(1314, 'KOL J zorla basarisiz (EK-1)')"

# Metin capalari (motor kaynagi). Her biri kendi KAPSAMINDA TAM 1 kez gecmeli.
A_ESKI = 'yakalandi = (k != 0) and (("[%s]" % kapi) in c)'
A_YENI = 'yakalandi = (k != 0) and (("[%s]" % kapi) in c or ("[%s-" % kapi) in c)'
B_ESKI = 'parca_ok = (icerik_parcasi is None) or (icerik_parcasi in c)'
B_YENI = 'parca_ok = True'
C_ESKI = 'dict(siki=True)'
C_YENI = 'dict()'

_SATIR = re.compile(r"^\s*(M-\S+)\s.*?->\s*(ISIRDI|KACTI|KURULAMADI|UYGULANMAZ)", re.M)


class Olculemedi(Exception):
    """Kurulum/capa/kosum basarisiz — KOL HUKMU DEGILDIR."""


def kos(motor, *argv, kok=None, sure=240):
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                       timeout=sure)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# =============================================================== AST OKUMA
def _cmd_isir(agac):
    for d in agac.body:
        if isinstance(d, ast.FunctionDef) and d.name == "cmd_isir":
            return d
    raise Olculemedi("motorda `cmd_isir` bulunamadi")


def _atama(fn, ad):
    """cmd_isir GOVDESINDEKI (ic fonksiyonlara inmeden) `ad = ...` atamasinin degeri."""
    bulunan = [d.value for d in fn.body if isinstance(d, ast.Assign)
               and len(d.targets) == 1 and isinstance(d.targets[0], ast.Name)
               and d.targets[0].id == ad]
    if len(bulunan) != 1:
        raise Olculemedi("cmd_isir icinde `%s` atamasi %d kez (1 olmali)" % (ad, len(bulunan)))
    return bulunan[0]


def _ic_fonksiyon(fn, ad):
    bulunan = [d for d in fn.body if isinstance(d, ast.FunctionDef) and d.name == ad]
    if len(bulunan) != 1:
        raise Olculemedi("cmd_isir icinde `def %s` %d kez (1 olmali)" % (ad, len(bulunan)))
    return bulunan[0]


def motor_tablolari(kaynak):
    """Doner: parca {ad: parca}, sinamalar [(ad, kapi)], siki_adlar [ad],
    git_parca {ad: (kapi, parca)} (`sinamalar_git` 4'lu tuple'lari)."""
    try:
        agac = ast.parse(kaynak)
    except SyntaxError as e:
        raise Olculemedi("motor ayristirilamadi: %s" % e)
    fn = _cmd_isir(agac)
    try:
        parca = ast.literal_eval(_atama(fn, TABLO))
    except ValueError as e:
        raise Olculemedi("`%s` bir sozluk LITERALI degil: %s" % (TABLO, e))
    if not isinstance(parca, dict) or not parca:
        raise Olculemedi("`%s` bos ya da sozluk degil" % TABLO)
    sin = _atama(fn, "sinamalar")
    if not isinstance(sin, ast.List):
        raise Olculemedi("`sinamalar` bir liste literali degil")
    sinamalar = []
    for e in sin.elts:
        if not (isinstance(e, ast.Tuple) and len(e.elts) >= 2
                and all(isinstance(x, ast.Constant) and isinstance(x.value, str)
                        for x in e.elts[:2])):
            raise Olculemedi("`sinamalar` ogesi (ad, kapi, fn) bicimi disinda (satir %d)"
                             % e.lineno)
        sinamalar.append((e.elts[0].value, e.elts[1].value))
    sec = _atama(fn, "_h1_secenek")
    if not isinstance(sec, ast.Dict):
        raise Olculemedi("`_h1_secenek` bir sozluk literali degil")
    siki_adlar = []
    for k, v in zip(sec.keys, sec.values):
        if not (isinstance(k, ast.Constant) and isinstance(v, ast.Call)):
            raise Olculemedi("`_h1_secenek` ogesi {ad: dict(...)} bicimi disinda")
        for kw in v.keywords:
            if kw.arg == "siki" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                siki_adlar.append(k.value)
    git_parca = {}                                   # ad -> (kapi, parca)
    # `sinamalar_git` (mutant_git) ve `sinamalar_baglanti` (M-HLINK: MutantUygulanmaz'i da
    # yakalayan kosucu) AYNI 4'lu bicimdedir: (ad, kapi, fn, parca).
    for liste_ad in ("sinamalar_git", "sinamalar_baglanti"):
        sg = _atama(fn, liste_ad)
        if not isinstance(sg, ast.List):
            raise Olculemedi("`%s` bir liste literali degil" % liste_ad)
        for e in sg.elts:
            if (isinstance(e, ast.Tuple) and len(e.elts) == 4
                    and all(isinstance(e.elts[i], ast.Constant) and isinstance(e.elts[i].value, str)
                            for i in (0, 1, 3))):
                git_parca[e.elts[0].value] = (e.elts[1].value, e.elts[3].value)
    return parca, sinamalar, siki_adlar, git_parca


def kimlik(ad):
    return ad.split()[0]


# ======================================================== SABLON ESLEMESI
# EK-1 a (besli-paket/IS_EMRI_H11_ISIR.md, 28 Eyl 2026): parca fail()'in KAYNAK
# metninde birebir ARANMAZ — `%s yok` gibi cumleler kaynakta parcanin kendisini
# tasimaz. fail()'in ikinci argumani AST'ten SABLONA cevrilir; sablon bir birim
# listesidir: ("C", karakter) sabit karakter · ("P", sinif) yer tutucu (en az 1
# karakter; sinif None = TEK SOZCUK, yani bosluksuz). Kosullu ifade iki sablon
# verir; cagri sablonlarindan HERHANGI birine uyuyorsa parca o fail()'e uyar.
_BICIM = re.compile(r"%(?:\(\w+\))?[-#0 +]*(?:\d+|\*)?(?:\.(?:\d+|\*))?([a-zA-Z%])")
_RAKAM = "0123456789-"


def _yer_tutucu_sinifi(tur):
    """printf tur harfi -> yer tutucunun karakter sinifi (None = tek sozcuk)."""
    if tur in "diu":
        return _RAKAM
    if tur in "eEfFgG":
        return _RAKAM + ".eE+"
    if tur in "xX":
        return "0123456789abcdefABCDEF"
    return None


def _printf(metin):
    out, i = [], 0
    for m in _BICIM.finditer(metin):
        out.extend(("C", ch) for ch in metin[i:m.start()])
        out.append(("C", "%") if m.group(1) == "%" else ("P", _yer_tutucu_sinifi(m.group(1))))
        i = m.end()
    out.extend(("C", ch) for ch in metin[i:])
    return out


def _sablonlar(d):
    """fail() ikinci argumani (AST) -> olasi sablonlar. Sabit metin literal kalir
    (`%` uygulanmadiysa `%s` de duz metindir); `%` bicimi printf; `+` uc uca;
    f-string sabit parca + yer tutucu; kosullu ifade iki kol; geri kalan her ifade
    TEK yer tutucudur."""
    yer = [[("P", None)]]
    if isinstance(d, ast.Constant) and isinstance(d.value, str):
        return [[("C", ch) for ch in d.value]]
    if isinstance(d, ast.BinOp) and isinstance(d.op, ast.Mod):
        sol = _sablonlar(d.left)
        if all(t == "C" for s in sol for t, _ in s):
            return [_printf("".join(ch for _, ch in s)) for s in sol]
        return yer
    if isinstance(d, ast.BinOp) and isinstance(d.op, ast.Add):
        return [a + b for a in _sablonlar(d.left) for b in _sablonlar(d.right)]
    if isinstance(d, ast.IfExp):
        return _sablonlar(d.body) + _sablonlar(d.orelse)
    if isinstance(d, ast.JoinedStr):
        out = [[]]
        for v in d.values:
            ek = _sablonlar(v) if isinstance(v, ast.Constant) else yer
            out = [a + b for a in out for b in ek]
        return out
    return yer


def _uyar(parca, sablon):
    """`parca`, `sablon`un bir ciktisinin ALT DIZESI olabiliyor mu — ve en az bir
    SABIT karakteri kapsayarak mi? (Yalniz yer tutucunun icine dusen parca "uymaz":
    aksi halde her parca her `%s`li cumleye uyardi.) Durum: (birim, yer tutucuda
    en az 1 karakter yendi, sabit karakter yendi)."""
    n = len(sablon)
    durum = {(k, False, False) for k in range(n)}     # parca HERHANGI bir birimde baslar
    for ch in parca:
        yeni = set()
        for k, ici, sabit in durum:
            if k >= n:
                continue
            tur, deger = sablon[k]
            if tur == "C":
                if ch == deger:
                    yeni.add((k + 1, False, True))
            elif (not ch.isspace()) if deger is None else (ch in deger):
                yeni.add((k, True, sabit))
        yeni |= {(k + 1, False, sabit) for k, ici, sabit in yeni if ici}
        durum = yeni
        if not durum:
            return False
    return any(sabit for _, _, sabit in durum)


def cagri_sablonlari(kaynak):
    """sabotaj.fail_cagrilari SIRASIYLA: [(cagri, sablonlar, ust fonksiyon adi)]."""
    import sabotaj                         # faz0/ sys.path[0]'dadir
    agac = ast.parse(kaynak)
    dugum = {(d.lineno, d.col_offset): d for d in ast.walk(agac)
             if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "fail"}
    ust = [(f.lineno, f.end_lineno, f.name) for f in agac.body
           if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    out = []
    for h in sabotaj.fail_cagrilari(kaynak):
        d = dugum[(h["lineno"], h["col"])]
        sab = _sablonlar(d.args[1]) if len(d.args) > 1 else [[("P", None)]]
        fn = next((ad for b, s, ad in ust if b <= h["lineno"] <= s), None)
        out.append((h, sab, fn))
    return out


def uyan_cagrilar(parca, cs):
    return [h for h, sab, _ in cs if any(_uyar(parca, s) for s in sab)]


def _tanim(uyan):
    t = ", ".join("#%02d sat %d [%s]" % (h["no"], h["lineno"], h["kapi"]) for h in uyan[:4])
    return t + (" ... +%d" % (len(uyan) - 4) if len(uyan) > 4 else "")


# ================================================================== KOL O
def kol_o(kaynak):
    """Doner: (bulgular, sabote edilecek fail() hedefi, parca sozlugu)."""
    import h1_kapsam_mutanti
    parca, sinamalar, siki_adlar, git_parca = motor_tablolari(kaynak)
    kapisi = dict(sinamalar)
    cs = cagri_sablonlari(kaynak)
    cagrilar = [h for h, _, _ in cs]
    try:
        hedefler, _ = h1_kapsam_mutanti._h1_hedefleri(kaynak)
    except h1_kapsam_mutanti.Olculemedi as e:
        raise Olculemedi("H1 eksen eslemesi kurulamadi: %s" % e)
    b = []
    h1_parca = {a: p for a, p in parca.items() if kapisi.get(a) == "H1"}
    h11_parca = {a: p for a, p in parca.items() if kapisi.get(a) == "H11"}
    print("  motordaki fail() sayisi: %d · H1 fail(): %d · parca: %d"
          % (len(cagrilar), sum(1 for h in cagrilar if h["kapi"] == "H1"), len(h1_parca)))
    POZ_ETIKET = tuple(e for e, _ in POZISYON_GRUPLARI)
    for kapi in ("H1",) + POZ_ETIKET:
        for a in [a for a, k in sinamalar if k == kapi]:
            if a not in parca:
                b.append("etiketi %s olan `%s` mutantinin PARCASI YOK" % (kapi, a))
    for a in parca:
        if a not in kapisi:
            b.append("parca anahtari `%s` hicbir `sinamalar` adi DEGIL (sessizce "
                     "uygulanmaz)" % a)
        elif kapisi[a] not in ("H1",) + POZ_ETIKET and kimlik(a) not in TEK_TANIK_HEDEF:
            b.append("`%s` [%s]: bu betik o kapinin eksen eslemesini TANIMIYOR" % (a, kapisi[a]))
    ortulen = set()
    sabotaj_hedefi = None
    for a, p in sorted(h1_parca.items(), key=lambda x: kimlik(x[0])):
        uyan = uyan_cagrilar(p, cs)
        eksen = HEDEF_EKSEN.get(kimlik(a))
        if eksen is None:
            b.append("`%s`: hedef ekseni bu betikte TANIMSIZ" % a)
            continue
        hedef = hedefler[eksen]
        if len(uyan) != 1:
            b.append("`%s` parcasi %d fail()'e uyuyor (TAM 1 olmali): %r -> %s"
                     % (kimlik(a), len(uyan), p, _tanim(uyan) or "-"))
            continue
        h = uyan[0]
        if h["kapi"] != "H1" or h["lineno"] != hedef["lineno"]:
            b.append("`%s` parcasi YANLIS fail()'e uyuyor: %s (hedef eksen %d = #%02d sat %d)"
                     % (kimlik(a), _tanim(uyan), eksen, hedef["no"], hedef["lineno"]))
            continue
        ortulen.add(h["lineno"])
        if kimlik(a) == SABOTAJ_KIMLIK:
            sabotaj_hedefi = h
        print("  %-6s eksen %d -> #%02d sat %-5d TAM 1 fail() : %r"
              % (kimlik(a), eksen, h["no"], h["lineno"], p))
    h1_hepsi = set(h["lineno"] for h in hedefler.values())
    if ortulen != h1_hepsi:
        b.append("parcalar H1'in alti fail()'ini ORTMUYOR: eksik satirlar %s"
                 % sorted(h1_hepsi - ortulen))

    # ---- H11/H6/H8/H16 (IS_EMRI_H11_ISIR.md + IS_EMRI_H8_H6_H16_ISIR.md):
    # hedef = fail()'in KONUMU (fonksiyon, o etikete gore sirasi, 1'den).
    # H11'in TEK ekseniydi; H8_H6_H16 turunde AYNI dongu genellestirildi
    # (POZISYON_GRUPLARI) — davranis H11 icin BIREBIR eskisi (sadece kod
    # tekrari kalkti).
    konum_g, sira_g = {}, {}
    izlenen_etiket = set(dict(POZISYON_GRUPLARI)) | {e for e, _, _ in TEK_TANIK_HEDEF.values()}
    for h, _, fn in cs:
        etiket = h["kapi"]
        if etiket in izlenen_etiket:
            sira_g.setdefault(etiket, {})
            sira_g[etiket][fn] = sira_g[etiket].get(fn, 0) + 1
            konum_g.setdefault(etiket, {})[(fn, sira_g[etiket][fn])] = h
    for etiket, hedef_map in POZISYON_GRUPLARI:
        konum = konum_g.get(etiket, {})
        etiket_parca = {a: p for a, p in parca.items() if kapisi.get(a) == etiket}
        print("  %s fail(): %d · parca: %d" % (etiket, len(konum), len(etiket_parca)))
        if sorted(konum) != sorted(hedef_map.values()):
            b.append("%s fail() KONUMLARI beklenen (fonksiyon, sira) kumesi DEGIL: motorda %s"
                     % (etiket, sorted(konum)))
        ortulen = set()
        for a, p in sorted(etiket_parca.items(), key=lambda x: kimlik(x[0])):
            hk = hedef_map.get(kimlik(a))
            if hk is None:
                b.append("`%s`: hedef ekseni bu betikte TANIMSIZ" % a)
                continue
            uyan = uyan_cagrilar(p, cs)
            if len(uyan) != 1:
                b.append("`%s` parcasi %d fail()'e uyuyor (TAM 1 olmali): %r -> %s"
                         % (kimlik(a), len(uyan), p, _tanim(uyan) or "-"))
                continue
            h, hedef = uyan[0], konum.get(hk)
            if hedef is None or h["lineno"] != hedef["lineno"]:
                b.append("`%s` parcasi YANLIS fail()'e uyuyor: %s (hedef %s/%d)"
                         % (kimlik(a), _tanim(uyan), hk[0], hk[1]))
                continue
            ortulen.add(h["lineno"])
            print("  %-7s %-17s -> #%02d sat %-5d TAM 1 fail() : %r"
                  % (kimlik(a), "%s/%d" % hk, h["no"], h["lineno"], p))
        hepsi = set(h["lineno"] for h in konum.values())
        if ortulen != hepsi:
            b.append("parcalar %s'in %d fail()'ini ORTMUYOR: eksik satirlar %s"
                     % (etiket, len(hepsi), sorted(hepsi - ortulen)))

    # ---- TEK TANIK (IS_EMRI_TEK_TANIK_ISIR.md): tamamlik ISTENMEZ (kapilarin diger
    # mutantlari parcasiz); her parca TAM 1 fail()'e uymali ve o fail() beklenen
    # (etiket, fonksiyon, sira) KONUMUNDA olmali.
    tek_parca = {a: p for a, p in parca.items() if kimlik(a) in TEK_TANIK_HEDEF}
    tek_etiket = {a: kapisi.get(a) for a in tek_parca}
    for a, (kp, p) in git_parca.items():
        if kimlik(a) in TEK_TANIK_HEDEF:
            tek_parca[a] = p
            tek_etiket[a] = kp
    print("  TEK TANIK fail(): parca %d / beklenen %d" % (len(tek_parca), len(TEK_TANIK_HEDEF)))
    for kim in TEK_TANIK_HEDEF:
        if kim not in {kimlik(a) for a in tek_parca}:
            b.append("TEK TANIK `%s` mutantinin PARCASI YOK" % kim)
    for a, p in sorted(tek_parca.items(), key=lambda x: kimlik(x[0])):
        etiket, fn0, sira0 = TEK_TANIK_HEDEF[kimlik(a)]
        if tek_etiket[a] != etiket:
            b.append("`%s`: kapi etiketi %r (beklenen %r)" % (kimlik(a), tek_etiket[a], etiket))
            continue
        # Tekillik AYNI ETIKETLI fail()'ler arasinda aranir: `mutant()`/`mutant_git()`
        # eslesmesi `[etiket]` VE parcayi BIRLIKTE ister; baska etiketli bir sablona
        # statik uyum (or. "git'te IZLENMIYOR" ~ H12 "git'te %s tarihinde") runtime'da
        # etkisizdir. Etiket-disi uyum sayisi bilgi olarak basilir.
        tum = uyan_cagrilar(p, cs)
        uyan = [x for x in tum if x["kapi"] == etiket]
        if len(uyan) != 1:
            b.append("`%s` parcasi [%s] etiketli %d fail()'e uyuyor (TAM 1 olmali): %r -> %s"
                     % (kimlik(a), etiket, len(uyan), p, _tanim(uyan) or "-"))
            continue
        h, hedef = uyan[0], konum_g.get(etiket, {}).get((fn0, sira0))
        if hedef is None or h["lineno"] != hedef["lineno"]:
            b.append("`%s` parcasi YANLIS fail()'e uyuyor: %s (hedef %s %s/%d)"
                     % (kimlik(a), _tanim(uyan), etiket, fn0, sira0))
            continue
        print("  %-7s %-24s -> #%02d sat %-5d TAM 1 [%s] fail() (etiket-disi uyum %d) : %r"
              % (kimlik(a), "%s/%d" % (fn0, sira0), h["no"], h["lineno"], etiket,
                 len(tum) - 1, p))
    if [kimlik(a) for a in siki_adlar] != [SIKI_KIMLIK]:
        b.append("`siki=True` alan mutantlar %s (YALNIZ %s olmali)"
                 % ([kimlik(a) for a in siki_adlar], SIKI_KIMLIK))
    if sabotaj_hedefi is None and not b:
        b.append("%s parcasinin fail()'i bulunamadi" % SABOTAJ_KIMLIK)
    return b, sabotaj_hedefi, parca


# ============================================================ MOTOR KOPYASI
def _kapsamda_degistir(kaynak, fonksiyon, eski, yeni):
    """`cmd_isir` (fonksiyon=None) ya da onun ic fonksiyonu `fonksiyon`un SATIR
    araliginda `eski`yi `yeni` ile degistirir; aralikta TAM 1 kez gecmeli."""
    agac = ast.parse(kaynak)
    fn = _cmd_isir(agac)
    if fonksiyon is not None:
        fn = _ic_fonksiyon(fn, fonksiyon)
    L = kaynak.split("\n")
    bas, son = fn.lineno - 1, fn.end_lineno
    parca = "\n".join(L[bas:son])
    n = parca.count(eski)
    if n != 1:
        raise Olculemedi("capa `%s` kapsaminda %d kez gecti (1 olmali): %r"
                         % (fonksiyon or "cmd_isir", n, eski))
    L[bas:son] = parca.replace(eski, yeni, 1).split("\n")
    return "\n".join(L)


def motor_turet(kaynak, sabotaj_hedefi, degisimler):
    import sabotaj
    s = kaynak
    if sabotaj_hedefi is not None:
        s = sabotaj.sabote_et(s, sabotaj_hedefi)
    for fonksiyon, eski, yeni in degisimler:
        s = _kapsamda_degistir(s, fonksiyon, eski, yeni)
    try:
        compile(s, "<isir_eslesme>", "exec")
    except SyntaxError as e:
        raise Olculemedi("turetilen motor derlenmiyor: %s" % e)
    return s


# ================================================================ KOSUM
def sablon_kur(motor, taban):
    kok = os.path.join(taban, "sablon")
    os.makedirs(kok)
    for argv in (("kur", "--ad", "IsirEslesme"),
                 ("not", "--konu=genel-durum", "--metin=isir eslesme sablonu ilk not"),
                 ("derle",)):
        k, c = kos(motor, *argv, kok=kok)
        if k != 0:
            raise Olculemedi("sablon: %s exit %d: %s" % (argv[0], k, c[-300:]))
    k, c = kos(motor, "kapi", kok=kok)
    if k != 0:
        raise Olculemedi("sablon: temiz motorda kapi exit %d (isir kosamaz)" % k)
    return kok


def isir_kos(motor_metni, sablon, taban, ad):
    """Turetilmis motoru yazar, sablonun KOPYASINDA `isir` kosar.
    Doner: (exit, {kimlik: hukum}, ham cikti)."""
    d = os.path.join(taban, ad)
    os.makedirs(d)
    mp = os.path.join(d, "hafiza.py")
    with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
        f.write(motor_metni)
    kok = os.path.join(d, "p")
    shutil.copytree(sablon, kok)
    try:
        k, c = kos(mp, "isir", kok=kok, sure=1200)
    except subprocess.TimeoutExpired:
        raise Olculemedi("%s: isir zaman asimi (1200 sn)" % ad)
    if "Traceback" in c:
        raise Olculemedi("%s: isir COKTU (Traceback): %s" % (ad, c[-300:]))
    hukum = {}
    for m in _SATIR.finditer(c):
        hukum.setdefault(m.group(1), m.group(2))
    if not hukum:
        raise Olculemedi("%s: isir ciktisinda mutant satiri yok (exit %d): %s"
                         % (ad, k, c[-300:]))
    return k, hukum, c


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN_MOTOR)
    print(CIZGI)
    print("ISIR ESLESME MUTANTI (SIK B: A tam etiket · B eksen parcasi · C siki)")
    print("motor: %s · platform: %s" % (motor, sys.platform))
    print(CIZGI)
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    # ---- KOL O -------------------------------------------------------------
    print("\n--- KOL O: statik oz sinama (parca -> TAM 1 fail(), hedef eksen) ---")
    try:
        bulgu_o, sab_hedef, parca = kol_o(kaynak)
    except (Olculemedi, ImportError) as e:
        print("SONUC: OLCULEMEDI — KOL O: %s" % e)
        return 2
    for x in bulgu_o:
        print("  ! %s" % x)
    if bulgu_o:
        print("\nSONUC: KIRMIZI — KOL O: %d bulgu (parca tablosu kendi sozlesmesini "
              "tutmuyor; dinamik kollar KOSULMADI)." % len(bulgu_o))
        return 1
    print("  KOL O -> TEMIZ (sabote edilecek fail(): #%02d sat %d, METINDEN bulundu)"
          % (sab_hedef["no"], sab_hedef["lineno"]))

    # ---- motor turevleri ---------------------------------------------------
    A = ("mutant", A_ESKI, A_YENI)
    B = ("mutant", B_ESKI, B_YENI)
    C = (None, C_ESKI, C_YENI)
    J = (JUNCTION_FONKSIYON, JUNCTION_ESKI, JUNCTION_YENI)
    try:
        turevler = [
            ("KOL 0 ", "temiz motor (negatif kontrol)", motor_turet(kaynak, None, [])),
            ("KOL a ", "satir KAYIP sabote + ESKI kural (A ve B geri)",
             motor_turet(kaynak, sab_hedef, [A, B])),
            ("KOL a1", "satir KAYIP sabote + YALNIZ onek dali geri",
             motor_turet(kaynak, sab_hedef, [A])),
            ("KOL a2", "satir KAYIP sabote + YALNIZ parca sarti kalkti",
             motor_turet(kaynak, sab_hedef, [B])),
            ("KOL b ", "satir KAYIP sabote + YENI kural",
             motor_turet(kaynak, sab_hedef, [])),
            ("KOL c ", "M-H1s'ten siki=True kaldirildi (sabotaj YOK)",
             motor_turet(kaynak, None, [C])),
            ("KOL J ", "EK-1: %s symlink zorla basarisiz (junction kolu)" % JUNCTION_KIMLIK,
             motor_turet(kaynak, None, [J])),
        ]
    except Olculemedi as e:
        print("SONUC: OLCULEMEDI — motor turetilemedi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="isir_eslesme_")
    try:
        try:
            sablon = sablon_kur(motor, taban)
        except (Olculemedi, subprocess.TimeoutExpired) as e:
            print("SONUC: OLCULEMEDI — %s" % e)
            return 2
        print("\n--- DINAMIK KOLLAR (kur+not+derle sablonu, her kol AYRI kopyada `isir`) ---")
        sonuc = {}
        with ThreadPoolExecutor(max_workers=3) as ex:
            isler = {ad.strip(): ex.submit(isir_kos, metin, sablon, taban,
                                           ad.strip().replace(" ", "_"))
                     for ad, _, metin in turevler}
            for ad, is_ in isler.items():
                try:
                    sonuc[ad] = is_.result()
                except Olculemedi as e:
                    sonuc[ad] = e
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    kirmizi, olculemeyen = 0, 0
    _tum_pozisyon_kimlik = [a for _, hd in POZISYON_GRUPLARI for a in hd]
    # M-H9 mutant_git'tir: bu betigin sablonu git'SIZ kurulur -> UYGULANMAZ (gercek
    # davranisi sabotaj.py #4629 KAPSAMLI + isir_uygulanmaz_mutanti KOL 2 olcer).
    # M-HLINK de benzeri: hardlink kurulamayan bir dosya sisteminde UYGULANMAZ olabilir (sebep basilir,
    # sahte KACTI/ISIRDI yok); hardlink kurulan ortamda ISIRDI beklenir.
    _tek_mutant = [x for x in TEK_TANIK_HEDEF if x not in ("M-H9", "M-HLINK")]
    beklenen = {
        "KOL 0": ("H1'in yedi, H11/H6/H8/H16'nin TUM ve tek tanik mutantlari ISIRDI "
                  "(M-H9: git'siz sablonda UYGULANMAZ), exit 0",
                  lambda k, h: k == 0 and all(h.get(x) == "ISIRDI"
                                              for x in list(HEDEF_EKSEN) + _tum_pozisyon_kimlik
                                              + _tek_mutant)
                  and h.get("M-H9") in ("ISIRDI", "UYGULANMAZ")
                  and h.get("M-HLINK") in ("ISIRDI", "UYGULANMAZ")),
        "KOL a": ("M-H1 ISIRDI (maskeleme URETILDI)",
                  lambda k, h: h.get("M-H1") == "ISIRDI"),
        "KOL a1": ("M-H1 ve M-H1b KACTI (B tek basina yeter)",
                   lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL a2": ("M-H1 ve M-H1b KACTI (A tek basina yeter)",
                   lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL b": ("M-H1 ve M-H1b KACTI",
                  lambda k, h: h.get("M-H1") == "KACTI" and h.get("M-H1b") == "KACTI"),
        "KOL c": ("M-H1s KACTI ya da KURULAMADI",
                  lambda k, h: h.get("M-H1s") in ("KACTI", "KURULAMADI")),
        "KOL J": ("Windows'ta %s ISIRDI (junction'a dustu); Windows disinda "
                  "KURULAMADI (durustce SINANMADI, asla sahte KACTI/ISIRDI)" % JUNCTION_KIMLIK,
                  lambda k, h: h.get(JUNCTION_KIMLIK) == ("ISIRDI" if os.name == "nt"
                                                           else "KURULAMADI")),
    }
    for ad, aciklama, _ in turevler:
        ad = ad.strip()
        r = sonuc[ad]
        if isinstance(r, Olculemedi):
            print("  %-6s %-46s -> OLCULEMEDI: %s" % (ad, aciklama, r))
            olculemeyen += 1
            continue
        k, h, _c = r
        ozet = " ".join("%s=%s" % (x, h.get(x, "-")) for x in sorted(HEDEF_EKSEN))
        tanim, olcut = beklenen[ad]
        tamam = olcut(k, h)
        print("  %-6s %-46s -> %s" % (ad, aciklama, "BEKLENDIGI GIBI" if tamam else "BEKLENMEDIK"))
        print("         isir exit %d · %s" % (k, ozet))
        if ad == "KOL 0":
            for etiket, hedef_map in POZISYON_GRUPLARI:
                print("         %-3s: %s" % (etiket, " ".join(
                    "%s=%s" % (x, h.get(x, "-")) for x in sorted(hedef_map))))
            print("         TEK: %s" % " ".join(
                "%s=%s" % (x, h.get(x, "-")) for x in sorted(TEK_TANIK_HEDEF)))
        print("         beklenen: %s" % tanim)
        if ad == "KOL c" and tamam:
            print("         OLCULDU: M-H1s `siki`siz -> %s" % h.get("M-H1s"))
        if ad == "KOL J":
            print("         OLCULDU: platform=%s -> %s=%s" % (os.name, JUNCTION_KIMLIK, h.get(JUNCTION_KIMLIK)))
        if not tamam:
            kirmizi += 1
    print()
    if kirmizi:
        print("SONUC: KIRMIZI — %d kol beklenmedik (kural/parca/siki sozlesmesi tutmuyor)."
              % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kol kosulamadi; sessiz PASS verilmez." % olculemeyen)
        return 2
    print("SONUC: YESIL — KOL O temiz; maskeleme eski kuralla URETILDI, A ve B ayri "
          "ayri yetiyor, yeni kuralda M-H1/M-H1b KACTI, `siki` parametresi CANLI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

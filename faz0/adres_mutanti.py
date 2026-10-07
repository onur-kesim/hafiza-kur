#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ADRES MUTANTI (besli-paket/IS_EMRI_P2_ADRES_DEFTERI.md, 7 Eki 2026, Onur kilidi 6-7 Eki: P2 `hafiza.py` icine, SARTLI).

NEDEN VAR
  `hafiza.py adres` (kod adres defteri: tanim + cagiranlar) iki sey vaat eder: (1) cevap DOGRUDUR (yol + satir araligi + govde
  parmak izi), (2) cevap GIZLENEMEZ bayatlayabilir ve `kapi`yi/`derle`yi/`not`u ETKILEMEZ. Bu betik her vaadi AYRI bir kolda ve AYRI
  bir EKSENDE sinar; her kolun sabotaji YALNIZ kendi ekseninde isirir, ortusme raporlanir (gizlenmez).

KOLLAR (her biri ayri etiketli eksenler; beklentiler FIKSTURDEN ELLE yazilidir — motor sabitinden DEGIL: paylasilan kural = paylasilan korluk)
  A-TANIM        dort dilin (py/cs/dart/ts) fikstur dosyalarinda bilinen DORT tanim dogru yol + satir araligiyla     [TANIM-PY|CS|DART|TS]
  A-CAGIRAN      bilinen cagri listede (CAGIRAN-VAR); cagri silinince listeden DUSER (CAGIRAN-DUSER); tanim satiri cagiran
                 sayilmaz (CAGIRAN-TANIM-HARIC)
  A-PARMAK       govde degisince iz DEGISIR (PARMAK-DEGISIR); yalniz satir sonu bosluk (PARMAK-BOSLUK) / CRLF (PARMAK-CRLF) degisince AYNI
  A-BAYAT        dosya degisince ilk satir `ADRES DEFTERI BAYAT: 1 dosya degisti` + exit 1 (BAYAT-VAR); degismeyince sessiz exit 0 (BAYAT-YOK)CIKIS KODU  0 tum kollar temiz + olculebilen her sabotaj ISIRDI · 1 kol BEKLENMEDIK / sabotaj KACTI ·
            2 OLCULEMEDI (git yok, capa uymadi, duzenek kurulamadi)
"""
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
KOL_SIRASI = ("A-TANIM", "A-CAGIRAN", "A-PARMAK", "A-BAYAT")
KOL_ETIKET = {"A-TANIM": "TANIM", "A-CAGIRAN": "CAGIRAN", "A-PARMAK": "PARMAK", "A-BAYAT": "BAYAT"}
UZUN_YOL_ADET = 600                     # 600 x 72 kr = 43.200 kr > 32.767 (Windows komut satiri siniri); kisa izole TEMP'te tek yol < 260


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


# ------------------------------------------------------------------ FIKSTURLER (satir numaralari ELLE; degistirirsen BEKLENEN'i de)

PY_FX = '''"""Fikstur."""

SABIT = 5


class Kasa:
    """Kasa."""

    def ac(self, x):
        return x + 1


def hesapla(a, b):
    if a:
        return a
    return b
'''
CS_FX = '''namespace Demo;

public sealed class Kasa(int baslangic)
{
    private readonly int _deger = baslangic;

    public int Ac(int x)
    {
        return x + _deger;
    }

    public int Kapat() => 0;
}
'''
DART_FX = '''const String sabit = 'x';

class Kasa {
  int ac(int x) {
    return x + 1;
  }

  String get ad => 'kasa';
}
'''
TS_FX = '''export const SABIT = 5;

export class Kasa {
  ac(x: number): number {
    return x + 1;
  }
}

export const hesapla = (a: number) => a + 1;
'''
FIKSTUR = {"py": ("src/fx.py", PY_FX), "cs": ("src/Fx.cs", CS_FX), "dart": ("src/fx.dart", DART_FX), "ts": ("src/fx.ts", TS_FX)}
# (tur, nitelikli ad, bas, bit): ELLE yazildi
BEKLENEN = {
    "py": [("sabit", "SABIT", 3, 3), ("sinif", "Kasa", 6, 10), ("metot", "Kasa.ac", 9, 10), ("fonksiyon", "hesapla", 13, 16)],
    "cs": [("sinif", "Kasa", 3, 13), ("alan", "Kasa._deger", 5, 5), ("metot", "Kasa.Ac", 7, 10), ("metot", "Kasa.Kapat", 12, 12)],
    "dart": [("sabit", "sabit", 1, 1), ("sinif", "Kasa", 3, 9), ("metot", "Kasa.ac", 4, 6), ("ozellik", "Kasa.ad", 8, 8)],
    "ts": [("sabit", "SABIT", 1, 1), ("sinif", "Kasa", 3, 7), ("metot", "Kasa.ac", 4, 6), ("fonksiyon", "hesapla", 9, 9)],
}
CAGIRAN_ANA = '''public class Kullan
{
    public int Calis(Kasa k)
    {
        return k.Ac(1);
    }
}
'''
CAGIRAN_SILINMIS = CAGIRAN_ANA.replace("return k.Ac(1);", "return 1;")
PARMAK_PY = '''def f(a):
    b = a + 1
    return b
'''


# ------------------------------------------------------------------ yardimcilar

def _cikti_kodlamasi_ortami():
    return dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", GIT_CONFIG_NOSYSTEM="1",
                GIT_AUTHOR_NAME="adr", GIT_AUTHOR_EMAIL="adr@example.invalid",
                GIT_COMMITTER_NAME="adr", GIT_COMMITTER_EMAIL="adr@example.invalid")


def _git(kok, *args):
    return subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"] + list(args),
                          capture_output=True, env=_cikti_kodlamasi_ortami())


def _yaz(yol, metin, crlf=False):
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    veri = metin.replace("\n", "\r\n") if crlf else metin
    with io.open(yol, "w", encoding="utf-8", newline="") as f:
        f.write(veri)


def _sil(yol):
    def onar(fonk, p, *_):
        try:
            os.chmod(p, stat.S_IRWXU)
            fonk(p)
        except OSError:
            return
    if sys.version_info >= (3, 12):
        shutil.rmtree(yol, onexc=onar)
    else:
        shutil.rmtree(yol, onerror=onar)


def proje(taban, ad, dosyalar):
    """`dosyalar` {goreli yol: metin} ile git deposu kurar (tek commit). DONER kok."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    for y, m in dosyalar.items():
        _yaz(os.path.join(kok, *y.split("/")), m)
    _git(kok, "add", "-A")
    if _git(kok, "commit", "-q", "-m", "ilk").returncode != 0:
        raise Kurulamadi("git commit basarisiz")
    return kok


def kos(motor, kok, *args):
    """Motoru ALT SUREC olarak kosar -> (exit, stdout, stderr)."""
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(args) + ["--kok", kok], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=_cikti_kodlamasi_ortami())
    return r.returncode, r.stdout, r.stderr


def kur(motor, kok):
    kod, o, e = kos(motor, kok, "adres", "--kur")
    if kod != 0:
        raise Kurulamadi("adres --kur basarisiz (exit=%s): %s" % (kod, (o + e).strip()[-200:]))


def defter(kok):
    """ADRES.tsv -> (baslik satiri, [(yol, tur, ad, bas, bit, iz)])."""
    p = os.path.join(kok, "arsiv", "hafiza", "ADRES.tsv")
    with io.open(p, encoding="utf-8", newline="") as f:
        sat = f.read().split("\n")
    return sat[0], [tuple(s.split("\t")) for s in sat[1:] if s]


def tanimlar(kok, yol):
    return [(r[1], r[2], int(r[3]), int(r[4])) for r in defter(kok)[1] if r[0] == yol and r[1] != "dosya"]


def iz(kok, yol, ad):
    return [r[5] for r in defter(kok)[1] if r[0] == yol and r[2] == ad][0]


# ------------------------------------------------------------------ KOLLAR (her biri [(etiket, mesaj)] = bulgular)

def kol_tanim(motor, taban):
    """A-TANIM: dort dilin fikstur dosyasinda bilinen tanimlar (tur, ad, satir araligi) — TAM esitlik."""
    b = []
    kok = proje(taban, "tanim", dict((yol, m) for yol, m in FIKSTUR.values()))
    kur(motor, kok)
    for dil, (yol, _m) in sorted(FIKSTUR.items()):
        bulunan, beklenen = sorted(tanimlar(kok, yol)), sorted(BEKLENEN[dil])
        if bulunan != beklenen:
            b.append(("TANIM-%s" % dil.upper(), "%s: bulunan %r != beklenen %r" % (yol, bulunan, beklenen)))
    return b


def _cagiranlar(cikti):
    """`adres <ad>` ciktisinin CAGIRANLAR satirlari."""
    bolum = cikti.split("CAGIRANLAR")
    return [l.strip() for l in bolum[1].split("\n")[1:] if l.startswith("  ") and "NOT:" not in l] if len(bolum) > 1 else []


def kol_cagiran(motor, taban):
    """A-CAGIRAN: bilinen cagri listede · cagri silinince DUSER · tanim satiri kendini cagiran SAYILMAZ."""
    b = []
    kok = proje(taban, "cagiran", {"src/Kasa.cs": CS_FX, "src/Kullan.cs": CAGIRAN_ANA})
    kur(motor, kok)
    kod, o, _e = kos(motor, kok, "adres", "Ac")
    liste = _cagiranlar(o)
    if not any(l.startswith("src/Kullan.cs") and l.endswith(":5") for l in liste):
        b.append(("CAGIRAN-VAR", "bilinen cagri (src/Kullan.cs:5) listede YOK: exit=%s liste=%r" % (kod, liste)))
    if any(l.startswith("src/Kasa.cs") and ":7" in l for l in liste):
        b.append(("CAGIRAN-TANIM-HARIC", "tanim satiri (src/Kasa.cs:7) kendini cagiran SAYILDI: %r" % liste))
    _yaz(os.path.join(kok, "src", "Kullan.cs"), CAGIRAN_SILINMIS)
    kur(motor, kok)
    kod, o, _e = kos(motor, kok, "adres", "Ac")
    if any(l.startswith("src/Kullan.cs") for l in _cagiranlar(o)):
        b.append(("CAGIRAN-DUSER", "cagri silindi ama src/Kullan.cs hala cagiran: %r" % _cagiranlar(o)))
    return b


def kol_parmak(motor, taban):
    """A-PARMAK: govde degisince iz degisir; yalniz satir sonu bosluk / CRLF degisince AYNI."""
    b = []
    kok = proje(taban, "parmak", {"src/f.py": PARMAK_PY})
    yol = os.path.join(kok, "src", "f.py")
    kur(motor, kok)
    ilk = iz(kok, "src/f.py", "f")
    _yaz(yol, PARMAK_PY.replace("a + 1", "a + 2"))
    kur(motor, kok)
    if iz(kok, "src/f.py", "f") == ilk:
        b.append(("PARMAK-DEGISIR", "govde degisti ama parmak izi AYNI (%s)" % ilk))
    _yaz(yol, "".join(s + "   \t\n" for s in PARMAK_PY.split("\n")[:-1]))
    kur(motor, kok)
    if iz(kok, "src/f.py", "f") != ilk:
        b.append(("PARMAK-BOSLUK", "yalniz satir sonu boslugu degisti ama iz DEGISTI (%s -> %s)" % (ilk, iz(kok, "src/f.py", "f"))))
    _yaz(yol, PARMAK_PY, crlf=True)
    kur(motor, kok)
    if iz(kok, "src/f.py", "f") != ilk:
        b.append(("PARMAK-CRLF", "yalniz CRLF'e cevrildi ama iz DEGISTI (%s -> %s)" % (ilk, iz(kok, "src/f.py", "f"))))
    return b


def kol_bayat(motor, taban):
    """A-BAYAT: dosya degisince BAYAT + exit 1; degismeyince sessiz exit 0."""
    b = []
    kok = proje(taban, "bayat", {"src/fx.ts": TS_FX})
    kur(motor, kok)
    kod, o, _e = kos(motor, kok, "adres", "Kasa")
    if kod != 0 or "BAYAT" in o:
        b.append(("BAYAT-YOK", "degismeyen agacta exit=%s ya da BAYAT basildi: %r" % (kod, o.split("\n")[0])))
    _yaz(os.path.join(kok, "src", "fx.ts"), TS_FX + "// yeni satir\n")
    kod, o, _e = kos(motor, kok, "adres", "Kasa")
    if kod != 1 or not o.startswith("ADRES DEFTERI BAYAT: 1 dosya degisti"):
        b.append(("BAYAT-VAR", "dosya degisti ama exit=%s ilk satir=%r" % (kod, o.split("\n")[0])))
    return b


# kol adi -> kosucu(motor, kol_tabani, ad, motor_kaynagi) -> [(etiket, mesaj)]
KOLLAR = {
    "A-TANIM": lambda m, t, _a, _k: kol_tanim(m, t),
    "A-CAGIRAN": lambda m, t, _a, _k: kol_cagiran(m, t),
    "A-PARMAK": lambda m, t, _a, _k: kol_parmak(m, t),
    "A-BAYAT": lambda m, t, _a, _k: kol_bayat(m, t),
}


def _motor_yaz(metin, hedef_dizin, ad):
    try:
        compile(metin, "<%s>" % ad, "exec")
    except SyntaxError as e:
        return None, "motor derlenmiyor: %s" % e
    os.makedirs(hedef_dizin, exist_ok=True)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(metin)
    return p, None


def hepsi(motor, taban, ad, kaynak, kollar):
    """Secili kollarin bulgulari -> [(etiket, mesaj)]; A-KOMUT-SATIRI Windows disinda `OLCULEMEDI-WIN`."""
    b = []
    for k in kollar:
        b += KOLLAR[k](motor, os.path.join(taban, "k_" + ad), ad, kaynak)
    return b


# ------------------------------------------------------------------ SABOTAJLAR
# (ad, kol, etiket, ankor, yeni): ankor motorda TAM 1 kez gecmeli (aksi OLCULEMEDI). `etiket` = o sabotajin KENDI ekseni.
SABOTAJLAR = (
    ("M-T1 Python cikaricisi kapali", "A-TANIM", "TANIM-PY",
     '    if dil == "py":\n        return _ad_py(metin)\n',
     '    if dil == "py":\n        return []      # MUTANT\n'),
    ("M-T2 C# cikaricisi kapali", "A-TANIM", "TANIM-CS",
     "    S = _ad_hazirla(dil, metin)\n    cikti = []\n",
     '    if dil == "cs":      # MUTANT\n        return []\n    S = _ad_hazirla(dil, metin)\n    cikti = []\n'),
    ("M-T3 Dart cikaricisi kapali", "A-TANIM", "TANIM-DART",
     "    S = _ad_hazirla(dil, metin)\n    cikti = []\n",
     '    if dil == "dart":      # MUTANT\n        return []\n    S = _ad_hazirla(dil, metin)\n    cikti = []\n'),
    ("M-T4 TS/JS cikaricisi kapali", "A-TANIM", "TANIM-TS",
     "    S = _ad_hazirla(dil, metin)\n    cikti = []\n",
     '    if dil == "ts":      # MUTANT\n        return []\n    S = _ad_hazirla(dil, metin)\n    cikti = []\n'),
    ("M-C1 tanim satiri HARIC tutulmaz (tanim kendini cagiran sanilir)", "A-CAGIRAN", "CAGIRAN-TANIM-HARIC",
     "            if (yol, satir) not in tanim_satiri:\n",
     "            if True:      # MUTANT\n"),
    ("M-C2 cagiranlar HIC aranmaz", "A-CAGIRAN", "CAGIRAN-VAR",
     "        arama = _adres_arama(adlar[0]) if len(adlar) == 1 else None\n",
     "        arama = None      # MUTANT\n"),
    ("M-P1 satir sonu normallestirmesi KAPALI (CRLF + bosluk)", "A-PARMAK", "PARMAK-CRLF",
     '    s = _ADRES_SON_BOSLUK.sub("", _ADRES_SATIR_SONU.sub("\\n", s))\n',
     "    s = s      # MUTANT\n"),
    ("M-P2 yalniz satir sonu BOSLUGU kirpilmaz (CRLF hala cevrilir)", "A-PARMAK", "PARMAK-BOSLUK",
     '_ADRES_SON_BOSLUK = re.compile(r"(?<![ \\t])[ \\t]+(?=\\n|\\Z)")',
     '_ADRES_SON_BOSLUK = re.compile(r"(?!)")  # MUTANT: '),
    ("M-P3 parmak izi SABIT (govde degisince degismez)", "A-PARMAK", "PARMAK-DEGISIR",
     '    return _adres_sha("\\n".join(satirlar[bas - 1:bit]))[:8]\n',
     '    return "00000000"      # MUTANT\n'),
    ("M-B1 agac ozeti karsilastirmasi KAPALI (bayat hic bildirilmez)", "A-BAYAT", "BAYAT-VAR",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != baslik.get("ozet")\n',
     "    bayat = False      # MUTANT\n"),
    ("M-B2 agac ozeti HER ZAMAN farkli (degismeyen agac bayat sanilir)", "A-BAYAT", "BAYAT-YOK",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != baslik.get("ozet")\n',
     "    bayat = True      # MUTANT\n"),
)


def main():
    yol = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else VARSAYILAN)
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok.")
        return 2
    kollar = list(KOL_SIRASI)
    print(CIZGI)
    print("ADRES MUTANTI — motor: %s · platform: %s" % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="adr_")
    try:
        try:
            temiz = hepsi(yol, os.path.join(taban, "t"), "temiz", s, kollar)
        except Kurulamadi as e:
            print("SONUC: OLCULEMEDI — duzenek kurulamadi (arac kusuru, kapi kor DEGIL): %s" % e)
            return 2
        olcul = [x for x in temiz if x[0] == "OLCULEMEDI-WIN"]
        kotu = [x for x in temiz if x[0] != "OLCULEMEDI-WIN"]
        for k in kollar:
            on = KOL_ETIKET[k]
            kolun = [x for x in kotu if x[0] == on or x[0].startswith(on + "-")]
            sinirli = k == "A-KOMUT-SATIRI" and olcul
            print("  %-15s : %s" % (k, ("OLCULEMEDI: bu platformda sinir yok (Windows komut satiri sinirina ozgu; beyanli, sessiz YESIL degil)"
                                        if sinirli else ("TEMIZ" if not kolun else "BEKLENMEDIK"))))
        for et, m in kotu:
            print("      ! %s: %s" % (et, m))
        if kotu:
            print("\nSONUC: KIRMIZI — temiz motorun kollari BEKLENMEDIK.")
            return 1
        print("\n--- SABOTAJLAR (her biri KENDI ekseninde ISIRMALI; ortusme raporlanir) ---")
        kacan, olculemeyen = [], []
        for sira, (ad, kol, etiket, ankor, yeni) in enumerate(SABOTAJLAR, 1):
            if kol not in kollar:
                continue
            if etiket == "KOMUT-SATIRI" and os.name != "nt":
                print("  %-60s -> OLCULEMEDI: bu platformda sinir yok (yalniz Windows'ta isirir)" % ad)
                olculemeyen.append(ad)
                continue
            n = s.count(ankor)
            if n != 1:
                print("SONUC: OLCULEMEDI — %s: capa %d yerde gecti (1 olmali): %r" % (ad, n, ankor.strip()[:70]))
                return 2
            sab, hata = _motor_yaz(s.replace(ankor, yeni, 1), os.path.join(taban, "s%d" % sira), "s%d" % sira)
            if sab is None:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, hata))
                return 2
            try:
                atesler = {e for e, _ in hepsi(sab, os.path.join(taban, "ks%d" % sira), "s%d" % sira, io.open(sab, encoding="utf-8", newline="").read(), [kol])}
            except Kurulamadi as e:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, e))
                return 2
            atesler -= {"OLCULEMEDI-WIN"}
            if etiket in atesler:
                ort = sorted(atesler - {etiket})
                print("  %-60s -> ISIRDI ✓  (%s%s)" % (ad, etiket, ("; ortusme: " + ", ".join(ort)) if ort else ""))
            else:
                print("  %-60s -> KACTI ✗  (%s ekseni sabotajda TEMIZ; atesleyen: %s)" % (ad, etiket, ", ".join(sorted(atesler)) or "hicbiri"))
                kacan.append(ad)
        print(CIZGI)
        if kacan:
            print("SONUC: KIRMIZI — KACTI: %s" % "; ".join(kacan))
            return 1
        if olculemeyen:
            print("SONUC: YESIL (SINIRLI) — olculebilen her sabotaj ISIRDI; %d OLCULEMEDI (Windows'a ozgu)." % len(olculemeyen))
        else:
            print("SONUC: YESIL — tum kollar temiz, %d sabotaj AYRI eksende ISIRDI." % len(SABOTAJLAR))
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ADRES MUTANTI (besli-paket/IS_EMRI_P2_ADRES_DEFTERI.md, 7 Eki 2026, Onur kilidi 6-7 Eki: P2 `hafiza.py` icine, SARTLI).

NEDEN VAR
  `hafiza.py adres` (kod adres defteri: tanim + cagiranlar) iki sey vaat eder: (1) cevap DOGRUDUR (yol + satir araligi + govde
  parmak izi), (2) cevap GIZLENEMEZ bayatlayabilir ve `kapi`yi/`derle`yi/`not`u ETKILEMEZ. Bu betik her vaadi AYRI bir kolda ve AYRI
  bir EKSENDE sinar; her kolun sabotaji YALNIZ kendi ekseninde isirir, ortusme raporlanir (gizlenmez).

KOLLAR (her biri ayri etiketli eksenler; beklentiler FIKSTURDEN ELLE yazilidir — motor sabitinden DEGIL: paylasilan kural = paylasilan korluk)
  A-TANIM        dort dilin (py/cs/dart/ts) fikstur dosyalarinda bilinen DORT tanim dogru yol + satir araligiyla     [TANIM-PY|CS|DART|TS]
                 + bozuk TS girdisinde (bitmemis yorum = uzun bosluk dizisi; uzun satir sonu dizisi) `--kur` zaman asimina
                 UGRAMAZ: sure DOGRUSAL (P2-ONCEDEN-01)                                                                [TANIM-TS-SURE]
  A-CAGIRAN      bilinen cagri listede (CAGIRAN-VAR); cagri silinince listeden DUSER (CAGIRAN-DUSER); tanim satiri cagiran
                 sayilmaz (CAGIRAN-TANIM-HARIC)
                 + (KALEM 4) ham bayt on suzmesi hem soguk hem SICAK onbellekte cagriyi KACIRMAZ: UTF-16 BOM'lu dosya (CAGIRAN-KODLAMA) ·
                 ad baytlarini bolen ortadaki U+FEFF (CAGIRAN-FEFF) · ASCII-disi ad + latin-1 dosya (CAGIRAN-ASCII-DISI)
  A-PARMAK       govde degisince iz DEGISIR (PARMAK-DEGISIR); yalniz satir sonu bosluk (PARMAK-BOSLUK) / CRLF (PARMAK-CRLF) degisince AYNI
  A-BAYAT        dosya degisince ilk satir `ADRES DEFTERI BAYAT: 1 dosya degisti` + exit 1 (BAYAT-VAR); degismeyince sessiz exit 0 (BAYAT-YOK)
                 + (KALEM 4, P2.1) sorgu onbellegi dogrulugu DEGISTIRMEZ: SICAK onbellekle degisiklik (BAYAT-VAR) · git add (BAYAT-STAGE) ·
                 commit (BAYAT-COMMIT) · ayni mtime + farkli boyut (BAYAT-BOYUT) · ayni boyut + korunmus mtime, onbellek taze = RACY
                 (BAYAT-ZAMAN) · icerik degisti + `--kur` yenilendi, eski deftere bagli onbellek kullanilmaz, BAYAT YOK (BAYAT-KUR) ·
                 bozuk onbellek (BAYAT-ONB-BOZUK) / yazilamayan onbellek (BAYAT-ONB-YAZ) TAM yola duser, komut dusmez · gecici dizin
                 proje icindeyse onbellek KAPALI, projeye dosya eklenmez (BAYAT-ONB-PROJE). `adres` icin TEMP projeye ozel dizine yonlenir.
                 + PAY'dan ESKI dosyada ayni boyut + os.utime ile GERI ALINMIS mtime ile icerik degisikligi GORULUR (POSIX ve WINDOWS):
                 anahtara degisiklik zamani girer (POSIX st_ctime; Windows NTFS/ReFS ChangeTime, ctypes) (BAYAT-CTIME) · POSIX: ctime
                 kaymasi okunamaz (chmod 000) dosyayi da yeniden okutur (BAYAT-OKUNMAZ) · 1e999 gibi tasan sayili bozuk onbellek TAM
                 yola duser (BAYAT-ONB-BOZUK). Racy korumasi ve `--kur` baglamasi degisiklik zamaninin YANINDA sinanir: bu iki
                 sabotaj onu da kor eder (aksi halde o onlari ortuk korurdu).
                 BILINEN SINIR (sabotajla DEGIL, beyanla; Windows): NTFS/ReFS DISI birimde (FAT/exFAT) ChangeTime anlamsiz: onbellek
                 KAPALI, tam yol (dogruluk korunur, hiz kazanci yok). FAT'ta bu kapali yol OLCULEMEDI (FAT birimi yok).
  A-DETERMINIZM  iki `--kur` bit-bit ayni (DETERMINIZM-AYNI); satirlar kanonik sirada (DETERMINIZM-SIRA: dort dil, adlari DIL SIRASINA
                 ters serpistirilmis dosyalar — siralama kapaliysa dil gruplamasi gorunur)
  A-MASKE        (KALEM 2, P2.1) cagiran listesinde yorum/dize ici gecis YOK: ayni ad bir gercek cagri + bir yorumda + bir dizede +
                 bir interpolasyon deliginde (gercek cagri) -> liste yalniz gercekleri sayar, "NOT: 2 yorum/metin icindeki gecis
                 sayilmadi" beyan edilir; dort dil (C# Dart Python TS/TSX) + Dart `$ad` + maske kurulamayan dosya (ham taranir, BILDIRILIR)
                 + JSX bilesen etiketi (`<Kart/>` `</Kart>`) GERCEK cagri, kucuk harfli HTML etiketi (`<sekme/>`) degil + Python dize
                 onek harfi (`f"..` `rb".."`) dizenin parcasi + C# ham interpolasyonlu dize deligi (`$$` + 3 tirnak + `{{X()}}`) kod, metni degil +
                 Python bicim belirteci (`f"{x:ad}"`) ve C# bicim belirteci (`$"{x,10:ad}"`; `global::` takma adi DEGIL) kod DEGIL, ic ice
                 `{..}` kod + 30 ic ice f-dize ZAMAN ASIMINA ugramaz (K-1) + maske ARAC KUSURU yutulmaz (exit 3)
                                                                                                  [MASKE|-GERCEK|-DELIK|-NOT|-HAM|-KUSUR|-DERIN]
  A-ATLA         (KALEM 3, P2.1) gomulu/uretilmis dosyalar (.yarn/ node_modules/ vendor/ dist/ build/ dizin bilesenleri, *.min.js, *.cjs;
                 izlenmis olsalar bile) TARANMAZ: tanim/cagiran listesinde YOK, defterde dosya satiri YOK, bayatlik saymaz; atlanma
                 `--kur` konsolunda (`ATLANAN: n dosya (...)`) ve ADRES.tsv basliginda (`atlanan=`) BEYAN edilir; `src/build_tools/`
                 ve `src/Dist/` (buyuk harf) atlanMAZ; atlama kapsam-disi sayimindan ONCE (atlanan dosya KAPSAM DISI'na girmez);
                 git'siz dosya sistemi kipinde de ayni suzgec                                          [ATLA|-BEYAN|-BAYAT]
  A-ETKI         iki eksen. (1) CALISMA ANI: adres cikaricisi BILEREK bozukken `kapi` · `kapi --siki` · `devral --kesif` ciktisi (exit +
                 stdout + stderr) BAYT-BAYT ayni (ETKI). (2) YUKLEME ANI (KALEM 1, P2.1): adres desen/tablo ogesine YUKLEMEDE patlayan
                 gecersiz regex enjekte edilmis motorda `kapi` · `kapi --siki` · `devral --kesif` · `not` · `derle` ciktisi (kok yolu ve
                 gun/saat normallestirilmis) temizle BAYT-BAYT ayni ve `adres --kur` exit 3 (ARAC KUSURU) (ETKI-YUKLEME)
  A-KOMUT-SATIRI YALNIZ Windows: 43.200 karakterlik yol kumesinde `--kur` COKMEZ, kaynak=git (KOMUT-SATIRI); Linux/macOS: OLCULEMEDI beyani

CIKIS KODU  0 tum kollar temiz + olculebilen her sabotaj ISIRDI · 1 kol BEKLENMEDIK / sabotaj KACTI ·
            2 OLCULEMEDI (git yok, capa uymadi, duzenek kurulamadi)
"""
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
KOL_SIRASI = ("A-TANIM", "A-CAGIRAN", "A-PARMAK", "A-BAYAT", "A-DETERMINIZM", "A-MASKE", "A-ATLA", "A-ETKI", "A-EZME", "A-EKSIK",
             "P5-DAMGA", "A-KOMUT-SATIRI")
KOL_ETIKET = {"A-TANIM": "TANIM", "A-CAGIRAN": "CAGIRAN", "A-PARMAK": "PARMAK", "A-BAYAT": "BAYAT", "A-DETERMINIZM": "DETERMINIZM", "A-MASKE": "MASKE", "A-ATLA": "ATLA", "A-ETKI": "ETKI", "A-EZME": "EZME", "A-EKSIK": "EKSIK", "P5-DAMGA": "DAMGA", "A-KOMUT-SATIRI": "KOMUT-SATIRI"}
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
CAGIRAN_FEFF = CAGIRAN_ANA.replace("k.Ac(1)", "k.A﻿c(1)")       # ortada U+FEFF: ham baytlarda `Ac` YOK; metne cevrilince U+FEFF silinir
KAFE_AD = "Café"                                                # ASCII-disi ad
KAFE_CS = "public class Kafe\n{\n    public int %s()\n    {\n        return 1;\n    }\n}\n" % KAFE_AD
KAFE_CAGIRAN = ("public class KafeKullan\n{\n    public int Calis(Kafe k)\n    {\n        return k.%s();\n    }\n}\n" % KAFE_AD)   # latin-1 yazilir
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


def onb_dizini(kok):
    """`adres` sorgu onbellegi (motor: `tempfile.gettempdir()`) bu projeye OZEL dizine yonlenir: sistem TEMP'i kirlenmez, onbellek
    dosyasi bu dizinden bulunur (motorun anahtar hesabi KOPYALANMAZ: paylasilan kural = paylasilan korluk)."""
    d = kok.rstrip("/\\") + "_onb"
    os.makedirs(d, exist_ok=True)
    return d


def onb_dosyasi(kok):
    """Projenin onbellek dosyasi (yoksa None)."""
    d = onb_dizini(kok)
    bul = sorted(x for x in os.listdir(d) if x.startswith("hafiza-adres-") and not x.endswith(".tmp"))
    return os.path.join(d, bul[0]) if bul else None


def kos(motor, kok, *args, zaman_asimi=None, tmp=None):
    """Motoru ALT SUREC olarak kosar -> (exit, stdout, stderr). `zaman_asimi` asilirsa subprocess.TimeoutExpired.
    `tmp`: `adres` icin gecici dizin (varsayilan: projeye ozel `onb_dizini`)."""
    ortam = _cikti_kodlamasi_ortami()
    if args[:1] == ("adres",):
        d = tmp or onb_dizini(kok)
        ortam.update(TMPDIR=d, TEMP=d, TMP=d)
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(args) + ["--kok", kok], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=ortam, timeout=zaman_asimi)
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
    return b + kol_tanim_sure(motor, taban)


# DOGRUSALLIK (P2-ONCEDEN-01): bozuk/bitmemis girdide sure dogrusal kalir. (1) bitmemis yorum = uzun BOSLUK dizisi: bitisik `\s*`
# ciftleri/ucluleri desende n^2/n^3 geri izleme verir (eski motor 2 KB'de 30 s). (2) satir sonu dizisi: ASI hukmu dizinin HER satir
# sonu icin yeniden hesaplanirsa n^2 (eski motor 16 KB'de 22 s). Zaman asimi SABOTAJ bayragidir; saglam motor milisaniyeler tutar.
SURE_TS = {"src/yorum.ts": "class A {\n  async checkCu/*" + "x" * 4000 + "\n",
           "src/satir.ts": "class A {\n  foo =" + "\n" * 40000 + " 1\n}\n"}
SURE_ZAMAN_ASIMI = 20


def kol_tanim_sure(motor, taban):
    """A-TANIM (SURE): bozuk TS girdisinde `adres --kur` zaman asimina UGRAMAZ ve temiz biter."""
    kok = proje(taban, "sure", SURE_TS)
    try:
        kod, o, e = kos(motor, kok, "adres", "--kur", zaman_asimi=SURE_ZAMAN_ASIMI)
    except subprocess.TimeoutExpired:
        return [("TANIM-TS-SURE", "bozuk TS girdisinde `adres --kur` %d s icinde BITMEDI (dogrusal degil)" % SURE_ZAMAN_ASIMI)]
    if kod != 0:
        return [("TANIM-TS-SURE", "bozuk TS girdisinde `adres --kur` exit=%s: %r" % (kod, (o + e).strip()[-120:]))]
    return []


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
    return b + kol_cagiran_kodlama(motor, taban)


def _platform_sinir(etiket):
    """Etiketin ekseni bu platformda/kullanicida OLCULEMIYORSA nedeni (sabotaj da fikstur de atlanir, beyan edilir), yoksa None."""
    if etiket == "KOMUT-SATIRI" and os.name != "nt":
        return "bu platformda sinir yok (yalniz Windows'ta isirir)"
    if etiket == "BAYAT-OKUNMAZ" and (os.name == "nt" or os.geteuid() == 0):
        return "okuma izni yalniz POSIX'te ve root olmayan kullanicida sinanir"
    if etiket == "EKSIK-BELLEKTE" and os.name != "nt" and os.geteuid() == 0:
        return "yazma izni kontrolu root icin anlamsiz (root her dosyaya yazar)"
    return None


CTIME_BEKLE_SN = 3.3        # motorun racy payi (3 sn) + pay: fikstur dosyalarinin degisiklik zamani da "eski" olsun


def _ctime_yasla():
    """utime/yazma degisiklik zamanini (POSIX ctime, Windows ChangeTime) ILERLETIR (ayarlanamaz): onbellek girdisi olusabilmesi icin
    onun racy payindan eski olmasi beklenir (HER platformda)."""
    time.sleep(CTIME_BEKLE_SN)


def kol_cagiran_kodlama(motor, taban):
    """A-CAGIRAN (KALEM 4): cagiran aramasinin ham bayt on suzmesi cagriyi KACIRMAZ: UTF-16 BOM'lu dosya (ad baytlari NUL'larla ayrik;
    CAGIRAN-KODLAMA) · ad baytlarini bolen ortadaki U+FEFF (metne cevrilince silinir; CAGIRAN-FEFF) · ASCII-disi ad + latin-1 dosya
    (ad UTF-8 baytlariyla aranirsa dosya atlanir; CAGIRAN-ASCII-DISI). Dosyalar 1 saat ESKI: ucuncu sorgu SICAK onbellekten (on suzme
    yalniz orada isler; ikinci sorgu degisiklik zamani payi bekledikten sonra onbellegi doldurur). Her cagiran 5. satirda, her sorguda."""
    kok = proje(taban, "cagiran_kodlama", {"src/Kasa.cs": CS_FX})
    with io.open(os.path.join(kok, "src", "Kullan16.cs"), "wb") as f:
        f.write(CAGIRAN_ANA.encode("utf-16"))
    _yaz(os.path.join(kok, "src", "KullanFeff.cs"), CAGIRAN_FEFF)
    _yaz(os.path.join(kok, "src", "Kafe.cs"), KAFE_CS)
    with io.open(os.path.join(kok, "src", "KafeKullan.cs"), "wb") as f:
        f.write(KAFE_CAGIRAN.encode("latin-1"))
    eski = time.time_ns() - 3600 * 10 ** 9
    for ad in ("Kasa.cs", "Kullan16.cs", "KullanFeff.cs", "Kafe.cs", "KafeKullan.cs"):
        os.utime(os.path.join(kok, "src", ad), ns=(eski, eski))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "kodlama")
    kur(motor, kok)
    b = []
    sorgular = (("Ac", "src/Kullan16.cs", "CAGIRAN-KODLAMA", "UTF-16 BOM'lu"),
                ("Ac", "src/KullanFeff.cs", "CAGIRAN-FEFF", "ortada U+FEFF'li"),
                (KAFE_AD, "src/KafeKullan.cs", "CAGIRAN-ASCII-DISI", "latin-1 (ASCII-disi ad)"))
    for ne in ("soguk", "isinma", "sicak"):
        if ne == "isinma":
            _ctime_yasla()
        for ad, yol, etiket, ne_dosya in sorgular:
            kod, o, _e = kos(motor, kok, "adres", ad)
            if not any(l.startswith(yol) and l.endswith(":5") for l in _cagiranlar(o)):
                b.append((etiket, "%s onbellek: %s %s:5 cagirani listede YOK: exit=%s liste=%r" % (ne, ne_dosya, yol, kod, _cagiranlar(o))))
        if ne == "isinma" and onb_dosyasi(kok) is None:
            raise Kurulamadi("cagiran_kodlama: isinma turunda onbellek dosyasi YAZILMADI (sicak tur sicak olmaz)")
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
    return b + kol_bayat_onbellek(motor, taban)


# KALEM 4 (P2.1): sorgu onbellegi. Onbellek YALNIZ hiz icindir; bayatlik hukmu onunla DEGISMEZ. Eksenler (hepsi `fx.ts` tek dosya):
#   SICAK fikstur = dosya 1 saat ESKI (mtime) -> `--kur` -> bir sorgu (onbellek DOLAR: girdi racy degil). Onbellek girdisi BULUNUR.
ESKI_SANIYE = 3600
YENI_SATIR = TS_FX + "// yeni satir\n"
AYNI_BOYUT = TS_FX.replace("SABIT = 5", "SABIT = 6")        # ayni bayt sayisi, farkli icerik
YAN_TS = "export const YAN = 1;\n"
BAYAT_BIR = "ADRES DEFTERI BAYAT: 1 dosya degisti"


def _zamanla(yol, ns):
    os.utime(yol, ns=(ns, ns))


def _bayat_sorgu(motor, kok):
    kod, o, _e = kos(motor, kok, "adres", "Kasa")
    return kod, o


def _bayat_hukum(b, etiket, ne, sonuc, bayat):
    """`sonuc` = (exit, stdout). bayat=True: ilk satir `BAYAT: 1 dosya degisti` + exit 1. bayat=False: BAYAT YOK + exit 0."""
    kod, o = sonuc
    ilk = o.split("\n")[0]
    if bayat and (kod != 1 or not ilk.startswith(BAYAT_BIR)):
        b.append((etiket, "%s: exit=%s ilk satir=%r (BAYAT + exit 1 beklenir)" % (ne, kod, ilk)))
    if not bayat and (kod != 0 or "BAYAT" in o):
        b.append((etiket, "%s: exit=%s ilk satir=%r (sessiz exit 0 beklenir)" % (ne, kod, ilk)))


SICAK_ADLAR = ("bayat_sicak", "bayat_boyut", "bayat_kur", "bayat_bozuk", "bayat_proje", "bayat_ctime", "bayat_okunmaz")


def _sicak_kur(motor, taban, ad):
    """-> (kok, fx.ts yolu, eski mtime ns). Dosya ESKI -> `--kur`. (Onbellegi `_sicak_isit` doldurur.)"""
    kok = proje(taban, ad, {"src/fx.ts": TS_FX, "src/yan.ts": YAN_TS})
    yol = os.path.join(kok, "src", "fx.ts")
    eski = time.time_ns() - ESKI_SANIYE * 10 ** 9
    _zamanla(yol, eski)
    _zamanla(os.path.join(kok, "src", "yan.ts"), eski)      # degismeyen ESKI dosya: onbellek bos kalmaz (yazma denemesi olur)
    kur(motor, kok)
    return kok, yol, eski


def _sicak_isit(motor, kok):
    """Bir sorgu: onbellek dolar (degismeyen agac temiz)."""
    ilk = _bayat_sorgu(motor, kok)
    if onb_dosyasi(kok) is None:                       # exit'e BAKILMAZ: hukmu BAYAT-YOK kolu verir (sabotajli motorda 1 olabilir)
        raise Kurulamadi("sicak fikstur: ilk sorgu (exit=%s) onbellek dosyasi YAZMADI (%r)" % (ilk[0], ilk[1][:80]))


def _sicak_projeler(motor, taban):
    """Butun sicak fiksturleri BIR KEZ kurar: hepsi `--kur`lanir, degisiklik zamani payi BIR kez beklenir, sonra her biri isitilir
    (fikstur basina bekleme olmasin). -> {ad: (kok, fx.ts yolu, eski mtime ns)}."""
    p = dict((ad, _sicak_kur(motor, taban, ad)) for ad in SICAK_ADLAR)
    _ctime_yasla()
    for kok, _yol, _eski in p.values():
        _sicak_isit(motor, kok)
    return p


def kol_bayat_onbellek(motor, taban):
    """A-BAYAT (KALEM 4): onbellekli ucuz yol dogrulugu DEGISTIRMEZ. Sicak onbellekle: sessiz agac temiz (BAYAT-YOK) · degisiklik
    (BAYAT-VAR) · `git add` (BAYAT-STAGE) · commit (BAYAT-COMMIT) · ayni mtime + FARKLI boyut (BAYAT-BOYUT) · ayni boyut + korunmus
    mtime, onbellek taze (BAYAT-ZAMAN: racy) · icerik `--kur`dan once degisti (BAYAT-KUR: eski deftere bagli onbellek kullanilmaz)
    · ayni boyut + GERI ALINMIS ESKI mtime (BAYAT-CTIME; Windows'ta NTFS ChangeTime) · okunamaz dosya (BAYAT-OKUNMAZ, POSIX, root degil)
    · bozuk / yazilamayan onbellek TAM yola duser (BAYAT-ONB-BOZUK / BAYAT-ONB-YAZ)."""
    b = []
    sp = _sicak_projeler(motor, taban)
    kok, yol, eski = sp["bayat_sicak"]
    _bayat_hukum(b, "BAYAT-YOK", "sicak onbellek, degismeyen agac", _bayat_sorgu(motor, kok), False)
    _yaz(yol, YENI_SATIR)
    _bayat_hukum(b, "BAYAT-VAR", "sicak onbellek, dosya degisti", _bayat_sorgu(motor, kok), True)
    _git(kok, "add", "-A")
    _bayat_hukum(b, "BAYAT-STAGE", "degisiklik git add edildi", _bayat_sorgu(motor, kok), True)
    _git(kok, "commit", "-q", "-m", "degisti")
    _bayat_hukum(b, "BAYAT-COMMIT", "degisiklik commit edildi", _bayat_sorgu(motor, kok), True)
    return b + kol_bayat_ctime(motor, sp) + kol_bayat_zaman(motor, taban, sp)


def kol_bayat_ctime(motor, sp):
    """A-BAYAT (K4-02/K4-04/K4-W1 duzeltmesi): sicak onbellekle ayni boyut + os.utime ile GERI ALINMIS ESKI mtime -> BAYAT (anahtarda
    degisiklik zamani var: icerik yazmak onu ilerletir, utime geri alamaz; Windows'ta NTFS ChangeTime) · POSIX: okunamaz dosya (`chmod 000`: ctime kayar) cagiransiz sorguda da
    BAYAT sayilir (dosya yeniden okunmayi dener, okunamayinca bugunden duser)."""
    b = []
    if not _platform_sinir("BAYAT-CTIME"):
        kok, yol, eski = sp["bayat_ctime"]
        _yaz(yol, AYNI_BOYUT)
        _zamanla(yol, eski)                            # mtime GERI ALINDI: yalniz ctime ilerledi
        _bayat_hukum(b, "BAYAT-CTIME", "ayni boyut + geri alinmis ESKI mtime, onbellek sicak", _bayat_sorgu(motor, kok), True)
    if not _platform_sinir("BAYAT-OKUNMAZ"):
        kok, _yol, _eski = sp["bayat_okunmaz"]
        yan = os.path.join(kok, "src", "yan.ts")
        os.chmod(yan, 0)
        try:
            kod, o, _e = kos(motor, kok, "adres", "--mahalle", "src")
        finally:
            os.chmod(yan, stat.S_IRUSR | stat.S_IWUSR)
        _bayat_hukum(b, "BAYAT-OKUNMAZ", "sicak onbellek, src/yan.ts okunamaz (chmod 000), cagiransiz sorgu", (kod, o), True)
    return b


def kol_bayat_zaman(motor, taban, sp):
    """A-BAYAT (KALEM 4) devami: mtime tuzaklari + `--kur` baglama + bozuk/yazilamayan onbellek."""
    b = []
    kok, yol, eski = sp["bayat_boyut"]
    _yaz(yol, YENI_SATIR)
    _zamanla(yol, eski)
    _bayat_hukum(b, "BAYAT-BOYUT", "mtime ayni, boyut farkli", _bayat_sorgu(motor, kok), True)
    kok = proje(taban, "bayat_zaman", {"src/fx.ts": TS_FX})
    yol = os.path.join(kok, "src", "fx.ts")
    kur(motor, kok)
    os.utime(yol, None)                                # mtime = SIMDI: onbellek yazildigi ana yakin (racy)
    mtime = os.stat(yol).st_mtime_ns
    _bayat_hukum(b, "BAYAT-YOK", "taze dosya, degismeyen agac", _bayat_sorgu(motor, kok), False)
    _yaz(yol, AYNI_BOYUT)
    _zamanla(yol, mtime)
    _bayat_hukum(b, "BAYAT-ZAMAN", "ayni boyut + korunmus mtime, onbellek taze", _bayat_sorgu(motor, kok), True)
    kok, yol, eski = sp["bayat_kur"]
    _yaz(yol, AYNI_BOYUT)
    _zamanla(yol, eski)                                # onbellek (eski defter) bunu GOREMEZ; `--kur` defteri yeniler
    kur(motor, kok)
    _bayat_hukum(b, "BAYAT-KUR", "icerik degisti, `--kur` yenilendi", _bayat_sorgu(motor, kok), False)
    return b + kol_bayat_onbellek_bozuk(motor, sp)


def kol_bayat_onbellek_bozuk(motor, sp):
    """A-BAYAT (KALEM 4) devami: onbellek dosyasi bozuk (JSON degil / yanlis tur / 1e999 gibi tasan sayi) ya da yazilamaz (yerinde dizin
    var) -> TAM yol, degisiklik yine BAYAT, komut dusmez."""
    b = []
    kok, yol, _eski = sp["bayat_bozuk"]
    _yaz(yol, YENI_SATIR)
    with io.open(onb_dosyasi(kok), encoding="utf-8") as f:
        gecerli = json.load(f)
    gecerli["dosyalar"]["src/fx.ts"][0] = "@@TASAN@@"
    tasan = json.dumps(gecerli).replace('"@@TASAN@@"', "1e999")      # `int(inf)` -> OverflowError (JSON'da gecerli degil ama Python okur)
    for icerik in (tasan, "{bozuk", "[]", '{"surum": 2, "ozet": null, "dosyalar": 5}'):
        _yaz(onb_dosyasi(kok), icerik)
        _bayat_hukum(b, "BAYAT-ONB-BOZUK", "onbellek icerigi %r" % icerik[-60:], _bayat_sorgu(motor, kok), True)
    onb = onb_dosyasi(kok)
    os.remove(onb)
    os.mkdir(onb)                                      # yazma hedefi DIZIN: os.replace basarisiz olur
    _bayat_hukum(b, "BAYAT-ONB-YAZ", "onbellek yolu dizin (yazilamaz)", _bayat_sorgu(motor, kok), True)
    return b + kol_bayat_proje_ici(motor, sp)


def kol_bayat_proje_ici(motor, sp):
    """A-BAYAT (KALEM 4) devami: gecici dizin PROJE AGACININ ICINDEYSE (tempfile hicbir adaya yazamazsa cwd'ye duser) onbellek
    KAPALI: projeye dosya EKLENMEZ, sorgu yine dogru (BAYAT-ONB-PROJE)."""
    kok, yol, _eski = sp["bayat_proje"]
    ic = os.path.join(kok, "tmpic")
    os.makedirs(ic)
    _yaz(yol, YENI_SATIR)
    kod, o, _e = kos(motor, kok, "adres", "Kasa", tmp=ic)
    if os.listdir(ic):
        return [("BAYAT-ONB-PROJE", "gecici dizin proje icindeyken projeye dosya yazildi: %r" % os.listdir(ic))]
    if kod != 1 or not o.startswith(BAYAT_BIR):
        return [("BAYAT-ONB-PROJE", "gecici dizin proje icindeyken sorgu exit=%s ilk satir=%r" % (kod, o.split("\n")[0]))]
    return []


SERPISTIR ={"a.ts": TS_FX, "b.py": PY_FX, "c.dart": DART_FX, "d.cs": CS_FX}       # alfabetik sira != dil sirasi (py cs dart ts)


def kol_determinizm(motor, taban):
    """A-DETERMINIZM: iki `--kur` bit-bit ayni; satirlar kanonik (yol, bas, -bit, tur, ad) sirasinda."""
    b = []
    kok = proje(taban, "det1", SERPISTIR)
    kur(motor, kok)
    p = os.path.join(kok, "arsiv", "hafiza", "ADRES.tsv")
    ilk = open(p, "rb").read()
    kur(motor, kok)
    if open(p, "rb").read() != ilk:
        b.append(("DETERMINIZM-AYNI", "ayni agacta iki `--kur` FARKLI bayt uretti"))
    sat = defter(kok)[1]
    anahtar = lambda r: (r[0], int(r[3]), -int(r[4]), r[1], r[2])
    if sat != sorted(sat, key=anahtar):
        b.append(("DETERMINIZM-SIRA", "satirlar kanonik (yol, bas, -bit, tur, ad) sirasinda DEGIL: ilk sapma %r" % (
            [(x, y) for x, y in zip(sat, sorted(sat, key=anahtar)) if x != y][:1],)))
    return b


# ------------------------------------------------------------------ A-MASKE (P2.1 KALEM 2): cagiran listesinde yorum/metin gurultusu yok
# Her fikstur dosyasinda ayni ad: BIR gercek cagri · BIR yorumda · BIR dizede · BIR interpolasyon deliginde gercek cagri.
# Beklenen (ELLE, motor sabitinden DEGIL): cagiran satirlari = gercek + delik; "NOT: 2 yorum/metin icindeki gecis sayilmadi".
CS_MASKE = '''public class M
{
    public int HedefCs(int x) => x;

    public int Kos()
    {
        var a = HedefCs(1);
        // HedefCs yorumda
        var b = "HedefCs metinde";
        var c = $"{HedefCs(2)}";
        var d = $$"""{"k":"{{HedefCs(3)}}"}""";
        var e = $$"""HedefCs ham metinde""";
        var bf = $"{a,10:HedefCs}";
        var bg = $"{HedefCs(4):N}";
        var bh = $"{global::System.Math.Max(HedefCs(5), 1)}";
        return a + b.Length + c.Length + d.Length + e.Length + bf.Length + bg.Length + bh.Length;
    }
}
'''
DART_MASKE = '''class M {
  int hedefDart(int x) => x;
  int sayacDart = 0;

  int kos() {
    var a = hedefDart(1);
    // hedefDart yorumda; sayacDart de yorumda
    var b = 'hedefDart metinde';
    var c = '${hedefDart(2)}';
    var d = '$sayacDart';
    var e = 'sayacDart metinde';
    return a + b.length + c.length + d.length + e.length;
  }
}
'''
PY_MASKE = '''def hedef_py(x):
    return x


def kos():
    a = hedef_py(1)
    # hedef_py yorumda
    b = "hedef_py metinde"
    c = f"{hedef_py(2)}"
    d = f"{a:>{hedef_py(3)}}"
    e = f"{a:hedef_py}"
    return a, b, c, d, e
'''
TS_MASKE = '''export function hedefTs(x: number): number {
  return x;
}

export function kos(): number {
  const a = hedefTs(1);
  // hedefTs yorumda
  const b = 'hedefTs metinde';
  const c = `${hedefTs(2)}`;
  return a + b.length + c.length;
}
'''
TSX_MASKE = '''export function hedefTsx(x: number): number {
  return x;
}

export const Kos = () => {
  const a = hedefTsx(1);
  // hedefTsx yorumda
  return <div title="hedefTsx">{hedefTsx(a)}</div>;
};
'''
# JSX bilesen etiketi: acilis + kapanis adi GERCEK cagri; ozellik dizesi ve {/* */} yorumu degil; kucuk harfli `<sekme />` HTML etiketi
KART_MASKE = '''export function HedefKart(p: { a: number }) {
  return <span>{p.a}</span>;
}

export const Sayfa = () => (
  <section title="HedefKart">
    <HedefKart a={1} />
    {/* HedefKart yorumda */}
    <HedefKart a={2}>x</HedefKart>
  </section>
);

export function sekme() {
  return 1;
}

export const Y = () => <sekme />;
'''
# Python dize onek harfleri (f"" rb"") dizenin parcasidir: `f` / `rb` adli islevin cagiranlari yalniz gercek cagrilar
ONEK_MASKE = '''def f(x):
    return x


def rb(x):
    return x


a = f(1)
b = f"metin {a}"
c = rb"ham"
d = rb(2)
'''
# 30 ic ice f-dize; 2. satir: ayni derinlikte bicim belirteci DELIKLERI icinde (`F` oneki: `f` adli islev sayaclarina karismaz). Eski motor icte yeniden tarayip 2^30 is yapardi
IC_MASKE = ("a = " + 'F"{' * 30 + "hedef_ic(1)" + '}"' * 30 + "\n" +
            "b = " + 'F"{a:>{(' * 30 + "hedef_ic(2)" + ')}}"' * 30 + "\n")
HAM_MASKE = "export function hedefHam(): number {\n  return 1;\n}\n"
# 150 ic ice JSX elemani = JSX derinlik siniri (100) asilir: maske KURULAMAZ, dosya ham taranir ve bu BILDIRILIR
DERIN_MASKE = "export const D = " + "<a>" * 150 + "x" + "</a>" * 150 + ";\n// hedefHam yorumda\nhedefHam();\n"
MASKE_DOSYALAR = {"src/M.cs": CS_MASKE, "src/m.dart": DART_MASKE, "src/m.py": PY_MASKE, "src/m.ts": TS_MASKE, "src/m.tsx": TSX_MASKE,
                  "src/ham.ts": HAM_MASKE, "src/derin.tsx": DERIN_MASKE, "src/kart.tsx": KART_MASKE, "src/onek.py": ONEK_MASKE,
                  "src/ic_tanim.py": "def hedef_ic(x):\n    return x\n", "src/ic.py": IC_MASKE}
# (ad, gercek cagri satirlari, interpolasyon deligindeki gercek cagri satirlari, beklenen "sayilmadi" sayisi): ELLE
MASKE_BEKLENEN = (
    ("HedefCs", {7}, {10, 11, 14, 15}, 4),      # 4 = yorum + dize + ham dize metni + bicim belirteci (`{a,10:HedefCs}` kod DEGIL)
    ("hedefDart", {6}, {9}, 2),
    ("sayacDart", set(), {10}, 2),
    ("hedef_py", {6}, {9, 10}, 3),      # 3 = yorum + dize + bicim belirteci (`{a:hedef_py}` kod DEGIL)
    ("hedefTs", {6}, {9}, 2),
    ("hedefTsx", {6}, {8}, 2),
    ("HedefKart", {7, 9}, set(), 2),
    ("sekme", set(), set(), 1),
    ("f", {9}, set(), 4),      # 4 = m.py:9,10,11 + onek.py:10 (`f"` onek harfi)
    ("rb", {12}, set(), 1),
)
MASKE_KUSUR_ANKOR = "    kayit = _AD_KAYIT[0] = [] if delik_kod else None\n"


def _cagiran_satirlari(cikti):
    """`adres <ad>` ciktisindaki cagiran satir numaralari (kume)."""
    return set(int(x) for l in _cagiranlar(cikti) for x in re.findall(r"\d+", l.rsplit(":", 1)[1]))


def kol_maske(motor, taban):
    """A-MASKE: yorum/dize icindeki gecis cagiran SAYILMAZ (MASKE) · interpolasyon deliginin gercek cagrisi SAYILIR (MASKE-DELIK) ·
    gercek cagri kaybolmaz (MASKE-GERCEK) · maskelenen gecis sayisi "NOT" satiriyla BEYAN edilir (MASKE-NOT) · maske kurulamayan
    dosya ham taranir ve BILDIRILIR (MASKE-HAM)."""
    b = []
    kok = proje(taban, "maske", MASKE_DOSYALAR)
    kur(motor, kok)
    for ad, gercek, delik, say in MASKE_BEKLENEN:
        _kod, o, _e = kos(motor, kok, "adres", ad)
        sat = _cagiran_satirlari(o)
        if sat - gercek - delik:
            b.append(("MASKE", "%s: yorum/dize icindeki gecis cagiran SAYILDI: fazla satirlar %s (liste %s)" % (ad, sorted(sat - gercek - delik), sorted(sat))))
        if gercek - sat:
            b.append(("MASKE-GERCEK", "%s: gercek cagri listede YOK: %s (liste %s)" % (ad, sorted(gercek - sat), sorted(sat))))
        if delik - sat:
            b.append(("MASKE-DELIK", "%s: interpolasyon deligindeki gercek cagri listede YOK: %s (liste %s)" % (ad, sorted(delik - sat), sorted(sat))))
        satirlar, beklenen = o.split("\n"), "NOT: %d yorum/metin icindeki gecis sayilmadi" % say
        son = satirlar.index("NOT: cagiranlar sozcuk eslesmesidir") if "NOT: cagiranlar sozcuk eslesmesidir" in satirlar else -1
        if beklenen not in satirlar or not 0 <= satirlar.index(beklenen) < son:
            b.append(("MASKE-NOT", "%s: %r satiri (\"NOT: cagiranlar...\" satirindan ONCE) yok: %r" % (ad, beklenen, [l for l in satirlar if l.startswith("NOT:")])))
    try:
        _kod, o, _e = kos(motor, kok, "adres", "hedef_ic", zaman_asimi=SURE_ZAMAN_ASIMI)
    except subprocess.TimeoutExpired:
        b.append(("MASKE-DERIN", "30 ic ice f-dize: `adres hedef_ic` %d s icinde BITMEDI (maske suresi dogrusal/karesel degil)" % SURE_ZAMAN_ASIMI))
    else:
        if "maske kurulamadi" in o or "yorum/metin icindeki" in o or _cagiran_satirlari(o) != {1, 2}:
            b.append(("MASKE-DERIN", "30 ic ice f-dize: deligin gercek cagrilari (src/ic.py:1,2) tek cagiran olmali, maske kurulmali, gecis sayilmamali: %r" % (o,)))
    kaynak = io.open(motor, encoding="utf-8", newline="").read()
    if kaynak.count(MASKE_KUSUR_ANKOR) != 1:
        raise Kurulamadi("maske kusuru capasi %d yerde gecti (1 olmali)" % kaynak.count(MASKE_KUSUR_ANKOR))
    bozuk, hata = _motor_yaz(kaynak.replace(MASKE_KUSUR_ANKOR, '    if delik_kod:      # MUTANT: maske ARAC KUSURU\n        raise ValueError("bilerek bozuk maske")\n' + MASKE_KUSUR_ANKOR, 1),
                             os.path.join(taban, "maske_bozuk"), "maske_bozuk")
    if bozuk is None:
        raise Kurulamadi(hata)
    kod, o, e = kos(bozuk, kok, "adres", "hedefTs")
    if kod != 3:
        b.append(("MASKE-KUSUR", "maske ARAC KUSURU (beklenmedik istisna) firlatirken `adres hedefTs` exit=%s (3 = ARAC KUSURU beklenir); cikti=%r" % (
            kod, (o + e).strip()[-120:])))
    _kod, o, _e = kos(motor, kok, "adres", "hedefHam")
    if "NOT: 1 dosyada maske kurulamadi" not in o:
        b.append(("MASKE-HAM", "JSX derinlik siniri asildi (maske kurulamaz) ama maske-kurulamadi NOTU yok: %r" % (o,)))
    if 3 not in _cagiran_satirlari(o):
        b.append(("MASKE-GERCEK", "hedefHam: maskesi kurulamayan dosyada gercek cagri (src/derin.tsx:3) listede YOK: %r" % (o,)))
    return b


# ------------------------------------------------------------------ A-ATLA (P2.1 KALEM 3): gomulu/uretilmis dosyalar taranmaz, atlanma BEYAN edilir
# Her fikstur dosyasinda ayni ad `atlaHedef` (tanim + cagri). Beklentiler ELLE yazildi (motor sabitinden DEGIL).
ATLA_IS = "function atlaHedef() {\n  return 1;\n}\natlaHedef();\n"
ATLA_OK = "export function atlaHedef(): number {\n  return 1;\n}\nexport const t = atlaHedef();\n"
ATLA_TEMEL = {".yarn/x.cjs": ATLA_IS, "node_modules/a/b.js": ATLA_IS, "src/ok.ts": ATLA_OK}
ATLA_TEMEL_SATIR = "ATLANAN: 2 dosya (.yarn 1, node_modules 1)"
ATLA_AYRINTI = {".yarn/x.cjs": ATLA_IS, ".yarn/p.kt": "fun atlaHedef() {}\n", "node_modules/a/b.js": ATLA_IS, "node_modules/a/package.json": "{}\n",
                "vendor/v.ts": ATLA_OK, "dist/d.js": ATLA_IS, "lib/build/b.ts": ATLA_OK, "public/app.min.js": ATLA_IS, "tools/k.cjs": ATLA_IS,
                "src/ok.ts": ATLA_OK, "src/build_tools/bt.ts": ATLA_OK, "src/Dist/up.ts": ATLA_OK, "src/m.mjs": ATLA_IS, "src/app.js": ATLA_IS,
                "src/dist.ts": ATLA_OK, "src/x.kt": "fun atlaHedef() {}\n"}
ATLA_AYRINTI_KALAN = ["src/Dist/up.ts", "src/app.js", "src/build_tools/bt.ts", "src/dist.ts", "src/m.mjs", "src/ok.ts"]
ATLA_AYRINTI_SATIR = "ATLANAN: 8 dosya (.yarn 2, *.cjs 1, *.min.js 1, build 1, dist 1, node_modules 1, vendor 1)"
ATLA_FS = {".yarn/x.cjs": ATLA_IS, "vendor/v.ts": ATLA_OK, "node_modules/a/b.js": ATLA_IS, "src/ok.ts": ATLA_OK}


def _tanim_yollari(cikti):
    """`adres <ad>` ciktisinin TANIM satirlarinin yollari (sirali)."""
    bolum = cikti.split("TANIM (", 1)
    yollar = []
    for l in (bolum[1].split("\n")[1:] if len(bolum) > 1 else []):
        if not l.startswith("  ") or l.startswith("  +"):
            break
        yollar.append(l.strip().split(" > ")[0])
    return sorted(yollar)


def _atla_sorgu(motor, kok, etiket, bekle_tanim, bekle_cagiran):
    """`adres atlaHedef`: TANIM yollari ve CAGIRAN yollari ELLE beklentiyle esit olmali; bayat/yanlis exit yok. -> [(etiket, mesaj)]"""
    kod, o, _e = kos(motor, kok, "adres", "atlaHedef")
    b = []
    if _tanim_yollari(o) != bekle_tanim:
        b.append(("ATLA", "%s: TANIM yollari %r != beklenen %r" % (etiket, _tanim_yollari(o), bekle_tanim)))
    yollar = sorted(set(l.split(" > ")[0] for l in _cagiranlar(o)))
    if yollar != bekle_cagiran:
        b.append(("ATLA", "%s: CAGIRAN yollari %r != beklenen %r" % (etiket, yollar, bekle_cagiran)))
    if kod != 0 or "BAYAT" in o:
        b.append(("ATLA-BAYAT", "%s: kurulmus defterde sorgu exit=%s ya da BAYAT basildi (kur ve sorgu AYNI suzgeci kullanmali): %r" % (
            etiket, kod, o.split("\n")[0])))
    return b


def _atla_kur(motor, kok, etiket):
    kod, o, e = kos(motor, kok, "adres", "--kur")
    if kod != 0:
        raise Kurulamadi("%s: adres --kur basarisiz (exit=%s): %s" % (etiket, kod, (o + e).strip()[-200:]))
    return [l.strip() for l in o.split("\n")]


def kol_atla(motor, taban):
    """A-ATLA: atlanan dosya tanim/cagiran listesinde YOK (ATLA) · `--kur` konsolu + baslik ATLANAN'i BEYAN eder (ATLA-BEYAN) ·
    atlanan dosyanin degismesi BAYAT yapmaz (ATLA-BAYAT) · `src/build_tools/` + `src/Dist/` atlanmaz, atlanan KAPSAM DISI'na girmez · git'siz kip."""
    b = []
    kok = proje(taban, "atla", ATLA_TEMEL)
    satirlar = _atla_kur(motor, kok, "temel")
    if ATLA_TEMEL_SATIR not in satirlar:
        b.append(("ATLA-BEYAN", "temel: `--kur` ciktisinda %r yok: %r" % (ATLA_TEMEL_SATIR, [l for l in satirlar if "ATLANAN" in l])))
    baslik, sat = defter(kok)
    if not baslik.endswith(" atlanan=.yarn:1,node_modules:1"):
        b.append(("ATLA-BEYAN", "temel: ADRES.tsv basliginda `atlanan=.yarn:1,node_modules:1` yok: ...%s" % baslik[-80:]))
    sizan = sorted(set(r[0] for r in sat if r[0].startswith((".yarn/", "node_modules/"))))
    if sizan:
        b.append(("ATLA", "temel: defterde atlanan dosyalarin satiri VAR: %r" % sizan))
    b += _atla_sorgu(motor, kok, "temel", ["src/ok.ts"], ["src/ok.ts"])
    _yaz(os.path.join(kok, ".yarn", "x.cjs"), ATLA_IS + "// degisti\n")
    b += _atla_sorgu(motor, kok, "temel (atlanan dosya degisti)", ["src/ok.ts"], ["src/ok.ts"])
    kok = proje(taban, "atla_ayrinti", ATLA_AYRINTI)
    satirlar = _atla_kur(motor, kok, "ayrinti")
    if ATLA_AYRINTI_SATIR not in satirlar:
        b.append(("ATLA-BEYAN", "ayrinti: %r yok: %r" % (ATLA_AYRINTI_SATIR, [l for l in satirlar if "ATLANAN" in l])))
    if "KAPSAM DISI DIL: 1 dosya (.kt 1)" not in satirlar:
        b.append(("ATLA", "ayrinti: atlanan .yarn/p.kt KAPSAM DISI'na girdi (ya da src/x.kt yok): %r" % [l for l in satirlar if "KAPSAM" in l]))
    if not any(l.startswith("dosya  : 6, tanim") for l in satirlar):
        b.append(("ATLA", "ayrinti: taranan dosya sayisi 6 degil: %r" % [l for l in satirlar if l.startswith("dosya")]))
    b += _atla_sorgu(motor, kok, "ayrinti", ATLA_AYRINTI_KALAN, ATLA_AYRINTI_KALAN)
    return b + kol_atla_fs(motor, taban)


def kol_atla_fs(motor, taban):
    """A-ATLA (git'siz dosya sistemi kipi): ayni suzgec; `node_modules` yuruyusce BUDANIR (not ile beyan)."""
    kok = os.path.join(taban, "atla_fs")
    for y, m in ATLA_FS.items():
        _yaz(os.path.join(kok, *y.split("/")), m)
    satirlar = _atla_kur(motor, kok, "fs")
    b = []
    if not any(l.startswith("kaynak : dosya sistemi") for l in satirlar):
        raise Kurulamadi("atla_fs: git'siz kip kurulamadi (kaynak dosya sistemi degil): %r" % satirlar[:4])
    if "ATLANAN: 2 dosya (.yarn 1, vendor 1)" not in satirlar:
        b.append(("ATLA-BEYAN", "fs: `ATLANAN: 2 dosya (.yarn 1, vendor 1)` yok: %r" % [l for l in satirlar if "ATLANAN" in l]))
    return b + _atla_sorgu(motor, kok, "fs", ["src/ok.ts"], ["src/ok.ts"])


# ------------------------------------------------------------------ A-EZME / A-EKSIK (P5 KALEM 0): cikarici kusuru SAGLAM defteri ezmez; EKSIK defter
# sorguda "guncel" sayilmaz. ARIZALI motor = ayni motorun C#/Dart/TS desen tablosu ILK KULLANIMDA patlayan kopyasi (Python `ast` yolu tabloya
# dokunmaz): py dosyalari tanimlanir, C# dosyasi `cikarici` istisnasi verir -> `--kur` exit 3 (Cowork O14 `inj_tablo` enjeksiyonuyla ayni sinif).
EZME_DOSYALAR = {"src/fx.py": PY_FX, "src/Fx.cs": CS_FX}       # 4 py + 4 cs = 8 tanim (BEKLENEN)
EZME_BASLIK = "ADRES DEFTERI KURULAMADI: 1 dosyada cikarici istisnasi"
TABLO_ANKOR = (r'    delegate = (re.compile(r"%sdelegate\s+%s\s+(?P<ad>%s)\s*(?:%s)?\(" % (mod, tip, _N, _G2)), "tip", "")' + "\n")   # C# `delegate` kurali


def _tablo_bozuk_yaz(kaynak, hedef_dizin, ad):
    """Cikarici BEKLENMEDIK istisna firlatan motor kopyasi: C# kural tablosu ilk kullanimda patlar (modul yuklemede DEGIL)."""
    if kaynak.count(TABLO_ANKOR) != 1:
        return None, "tablo bozucu capasi %d yerde gecti (1 olmali)" % kaynak.count(TABLO_ANKOR)
    metin = kaynak.replace(TABLO_ANKOR, '    delegate = (re.compile("(("), "tip", "")      # MUTANT: tablo ogesi ilk kullanimda patlar\n', 1)
    return _motor_yaz(metin, hedef_dizin, ad)


def _defter_yolu(kok):
    return os.path.join(kok, "arsiv", "hafiza", "ADRES.tsv")


def _bozuk_motor(taban, ad, kaynak):
    bozuk, hata = _tablo_bozuk_yaz(kaynak, os.path.join(os.path.dirname(taban), "tablo_" + ad), "tablo_" + ad)
    if bozuk is None:
        raise Kurulamadi(hata)
    return bozuk


def kol_ezme(motor, taban, bozuk):
    """A-EZME: arac kusurunda (exit 3) mevcut SAGLAM defter EZILMEZ (EZME: bayt-bayt ayni · EZME-BASLIK `KURULAMADI` · EZME-KORUNDU
    `ESKI DEFTER KORUNDU` satiri) · saglam defter YOKSA eksik defter `EKSIK KURULDU` der ve `cikarici=` damgasi tasir (EZME-EKSIK) ·
    BOZUK defter korunmaz (EZME-BOZUK) · EKSIK defter SAGLAM sayilmaz, yeni eksik defter onun USTUNE yazilir (EZME-USTUNE) ·
    exit 0 yolu `KURULDU` der ve `cikarici=` alani YOK (EZME-SAGLAM)."""
    b = []
    kok = proje(taban, "ezme", EZME_DOSYALAR)
    kod, o, e = kos(motor, kok, "adres", "--kur")
    if kod != 0 or not o.startswith("ADRES DEFTERI KURULDU: arsiv/hafiza/ADRES.tsv ("):
        b.append(("EZME-SAGLAM", "saglam motor exit=%s ilk satir=%r (exit 0 + `ADRES DEFTERI KURULDU:` beklenir)" % (kod, o.split("\n")[0])))
    once = io.open(_defter_yolu(kok), "rb").read()
    if b"cikarici=" in once.split(b"\n")[0]:
        b.append(("EZME-SAGLAM", "cikarici kusuru YOKKEN baslikta `cikarici=` alani var: %r" % once.split(b"\n")[0][-60:]))
    kod, o, e = kos(bozuk, kok, "adres", "--kur")
    if kod != 3:
        raise Kurulamadi("arizali motor `--kur` exit=%s (3 beklenir): %r" % (kod, (o + e).strip()[-160:]))
    sonra = io.open(_defter_yolu(kok), "rb").read()
    if sonra != once:
        b.append(("EZME", "arac kusurunda SAGLAM defter DEGISTI (%d -> %d bayt)" % (len(once), len(sonra))))
    sat = o.split("\n")
    if sat[0] != EZME_BASLIK:
        b.append(("EZME-BASLIK", "ilk satir %r != %r" % (sat[0], EZME_BASLIK)))
    korundu = "ESKI DEFTER KORUNDU: arsiv/hafiza/ADRES.tsv (%d bayt, tanim 8)" % len(once)
    if korundu not in sat:
        b.append(("EZME-KORUNDU", "%r satiri yok: %r" % (korundu, sat[:4])))
    if not any(l.startswith("  ATLANDI: 1 dosya (cikarici 1); ilk: src/Fx.cs") for l in sat) or \
            not any(l.startswith("  ARAC KUSURU: 1 dosyada cikarici BEKLENMEDIK istisna firlatti") for l in sat):
        b.append(("EZME-KORUNDU", "KORUNDU yolunda ATLANDI / ARAC KUSURU satirlari yok: %r" % sat))
    # saglam defter YOK: eksik defter yazilir, ilk satir basari DEMEZ
    kok2 = proje(taban, "ezme_yok", EZME_DOSYALAR)
    kod, o, e = kos(bozuk, kok2, "adres", "--kur")
    baslik = io.open(_defter_yolu(kok2), encoding="utf-8").read().split("\n")[0] if os.path.isfile(_defter_yolu(kok2)) else ""
    if kod != 3 or not o.startswith("ADRES DEFTERI EKSIK KURULDU: arsiv/hafiza/ADRES.tsv (") or " cikarici=1" not in baslik:
        b.append(("EZME-EKSIK", "defter YOKKEN: exit=%s ilk satir=%r baslik sonu=%r" % (kod, o.split("\n")[0], baslik[-40:])))
    # EKSIK defter SAGLAM DEGIL: ikinci arizali `--kur` onu KORUMAZ, yenisini (yine eksik) yazar
    _yaz(os.path.join(kok2, "src", "yeni.py"), "def yeni():\n    return 1\n")
    _git(kok2, "add", "-A")
    kod, o, e = kos(bozuk, kok2, "adres", "--kur")
    if kod != 3 or not o.startswith("ADRES DEFTERI EKSIK KURULDU:") or "yeni" not in io.open(_defter_yolu(kok2), encoding="utf-8").read():
        b.append(("EZME-USTUNE", "eksik defterin USTUNE: exit=%s ilk satir=%r" % (kod, o.split("\n")[0])))
    # BOZUK defter saglam degil: ezilir
    kok3 = proje(taban, "ezme_bozuk", EZME_DOSYALAR)
    os.makedirs(os.path.dirname(_defter_yolu(kok3)))
    _yaz(_defter_yolu(kok3), "bu bir defter degil\n")
    kod, o, e = kos(bozuk, kok3, "adres", "--kur")
    if kod != 3 or not o.startswith("ADRES DEFTERI EKSIK KURULDU:"):
        b.append(("EZME-BOZUK", "bozuk defter: exit=%s ilk satir=%r" % (kod, o.split("\n")[0])))
    return b


def kol_eksik(motor, taban, bozuk):
    """A-EKSIK: EKSIK defter (cikarici kusurlu) sorguda 'guncel' SAYILMAZ: SAGLAM motorla `adres <ad>` defteri yeniden kurar ve tanimi
    BULUR (EKSIK-YENIDEN) · ikinci sorguda yeniden kurma YOK (EKSIK-TEKRAR) · `sozdizimi` atlamasi EKSIK degildir, yeniden kurmayi
    tetiklemez (EKSIK-SOZDIZIMI) · arizali motorda hala eksik: ESKI defter korunur, durum `EKSIK` basilir, sorgu dusmez (EKSIK-HALA)."""
    b = []
    kok = proje(taban, "eksik", EZME_DOSYALAR)
    kod, o, e = kos(bozuk, kok, "adres", "--kur")
    if kod != 3 or " cikarici=1" not in io.open(_defter_yolu(kok), encoding="utf-8").read().split("\n")[0]:
        raise Kurulamadi("eksik defter kurulamadi: exit=%s %r" % (kod, (o + e).strip()[-160:]))
    kod, o, e = kos(bozuk, kok, "adres", "Kapat")
    if "ADRES DEFTERI EKSIK: 1 dosyada cikarici istisnasi" not in o or kod != 1:
        b.append(("EKSIK-HALA", "arizali motorla sorgu: exit=%s cikti=%r (EKSIK satiri + exit 1 beklenir)" % (kod, o[:160])))
    kod, o, e = kos(motor, kok, "adres", "Kapat")
    sat = o.split("\n")
    baslik = io.open(_defter_yolu(kok), encoding="utf-8").read().split("\n")[0]
    if kod != 0 or "TANIM (1):" not in sat or not any(l.strip().startswith("src/Fx.cs > Kasa > Kapat ") for l in sat):
        b.append(("EKSIK-YENIDEN", "saglam motor: exit=%s; eksik defterde `Kapat` BULUNAMADI ya da exit != 0: %r" % (kod, o[:200])))
    if " cikarici=" in baslik or " tanim=8 " not in baslik:
        b.append(("EKSIK-YENIDEN", "saglam motordan sonra defter hala eksik: %r" % baslik[-90:]))
    kod, o, e = kos(motor, kok, "adres", "Kapat")
    if "YENIDEN KURULDU" in o or kod != 0:
        b.append(("EKSIK-TEKRAR", "defter onarildiktan sonra sorgu yine yeniden kurdu / exit=%s: %r" % (kod, o[:120])))
    kok2 = proje(taban, "eksik_sozdizimi", {"src/ok.py": PY_FX, "src/kotu.py": "def (:\n"})
    kod, o, e = kos(motor, kok2, "adres", "--kur")
    if kod != 0 or " atlandi=1 " not in io.open(_defter_yolu(kok2), encoding="utf-8").read().split("\n")[0]:
        raise Kurulamadi("sozdizimi fiksturu kurulamadi: exit=%s %r" % (kod, (o + e).strip()[-160:]))
    kod, o, e = kos(motor, kok2, "adres", "hesapla")
    if "YENIDEN KURULDU" in o or "EKSIK" in o or kod != 0:
        b.append(("EKSIK-SOZDIZIMI", "yalniz `sozdizimi` atlamali defter EKSIK sayildi: exit=%s %r" % (kod, o[:160])))
    if not _platform_sinir("EKSIK-BELLEKTE"):          # yazilamayan defter: sorgu YINE cevaplanir (bellekteki yeni defterle), dosya DEGISMEZ
        kok3 = proje(taban, "eksik_bellekte", EZME_DOSYALAR)
        kos(bozuk, kok3, "adres", "--kur")
        p3 = _defter_yolu(kok3)
        once = io.open(p3, "rb").read()
        os.chmod(p3, stat.S_IREAD)
        try:
            kod, o, e = kos(motor, kok3, "adres", "Kapat")
        finally:
            os.chmod(p3, stat.S_IREAD | stat.S_IWRITE)
        if kod != 0 or "ADRES DEFTERI YENIDEN KURULDU (BELLEKTE)" not in o or "src/Fx.cs > Kasa > Kapat " not in o \
                or io.open(p3, "rb").read() != once:
            b.append(("EKSIK-BELLEKTE", "yazilamayan eksik defter: exit=%s cikti=%r (BELLEKTE satiri + tanim BULUNMALI, defter DEGISMEMELI)" % (kod, o[:200])))
    return b


def kos_ezme(motor, taban, ad, kaynak):
    return kol_ezme(motor, taban, _bozuk_motor(taban, "ezme_" + ad, kaynak))


def kos_eksik(motor, taban, ad, kaynak):
    return kol_eksik(motor, taban, _bozuk_motor(taban, "eksik_" + ad, kaynak))


# ------------------------------------------------------------------ P5-DAMGA (P5 KALEM 1): `not` aninda satir ici parmak izli atif
# Beklentiler FIKSTURDEN ELLE: iz = fikstur satirlarinin SHA-256'sinin ilk 8 hex'i (motordan DEGIL hashlib'den). Tekil ad ve `yol:N` ->
# damga; ayni ad iki dosyada / ayni dosyada asiri yuklu -> damga YOK + COKLU; ikinci `not` damgali metinle -> cift damga YOK; `derle`
# damgayi oldugu gibi tasir; kod citi / cift backtick ici damgalanmaz; bitisik sonek damgalanmaz; BAYAT defterde `yol:N` CANLI dosyaya
# gore cozulur; defter yok/eksik/bozuk, arizali cikarici, istisna -> OLCULEMEDI (`not` exit 0, fragman yazilir); sonuc DETERMINIST.
DAMGA_A = '''def tekil_islev(x):
    return x + 1


def ortak_islev(x):
    return x


class Kasa:
    def kapat_kasa(self):
        return 0
'''
DAMGA_B = '''def ortak_islev(y):
    return y * 2
'''
DAMGA_CS = '''public class Hesap
{
    public int Hesapla(int x) => x;
    public int Hesapla(string s) => 0;
}
'''
DAMGA_DOSYALAR = {"src/a.py": DAMGA_A, "src/b.py": DAMGA_B, "src/Fx.cs": CS_FX, "src/Hesap.cs": DAMGA_CS}
DAMGA_IZ = hashlib.sha256("def tekil_islev(x):\n    return x + 1".encode("utf-8")).hexdigest()[:8]       # a.py L1-2
DAMGA_IC_IZ = hashlib.sha256("    def kapat_kasa(self):\n        return 0".encode("utf-8")).hexdigest()[:8]     # a.py L10-11 (sinif DEGIL uye)
DAMGA_METIN = "\n".join((
    "1. `tekil_islev` degisti.",
    "2. `ortak_islev` iki yerde; `Hesapla` asiri yuklu.",
    "3. `a.py:2` bu satira bakiyor; `a.py:11` metodun icinde; `a.py:1-2` aralik; `a.py:2-1` ters aralik.",
    "4. `yok_boyle_ad` yok.",
    "5. `x` kisa; `src/b.py` yol degil.",
    "6. ``kapat_kasa`` cift backtick.",
    "7. `kapat_kasa`un bitisik sonek.",
    "```",
    "`tekil_islev` cit icinde",
    "```",
))
DAMGA_BEKLENEN = (DAMGA_METIN.replace("`tekil_islev` degisti", "`tekil_islev`#%s degisti" % DAMGA_IZ)
                  .replace("`a.py:2` bu", "`a.py:2`#%s bu" % DAMGA_IZ).replace("`a.py:11` met", "`a.py:11`#%s met" % DAMGA_IC_IZ)
                  .replace("`a.py:1-2` ara", "`a.py:1-2`#%s ara" % DAMGA_IZ))
DAMGA_NOT_ARGS = ("not", "--konu", "genel-durum", "--tur", "durum", "--metin")
DAMGA_ISTISNA_ANKOR = "def _damga_uygula_ic(kok, y, govde):\n"
DAMGA_YASAK_CAGRI = ("oldur", "yaz", "kilit_al", "zincir_halka", "_arsive_tasi", "exit")


def _gunluk_adlari(kok):
    d = os.path.join(kok, "gunluk")
    return set(x for x in os.listdir(d) if x.endswith(".md"))


def _not_kos(motor, kok, metin):
    """`not` -> (exit, stdout, stderr, yeni fragmanin govdesi ya da None, fragman adi). Fragman sirasi dosya adindan DEGIL, once/sonra farkindan."""
    once = _gunluk_adlari(kok)
    kod, o, e = kos(motor, kok, *(DAMGA_NOT_ARGS + (metin,)))
    yeni = sorted(_gunluk_adlari(kok) - once)
    if len(yeni) != 1:
        return kod, o, e, None, None
    ham = io.open(os.path.join(kok, "gunluk", yeni[0]), encoding="utf-8", newline="").read()
    return kod, o, e, ham.split("\n---\n\n", 1)[1].rstrip("\n"), yeni[0]


def _hafiza_proje(motor, taban, ad, dosyalar):
    """`dosyalar` + `kur` + commit -> kok."""
    kok = proje(taban, ad, dosyalar)
    kod, o, e = kos(motor, kok, "kur", "--ad", "ADR")
    if kod != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (kod, (o + e).strip()[-160:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "hafiza")
    return kok


def _atif_satirlari(o):
    """`not` ciktisinin FRAGMAN satirindan SONRAKI satirlari (damga/atif/dogusta bayat bildirimleri)."""
    s = o.split("\n")
    i = next((k for k, l in enumerate(s) if l.startswith("FRAGMAN: ")), -1)
    return [l for l in s[i + 1:] if l.strip()]


def _blok_cagrilari(kaynak, bas, son):
    """Motor kaynaginda `bas`..`son` isaretleri arasindaki (P5 blogu) HER cagri adi (AST): `oldur`/`yaz` gibi hukum-yan etkili cagrilar."""
    import ast
    i, j = kaynak.index(bas), kaynak.index(son)
    govde = "\n".join(kaynak[i:j].split("\n"))
    adlar = set()
    for n in ast.walk(ast.parse(govde)):
        if isinstance(n, ast.Call):
            adlar.add(n.func.id if isinstance(n.func, ast.Name) else getattr(n.func, "attr", ""))
    return adlar


def kol_damga(motor, taban, bozuk, istisnali):
    """P5-DAMGA: tekil ad + `yol:N` + `yol:N-M` damgalanir (DAMGA-VAR) · ic ice tanimda en dar tanim (DAMGA-IC) · COKLU: iki dosya +
    asiri yuklu (DAMGA-COKLU) · bulunamayan / ters aralik COZULEMEDI (DAMGA-COZULEMEDI / DAMGA-ARALIK) · ikinci `not` damgali metinle
    cift damga uretmez (DAMGA-TEKRAR) · kod citi (DAMGA-CIT) · cift backtick (DAMGA-CIFT) · bitisik sonek (DAMGA-SONEK) ici damgalanmaz ·
    `derle` damgayi oldugu gibi tasir (DAMGA-DERLE) · BAYAT defterde `yol:N` CANLI dosyaya gore (DAMGA-BAYAT) · defter yok (DAMGA-YOK) /
    eksik (DAMGA-EKSIK) / bozuk (DAMGA-BOZUK) -> OLCULEMEDI · kok disina kacan defter yolu okunmaz (DAMGA-YOL) · sonuc DETERMINIST
    (DAMGA-DETERMINIZM) · blok `oldur`/`yaz` cagirmaz (DAMGA-OLDUR) · cikarici kusuru / istisna `not`u DUSURMEZ (DAMGA-CIKARICI /
    DAMGA-ISTISNA)."""
    b = []
    kok = _hafiza_proje(motor, taban, "damga", DAMGA_DOSYALAR)
    kod, o, e, govde, ad0 = _not_kos(motor, kok, DAMGA_METIN)
    if kod != 0 or govde != DAMGA_METIN or "ATIF OLCULEMEDI: adres defteri YOK" not in o:
        b.append(("DAMGA-YOK", "defter YOKKEN: exit=%s govde ayni=%s cikti=%r (exit 0 + metin AYNI + OLCULEMEDI beklenir)" % (
            kod, govde == DAMGA_METIN, (o + e)[-160:])))
    os.remove(os.path.join(kok, "gunluk", ad0))
    kur(motor, kok)
    kod, o, e, govde, ad1 = _not_kos(motor, kok, DAMGA_METIN)
    sat = o.split("\n")
    govde = govde or ""
    beklenen_satir = "ATIF DAMGALANDI: 4 (a.py:1-2#%s, a.py:11#%s, a.py:2#%s, tekil_islev#%s)" % (DAMGA_IZ, DAMGA_IC_IZ, DAMGA_IZ, DAMGA_IZ)
    if kod != 0 or "`tekil_islev`#%s degisti" % DAMGA_IZ not in govde or "`a.py:2`#%s bu" % DAMGA_IZ not in govde:
        b.append(("DAMGA-VAR", "tekil ad ya da `yol:N` damgalanmadi (beklenen iz %s): exit=%s govde=%r" % (DAMGA_IZ, kod, govde[:200])))
    if beklenen_satir not in sat:
        b.append(("DAMGA-VAR", "%r satiri yok: %r" % (beklenen_satir, o[-300:])))
    if "`a.py:11`#%s met" % DAMGA_IC_IZ not in govde:
        b.append(("DAMGA-IC", "ic ice tanimda `yol:N` EN DAR tanima (uye) damgalanmali, sinifa degil (beklenen iz %s): %r" % (DAMGA_IC_IZ, govde[:200])))
    if "ATIF COKLU: ortak_islev (2 tanim) - damgalanmadi" not in sat or "ATIF COKLU: Hesapla (2 tanim) - damgalanmadi" not in sat \
            or "`ortak_islev` iki yerde; `Hesapla` asiri" not in govde:
        b.append(("DAMGA-COKLU", "ayni ad iki dosyada / asiri yuklu: damga YOK + COKLU satirlari beklenir: govde=%r cikti=%r" % (govde[:160], o[-240:])))
    if "ATIF COZULEMEDI: yok_boyle_ad" not in sat:
        b.append(("DAMGA-COZULEMEDI", "bulunamayan ad icin COZULEMEDI satiri yok: %r" % o[-200:]))
    if "ATIF COZULEMEDI: a.py:2-1" not in sat or "`a.py:2-1` ters" not in govde:
        b.append(("DAMGA-ARALIK", "ters aralik (`a.py:2-1`) COZULEMEDI olmali, damgalanmamali: govde=%r cikti=%r" % (govde[:200], o[-240:])))
    if "`tekil_islev` cit icinde" not in govde.split("\n"):
        b.append(("DAMGA-CIT", "kod citi icindeki belirtec DAMGALANDI: %r" % govde[-80:]))
    if "``kapat_kasa`` cift backtick" not in govde:
        b.append(("DAMGA-CIFT", "cift backtick araligi bozuldu / damgalandi: %r" % govde[-160:]))
    if "`kapat_kasa`un bitisik" not in govde or "ATIF OLCULEMEDI: kapat_kasa (bitisik sonek - damgalanmadi)" not in sat:
        b.append(("DAMGA-SONEK", "bitisik soneki olan belirtec DAMGALANDI ya da OLCULEMEDI satiri yok: govde=%r cikti=%r" % (govde[-120:], o[-240:])))
    if govde != DAMGA_BEKLENEN:
        b.append(("DAMGA-VAR", "fragman govdesi beklenenle ayni degil:\n    %r\n    %r" % (govde, DAMGA_BEKLENEN)))
    kod, o2, e, ikinci, _ad2 = _not_kos(motor, kok, govde)             # ikinci `not`: DAMGALI metinle
    if ikinci != DAMGA_BEKLENEN or kod != 0 or "ATIF DAMGALANDI" in o2:
        b.append(("DAMGA-TEKRAR", "damgali metin yeniden damgalandi / exit=%s: %r" % (kod, (ikinci or "")[:200])))
    sonuclar = [_atif_satirlari(o)] + [_atif_satirlari(_not_kos(motor, kok, DAMGA_METIN)[1]) for _ in range(3)]
    if any(x != sonuclar[0] for x in sonuclar):
        b.append(("DAMGA-DETERMINIZM", "ayni metin + ayni agac: `not` bildirimleri calismalar arasi FARKLI: %r" % (sonuclar,)))
    kod, o3, e = kos(motor, kok, "derle")
    canli = io.open(os.path.join(kok, "PROJE_HAFIZA.md"), encoding="utf-8", newline="").read()
    if "`tekil_islev`#%s degisti" % DAMGA_IZ not in canli or "`a.py:2`#%s bu" % DAMGA_IZ not in canli:
        b.append(("DAMGA-DERLE", "`derle` damgayi canliya oldugu gibi tasimadi (exit=%s): damgali satir canlida yok" % kod))
    kaynak = io.open(motor, encoding="utf-8", newline="").read()
    cagri = _blok_cagrilari(kaynak, "# ==== PARMAK IZLI ATIF (P5) BASLANGIC ====", "# ==== PARMAK IZLI ATIF (P5) SON ====") & set(DAMGA_YASAK_CAGRI)
    if cagri:
        b.append(("DAMGA-OLDUR", "P5 blogu hukum-yan etkili cagri iceriyor (KISIT: yalniz uyari uretir): %s" % sorted(cagri)))
    return b + kol_damga_defter(motor, taban) + kol_damga_arizali(motor, taban, bozuk, istisnali)


def kol_damga_defter(motor, taban):
    """Defter durumlari: BAYAT defterde `yol:N` canli dosyaya gore (DAMGA-BAYAT) · EKSIK/BOZUK defter -> OLCULEMEDI (DAMGA-EKSIK/-BOZUK) ·
    defterdeki kok disina kacan yol okunmaz (DAMGA-YOL)."""
    b = []
    kok = _hafiza_proje(motor, taban, "damga_bayat", {"src/a.py": DAMGA_A})
    kur(motor, kok)
    _yaz(os.path.join(kok, "src", "a.py"), "# bir\n# iki\n# uc\n" + DAMGA_A)            # tekil_islev artik L4-5; defter ESKI
    kod, o, e, govde, _ad = _not_kos(motor, kok, "1. `a.py:5` yeni yeri; `a.py:2` artik tanim DISI.")
    if kod != 0 or govde != "1. `a.py:5`#%s yeni yeri; `a.py:2` artik tanim DISI." % DAMGA_IZ or "ATIF COZULEMEDI: a.py:2" not in o:
        b.append(("DAMGA-BAYAT", "bayat defter: `yol:N` CANLI dosyaya gore cozulmeli (a.py:5 -> tekil_islev, a.py:2 -> tanim disi): exit=%s govde=%r cikti=%r" % (
            kod, govde, o[-200:])))
    _yaz(os.path.join(kok, "src", "a.py"), DAMGA_A)
    # EKSIK defter (arizali motorla kuruldu) ve BOZUK defter
    eksik = _hafiza_proje(motor, taban, "damga_eksik", DAMGA_DOSYALAR)
    kos(_BOZUK_ADRES[0], eksik, "adres", "--kur")
    kod, o, e, govde, _ad = _not_kos(motor, eksik, "1. `tekil_islev` degisti.")
    if kod != 0 or govde != "1. `tekil_islev` degisti." or "ATIF OLCULEMEDI: adres defteri EKSIK" not in o:
        b.append(("DAMGA-EKSIK", "EKSIK defter: exit=%s govde=%r cikti=%r (metin AYNI + `adres defteri EKSIK` beklenir)" % (kod, govde, o[-200:])))
    bozuk = _hafiza_proje(motor, taban, "damga_bozuk", DAMGA_DOSYALAR)
    os.makedirs(os.path.dirname(_defter_yolu(bozuk)), exist_ok=True)
    _yaz(_defter_yolu(bozuk), "bu bir defter degil\n")
    kod, o, e, govde, _ad = _not_kos(motor, bozuk, "1. `tekil_islev` degisti.")
    if kod != 0 or govde != "1. `tekil_islev` degisti." or "ATIF OLCULEMEDI: adres defteri BOZUK" not in o:
        b.append(("DAMGA-BOZUK", "BOZUK defter: exit=%s govde=%r cikti=%r" % (kod, govde, o[-200:])))
    # kok disina kacan defter yolu
    yol = _hafiza_proje(motor, taban, "damga_yol", {"src/a.py": DAMGA_A})
    kur(motor, yol)
    dis = os.path.join(os.path.dirname(yol), "dis_proje")
    _yaz(os.path.join(dis, "x.py"), "def dis_islev(x):\n    return x\n")
    sha = hashlib.sha256(b"def dis_islev(x):\n    return x").hexdigest()
    p = _defter_yolu(yol)
    metin = io.open(p, encoding="utf-8", newline="").read()
    _yaz(p, metin + "../dis_proje/x.py\tdosya\t%s\t1\t2\t%s\n../dis_proje/x.py\tfonksiyon\tdis_islev\t1\t2\t%s\n" % (sha, sha[:8], sha[:8]))
    kod, o, e, govde, _ad = _not_kos(motor, yol, "1. `dis_islev` kok disinda.")
    if kod != 0 or govde != "1. `dis_islev` kok disinda." or "ATIF OLCULEMEDI: dis_islev (YOL_GECERSIZ)" not in o:
        b.append(("DAMGA-YOL", "defterdeki kok disi yol okundu / damgalandi: exit=%s govde=%r cikti=%r" % (kod, govde, o[-200:])))
    return b


_BOZUK_ADRES = [None]


def kol_damga_arizali(motor, taban, bozuk, istisnali):
    """Arizali cikarici (C# tablosu patlar) ve damga adiminin KENDI istisnasi `not`u DUSURMEZ: exit 0, fragman YAZILIR, traceback YOK.
    Cikarici kusuru DOSYA basina OLCULEMEDI'dir (DAMGA-CIKARICI): ayni metindeki saglam Python sembolu YINE damgalanir; damga
    adiminin kendi istisnasinda (DAMGA-ISTISNA) metin DEGISMEZ. Defter SAGLAM motorla kuruludur."""
    b = []
    ana = _hafiza_proje(motor, taban, "damga_ariza", DAMGA_DOSYALAR)
    kur(motor, ana)
    kok = os.path.join(taban, "damga_cikarici")
    shutil.copytree(ana, kok)
    metin = "1. `tekil_islev` py'de; `Kapat` cs'te."
    kod, o, e, govde, _ad = _not_kos(bozuk, kok, metin)
    beklenen = "1. `tekil_islev`#%s py'de; `Kapat` cs'te." % DAMGA_IZ
    if kod != 0 or govde != beklenen or "ATIF OLCULEMEDI: Kapat (CIKARICI)" not in o or "Traceback" in (o + e):
        b.append(("DAMGA-CIKARICI", "arizali cikarici: exit=%s govde=%r cikti=%r (exit 0 + saglam sembol damgali + `Kapat (CIKARICI)` beklenir)" % (
            kod, govde, (o + e)[-200:])))
    kok = os.path.join(taban, "damga_istisna")
    shutil.copytree(ana, kok)
    kod, o, e, govde, _ad = _not_kos(istisnali, kok, metin)
    if kod != 0 or govde != metin or "ATIF OLCULEMEDI: RuntimeError" not in o or "Traceback" in (o + e):
        b.append(("DAMGA-ISTISNA", "damga adimi istisnasi: exit=%s govde=%r cikti=%r (exit 0 + metin AYNI + `OLCULEMEDI: RuntimeError` beklenir)" % (
            kod, govde, (o + e)[-200:])))
    return b


def kos_damga(motor, taban, ad, kaynak):
    bozuk = _bozuk_motor(taban, "damga_" + ad, kaynak)
    _BOZUK_ADRES[0] = bozuk
    if kaynak.count(DAMGA_ISTISNA_ANKOR) != 1:
        raise Kurulamadi("damga istisna capasi %d yerde gecti (1 olmali)" % kaynak.count(DAMGA_ISTISNA_ANKOR))
    istisnali, hata = _motor_yaz(kaynak.replace(DAMGA_ISTISNA_ANKOR, DAMGA_ISTISNA_ANKOR + '    raise RuntimeError("bilerek bozuk damga adimi")      # MUTANT\n', 1),
                                 os.path.join(os.path.dirname(taban), "istisna_" + ad), "istisna_" + ad)
    if istisnali is None:
        raise Kurulamadi(hata)
    return kol_damga(motor, taban, bozuk, istisnali)


def _kapi_kosusu(motor, kok):
    cikti = []
    for args in (("kapi",), ("kapi", "--siki"), ("devral", "--kesif")):
        kod, o, e = kos(motor, kok, *args)
        cikti.append((args, kod, o.replace(kok, "<KOK>"), e.replace(kok, "<KOK>")))
    return cikti


def kol_etki(motor, taban, bozuk_motor):
    """A-ETKI: cikarici BILEREK bozukken (`bozuk_motor`: _adres_cikar istisna firlatir) `kapi`/`kapi --siki`/`devral --kesif`
    ciktisi ILE bozulmamis motorunki bayt-bayt ayni olmali. Ayni baslangic durumu icin ayni projenin iki KOPYASI kosulur."""
    b = []
    ana = proje(taban, "etki", dict((yol, m) for yol, m in FIKSTUR.values()))
    r = kos(motor, ana, "kur", "--ad", "ADR")
    if r[0] != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (r[0], (r[1] + r[2]).strip()[-160:]))
    _git(ana, "add", "-A")
    _git(ana, "commit", "-q", "-m", "hafiza")
    kopya = os.path.join(taban, "etki_kopya")
    shutil.copytree(ana, kopya)
    saglam, bozuk = _kapi_kosusu(motor, ana), _kapi_kosusu(bozuk_motor, kopya)
    for s, z in zip(saglam, bozuk):
        if s != z:
            b.append(("ETKI", "`%s` ciktisi adres cikaricisi bozukken DEGISTI: exit %s -> %s; ilk fark: %r" % (
                " ".join(s[0]), s[1], z[1], [(x, y) for x, y in zip((s[2] + s[3]).split("\n"), (z[2] + z[3]).split("\n")) if x != y][:1])))
    return b


_TARIH = re.compile(r"\d{4}-\d{2}-\d{2}(?:-\d{4})?")     # `not`/`derle` ciktisinda degisken olan TEK sey: gun ve gunluk dosya adindaki SSDD
YUKLEME_KOMUTLARI = (("kapi",), ("kapi", "--siki"), ("devral", "--kesif"),
                     ("not", "--konu", "genel-durum", "--tur", "durum", "--metin", "yukleme ani sinamasi"), ("derle",))


def _normalle(kok, metin):
    return _TARIH.sub("<TARIH>", metin.replace(kok, "<KOK>"))


def _yukleme_kosusu(motor, kok):
    """`YUKLEME_KOMUTLARI`ni sirayla kosar -> [(args, exit, stdout, stderr)] (kok yolu ve gun/saat normallestirilmis)."""
    cikti = []
    for args in YUKLEME_KOMUTLARI:
        kod, o, e = kos(motor, kok, *args)
        cikti.append((args, kod, _normalle(kok, o), _normalle(kok, e)))
    return cikti


def kol_etki_yukleme(motor, taban, yukleme_bozuk):
    """A-ETKI (YUKLEME ANI): adres desen/tablo ogesi YUKLEMEDE patlayan motorda (`yukleme_bozuk`) kapi/kapi --siki/devral --kesif/
    not/derle ciktisi temiz motorunkiyle bayt-bayt ayni; `adres --kur` ise exit 3 (ARAC KUSURU)."""
    b = []
    ana = proje(taban, "yukleme", dict((yol, m) for yol, m in FIKSTUR.values()))
    r = kos(motor, ana, "kur", "--ad", "ADR")
    if r[0] != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (r[0], (r[1] + r[2]).strip()[-160:]))
    _git(ana, "add", "-A")
    _git(ana, "commit", "-q", "-m", "hafiza")
    kopya = os.path.join(taban, "yukleme_kopya")
    shutil.copytree(ana, kopya)
    saglam, bozuk = _yukleme_kosusu(motor, ana), _yukleme_kosusu(yukleme_bozuk, kopya)
    for s, z in zip(saglam, bozuk):
        if s != z:
            b.append(("ETKI-YUKLEME", "`%s` ciktisi adres deseni YUKLEMEDE patlarken DEGISTI: exit %s -> %s; ilk fark: %r" % (
                " ".join(s[0]), s[1], z[1], [(x, y) for x, y in zip((s[2] + s[3]).split("\n"), (z[2] + z[3]).split("\n")) if x != y][:1])))
    kod, o, e = kos(yukleme_bozuk, kopya, "adres", "--kur")
    if kod != 3:
        b.append(("ETKI-YUKLEME", "yukleme-bozuk motorda `adres --kur` exit=%s (3 = ARAC KUSURU beklenir); cikti=%r" % (
            kod, (o + e).strip()[-120:])))
    return b


YUKLEME_ANKOR_DESEN = '_AD_BRC = _ad_re(r"[{}]")\n'
YUKLEME_ANKOR_TABLO = (r'    delegate = (re.compile(r"%sdelegate\s+%s\s+(?P<ad>%s)\s*(?:%s)?\(" % (mod, tip, _N, _G2)), "tip", "")' + "\n")


def _yukleme_bozuk_yaz(kaynak, hedef_dizin, ad):
    """Yukleme aninda patlayan motor kopyasi: bir MODUL DUZEYI desene (`_AD_BRC`) VE bir TABLO ogesine (C# `delegate` kurali) gecersiz
    regex enjekte edilir. Tembel kurulumda ikisi de ilk `adres` kullanimina kadar patlamaz."""
    for ankor in (YUKLEME_ANKOR_DESEN, YUKLEME_ANKOR_TABLO):
        if kaynak.count(ankor) != 1:
            return None, "yukleme bozucu capasi %d yerde gecti (1 olmali): %r" % (kaynak.count(ankor), ankor.strip()[:60])
    metin = kaynak.replace(YUKLEME_ANKOR_DESEN, '_AD_BRC = _ad_re(r"[{")      # MUTANT: yukleme-bozuk desen\n', 1)
    metin = metin.replace(YUKLEME_ANKOR_TABLO, '    delegate = (re.compile("(("), "tip", "")      # MUTANT: yukleme-bozuk tablo ogesi\n', 1)
    return _motor_yaz(metin, hedef_dizin, ad)


def _bozuk_motor_yaz(kaynak, hedef_dizin, ad):
    """Cikaricisi BILEREK bozuk motor kopyasi (A-ETKI kontrolu)."""
    ankor = '    if dil == "py":\n        return _ad_py(metin)\n'
    if kaynak.count(ankor) != 1:
        return None, "bozucu capa %d yerde gecti (1 olmali)" % kaynak.count(ankor)
    metin = kaynak.replace(ankor, '    raise RuntimeError("bilerek bozuk adres cikaricisi")      # MUTANT\n' + ankor, 1)
    return _motor_yaz(metin, hedef_dizin, ad)


def kos_etki(motor, taban, ad, kaynak):
    bozuk, hata = _bozuk_motor_yaz(kaynak, os.path.join(os.path.dirname(taban), "bozuk_" + ad), "bozuk_" + ad)
    if bozuk is None:
        raise Kurulamadi(hata)
    yukleme, hata = _yukleme_bozuk_yaz(kaynak, os.path.join(os.path.dirname(taban), "yukleme_" + ad), "yukleme_" + ad)
    if yukleme is None:
        raise Kurulamadi(hata)
    return kol_etki(motor, taban, bozuk) + kol_etki_yukleme(motor, taban, yukleme)


def kol_komut_satiri(motor, taban):
    """A-KOMUT-SATIRI (YALNIZ Windows): toplam yol uzunlugu > 32.767 kr gercek git projesinde `--kur` COKMEZ ve kaynak=git."""
    if os.name != "nt":
        return None
    yollar = ["veri/w%04d_%s.py" % (i, "q" * 56) for i in range(UZUN_YOL_ADET)]
    kok = proje(taban, "uzun", dict((y, "def f():\n    return 1\n") for y in yollar))
    if max(len(os.path.join(kok, *y.split("/"))) for y in yollar) >= 260:
        raise Kurulamadi("tek yol >= 260 (TEMP kisa degil): %s" % kok)
    kod, o, e = kos(motor, kok, "adres", "--kur")
    if kod != 0 or "git (izlenen dosyalar)" not in o:
        return [("KOMUT-SATIRI", "43.200 kr yol kumesinde `--kur` exit=%s; cikti=%r" % (kod, (o + e).strip()[:160]))]
    return []


def kos_komut_satiri(motor, taban, _ad, _kaynak):
    w = kol_komut_satiri(motor, taban)
    return [("OLCULEMEDI-WIN", "bu platformda sinir yok")] if w is None else w


# kol adi -> kosucu(motor, kol_tabani, ad, motor_kaynagi) -> [(etiket, mesaj)]
KOLLAR = {
    "A-TANIM": lambda m, t, _a, _k: kol_tanim(m, t),
    "A-CAGIRAN": lambda m, t, _a, _k: kol_cagiran(m, t),
    "A-PARMAK": lambda m, t, _a, _k: kol_parmak(m, t),
    "A-BAYAT": lambda m, t, _a, _k: kol_bayat(m, t),
    "A-DETERMINIZM": lambda m, t, _a, _k: kol_determinizm(m, t),
    "A-MASKE": lambda m, t, _a, _k: kol_maske(m, t),
    "A-ATLA": lambda m, t, _a, _k: kol_atla(m, t),
    "A-ETKI": kos_etki,
    "A-EZME": kos_ezme,
    "A-EKSIK": kos_eksik,
    "P5-DAMGA": kos_damga,
    "A-KOMUT-SATIRI": kos_komut_satiri,
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
# ankor/yeni ayni uzunlukta TUPLE olabilir: sabotaj birden cok yerde birlikte uygulanir (her ankor TAM 1 kez).
# degisiklik zamanini (POSIX ctime / Windows ChangeTime) anahtardan cikarir: "ayni boyut + geri alinmis mtime" ve eski deftere bagli onbellek onun YUZUNDEN gorulur; racy ve ozet
# baglama sabotajlari kendi eksenlerinde ISIRABILSIN diye ctime'i de kor eder (aksi halde ctime onlari ortuk korurdu).
CTIME_ANKOR = 'ct = _adres_nt_degisim_ns(kok, p) if os.name == "nt" else st.st_ctime_ns'
CTIME_KOR = "ct = 0"
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
    ("M-T5 TS uye deseninde bitisik \\s* dizileri GERI gelir (kubik geri izleme)", "A-TANIM", "TANIM-TS-SURE",
     r'        (re.compile(r"%s(?:\*\s*)?(?P<ad>%s)\s*(?:\?\s*)?%s\(" % (_TS_MOD, _N, _TS_GN)), "metot", "j"),' + "\n",
     r'        (re.compile(r"%s\*?\s*(?P<ad>%s)\s*\??\s*(?:%s)?\(" % (_TS_MOD, _N, _G2)), "metot", "j"),' + "\n"),
    ("M-T6 baslik taramasi bosluk dizisindeki HER satir sonunda ASI hesaplar (kuadratik)", "A-TANIM", "TANIM-TS-SURE",
     r'        k = _ad_bosluk(S.m, k, b) if S.m[k:k + 1] == "\n" else k + 1',
     "        k += 1"),
    ("M-C1 tanim satiri HARIC tutulmaz (tanim kendini cagiran sanilir)", "A-CAGIRAN", "CAGIRAN-TANIM-HARIC",
     "            if (yol, satir) not in tanim_satiri:\n",
     "            if True:      # MUTANT\n"),
    ("M-C2 cagiranlar HIC aranmaz", "A-CAGIRAN", "CAGIRAN-VAR",
     "        arama = _adres_arama(adlar[0]) if len(adlar) == 1 else None\n",
     "        arama = None      # MUTANT\n"),
    ("M-M1 cagiran taramasi MASKESIZ (ham metin taranir)", "A-MASKE", "MASKE",
     "        maske = _ad_maske(metin, ana, ac, True)\n",
     "        maske = metin      # MUTANT\n"),
    ("M-M2 Python dosyalarinda maske YOK (yalniz py ham taranir)", "A-MASKE", "MASKE",
     "        maske = _ad_maske(metin, ana, ac, True)\n",
     '        maske = metin if dil == "py" else _ad_maske(metin, ana, ac, True)      # MUTANT\n'),
    ("M-M3 interpolasyon delikleri MASKELENIR (delik_kod kapali)", "A-MASKE", "MASKE-DELIK",
     "        maske = _ad_maske(metin, ana, ac, True)\n",
     "        maske = _ad_maske(metin, ana, ac)      # MUTANT\n"),
    ("M-M4 Dart `$ad` basit ic eklemesi MASKELENIR", "A-MASKE", "MASKE-DELIK",
     r'    delik = None if ham else r"\$\{|\$(?=[A-Za-z_])"' + "\n",
     r'    delik = None if ham else r"\$\{"      # MUTANT' + "\n"),
    ("M-M5 maskelenen gecis NOTU basilmaz", "A-MASKE", "MASKE-NOT",
     '        print("NOT: %d yorum/metin icindeki gecis sayilmadi" % notlar[0])\n',
     "        pass      # MUTANT\n"),
    ("M-M6 maskelenen gecis sayisi YANLIS (+1)", "A-MASKE", "MASKE-NOT",
     "    maskeli = sum(",
     "    maskeli = 1 + sum("),
    ("M-M7 maske kurulamadi NOTU basilmaz (ham tarama SESSIZ)", "A-MASKE", "MASKE-HAM",
     '        print("NOT: %d dosyada maske kurulamadi - ham metin tarandi (o dosyada yorum/metin icindeki gecisler de sayildi)" % notlar[1])\n',
     "        pass      # MUTANT\n"),
    ("M-M8 JSX etiket adlari MASKELENIR (bilesen kullanimi cagiran sayilmaz)", "A-MASKE", "MASKE-GERCEK",
     '    if ad and ("." in ad or not "a" <= ad[0] <= "z"):\n',
     "    if False:      # MUTANT\n"),
    ("M-M9 kucuk harfli HTML etiket adlari da KOD sayilir", "A-MASKE", "MASKE",
     '    if ad and ("." in ad or not "a" <= ad[0] <= "z"):\n',
     "    if ad:      # MUTANT\n"),
    ("M-M10 Python/Dart dize ONEK harfi maskede KALIR", "A-MASKE", "MASKE",
     '    p = len(seg) - len(seg.lstrip(_AD_HARF)) if kod and g == "ds" else 0\n',
     "    p = 0      # MUTANT\n"),
    ("M-M11 maske ARAC KUSURU yutulur (ham taramaya duser, exit 0)", "A-MASKE", "MASKE-KUSUR",
     "    except RecursionError:\n        return _adres_satir_isabetleri(metin, desen), 0, 1\n",
     "    except Exception:      # MUTANT\n        return _adres_satir_isabetleri(metin, desen), 0, 1\n"),
    ("M-M12 C# ham interpolasyonlu dizenin delikleri taranmaz (delik icindeki cagri KAYBOLUR)", "A-MASKE", "MASKE-DELIK",
     "    if nq >= 3 and dolar:  ",
     "    if False:  "),
    ("M-M13 Python bicim belirteci KOD sayilir (`f\"{x:ad}\"` adli cagiran sizar)", "A-MASKE", "MASKE",
     "    return _ad_delik(t, i, _ad_pm_ic, _AD_DELIK_PAR_PY, 1)\n",
     "    return _ad_delik(t, i, _ad_pm_ic, _AD_DELIK_PAR, 1)      # MUTANT: `:` aranmaz\n"),
    ("M-M14 f-dize deligi IKI KEZ taranir (ic ice dizelerde ustel sure)", "A-MASKE", "MASKE-DERIN",
     "    return _ad_delik(t, i, _ad_pm_ic, _AD_DELIK_PAR_PY, 1)\n",
     "    _ad_delik(t, i, _ad_pm_ic, _AD_DELIK_PAR_PY, 1)      # MUTANT\n    return _ad_delik(t, i, _ad_pm_ic, _AD_DELIK_PAR_PY, 1)\n"),
    ("M-M15 C# bicim belirteci KOD sayilir (`$\"{x,10:ad}\"` adli cagiran sizar)", "A-MASKE", "MASKE",
     "    return _ad_delik(t, i, _ad_cs_ic, _AD_DELIK_PAR_CS_K, 2)\n",
     "    return _ad_delik(t, i, _ad_cs_ic, _AD_DELIK_PAR_CS)      # MUTANT\n"),
    ("M-M16 C# `global::` takma adi bicim belirteci baslatir (delik icindeki cagri KAYBOLUR)", "A-MASKE", "MASKE-DELIK",
     '                if kolon == 2 and t[i:i + 1] == ":":\n',
     "                if False:      # MUTANT\n"),
    ("M-A1 atlama KAPALI (gomulu/uretilmis dosyalar taranir)", "A-ATLA", "ATLA",
     "        et = _adres_atla_etiketi(y)\n",
     "        et = None      # MUTANT\n"),
    ("M-A2 ATLANAN satiri basilmaz (SESSIZ atlama)", "A-ATLA", "ATLA-BEYAN",
     '        print("  " + _adres_atlanan_satiri(atlanan))\n',
     "        pass      # MUTANT\n"),
    ("M-A3 baslikta atlanan alani yok (defterde SESSIZ atlama)", "A-ATLA", "ATLA-BEYAN",
     "_adres_disi_metni(atlanan)))",
     '"-"))      # MUTANT' + "\n"),
    ("M-A4 dizin eslesmesi ALT DIZGE (src/build_tools/ de atlanir)", "A-ATLA", "ATLA",
     "        if parca in _ADRES_ATLA_DIZIN:\n",
     "        if any(d in parca for d in _ADRES_ATLA_DIZIN):      # MUTANT\n"),
    ("M-A5 dizin eslesmesi buyuk/kucuk harf DUYARSIZ (src/Dist/ de atlanir)", "A-ATLA", "ATLA",
     "        if parca in _ADRES_ATLA_DIZIN:\n",
     "        if parca.lower() in _ADRES_ATLA_DIZIN:      # MUTANT\n"),
    ("M-A6 atlanan kod-disi dosya KAPSAM DISI sayimina girer (atlama sayimdan SONRA)", "A-ATLA", "ATLA",
     "        et = _adres_atla_etiketi(y)\n",
     "        et = _adres_atla_etiketi(y) if uz in _ADRES_UZANTI else None      # MUTANT\n"),
    ("M-A7 sorgu suzgeci YOK (bayatlik atlanan dosyalari sayar)", "A-ATLA", "ATLA-BAYAT",
     "    kod = _adres_yol_ayir(_adres_dosyalar(kok)[1])[0]\n",
     "    kod = dict((d, []) for d in _ADRES_DIL_SIRA)      # MUTANT: sorgu suzgeci yok\n"
     "    for y in _adres_dosyalar(kok)[1]:\n"
     "        if os.path.splitext(y)[1].lower() in _ADRES_UZANTI:\n"
     "            kod[_ADRES_UZANTI[os.path.splitext(y)[1].lower()]].append(y)\n"),
    ("M-P1 satir sonu normallestirmesi KAPALI (CRLF + bosluk)", "A-PARMAK", "PARMAK-CRLF",
     '    s = _ADRES_SON_BOSLUK.sub("", _ADRES_SATIR_SONU.sub("\\n", s))\n',
     "    s = s      # MUTANT\n"),
    ("M-P2 yalniz satir sonu BOSLUGU kirpilmaz (CRLF hala cevrilir)", "A-PARMAK", "PARMAK-BOSLUK",
     '_ADRES_SON_BOSLUK = _ad_re(r"(?<![ \\t])[ \\t]+(?=\\n|\\Z)")',
     '_ADRES_SON_BOSLUK = _ad_re(r"(?!)")  # MUTANT: '),
    ("M-P3 parmak izi SABIT (govde degisince degismez)", "A-PARMAK", "PARMAK-DEGISIR",
     '    return _adres_sha("\\n".join(satirlar[bas - 1:bit]))[:8]\n',
     '    return "00000000"      # MUTANT\n'),
    ("M-B1 agac ozeti karsilastirmasi KAPALI (bayat hic bildirilmez)", "A-BAYAT", "BAYAT-VAR",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != baslik.get("ozet")\n',
     "    bayat = False      # MUTANT\n"),
    ("M-B2 agac ozeti HER ZAMAN farkli (degismeyen agac bayat sanilir)", "A-BAYAT", "BAYAT-YOK",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != baslik.get("ozet")\n',
     "    bayat = True      # MUTANT\n"),
    ("M-B3 RACY korumasi KAPALI (taze dosya da onbellege girer; ctime de kor: racy tek koruma kalsin)", "A-BAYAT", "BAYAT-ZAMAN",
     ("    return max(anahtar[0], anahtar[2]) < t0 - _ADRES_ONB_PAY\n", CTIME_ANKOR),
     ("    return True      # MUTANT\n", CTIME_KOR)),
    ("M-B4 ucuz yol HER ZAMAN guvenir (anahtar karsilastirmasi yok; dosya degisti)", "A-BAYAT", "BAYAT-VAR",
     "    sha = g[3] if (anahtar is not None and g is not None and g[:3] == anahtar) else None\n",
     "    sha = g[3] if g is not None else None      # MUTANT\n"),
    ("M-B5 ucuz yol HER ZAMAN guvenir (anahtar karsilastirmasi yok; git add)", "A-BAYAT", "BAYAT-STAGE",
     "    sha = g[3] if (anahtar is not None and g is not None and g[:3] == anahtar) else None\n",
     "    sha = g[3] if g is not None else None      # MUTANT\n"),
    ("M-B6 ucuz yol HER ZAMAN guvenir (anahtar karsilastirmasi yok; commit)", "A-BAYAT", "BAYAT-COMMIT",
     "    sha = g[3] if (anahtar is not None and g is not None and g[:3] == anahtar) else None\n",
     "    sha = g[3] if g is not None else None      # MUTANT\n"),
    ("M-B7 anahtar yalniz mtime (boyut yok sayilir)", "A-BAYAT", "BAYAT-BOYUT",
     "    sha = g[3] if (anahtar is not None and g is not None and g[:3] == anahtar) else None\n",
     "    sha = g[3] if (anahtar is not None and g is not None and g[0] == anahtar[0]) else None      # MUTANT\n"),
    ("M-B8 onbellek eski deftere (ozet) BAGLANMAZ (ctime de kor: tek koruma ozet baglamasi kalsin)", "A-BAYAT", "BAYAT-KUR",
     ('        if v["surum"] != _ADRES_ONB_SURUM or v["ozet"] != ozet:\n', CTIME_ANKOR),
     ('        if v["surum"] != _ADRES_ONB_SURUM:      # MUTANT\n', CTIME_KOR)),
    ("M-B9 bozuk onbellek istisnasi YUTULMAZ (komut duser)", "A-BAYAT", "BAYAT-ONB-BOZUK",
     "    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, RecursionError, OverflowError):\n",
     "    except OSError:      # MUTANT\n"),
    ("M-B12 ctime anahtarda YOK (ayni boyut + geri alinmis eski mtime GORULMEZ)", "A-BAYAT", "BAYAT-CTIME",
     CTIME_ANKOR, CTIME_KOR),
    ("M-B13 tasan sayili (1e999) onbellek OverflowError ile komutu dusurur", "A-BAYAT", "BAYAT-ONB-BOZUK",
     "RecursionError, OverflowError):\n", "RecursionError):      # MUTANT\n"),
    ("M-B10 onbellek YAZMA hatasi komutu dusurur", "A-BAYAT", "BAYAT-ONB-YAZ",
     "        os.replace(gecici, yol)\n    except OSError:\n",
     "        os.replace(gecici, yol)\n    except KeyError:      # MUTANT\n"),
    ("M-B11 gecici dizin PROJE ICINDE olsa da onbellek yazilir (proje agacina dosya EKLENIR)", "A-BAYAT", "BAYAT-ONB-PROJE",
     "    if icinde:\n        return None\n",
     "    if False:      # MUTANT\n        return None\n"),
    ("M-C3 ham bayt on suzmesi BOM'a bakmaz (UTF-16 dosyadaki cagri KAYBOLUR)", "A-CAGIRAN", "CAGIRAN-KODLAMA",
     "arama[2] not in ham and _adres_bom(ham) is None and ",
     "arama[2] not in ham and "),
    ("M-C4 ham bayt on suzmesi ortadaki U+FEFF'e bakmaz (`A<FEFF>c` cagrisi KAYBOLUR)", "A-CAGIRAN", "CAGIRAN-FEFF",
     r' and ham.find(b"\xef\xbb\xbf", 1) < 0:', ":      # MUTANT"),
    ("M-C5 ASCII-disi ad da UTF-8 bayt ipucuyla aranir (latin-1 dosyadaki cagri KAYBOLUR)", "A-CAGIRAN", "CAGIRAN-ASCII-DISI",
     'ad.encode("ascii") if ad.isascii() else None', 'ad.encode("utf-8")'),
    ("M-D1 siralama KAPALI", "A-DETERMINIZM", "DETERMINIZM-SIRA",
     "    sat.sort(key=lambda r: (r[0], r[3], -r[4], r[1], r[2]))\n",
     "    pass      # MUTANT\n"),
    ("M-D2 baslik surec numarasi tasir (iki kosum farkli)", "A-DETERMINIZM", "DETERMINIZM-AYNI",
     "% (_ADRES_BICIM, SURUM, kaynak,",
     "% (_ADRES_BICIM, SURUM + str(os.getpid()), kaynak,"),
    ("M-E1 `kapi` adres cikaricisini cagirir", "A-ETKI", "ETKI",
     "    kok = kok_bul(a.kok); _KAPI_KOK[0] = kok\n    rc = rc_oku(kok); y = Y(kok, rc)\n",
     "    kok = kok_bul(a.kok); _KAPI_KOK[0] = kok\n    rc = rc_oku(kok); y = Y(kok, rc)\n"
     '    _adres_cikar("py", "x = 1")      # MUTANT: kapi adres koduna baglandi\n'),
    ("M-E2 tembel regex vekili EAGER (desenler yuklemede derlenir)", "A-ETKI", "ETKI-YUKLEME",
     "    return _AdRe(kaynak, bayrak)\n",
     "    return re.compile(kaynak, bayrak)      # MUTANT\n"),
    ("M-E3 desen TABLOLARI modul duzeyinde kurulur", "A-ETKI", "ETKI-YUKLEME",
     "def _ad_siniflandir(S, i, j, son, ust):\n",
     "_ad_tablo()      # MUTANT: tablolar yuklemede kurulur\n\n\ndef _ad_siniflandir(S, i, j, son, ust):\n"),
    ("M-E4 cikarici istisnasi `sozdizimi` sayilir (adres --kur exit 3 yerine 0)", "A-ETKI", "ETKI-YUKLEME",
     '                atla.setdefault("cikarici", []).append(yol)\n',
     '                atla.setdefault("sozdizimi", []).append(yol)      # MUTANT\n'),
    ("M-Z1 koruma KAPALI (arac kusurunda saglam defter ezilir)", "A-EZME", "EZME",
     '    korunan = _adres_eski_saglam(p) if atla.get("cikarici") else None',
     "    korunan = None      # MUTANT"),
    ("M-Z2 eksik kurulus basari der (`KURULDU`; `EKSIK` yok)", "A-EZME", "EZME-EKSIK",
     '"EKSIK " if atla.get("cikarici") else ""',
     '""'),
    ("M-Z3 EKSIK defter de SAGLAM sayilir (ustune yazilmaz, korunur)", "A-EZME", "EZME-USTUNE",
     '    if durum != "tamam" or _adres_eksik_mi(veri[0]):\n        return None\n',
     '    if durum != "tamam":      # MUTANT\n        return None\n'),
    ("M-Z4 basliga `cikarici=` damgasi YAZILMAZ (eksik defter taninmaz)", "A-EZME", "EZME-EKSIK",
     '        baslik += " cikarici=%d" % len(atla["cikarici"])',
     "        pass      # MUTANT"),
    ("M-Z5 KORUNDU yolunda ATLANDI satiri basilmaz (korunan defterin sebebi gizlenir)", "A-EZME", "EZME-KORUNDU",
     '        print("ESKI DEFTER KORUNDU: %s (%d bayt, tanim %s)" % (_rel(p, kok), korunan[0], korunan[1]))\n'
     '        print("  " + _adres_sebep_satiri("ATLANDI", atla))\n',
     '        print("ESKI DEFTER KORUNDU: %s (%d bayt, tanim %s)" % (_rel(p, kok), korunan[0], korunan[1]))\n'
     "        pass      # MUTANT\n"),
    ("M-X1 sorguda yeniden deneme KAPALI (eksik defter 'guncel' kalir)", "A-EKSIK", "EKSIK-YENIDEN",
     '    if durum == "tamam" and _adres_eksik_mi(veri[0]):',
     "    if False:      # MUTANT"),
    ("M-X2 EKSIK olcutu `atlandi>0` (sozdizimi atlamasi da yeniden kurdurur)", "A-EKSIK", "EKSIK-SOZDIZIMI",
     '    return baslik.get("cikarici", "0") not in ("", "0")\n',
     '    return baslik.get("atlandi", "0") not in ("", "0")      # MUTANT\n'),
    ("M-X3 yeniden kurulus her seferinde (onarilan defter de EKSIK sanilir)", "A-EKSIK", "EKSIK-TEKRAR",
     '    return baslik.get("cikarici", "0") not in ("", "0")\n',
     "    return True      # MUTANT\n"),
    ("M-X4 yeniden kurma hala eksikse sessiz (EKSIK satiri basilmaz)", "A-EKSIK", "EKSIK-HALA",
     '        print("ADRES DEFTERI EKSIK: %d dosyada cikarici istisnasi (yeniden kurma denendi: hala eksik) - hafiza.py adres --kur"\n'
     '              % len(atla["cikarici"]))\n',
     "        pass      # MUTANT\n"),
    ("M-D1 cozum atlanir (belirtec hic cozulmez: damga YOK)", "P5-DAMGA", "DAMGA-VAR",
     "    cozum = dict(((m, t), _damga_coz(kok, indeks, onbellek, m, t)) for m, t in tum)\n",
     '    cozum = dict(((m, t), ("yok", None, None)) for m, t in tum)      # MUTANT\n'),
    ("M-D2 TEK kurali YOK (ayni ad iki dosyada ilkine damgalanir)", "P5-DAMGA", "DAMGA-COKLU",
     '        return ("tek", a[0][0], a[0][1]) if len(a) == 1 else (("coklu", len(a), None) if a else ("yok", None, None))\n',
     '        return ("tek", a[0][0], a[0][1]) if a else ("yok", None, None)      # MUTANT\n'),
    ("M-D3 idempotent DEGIL (damgali belirtec yeniden damgalanir)", "P5-DAMGA", "DAMGA-TEKRAR",
     ('    aday = sorted({(j[1], j[2]) for _i, j in jetonlar if j[3] is None and j[4]})\n',
      '    for i, (son, m, t, _d, olur) in reversed([(i, j) for i, j in jetonlar if j[3] is None]):\n'),
     ('    aday = sorted({(j[1], j[2]) for _i, j in jetonlar if j[4]})      # MUTANT\n',
      '    for i, (son, m, t, _d, olur) in reversed(jetonlar):      # MUTANT\n')),
    ("M-D4 kod citi ici de damgalanir", "P5-DAMGA", "DAMGA-CIT",
     "    jetonlar = [(i, j) for i, s in enumerate(L) if not ic[i] for j in _damga_jetonlar(s)]\n",
     "    jetonlar = [(i, j) for i, s in enumerate(L) for j in _damga_jetonlar(s)]      # MUTANT\n"),
    ("M-D5 damga adimi istisnasi `not`a SIZAR (yakalama dar)", "P5-DAMGA", "DAMGA-ISTISNA",
     "    except (Exception, SystemExit) as e:  # noqa: BLE001 - KISIT 6-3: damga/dogus",
     "    except KeyError as e:  # noqa: BLE001 - KISIT 6-3: damga/dogus"),
    ("M-D6 yol:N EN GENIS kapsayan tanima damgalanir (uye degil sinif)", "P5-DAMGA", "DAMGA-IC",
     "    en_dar = min(k[0] for k in kap)\n",
     "    en_dar = max(k[0] for k in kap)      # MUTANT\n"),
    ("M-D7 cikarici kusuru yutulmaz (per-dosya yakalama dar: `not` exit != 0)", "P5-DAMGA", "DAMGA-CIKARICI",
     "    except Exception:  # noqa: BLE001 - cikarici kusuru",
     "    except KeyError:  # noqa: BLE001 - cikarici kusuru"),
    ("M-D8 `yol:N` satir eslemesi CANLI dosyadan degil commit'li (BAYAT) surumden yapilir", "P5-DAMGA", "DAMGA-BAYAT",
     "    return _damga_ham_satirlar(yol, ham, dil)\n\n\ndef _damga_satirlar(kok, yol, onbellek):\n",
     '    r_ = _adres_git(kok, "show", "HEAD:./" + yol)      # MUTANT: canli yerine commit\'li surum\n'
     "    ham = r_.stdout if r_.returncode == 0 else ham\n"
     "    return _damga_ham_satirlar(yol, ham, dil)\n\n\ndef _damga_satirlar(kok, yol, onbellek):\n"),
    ("M-D9 kapanis backtick'ine bitisik sonekli belirtec de damgalanir (idempotans bozulur)", "P5-DAMGA", "DAMGA-SONEK",
     "d is not None or not _DAMGA_KELIME.match(sonra)",
     "True"),
    ("M-D10 cift/uclu backtick araligi atlanmaz (damga backtick kosusunu boler)", "P5-DAMGA", "DAMGA-CIFT",
     '        if once == "`" or sonra == "`":\n            continue\n',
     "        if False:      # MUTANT\n            continue\n"),
    ("M-D11 ters aralik (M<N) cozulur (ilgisiz sembole damgalanir)", "P5-DAMGA", "DAMGA-ARALIK",
     "    if son < bas or len(dosya) != 1:\n",
     "    if len(dosya) != 1:      # MUTANT\n"),
    ("M-D12 EKSIK defter kullanilir (cikarici kusuru gizlenir)", "P5-DAMGA", "DAMGA-EKSIK",
     '    if _adres_eksik_mi(veri[0]):\n        return "eksik", "adres defteri EKSIK (cikarici kusuru) - hafiza.py adres --kur"\n',
     '    if False:      # MUTANT\n        return "eksik", "adres defteri EKSIK (cikarici kusuru) - hafiza.py adres --kur"\n'),
    ("M-D13 defterdeki kok disi yol (`..`) reddedilmez", "P5-DAMGA", "DAMGA-YOL",
     '    if yol.startswith("/") or ".." in yol.split("/"):\n        return None, "YOL_GECERSIZ"\n',
     '    if False:      # MUTANT\n        return None, "YOL_GECERSIZ"\n'),
    ("M-D14 belirtec sirasi KUMEYE birakilir (calismalar arasi sira degisir: determinizm bozulur)", "P5-DAMGA", "DAMGA-DETERMINIZM",
     '    aday = sorted({(j[1], j[2]) for _i, j in jetonlar if j[3] is None and j[4]})\n',
     '    aday = list({(j[1], j[2]) for _i, j in jetonlar if j[3] is None and j[4]})      # MUTANT\n'),
    ("M-D15 damga blogu `oldur` cagirir (stderr'e HATA basar, cikis yolu acilir)", "P5-DAMGA", "DAMGA-OLDUR",
     "    d, yol, tam = cozum\n",
     '    d, yol, tam = cozum\n    oldur("MUTANT: damga blogundan oldur")      # MUTANT\n'),
    ("M-K1 dosya listesi TEK git cagrisina dizilir", "A-KOMUT-SATIRI", "KOMUT-SATIRI",
     '    r = _adres_git(kok, "ls-files", "-z")\n',
     '    r = _adres_git(kok, "ls-files", "-z")\n'
     '    r = _adres_git(kok, "ls-files", "-z", "--", *[x.decode("utf-8", "replace") for x in r.stdout.split(b"\\0") if x])  # MUTANT\n'),
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
    for arg in sys.argv[1:]:            # gelistirme kolayligi: `--kol=A-EZME,A-EKSIK` yalniz o kollari kosar (CI bayraksiz kosar)
        if arg.startswith("--kol="):
            kollar = [k for k in kollar if k in arg[len("--kol="):].split(",")]
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
            sinir = _platform_sinir(etiket)
            if sinir:
                print("  %-60s -> OLCULEMEDI: %s" % (ad, sinir))
                olculemeyen.append(ad)
                continue
            ankorlar, yeniler = (ankor, yeni) if isinstance(ankor, tuple) else ((ankor,), (yeni,))      # tuple: BIRDEN cok yerde sabotaj
            sabotajli = s
            for a1, y1 in zip(ankorlar, yeniler):
                n = s.count(a1)
                if n != 1:
                    print("SONUC: OLCULEMEDI — %s: capa %d yerde gecti (1 olmali): %r" % (ad, n, a1.strip()[:70]))
                    return 2
                sabotajli = sabotajli.replace(a1, y1, 1)
            sab, hata = _motor_yaz(sabotajli, os.path.join(taban, "s%d" % sira), "s%d" % sira)
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
            print("SONUC: YESIL (SINIRLI) — olculebilen her sabotaj ISIRDI; %d OLCULEMEDI (platforma/kullaniciya ozgu)." % len(olculemeyen))
        else:
            print("SONUC: YESIL — tum kollar temiz, %d sabotaj AYRI eksende ISIRDI." % sum(1 for x in SABOTAJLAR if x[1] in kollar))
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

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
  A-EZME, A-EKSIK (P5 K0) ve P5-DAMGA / P5-H20 / P5-DOGUS (P5 K1-K3): ilgili kol fonksiyonlarinin docstring'inde aciklanir.
  P5-SAYIM       (P5.2 K6) damgasiz belirtec arac kusurunda DUSMEZ: ad belirteci de `yol:N` de OLCULEMEDI'ye gecer, ayrim gorunur, siniflarin
                 toplami AZALMAZ (yalniz `yok` olan kadar artar), asiri yuklu `yol:N` COKLU    [SAYIM-ENJEKSIYON|-TOPLAM|-AYRIM|-AD|-YOK|-COKLU]
  P5-SABIT       (P5.2 K5) dil sabitleri (`true false null None True False nil this self void undefined`) aday DEGIL: satir/damga/H20
                 sayimi YOK (tanimli `void` bile); listede OLMAYAN `trueValue`/`TRUE` COZULEMEDI der  [SABIT-VAR|-TAM|-H20]
  P5-BIRLESIK    (P5.2 K4) ad 2-5 tanima cozulunce BIRLESIK damga: `[k tanim]` damga + tekil ad K1 iziyle bayt-ayni; bir tanim degisince /
                 eklenince / silinince H20 `GOVDE DEGISTI`; dosya yeniden adlandirilinca iz DEGISMEZ; 6+ tanim damga YOK + COKLU + K3
                 beyani (tavan korumalari AYRI AYRI: defter satiri / canli / K3); aday dosya arizaliysa ya da KISMEN yoksa (DEFTER_BAYAT)
                 KISMI iz yazilmaz; K3 `<k> tanimdan <x>'u` + silinen + yas notu + 20 dosya tavani (en az dosyali once) + sure butcesi +
                 git nesne kenar durumlari (kayip nesne, dizin yol, .ts/.tsx, `%` yol, >8 MB gecmis); defter ATLANDI notu
                 [BIRLESIK-VAR|-TEKIL|-DEGISTI|-EKLENDI|-YOL|-BAYAT|-TAVAN|-COKLU|-ARIZA|-KARDES|-OZDES|-DOSYACOK|-DOGUS|-SILINEN|
                  -DOSYAYOK|-CALISMA|-BUTCE|-KAP|-ATLANDI|-NESNE|-CIKARICI|-YOLKACIS|-YOLCOKLU|-SAYISIZ]
                 + (P5.3 KALEM 7) BAYAT defterde (`adres --kur` YOK) H20 YENI tanimi da gorur: yeni dosyada 4. tanim · tekil -> coklu ·
                 ayni dosyada yeni tam ad · silinen/tasinan/izlenmeyen dosya · 100/101 bayat dosya ve 8 MiB bayt tavani (OLCULEMEDI
                 [DEFTER_BAYAT], kesin pozitif KORUNUR) · `yol:N` + yeni ayni adli dosya · kapi DISKE YAZMAZ (sicak onbellek dahil) ·
                 bayatlik olcumu arizasi [DEFTER_BAYATLIK] · cikarilamayan yeni dosya kapsami bozar / adi icermiyorsa gurultu yok ·
                 cikarici kusuru [DEFTER_EKSIK] · sayim defterden; hukum `--kur` sonrasiyla BAYT-AYNI
                 + defter `kaynak=git` iken `.git`siz kopya: evren uyusmazligi OLCULEMEDI [DEFTER_BAYATLIK] · degisen dosya cikarilamaz
                 hale gelirse satirlari `--kur` gibi duser · surekli okunamayan dosya gurultu yapmaz · izlenen dosya diskten silinirse bayat
                 `SEMBOL YOK`, `--kur` sonrasi ATLANDI (beyanli ayrisma)
                 [BIRLESIK-TAZE|-TEKIL|-AD|-SILINEN|-TAVAN|-BAYT|-YOL|-YAZMA|-ARIZA|-KAPSAM|-GURULTU|-OKUNMAZ|-EKSIK|-KAYNAK|-SAYIM|-NOT]
  P5.4 (KALEM 8) P5-DAMGA genisler: `not` (K1 damga + K3 dogusta bayat) bayat defterde H20'nin taze kumesini kullanir: yeni dosyada ayni ad ->
                 `[k+1]` damga, hemen kapi GOVDE DEGISTI 0 · tekil -> coklu / yeni tam ad · taze kume cikarilamaz -> damga YOK + OLCULEMEDI
                 (olcum arizasi / 101 dosya / cikarici kusuru) · adaysiz not taze kume cikarmaz · adi iceren cikarilamayan yeni dosya -> damga YOK ·
                 `not` onbellegi yazmaz   [DAMGA-TAZE|-TEKIL|-YOK|-ADAYSIZ|-TAVAN|-BILINMEZ|-GURULTU|-YAZMA]

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
             "P5-DAMGA", "P5-H20", "P5-DOGUS", "P5-BIRLESIK", "P5-SABIT", "P5-SAYIM", "A-KOMUT-SATIRI")
KOL_ETIKET = {"A-TANIM": "TANIM", "A-CAGIRAN": "CAGIRAN", "A-PARMAK": "PARMAK", "A-BAYAT": "BAYAT", "A-DETERMINIZM": "DETERMINIZM", "A-MASKE": "MASKE", "A-ATLA": "ATLA", "A-ETKI": "ETKI", "A-EZME": "EZME", "A-EKSIK": "EKSIK", "P5-DAMGA": "DAMGA", "P5-H20": "H20", "P5-DOGUS": "DOGUS", "P5-BIRLESIK": "BIRLESIK", "P5-SABIT": "SABIT", "P5-SAYIM": "SAYIM", "A-KOMUT-SATIRI": "KOMUT-SATIRI"}
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
    `tmp`: `adres` ve `kapi` icin gecici dizin (varsayilan: projeye ozel `onb_dizini`; `kapi` P5.3'ten beri stat onbellegini OKUR)."""
    ortam = _cikti_kodlamasi_ortami()
    if args[:1] in (("adres",), ("kapi",)) or tmp is not None:
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
# sonu icin yeniden hesaplanirsa n^2 (eski motor 16 KB'de 22 s). Saglam motor milisaniyeler tutar (sure = surec acilisi).
#
# HUKUM ORANLA (IS_EMRI_ADRES_SURE_EKSENI.md, CI #133): "20 s mutlak" esik DUVAR SAATINE baglidir — hizli runner'da kubik geri izleme
# 20 s'nin altinda bitip M-T5'i gorunmez kildi (aralikli: #130 kirmizi, #131/#132 yesil, #133 kirmizi). Duvar saati esigi hukum DEGILDIR;
# ayni girdi iki boyutta (n ve 4n) kosulur, hukum ORANDAN verilir. Dogrusal ≈4, kuadratik ≈16, kubik ≈64.
SURE_BOYUT = {"yorum": (2000, 8000), "satir": (20000, 80000)}      # (n, 4n): yorum = `x` sayisi, satir = `\n` sayisi
SURE_ZAMAN_ASIMI = 20       # (a) MUTLAK ust sinir: asarsa hukum kesin (sabotajli motor dakikalar surer; sinir yalniz kosuyu kisaltir)
SURE_KOSUM = 2              # her boyutta en az 2 kosum, MIN alinir (tek kosumluk gurultu hukmu cevirmez)
SURE_TABAN = 0.5            # (b) gurultu tabani (s): t(4n) bunun altindaysa oran ANLAMSIZ (surec acilisi ~0.35 s, oran ~1 cikar)
SURE_ORAN = 8               # (b) t(4n)/t(n) bunu asarsa dogrusal degil (ara deger: dogrusal 4 < 8 < kuadratik 16)
SURE_ORAN_ACIK = True       # OLCUT SINAMASI bunu kapatip eski (yalniz mutlak) hukmu yeniden uretir
SURE_KAYIT = []             # ham olcumler (eksen, n, [sureler], zaman_asimi_mi): `ADRES_SURE_KAYIT=<dosya>` ile jsonl'a da yazilir


def _sure_girdi(eksen, n):
    if eksen == "yorum":
        return {"src/yorum.ts": "class A {\n  async checkCu/*" + "x" * n + "\n"}
    return {"src/satir.ts": "class A {\n  foo =" + "\n" * n + " 1\n}\n"}


def sure_olc(motor, taban, eksen, n):
    """`adres --kur`u taze projede SURE_KOSUM kez kosar -> (min sure | None (zaman asimi), exit/hata bulgusu | None). Zaman asimi ilk kosumda keser."""
    ham = []
    for _ in range(SURE_KOSUM):
        kok = proje(taban, "sure_%s_%d_%d" % (eksen, n, len(SURE_KAYIT) * 10 + len(ham)), _sure_girdi(eksen, n))
        t0 = time.time()
        try:
            kod, o, e = kos(motor, kok, "adres", "--kur", zaman_asimi=SURE_ZAMAN_ASIMI)
        except subprocess.TimeoutExpired:
            _sure_kayit(eksen, n, ham, True)
            return None, None
        ham.append(round(time.time() - t0, 3))
        if kod != 0:
            _sure_kayit(eksen, n, ham, False)
            return min(ham), "exit=%s: %r" % (kod, (o + e).strip()[-120:])
    _sure_kayit(eksen, n, ham, False)
    return min(ham), None


def _sure_kayit(eksen, n, ham, asim):
    SURE_KAYIT.append((eksen, n, list(ham), asim))
    d = os.environ.get("ADRES_SURE_KAYIT")
    if d:
        with io.open(d, "a", encoding="utf-8") as f:
            f.write(json.dumps({"eksen": eksen, "n": n, "ham_sn": ham, "zaman_asimi": asim, "platform": sys.platform}) + "\n")


def sure_hukmu(t1, t4, oran_acik=True):
    """SAF hukum: t1 = t(n), t4 = t(4n) (None = zaman asimi) -> None (dogrusal) | gerekce. Duvar saati esigi tek basina hukum DEGILDIR."""
    if t1 is None or t4 is None:
        return "%d s MUTLAK siniri asti" % SURE_ZAMAN_ASIMI
    if oran_acik and t4 >= SURE_TABAN and t4 / max(t1, 1e-3) > SURE_ORAN:
        return "sure orani %.1f > %d (t(n)=%.2f s, t(4n)=%.2f s; dogrusal ≈4, kuadratik ≈16, kubik ≈64)" % (t4 / max(t1, 1e-3), SURE_ORAN, t1, t4)
    return None


def sure_olcumleri(motor, taban, boyut):
    """-> {eksen: (t1, t4, hata)}; hata = exit != 0 bulgusu."""
    out = {}
    for eksen, (n, n4) in sorted(boyut.items()):
        t1, h1 = sure_olc(motor, taban, eksen, n)
        t4, h4 = (None, None) if t1 is None else sure_olc(motor, taban, eksen, n4)
        out[eksen] = (t1, t4, h1 or h4)
    return out


SURE_OLCUT_BOYUT = {"yorum": (500, 2000)}      # "HIZLI RUNNER" benzetimi: M-T5 burada 20 s'nin cok altinda bitmeli (yerelde ~7 s)


def olcut_sinamasi(s, taban):
    """OLCUTUN KENDI SABOTAJI (hafiza-kur_olcut_dersi): oran kontrolu KAPALI (yalniz mutlak sinir) + girdi KUCUK -> M-T5 KACMALI; ayni
    olcumde oran ACIK -> YAKALAMALI. Eski/yeni olcut AYNI olcum uzerinde yarisir (tek koşum, iki hukum). -> bulgu listesi."""
    ad = [x for x in SABOTAJLAR if x[0].startswith("M-T5 ")][0]
    if s.count(ad[3]) != 1:
        raise Kurulamadi("olcut sinamasi: M-T5 capasi %d yerde" % s.count(ad[3]))
    sab, hata = _motor_yaz(s.replace(ad[3], ad[4], 1), os.path.join(taban, "olcut"), "olcut")
    if sab is None:
        raise Kurulamadi("olcut sinamasi: " + hata)
    (t1, t4, hata), = sure_olcumleri(sab, os.path.join(taban, "olcutk"), SURE_OLCUT_BOYUT).values()
    eski, yeni = sure_hukmu(t1, t4, False), sure_hukmu(t1, t4, True)
    print("  OLCUT SINAMASI (M-T5, n=%d/%d, t(n)=%s t(4n)=%s): eski olcut (oran KAPALI) -> %s · yeni olcut -> %s" % (
        SURE_OLCUT_BOYUT["yorum"] + ("ASIM" if t1 is None else "%.2f s" % t1, "ASIM" if t4 is None else "%.2f s" % t4,
                                      "KACTI" if not eski else "yakaladi", "YAKALADI" if yeni else "KACTI")))
    b = []
    if eski:
        b.append("OLCUT-DUZENEK: kucuk girdide eski (mutlak) olcut zaten yakaladi — benzetim hizli runner'i temsil etmiyor (%s)" % eski)
    if not yeni:
        b.append("OLCUT-KOR: oran olcutu hizli-runner benzetiminde M-T5'i YAKALAMADI")
    return b


def kol_tanim_sure(motor, taban):
    """A-TANIM (SURE): bozuk TS girdisinde `adres --kur` temiz biter ve suresi DOGRUSAL kalir (oranla; bkz. SURE_*)."""
    b = []
    for eksen, (t1, t4, hata) in sure_olcumleri(motor, taban, SURE_BOYUT).items():
        g = sure_hukmu(t1, t4, SURE_ORAN_ACIK)
        print("      [sure %s n=%d/%d] t(n)=%s t(4n)=%s%s" % (eksen, SURE_BOYUT[eksen][0], SURE_BOYUT[eksen][1],
              "ASIM" if t1 is None else "%.2f s" % t1, "ASIM" if t4 is None else "%.2f s" % t4, " -> " + g if g else ""))
        if hata:
            b.append(("TANIM-TS-SURE", "bozuk TS girdisinde (%s) `adres --kur` %s" % (eksen, hata)))
        elif g:
            b.append(("TANIM-TS-SURE", "bozuk TS girdisinde (%s) `adres --kur` DOGRUSAL degil: %s" % (eksen, g)))
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
# damga; ayni ad iki dosyada / ayni dosyada asiri yuklu -> BIRLESIK damga `[2 tanim]` (6+ tanim: damga YOK + COKLU, P5-BIRLESIK kolu);
# ikinci `not` damgali metinle -> cift damga YOK; `derle`
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
def _sha8(metin):
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()[:8]


def _bir_iz(*izler):
    """BIRLESIK damga izi BEKLENTISI (is emri P5.2 tanimi, motordan DEGIL): sha256("\\n".join(sorted(tek tek govde izleri)))[:8]."""
    return _sha8("\n".join(sorted(izler)))


DAMGA_IZ = hashlib.sha256("def tekil_islev(x):\n    return x + 1".encode("utf-8")).hexdigest()[:8]       # a.py L1-2
DAMGA_IC_IZ = hashlib.sha256("    def kapat_kasa(self):\n        return 0".encode("utf-8")).hexdigest()[:8]     # a.py L10-11 (sinif DEGIL uye)
DAMGA_ORTAK_IZ = _bir_iz(_sha8("def ortak_islev(x):\n    return x"), _sha8("def ortak_islev(y):\n    return y * 2"))   # a.py L5-6 + b.py L1-2
DAMGA_HESAPLA_IZ = _bir_iz(_sha8("    public int Hesapla(int x) => x;"), _sha8("    public int Hesapla(string s) => 0;"))   # Hesap.cs L3, L4
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
                  .replace("`a.py:1-2` ara", "`a.py:1-2`#%s ara" % DAMGA_IZ)
                  .replace("`ortak_islev` iki yerde; `Hesapla` asiri", "`ortak_islev`#%s iki yerde; `Hesapla`#%s asiri" % (DAMGA_ORTAK_IZ, DAMGA_HESAPLA_IZ)))
DAMGA_NOT_ARGS = ("not", "--konu", "genel-durum", "--tur", "durum", "--metin")
DAMGA_ISTISNA_ANKOR = "def _damga_uygula_ic(kok, y, govde):\n"
DAMGA_YASAK_CAGRI = ("oldur", "yaz", "kilit_al", "zincir_halka", "_arsive_tasi", "exit")


def _gunluk_adlari(kok):
    d = os.path.join(kok, "gunluk")
    return set(x for x in os.listdir(d) if x.endswith(".md"))


def _not_kos(motor, kok, metin, butce_ok=False):
    """`not` -> (exit, stdout, stderr, yeni fragmanin govdesi ya da None, fragman adi). Fragman sirasi dosya adindan DEGIL, once/sonra farkindan.
    Doguste bayat sure butcesi (15 sn) YUK altinda asilirsa duzenek KURULAMADI (OLCULEMEDI): temiz kosuda sahte KIRMIZI, sabotaj kosusunda
    sahte ISIRDI verilmez (`butce_ok`: butce yolunu bilerek sinayan vektor)."""
    once = _gunluk_adlari(kok)
    kod, o, e = kos(motor, kok, *(DAMGA_NOT_ARGS + (metin,)))
    if not butce_ok and "sure butcesi asildi" in o:
        raise Kurulamadi("doguste bayat 15 sn butcesi ASILDI (makine yukte): sonuc OLCULEMEDI, temiz/sabotaj hukmu verilmez: %r" % o[-200:])
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
    """P5-DAMGA: tekil ad + `yol:N` + `yol:N-M` damgalanir (DAMGA-VAR) · ic ice tanimda en dar tanim (DAMGA-IC) · ayni ad iki dosyada /
    asiri yuklu: BIRLESIK damga, COKLU satiri YOK (DAMGA-IKILI; birlesik ayrintisi P5-BIRLESIK kolunda) · bulunamayan / ters aralik
    COZULEMEDI (DAMGA-COZULEMEDI / DAMGA-ARALIK) · ikinci `not` damgali metinle
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
    beklenen_satir = ("ATIF DAMGALANDI: 6 (Hesapla#%s [2 tanim], a.py:1-2#%s, a.py:11#%s, a.py:2#%s, ortak_islev#%s [2 tanim], tekil_islev#%s)"
                      % (DAMGA_HESAPLA_IZ, DAMGA_IZ, DAMGA_IC_IZ, DAMGA_IZ, DAMGA_ORTAK_IZ, DAMGA_IZ))
    if kod != 0 or "`tekil_islev`#%s degisti" % DAMGA_IZ not in govde or "`a.py:2`#%s bu" % DAMGA_IZ not in govde:
        b.append(("DAMGA-VAR", "tekil ad ya da `yol:N` damgalanmadi (beklenen iz %s): exit=%s govde=%r" % (DAMGA_IZ, kod, govde[:200])))
    if beklenen_satir not in sat:
        b.append(("DAMGA-VAR", "%r satiri yok: %r" % (beklenen_satir, o[-300:])))
    if "`a.py:11`#%s met" % DAMGA_IC_IZ not in govde:
        b.append(("DAMGA-IC", "ic ice tanimda `yol:N` EN DAR tanima (uye) damgalanmali, sinifa degil (beklenen iz %s): %r" % (DAMGA_IC_IZ, govde[:200])))
    if any(l.startswith("ATIF COKLU") for l in sat) or "`ortak_islev`#%s iki yerde; `Hesapla`#%s asiri" % (DAMGA_ORTAK_IZ, DAMGA_HESAPLA_IZ) not in govde:
        b.append(("DAMGA-IKILI", "ayni ad iki dosyada / asiri yuklu: BIRLESIK damga (`#%s`/`#%s`) VAR + COKLU satiri YOK beklenir: govde=%r cikti=%r" % (
            DAMGA_ORTAK_IZ, DAMGA_HESAPLA_IZ, govde[:160], o[-240:])))
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


# ------------------------------------------------------------------ P5.4 (KALEM 8): `not` bayat defterde H20'nin taze kumesini kullanir
def _dt_not(motor, kok, metin, tmp=None):
    """`not` -> (exit, FRAGMAN SONRASI satirlar, govde, stderr)."""
    once = _gunluk_adlari(kok)
    kod, o, e = kos(motor, kok, *(DAMGA_NOT_ARGS + (metin,)), tmp=tmp)
    yeni = sorted(_gunluk_adlari(kok) - once)
    govde = None
    if len(yeni) == 1:
        ham = io.open(os.path.join(kok, "gunluk", yeni[0]), encoding="utf-8", newline="").read()
        govde = ham.split("\n---\n\n", 1)[1].rstrip("\n")
    return kod, _atif_satirlari(o), govde, e


def _dt_taban(motor, taban, ad, ek=None, n=3):
    """`n` tanimli `ortak_ad` + 4. tanim YENI dosyada COMMIT'li, `adres --kur` YOK (defter BAYAT) -> (kok, 4. tanimin commit sha'si)."""
    kok = _b_proje(motor, taban, ad, n, ek)
    return kok, _b_commit(kok, {"src/p%d.py" % (n + 1): _b_py(n + 1)}, "4. tanim yeni dosyada")


def _v_dtaze(motor, taban, b):
    """DAMGA-TAZE: bayat defter + yeni dosyada ayni ad -> `not` TAZE kumeden `[4 tanim]` damgalar (K1) ve K3 `4 tanimdan 1'i son commit'te`;
    hemen `derle` + `kapi` GOVDE DEGISTI 0 (sahte uyari YOK); `--kur` sonrasi ayni not AYNI damga."""
    b4 = _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])
    kok, sha = _dt_taban(motor, taban, "dt_taze")
    kod, sat, govde, _e = _dt_not(motor, kok, "1. `ortak_ad` dort yerde.")
    if kod != 0 or govde != "1. `ortak_ad`#%s dort yerde." % b4 or "ATIF DAMGALANDI: 1 (ortak_ad#%s [4 tanim])" % b4 not in sat:
        b.append(("DAMGA-TAZE", "bayat defter + yeni dosyada ayni ad: TAZE kumeden `[4 tanim]` damga beklenir: exit=%s govde=%r satirlar=%r" % (kod, govde, sat)))
    if "DIKKAT: ortak_ad 4 tanimdan 1'i son commit'te degisti (%s) - iddiayi kodla teyit et" % sha[:7] not in sat:
        b.append(("DAMGA-TAZE", "K3 TAZE kumeyle `4 tanimdan 1'i son commit'te degisti` beklenir: %r" % sat))
    _b_derle(motor, kok)
    _h20_hukum_say(b, "DAMGA-TAZE", "not'tan hemen sonra kapi: `GOVDE DEGISTI 0` (sahte uyari YOK)", motor, kok, BIRLESIK_TABAN1, None)
    kur(motor, kok)
    _kod, _sat, govde2, _e = _dt_not(motor, kok, "2. `ortak_ad` yine.")
    if govde2 != "2. `ortak_ad`#%s yine." % b4:
        b.append(("DAMGA-TAZE", "`--kur` sonrasi ayni not AYNI damgayi basmali (bayat == taze): govde=%r" % govde2))


def _v_dtaze_tekil(motor, taban, b):
    """DAMGA-TAZE-TEKIL: tekil ad + yeni dosyada ayni adli ikinci tanim -> `[2 tanim]` damga · AYNI dosyada baska sinifta ayni uye adi -> `[2 tanim]`."""
    t_iz = _sha8("def tekil_ad(x):\n    return x")
    kok = _b_proje(motor, taban, "dt_tekil", 1, {"src/a.py": "def tekil_ad(x):\n    return x\n"})
    _b_commit(kok, {"src/b.py": "def tekil_ad(y):\n    return y * 3\n"}, "ikinci tanim yeni dosyada")
    yeni = _bir_iz(t_iz, _sha8("def tekil_ad(y):\n    return y * 3"))
    kod, sat, govde, _e = _dt_not(motor, kok, "1. `tekil_ad` iki yerde.")
    if "ATIF DAMGALANDI: 1 (tekil_ad#%s [2 tanim])" % yeni not in sat:
        b.append(("DAMGA-TAZE-TEKIL", "tekil -> coklu (yeni dosya): `[2 tanim]` damga beklenir: %r" % sat))
    m_iz = _sha8("    def hesapla(self):\n        return 1")
    ad = _b_proje(motor, taban, "dt_ad", 1, {"src/m.py": "class A:\n    def hesapla(self):\n        return 1\n"})
    _b_commit(ad, {"src/m.py": "class A:\n    def hesapla(self):\n        return 1\n\n\nclass B:\n    def hesapla(self):\n        return 2\n"},
              "baska sinifta ayni uye adi")
    yeni2 = _bir_iz(m_iz, _sha8("    def hesapla(self):\n        return 2"))
    kod, sat, govde, _e = _dt_not(motor, ad, "1. `hesapla` iki sinifta.")
    if "ATIF DAMGALANDI: 1 (hesapla#%s [2 tanim])" % yeni2 not in sat:
        b.append(("DAMGA-TAZE-TEKIL", "ayni dosyada yeni tam ad: `[2 tanim]` damga beklenir: %r" % sat))


def _v_dtaze_yok(motor, taban, b, tarama_bozuk, bozuk):
    """DAMGA-TAZE-YOK: taze kume CIKARILAMAZSA damga BASILMAZ (`ATIF OLCULEMEDI: ad (DEFTER_BAYAT)` + `ATIF NOT` sebep + K3 `OLCULEMEDI`; govde
    DEGISMEZ, exit 0, stderr sizmaz) — bayatlik olcum arizasi (enjeksiyon) · 101 bayat dosya (tavan) · cikarici KUSURU (yeni C# dosya).
    100 bayat dosya (tavan DAHIL) hala damgalanir. ADAYSIZ not: taze kume HIC cikarilmaz (bozuk motorla bile cikti bayt-ayni)."""
    kok, _sha = _dt_taban(motor, taban, "dt_yok")
    kod, sat, govde, e = _dt_not(tarama_bozuk, kok, "1. `ortak_ad` dort yerde.")
    bekle = ["ATIF OLCULEMEDI: ortak_ad (DEFTER_BAYAT)",
             "ATIF NOT: taze aday kumesi cikarilamadi (bayatlik: SystemExit) - eksik kumeden damga/dogusta bayat VERILMEZ; hafiza.py adres --kur",
             "DOGUSTA BAYAT: OLCULEMEDI (DEFTER_BAYAT: taze aday kumesi cikarilamadi)"]
    if kod != 0 or govde != "1. `ortak_ad` dort yerde." or sat != bekle or "HATA:" in e:
        b.append(("DAMGA-TAZE-YOK", "bayatlik olcumu arizali: damga YOK + OLCULEMEDI + ATIF NOT + K3 satiri; govde ayni, stderr sessiz: exit=%s govde=%r satirlar=%r err=%r" % (
            kod, govde, sat, e[-100:])))
    kod, sat, govde, e = _dt_not(tarama_bozuk, kok, "2. duz metin: kod adresi yok.")
    if kod != 0 or sat != []:
        b.append(("DAMGA-TAZE-ADAYSIZ", "ADAYSIZ not: taze kume HIC cikarilmaz (bozuk motorla bile satir YOK): exit=%s satirlar=%r" % (kod, sat)))
    kod, sat, govde, e = _dt_not(tarama_bozuk, kok, "3. `ortak_ad`#00000000 yalniz damgali atif.")      # damgali belirtec ADAY degildir
    if kod != 0 or sat != []:
        b.append(("DAMGA-TAZE-ADAYSIZ", "yalniz DAMGALI belirtec (aday YOK): taze kume cikarilmaz, satir YOK (bayt-bayt eski): exit=%s satirlar=%r" % (kod, sat)))
    # tavan: 100 bayat dosya damgalanir, 101 -> OLCULEMEDI
    e_dos = dict(("src/e%03d.py" % i, "def e%03d_islev():\n    return 0\n" % i) for i in range(101))
    tv = _b_proje(motor, taban, "dt_tavan", 3, e_dos)
    _b_commit(tv, dict(("src/e%03d.py" % i, "def e%03d_islev():\n    return 1\n" % i) for i in range(100)), "100 dosya degisti")
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    kod, sat, govde, _e = _dt_not(motor, tv, "1. `ortak_ad` uc yerde.")
    if "ATIF DAMGALANDI: 1 (ortak_ad#%s [3 tanim])" % b3 not in sat:
        b.append(("DAMGA-TAZE-TAVAN", "100 bayat dosya (tavan DAHIL): taze kumeyle damgalanir: %r" % sat))
    _b_commit(tv, {"src/e100.py": "def e100_islev():\n    return 1\n"}, "101. dosya degisti")
    kod, sat, govde, _e = _dt_not(motor, tv, "2. `ortak_ad` yine.")
    if govde != "2. `ortak_ad` yine." or sat[:1] != ["ATIF OLCULEMEDI: ortak_ad (DEFTER_BAYAT)"] or \
            "ATIF NOT: taze aday kumesi cikarilamadi (bayat: 101 dosya degisti) - eksik kumeden damga/dogusta bayat VERILMEZ; hafiza.py adres --kur" not in sat:
        b.append(("DAMGA-TAZE-TAVAN", "101 bayat dosya (tavan ASILDI): damga YOK + `DEFTER_BAYAT` + sebep beklenir: govde=%r satirlar=%r" % (govde, sat)))
    # cikarici KUSURU: yeni C# dosya + C# cikaricisi arizali motor
    ek = _b_proje(motor, taban, "dt_eksik", 3)
    _b_commit(ek, {"src/Q.cs": "public class Q\n{\n    public int Baska(int x) => x;\n}\n"}, "yeni C# dosya")
    kod, sat, govde, _e = _dt_not(bozuk, ek, "1. `ortak_ad` uc yerde.")
    if govde != "1. `ortak_ad` uc yerde." or sat[:1] != ["ATIF OLCULEMEDI: ortak_ad (DEFTER_BAYAT)"] or \
            "ATIF NOT: taze aday kumesi cikarilamadi (kusur: CIKARICI) - eksik kumeden damga/dogusta bayat VERILMEZ; hafiza.py adres --kur" not in sat:
        b.append(("DAMGA-TAZE-YOK", "yeni dosyanin cikaricisi arizali (kusur): damga YOK + sebep `kusur: CIKARICI`: govde=%r satirlar=%r" % (govde, sat)))


def _v_dtaze_bilinmez(motor, taban, b):
    """DAMGA-TAZE-BILINMEZ: yeni dosya CIKARILAMAZ (sozdizimi hatasi) ve adi iceriyorsa o adin kumesi EKSIK olabilir -> damga YOK
    (`OLCULEMEDI (DEFTER_BAYAT)`, K3 `ortak_ad: DEFTER_BAYAT`); adi ICERMIYORSA damga basilir (+ `ATIF NOT: defter ATLANDI`) — gurultu YOK."""
    k1 = _b_proje(motor, taban, "dt_kotu1", 3)
    _b_commit(k1, {"src/kotu.py": "def ortak_ad(x:\n"}, "yeni dosya bozuk ve ad geciyor")
    kod, sat, govde, _e = _dt_not(motor, k1, "1. `ortak_ad` var.")
    if govde != "1. `ortak_ad` var." or "ATIF OLCULEMEDI: ortak_ad (DEFTER_BAYAT)" not in sat \
            or "DOGUSTA BAYAT: OLCULEMEDI (ortak_ad: DEFTER_BAYAT)" not in sat:
        b.append(("DAMGA-TAZE-BILINMEZ", "bozuk yeni dosya adi iceriyor: damga YOK + `OLCULEMEDI (DEFTER_BAYAT)` (K1 + K3): govde=%r satirlar=%r" % (govde, sat)))
    k2 = _b_proje(motor, taban, "dt_kotu2", 3)
    _b_commit(k2, {"src/kotu.py": "def baska_ad(x:\n"}, "yeni dosya bozuk, ad YOK")
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    kod, sat, govde, _e = _dt_not(motor, k2, "1. `ortak_ad` var.")
    if govde != "1. `ortak_ad`#%s var." % b3 or "ATIF DAMGALANDI: 1 (ortak_ad#%s [3 tanim])" % b3 not in sat:
        b.append(("DAMGA-TAZE-GURULTU", "bozuk yeni dosya adi ICERMIYOR: damga basilir (gurultu yok): govde=%r satirlar=%r" % (govde, sat)))
    # TEK tanimli ad + o tanimin dosyasi bozuldu (taze kumede satiri DUSER: ad `yok`): `COZULEMEDI` DEGIL, `OLCULEMEDI (DEFTER_BAYAT)` (K1 + K3)
    k3 = _b_proje(motor, taban, "dt_kotu3", 1, {"src/t.py": "def tekil_ad(x):\n    return x\n"})
    _b_commit(k3, {"src/t.py": "def tekil_ad(x:\n"}, "tekil tanimin dosyasi bozuldu")
    kod, sat, govde, _e = _dt_not(motor, k3, "1. `tekil_ad` var.")
    if govde != "1. `tekil_ad` var." or "ATIF OLCULEMEDI: tekil_ad (DEFTER_BAYAT)" not in sat or "ATIF COZULEMEDI: tekil_ad" in sat:
        b.append(("DAMGA-TAZE-BILINMEZ", "tekil adin dosyasi bozuk: `OLCULEMEDI (DEFTER_BAYAT)` beklenir (`COZULEMEDI` DEGIL): govde=%r satirlar=%r" % (govde, sat)))
    if "DOGUSTA BAYAT: OLCULEMEDI (tekil_ad: DEFTER_BAYAT)" not in sat:
        b.append(("DAMGA-TAZE-BILINMEZ", "tekil adin dosyasi bozuk: K3 `OLCULEMEDI (tekil_ad: DEFTER_BAYAT)` beklenir: satirlar=%r" % (sat,)))


def _v_dtaze_yazma(motor, taban, b):
    """DAMGA-TAZE-YAZMA: bayat defterde `not` stat onbellegini YAZMAZ (`kapi` ile ayni: `_adres_bugun(yaz=False)`): gecici dizin (SICAK onbellek)
    `not` oncesi/sonrasi bayt-ayni."""
    kok = _b_proje(motor, taban, "dt_yazma", 3)
    kos(motor, kok, "adres", "ortak_ad")                      # onbellegi ISIT (defter guncel)
    _b_commit(kok, {"src/p4.py": _b_py(4)}, "yeni dosya")
    time.sleep(3.3)                                           # yeni dosya RACY paydan yasli: onbellege GIRER
    tmp = onb_dizini(kok)

    def goruntu():
        return sorted((f, hashlib.sha256(open(os.path.join(tmp, f), "rb").read()).hexdigest()) for f in os.listdir(tmp))
    once = goruntu()
    kod, sat, govde, _e = _dt_not(motor, kok, "1. `ortak_ad` dort yerde.", tmp=tmp)
    if goruntu() != once:
        b.append(("DAMGA-TAZE-YAZMA", "bayat defterde `not` stat onbellegini YAZDI (gecici dizin degisti)"))
    if "ATIF DAMGALANDI: 1 (ortak_ad#%s [4 tanim])" % _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)]) not in sat:
        b.append(("DAMGA-TAZE-YAZMA", "SICAK onbellekle de taze kume `[4 tanim]`: %r" % sat))


def kol_damga_taze(motor, taban, bozuk, tarama_bozuk):
    """P5.4 (KALEM 8) — P5-DAMGA kolunun DAMGA-TAZE-* eksenleri: bayat defter + yeni dosya -> `not` taze kumeden `[k+1]` damga, K3 taze kumeyle,
    hemen `kapi` GOVDE DEGISTI 0 (DAMGA-TAZE) · tekil -> coklu / yeni tam ad (DAMGA-TAZE-TEKIL) · taze kume cikarilamaz -> damga YOK +
    OLCULEMEDI (DAMGA-TAZE-YOK) · 100/101 dosya tavani (DAMGA-TAZE-TAVAN) · adaysiz not taze kume cikarmaz (DAMGA-TAZE-ADAYSIZ) · cikarilamayan
    yeni dosya adi iceriyorsa damga YOK, icermiyorsa gurultu yok (DAMGA-TAZE-BILINMEZ / -GURULTU) · `not` onbellegi yazmaz (DAMGA-TAZE-YAZMA)."""
    b = []
    for etiketler, f in (
            (("DAMGA-TAZE",), lambda: _v_dtaze(motor, taban, b)),
            (("DAMGA-TAZE-TEKIL",), lambda: _v_dtaze_tekil(motor, taban, b)),
            (("DAMGA-TAZE-YOK", "DAMGA-TAZE-ADAYSIZ", "DAMGA-TAZE-TAVAN"), lambda: _v_dtaze_yok(motor, taban, b, tarama_bozuk, bozuk)),
            (("DAMGA-TAZE-BILINMEZ", "DAMGA-TAZE-GURULTU"), lambda: _v_dtaze_bilinmez(motor, taban, b)),
            (("DAMGA-TAZE-YAZMA",), lambda: _v_dtaze_yazma(motor, taban, b))):
        if _calissin(*etiketler):
            f()
    return b


def kos_damga(motor, taban, ad, kaynak):
    taze_ekseni = _SADECE[0] is not None and _SADECE[0].startswith("DAMGA-TAZE")
    bozuk = _bozuk_motor(taban, "damga_" + ad, kaynak)
    _BOZUK_ADRES[0] = bozuk
    if kaynak.count(DAMGA_ISTISNA_ANKOR) != 1:
        raise Kurulamadi("damga istisna capasi %d yerde gecti (1 olmali)" % kaynak.count(DAMGA_ISTISNA_ANKOR))
    istisnali, hata = _motor_yaz(kaynak.replace(DAMGA_ISTISNA_ANKOR, DAMGA_ISTISNA_ANKOR + '    raise RuntimeError("bilerek bozuk damga adimi")      # MUTANT\n', 1),
                                 os.path.join(os.path.dirname(taban), "istisna_" + ad), "istisna_" + ad)
    if istisnali is None:
        raise Kurulamadi(hata)
    anc2 = '            return _adres_bugun(kok, ozet, None, '      # ONEK capa: sabotaj son argumani degistirebilir
    if kaynak.count(anc2) != 1:
        raise Kurulamadi("bayatlik olcumu capasi %d yerde gecti (1 olmali)" % kaynak.count(anc2))
    tarama, hata = _motor_yaz(kaynak.replace(anc2, '            oldur("ENJEKSIYON: git ls-files BASARISIZ (bayatlik olcumu arizasi)", 3)\n' + anc2, 1),
                              os.path.join(os.path.dirname(taban), "tarama_dmg_" + ad), "tarama_dmg_" + ad)
    if tarama is None:
        raise Kurulamadi(hata)
    if taze_ekseni:
        return kol_damga_taze(motor, taban, bozuk, tarama)
    return kol_damga(motor, taban, bozuk, istisnali) + kol_damga_taze(motor, taban, bozuk, tarama)


# ------------------------------------------------------------------ P5-H20 (P5 KALEM 2): `kapi` H20 — govde degisti mi (UYARI, exit DEGISMEZ)
# Beklentiler FIKSTURDEN ELLE (izler hashlib'den, motordan DEGIL). Taban durum: iki damgali atif (tekil_islev, kapat_kasa) + bir
# damgasiz cozulebilir belirtec (ikinci_islev): `2 atif | 0 | 0 | 0 | 1 DAMGASIZ`.
H20_A = '''def tekil_islev(x):
    return x + 1


def ikinci_islev(x):
    return x * 2


class Kasa:
    def kapat_kasa(self):
        return 0
'''
H20_DEGISEN = H20_A.replace("def tekil_islev(x):\n    return x + 1\n", "def tekil_islev(x):\n    x = x + 0\n    return x + 1\n")
H20_KAYAN = "# yorum bir\n# yorum iki\n\n" + H20_A
H20_KOMSU = H20_A.replace("return x * 2", "return x * 3")
H20_SILINEN = H20_A.replace("    def kapat_kasa(self):\n        return 0\n", "    pass\n")
H20_IZ = hashlib.sha256("def tekil_islev(x):\n    return x + 1".encode("utf-8")).hexdigest()[:8]
H20_YENI_IZ = hashlib.sha256("def tekil_islev(x):\n    x = x + 0\n    return x + 1".encode("utf-8")).hexdigest()[:8]
H20_KAPAT_IZ = hashlib.sha256("    def kapat_kasa(self):\n        return 0".encode("utf-8")).hexdigest()[:8]
H20_TABAN = "H20: 2 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 1 DAMGASIZ"
H20_ISTISNA_ANKOR = "def _h20_hesapla(kok, y):\n"
H20_TOPLU = "\n".join("def toplu_islev_%02d(x):\n    return x + %d\n" % (i, i) for i in range(22))


def _h20_satirlari_al(o):
    return ["H20:" + l.split("H20:", 1)[1].rstrip() for l in o.split("\n") if "H20:" in l]


def _kapi_diger(o):
    """`kapi` ciktisinin H20 DISINDAki satirlari (kok yolu normallestirilmis)."""
    return [l for l in o.split("\n") if "H20:" not in l]


def _h20_proje(motor, taban, ad):
    """Taban durum: defter YOKKEN damgasiz not + `adres --kur` + damgali not + derle + commit -> (kok, kurulum bulgulari). Kurulum
    adimlari sabotajli motorda beklenen damgayi uretmeyebilir: bu bir BULGUDUR (H20-KURULUM), duzenegin cokmesi DEGIL."""
    b = []
    kok = _hafiza_proje(motor, taban, ad, {"src/a.py": H20_A, "src/Fx.cs": CS_FX})
    kod, o, e = kos(motor, kok, "not", "--konu", "damgasiz-not", "--yeni-konu", "H20 fiksturu: damgasiz belirtec", "--tur", "durum",
                    "--metin", "3. `ikinci_islev` damgasiz.")
    if kod != 0:
        raise Kurulamadi("damgasiz not basarisiz: %r" % (o + e)[-160:])
    kur(motor, kok)
    kod, o, e = kos(motor, kok, *(DAMGA_NOT_ARGS + ("1. `tekil_islev` ilk iddia.\n2. `kapat_kasa` ikinci iddia.",)))
    if kod != 0 or ("ATIF DAMGALANDI: 2 (kapat_kasa#%s, tekil_islev#%s)" % (H20_KAPAT_IZ, H20_IZ)) not in o:
        b.append(("H20-KURULUM", "damgali not beklenen damgalari uretmedi: exit=%s %r" % (kod, o[-200:])))
    kod, o, e = kos(motor, kok, "derle")
    if kod != 0:
        raise Kurulamadi("derle basarisiz: exit=%s %r" % (kod, (o + e)[-200:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "h20")
    return kok, b


def _h20_kapi(motor, kok, *args):
    kod, o, e = kos(motor, kok, "kapi", *args)
    return kod, o.replace(kok, "<KOK>"), e


def _h20_hukum_say(b, etiket, ne, motor, kok, beklenen_satir, exit0, ayrinti=None):
    """Tek durum: H20 ozet satiri BIREBIR `beklenen_satir`, (varsa) ayrinti satiri, exit `exit0` ile ayni (UYARI: exit DEGISMEZ)."""
    kod, o, e = _h20_kapi(motor, kok)
    h20 = _h20_satirlari_al(o)
    if not h20 or h20[0] != beklenen_satir:
        b.append((etiket, "%s: H20 ozeti %r != beklenen %r" % (ne, h20[:1], beklenen_satir)))
    if ayrinti is not None and ayrinti not in h20:
        b.append((etiket, "%s: ayrinti satiri %r yok: %r" % (ne, ayrinti, h20)))
    if exit0 is not None and kod != exit0:
        b.append(("H20-EXIT", "%s: kapi exit=%s (H20 UYARIDIR, exit degismemeli: %s)" % (ne, kod, exit0)))
    return kod, o


def kol_h20(motor, taban, bozuk, istisnali):
    """P5-H20: damgali fikstur sessiz (H20-AYNI) ve damgasiz sayilir (H20-DAMGASIZ) · govdeye satir eklenir -> `GOVDE DEGISTI 1` + ayrinti
    (H20-DEGISTI) · govde ayni, yalniz satir kayar -> 0 (H20-KAYMA) · BASKA sembol degisir -> 0 (H20-KOMSU) · sembol silinir ->
    `SEMBOL YOK 1` (H20-YOK) · `--siki`de de UYARI (H20-SIKI) · defter YOKKEN damgali atif OLCULEMEDI sayilir, gizlenmez (H20-DEFTER)
    · atifsiz/damgasiz proje SESSIZ (H20-SESSIZ) · cikarici kusuru / H20 istisnasi OLCULEMEDI'dir ve diger TUM `kapi` satirlari + exit
    ayni (H20-CIKARICI / H20-ISTISNA)."""
    b = []
    kok, kurulum = _h20_proje(motor, taban, "h20")
    b += kurulum
    yol = os.path.join(kok, "src", "a.py")
    kod0, o0, _e0 = _h20_kapi(motor, kok)
    h20 = _h20_satirlari_al(o0)
    if h20 != [H20_TABAN]:
        b.append(("H20-AYNI", "damgali + degismemis fikstur: H20 satirlari %r != [%r]" % (h20, H20_TABAN)))
        if not any(l.endswith("| 1 DAMGASIZ") for l in h20):
            b.append(("H20-DAMGASIZ", "damgasiz cozulebilir belirtec (ikinci_islev) 1 DAMGASIZ olarak SAYILMADI: %r" % h20))
    siki0 = kos(motor, kok, "kapi", "--siki")[0]
    _yaz(yol, H20_DEGISEN)
    ayr = "H20: md.1 `tekil_islev` #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (H20_IZ, H20_YENI_IZ)
    _h20_hukum_say(b, "H20-DEGISTI", "govdeye satir eklendi", motor, kok,
                   "H20: 2 atif | 1 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 1 DAMGASIZ", kod0, ayr)
    kod_s, o_s, _e = kos(motor, kok, "kapi", "--siki")
    if "1 GOVDE DEGISTI" not in o_s or kod_s != siki0:
        b.append(("H20-SIKI", "`kapi --siki`: exit=%s (taban %s), H20 `1 GOVDE DEGISTI` satiri %s" % (kod_s, siki0, "var" if "1 GOVDE DEGISTI" in o_s else "YOK")))
    _yaz(yol, H20_KAYAN)
    _h20_hukum_say(b, "H20-KAYMA", "govde ayni, satirlar kaydi", motor, kok, H20_TABAN, kod0)
    _yaz(yol, H20_KOMSU)
    _h20_hukum_say(b, "H20-KOMSU", "baska sembol degisti", motor, kok, H20_TABAN, kod0)
    _yaz(yol, H20_SILINEN)
    _h20_hukum_say(b, "H20-YOK", "sembol silindi", motor, kok,
                   "H20: 2 atif | 0 GOVDE DEGISTI | 1 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 1 DAMGASIZ", kod0,
                   "H20: md.2 `kapat_kasa` #%s SEMBOL YOK - IDDIA KODDAN ESKI OLABILIR" % H20_KAPAT_IZ)
    _yaz(yol, H20_A)
    # arizali cikarici (RuntimeError) ve H20'nin KENDI istisnasi: H20 OLCULEMEDI; diger HER satir + exit ayni
    for etiket, m, bekle in (("H20-CIKARICI", bozuk,
                              "H20: 2 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 3 OLCULEMEDI (damgali 2, damgasiz 1) [CIKARICI:3] | 0 COKLU | 0 DAMGASIZ"),
                             ("H20-ISTISNA", istisnali, "H20: OLCULEMEDI (RuntimeError)")):
        kod, o, e = _h20_kapi(m, kok)
        if _h20_satirlari_al(o)[:1] != [bekle]:
            b.append((etiket, "H20 satiri %r != beklenen %r (cikti %r)" % (_h20_satirlari_al(o)[:2], bekle, (o + e)[-160:])))
        if kod != kod0 or _kapi_diger(o) != _kapi_diger(o0) or "Traceback" in e:
            b.append((etiket, "H20 istisnasi `kapi`nin DIGER hukumlerini etkiledi: exit %s -> %s; ilk fark: %r" % (
                kod0, kod, [(x, y) for x, y in zip(_kapi_diger(o0), _kapi_diger(o)) if x != y][:1])))
    # EKSIK defter: damgali atif OLCULEMEDI [DEFTER_EKSIK]; BOZUK defter [DEFTER_BOZUK]
    p = os.path.join(kok, "arsiv", "hafiza", "ADRES.tsv")
    saglam = io.open(p, encoding="utf-8", newline="").read()
    os.remove(p)
    kos(_BOZUK_ADRES[0], kok, "adres", "--kur")
    _h20_hukum_say(b, "H20-EKSIK", "defter EKSIK", motor, kok,
                   "H20: 2 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 2 OLCULEMEDI [DEFTER_EKSIK:2] | 0 COKLU | 0 DAMGASIZ", kod0)
    _yaz(p, "bozuk\n")
    _h20_hukum_say(b, "H20-BOZUK", "defter BOZUK", motor, kok,
                   "H20: 2 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 2 OLCULEMEDI [DEFTER_BOZUK:2] | 0 COKLU | 0 DAMGASIZ", kod0)
    os.remove(p)
    # defter YOK: damgali atif OLCULEMEDI olarak SAYILIR (gizlenmez)
    _h20_hukum_say(b, "H20-DEFTER", "defter YOK", motor, kok,
                   "H20: 2 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 2 OLCULEMEDI [DEFTER_YOK:2] | 0 COKLU | 0 DAMGASIZ", kod0)
    _yaz(p, saglam)
    return b + kol_h20_ayrinti(motor, taban) + kol_h20_sessiz(motor, taban)


def kol_h20_ayrinti(motor, taban):
    """P5-H20 ayrintilari: numarasiz satirdaki damgali atif okunur (H20-SATIR) · damgali `yol:N` govde degisince YAKALANIR, satir
    kayinca AYNI (H20-YOL) · ekran tavani 20, HEPSI sayilir (H20-TAVAN) · kod citi icindeki damgali belirtec sayilmaz (H20-CIT) ·
    defter ATLANDI dosya tasirken kayip sembol SEMBOL YOK degil OLCULEMEDI [DEFTER_ATLANDI] (H20-ATLANDI)."""
    b = []
    sat, _k = _h20_proje(motor, taban, "h20_satir")
    _yaz(os.path.join(sat, "src", "a.py"), H20_A)
    kos(motor, sat, *(DAMGA_NOT_ARGS + ("- `kapat_kasa` numarasiz satir (madde DEGIL).",)))
    kos(motor, sat, "derle")
    _yaz(os.path.join(sat, "src", "a.py"), H20_A.replace("        return 0\n", "        return 7\n"))
    _kod, o, _e = _h20_kapi(motor, sat)
    h20 = _h20_satirlari_al(o)
    yeni = hashlib.sha256("    def kapat_kasa(self):\n        return 7".encode("utf-8")).hexdigest()[:8]
    if not any(l.startswith("H20: satir ") and "`kapat_kasa`" in l and l.endswith(" -> #%s IDDIA KODDAN ESKI OLABILIR" % yeni) for l in h20):
        b.append(("H20-SATIR", "numarasiz satirdaki damgali atif okunmadi: %r" % h20))
    # `yol:N`
    yp = _hafiza_proje(motor, taban, "h20_yol", {"src/a.py": H20_A})
    kur(motor, yp)
    kos(motor, yp, *(DAMGA_NOT_ARGS + ("1. `a.py:2` tekil_islev'in govdesi.",)))
    kos(motor, yp, "derle")
    _git(yp, "add", "-A")
    _git(yp, "commit", "-q", "-m", "yol")
    _yaz(os.path.join(yp, "src", "a.py"), H20_KAYAN)
    kod, o, _e = _h20_kapi(motor, yp)
    if _h20_satirlari_al(o)[:1] != ["H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ"]:
        b.append(("H20-YOL", "damgali `yol:N`, govde ayni + satirlar kaydi: %r" % _h20_satirlari_al(o)[:2]))
    _yaz(os.path.join(yp, "src", "a.py"), H20_DEGISEN)
    kod, o, _e = _h20_kapi(motor, yp)
    if _h20_satirlari_al(o)[:2] != ["H20: 1 atif | 1 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ",
                                    "H20: md.1 `a.py:2` #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (H20_IZ, H20_YENI_IZ)]:
        b.append(("H20-YOL", "damgali `yol:N`, govde degisti: %r" % _h20_satirlari_al(o)[:2]))
    # tavan 20: 22 damgali atif, hepsi degisir
    tp = _hafiza_proje(motor, taban, "h20_tavan", {"src/t.py": H20_TOPLU})
    kur(motor, tp)
    metin = "\n".join("%d. `toplu_islev_%02d` iddia." % (i + 1, i) for i in range(22))
    kos(motor, tp, *(DAMGA_NOT_ARGS + (metin,)))
    kos(motor, tp, "derle")
    _yaz(os.path.join(tp, "src", "t.py"), H20_TOPLU.replace("return x +", "return 9 * x +"))
    kod, o, _e = _h20_kapi(motor, tp)
    h20 = _h20_satirlari_al(o)
    if h20[:1] != ["H20: 22 atif | 22 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ"] or len(h20) != 22 \
            or h20[-1] != "H20: ... +2 daha (ekranda kirpildi, HEPSI sayildi)":
        b.append(("H20-TAVAN", "22 degisen atif: ozet 22 sayilmali, 20 satir + `+2 daha`: ilk=%r uzunluk=%d son=%r" % (h20[:1], len(h20), h20[-1:])))
    # kod citi icindeki damgali belirtec SAYILMAZ
    cp = _hafiza_proje(motor, taban, "h20_cit", {"src/a.py": H20_A})
    kur(motor, cp)
    canli = os.path.join(cp, "PROJE_HAFIZA.md")
    _yaz(canli, io.open(canli, encoding="utf-8", newline="").read() + "\n```\n1. `tekil_islev`#%s cit icinde\n```\n" % H20_IZ)
    _yaz(os.path.join(cp, "src", "a.py"), H20_DEGISEN)
    kod, o, _e = _h20_kapi(motor, cp)
    if _h20_satirlari_al(o):
        b.append(("H20-CIT", "kod citi icindeki damgali belirtec H20'ye GIRDI: %r" % _h20_satirlari_al(o)[:2]))
    # ATLANDI dosya (sozdizimi hatali) varken kayip sembol SEMBOL YOK DEGIL OLCULEMEDI
    ap = _hafiza_proje(motor, taban, "h20_atlandi", {"src/a.py": H20_A, "src/kotu.py": "def (:\n"})
    kur(motor, ap)
    kos(motor, ap, *(DAMGA_NOT_ARGS + ("1. `kapat_kasa` iddia.",)))
    kos(motor, ap, "derle")
    _yaz(os.path.join(ap, "src", "a.py"), H20_SILINEN)
    kod, o, _e = _h20_kapi(motor, ap)
    if _h20_satirlari_al(o)[:1] != ["H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_ATLANDI:1] | 0 COKLU | 0 DAMGASIZ"]:
        b.append(("H20-ATLANDI", "defter ATLANDI tasirken sembol YOK hukmu verildi: %r" % _h20_satirlari_al(o)[:2]))
    return b


def kol_h20_sessiz(motor, taban):
    """Atifsiz ya da damgasiz projelerde H20 SESSIZDIR (H20-SESSIZ): hic belirtec yok · belirtec var (canlida, `derle` ile) ama defter
    yok ve damga yok."""
    b = []
    bos = _hafiza_proje(motor, taban, "h20_bos", {"src/a.py": H20_A})
    _kod, o, _e = kos(motor, bos, "kapi")
    ikinci = _hafiza_proje(motor, taban, "h20_defter_yok", {"src/a.py": H20_A})
    kos(motor, ikinci, "not", "--konu", "genel-durum", "--tur", "durum", "--metin", "1. `tekil_islev` damgasiz ve defter yok.")
    kod, o_d, _e = kos(motor, ikinci, "derle")
    canli = io.open(os.path.join(ikinci, "PROJE_HAFIZA.md"), encoding="utf-8", newline="").read()
    if "`tekil_islev` damgasiz ve defter yok" not in canli:
        raise Kurulamadi("H20-SESSIZ duzenegi: belirtec canliya girmedi (derle exit=%s)" % kod)
    _kod2, o2, _e2 = kos(motor, ikinci, "kapi")
    if "H20" in o or "H20" in o2:
        b.append(("H20-SESSIZ", "atifsiz / damgasiz-defterisiz projede H20 satiri basildi: %r %r" % (_h20_satirlari_al(o), _h20_satirlari_al(o2))))
    return b



def kos_h20(motor, taban, ad, kaynak):
    bozuk, hata = _bozuk_motor_yaz(kaynak, os.path.join(os.path.dirname(taban), "h20_bozuk_" + ad), "h20_bozuk_" + ad)
    if bozuk is None:
        raise Kurulamadi(hata)
    _BOZUK_ADRES[0] = _bozuk_motor(taban, "h20_tablo_" + ad, kaynak)       # EKSIK defter kurmak icin (C# tablosu patlar)
    if kaynak.count(H20_ISTISNA_ANKOR) != 1:
        raise Kurulamadi("h20 istisna capasi %d yerde gecti (1 olmali)" % kaynak.count(H20_ISTISNA_ANKOR))
    istisnali, hata = _motor_yaz(kaynak.replace(H20_ISTISNA_ANKOR, H20_ISTISNA_ANKOR + '    raise RuntimeError("bilerek bozuk H20")      # MUTANT\n', 1),
                                 os.path.join(os.path.dirname(taban), "h20_istisna_" + ad), "h20_istisna_" + ad)
    if istisnali is None:
        raise Kurulamadi(hata)
    return kol_h20(motor, taban, bozuk, istisnali)


# ------------------------------------------------------------------ P5-DOGUS (P5 KALEM 3): `not` aninda DOGUSTA BAYAT uyarisi
# Fikstur: a.py V0 (c1) -> V1 (c2: `hedef_islev` govdesi DEGISIR) -> `sonra` ilgisiz commit (yalniz notlar.txt). Degisikligi
# getiren commit HEAD'den `sonra` commit once. Beklentiler ELLE: k = `sonra`; sha `git rev-parse`tan (motordan DEGIL).
# N=5: son 5 commit (HEAD..HEAD~4) icinde GETIRILEN degisiklik uyarilir -> sonra 0..4 uyari VAR, 5 ve 6 YOK.
DOGUS_V0 = "def hedef_islev(x):\n    return x + 1\n\n\ndef diger(y):\n    return y\n"
DOGUS_V1 = DOGUS_V0.replace("return x + 1", "return x + 2")
DOGUS_V2 = DOGUS_V0.replace("return x + 1", "return x + 3")
DOGUS_METIN = "1. `hedef_islev` dogru calisir."
DOGUS_ISTISNA_ANKOR = "def _dogus_hepsi(kok, semboller, onbellek):\n"


def _git_t(kok, tarih, *args):
    """`_git` + KONTROLLU yazar/islemci tarihi (commit sirasi tarihe bagli sinamalar icin)."""
    ortam = _cikti_kodlamasi_ortami()
    ortam.update(GIT_AUTHOR_DATE=tarih, GIT_COMMITTER_DATE=tarih)
    return subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"] + list(args), capture_output=True, env=ortam)


def _dogus_commit(kok, yol, metin, mesaj):
    _yaz(os.path.join(kok, *yol.split("/")), metin)
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", mesaj)
    return _git(kok, "rev-parse", "HEAD").stdout.decode("ascii").strip()


def _dogus_ilgisiz(kok, n, yol="notlar.txt", baslangic=0):
    """`n` ilgisiz commit (yalniz `yol`: icerik HER commit'te FARKLI olmali yoksa commit olusmaz)."""
    for i in range(n):
        _dogus_commit(kok, yol, "%d\n" % (baslangic + i + 1), "ilgisiz %d" % (baslangic + i + 1))


def _dogus_proje(motor, taban, ad, sonra, on="", dizin=None):
    """-> (kok, degisikligi getiren commit'in sha'si). `kur` + `adres --kur` yapilmis; calisma agaci TEMIZ. `dizin`: proje git
    deposunun ALT dizini ise (`app`)."""
    on_ek = (dizin + "/") if dizin else ""
    dosyalar = {on_ek + "src/a.py": DOGUS_V0, on_ek + "notlar.txt": "0\n"}
    repo = proje(taban, ad, dosyalar)
    kok = os.path.join(repo, dizin) if dizin else repo
    kod, o, e = kos(motor, kok, "kur", "--ad", "ADR")
    if kod != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (kod, (o + e).strip()[-160:]))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "hafiza")
    degisen = _dogus_commit(repo, on_ek + "src/a.py", DOGUS_V1, "govde degisti")
    _dogus_ilgisiz(repo, sonra, on_ek + "notlar.txt")
    kur(motor, kok)                      # ADRES.tsv izlenmeyen dosya olarak kalir (commit YOK: degisiklik `sonra` commit once kalsin)
    return kok, degisen


def _dogus_not(motor, kok, metin=DOGUS_METIN):
    kod, o, e, govde, _ad = _not_kos(motor, kok, metin)
    return kod, o, e, [l for l in o.split("\n") if l.startswith(("DIKKAT:", "DOGUSTA BAYAT:"))], govde


def _dogus_beklenen(k, sha):
    ne = "son commit'te degisti" if k == 0 else "%d commit once degisti" % k
    return "DIKKAT: hedef_islev govdesi %s (%s) - iddiayi kodla teyit et" % (ne, sha[:7])


def kol_dogus(motor, taban, istisnali):
    """P5-DOGUS: degisiklik k commit once (k=0..4) -> `k commit once degisti (<sha>)` (DOGUS-VAR) · N sinirinin DISINDA (5, 6) ->
    uyari YOK (DOGUS-SINIR) · en yakin degisim (DOGUS-YAKIN) · first-parent (DOGUS-MERGE) · alt dizin projesi (DOGUS-ALTDIZIN) ·
    calisma agaci HEAD'den farkli -> `commit'lenmemis degisiklik` (DOGUS-COMMITSIZ) · calisma agaci cikarilamazsa hukum VERILMEZ
    (DOGUS-CALISMA) · git yok / depo degil -> OLCULEMEDI (DOGUS-GITSIZ) · sig gecmis -> OLCULEMEDI (DOGUS-SIG) · 20 dosya tavani
    BEYAN edilir (DOGUS-TAVAN) · bu adimin istisnasi `not`u ve damgayi DUSURMEZ (DOGUS-ISTISNA) · `not` exit'i hep 0 (DOGUS-EXIT)."""
    b = []
    kok6 = None
    for sonra in (0, 2, 4, 5, 6):
        kok, degisen = _dogus_proje(motor, taban, "dogus%d" % sonra, sonra)
        kod, o, e, satirlar, govde = _dogus_not(motor, kok)
        if kod != 0:
            b.append(("DOGUS-EXIT", "sonra=%d: `not` exit=%s (0 beklenir)" % (sonra, kod)))
        if sonra <= 4:
            if satirlar != [_dogus_beklenen(sonra, degisen)]:
                b.append(("DOGUS-VAR", "degisiklik %d commit once: satirlar %r != [%r]" % (sonra, satirlar, _dogus_beklenen(sonra, degisen))))
        elif satirlar:
            b.append(("DOGUS-SINIR", "degisiklik %d commit once (N=5 DISI): uyari BASILDI: %r" % (sonra, satirlar)))
        if sonra == 6:
            kok6 = kok
    # en yakin degisim: V0 -> c2 (V1) -> 1 ilgisiz -> c4 (V2) -> 1 ilgisiz: degisim k=1 (c4) ve k=3 (c2): YALNIZ en yakini
    yk = proje(taban, "dogus_yakin", {"src/a.py": DOGUS_V0, "notlar.txt": "0\n"})
    kos(motor, yk, "kur", "--ad", "ADR")
    _git(yk, "add", "-A")
    _git(yk, "commit", "-q", "-m", "hafiza")
    _dogus_commit(yk, "src/a.py", DOGUS_V1, "c2")
    _dogus_ilgisiz(yk, 1)
    c4 = _dogus_commit(yk, "src/a.py", DOGUS_V2, "c4")
    _dogus_ilgisiz(yk, 1, baslangic=10)
    kur(motor, yk)
    kod, o, e, satirlar, govde = _dogus_not(motor, yk)
    if satirlar != [_dogus_beklenen(1, c4)]:
        b.append(("DOGUS-YAKIN", "iki degisim (k=1, k=3): yalniz EN YAKIN (k=1, %s) beklenir: %r" % (c4[:7], satirlar)))
    # first-parent: degisiklik bir birlestirme (merge) commit'iyle gelir; `k` ana hattin (first-parent) mesafesidir. Tarihler KONTROLLU:
    # ana hattaki ilgisiz commit ozellik commit'inden ESKI -> tarih sirasi first-parent'tan FARKLI cikar (first-parent kapaliysa k/sha kayar)
    mg = proje(taban, "dogus_merge", {"src/a.py": DOGUS_V0, "notlar.txt": "0\n"})
    kos(motor, mg, "kur", "--ad", "ADR")
    _git(mg, "add", "-A")
    _git_t(mg, "2026-01-01T10:00:00+0000", "commit", "-q", "-m", "hafiza")
    ana = _git(mg, "rev-parse", "--abbrev-ref", "HEAD").stdout.decode("ascii").strip()
    _git(mg, "checkout", "-q", "-b", "ozellik")
    _git(mg, "checkout", "-q", ana)
    _yaz(os.path.join(mg, "notlar.txt"), "ana\n")
    _git(mg, "add", "-A")
    _git_t(mg, "2026-01-01T10:01:00+0000", "commit", "-q", "-m", "ana hatta ilgisiz")
    _git(mg, "checkout", "-q", "ozellik")
    _yaz(os.path.join(mg, "src", "a.py"), DOGUS_V1)
    _git(mg, "add", "-A")
    _git_t(mg, "2026-01-01T10:02:00+0000", "commit", "-q", "-m", "ozellik: govde")
    _git(mg, "checkout", "-q", ana)
    _git_t(mg, "2026-01-01T10:03:00+0000", "merge", "-q", "--no-ff", "-m", "birlestir", "ozellik")
    m_sha = _git(mg, "rev-parse", "HEAD").stdout.decode("ascii").strip()
    for i in range(2):
        _yaz(os.path.join(mg, "notlar.txt"), "son %d\n" % i)
        _git(mg, "add", "-A")
        _git_t(mg, "2026-01-01T10:0%d:00+0000" % (4 + i), "commit", "-q", "-m", "ilgisiz %d" % i)
    kur(motor, mg)
    kod, o, e, satirlar, govde = _dogus_not(motor, mg)
    if satirlar != [_dogus_beklenen(2, m_sha)]:
        b.append(("DOGUS-MERGE", "birlestirme commit'iyle gelen degisim (first-parent k=2, %s) beklenir: %r" % (m_sha[:7], satirlar)))
    # alt dizin projesi: kok git deposunun `app/` dizini
    alt, alt_sha = _dogus_proje(motor, taban, "dogus_alt", 2, dizin="app")
    kod, o, e, satirlar, govde = _dogus_not(motor, alt)
    if satirlar != [_dogus_beklenen(2, alt_sha)]:
        b.append(("DOGUS-ALTDIZIN", "git deposunun ALT dizini projesi: satirlar %r != [%r]" % (satirlar, _dogus_beklenen(2, alt_sha))))
    # calisma agaci HEAD'den farkli
    _yaz(os.path.join(kok6, "src", "a.py"), DOGUS_V1.replace("return x + 2", "return x + 3"))
    kod, o, e, satirlar, govde = _dogus_not(motor, kok6)
    if satirlar != ["DIKKAT: hedef_islev commit'lenmemis degisiklik tasiyor"]:
        b.append(("DOGUS-COMMITSIZ", "calisma agacinda commit'siz govde degisikligi: satirlar %r" % satirlar))
    # calisma agaci cikarilamiyor (sozdizimi hatasi): P5.4'ten beri taze kume bu dosyanin satirlarini DUSURUR (`--kur` gibi): K1
    # `COZULEMEDI`, K3 SESSIZ (eksik/olmayan kumeden `commit'lenmemis` hukmu VERILMEZ; `_dogus_calisma` OLCULEMEDI dali yaris savunmasi)
    _yaz(os.path.join(kok6, "src", "a.py"), "def (:\n")
    kod, o, e, satirlar, govde = _dogus_not(motor, kok6)
    if satirlar != [] or kod != 0 or "ATIF COZULEMEDI: hedef_islev" not in o.split("\n"):
        b.append(("DOGUS-CALISMA", "calisma agaci cikarilamiyorken: K1 `COZULEMEDI`, K3 sessiz beklenir: exit=%s satirlar %r cikti=%r" % (kod, satirlar, o[-160:])))
    _yaz(os.path.join(kok6, "src", "a.py"), DOGUS_V1)
    # 20 dosya tavani: 21 dosya, hepsi sorulamaz -> beyan
    tv = proje(taban, "dogus_tavan", dict(("src/f%02d.py" % i, "def tavan_islev_%02d(x):\n    return x\n" % i) for i in range(21)))
    kos(motor, tv, "kur", "--ad", "ADR")
    _git(tv, "add", "-A")
    _git(tv, "commit", "-q", "-m", "hafiza")
    kur(motor, tv)
    metin = "\n".join("%d. `tavan_islev_%02d` iddia." % (i + 1, i) for i in range(21))
    kod, o, e, satirlar, govde = _dogus_not(motor, tv, metin)
    if satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (21 dosya: git gecmisi yalniz en cok 20 dosya icin soruldu; hukumsuz: tavan_islev_20)"]:
        b.append(("DOGUS-TAVAN", "21 dosyalik not: tavan BEYAN edilmeli: satirlar %r" % satirlar))
    # git'siz proje (dosya sistemi kipi): OLCULEMEDI
    gitsiz = os.path.join(taban, "dogus_gitsiz")
    _yaz(os.path.join(gitsiz, "src", "a.py"), DOGUS_V1)
    kod, o, e = kos(motor, gitsiz, "kur", "--ad", "ADR")
    if kod != 0:
        raise Kurulamadi("git'siz kur basarisiz: exit=%s %r" % (kod, (o + e)[-160:]))
    kur(motor, gitsiz)
    kod, o, e, satirlar, govde = _dogus_not(motor, gitsiz)
    if kod != 0 or satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (git deposu degil)"]:
        b.append(("DOGUS-GITSIZ", "git'siz proje: exit=%s satirlar %r" % (kod, satirlar)))
    # sig gecmis: 7 commit'lik depodan --depth 2 klon
    sig = os.path.join(taban, "dogus_sig")
    url = "file://" + ("" if kok6.startswith("/") else "/") + kok6.replace("\\", "/")
    r = subprocess.run(["git", "clone", "-q", "--depth", "2", url, sig], capture_output=True, env=_cikti_kodlamasi_ortami())
    if r.returncode != 0:
        raise Kurulamadi("sig klon basarisiz: %r" % r.stderr[-160:])
    kur(motor, sig)
    kod, o, e, satirlar, govde = _dogus_not(motor, sig)
    if kod != 0 or satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (sig gecmis: 2 commit)"]:
        b.append(("DOGUS-SIG", "sig klon: exit=%s satirlar %r" % (kod, satirlar)))
    # bu adimin istisnasi: not exit 0 + damga YERINDE + OLCULEMEDI
    kok, degisen = _dogus_proje(motor, taban, "dogus_istisna", 1)
    kod, o, e, satirlar, govde = _dogus_not(istisnali, kok)
    iz = hashlib.sha256("def hedef_islev(x):\n    return x + 2".encode("utf-8")).hexdigest()[:8]
    if (kod != 0 or satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (RuntimeError)"] or govde != "1. `hedef_islev`#%s dogru calisir." % iz
            or "Traceback" in (o + e)):
        b.append(("DOGUS-ISTISNA", "dogusta bayat istisnasi: exit=%s satirlar=%r govde=%r (exit 0 + damga yerinde + OLCULEMEDI beklenir)" % (
            kod, satirlar, govde)))
    return b


def kos_dogus(motor, taban, ad, kaynak):
    if kaynak.count(DOGUS_ISTISNA_ANKOR) != 1:
        raise Kurulamadi("dogus istisna capasi %d yerde gecti (1 olmali)" % kaynak.count(DOGUS_ISTISNA_ANKOR))
    istisnali, hata = _motor_yaz(kaynak.replace(DOGUS_ISTISNA_ANKOR, DOGUS_ISTISNA_ANKOR + '    raise RuntimeError("bilerek bozuk dogusta bayat")      # MUTANT\n', 1),
                                 os.path.join(os.path.dirname(taban), "dogus_istisna_" + ad), "dogus_istisna_" + ad)
    if istisnali is None:
        raise Kurulamadi(hata)
    return kol_dogus(motor, taban, istisnali)


# ------------------------------------------------------------------ P5-BIRLESIK (P5.2 KALEM 4): ad 2-5 tanima cozulunce BIRLESIK damga
# Beklentiler FIKSTURDEN ELLE (izler hashlib'den; `_bir_iz` is emrinin tanimi: sha256("\n".join(sorted(izler)))[:8], yol GIRMEZ).
# `ortak_ad` n. dosyada `return x + n` govdesiyle tanimli (src/p<n>.py). Tekil ad = K1 izi (defterdeki iz) ile BAYT-AYNI.
# Sabotaj kosularinda YALNIZ sabotajin KENDI ekseninin vektorleri kosulur (`_SADECE`); temiz kosuda hepsi.
BIRLESIK_TABAN3 = "H20: 3 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ"
BIRLESIK_TABAN1 = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ"
BIRLESIK_DEGISTI1 = "H20: 1 atif | 1 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ"
_SADECE = [None]


def _calissin(*etiketler):
    """Sabotaj kosusunda yalniz sabotajin ekseni (`_SADECE[0]`); temiz kosuda (None) hepsi."""
    return _SADECE[0] is None or _SADECE[0] in etiketler


def _b_py(n):
    return "def ortak_ad(x):\n    return x + %d\n" % n


def _b_iz(n):
    return _sha8("def ortak_ad(x):\n    return x + %d" % n)


def _b_proje(motor, taban, ad, n, ek=None):
    """`ortak_ad`: src/p1.py .. src/p<n>.py (+ `ek` dosyalar + notlar.txt) -> `kur` + commit + adres defteri (izlenmeyen)."""
    dosyalar = dict(("src/p%d.py" % i, _b_py(i)) for i in range(1, n + 1))
    dosyalar["notlar.txt"] = "0\n"
    dosyalar.update(ek or {})
    kok = _hafiza_proje(motor, taban, ad, dosyalar)
    kur(motor, kok)
    return kok


def _b_commit(kok, dosyalar, mesaj):
    for y, m in dosyalar.items():
        _yaz(os.path.join(kok, *y.split("/")), m)
    _git(kok, "add", "-A")
    if _git(kok, "commit", "-q", "-m", mesaj).returncode != 0:
        raise Kurulamadi("commit basarisiz: %s" % mesaj)
    return _git(kok, "rev-parse", "HEAD").stdout.decode("ascii").strip()


def _b_derle(motor, kok):
    kod, o, e = kos(motor, kok, "derle")
    if kod != 0:
        raise Kurulamadi("derle basarisiz: exit=%s %r" % (kod, (o + e)[-160:]))
    _git(kok, "add", "-A")
    if _git(kok, "commit", "-q", "-m", "b").returncode != 0:
        raise Kurulamadi("derle sonrasi commit basarisiz")


def _b_damgali(motor, taban, ad, n, metin="1. `ortak_ad` uc yerde.", ek=None):
    """`n` tanimli proje + damgali `not` + derle + commit -> kok."""
    kok = _b_proje(motor, taban, ad, n, ek)
    kos(motor, kok, *(DAMGA_NOT_ARGS + (metin,)))
    _b_derle(motor, kok)
    return kok


def _b_dogus_proje(motor, taban, ad, n=3, dosyalar=None):
    """`kur` + commit yapilmis proje (adres defteri YOK: vektor `kur`u kendisi cagirir)."""
    d = dict(dosyalar) if dosyalar is not None else dict(("src/p%d.py" % i, _b_py(i)) for i in range(1, n + 1))
    d["notlar.txt"] = "0\n"
    return _hafiza_proje(motor, taban, ad, d)


def _v_var(motor, taban, b):
    """BIRLESIK-VAR / BIRLESIK-TEKIL: 3 dosyada ayni ad -> TEK birlesik damga + `[3 tanim]`; yol:N damgasi ayri; tekil ad K1 izi."""
    b3, t_iz = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _sha8("def tekil_ad(x):\n    return x")
    kok = _b_proje(motor, taban, "bir_var", 3, {"src/t.py": "def tekil_ad(x):\n    return x\n"})
    metin = "1. `ortak_ad` uc yerde.\n2. `tekil_ad` tek yerde.\n3. `p1.py:2` birinci."
    kod, o, e, govde, _ad = _not_kos(motor, kok, metin)
    beklenen = "1. `ortak_ad`#%s uc yerde.\n2. `tekil_ad`#%s tek yerde.\n3. `p1.py:2`#%s birinci." % (b3, t_iz, _b_iz(1))
    satir = "ATIF DAMGALANDI: 3 (ortak_ad#%s [3 tanim], p1.py:2#%s, tekil_ad#%s)" % (b3, _b_iz(1), t_iz)
    if kod != 0 or govde != beklenen or satir not in o.split("\n") or "ATIF COKLU" in o or "ATIF NOT" in o:
        b.append(("BIRLESIK-VAR", "3 dosyada ayni ad: TEK birlesik damga `#%s` + `[3 tanim]` beklenir: exit=%s govde=%r cikti=%r" % (
            b3, kod, govde, o[-240:])))
    if iz(kok, "src/t.py", "tekil_ad") != t_iz or "`tekil_ad`#%s" % t_iz not in (govde or ""):
        b.append(("BIRLESIK-TEKIL", "tekil adin damgasi defterdeki izle (K1) bayt-ayni olmali (beklenen %s): govde=%r" % (t_iz, govde)))
    _b_derle(motor, kok)
    _h20_hukum_say(b, "BIRLESIK-VAR", "birlesik damgali taban", motor, kok, BIRLESIK_TABAN3, None)


def _v_degisti(motor, taban, b):
    """BIRLESIK-DEGISTI: tanimlardan SONUNCUSU (ilkine bakan sabotaj kacirir) degisince H20 `GOVDE DEGISTI 1` + `[3 tanim] #eski -> #yeni`."""
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    kok = _b_damgali(motor, taban, "bir_degisti", 3)
    kod0, _o = _h20_hukum_say(b, "BIRLESIK-DEGISTI", "taban", motor, kok, BIRLESIK_TABAN1, None)
    _yaz(os.path.join(kok, "src", "p3.py"), _b_py(30))
    _h20_hukum_say(b, "BIRLESIK-DEGISTI", "3. tanimin govdesi degisti", motor, kok, BIRLESIK_DEGISTI1, kod0,
                   "H20: md.1 `ortak_ad` [3 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(_b_iz(1), _b_iz(2), _b_iz(30))))


def _v_eklendi(motor, taban, b):
    """BIRLESIK-EKLENDI: ayni dosyada ek tanim (asiri yuk) BAYAT defterle de yakalanir; YENI dosyada eklenen tanim da (P5.3: H20 bayat defterde
    degisen/yeni dosyalari bellekte yeniden cikarir; ayrintisi BIRLESIK-TAZE vektorlerinde); iki tanim silinince `[2 tanim]`."""
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    ek = _b_damgali(motor, taban, "bir_ekle", 3)
    kod1, _o = _h20_hukum_say(b, "BIRLESIK-EKLENDI", "taban", motor, ek, BIRLESIK_TABAN1, None)
    p2 = os.path.join(ek, "src", "p2.py")
    _yaz(p2, _b_py(2) + "\n\n" + _b_py(40))                   # ayni dosyada ikinci tanim (defter BAYAT: kur YOK)
    _h20_hukum_say(b, "BIRLESIK-EKLENDI", "ayni dosyada ek tanim (bayat defter)", motor, ek, BIRLESIK_DEGISTI1, kod1,
                   "H20: md.1 `ortak_ad` [4 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(_b_iz(1), _b_iz(2), _b_iz(40), _b_iz(3))))
    _yaz(p2, _b_py(2))
    _yaz(os.path.join(ek, "src", "p4.py"), _b_py(4))          # IZLENMEYEN yeni dosya: `adres` evreninde (git ls-files) YOK, H20 de gormez
    _h20_hukum_say(b, "BIRLESIK-EKLENDI", "izlenmeyen yeni dosyada tanim (git add YOK): `adres` evrenine girmez", motor, ek, BIRLESIK_TABAN1, kod1)
    _git(ek, "add", "-A")                                     # izleniyor, defter bayat (P5.3: H20 bellekte taze aday kumesi cikarir)
    _h20_hukum_say(b, "BIRLESIK-EKLENDI", "yeni dosyada tanim izleniyor, defter bayat (P5.3: gorunur)", motor, ek, BIRLESIK_DEGISTI1, kod1,
                   "H20: md.1 `ortak_ad` [4 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])))
    kur(motor, ek)
    _h20_hukum_say(b, "BIRLESIK-EKLENDI", "yeni dosyada tanim, defter yenilendi", motor, ek, BIRLESIK_DEGISTI1, kod1,
                   "H20: md.1 `ortak_ad` [4 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])))
    _git(ek, "rm", "-q", "-f", "src/p3.py", "src/p4.py")
    kur(motor, ek)
    _h20_hukum_say(b, "BIRLESIK-EKLENDI", "iki tanim silindi, defter yenilendi", motor, ek, BIRLESIK_DEGISTI1, kod1,
                   "H20: md.1 `ortak_ad` [2 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(_b_iz(1), _b_iz(2))))


def _v_yol(motor, taban, b):
    """BIRLESIK-YOL: dosya yeniden adlandirilinca (defter yenilendi) iz DEGISMEZ: yol izde YOK, `sorted` hash sirasini sabitler."""
    yl = _b_damgali(motor, taban, "bir_yol", 3)
    _git(yl, "mv", "src/p1.py", "src/z1.py")
    kur(motor, yl)
    _h20_hukum_say(b, "BIRLESIK-YOL", "dosya yeniden adlandirildi (govde ayni, defter yenilendi)", motor, yl, BIRLESIK_TABAN1, None)


def _v_bayat(motor, taban, b):
    """BIRLESIK-BAYAT: adaylardan BIR KISMI canli cikarimda yoksa (tasinmis dosya, defter BAYAT) K1/K3 kismi kumeden iz/hukum vermez:
    K1 damga YOK (`OLCULEMEDI (DEFTER_BAYAT)`), K3 `OLCULEMEDI (<ad>: DEFTER_BAYAT)`. H20 (P5.3) taze aday kumesini bellekte cikarir:
    govde ayni -> `ayni` (BIRLESIK-TAZE ailesi)."""
    ba = _b_damgali(motor, taban, "bir_bayat", 3)
    _git(ba, "mv", "src/p1.py", "src/z1.py")                  # defter YENILENMEDI
    _h20_hukum_say(b, "BIRLESIK-BAYAT", "aday dosya tasindi, defter bayat (P5.3: H20 govde AYNI: `ayni`, OLCULEMEDI DEGIL)", motor, ba,
                   BIRLESIK_TABAN1, None)
    kod, o, e, govde, _ad = _not_kos(motor, ba, "1. `ortak_ad` yine.")
    sat = o.split("\n")
    b3_ = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    if kod != 0 or govde != "1. `ortak_ad`#%s yine." % b3_ or "ATIF DAMGALANDI: 1 (ortak_ad#%s [3 tanim])" % b3_ not in sat \
            or "DIKKAT: ortak_ad commit'lenmemis degisiklik tasiyor" not in sat:
        b.append(("BIRLESIK-BAYAT", "bayat defter + tasinmis aday (P5.4: K1/K3 taze kume): `[3 tanim]` damga + `commit'lenmemis` beklenir: exit=%s govde=%r cikti=%r" % (
            kod, govde, (o[-260:]))))
    # tasima COMMIT'LENDI (defter hala bayat): K3 TAZE kumeyle `son commit'te degisti` der (tasinan dosya "yeni dosya" gibi gorunur: bilinen sinir 6)
    c_t = _b_commit(ba, {}, "z1 tasindi")
    satirlar = _dogus_not(motor, ba, "2. `ortak_ad` yine.")[3]
    if satirlar != ["DIKKAT: ortak_ad 3 tanimdan 1'i son commit'te degisti (%s) - iddiayi kodla teyit et" % c_t[:7]]:
        b.append(("BIRLESIK-BAYAT", "commit'li tasima + bayat defter (P5.4: K3 taze kume): `3 tanimdan 1'i son commit'te degisti` beklenir: satirlar %r" % satirlar))
    # P5.4: defter GUNCEL (ozet esit: tazeleme YOK) ama bir aday satirin TAM adi canli cikarimda YOK (eski motor cikarimi / elle duzenleme):
    # KISMI aday kaybi (`_ad_cozum`) -> K1 damga YOK `OLCULEMEDI (DEFTER_BAYAT)`, K3 `OLCULEMEDI`, H20 `[DEFTER_BAYAT]`
    sk = _b_damgali(motor, taban, "bir_bayat_kayma", 3)
    _defter_tam_degistir(sk, "src/p1.py", "ortak_ad", "Zz.ortak_ad")
    _h20_hukum_say(b, "BIRLESIK-BAYAT", "defter GUNCEL ama aday satir canli cikarimda YOK: kismi kume", motor, sk,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYAT:1] | 0 COKLU | 0 DAMGASIZ", None)
    kod, o, e, govde, _ad = _not_kos(motor, sk, "2. `ortak_ad` yine.")
    sat = o.split("\n")
    if kod != 0 or govde != "2. `ortak_ad` yine." or "ATIF OLCULEMEDI: ortak_ad (DEFTER_BAYAT)" not in sat \
            or "DOGUSTA BAYAT: OLCULEMEDI (ortak_ad: DEFTER_BAYAT)" not in sat:
        b.append(("BIRLESIK-BAYAT", "defter GUNCEL ama aday satir canli cikarimda YOK: damga YOK + `OLCULEMEDI (DEFTER_BAYAT)` (K1 ve K3): exit=%s govde=%r cikti=%r" % (
            kod, govde, o[-240:])))


def _v_tavan(motor, taban, b):
    """BIRLESIK-TAVAN / BIRLESIK-COKLU: tavan korumalari AYRI AYRI sinanir (defter satiri / canli iz / HEAD): 5 tanim damgali (tavan DAHIL) ·
    defter 6 + canli 5 (H20 ve K1) · defter 5 + canli 6 (H20, K1, K3) · 6 tanimla baslarsa damga YOK + COKLU sayimi + K3 beyani."""
    b5 = _bir_iz(*[_b_iz(i) for i in range(1, 6)])
    t = _b_proje(motor, taban, "bir_tavan5", 5)
    kod, o, e, govde, _ad = _not_kos(motor, t, "1. `ortak_ad` bes yerde.")
    if kod != 0 or govde != "1. `ortak_ad`#%s bes yerde." % b5 or "ATIF DAMGALANDI: 1 (ortak_ad#%s [5 tanim])" % b5 not in o.split("\n"):
        b.append(("BIRLESIK-TAVAN", "5 tanim (tavan DAHIL) damgalanmali: govde=%r cikti=%r" % (govde, o[-200:])))
    _b_derle(motor, t)
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "tam 5 tanim H20 AYNI (tavan DAHIL)", motor, t, BIRLESIK_TABAN1, None)
    _yaz(os.path.join(t, "src", "p5.py"), _b_py(50))
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "tam 5 tanim, biri degisti", motor, t, BIRLESIK_DEGISTI1, None,
                   "H20: md.1 `ortak_ad` [5 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
                       b5, _bir_iz(*([_b_iz(i) for i in (1, 2, 3, 4)] + [_b_iz(50)]))))
    _yaz(os.path.join(t, "src", "p5.py"), _b_py(5))
    # (a) defter 6 satir, canli 5, defter BAYAT: P5.3 H20 taze kumeyi (5) cikarir -> tavan DEGIL, `ayni`; K1 hala defter satirini sayar (d)
    _yaz(os.path.join(t, "src", "p6.py"), _b_py(6))
    _git(t, "add", "-A")
    kur(motor, t)
    os.remove(os.path.join(t, "src", "p6.py"))
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "defter 6 satir / canli 5 tanim, defter bayat: taze kume 5", motor, t, BIRLESIK_TABAN1, None)
    # (d) K1 ayni durum (P5.4): defter 6 satir, canli 5, defter BAYAT -> taze kume 5: `[5 tanim]` damga (defter satiri tavani DEGIL)
    kod, o, e, govde, _ad = _not_kos(motor, t, "2. `ortak_ad` yine.")
    if "ATIF DAMGALANDI: 1 (ortak_ad#%s [5 tanim])" % b5 not in o.split("\n") or govde != "2. `ortak_ad`#%s yine." % b5:
        b.append(("BIRLESIK-TAVAN", "K1: defter 6 satir (canli 5, bayat): taze kume `[5 tanim]` damga beklenir: govde=%r cikti=%r" % (govde, o[-220:])))
    # (b)(c)(e) defter 5 satir, canli 6 (ayni dosyada ek asiri yuk; kur YOK)
    u = _b_damgali(motor, taban, "bir_tavan5b", 5, "1. `ortak_ad` bes yerde.")
    _yaz(os.path.join(u, "src", "p2.py"), _b_py(2) + "\n\n" + _b_py(60))
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "defter 5 satir / canli 6 tanim (H20 canli tavan)", motor, u,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [COKLU_TAVAN:1] | 0 COKLU | 0 DAMGASIZ", None)
    _b_commit(u, {}, "ek asiri yuk")
    kod, o, e, govde, _ad = _not_kos(motor, u, "2. `ortak_ad` yine.")
    sat = o.split("\n")
    if "ATIF COKLU: ortak_ad (6 tanim, tavan 5) - damgalanmadi" not in sat or govde != "2. `ortak_ad` yine.":
        b.append(("BIRLESIK-TAVAN", "K1: canli 6 tanim: damga YOK + `ATIF COKLU (6 tanim, tavan 5)`: govde=%r cikti=%r" % (govde, o[-220:])))
    if "DOGUSTA BAYAT: OLCULEMEDI (ortak_ad COKLU)" not in sat:
        b.append(("BIRLESIK-COKLU", "K3: HEAD'de 6 tanim: `OLCULEMEDI (ortak_ad COKLU)` beklenir (6 tanim icin `6 tanimdan x'u` YAZILMAZ): %r" % o[-220:]))
    # (a2) defter GUNCEL (ozet esit; yalniz tanim satirlari elle degisti: eski motor cikarimi / elle duzenleme) ve 6 SATIR, canli 5: H20 defter
    # satiri tavani (bayat defter yolu bunu gormez: tazelenmez)
    g = _b_damgali(motor, taban, "bir_tavan_g6", 5, "1. `ortak_ad` bes yerde.")
    _defter_satiri(g, "src/p1.py", "ortak_ad", +1)
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "defter 6 satir (GUNCEL) / canli 5 tanim", motor, g,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [COKLU_TAVAN:1] | 0 COKLU | 0 DAMGASIZ", None)
    kod, o, e, govde, _ad = _not_kos(motor, g, "2. `ortak_ad` yine.")        # K1 defter satiri tavani (defter GUNCEL: tazeleme yok)
    if "ATIF COKLU: ortak_ad (6 tanim, tavan 5) - damgalanmadi" not in o.split("\n") or govde != "2. `ortak_ad` yine.":
        b.append(("BIRLESIK-TAVAN", "K1: defter 6 satir (GUNCEL, canli 5): `ATIF COKLU (6 tanim, tavan 5)` beklenir: govde=%r cikti=%r" % (govde, o[-220:])))
    # (f) defter GUNCEL 5 satir (bir satir elle silindi), canli 6: H20 canli tanim tavani
    h = _b_damgali(motor, taban, "bir_tavan_g5", 5, "1. `ortak_ad` bes yerde.")
    _yaz(os.path.join(h, "src", "p2.py"), _b_py(2) + "\n\n" + _b_py(60))
    _git(h, "add", "-A")
    kur(motor, h)
    _defter_satiri(h, "src/p2.py", "ortak_ad", -1)
    _h20_hukum_say(b, "BIRLESIK-TAVAN", "defter 5 satir (GUNCEL) / canli 6 tanim", motor, h,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [COKLU_TAVAN:1] | 0 COKLU | 0 DAMGASIZ", None)
    kod, o, e, govde, _ad = _not_kos(motor, h, "2. `ortak_ad` yine.")        # K1 canli tanim tavani (defter GUNCEL: tazeleme yok)
    if "ATIF COKLU: ortak_ad (6 tanim, tavan 5) - damgalanmadi" not in o.split("\n") or govde != "2. `ortak_ad` yine.":
        b.append(("BIRLESIK-TAVAN", "K1: defter 5 satir (GUNCEL, canli 6): `ATIF COKLU (6 tanim, tavan 5)` beklenir: govde=%r cikti=%r" % (govde, o[-220:])))
    # K3 ayni durumda (P5.4: taze kume = defter, cozum 5 `birlesik` ama K1 canli sayim 6 `coklu`): K1 hukmuyle tutarli `COKLU` beyani
    if "DOGUSTA BAYAT: OLCULEMEDI (ortak_ad COKLU)" not in o.split("\n"):
        b.append(("BIRLESIK-COKLU", "K3: defter 5 satir (GUNCEL, canli 6): `OLCULEMEDI (ortak_ad COKLU)` beklenir (K1 hukmuyle tutarli): %r" % o[-220:]))
    # 6 tanimla baslarsa: damga YOK + COKLU sayimi + K3 beyani
    t6 = _b_proje(motor, taban, "bir_tavan6", 6)
    kod, o, e, govde, _ad = _not_kos(motor, t6, "1. `ortak_ad` alti yerde.")
    sat = o.split("\n")
    if kod != 0 or govde != "1. `ortak_ad` alti yerde." or "ATIF COKLU: ortak_ad (6 tanim, tavan 5) - damgalanmadi" not in sat:
        b.append(("BIRLESIK-TAVAN", "6 tanim: damga YOK + `ATIF COKLU ... (6 tanim, tavan 5)` beklenir: exit=%s govde=%r cikti=%r" % (kod, govde, o[-220:])))
    if "DOGUSTA BAYAT: OLCULEMEDI (ortak_ad COKLU)" not in sat:
        b.append(("BIRLESIK-COKLU", "6 tanimli ad icin K3 `OLCULEMEDI (ortak_ad COKLU)` beyani yok: %r" % o[-220:]))
    _b_derle(motor, t6)
    _h20_hukum_say(b, "BIRLESIK-COKLU", "6 tanimli damgasiz ad H20'de SAYILIR", motor, t6,
                   "H20: 0 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 1 COKLU | 0 DAMGASIZ", None)


def _v_ariza(motor, taban, b, bozuk):
    """BIRLESIK-ARIZA: ayni ad iki Python + bir C# dosyada; C# cikaricisi patlar -> KISMI birlesik iz YAZILMAZ."""
    ar = _b_proje(motor, taban, "bir_ariza", 2, {"src/Q.cs": "public class Q\n{\n    public int ortak_ad(int x) => x;\n}\n"})
    kod, o, e, govde, _ad = _not_kos(bozuk, ar, "1. `ortak_ad` karisik dillerde.")
    if kod != 0 or govde != "1. `ortak_ad` karisik dillerde." or "ATIF OLCULEMEDI: ortak_ad (CIKARICI)" not in o:
        b.append(("BIRLESIK-ARIZA", "bir aday dosyanin cikaricisi patladi: damga YOK (KISMI iz degil) + `OLCULEMEDI (CIKARICI)`: exit=%s govde=%r cikti=%r" % (
            kod, govde, (o + e)[-200:])))


def _v_kardes(motor, taban, b):
    """BIRLESIK-KARDES: eski TEKIL damga + sonradan ayni adli kardes tanim -> GOVDE DEGISTI (tanim kumesi) ama ayrinti satiri govdenin
    DURDUGUNU soyler."""
    t_iz = _sha8("def tekil_ad(x):\n    return x")
    kok = _b_damgali(motor, taban, "bir_kardes", 1, "1. `tekil_ad` tek.", {"src/a.py": "def tekil_ad(x):\n    return x\n"})
    # `ortak_ad` p1.py'de; `tekil_ad` a.py'de: ikinci `tekil_ad` b.py'ye eklenir ve defter yenilenir
    _yaz(os.path.join(kok, "src", "b.py"), "def tekil_ad(y):\n    return y * 3\n")
    _git(kok, "add", "-A")
    kur(motor, kok)
    yeni = _bir_iz(t_iz, _sha8("def tekil_ad(y):\n    return y * 3"))
    kod, o, e = _h20_kapi(motor, kok)
    h20 = _h20_satirlari_al(o)
    if "H20: md.1 `tekil_ad` [2 tanim] #%s -> #%s TANIM SAYISI DEGISTI (damgali govde duruyor) - IDDIA KODDAN ESKI OLABILIR" % (t_iz, yeni) not in h20:
        b.append(("BIRLESIK-KARDES", "eski tekil damga + kardes tanim: `TANIM SAYISI DEGISTI (damgali govde duruyor)` etiketi beklenir: %r" % h20))


def _v_ozdes(motor, taban, b):
    """BIRLESIK-OZDES: ayni govdeli tanimlar COKLU KUME olarak korunur (`set` degil): iz = sha(sorted([f, f, g]))."""
    f, g = _sha8("def ortak_ad(x):\n    return x + 1"), _sha8("def ortak_ad(x):\n    return x + 3")
    kok = _b_proje(motor, taban, "bir_ozdes", 0, {"src/p1.py": _b_py(1), "src/p2.py": _b_py(1), "src/p3.py": _b_py(3)})
    kod, o, e, govde, _ad = _not_kos(motor, kok, "1. `ortak_ad` uc yerde.")
    beklenen = _bir_iz(f, f, g)
    if govde != "1. `ortak_ad`#%s uc yerde." % beklenen or "ATIF DAMGALANDI: 1 (ortak_ad#%s [3 tanim])" % beklenen not in o.split("\n"):
        b.append(("BIRLESIK-OZDES", "ozdes govdeli iki tanim: iz sha(sorted([f, f, g])) = %s beklenir: govde=%r cikti=%r" % (beklenen, govde, o[-200:])))


def _v_dosyacok(motor, taban, b):
    """BIRLESIK-DOSYACOK: damgali `yol:N`'in soneki sonradan iki dosyaya cozulurse `OLCULEMEDI [DOSYA_COK]` (H18'in sebep adi; `COKLU`
    alanindan ayri)."""
    kok = _b_damgali(motor, taban, "bir_dosyacok", 1, "1. `p1.py:2` birinci.")
    _yaz(os.path.join(kok, "lib", "p1.py"), "def baska(x):\n    return x\n")
    _git(kok, "add", "-A")
    kur(motor, kok)
    _h20_hukum_say(b, "BIRLESIK-DOSYACOK", "sonek iki dosyaya cozuluyor", motor, kok,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DOSYA_COK:1] | 0 COKLU | 0 DAMGASIZ", None)
    iki = _b_proje(motor, taban, "bir_yolcoklu", 1, {"lib/p1.py": "def baska(x):\n    return x\n"})
    kod, o, e, govde, _ad = _not_kos(motor, iki, "1. `p1.py:2` iki yerde.")
    if "ATIF COKLU: p1.py:2 (2 tanim) - damgalanmadi" not in o.split("\n") or govde != "1. `p1.py:2` iki yerde.":
        b.append(("BIRLESIK-COKLU", "`yol:N` iki dosyaya cozulur: `ATIF COKLU: p1.py:2 (2 tanim)` (tavan metni DEGIL): govde=%r cikti=%r" % (govde, o[-200:])))


def _v_dogus(motor, taban, b):
    """BIRLESIK-DOGUS: ucundan 1'i 2 commit once -> `3 tanimdan 1'i` · uc tanim ayni commit'te -> `3'u` (kabul dizesi) · farkli yaslar:
    EN YAKIN commit + sayi + `(en yakin; n tanim daha eski)` · 4 ve 5 tanim (ek tablosu) · yeniden adlandirma K3'te `degisti` (beyanli)."""
    metin = "1. `ortak_ad` iddia."
    kok = _b_dogus_proje(motor, taban, "bir_dogus1")
    c_a = _b_commit(kok, {"src/p2.py": _b_py(20)}, "p2 degisti")
    _dogus_ilgisiz(kok, 2)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad 3 tanimdan 1'i 2 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, metin)[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-DOGUS", "3 tanimdan 1'i 2 commit once degisti: satirlar %r != %r" % (satirlar, bekle)))
    kok = _b_dogus_proje(motor, taban, "bir_dogus3")
    c_a = _b_commit(kok, {"src/p1.py": _b_py(10), "src/p2.py": _b_py(20), "src/p3.py": _b_py(30)}, "uc tanim degisti")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad 3 tanimdan 3'u 1 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, metin)[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-DOGUS", "3 tanimdan 3'u 1 commit once degisti: satirlar %r != %r" % (satirlar, bekle)))
    # farkli yaslar: p3 (k=3, eski) sonra p1 (k=1, yakin) -> en yakin = p1'in commit'i, sayi 2, `(en yakin; 1 tanim daha eski)`
    kok = _b_dogus_proje(motor, taban, "bir_dogus2")
    _b_commit(kok, {"src/p3.py": _b_py(30)}, "p3 degisti")
    _dogus_ilgisiz(kok, 1)
    c_b = _b_commit(kok, {"src/p1.py": _b_py(10)}, "p1 degisti")
    _dogus_ilgisiz(kok, 1, baslangic=10)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad 3 tanimdan 2'si 1 commit once degisti (%s) (en yakin; 1 tanim daha eski) - iddiayi kodla teyit et" % c_b[:7]]
    satirlar = _dogus_not(motor, kok, metin)[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-DOGUS", "iki farkli commit: EN YAKIN (p1) + sayi 2 + yas notu: satirlar %r != %r" % (satirlar, bekle)))
    # ek tablosu: 5 tanimdan 4'u / 5'i
    for n_degisen, ek in ((4, "4'u"), (5, "5'i")):
        kok = _b_dogus_proje(motor, taban, "bir_dogus_ek%d" % n_degisen, 5)
        c_a = _b_commit(kok, dict(("src/p%d.py" % i, _b_py(10 * i)) for i in range(1, n_degisen + 1)), "degisti")
        kur(motor, kok)
        bekle = ["DIKKAT: ortak_ad 5 tanimdan %s son commit'te degisti (%s) - iddiayi kodla teyit et" % (ek, c_a[:7])]
        satirlar = _dogus_not(motor, kok, metin)[3]
        if satirlar != bekle:
            b.append(("BIRLESIK-DOGUS", "5 tanimdan %s: satirlar %r != %r" % (ek, satirlar, bekle)))
    # yeniden adlandirma K3'te `degisti` sayilir (beyanli sinir): z1.py pencerenin eski surumlerinde YOK
    kok = _b_dogus_proje(motor, taban, "bir_dogus_ad")
    _git(kok, "mv", "src/p1.py", "src/z1.py")
    c_a = _b_commit(kok, {}, "yeniden adlandirildi")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad 3 tanimdan 1'i 1 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, metin)[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-DOGUS", "yeniden adlandirma K3'te `degisti` (beyanli sinir): satirlar %r != %r" % (satirlar, bekle)))


def _v_silinen(motor, taban, b):
    """BIRLESIK-SILINEN: pencerede SILINEN tanim K3'te gorunur: TEK tanimda (asiri yukten biri silindi) eski metin BAYT-BAYT; 2+ tanimda
    `pencerede s tanim silindi`."""
    metin = "1. `Hesapla` iddia."
    kok = _b_dogus_proje(motor, taban, "bir_silinen1", dosyalar={"src/Hesap.cs": DAMGA_CS})
    c_a = _b_commit(kok, {"src/Hesap.cs": DAMGA_CS.replace("    public int Hesapla(string s) => 0;\n", "")}, "asiri yuk silindi")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    bekle = ["DIKKAT: Hesapla govdesi 1 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, metin)[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-SILINEN", "tek tanim: asiri yuklerden biri 1 commit once silindi (eski metin bayt-bayt): satirlar %r != %r" % (satirlar, bekle)))
    # 2+ tanim: ayni dosyada ikinci `ortak_ad` silinir
    kok = _b_dogus_proje(motor, taban, "bir_silinen2", dosyalar={"src/p1.py": _b_py(1), "src/p2.py": _b_py(2) + "\n\n" + _b_py(40)})
    c_a = _b_commit(kok, {"src/p2.py": _b_py(2)}, "ikinci tanim silindi")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad pencerede 1 tanim silindi (1 commit once, %s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, "1. `ortak_ad` iddia.")[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-SILINEN", "2 tanim: pencerede 1 tanim silindi: satirlar %r != %r" % (satirlar, bekle)))
    # degisen + silinen AYNI commit'te: `(+1 silinen)`
    kok = _b_dogus_proje(motor, taban, "bir_silinen3", dosyalar={"src/p1.py": _b_py(1), "src/p2.py": _b_py(2) + "\n\n" + _b_py(40)})
    c_a = _b_commit(kok, {"src/p1.py": _b_py(10), "src/p2.py": _b_py(2)}, "degisti + silindi")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad 2 tanimdan 1'i 1 commit once degisti (%s) (+1 silinen) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, "1. `ortak_ad` iddia.")[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-SILINEN", "degisen + silinen ayni commit: `(+1 silinen)` beklenir: satirlar %r != %r" % (satirlar, bekle)))
    # silme pencere SINIRINDA (4 commit once; 5. surum = hafiza)
    kok = _b_dogus_proje(motor, taban, "bir_silinen4", dosyalar={"src/p1.py": _b_py(1), "src/p2.py": _b_py(2) + "\n\n" + _b_py(40)})
    c_a = _b_commit(kok, {"src/p2.py": _b_py(2)}, "ikinci tanim silindi")
    _dogus_ilgisiz(kok, 4)
    kur(motor, kok)
    bekle = ["DIKKAT: ortak_ad pencerede 1 tanim silindi (4 commit once, %s) - iddiayi kodla teyit et" % c_a[:7]]
    satirlar = _dogus_not(motor, kok, "1. `ortak_ad` iddia.")[3]
    if satirlar != bekle:
        b.append(("BIRLESIK-SILINEN", "silme pencere SINIRINDA (4 commit once): satirlar %r != %r" % (satirlar, bekle)))


def _v_dosyayok(motor, taban, b):
    """BIRLESIK-DOSYAYOK: TUM aday dosyalar silindi (defter bayat): K1 `OLCULEMEDI (DOSYA_YOK)`, damgali H20 `SEMBOL YOK`; sembol silindi
    ama dosya duruyor: K1 `COZULEMEDI` (iki hukum AYRI: dosya yoklugu defter eskimesidir, tanim yoklugu kod degisimidir)."""
    kok = _b_damgali(motor, taban, "bir_dosyayok", 2, "1. `ortak_ad` iki dosyada.")
    os.remove(os.path.join(kok, "src", "p1.py"))
    os.remove(os.path.join(kok, "src", "p2.py"))
    kod, o, e, govde, _ad = _not_kos(motor, kok, "2. `ortak_ad` yine.")
    if kod != 0 or "ATIF COZULEMEDI: ortak_ad" not in o.split("\n"):
        b.append(("BIRLESIK-DOSYAYOK", "tum aday dosyalar silindi (P5.4: taze kumede satirsiz): `ATIF COZULEMEDI: ortak_ad` beklenir: exit=%s %r" % (kod, o[-200:])))
    if any(l.startswith("DOGUSTA") for l in o.split("\n")):
        b.append(("BIRLESIK-DOSYAYOK", "tum aday dosyalar silindi: K3 SESSIZ beklenir (taze kume bos): %r" % o[-260:]))
    _h20_hukum_say(b, "BIRLESIK-DOSYAYOK", "tum aday dosyalar silindi: damgali atif SEMBOL YOK", motor, kok,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 1 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ", None)
    ty = _b_damgali(motor, taban, "bir_tamyok", 1, "1. `ortak_ad` tek.")
    _yaz(os.path.join(ty, "src", "p1.py"), "x = 1\n")
    kod, o, e, govde, _ad = _not_kos(motor, ty, "2. `ortak_ad` yine.")
    if kod != 0 or "ATIF COZULEMEDI: ortak_ad" not in o.split("\n"):
        b.append(("BIRLESIK-DOSYAYOK", "sembol silindi, dosya duruyor: `ATIF COZULEMEDI: ortak_ad` beklenir (DOSYA_YOK DEGIL): exit=%s %r" % (kod, o[-200:])))
    # H20 yedek yolu (taze kume cikarilamaz: `.git`siz kopya, bayatlik KAYNAK): damgasiz `ortak_ad` defter indeksinden sinanir (`_ad_cozum`):
    # TUM aday dosyalar yok -> damgasiz-OLCULEMEDI [DOSYA_YOK]; sembol silindi dosya duruyor -> `yok` (DOSYA_YOK DEGIL)
    d1 = _hafiza_proje(motor, taban, "bir_dyok_h20", {"src/p1.py": _b_py(1), "src/p2.py": _b_py(2), "notlar.txt": "0\n"})
    kod, o, e = kos(motor, d1, "not", "--konu", "damgasiz-not", "--yeni-konu", "damgasiz", "--tur", "durum", "--metin", "1. `ortak_ad` damgasiz.")
    if kod != 0:
        raise Kurulamadi("damgasiz not basarisiz: %r" % (o + e)[-160:])
    kur(motor, d1)
    _b_derle(motor, d1)
    k_yok = d1 + "_gitsiz_yok"
    shutil.copytree(d1, k_yok, ignore=shutil.ignore_patterns(".git"))
    os.remove(os.path.join(k_yok, "src", "p1.py"))
    os.remove(os.path.join(k_yok, "src", "p2.py"))
    _h20_hukum_say(b, "BIRLESIK-DOSYAYOK", "H20 yedek yolu: tum aday dosyalar yok (.git'siz kopya)", motor, k_yok,
                   "H20: 0 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI (damgali 0, damgasiz 1) [DOSYA_YOK:1] | 0 COKLU | 0 DAMGASIZ", None)
    k_dur = d1 + "_gitsiz_dur"
    shutil.copytree(d1, k_dur, ignore=shutil.ignore_patterns(".git"))
    _yaz(os.path.join(k_dur, "src", "p1.py"), "x = 1\n")
    _yaz(os.path.join(k_dur, "src", "p2.py"), "y = 2\n")
    kod, o, e = _h20_kapi(motor, k_dur)
    if _h20_satirlari_al(o):
        b.append(("BIRLESIK-DOSYAYOK", "H20 yedek yolu: sembol silindi, dosyalar duruyor (.git'siz kopya): damgasiz `yok` SESSIZ beklenir (DOSYA_YOK DEGIL): %r" % (
            _h20_satirlari_al(o),)))


def _v_calisma(motor, taban, b):
    """BIRLESIK-CALISMA: calisma agacinda commit'siz degisiklik IKINCI-UCUNCU tanimda (ilk grup degil) da `commit'lenmemis` der."""
    kok = _b_dogus_proje(motor, taban, "bir_calisma")
    _dogus_ilgisiz(kok, 1)
    kur(motor, kok)
    _yaz(os.path.join(kok, "src", "p3.py"), _b_py(33))
    satirlar = _dogus_not(motor, kok, "1. `ortak_ad` iddia.")[3]
    if satirlar != ["DIKKAT: ortak_ad commit'lenmemis degisiklik tasiyor"]:
        b.append(("BIRLESIK-CALISMA", "3. tanimda commit'siz degisiklik: `commit'lenmemis` beklenir: satirlar %r" % satirlar))


def _v_butce(motor, taban, b, butcesiz):
    """BIRLESIK-BUTCE: sure butcesi asilirsa (butcesiz motor: `_DOGUS_BUTCE = 0`) dosyalar `OLCULEMEDI` diye BEYAN edilir ve belirtec ADI
    sayilir; hukum VERILMEZ (butce kontrolu kalkarsa gercek hukum basilirdi)."""
    kok = _b_dogus_proje(motor, taban, "bir_butce")
    c_a = _b_commit(kok, {"src/p2.py": _b_py(20)}, "p2 degisti")
    kur(motor, kok)
    kod, o, e, govde, _ad = _not_kos(butcesiz, kok, "1. `ortak_ad` iddia.", True)
    sat = [l for l in o.split("\n") if l.startswith(("DIKKAT:", "DOGUSTA BAYAT:"))]
    if sat != ["DOGUSTA BAYAT: OLCULEMEDI (3 dosya: 0 sn sure butcesi asildi; hukumsuz: ortak_ad)"]:
        b.append(("BIRLESIK-BUTCE", "butce asildi: tum dosyalar `OLCULEMEDI` + `hukumsuz: ortak_ad` beklenir (%s): satirlar %r" % (c_a[:7], sat)))


def _v_kap(motor, taban, b):
    """BIRLESIK-KAP: 20 dosya tavaninda EN AZ dosyali belirtec once secilir (tekil adlar birlesik adlarin dosyalari yuzunden dusmez);
    sigmayan birlesik ad ADIYLA beyan edilir; 5'ten cok hukumsuz ad `+N daha` ile kirpilir."""
    dos = {"notlar.txt": "0\n"}
    for ad in ("coklu_a", "coklu_b"):
        for i in range(1, 6):
            dos["src/%s%d.py" % (ad[-1], i)] = "def %s(x):\n    return x + %d\n" % (ad, i)
    for i in range(12):
        dos["src/t%02d.py" % i] = "def tekil_%02d(x):\n    return x\n" % i
    kok = _b_dogus_proje(motor, taban, "bir_kap", dosyalar=dos)
    c_a = _b_commit(kok, dict(("src/t%02d.py" % i, "def tekil_%02d(x):\n    return x + 1\n" % i) for i in range(12)), "tekiller degisti")
    kur(motor, kok)
    metin = "\n".join(["1. `coklu_a` `coklu_b`"] + ["%d. `tekil_%02d` iddia." % (i + 2, i) for i in range(12)])
    satirlar = _dogus_not(motor, kok, metin)[3]
    bekle = ["DIKKAT: tekil_%02d govdesi son commit'te degisti (%s) - iddiayi kodla teyit et" % (i, c_a[:7]) for i in range(12)]
    bekle.append("DOGUSTA BAYAT: OLCULEMEDI (22 dosya: git gecmisi yalniz en cok 20 dosya icin soruldu; hukumsuz: coklu_b)")
    if satirlar != bekle:
        b.append(("BIRLESIK-KAP", "20 dosya tavani: 12 tekil ad + coklu_a yargilanir, coklu_b ADIYLA hukumsuz: satirlar %r" % satirlar))
    # KISMEN sigan ad: zz_ad {z1, z2} secilir (20. dosya), ww_ad {z1, w1, w2}: z1 secilmis AMA w1/w2 sigmaz -> ww_ad ADIYLA hukumsuz
    dos = dict(("src/s%02d.py" % i, "def s_ad_%02d(x):\n    return x\n" % i) for i in range(18))
    dos["src/z1.py"] = "def zz_ad(x):\n    return x\n\n\ndef ww_ad(x):\n    return x\n"
    dos["src/z2.py"] = "def zz_ad(y):\n    return y\n"
    dos["src/w1.py"] = "def ww_ad(a):\n    return a\n"
    dos["src/w2.py"] = "def ww_ad(c):\n    return c\n"
    kp = _b_dogus_proje(motor, taban, "bir_kismi", dosyalar=dos)
    kur(motor, kp)
    metin = "\n".join(["1. `zz_ad` `ww_ad`"] + ["%d. `s_ad_%02d` iddia." % (i + 2, i) for i in range(18)])
    satirlar = _dogus_not(motor, kp, metin)[3]
    if satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (22 dosya: git gecmisi yalniz en cok 20 dosya icin soruldu; hukumsuz: ww_ad)"]:
        b.append(("BIRLESIK-KAP", "ad dosyalarinin KISMI tavana sigiyor: ww_ad ADIYLA hukumsuz (KeyError DEGIL): satirlar %r" % satirlar))
    k26 = _b_dogus_proje(motor, taban, "bir_kap26", dosyalar=dict([("src/n%02d.py" % i, "def tek_ad_%02d(x):\n    return x\n" % i)
                                                                for i in range(26)]))
    kur(motor, k26)
    satirlar = _dogus_not(motor, k26, "\n".join("%d. `tek_ad_%02d` iddia." % (i + 1, i) for i in range(26)))[3]
    if satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (26 dosya: git gecmisi yalniz en cok 20 dosya icin soruldu; "
                    "hukumsuz: tek_ad_20, tek_ad_21, tek_ad_22, tek_ad_23, tek_ad_24 +1 daha)"]:
        b.append(("BIRLESIK-KAP", "26 tekil ad: 6 hukumsuz, en cok 5 ad + `+1 daha`: satirlar %r" % satirlar))


def _v_atlandi(motor, taban, b):
    """BIRLESIK-ATLANDI: defter ATLANDI dosya tasirken (sozdizimi hatasi) ad icin tanim kumesi EKSIK olabilir: damga basilir AMA beyan
    edilir (`ATIF NOT`); tam kapsamli defterde NOT YOK."""
    kok = _b_proje(motor, taban, "bir_atlandi", 2, {"src/kotu.py": "def (:\n"})
    kod, o, e, govde, _ad = _not_kos(motor, kok, "1. `ortak_ad` iki yerde.")
    sat = o.split("\n")
    dam = _bir_iz(_b_iz(1), _b_iz(2))
    if kod != 0 or "ATIF DAMGALANDI: 1 (ortak_ad#%s [2 tanim])" % dam not in sat or \
            not any(l.startswith("ATIF NOT: defter ATLANDI dosya iceriyor - ad icin tanim kumesi EKSIK olabilir") for l in sat):
        b.append(("BIRLESIK-ATLANDI", "defter ATLANDI dosya tasiyor: damga + `ATIF NOT: defter ATLANDI ...` beklenir: exit=%s %r" % (kod, o[-300:])))


def _v_nesne(motor, taban, b):
    """BIRLESIK-NESNE: git nesne/okuma kenar durumlari: kayip nesne (`cat-file missing` + exit 0) `ls-tree` ile ONAYLANMADAN 'dosya yok'
    sayilmaz · dizin olan yol kayit hizasini BOZMAZ · `.ts` ve `.tsx` ayni bayt ayri cikarici · defter yolundaki `%XX` kacisi cozulur
    · >8 MB gecmis surum `BUYUK`."""
    # (1) kayip kok-agac nesnesi: HEAD~3'un tree'si yok -> `missing`, exit 0; hukum VERILMEZ
    k1 = _hafiza_proje(motor, taban, "bir_kayip", {"src/a_mod.py": DOGUS_V0, "notlar.txt": "0\n"})
    _dogus_ilgisiz(k1, 4)
    kur(motor, k1)
    agac = _git(k1, "rev-parse", "HEAD~3^{tree}").stdout.decode("ascii").strip()
    nesne = os.path.join(k1, ".git", "objects", agac[:2], agac[2:])
    if os.path.isfile(nesne):
        os.chmod(nesne, stat.S_IWRITE)
        os.remove(nesne)
        kod, o, e, satirlar, govde = _dogus_not(motor, k1, "1. `hedef_islev` iddia.")
        if satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (hedef_islev: GIT_OKUNAMADI)"]:
            b.append(("BIRLESIK-NESNE", "kayip nesne: `OLCULEMEDI (GIT_OKUNAMADI)` beklenir (sahte `degisti` DEGIL): satirlar %r" % satirlar))
    # (2) bir surumde `src/q.py` DIZIN: kayit hizasi korunur, sonraki dosya (r.py) YARGILANIR
    k2 = _hafiza_proje(motor, taban, "bir_dizin", {"src/q.py/ic.txt": "x\n", "src/r.py": "def r_islev(x):\n    return x\n", "notlar.txt": "0\n"})
    _sil(os.path.join(k2, "src", "q.py"))
    c_a = _b_commit(k2, {"src/q.py": "def q_islev(x):\n    return x\n", "src/r.py": "def r_islev(x):\n    return x + 1\n"}, "dizin -> dosya")
    kur(motor, k2)
    satirlar = _dogus_not(motor, k2, "1. `q_islev` `r_islev` iddia.")[3]
    bekle = ["DOGUSTA BAYAT: OLCULEMEDI (q_islev: GIT_OKUNAMADI)",
             "DIKKAT: r_islev govdesi son commit'te degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]
    if satirlar != bekle:
        b.append(("BIRLESIK-NESNE", "dizin olan yol: q_islev OLCULEMEDI, r_islev YARGILANIR: satirlar %r != %r" % (satirlar, bekle)))
    # (3) ayni bayt .ts + .tsx: cikarici dili AYRI (`.tsx` JSX maskeli)
    jsx = "export function KartBilesen() {\n  return <p>use ` here</p>;\n}\n\nexport function DigerIslev(x: number) {\n  return x + 1;\n}\n"
    k3 = _hafiza_proje(motor, taban, "bir_tsx", {"src/a.ts": jsx, "src/a.tsx": jsx, "notlar.txt": "0\n"})
    _dogus_ilgisiz(k3, 2)
    kur(motor, k3)
    kod, o, e, satirlar, govde = _dogus_not(motor, k3, "1. `KartBilesen` var; `DigerIslev` var.")
    if satirlar:
        b.append(("BIRLESIK-CIKARICI", "ayni bayt .ts + .tsx (cikarici AYRI): `commit'lenmemis` SAHTE uyari YOK beklenir: satirlar %r" % satirlar))
    # (4) defter yolu `%` iceriyor (`%25` kacisi): cat-file'a COZULMUS yol gider
    k4 = _hafiza_proje(motor, taban, "bir_yuzde", {"src/y%25z.py": "def yuzde_islev(x):\n    return x\n", "notlar.txt": "0\n"})
    c_a = _b_commit(k4, {"src/y%25z.py": "def yuzde_islev(x):\n    return x + 1\n"}, "degisti")
    _dogus_ilgisiz(k4, 1)
    kur(motor, k4)
    satirlar = _dogus_not(motor, k4, "1. `yuzde_islev` iddia.")[3]
    if satirlar != ["DIKKAT: yuzde_islev govdesi 1 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]:
        b.append(("BIRLESIK-YOLKACIS", "yolda `%%`: kacis cozulur, degisim gorulur: satirlar %r" % satirlar))
    # (5) 8 MB'tan buyuk GECMIS surum: okunmaz, `BUYUK`
    k5 = _hafiza_proje(motor, taban, "bir_buyuk", {"src/g.py": "#" * 8600000 + "\ndef buyuk_islev(x):\n    return x\n", "notlar.txt": "0\n"})
    _b_commit(k5, {"src/g.py": "def buyuk_islev(x):\n    return x\n"}, "kucultuldu")
    _dogus_ilgisiz(k5, 1)
    kur(motor, k5)
    satirlar = _dogus_not(motor, k5, "1. `buyuk_islev` iddia.")[3]
    if satirlar != ["DOGUSTA BAYAT: OLCULEMEDI (buyuk_islev: BUYUK)"]:
        b.append(("BIRLESIK-NESNE", "8 MB'tan buyuk gecmis surum: `OLCULEMEDI (BUYUK)` beklenir: satirlar %r" % satirlar))


def _v_kucukler(motor, taban, b):
    """BIRLESIK-YOLCOKLU / BIRLESIK-SAYISIZ: asiri yuklu `yol:N` K1'de `ATIF COKLU (2 tanim)`; K3'te `yol:N` eski metin (`govdesi`) ve
    COKLU DEGIL; numarasiz satirdaki damgasiz belirtec H20 siniflarina GIRMEZ."""
    kc = _hafiza_proje(motor, taban, "bir_asiri", {"src/Hesap.cs": DAMGA_CS, "notlar.txt": "0\n"})
    c_a = _b_commit(kc, {"src/Hesap.cs": DAMGA_CS.replace("=> x;", "=> x + 1;")}, "asiri yuk degisti")
    _dogus_ilgisiz(kc, 1)
    kur(motor, kc)
    kod, o, e, satirlar, govde = _dogus_not(motor, kc, "1. `src/Hesap.cs:3` iddia.")
    if "ATIF COKLU: src/Hesap.cs:3 (2 tanim) - damgalanmadi" not in o.split("\n"):
        b.append(("BIRLESIK-YOLCOKLU", "asiri yuklu `yol:N`: `ATIF COKLU: ... (2 tanim)` beklenir: %r" % o[-200:]))
    if satirlar != ["DIKKAT: src/Hesap.cs:3 govdesi 1 commit once degisti (%s) - iddiayi kodla teyit et" % c_a[:7]]:
        b.append(("BIRLESIK-YOLCOKLU", "asiri yuklu `yol:N` K3: tek tanim metni (`govdesi`), COKLU/`k tanimdan` DEGIL: satirlar %r" % satirlar))
    ns = _hafiza_proje(motor, taban, "bir_numarasiz", {"src/a.py": H20_A})
    kos(motor, ns, "not", "--konu", "damgasiz-not", "--yeni-konu", "numarasiz damgasiz", "--tur", "durum", "--metin",
        "- `ikinci_islev` numarasiz satir (madde DEGIL).")
    kur(motor, ns)
    kos(motor, ns, *(DAMGA_NOT_ARGS + ("1. `tekil_islev` ilk iddia.",)))
    kos(motor, ns, "derle")
    _git(ns, "add", "-A")
    _git(ns, "commit", "-q", "-m", "numarasiz")
    _h20_hukum_say(b, "BIRLESIK-SAYISIZ", "numarasiz satirdaki damgasiz belirtec sayilmaz", motor, ns,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ", None)


# ------------------------------------------------------------------ P5.3 (KALEM 7): BAYAT defterde H20 YENI tanimi gorur
def _defter_satiri(kok, yol, ad, fark):
    """ADRES.tsv'de `yol`daki ilk `ad` tanim satirini cogaltir (+1) ya da siler (-1): `dosya` satirlari ve baslik `ozet`i DOKUNULMAZ (defter
    bayat OLMAZ; eski motor cikarimi / elle duzenleme benzetimi)."""
    p = _defter_yolu(kok)
    sat = io.open(p, encoding="utf-8", newline="").read().split("\n")
    i = next(k for k, l in enumerate(sat) if k and l.split("\t")[:1] == [yol] and l.split("\t")[2:3] == [ad])
    sat[i:i + 1] = [sat[i], sat[i]] if fark > 0 else []
    _yaz(p, "\n".join(sat))


def _defter_tam_degistir(kok, yol, ad, yeni_ad):
    """ADRES.tsv'de `yol`daki ilk `ad` tanim satirinin AD sutununu `yeni_ad` yapar (`dosya` satirlari ve baslik `ozet`i DOKUNULMAZ: defter GUNCEL;
    eski motor cikarimi / elle duzenleme UYUSMAZLIGI benzetimi: aday satir canli cikarimda YOK)."""
    p = _defter_yolu(kok)
    sat = io.open(p, encoding="utf-8", newline="").read().split("\n")
    i = next(k for k, l in enumerate(sat) if k and l.split("\t")[:1] == [yol] and l.split("\t")[2:3] == [ad])
    r = sat[i].split("\t")
    r[2] = yeni_ad
    sat[i] = "\t".join(r)
    _yaz(p, "\n".join(sat))


def _taze_not(b, etiket, ne, motor, kok, beklenen_satir, ayrinti, exit0):
    """Bayat defterde (`adres --kur` YOK) H20 hukmu `beklenen_satir`/`ayrinti`; ardindan `--kur` ve hukmun BAYT-AYNI kaldigi (hukum defter
    tazeligine BAGLI degil: bayat defter SESSIZ TEMIZ uretemez)."""
    _kod, o = _h20_hukum_say(b, etiket, ne + " (defter BAYAT)", motor, kok, beklenen_satir, exit0, ayrinti)
    bayat = _h20_satirlari_al(o)
    kur(motor, kok)
    taze = _h20_satirlari_al(_h20_kapi(motor, kok)[1])
    if bayat != taze:
        b.append((etiket, "%s: bayat defterle H20 hukmu TAZE defterle AYNI olmali: %r != %r" % (ne, bayat, taze)))


def _v_taze(motor, taban, b):
    """BIRLESIK-TAZE (is emri KALEM 7): 4. tanim YENI dosyada eklenir + commit + `adres --kur` YOK -> `GOVDE DEGISTI 1 [4 tanim]`, `0/0`
    (SESSIZ TEMIZ) DEGIL; hukum `--kur` sonrasiyla bayt-ayni."""
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    kok = _b_damgali(motor, taban, "bir_taze", 3)
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, {"src/p4.py": _b_py(4)}, "4. tanim yeni dosyada")
    _taze_not(b, "BIRLESIK-TAZE", "4. tanim YENI dosyada", motor, kok, BIRLESIK_DEGISTI1,
              "H20: md.1 `ortak_ad` [4 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])), kod0)


def _v_taze_tekil(motor, taban, b):
    """BIRLESIK-TAZE-TEKIL: TEKIL damgali ad + yeni dosyada AYNI adli ikinci tanim (tekil -> coklu gecisi), defter bayat -> `[2 tanim]` +
    `TANIM SAYISI DEGISTI (damgali govde duruyor)`."""
    t_iz = _sha8("def tekil_ad(x):\n    return x")
    kok = _b_damgali(motor, taban, "bir_taze_tek", 1, "1. `tekil_ad` tek.", {"src/a.py": "def tekil_ad(x):\n    return x\n"})
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-TEKIL", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, {"src/b.py": "def tekil_ad(y):\n    return y * 3\n"}, "ikinci tanim yeni dosyada")
    yeni = _bir_iz(t_iz, _sha8("def tekil_ad(y):\n    return y * 3"))
    _taze_not(b, "BIRLESIK-TAZE-TEKIL", "tekil -> coklu (yeni dosya)", motor, kok, BIRLESIK_DEGISTI1,
              "H20: md.1 `tekil_ad` [2 tanim] #%s -> #%s TANIM SAYISI DEGISTI (damgali govde duruyor) - IDDIA KODDAN ESKI OLABILIR" % (t_iz, yeni), kod0)


def _v_taze_ad(motor, taban, b):
    """BIRLESIK-TAZE-AD: AYNI dosyada baska sinifta ayni uye adi (YENI tam ad `B.hesapla`; aday cift kumesinde yoktu), defter bayat."""
    m_iz = _sha8("    def hesapla(self):\n        return 1")
    kok = _b_damgali(motor, taban, "bir_taze_ad", 1, "1. `hesapla` tek.", {"src/m.py": "class A:\n    def hesapla(self):\n        return 1\n"})
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-AD", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, {"src/m.py": "class A:\n    def hesapla(self):\n        return 1\n\n\nclass B:\n    def hesapla(self):\n        return 2\n"},
              "baska sinifta ayni uye adi")
    yeni = _bir_iz(m_iz, _sha8("    def hesapla(self):\n        return 2"))
    _taze_not(b, "BIRLESIK-TAZE-AD", "ayni dosyada yeni tam ad", motor, kok, BIRLESIK_DEGISTI1,
              "H20: md.1 `hesapla` [2 tanim] #%s -> #%s TANIM SAYISI DEGISTI (damgali govde duruyor) - IDDIA KODDAN ESKI OLABILIR" % (m_iz, yeni), kod0)
    # degisen dosyalarin ESKI satirlari ciftlenmez: 3 tanimli ad, uc dosya da degisti (govde AYNI, yalniz yorum eklendi) -> satir sayisi 3 kalir
    # (6 olsaydi `OLCULEMEDI [COKLU_TAVAN]`)
    cf = _b_damgali(motor, taban, "bir_taze_cift", 3)
    _b_commit(cf, dict(("src/p%d.py" % i, _b_py(i) + "# yorum\n") for i in (1, 2, 3)), "yalniz yorum eklendi")
    _taze_not(b, "BIRLESIK-TAZE-AD", "degisen dosyalarda satirlar ciftlenmez", motor, cf, BIRLESIK_TABAN1, None, kod0)


def _v_taze_silinen(motor, taban, b):
    """BIRLESIK-TAZE-SILINEN: bir tanimin dosyasi SILINIR (commit, defter bayat) -> `[2 tanim]` (kismi kume `OLCULEMEDI` DEGIL) · dosya TASINIR
    (govde ayni) -> `ayni` · dosya IZLENMEZ olur ama diskte durur (`git rm --cached`: `--kur` onu hic gormez) -> `[2 tanim]`."""
    b3, b2 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _bir_iz(_b_iz(1), _b_iz(2))
    ayr = "H20: md.1 `ortak_ad` [2 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (b3, b2)
    kok = _b_damgali(motor, taban, "bir_taze_sil", 3)
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-SILINEN", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _git(kok, "rm", "-q", "-f", "src/p3.py")
    _b_commit(kok, {}, "p3 silindi")
    _taze_not(b, "BIRLESIK-TAZE-SILINEN", "tanimin dosyasi silindi", motor, kok, BIRLESIK_DEGISTI1, ayr, kod0)
    ty = _b_damgali(motor, taban, "bir_taze_tasi", 3)
    _git(ty, "mv", "src/p1.py", "src/z1.py")
    _b_commit(ty, {}, "p1 tasindi")
    _taze_not(b, "BIRLESIK-TAZE-SILINEN", "dosya tasindi (govde ayni)", motor, ty, BIRLESIK_TABAN1, None, kod0)
    iz = _b_damgali(motor, taban, "bir_taze_izsiz", 3)
    _git(iz, "rm", "--cached", "-q", "src/p3.py")
    if _git(iz, "commit", "-q", "-m", "p3 izlenmiyor").returncode != 0:
        raise Kurulamadi("izlenmeyen duruma gecis commit'i basarisiz")
    _taze_not(b, "BIRLESIK-TAZE-SILINEN", "dosya izlenmez oldu (diskte duruyor)", motor, iz, BIRLESIK_DEGISTI1, ayr, kod0)
    # izlenen dosya DISKTEN silindi (git rm YOK): P5.2 `_v_dosyayok` ile pinli `SEMBOL YOK`; `--kur` ayni dosyayi ATLANDI (okunamadi) sayar:
    # bayat durum bu sinifta `--kur`dan CESURDUR (beyanli ayrisma, README sinir 21)
    dy = _b_damgali(motor, taban, "bir_taze_diskte", 1, "1. `tekil_ad` tek.", {"src/t.py": "def tekil_ad(x):\n    return x\n"})
    os.remove(os.path.join(dy, "src", "t.py"))
    _h20_hukum_say(b, "BIRLESIK-TAZE-SILINEN", "izlenen dosya diskten silindi, defter bayat: SEMBOL YOK", motor, dy,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 1 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 0 DAMGASIZ", None)
    kur(motor, dy)
    _h20_hukum_say(b, "BIRLESIK-TAZE-SILINEN", "ayni durum `--kur` sonrasi: dosya ATLANDI sayilir (beyanli ayrisma)", motor, dy,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_ATLANDI:1] | 0 COKLU | 0 DAMGASIZ", None)


def _v_taze_tavan(motor, taban, b):
    """BIRLESIK-TAZE-TAVAN: bayat dosya sayisi `_H20_TAZE_TAVAN` (100) DAHIL tazelenir (hukum verilir); 101'de bellekte cikarim yapilmaz:
    `OLCULEMEDI [DEFTER_BAYAT]` (sessiz temiz DEGIL; maliyet siniri) ve KESIN POZITIF (govdesi degisen atif) KORUNUR."""
    e = dict(("src/e%03d.py" % i, "def e%03d_islev():\n    return 0\n" % i) for i in range(101))
    kok = _b_damgali(motor, taban, "bir_taze_tavan", 3, ek=e)
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-TAVAN", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, dict(("src/e%03d.py" % i, "def e%03d_islev():\n    return 1\n" % i) for i in range(100)), "100 dosya degisti")
    _h20_hukum_say(b, "BIRLESIK-TAZE-TAVAN", "100 bayat dosya (tavan DAHIL): tazelenir", motor, kok, BIRLESIK_TABAN1, kod0)
    _b_commit(kok, {"src/e100.py": "def e100_islev():\n    return 1\n"}, "101. dosya degisti")
    _h20_hukum_say(b, "BIRLESIK-TAZE-TAVAN", "101 bayat dosya (tavan ASILDI): OLCULEMEDI", motor, kok,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYAT:1] | 0 COKLU | 0 DAMGASIZ", kod0)
    _b_commit(kok, {"src/p3.py": _b_py(30)}, "p3 govdesi degisti")
    _h20_hukum_say(b, "BIRLESIK-TAZE-TAVAN", "101 bayat dosya + govde degisti: kesin pozitif KORUNUR", motor, kok, BIRLESIK_DEGISTI1, kod0,
                   "H20: md.1 `ortak_ad` [3 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
                       _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _bir_iz(_b_iz(1), _b_iz(2), _b_iz(30))))


def _v_taze_bayt(motor, taban, b):
    """BIRLESIK-TAZE-BAYT: bayat dosyalarin TOPLAM boyutu `_H20_TAZE_BAYT` (8 MiB) asarsa (sayi tavani altinda bile) bellekte cikarim
    yapilmaz: `OLCULEMEDI [DEFTER_BAYAT]`; tek 5 MB'lik bayat dosya tazelenir."""
    dolgu = "# " + "x" * 78 + "\n"
    buyuk = lambda i: dolgu * 65000 + "def g%d_islev():\n    return 1\n" % i      # ~5,1 MB
    kok = _b_damgali(motor, taban, "bir_taze_bayt", 3, ek={"src/g1.py": "def g1_islev():\n    return 0\n", "src/g2.py": "def g2_islev():\n    return 0\n"})
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-BAYT", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, {"src/g1.py": buyuk(1)}, "tek buyuk dosya")
    _h20_hukum_say(b, "BIRLESIK-TAZE-BAYT", "tek 5 MB bayat dosya: tazelenir", motor, kok, BIRLESIK_TABAN1, kod0)
    _b_commit(kok, {"src/g2.py": buyuk(2)}, "ikinci buyuk dosya")
    _h20_hukum_say(b, "BIRLESIK-TAZE-BAYT", "10 MB bayat dosya (bayt tavani ASILDI): OLCULEMEDI", motor, kok,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYAT:1] | 0 COKLU | 0 DAMGASIZ", kod0)
    # YENI (defterde olmayan) dosyalar da bayt toplamina girer: iki yeni 5 MB dosya
    yn = _b_damgali(motor, taban, "bir_taze_bayt2", 3)
    _b_commit(yn, {"src/h1.py": buyuk(1), "src/h2.py": buyuk(2)}, "iki yeni buyuk dosya")
    _h20_hukum_say(b, "BIRLESIK-TAZE-BAYT", "iki YENI 5 MB dosya (bayt tavani ASILDI): OLCULEMEDI", motor, yn,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYAT:1] | 0 COKLU | 0 DAMGASIZ", kod0)


def _v_taze_yol(motor, taban, b):
    """BIRLESIK-TAZE-YOL: damgali `yol:N`'in soneki sonradan (commit, defter bayat) iki dosyaya cozulur -> `OLCULEMEDI [DOSYA_COK]` (taban
    dosya listesi de tazelenir)."""
    kok = _b_damgali(motor, taban, "bir_taze_yol", 1, "1. `p1.py:2` birinci.")
    kod0 = _h20_hukum_say(b, "BIRLESIK-TAZE-YOL", "taban", motor, kok, BIRLESIK_TABAN1, None)[0]
    _b_commit(kok, {"lib/p1.py": "def baska(x):\n    return x\n"}, "ayni adli ikinci dosya")
    _taze_not(b, "BIRLESIK-TAZE-YOL", "sonek iki dosyaya cozuluyor", motor, kok,
              "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DOSYA_COK:1] | 0 COKLU | 0 DAMGASIZ", None, kod0)


def _agac_izi(kok, *dizinler):
    """Proje agacinin (`.git` HARIC) ve verilen dizinlerin dosya listesi + icerik ozeti: `kapi`nin DISKE yazip yazmadigini olcer."""
    izler = []
    for d in (kok,) + dizinler:
        for r, alt, dosyalar in os.walk(d):
            alt[:] = [x for x in alt if x != ".git"]
            for f in dosyalar:
                p = os.path.join(r, f)
                with open(p, "rb") as g:
                    izler.append((os.path.relpath(p, os.path.dirname(kok)), hashlib.sha256(g.read()).hexdigest()))
    return sorted(izler)


def _v_taze_yazma(motor, taban, b):
    """BIRLESIK-TAZE-YAZMA: bayat defterde `kapi` DISKE YAZMAZ: proje agaci (ADRES.tsv dahil) ve gecici dizin (SICAK stat onbellegi) kapi
    oncesi/sonrasi bayt-ayni; sicak onbellekle hukum soguktakiyle AYNI (yazma sabotaji onbellegi degistirir: yeni dosya onbellekte YOK)."""
    kok = _b_damgali(motor, taban, "bir_taze_yaz", 3)
    kos(motor, kok, "adres", "ortak_ad")                       # onbellegi ISIT (defter guncel; yazan `adres` yolu)
    _b_commit(kok, {"src/p4.py": _b_py(4)}, "yeni dosya")
    time.sleep(3.3)                                            # yeni dosya RACY paydan (3 sn) yasli: onbellege GIRER
    tmp = onb_dizini(kok)
    once = _agac_izi(kok, tmp)
    kod, o, _e = _h20_kapi(motor, kok)
    sonra = _agac_izi(kok, tmp)
    if once != sonra:
        b.append(("BIRLESIK-TAZE-YAZMA", "bayat defterde `kapi` DISKE yazdi (ekle/degis): %r" % (sorted(set(sonra) ^ set(once))[:4],)))
    b3 = _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3))
    if "H20: md.1 `ortak_ad` [4 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
            b3, _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])) not in _h20_satirlari_al(o):
        b.append(("BIRLESIK-TAZE-YAZMA", "SICAK onbellekle hukum soguktakiyle ayni olmali: %r" % _h20_satirlari_al(o)))


def _v_taze_ariza(motor, taban, b, tarama_bozuk):
    """BIRLESIK-TAZE-ARIZA: bayatlik OLCUMU patlarsa (`SystemExit` dahil) defter `guncel` SAYILMAZ: `ayni` atif `OLCULEMEDI [DEFTER_BAYATLIK]`
    olur, KESIN POZITIF (govdesi degisen atif) KORUNUR; diger TUM `kapi` satirlari + exit bozuk-olmayan motorla bayt-bayt AYNI."""
    kok = _b_damgali(motor, taban, "bir_taze_ariza", 3, "1. `ortak_ad` uc yerde.\n2. `tekil_ad` tek yerde.",
                     {"src/t.py": "def tekil_ad(x):\n    return x\n"})
    _b_commit(kok, {"src/p3.py": _b_py(30)}, "p3 govdesi degisti")
    kod_t, o_t, _e = _h20_kapi(motor, kok)
    kod, o, e = _h20_kapi(tarama_bozuk, kok)
    if "HATA:" in e:
        b.append(("BIRLESIK-TAZE-ARIZA", "bayatlik olcumu arizasinda `oldur`un stderr satiri SIZMAMALI (P5 blogu `oldur` yan etkisi yok): %r" % e[-160:]))
    h20 = _h20_satirlari_al(o)
    bekle = ["H20: 2 atif | 1 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYATLIK:1] | 0 COKLU | 0 DAMGASIZ",
             "H20: md.1 `ortak_ad` [3 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
                 _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _bir_iz(_b_iz(1), _b_iz(2), _b_iz(30)))]
    if h20 != bekle:
        b.append(("BIRLESIK-TAZE-ARIZA", "bayatlik olcumu arizali: pozitif KORUNUR + `ayni` -> `OLCULEMEDI [DEFTER_BAYATLIK:1]`: %r != %r" % (h20, bekle)))
    if kod != kod_t or _kapi_diger(o) != _kapi_diger(o_t):
        b.append(("BIRLESIK-TAZE-ARIZA", "bayatlik olcumu arizasi `kapi`nin DIGER hukumlerini/exit'ini degistirdi: exit %s != %s" % (kod, kod_t)))


def _v_taze_kapsam(motor, taban, b):
    """BIRLESIK-TAZE-KAPSAM/-GURULTU/-OKUNMAZ: bayat defterde YENI dosya cikarilamazsa tanimlari BILINMEZ: adi sozcuk olarak iceren dosyada
    `ayni` -> `OLCULEMEDI [DEFTER_ATLANDI]` (KAPSAM) · adi ICERMEYEN dosyada hukum DEGISMEZ, gurultu yok (GURULTU) · kaybolan sembol
    `SEMBOL YOK` DEGIL `OLCULEMEDI [DEFTER_ATLANDI]` (cikarilamayan yeni dosya ya da 9 MB'lik OKUNMAZ yeni dosya; OKUNMAZ)."""
    atl = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_ATLANDI:1] | 0 COKLU | 0 DAMGASIZ"
    k1 = _b_damgali(motor, taban, "bir_taze_kotu", 3)
    _b_commit(k1, {"src/kotu.py": "def ortak_ad(x:\n"}, "yeni dosya bozuk ve ad geciyor")
    _h20_hukum_say(b, "BIRLESIK-TAZE-KAPSAM", "yeni bozuk dosya adi iceriyor: `ayni` OLCULEMEDI", motor, k1, atl, None)
    k2 = _b_damgali(motor, taban, "bir_taze_kotu2", 3)
    _b_commit(k2, {"src/kotu.py": "def baska_ad(x:\n"}, "yeni dosya bozuk, ad YOK")
    _h20_hukum_say(b, "BIRLESIK-TAZE-GURULTU", "yeni bozuk dosya adi ICERMIYOR: hukum degismez", motor, k2, BIRLESIK_TABAN1, None)
    k3 = _b_damgali(motor, taban, "bir_taze_kotu3", 2)
    _b_commit(k3, {"src/p1.py": "x = 1\n", "src/p2.py": "y = 2\n", "src/kotu.py": "def (:\n"}, "tanimlar kalkti + yeni dosya bozuk")
    _h20_hukum_say(b, "BIRLESIK-TAZE-KAPSAM", "sembol kayboldu + yeni dosya cikarilamadi: SEMBOL YOK DEGIL", motor, k3, atl, None)
    k4 = _b_damgali(motor, taban, "bir_taze_buyuk", 2)
    _b_commit(k4, {"src/p1.py": "x = 1\n", "src/p2.py": "y = 2\n", "src/gen.py": "#" * 9000000 + "\ndef gen_islev(x):\n    return x\n"},
              "tanimlar kalkti + yeni 9 MB dosya")
    _h20_hukum_say(b, "BIRLESIK-TAZE-OKUNMAZ", "sembol kayboldu + yeni dosya OKUNAMIYOR (9 MB): SEMBOL YOK DEGIL", motor, k4, atl, None)
    # degisen dosya cikarilamaz hale gelir: eski satirlari `--kur` gibi DUSER (adi iceren bozuk dosya `ayni` DEGIL, kalan tanimlar `[2 tanim]`)
    k5 = _b_damgali(motor, taban, "bir_taze_kotu5", 3)
    kod5 = _h20_hukum_say(b, "BIRLESIK-TAZE-KAPSAM", "taban", motor, k5, BIRLESIK_TABAN1, None)[0]
    _b_commit(k5, {"src/p3.py": "def ortak_ad(x:\n"}, "p3 bozuldu (degisen dosya cikarilamaz)")
    _taze_not(b, "BIRLESIK-TAZE-KAPSAM", "degisen dosya cikarilamaz hale geldi", motor, k5, BIRLESIK_DEGISTI1,
              "H20: md.1 `ortak_ad` [2 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
                  _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _bir_iz(_b_iz(1), _b_iz(2))), kod5)
    # SUREKLI okunamayan izlenen dosya (defter ATLANDI tasir): ilgisiz kod degisikligi `ayni`yi gurultuye CEVIRMEZ
    k6 = _b_damgali(motor, taban, "bir_taze_kalici", 3, ek={"src/gen.py": "#" * 9000000 + "\n"})
    _b_commit(k6, {"src/x.py": "def baska_islev():\n    return 1\n"}, "ilgisiz yeni dosya")
    _h20_hukum_say(b, "BIRLESIK-TAZE-GURULTU", "surekli okunamayan dosya + ilgisiz degisiklik: hukum degismez", motor, k6, BIRLESIK_TABAN1, None)


def _v_taze_eksik(motor, taban, b, bozuk):
    """BIRLESIK-TAZE-EKSIK: bayat defterde YENI dosyanin cikaricisi KUSURLU (arac kusuru; `--kur` EKSIK defter yazardi) -> `ayni` atif
    `OLCULEMEDI [DEFTER_EKSIK]`, KESIN POZITIF (govdesi degisen atif) KORUNUR (ilgisiz dosyadaki arac kusuru alarmi silmez; sozdizimi
    hatasi DEGIL: o ATLANDI)."""
    kok = _b_damgali(motor, taban, "bir_taze_eksik", 3, "1. `ortak_ad` uc yerde.\n2. `tekil_ad` tek yerde.",
                     {"src/t.py": "def tekil_ad(x):\n    return x\n"})
    _b_commit(kok, {"src/p3.py": _b_py(30), "src/Q.cs": "public class Q\n{\n    public int Baska(int x) => x;\n}\n"},
              "p3 govdesi degisti + yeni C# dosya")
    kod, o, _e = _h20_kapi(bozuk, kok)
    h20 = _h20_satirlari_al(o)
    bekle = ["H20: 2 atif | 1 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_EKSIK:1] | 0 COKLU | 0 DAMGASIZ",
             "H20: md.1 `ortak_ad` [3 tanim] #%s -> #%s IDDIA KODDAN ESKI OLABILIR" % (
                 _bir_iz(_b_iz(1), _b_iz(2), _b_iz(3)), _bir_iz(_b_iz(1), _b_iz(2), _b_iz(30)))]
    if h20 != bekle:
        b.append(("BIRLESIK-TAZE-EKSIK", "yeni dosyanin cikaricisi arizali: pozitif KORUNUR + `ayni` -> `OLCULEMEDI [DEFTER_EKSIK:1]`: %r != %r" % (h20, bekle)))


def _v_taze_kaynak(motor, taban, b):
    """BIRLESIK-TAZE-KAYNAK: defter `git` kaynaklidir ama `kapi` `.git`siz bir KOPYADA kosar (evren `git ls-files` degil dosya sistemi):
    karsilastirma anlamsizdir -> `OLCULEMEDI [DEFTER_BAYATLIK]` (yeni dosya bu evrende gorunse de sahte `GOVDE DEGISTI` basilmaz)."""
    kok = _b_damgali(motor, taban, "bir_taze_kaynak", 3)
    _b_commit(kok, {"src/p4.py": _b_py(4)}, "yeni dosya")
    kopya = kok + "_gitsiz"
    shutil.copytree(kok, kopya, ignore=shutil.ignore_patterns(".git"))
    _h20_hukum_say(b, "BIRLESIK-TAZE-KAYNAK", ".git'siz kopya: evren defterinkinden farkli", motor, kopya,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 1 OLCULEMEDI [DEFTER_BAYATLIK:1] | 0 COKLU | 0 DAMGASIZ", None)


def _v_taze_sayim(motor, taban, b):
    """BIRLESIK-TAZE-SAYIM: DAMGASIZ/COKLU sayimi her zaman DEFTER indeksindendir (K1 hukmu; damgali atif VARLIGI sayimi degistirmez):
    damgasiz `ortak_ad` defterde 3 tanim (DAMGASIZ); yeni dosyada 3 tanim daha (taze kume 6 = COKLU olurdu) -> `1 DAMGASIZ`, `0 COKLU`."""
    kok = _hafiza_proje(motor, taban, "bir_taze_sayim", {"src/t.py": "def tekil_ad(x):\n    return x\n", "src/p1.py": _b_py(1),
                                                         "src/p2.py": _b_py(2), "src/p3.py": _b_py(3), "notlar.txt": "0\n"})
    kod, o, e = kos(motor, kok, "not", "--konu", "damgasiz-not", "--yeni-konu", "damgasiz", "--tur", "durum", "--metin", "1. `ortak_ad` damgasiz.")
    if kod != 0:
        raise Kurulamadi("damgasiz not basarisiz: %r" % (o + e)[-160:])
    kur(motor, kok)
    kos(motor, kok, *(DAMGA_NOT_ARGS + ("2. `tekil_ad` damgali.",)))
    _b_derle(motor, kok)
    _b_commit(kok, {"src/q1.py": _b_py(11), "src/q2.py": _b_py(12), "src/q3.py": _b_py(13)}, "3 tanim daha yeni dosyalarda")
    _h20_hukum_say(b, "BIRLESIK-TAZE-SAYIM", "sayim defterden: damgali atif VARKEN de 1 DAMGASIZ (COKLU DEGIL)", motor, kok,
                   "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 1 DAMGASIZ", None)


def _v_taze_not(motor, taban, b):
    """BIRLESIK-TAZE-NOT (P5.4 kabul vakasi): bayat defter + yeni dosyada aynı ad -> `not` TAZE kumeden `[4 tanim]` damgalar; hemen `kapi` sahte
    uyari VERMEZ (GOVDE DEGISTI 0). Ayrintisi P5-DAMGA kolunun DAMGA-TAZE vektorlerinde."""
    b4 = _bir_iz(*[_b_iz(i) for i in (1, 2, 3, 4)])
    kok = _b_damgali(motor, taban, "bir_taze_not", 3)
    _b_commit(kok, {"src/p4.py": _b_py(4)}, "4. tanim yeni dosyada")
    kod, o, e, govde, _ad = _not_kos(motor, kok, "2. `ortak_ad` yine.")
    if "ATIF DAMGALANDI: 1 (ortak_ad#%s [4 tanim])" % b4 not in o.split("\n"):
        b.append(("BIRLESIK-TAZE-NOT", "K1 bayat defterde H20'nin taze kumesiyle damgalar (`[4 tanim]`): %r" % o[-200:]))
    _b_derle(motor, kok)
    _h20_hukum_say(b, "BIRLESIK-TAZE-NOT", "not'tan hemen sonra kapi: sahte uyari YOK", motor, kok, BIRLESIK_TABAN1, None)


def kol_birlesik(motor, taban, bozuk, butcesiz, tarama_bozuk):
    """P5-BIRLESIK: `ortak_ad` 3 dosyada -> TEK birlesik damga `[3 tanim]` (BIRLESIK-VAR) · tekil ad izi defterdeki izle bayt-ayni
    (BIRLESIK-TEKIL) · SONUNCU tanim degisince H20 `GOVDE DEGISTI 1` + `[3 tanim] #eski -> #yeni` (BIRLESIK-DEGISTI) · ek / silinen
    tanim (BIRLESIK-EKLENDI) · dosya yeniden adlandirilinca iz DEGISMEZ (BIRLESIK-YOL) · aday dosya tasinmis + defter bayat: KISMI
    kumeden iz yok, `DEFTER_BAYAT` (BIRLESIK-BAYAT) · tavan 5: defter/canli/HEAD korumalari AYRI (BIRLESIK-TAVAN / BIRLESIK-COKLU)
    · aday dosya arizali -> kismi iz YOK (BIRLESIK-ARIZA) · eski tekil damga + kardes tanim (BIRLESIK-KARDES) · ozdes govdeler
    (BIRLESIK-OZDES) · `DOSYA_COK` etiketi (BIRLESIK-DOSYACOK) · K3 `<k> tanimdan <x>'u` + silinen (BIRLESIK-DOGUS /
    BIRLESIK-SILINEN)."""
    b = []
    vektorler = (
        (("BIRLESIK-VAR", "BIRLESIK-TEKIL"), lambda: _v_var(motor, taban, b)),
        (("BIRLESIK-DEGISTI",), lambda: _v_degisti(motor, taban, b)),
        (("BIRLESIK-EKLENDI",), lambda: _v_eklendi(motor, taban, b)),
        (("BIRLESIK-YOL",), lambda: _v_yol(motor, taban, b)),
        (("BIRLESIK-BAYAT",), lambda: _v_bayat(motor, taban, b)),
        (("BIRLESIK-TAVAN", "BIRLESIK-COKLU"), lambda: _v_tavan(motor, taban, b)),
        (("BIRLESIK-ARIZA",), lambda: _v_ariza(motor, taban, b, bozuk)),
        (("BIRLESIK-KARDES",), lambda: _v_kardes(motor, taban, b)),
        (("BIRLESIK-OZDES",), lambda: _v_ozdes(motor, taban, b)),
        (("BIRLESIK-DOSYACOK", "BIRLESIK-COKLU"), lambda: _v_dosyacok(motor, taban, b)),
        (("BIRLESIK-DOGUS",), lambda: _v_dogus(motor, taban, b)),
        (("BIRLESIK-SILINEN",), lambda: _v_silinen(motor, taban, b)),
        (("BIRLESIK-DOSYAYOK", "BIRLESIK-BAYAT"), lambda: _v_dosyayok(motor, taban, b)),
        (("BIRLESIK-CALISMA",), lambda: _v_calisma(motor, taban, b)),
        (("BIRLESIK-BUTCE",), lambda: _v_butce(motor, taban, b, butcesiz)),
        (("BIRLESIK-KAP",), lambda: _v_kap(motor, taban, b)),
        (("BIRLESIK-ATLANDI",), lambda: _v_atlandi(motor, taban, b)),
        (("BIRLESIK-NESNE", "BIRLESIK-CIKARICI", "BIRLESIK-YOLKACIS"), lambda: _v_nesne(motor, taban, b)),
        (("BIRLESIK-YOLCOKLU", "BIRLESIK-SAYISIZ"), lambda: _v_kucukler(motor, taban, b)),
        (("BIRLESIK-TAZE",), lambda: _v_taze(motor, taban, b)),
        (("BIRLESIK-TAZE-TEKIL",), lambda: _v_taze_tekil(motor, taban, b)),
        (("BIRLESIK-TAZE-AD",), lambda: _v_taze_ad(motor, taban, b)),
        (("BIRLESIK-TAZE-SILINEN",), lambda: _v_taze_silinen(motor, taban, b)),
        (("BIRLESIK-TAZE-TAVAN",), lambda: _v_taze_tavan(motor, taban, b)),
        (("BIRLESIK-TAZE-BAYT",), lambda: _v_taze_bayt(motor, taban, b)),
        (("BIRLESIK-TAZE-YOL",), lambda: _v_taze_yol(motor, taban, b)),
        (("BIRLESIK-TAZE-YAZMA",), lambda: _v_taze_yazma(motor, taban, b)),
        (("BIRLESIK-TAZE-ARIZA",), lambda: _v_taze_ariza(motor, taban, b, tarama_bozuk)),
        (("BIRLESIK-TAZE-KAPSAM", "BIRLESIK-TAZE-GURULTU", "BIRLESIK-TAZE-OKUNMAZ"), lambda: _v_taze_kapsam(motor, taban, b)),
        (("BIRLESIK-TAZE-EKSIK",), lambda: _v_taze_eksik(motor, taban, b, bozuk)),
        (("BIRLESIK-TAZE-KAYNAK",), lambda: _v_taze_kaynak(motor, taban, b)),
        (("BIRLESIK-TAZE-SAYIM",), lambda: _v_taze_sayim(motor, taban, b)),
        (("BIRLESIK-TAZE-NOT",), lambda: _v_taze_not(motor, taban, b)),
    )
    for etiketler, calistir in vektorler:
        if _calissin(*etiketler):
            calistir()
    return b


def kos_birlesik(motor, taban, ad, kaynak):
    anc = "_DOGUS_BUTCE = 15 "
    if kaynak.count(anc) != 1:
        raise Kurulamadi("butce capasi %d yerde gecti (1 olmali)" % kaynak.count(anc))
    butcesiz, hata = _motor_yaz(kaynak.replace(anc, "_DOGUS_BUTCE = 0 ", 1), os.path.join(os.path.dirname(taban), "butcesiz_" + ad), "butcesiz_" + ad)
    if butcesiz is None:
        raise Kurulamadi(hata)
    anc2 = '            return _adres_bugun(kok, ozet, None, '      # ONEK capa: M-U64 son argumani degistirir
    if kaynak.count(anc2) != 1:
        raise Kurulamadi("bayatlik olcumu capasi %d yerde gecti (1 olmali)" % kaynak.count(anc2))
    tarama, hata = _motor_yaz(kaynak.replace(anc2, '            oldur("ENJEKSIYON: git ls-files BASARISIZ (bayatlik olcumu arizasi)", 3)\n' + anc2, 1),
                              os.path.join(os.path.dirname(taban), "tarama_" + ad), "tarama_" + ad)
    if tarama is None:
        raise Kurulamadi(hata)
    return kol_birlesik(motor, taban, _bozuk_motor(taban, "bir_" + ad, kaynak), butcesiz, tarama)


# ------------------------------------------------------------------ P5-SABIT (P5.2 KALEM 5): dil sabitleri aday DEGIL
# Liste (README'de ACIK): true false null None True False nil this self void undefined — backtick'li olsa da tanimlayici adayi SAYILMAZ
# (`ATIF COZULEMEDI: true` gurultusu biter). Listede OLMAYAN her cozulemeyen ad (`trueValue`, `TRUE`: tam eslesme, buyuk/kucuk harf
# AYNEN) bugunku gibi COZULEMEDI der. `void` bu fiksturde TANIMLI bir islev: sabit olarak dislanir (cozulebilse de damga/sayim YOK).
SABIT_PY = "def void(x):\n    return x\n"
SABIT_METIN = "\n".join((
    "1. `true` `false` `null` `None` `True` `False` `this` `self` `void` `undefined` `nil` sabit.",
    "2. `trueValue` tanimsiz; `TRUE` listede degil; `Nonexistent` yok.",
))
SABIT_COZULEMEDI = ["ATIF COZULEMEDI: Nonexistent", "ATIF COZULEMEDI: TRUE", "ATIF COZULEMEDI: trueValue"]
SABIT_DESEN = re.compile(r"\b(?:true|false|null|None|True|False|this|self|void|undefined|nil)\b")


def kol_sabit(motor, taban):
    """P5-SABIT: dil sabitleri (`true false null None True False nil this self void undefined`) backtick'li olsa da aday DEGIL: satir
    YOK, damga YOK, H20 sayimi YOK — TANIMLI bir ad (`void`) olsa bile (SABIT-VAR) · listede OLMAYAN ad (`trueValue`, `TRUE`:
    tam eslesme, buyuk/kucuk harf AYNEN) bugunku gibi COZULEMEDI der (SABIT-TAM) · sabit canli defterde H20'yi ATESLEMEZ (SABIT-H20)."""
    b = []
    kok = _hafiza_proje(motor, taban, "sabit", {"src/v.py": SABIT_PY})
    kur(motor, kok)
    kod, o, e, govde, _ad = _not_kos(motor, kok, SABIT_METIN)
    sat = _atif_satirlari(o)
    if kod != 0 or govde != SABIT_METIN:
        b.append(("SABIT-VAR", "sabitler damgalanmamali / metin AYNI kalmali: exit=%s govde=%r cikti=%r" % (kod, govde, o[-200:])))
    if any(SABIT_DESEN.search(l) for l in sat):
        b.append(("SABIT-VAR", "dil sabiti icin `not` satiri uretildi: %r" % sat))
    if sat != SABIT_COZULEMEDI:
        b.append(("SABIT-TAM", "listede OLMAYAN adlar COZULEMEDI demeli (beklenen %r): %r" % (SABIT_COZULEMEDI, sat)))
    kd, od, ed = kos(motor, kok, "derle")
    if kd != 0 or "`void`" not in io.open(os.path.join(kok, "PROJE_HAFIZA.md"), encoding="utf-8", newline="").read():
        raise Kurulamadi("SABIT-H20 duzenegi: derle exit=%s ya da `void` canliya girmedi: %r" % (kd, (od + ed)[-160:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "sabit")
    kod, o, e = kos(motor, kok, "kapi")
    if _h20_satirlari_al(o):
        b.append(("SABIT-H20", "dil sabitleri H20'yi atesledi (sayilmamali): %r" % _h20_satirlari_al(o)))
    # DAMGALI sabit adli belirtec (eski `None`#hex: C# enum uyesi) GIZLENMEZ: damga acik bir isarettir
    ms = _hafiza_proje(motor, taban, "sabit_damgali", {"src/Mode.cs": "public enum Mode\n{\n    None,\n    Read\n}\n"})
    kur(motor, ms)
    kos(motor, ms, *(DAMGA_NOT_ARGS + ("1. `None`#816e08d4 eski damga.",)))
    kos(motor, ms, "derle")
    kod, o, e = kos(motor, ms, "kapi")
    if not any(l.startswith("H20: 1 atif | ") for l in _h20_satirlari_al(o)):
        b.append(("SABIT-DAMGALI", "damgali sabit adli belirtec H20'den gizlendi (`1 atif` beklenir): %r" % _h20_satirlari_al(o)))
    return b


def kos_sabit(motor, taban, _ad, _kaynak):
    return kol_sabit(motor, taban)


# ------------------------------------------------------------------ P5-SAYIM (P5.2 KALEM 6): damgasiz belirtec arac kusurunda DUSMEZ
# Degismez (defter TAMAMKEN, numarali madde ici COZULEBILIR aday belirtecler): damgali · COKLU · DAMGASIZ · damgasiz-OLCULEMEDI toplami arac
# kusuru enjeksiyonuyla AZALMAZ; yalniz saglamken `yok` olanlar (kod adresi olmayan satira bakan `yol:N`) kadar ARTABILIR — kusur `yok`
# hukmunu veremez. Sinif, `not`ta basilan K1 hukmuyle (`_damga_karar`) AYNI karardan gelir (ad belirteci de arizada OLCULEMEDI'dir).
SAYIM_ONCE = "\n".join((
    "3. `ikinci_islev` damgasiz.",
    "4. `a.py:6` damgasiz yol.",
    "5. `a.py:11` damgasiz yol 2.",
))
SAYIM_YOK = "6. `a.py:3` bos satir (hicbir tanimda DEGIL)."
SAYIM_SAGLAM = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 3 DAMGASIZ"
SAYIM_ARIZALI = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 4 OLCULEMEDI (damgali 1, damgasiz 3) [CIKARICI:4] | 0 COKLU | 0 DAMGASIZ"
SAYIM_YOK_SAGLAM = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 3 DAMGASIZ"
SAYIM_YOK_ARIZALI = "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 5 OLCULEMEDI (damgali 1, damgasiz 4) [CIKARICI:5] | 0 COKLU | 0 DAMGASIZ"


def _h20_sinif_toplami(satir):
    """H20 ozet satiri -> damgali + COKLU + DAMGASIZ + damgasiz-OLCULEMEDI (siniflarin toplami; ayrim yoksa OLCULEMEDI hep damgali)."""
    m = re.match(r"H20: (\d+) atif \| \d+ GOVDE DEGISTI \| \d+ SEMBOL YOK \| \d+ OLCULEMEDI(?: \(damgali \d+, damgasiz (\d+)\))?(?: \[[^\]]*\])? "
                 r"\| (\d+) COKLU \| (\d+) DAMGASIZ$", satir)
    if not m:
        return None
    a, ou, c, z = m.groups()
    return int(a) + int(c) + int(z) + int(ou or 0)


def _sayim_proje(motor, taban, ad, metin_once, dosyalar=None):
    """Damgasiz notlar (defter YOKKEN) + `adres --kur` + damgali not + derle + commit -> kok."""
    kok = _hafiza_proje(motor, taban, ad, dosyalar or {"src/a.py": H20_A})
    kod, o, e = kos(motor, kok, "not", "--konu", "damgasiz-not", "--yeni-konu", "SAYIM fiksturu: damgasiz belirtec", "--tur", "durum",
                    "--metin", metin_once)
    if kod != 0:
        raise Kurulamadi("damgasiz not basarisiz: %r" % (o + e)[-160:])
    kur(motor, kok)
    kod, o, e = kos(motor, kok, *(DAMGA_NOT_ARGS + ("1. `tekil_islev` ilk iddia.",)))
    kod, o2, e = kos(motor, kok, "derle")
    if kod != 0:
        raise Kurulamadi("derle basarisiz: exit=%s %r" % (kod, (o2 + e)[-200:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "sayim")
    return kok


def _sayim_karsilastir(b, etiket_toplam, kok, motor, bozuk, saglam_bekle, arizali_bekle, artis):
    """Saglam ve arizali motorda H20 ozeti: literaller + siniflarin toplami (`artis`: arizada beklenen +n) + H20 DISI satirlar/exit ayni."""
    kod0, o0, _e0 = _h20_kapi(motor, kok)
    h0 = _h20_satirlari_al(o0)
    if h0 != [saglam_bekle]:
        b.append(("SAYIM-ENJEKSIYON", "saglam motor: H20 satirlari %r != [%r]" % (h0, saglam_bekle)))
    kod, o, e = _h20_kapi(bozuk, kok)
    h1 = _h20_satirlari_al(o)
    if h1[:1] != [arizali_bekle]:
        b.append(("SAYIM-ENJEKSIYON", "cikarici arizali motor: H20 ozeti %r != %r" % (h1[:1], arizali_bekle)))
    t0, t1 = (_h20_sinif_toplami(h0[0]) if h0 else None), (_h20_sinif_toplami(h1[0]) if h1 else None)
    if t0 is None or t1 is None or t1 != t0 + artis:
        b.append((etiket_toplam, "siniflarin toplami: saglam=%s arizali=%s (arizada +%d beklenir; AZALMAMALI)" % (t0, t1, artis)))
    if kod != kod0 or _kapi_diger(o) != _kapi_diger(o0):
        b.append(("SAYIM-ENJEKSIYON", "H20 disindaki `kapi` satirlari / exit degisti: exit %s -> %s" % (kod0, kod)))
    return h1


def kol_sayim(motor, taban, bozuk):
    """P5-SAYIM: saglam motorda damgasiz cozulebilir belirtecler DAMGASIZ; cikarici arizali motorda ad belirteci de `yol:N` de OLCULEMEDI'ye
    gecer, `(damgali X, damgasiz Y)` ayrimi gorunur (SAYIM-ENJEKSIYON / SAYIM-AYRIM / SAYIM-AD) · siniflarin TOPLAMI enjeksiyonla
    AZALMAZ (SAYIM-TOPLAM) · yalniz saglamken `yok` olan belirtec kadar ARTAR (SAYIM-YOK) · asiri yuklu `yol:N` K1'de oldugu gibi COKLU
    (SAYIM-COKLU)."""
    b = []
    if _calissin("SAYIM-ENJEKSIYON", "SAYIM-TOPLAM", "SAYIM-AYRIM", "SAYIM-AD"):
        kok = _sayim_proje(motor, taban, "sayim", SAYIM_ONCE)
        h1 = _sayim_karsilastir(b, "SAYIM-TOPLAM", kok, motor, bozuk, SAYIM_SAGLAM, SAYIM_ARIZALI, 0)
        if h1[:1] and "(damgali 1, damgasiz 3)" not in h1[0]:
            b.append(("SAYIM-AYRIM", "OLCULEMEDI satirinda damgali/damgasiz ayrimi gorunmuyor: %r" % h1[:1]))
        if h1[:1] and "| 0 DAMGASIZ" not in h1[0]:
            b.append(("SAYIM-AD", "ARIZADA tek bir damgasiz belirtec (ad dahil) DAMGASIZ kalmamali: %r" % h1[:1]))
    if _calissin("SAYIM-SAF"):
        ks = _hafiza_proje(motor, taban, "sayim_saf", {"src/a.py": H20_A})
        kod, o, e = kos(motor, ks, "not", "--konu", "damgasiz-not", "--yeni-konu", "SAYIM fiksturu: yalniz damgasiz", "--tur", "durum",
                        "--metin", SAYIM_ONCE)
        kur(motor, ks)
        kd, od, ed = kos(motor, ks, "derle")
        if kod != 0 or kd != 0:
            raise Kurulamadi("SAYIM-SAF duzenegi: not exit=%s derle exit=%s" % (kod, kd))
        _git(ks, "add", "-A")
        _git(ks, "commit", "-q", "-m", "saf")
        kod0, o0, _e0 = _h20_kapi(motor, ks)
        h0 = _h20_satirlari_al(o0)
        kod1, o1, _e1 = _h20_kapi(bozuk, ks)
        h1 = _h20_satirlari_al(o1)
        if h0 != ["H20: 0 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 0 COKLU | 3 DAMGASIZ"]:
            b.append(("SAYIM-SAF", "damgali atif YOK, saglam motor: `3 DAMGASIZ` beklenir: %r" % h0))
        if h1 != ["H20: 0 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 3 OLCULEMEDI (damgali 0, damgasiz 3) [CIKARICI:3] | 0 COKLU | 0 DAMGASIZ"]:
            b.append(("SAYIM-SAF", "damgali atif YOK, cikarici arizali: damgasiz belirtecler OLCULEMEDI olarak GORUNMELI (sessizce dusmemeli): %r" % h1))
    if _calissin("SAYIM-YOK"):
        ky = _sayim_proje(motor, taban, "sayim_yok", SAYIM_ONCE + "\n" + SAYIM_YOK)
        _sayim_karsilastir(b, "SAYIM-YOK", ky, motor, bozuk, SAYIM_YOK_SAGLAM, SAYIM_YOK_ARIZALI, 1)
    if _calissin("SAYIM-COKLU"):
        kc = _hafiza_proje(motor, taban, "sayim_coklu", {"src/Hesap.cs": DAMGA_CS, "src/a.py": H20_A})
        kod, o, e = kos(motor, kc, "not", "--konu", "damgasiz-not", "--yeni-konu", "SAYIM fiksturu: asiri yuk", "--tur", "durum",
                        "--metin", "1. `Hesap.cs:3` asiri yuklu.")
        kur(motor, kc)
        kos(motor, kc, *(DAMGA_NOT_ARGS + ("2. `tekil_islev` ilk iddia.",)))
        kos(motor, kc, "derle")
        _git(kc, "add", "-A")
        _git(kc, "commit", "-q", "-m", "sayim")
        _h20_hukum_say(b, "SAYIM-COKLU", "asiri yuklu `yol:N` (K1'de COKLU) H20'de de COKLU", motor, kc,
                       "H20: 1 atif | 0 GOVDE DEGISTI | 0 SEMBOL YOK | 0 OLCULEMEDI | 1 COKLU | 0 DAMGASIZ", None)
    return b


def kos_sayim(motor, taban, ad, kaynak):
    bozuk, hata = _bozuk_motor_yaz(kaynak, os.path.join(os.path.dirname(taban), "sayim_bozuk_" + ad), "sayim_bozuk_" + ad)
    if bozuk is None:
        raise Kurulamadi(hata)
    return kol_sayim(motor, taban, bozuk)


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
    "P5-H20": kos_h20,
    "P5-DOGUS": kos_dogus,
    "P5-BIRLESIK": kos_birlesik,
    "P5-SABIT": kos_sabit,
    "P5-SAYIM": kos_sayim,
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
     "    kod = _adres_yol_ayir(yollar)[0]\n",
     "    kod = dict((d, []) for d in _ADRES_DIL_SIRA)      # MUTANT: sorgu suzgeci yok\n"
     "    for y in yollar:\n"
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
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != ozet\n',
     "    bayat = False      # MUTANT\n"),
    ("M-B2 agac ozeti HER ZAMAN farkli (degismeyen agac bayat sanilir)", "A-BAYAT", "BAYAT-YOK",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != ozet\n',
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
    ("M-D2 BIRLESIK kural YOK (ayni ad 2+ tanimda COKLU: eski K1 davranisi, damga yok)", "P5-DAMGA", "DAMGA-IKILI",
     '        return ("birlesik", tuple(sorted(set(a))), None) if len(a) <= _BIRLESIK_TAVAN else ("coklu", len(a), None)\n',
     '        return ("tek", a[0][0], a[0][1]) if len(a) == 1 else ("coklu", len(a), None)      # MUTANT\n'),
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
    ("M-H0 H20 `kapi`ya BAGLANMAZ (`_kapi_uyarilar` yalniz H18)", "P5-H20", "H20-AYNI",
     "    _kapi_h20(N, kok, y)\n",
     "    pass      # MUTANT\n"),
    ("M-H1 karsilastirma SABIT (ad: govde degisse de `ayni`)", "P5-H20", "H20-DEGISTI",
     '    if iz == damga[1:]:\n        return "ayni", None\n',
     '    if True:      # MUTANT\n        return "ayni", None\n'),
    ("M-H2 parmak izi DOSYA GENELI (satir kaymasi / komsu sembol govde degisti sayilir)", "P5-H20", "H20-KAYMA",
     '    return [(r[2], r[3], r[4], r[5]) for r in satirlar if r[1] != "dosya"], None\n',
     '    return [(r[2], r[3], r[4], _adres_sha(metin)[:8]) for r in satirlar if r[1] != "dosya"], None      # MUTANT\n'),
    ("M-H3 H20 istisnasi `kapi`ya SIZAR (yakalama dar)", "P5-H20", "H20-ISTISNA",
     "    except (Exception, SystemExit) as e:  # noqa: BLE001 - KISIT 6-3: H20",
     "    except KeyError as e:  # noqa: BLE001 - KISIT 6-3: H20"),
    ("M-H4 DAMGASIZ sayilmaz (gizlenir)", "P5-H20", "H20-DAMGASIZ",
     '            z += sinif == "damgasiz"\n',
     "            z += 0      # MUTANT\n"),
    ("M-H5 silinen sembol `ayni` sayilir (SEMBOL YOK ayrimi yok)", "P5-H20", "H20-YOK",
     '        return ("olculemedi", v) if sonuc == "olculemedi" else ("yok", None)\n',
     '        return ("olculemedi", v) if sonuc == "olculemedi" else ("ayni", None)      # MUTANT\n'),
    ("M-H6 defter yokken damgali atif SESSIZ (OLCULEMEDI gizlenir)", "P5-H20", "H20-DEFTER",
     '        return _h20_satirlari(a, [], [], {"DEFTER_" + durum.upper(): a} if a else {}, {}, 0, 0)\n',
     "        return []      # MUTANT\n"),
    ("M-H7 bos H20 de basilir (atifsiz projede gurultu: kapi ciktisi DEGISIR)", "P5-H20", "H20-SESSIZ",
     "    if not a and not z and not c and not olu:\n        return []\n",
     "    if False:      # MUTANT\n        return []\n"),
    ("M-H8 yalniz MADDE icindeki damgali atif okunur (numarasiz satirdaki damga GIZLENIR)", "P5-H20", "H20-SATIR",
     "    return [(madde.get(i), i + 1, m, t, d) for i, s in enumerate(L) if not ic[i] for (_son, m, t, d, _o) in _damga_jetonlar(s)]\n",
     "    return [(madde.get(i), i + 1, m, t, d) for i, s in enumerate(L) if not ic[i] and i in madde for (_son, m, t, d, _o) in _damga_jetonlar(s)]      # MUTANT\n"),
    ("M-H9 ekran tavani YOK (liste kirpilmaz: HEPSI basilir)", "P5-H20", "H20-TAVAN",
     "    cikti += ayrinti[:_H20_LISTE_TAVAN]\n",
     "    cikti += ayrinti      # MUTANT\n"),
    ("M-H10 kod citi icindeki damgali belirtec de sayilir", "P5-H20", "H20-CIT",
     "    return [(madde.get(i), i + 1, m, t, d) for i, s in enumerate(L) if not ic[i] for (_son, m, t, d, _o) in _damga_jetonlar(s)]\n",
     "    return [(madde.get(i), i + 1, m, t, d) for i, s in enumerate(L) for (_son, m, t, d, _o) in _damga_jetonlar(s)]      # MUTANT\n"),
    ("M-H11 SEMBOL YOK defter kapsami EKSIKKEN de hukum verilir (ATLANDI ayrimi yok)", "P5-H20", "H20-ATLANDI",
     '        if h == "yok" and not hukum[2]:\n',
     '        if False:      # MUTANT\n'),
    ("M-H12 EKSIK defter H20'de kullanilir (cikarici kusuru gizlenir)", "P5-H20", "H20-EKSIK",
     '    if _adres_eksik_mi(veri[0]):\n        return "eksik", "adres defteri EKSIK (cikarici kusuru) - hafiza.py adres --kur"\n',
     '    if False:      # MUTANT\n        return "eksik", "adres defteri EKSIK (cikarici kusuru) - hafiza.py adres --kur"\n'),
    ("M-H13 `yol:N` damga dosyada ARANMAZ (satir kaymasi govde degisti sayilir)", "P5-H20", "H20-YOL",
     '    if any(iz == damga[1:] for _t, _b, _e, iz in satirlar):\n        return "ayni", None\n',
     "    if False:      # MUTANT\n        return \"ayni\", None\n"),
    ("M-G1 N=0 (pencere YOK: uyari hic cikmaz)", "P5-DOGUS", "DOGUS-VAR",
     "_DOGUS_N = 5 ",
     "_DOGUS_N = 0 "),
    ("M-G2 N=100 (pencere SINIRSIZ: 5-6 commit once de uyarir)", "P5-DOGUS", "DOGUS-SINIR",
     "_DOGUS_N = 5 ",
     "_DOGUS_N = 100 "),
    ("M-G3 k YANLIS (+1 commit once)", "P5-DOGUS", "DOGUS-VAR",
     'else "%d commit once degisti" % k\n',
     'else "%d commit once degisti" % (k + 1)\n'),
    ("M-G4 yanlis commit'in sha'si (degisikligi getireninkine DEGIL, bir oncekinin)", "P5-DOGUS", "DOGUS-VAR",
     "_dogus_ne(esit), shalar[esit][:7])]",
     "_dogus_ne(esit), shalar[esit + 1][:7])]"),
    ("M-G5 commit'lenmemis degisiklik uyarisi YOK", "P5-DOGUS", "DOGUS-COMMITSIZ",
     "    if any(sorted(calisma[y][0].get(tam, ())) != sorted(kume[i][0].elements()) for i, (y, tam) in enumerate(gruplar)):\n",
     "    if False:      # MUTANT\n"),
    ("M-G6 git'siz proje SESSIZ (depo degil: OLCULEMEDI gizlenir)", "P5-DOGUS", "DOGUS-GITSIZ",
     '    if r.returncode != 0 or r.stdout.strip() != b"true":\n',
     "    if False:      # MUTANT\n"),
    ("M-G7 sig gecmis SESSIZ (kisa gecmis 'degismedi' sanilir)", "P5-DOGUS", "DOGUS-SIG",
     '        if s.returncode == 0 and s.stdout.strip() == b"true":\n',
     "        if False:      # MUTANT\n"),
    ("M-G8 dogusta bayat istisnasi `not`a SIZAR (yakalama dar)", "P5-DOGUS", "DOGUS-ISTISNA",
     "    except (Exception, SystemExit) as e:  # noqa: BLE001 - KISIT 6-3: dogusta bayat",
     "    except KeyError as e:  # noqa: BLE001 - KISIT 6-3: dogusta bayat"),
    ("M-G9 first-parent YOK (birlestirme gecmisi tarih sirasiyla gezilir: k/sha kayar)", "P5-DOGUS", "DOGUS-MERGE",
     '    r = _dogus_git(kok, "rev-list", "--first-parent", "-n", str(_DOGUS_N + 1), "HEAD", "--")\n',
     '    r = _dogus_git(kok, "rev-list", "-n", str(_DOGUS_N + 1), "HEAD", "--")      # MUTANT\n'),
    ("M-G10 git yolu depo KOKUNE gore (`--show-prefix` onegi YOK: alt dizin projesinde dosya `yok` sanilir)", "P5-DOGUS", "DOGUS-ALTDIZIN",
     '    return "%s:%s%s\\n" % (sha, onek, yol)\n',
     '    return "%s:%s\\n" % (sha, yol)      # MUTANT\n'),
    ("M-G11 20 dosya tavani SESSIZ kirpar (OLCULEMEDI beyani yok)", "P5-DOGUS", "DOGUS-TAVAN",
     "    if len(dosyalar) > _DOGUS_DOSYA_TAVAN:\n",
     "    if False:      # MUTANT\n"),
    ("M-G13 EN YAKIN degisim aranmaz: ardisik surumler karsilastirilir ve EN UZAK degisim bildirilir", "P5-DOGUS", "DOGUS-YAKIN",
     "            if g[k] != g[k + 1] and (esit is None or k < esit):\n",
     "            if g[k] != g[k + 1]:      # MUTANT\n"),
    ("M-U1 birlesik iz yerine yalniz ILK tanimin izi (sonraki tanim degisince H20 sessiz)", "P5-BIRLESIK", "BIRLESIK-DEGISTI",
     '    return izler[0] if len(izler) == 1 else _adres_sha("\\n".join(sorted(izler)))[:8]\n',
     "    return izler[0]      # MUTANT\n"),
    ("M-U2 birlesik izde `sorted` YOK (iz dosya yolu sirasina baglanir: dosya adi degisince iz degisir)", "P5-BIRLESIK", "BIRLESIK-YOL",
     '_adres_sha("\\n".join(sorted(izler)))[:8]',
     '_adres_sha("\\n".join(izler))[:8]'),
    ("M-U3 tanim tavani YOK (6+ tanim da damgalanir)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     "_BIRLESIK_TAVAN = 5 ",
     "_BIRLESIK_TAVAN = 50 "),
    ("M-U4 COKLU H20 ozetinde SAYILMAZ (6+ tanimli ad gorunmez)", "P5-BIRLESIK", "BIRLESIK-COKLU",
     '            c += sinif == "coklu"\n',
     "            c += 0      # MUTANT\n"),
    ("M-U5 H20 defter-satiri tavani YOK (defter 6 satir / canli 5: COKLU_TAVAN yerine DEFTER_BAYAT)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     '    if len(satirlar_) > _BIRLESIK_TAVAN:\n        return "olculemedi", "COKLU_TAVAN"\n',
     '    if False:      # MUTANT\n        return "olculemedi", "COKLU_TAVAN"\n'),
    ("M-U6 H20 canli-tanim tavani YOK (bugun 6 tanim: COKLU_TAVAN yerine GOVDE DEGISTI)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     '    if len(v) > _BIRLESIK_TAVAN:\n        return "olculemedi", "COKLU_TAVAN"\n',
     '    if False:      # MUTANT\n        return "olculemedi", "COKLU_TAVAN"\n'),
    ("M-U7 K1 defter-satiri tavani YOK (defter 6 satir / canli 5: COKLU yerine DEFTER_BAYAT)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     '        return ("birlesik", tuple(sorted(set(a))), None) if len(a) <= _BIRLESIK_TAVAN else ("coklu", len(a), None)\n',
     '        return ("birlesik", tuple(sorted(set(a))), None)      # MUTANT\n'),
    ("M-U8 K1 canli-tanim tavani YOK (canli 6 tanim damgalanir)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     '    return ("damga", _birlesik_iz(v), len(v)) if len(v) <= _BIRLESIK_TAVAN else ("coklu", len(v), 0)\n',
     '    return "damga", _birlesik_iz(v), len(v)      # MUTANT\n'),
    ("M-U9 K3 K1'in COKLU hukmunu (canli 6 tanim) yok sayar (6 tanim taranir: `6 tanimdan x'u`)", "P5-BIRLESIK", "BIRLESIK-COKLU",
     '        elif c[0] in ("tek", "birlesik") and k[0] == "coklu" and t == "ad":\n            coklu.append(m)\n',
     '        elif False:      # MUTANT\n            coklu.append(m)\n'),
    ("M-U10 aday dosya kusuru yutulur (KISMI kumeden damga ya da DEFTER_BAYAT yazilir: arac kusuru gorunmez)", "P5-BIRLESIK", "BIRLESIK-ARIZA",
     '        hata = hata or (sebep if d is None and sebep != "DOSYA_YOK" else None)\n',
     "        pass      # MUTANT\n"),
    ("M-U11 kismi aday kaybi yutulur (tasinmis dosya + bayat defter: KISMI kumeden damga / GOVDE DEGISTI)", "P5-BIRLESIK", "BIRLESIK-BAYAT",
     '    return ("olculemedi", "DEFTER_BAYAT") if kayip else ("tamam", izler)\n',
     '    return "tamam", izler      # MUTANT\n'),
    ("M-U13 K3 yalniz ILK tanimi tarar (diger tanimlarin degisimi gorunmez)", "P5-BIRLESIK", "BIRLESIK-DOGUS",
     "            sembol.append((m, t, list(c[1])))\n",
     "            sembol.append((m, t, list(c[1])[:1]))      # MUTANT\n"),
    ("M-U14 K3 degisen tanim sayisi HEPSI sayilir (`3 tanimdan 3'u` ama yalniz 1'i degisti)", "P5-BIRLESIK", "BIRLESIK-DOGUS",
     "    return esit, (min(dagilim) if dagilim else None), x, s, dagilim, toplam\n",
     "    return esit, (min(dagilim) if dagilim else None), (toplam if x else 0), s, dagilim, toplam      # MUTANT\n"),
    ("M-U15 K3 en yakin commit yerine EN UZAK degisim (sirali son tanimin commit'i)", "P5-BIRLESIK", "BIRLESIK-DOGUS",
     "    return esit, (min(dagilim) if dagilim else None), x, s, dagilim, toplam\n",
     "    return esit, (max(dagilim) if dagilim else None), x, s, dagilim, toplam      # MUTANT\n"),
    ("M-U16 K3 yas notu YOK (`(en yakin; n tanim daha eski)` yazilmaz: sayi tek commit'e ait sanilir)", "P5-BIRLESIK", "BIRLESIK-DOGUS",
     '(" (en yakin; %d tanim daha eski)" % (x - dagilim[degisim]) if dagilim[degisim] < x else "")',
     '""'),
    ("M-U17 sayi eki tablosu hep `i` (`3'u` -> `3'i`, `2'si` -> `2'i`)", "P5-BIRLESIK", "BIRLESIK-DOGUS",
     '_BIRLESIK_EK = {1: "i", 2: "si", 3: "u", 4: "u", 5: "i"}',
     '_BIRLESIK_EK = {1: "i", 2: "i", 3: "i", 4: "i", 5: "i"}'),
    ("M-U18 K3 TEK tanimda silinen/eklenen gorulmez (eski ardisik-farklilik kurali yerine kesisim)", "P5-BIRLESIK", "BIRLESIK-SILINEN",
     '        return ["DIKKAT: %s govdesi %s (%s) - iddiayi kodla teyit et" % (m, _dogus_ne(esit), shalar[esit][:7])] if esit is not None else []\n',
     '        return ["DIKKAT: %s govdesi %s (%s) - iddiayi kodla teyit et" % (m, _dogus_ne(degisim), shalar[degisim][:7])] if degisim is not None else []      # MUTANT\n'),
    ("M-U19 K3 2+ tanimda silinen tanim bildirilmez", "P5-BIRLESIK", "BIRLESIK-SILINEN",
     "    if s:\n        return [",
     "    if False:      # MUTANT\n        return ["),
    ("M-U20 `ATIF DAMGALANDI` satirinda `[k tanim]` YOK (birlesik izin kac tanimdan geldigi gorunmez)", "P5-BIRLESIK", "BIRLESIK-VAR",
     '" [%d tanim]" % karar[(m, t)][2] if karar[(m, t)][2] > 1 else ""',
     '""'),
    ("M-U21 TEK tanimda da birlesik hash (K1 damgalariyla geri uyum bozulur)", "P5-BIRLESIK", "BIRLESIK-TEKIL",
     '    return izler[0] if len(izler) == 1 else _adres_sha("\\n".join(sorted(izler)))[:8]\n',
     '    return _adres_sha("\\n".join(sorted(izler)))[:8]      # MUTANT\n'),
    ("M-U22 dosya YOLU birlesik ize girer (dosya adi degisince iz degisir)", "P5-BIRLESIK", "BIRLESIK-YOL",
     "            izler += a\n",
     '            izler += [(yol + ":" + i_) if len(adaylar) > 1 else i_ for i_ in a]      # MUTANT\n'),
    ("M-U23 H20 ayrinti satirinda `[k tanim]` YOK", "P5-BIRLESIK", "BIRLESIK-DEGISTI",
     '" [%d tanim]" % yeni[1] if yeni[1] > 1 else ""',
     '""'),
    ("M-U24 6+ tanimli ad icin K3 `OLCULEMEDI (<ad> COKLU)` beyani YOK", "P5-BIRLESIK", "BIRLESIK-COKLU",
     '        elif c[0] == "coklu" and t == "ad":\n            coklu.append(m)\n',
     "        elif False:      # MUTANT\n            coklu.append(m)\n"),
    ("M-U25 `TANIM SAYISI DEGISTI` etiketi YOK (eski tekil damga + kardes tanim: govdenin durdugu gorunmez)", "P5-BIRLESIK", "BIRLESIK-KARDES",
     '" TANIM SAYISI DEGISTI (damgali govde duruyor) -" if yeni[2] else ""',
     '""'),
    ("M-U26 ozdes govdeler tekillestirilir (`set`: COKLU KUME degil)", "P5-BIRLESIK", "BIRLESIK-OZDES",
     '_adres_sha("\\n".join(sorted(izler)))[:8]',
     '_adres_sha("\\n".join(sorted(set(izler))))[:8]'),
    ("M-U27 `yol:N` sonek cokluguna `COKLU` sebebi (H20 `COKLU` alaniyla ayni kelime)", "P5-BIRLESIK", "BIRLESIK-DOSYACOK",
     '        return ("olculemedi", "DOSYA_COK") if dosya else ("yok", None)\n',
     '        return ("olculemedi", "COKLU") if dosya else ("yok", None)      # MUTANT\n'),
    ("M-U28 `yol:N` COKLU'su da `tavan 5` metniyle basilir (tavan ile ilgisi yok)", "P5-BIRLESIK", "BIRLESIK-COKLU",
     "_BIRLESIK_TAVAN) if tur == \"ad\"\n",
     "_BIRLESIK_TAVAN) if True      # MUTANT\n"),
    ("M-S1 dil sabiti listesi BOS (sabitler aday: `true` COZULEMEDI gurultusu, tanimli `void` damgalanir)", "P5-SABIT", "SABIT-VAR",
     '_DAMGA_SABIT = frozenset(("true", "false", "null", "None", "True", "False", "nil", "this", "self", "void", "undefined"))\n',
     "_DAMGA_SABIT = frozenset()      # MUTANT\n"),
    ("M-S2 sabit listesi ALT DIZE eslesmesiyle genisler (`trueValue` de yutulur: her sey sabit)", "P5-SABIT", "SABIT-TAM",
     'if tur == "ad" and t in _DAMGA_SABIT and d is None:\n',
     'if tur == "ad" and any(k_ in t for k_ in _DAMGA_SABIT) and d is None:      # MUTANT\n'),
    ("M-S3 sabit eslesmesi buyuk/kucuk harfe DUYARSIZ (`TRUE` de yutulur, `None` aday kalir)", "P5-SABIT", "SABIT-TAM",
     'if tur == "ad" and t in _DAMGA_SABIT and d is None:\n',
     'if tur == "ad" and t.lower() in _DAMGA_SABIT and d is None:      # MUTANT\n'),
    ("M-S4 DAMGALI sabit adli belirtec de filtrelenir (eski `None`#hex H20'den GIZLENIR)", "P5-SABIT", "SABIT-DAMGALI",
     'if tur == "ad" and t in _DAMGA_SABIT and d is None:\n',
     'if tur == "ad" and t in _DAMGA_SABIT:      # MUTANT\n'),
    ("M-Y1 damgasiz belirtec arac kusurunda DUSER (eski davranis: hicbir sayiya girmez)", "P5-SAYIM", "SAYIM-ENJEKSIYON",
     '            if sinif == "olculemedi":\n                olu[v] = olu.get(v, 0) + 1\n',
     '            if False:      # MUTANT\n                olu[v] = olu.get(v, 0) + 1\n'),
    ("M-Y2 damgasiz-OLCULEMEDI DAMGASIZ'a eklenir (toplam korunur ama OLCULEMEDI gizlenir)", "P5-SAYIM", "SAYIM-ENJEKSIYON",
     '            z += sinif == "damgasiz"\n',
     '            z += sinif in ("damgasiz", "olculemedi")      # MUTANT\n'),
    ("M-Y3 damgasiz olculemeyen DAMGALI kovasina yazilir (ayrim gorunmez)", "P5-SAYIM", "SAYIM-AYRIM",
     "                olu[v] = olu.get(v, 0) + 1\n",
     "                olc[v] = olc.get(v, 0) + 1      # MUTANT\n"),
    ("M-Y4 damgali/damgasiz ayrimi HIC basilmaz", "P5-SAYIM", "SAYIM-AYRIM",
     '    ayrim = " (damgali %d, damgasiz %d)" % (sum(olc.values()), sum(olu.values())) if olu else ""\n',
     '    ayrim = ""      # MUTANT\n'),
    ("M-Y5 ad belirteci sinifi yalniz defterden (K1'in canli hukmu yerine: arizada DAMGASIZ kalir)", "P5-SAYIM", "SAYIM-AD",
     "    d, v, _k = _damga_karar(kok, _damga_coz(kok, indeks, onbellek, m, t), onbellek)\n",
     "    c_ = _damga_coz(kok, indeks, onbellek, m, t)      # MUTANT\n"
     '    d, v, _k = ("damga", None, 1) if c_[0] in ("tek", "birlesik") and t == "ad" else _damga_karar(kok, c_, onbellek)\n'),
    ("M-Y6 asiri yuklu `yol:N` H20'de DAMGASIZ sayilir (K1 COKLU der)", "P5-SAYIM", "SAYIM-COKLU",
     '    return {"damga": "damgasiz", "coklu": "coklu", "olculemedi": "olculemedi"}.get(d), v if d == "olculemedi" else None\n',
     '    return {"damga": "damgasiz", "coklu": "damgasiz", "olculemedi": "olculemedi"}.get(d), v if d == "olculemedi" else None      # MUTANT\n'),
    ("M-Y7 `yok` belirtec (tanim disi satir) SAYILIR (kod adresi olmayan sinifa girer)", "P5-SAYIM", "SAYIM-YOK",
     '    return {"damga": "damgasiz", "coklu": "coklu", "olculemedi": "olculemedi"}.get(d), v if d == "olculemedi" else None\n',
     '    return {"damga": "damgasiz", "coklu": "coklu", "olculemedi": "olculemedi", "yok": "damgasiz"}.get(d), v if d == "olculemedi" else None      # MUTANT\n'),
    ("M-U29 H20 defter-satiri tavani `>=` (TAM 5 tanimli damgali ad OLCULEMEDI [COKLU_TAVAN] olur)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     "    if len(satirlar_) > _BIRLESIK_TAVAN:\n",
     "    if len(satirlar_) >= _BIRLESIK_TAVAN:      # MUTANT\n"),
    ("M-U30 H20 canli-tanim tavani `>=` (TAM 5 canli tanim OLCULEMEDI [COKLU_TAVAN] olur)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     "    if len(v) > _BIRLESIK_TAVAN:\n",
     "    if len(v) >= _BIRLESIK_TAVAN:      # MUTANT\n"),
    ("M-U31 K1 defter-satiri tavani `<` (TAM 5 tanimli ad damgalanmaz)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     'if len(a) <= _BIRLESIK_TAVAN else ("coklu", len(a), None)',
     'if len(a) < _BIRLESIK_TAVAN else ("coklu", len(a), None)'),
    ("M-U32 K1 canli-tanim tavani `<` (TAM 5 canli tanim damgalanmaz)", "P5-BIRLESIK", "BIRLESIK-TAVAN",
     'if len(v) <= _BIRLESIK_TAVAN else ("coklu", len(v), 0)',
     'if len(v) < _BIRLESIK_TAVAN else ("coklu", len(v), 0)'),
    ("M-U33 tum aday dosyalar silindi: DOSYA_YOK bayragi dusurulur (H20 yedek yolu: damgasiz-OLCULEMEDI [DOSYA_YOK] gorunmez)", "P5-BIRLESIK", "BIRLESIK-DOSYAYOK",
     '        dosya_yok = dosya_yok or (d is None and sebep == "DOSYA_YOK")\n',
     "        dosya_yok = False      # MUTANT\n"),
    ("M-U34 sembol silindi/dosya duruyor: damgasiz `yok` OLCULEMEDI (DOSYA_YOK) sayilir (H20 yedek yolu: sessizlik yerine sayim)", "P5-BIRLESIK", "BIRLESIK-DOSYAYOK",
     '        return ("olculemedi", "DOSYA_YOK", 0) if v else ("yok", None, 0)\n',
     '        return "olculemedi", "DOSYA_YOK", 0      # MUTANT\n'),
    ("M-U35 commit'lenmemis kontrolu YALNIZ ilk tanim grubuna bakar", "P5-BIRLESIK", "BIRLESIK-CALISMA",
     "for i, (y, tam) in enumerate(gruplar)):\n",
     "for i, (y, tam) in enumerate(gruplar[:1])):      # MUTANT\n"),
    ("M-U36 sure butcesi KONTROLU yok (blob cikarirken butce asilsa da hukum verilir)", "P5-BIRLESIK", "BIRLESIK-BUTCE",
     "                if time.monotonic() - bas > _DOGUS_BUTCE:\n",
     "                if False:      # MUTANT\n"),
    ("M-U37 sure butcesi satirinda hukumsuz ad listesi TAVAN adlarindan alinir (yanlis liste)", "P5-BIRLESIK", "BIRLESIK-BUTCE",
     "% (len(atlanan), _DOGUS_BUTCE, _dogus_adlar(sure_adlar)))",
     "% (len(atlanan), _DOGUS_BUTCE, _dogus_adlar(tavan_adlar)))      # MUTANT"),
    ("M-U38 20 dosya tavani belirtecin dosyalarindan HERHANGI biri sigsa da belirteci yargilar (any -> all)", "P5-BIRLESIK", "BIRLESIK-KAP",
     "        if any(y not in surum_onb for y in yollar):\n",
     "        if all(y not in surum_onb for y in yollar):      # MUTANT\n"),
    ("M-U39 hukumsuz ad listesi KIRPILMAZ (`+N daha` yok)", "P5-BIRLESIK", "BIRLESIK-KAP",
     '    return (", ".join(adlar[:5]) + (" +%d daha" % (len(adlar) - 5) if len(adlar) > 5 else "")) if adlar else "-"\n',
     '    return ", ".join(adlar) if adlar else "-"      # MUTANT\n'),
    ("M-U40 20 dosya tavani ALFABETIK (en az dosyali belirtec once secilmez: tekil adlar birlesik adlarin dosyalarina yenilir)", "P5-BIRLESIK", "BIRLESIK-KAP",
     "    for _m, _t, g in sorted(semboller, key=lambda s: (len({y for y, _tam in s[2]}), s[0], s[1])):\n",
     "    for _m, _t, g in sorted(semboller, key=lambda s: (0, s[2][0][0], s[0], s[1])):      # MUTANT\n"),
    ("M-U41 `(+s silinen)` eki YOK (degisen + silinen ayni commit: silinen gorunmez)", "P5-BIRLESIK", "BIRLESIK-SILINEN",
     '(" (+%d silinen)" % s if s else "")',
     '""'),
    ("M-U42 pencere SINIRINDAKI (en eski) surum silinen sayimina girmez", "P5-BIRLESIK", "BIRLESIK-SILINEN",
     "        s += max([0] + [sum(v.values()) - bas for v in g[:n + 1]])\n",
     "        s += max([0] + [sum(v.values()) - bas for v in g[:n]])      # MUTANT\n"),
    ("M-U43 defter ATLANDI notu YOK (eksik tanim kumesinden damga sessizce basilir)", "P5-BIRLESIK", "BIRLESIK-ATLANDI",
     '        if not tam and any(t == "ad" and karar[(m, t)][0] == "damga" for m, t in aday):\n',
     "        if False:      # MUTANT\n"),
    ("M-U44 kayip nesne ls-tree ile ONAYLANMAZ (`cat-file missing` = dosya yok)", "P5-BIRLESIK", "BIRLESIK-NESNE",
     '            t = _dogus_git(kok, "ls-tree", "-z", sha, "--", yol)\n'
     '            cikti.append((None, None) if t.returncode == 0 and not t.stdout.strip(b"\\0") else (None, "GIT_OKUNAMADI"))\n',
     "            cikti.append((None, None))      # MUTANT\n"),
    ("M-U46 blob onbellegi cikarici diline bakmaz (.ts ve .tsx ayni anahtar)", "P5-BIRLESIK", "BIRLESIK-CIKARICI",
     "    cikarici = _adres_cikarici_dili(yol, dil)\n",
     "    cikarici = dil      # MUTANT\n"),
    ("M-U47 defter yolundaki `%XX` kacisi K3'te COZULMEZ", "P5-BIRLESIK", "BIRLESIK-YOLKACIS",
     "    ac = dict((y, _damga_yol_ac(y)) for y in yollar)\n",
     "    ac = dict((y, y) for y in yollar)      # MUTANT\n"),
    ("M-U48 `yol:N` asiri yuk K1 sayisi yanlis (`len(a)+1 tanim`)", "P5-BIRLESIK", "BIRLESIK-YOLCOKLU",
     '(("coklu", len(a), 0) if a else ("yok", None, 0))',
     '(("coklu", len(a) + 1, 0) if a else ("yok", None, 0))'),
    ("M-U49 K3 COKLU beyani `yol:N` icin de (tur kosulu YOK: asiri yuklu yol:N TARANMAZ)", "P5-BIRLESIK", "BIRLESIK-YOLCOKLU",
     '        elif c[0] in ("tek", "birlesik") and k[0] == "coklu" and t == "ad":\n',
     '        elif c[0] in ("tek", "birlesik") and k[0] == "coklu":      # MUTANT\n'),
    ("M-U50 `yol:N` K3 metni birlesik bicim (`2 tanimdan 1'i`): tur kosulu YOK", "P5-BIRLESIK", "BIRLESIK-YOLCOKLU",
     '    if t != "ad" or toplam <= 1:\n',
     "    if toplam <= 1:      # MUTANT\n"),
    ("M-U51 numarasiz satirdaki damgasiz belirtec de sayilir (madde siniri YOK)", "P5-BIRLESIK", "BIRLESIK-SAYISIZ",
     "            sinif, v = _h20_sinif(kok, indeks, onbellek, m, t) if no is not None else (None, None)\n",
     "            sinif, v = _h20_sinif(kok, indeks, onbellek, m, t)      # MUTANT\n"),
    ("M-U52 commit'li tasima + bayat defter: K3 eksik kumeden degisim/silinme hukmu verir (DEFTER_BAYAT atlanmaz)", "P5-BIRLESIK", "BIRLESIK-BAYAT",
     '        if (c[0] in ("tek", "birlesik") or (c[0] == "yok" and t == "ad")) and k[0] == "olculemedi" and k[1] == "DEFTER_BAYAT":\n',
     "        if False:      # MUTANT\n"),
    ("M-U53 bayatlik denetimi KAPALI (defter hep guncel sayilir: yeni dosyadaki tanim gorunmez, 0/0 SESSIZ TEMIZ)", "P5-BIRLESIK", "BIRLESIK-TAZE",
     '    bayat = _adres_ozet([(y, "dosya", s) for y, s in sorted(bugun.items())]) != ozet\n',
     "    bayat = False      # MUTANT\n"),
    ("M-U54 YENI dosyalar tazelenmez (yalniz defterde OLAN degisen dosyalar yeniden cikarilir)", "P5-BIRLESIK", "BIRLESIK-TAZE",
     "    degisen = sorted(y for y, s in bugun.items() if (eski.get(y) or (None,))[0] != s)\n",
     "    degisen = sorted(y for y, s in bugun.items() if y in eski and eski[y][0] != s)      # MUTANT\n"),
    ("M-U55 izlenmeyen silinen dosyalarin defter satirlari DUSULMEZ (`--kur`un hic gormeyecegi dosya aday kalir)", "P5-BIRLESIK", "BIRLESIK-TAZE-SILINEN",
     "    birak = set(taze) | set(bilinmez) | (set(eski) - set(bugun) - izlenen)\n",
     "    birak = set(taze) | set(bilinmez)      # MUTANT\n"),
    ("M-U56 `yol:N` dosya listesi (taban) defterden: yeni ayni adli dosya gorunmez", "P5-BIRLESIK", "BIRLESIK-TAZE-YOL",
     '    taban = {}\n    for y in sorted(bugun):\n        taban.setdefault(y.rsplit("/", 1)[-1], []).append(y)\n'
     '    return "tamam", (taban, ad, indeks[2] and not bilinmez, indeks[3], indeks[4], tuple(bilinmez), indeks[6])\n',
     '    return "tamam", (indeks[0], ad, indeks[2] and not bilinmez, indeks[3], indeks[4], tuple(bilinmez), indeks[6])      # MUTANT\n'),
    ("M-U57 bellekte cikarim DOSYA SAYISI tavani YOK (yuzlerce bayat dosya yeniden cikarilir, DEFTER_BAYAT hic cikmaz)", "P5-BIRLESIK", "BIRLESIK-TAZE-TAVAN",
     "    if len(degisen) > _H20_TAZE_TAVAN or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:\n",
     "    if sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:      # MUTANT\n"),
    ("M-U58 tavan siniri `>=` (tam 100 bayat dosya OLCULEMEDI sayilir)", "P5-BIRLESIK", "BIRLESIK-TAZE-TAVAN",
     "    if len(degisen) > _H20_TAZE_TAVAN or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:\n",
     "    if len(degisen) >= _H20_TAZE_TAVAN or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:      # MUTANT\n"),
    ("M-U59 tavan siniri +1 (101 bayat dosya da yeniden cikarilir)", "P5-BIRLESIK", "BIRLESIK-TAZE-TAVAN",
     "    if len(degisen) > _H20_TAZE_TAVAN or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:\n",
     "    if len(degisen) > _H20_TAZE_TAVAN + 1 or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:      # MUTANT\n"),
    ("M-U60 bellekte cikarim BAYT tavani YOK (toplam boyut sinirsiz)", "P5-BIRLESIK", "BIRLESIK-TAZE-BAYT",
     "    if len(degisen) > _H20_TAZE_TAVAN or sum(_h20_boyut(kok, y) for y in degisen) > _H20_TAZE_BAYT:\n",
     "    if len(degisen) > _H20_TAZE_TAVAN:      # MUTANT\n"),
    ("M-U61 bayatlik OLCUM hatasi sessizce `guncel` sayilir (defter eski, hukum eski defterden)", "P5-BIRLESIK", "BIRLESIK-TAZE-ARIZA",
     '        return "bayatlik", type(e).__name__\n',
     '        return "tamam", indeks      # MUTANT\n'),
    ("M-U62 yedek yolda (tavan/olcum hatasi) KESIN POZITIFLER atilir (govdesi degisen atif de OLCULEMEDI sayilir)", "P5-BIRLESIK", "BIRLESIK-TAZE-ARIZA",
     "        return _h20_satirlari(a, degisen, [], olc, olu, z, c)\n",
     "        return _h20_satirlari(a, [], [], olc, olu, z, c)      # MUTANT\n"),
    ("M-U63 yedek yolda `ayni`/`yok` OLCULEMEDI'ye cevrilmez (tavan asilinca 0/0 SESSIZ TEMIZ)", "P5-BIRLESIK", "BIRLESIK-TAZE-TAVAN",
     "        if kalan:\n",
     "        if False:      # MUTANT\n"),
    ("M-U64 `kapi` bayatlik gecisinde stat onbellegini YAZAR (`adres` sorgusunun yazan yolu: kapi diske yazar)", "P5-BIRLESIK", "BIRLESIK-TAZE-YAZMA",
     "            return _adres_bugun(kok, ozet, None, False)\n",
     "            return _adres_bugun(kok, ozet, None, True)      # MUTANT\n"),
    ("M-U65 cikarilamayan YENI dosya `tam kapsam`i bozmaz (SEMBOL YOK hukmu verilir)", "P5-BIRLESIK", "BIRLESIK-TAZE-KAPSAM",
     '    return "tamam", (taban, ad, indeks[2] and not bilinmez, indeks[3], indeks[4], tuple(bilinmez), indeks[6])\n',
     '    return "tamam", (taban, ad, indeks[2], indeks[3], indeks[4], tuple(bilinmez), indeks[6])      # MUTANT\n'),
    ("M-U66 cikarilamayan dosyada ad ARANMAZ (`ayni` korunur: adi iceren bozuk yeni dosya 0/0 SESSIZ TEMIZ)", "P5-BIRLESIK", "BIRLESIK-TAZE-KAPSAM",
     '        if h == "ayni" and t == "ad" and hukum[5] and _h20_gizli(kok, hukum, m, onbellek):\n',
     "        if False:      # MUTANT\n"),
    ("M-U67 cikarilamayan HER dosya adi iceriyor sayilir (suzgec YOK: ilgisiz bozuk dosya `ayni`yi OLCULEMEDI yapar)", "P5-BIRLESIK", "BIRLESIK-TAZE-GURULTU",
     "        if metin is None or desen.search(metin):\n",
     "        if True:      # MUTANT\n"),
    ("M-U68 cikarici KUSURU `EKSIK` degil bilinmez sayilir (`--kur`un EKSIK defteri gizlenir)", "P5-BIRLESIK", "BIRLESIK-TAZE-EKSIK",
     '        elif sebep == "CIKARICI":\n            return None, sebep\n',
     '        elif False:      # MUTANT\n            return None, sebep\n'),
    ("M-U69 izlenen ama bugun OKUNAMAYAN dosyalar gezilmez (yeni buyuk/ikili/link dosya tam kapsami bozmaz)", "P5-BIRLESIK", "BIRLESIK-TAZE-OKUNMAZ",
     "    for y in degisen + sorted(y for y in izlenen if y not in bugun):\n",
     "    for y in degisen:      # MUTANT\n"),
    ("M-U70 DAMGASIZ/COKLU sinifi TAZE indeksle yapilir (damgali atif VARKEN sayim degisir)", "P5-BIRLESIK", "BIRLESIK-TAZE-SAYIM",
     "            sinif, v = _h20_sinif(kok, indeks, onbellek, m, t) if no is not None else (None, None)\n",
     "            sinif, v = _h20_sinif(kok, hukum, onbellek, m, t) if no is not None else (None, None)      # MUTANT\n"),
    ("M-U71 degismeyen dosyalarin defter satirlari DUSER (aday kumesi yalniz yeniden cikarilan dosyalardan)", "P5-BIRLESIK", "BIRLESIK-TAZE",
     "    ad = dict((k, [(y, t) for y, t in v if y not in birak]) for k, v in indeks[1].items())\n",
     "    ad = {}      # MUTANT\n"),
    ("M-U72 degisen dosyanin ESKI satirlari da KALIR (yeni satirlar eklenir: ayni tam ad iki kez sayilir)", "P5-BIRLESIK", "BIRLESIK-TAZE-AD",
     "    birak = set(taze) | set(bilinmez) | (set(eski) - set(bugun) - izlenen)\n",
     "    birak = set(bilinmez) | (set(eski) - set(bugun) - izlenen)      # MUTANT\n"),
    ("M-U73 bayatlik olcumu `oldur`un stderr satirini SUSTURMAZ (P5 blogu `oldur` yan etkisi sizar)", "P5-BIRLESIK", "BIRLESIK-TAZE-ARIZA",
     "        with contextlib.redirect_stderr(io.StringIO()):\n",
     "        if True:      # MUTANT\n"),
    ("M-U74 cikarilamayan DEGISEN dosyanin eski satirlari DUSMEZ (`--kur` ile ayni aday kumesi degil: SOZDIZIMI/OLCULEMEDI sizar)", "P5-BIRLESIK", "BIRLESIK-TAZE-KAPSAM",
     "    birak = set(taze) | set(bilinmez) | (set(eski) - set(bugun) - izlenen)\n",
     "    birak = set(taze) | (set(eski) - set(bugun) - izlenen)      # MUTANT\n"),
    ("M-U75 SUREKLI okunamayan dosya her bayat kosuda YENI sayilir (defter ATLANDI tasirken de: ilgisiz degisiklikte gurultu)", "P5-BIRLESIK", "BIRLESIK-TAZE-GURULTU",
     "        elif y in indeks[4] or y in degisen or indeks[2]:\n",
     "        else:      # MUTANT\n"),
    ("M-U76 defter kaynagi/evren denetimi YOK (`.git`siz kopyada dosya sistemi evrenine karsi sahte GOVDE DEGISTI)", "P5-BIRLESIK", "BIRLESIK-TAZE-KAYNAK",
     '        if kaynak.startswith("git") != str(indeks[6]).startswith("git"):',
     "        if False:"),
    ("M-U77 yeni satirlar yalniz defterde OLMAYAN adlara eklenir (tekil -> coklu gecisi: ayni adli yeni tanim gorunmez)", "P5-BIRLESIK", "BIRLESIK-TAZE-TEKIL",
     '            ad.setdefault(t.rsplit(".", 1)[-1], []).append((y, t))\n',
     '            if t.rsplit(".", 1)[-1] not in ad:      # MUTANT\n'
     '                ad[t.rsplit(".", 1)[-1]] = [(y, t)]\n'),
    ("M-U78 cikarici KUSURU yedek yola girmez (kesin pozitifler ve sayimlar `DEFTER_KUSUR` ile silinir)", "P5-BIRLESIK", "BIRLESIK-TAZE-EKSIK",
     '    if durum in ("bayat", "bayatlik", "kusur"):',
     '    if durum in ("bayat", "bayatlik"):'),
    ("M-U79 bayt toplami yalniz DEFTERDE OLAN dosyalari sayar (yeni buyuk dosyalar tavana girmez)", "P5-BIRLESIK", "BIRLESIK-TAZE-BAYT",
     "sum(_h20_boyut(kok, y) for y in degisen)",
     "sum(_h20_boyut(kok, y) for y in degisen if y in eski)"),
    ("M-N1 `not` bayat defterde DEFTER kumesine geri doner (`[k]` damga: yeni dosyadaki tanim gorunmez; hemen kapi sahte uyari)", "P5-DAMGA", "DAMGA-TAZE",
     "        durum, indeks = _h20_taze(kok, indeks, onbellek)   # bayat defterde H20'nin BELLEKTEKI taze kumesi (ikinci yol YOK)\n"
     '        if durum != "tamam":\n'
     "            return govde, _damga_taze_yok(aday, sonekli, durum, indeks)\n",
     "        durum = \"tamam\"      # MUTANT\n"),
    ("M-N2 taze kume cikarilamazsa EKSIK (defter) kumeden damga BASILIR (yedek yol kapali)", "P5-DAMGA", "DAMGA-TAZE-YOK",
     "        durum, indeks = _h20_taze(kok, indeks, onbellek)   # bayat defterde H20'nin BELLEKTEKI taze kumesi (ikinci yol YOK)\n"
     '        if durum != "tamam":\n'
     "            return govde, _damga_taze_yok(aday, sonekli, durum, indeks)\n",
     "        sonuc_ = _h20_taze(kok, indeks, onbellek)\n"
     '        indeks = sonuc_[1] if sonuc_[0] == "tamam" else indeks      # MUTANT\n'),
    ("M-N3 yedek yolda K3 `OLCULEMEDI` satiri YOK (eksik kumeden dogusta-bayat sessiz)", "P5-DAMGA", "DAMGA-TAZE-YOK",
     '    notlar.append("DOGUSTA BAYAT: OLCULEMEDI (DEFTER_BAYAT: taze aday kumesi cikarilamadi)")\n',
     "    pass      # MUTANT\n"),
    ("M-N4 yedek yolda aday basina `ATIF OLCULEMEDI` satiri YOK (damga sessizce basilmaz)", "P5-DAMGA", "DAMGA-TAZE-YOK",
     '    notlar = ["ATIF OLCULEMEDI: %s (DEFTER_BAYAT)" % m for m, _t in aday]\n',
     "    notlar = []      # MUTANT\n"),
    ("M-N5 yedek yolda `ATIF NOT` sebep satiri YOK (cikarilamama nedeni gizlenir)", "P5-DAMGA", "DAMGA-TAZE-TAVAN",
     '    notlar.append("ATIF NOT: taze aday kumesi cikarilamadi (%s: %s) - eksik kumeden damga/dogusta bayat VERILMEZ; hafiza.py adres --kur"\n'
     "                  % (durum, sebep))\n",
     "    pass      # MUTANT\n"),
    ("M-N6 taze kume ADAY YOKKEN de cikarilir (`aday` kosulu kalkar: yalniz damgali belirtecli `not` maliyet/cikti degisir)", "P5-DAMGA", "DAMGA-TAZE-ADAYSIZ",
     "    if aday:        # P5.4: taze kume yalniz damgasiz ADAY belirtec VARKEN (aday yoksa `not` bayt-bayt ve sure olarak eski)\n",
     "    if True:      # MUTANT\n"),
    ("M-N7 cikarilamayan dosyada ad ARANMAZ (adi iceren bozuk yeni dosya varken eksik kumeden damga basilir)", "P5-DAMGA", "DAMGA-TAZE-BILINMEZ",
     "    _damga_bilinmez(kok, indeks, karar, onbellek)\n",
     "    pass      # MUTANT\n"),
    ("M-N8 cikarilamayan HER dosya damgayi engeller (ad suzgeci YOK: ilgisiz bozuk dosya gurultu)", "P5-DAMGA", "DAMGA-TAZE-GURULTU",
     '            if t == "ad" and k[0] in ("damga", "yok") and _h20_gizli(kok, indeks, m, onbellek):\n',
     '            if t == "ad" and k[0] in ("damga", "yok"):      # MUTANT\n'),
    ("M-N9 `not` bayatlik gecisinde stat onbellegini YAZAR (kapi ile ayni yol: `yaz=True`)", "P5-DAMGA", "DAMGA-TAZE-YAZMA",
     "            return _adres_bugun(kok, ozet, None, False)\n",
     "            return _adres_bugun(kok, ozet, None, True)      # MUTANT\n"),
    ("M-N10 cikarilamayan dosya adi iceriyorsa `yok` kararini DA cevirmez (tek tanimli ad + bozuk dosya: `COZULEMEDI` der, ad sessizce duser)", "P5-DAMGA", "DAMGA-TAZE-BILINMEZ",
     '            if t == "ad" and k[0] in ("damga", "yok") and _h20_gizli(kok, indeks, m, onbellek):\n',
     '            if t == "ad" and k[0] == "damga" and _h20_gizli(kok, indeks, m, onbellek):      # MUTANT\n'),
    ("M-N11 K3 `yok` cozumlu adin DEFTER_BAYAT beyanini dusurur (K1 `OLCULEMEDI` der, K3 sessiz)", "P5-DAMGA", "DAMGA-TAZE-BILINMEZ",
     '        if (c[0] in ("tek", "birlesik") or (c[0] == "yok" and t == "ad")) and k[0] == "olculemedi" and k[1] == "DEFTER_BAYAT":\n',
     '        if c[0] in ("tek", "birlesik") and k[0] == "olculemedi" and k[1] == "DEFTER_BAYAT":      # MUTANT\n'),
    ("M-Y8 H20 sessizlik kosulu `olu`yu yok sayar (damgali atif YOKKEN damgasiz-OLCULEMEDI sessizce duser)", "P5-SAYIM", "SAYIM-SAF",
     "    if not a and not z and not c and not olu:\n        return []\n",
     "    if not a and not z and not c:      # MUTANT\n        return []\n"),
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
    sabotaj_sec = None
    for arg in sys.argv[1:]:            # gelistirme kolayligi: `--kol=A-EZME,A-EKSIK` yalniz o kollari, `--sab=M-U12,M-U36` yalniz o sabotajlari kosar
        if arg.startswith("--kol="):
            kollar = [k for k in kollar if k in arg[len("--kol="):].split(",")]
        elif arg.startswith("--sab="):
            sabotaj_sec = tuple(x + " " for x in arg[len("--sab="):].split(",") if x)
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
        kacan, olculemeyen, kosulan = [], [], 0
        for sira, (ad, kol, etiket, ankor, yeni) in enumerate(SABOTAJLAR, 1):
            if kol not in kollar or (sabotaj_sec is not None and not ad.startswith(sabotaj_sec)):
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
            _SADECE[0] = etiket                 # P5-BIRLESIK: yalniz sabotajin KENDI ekseninin vektorleri kosulur (sure)
            try:
                atesler = {e for e, _ in hepsi(sab, os.path.join(taban, "ks%d" % sira), "s%d" % sira, io.open(sab, encoding="utf-8", newline="").read(), [kol])}
            except Kurulamadi as e:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, e))
                return 2
            finally:
                _SADECE[0] = None
            atesler -= {"OLCULEMEDI-WIN"}
            kosulan += 1
            if etiket in atesler:
                ort = sorted(atesler - {etiket})
                print("  %-60s -> ISIRDI ✓  (%s%s)" % (ad, etiket, ("; ortusme: " + ", ".join(ort)) if ort else ""))
            else:
                print("  %-60s -> KACTI ✗  (%s ekseni sabotajda TEMIZ; atesleyen: %s)" % (ad, etiket, ", ".join(sorted(atesler)) or "hicbiri"))
                kacan.append(ad)
        if sabotaj_sec is None and "A-TANIM" in kollar:
            os.makedirs(os.path.join(taban, "olcutk"), exist_ok=True)
            try:
                kacan += olcut_sinamasi(s, taban)
            except Kurulamadi as e:
                print("SONUC: OLCULEMEDI — %s" % e)
                return 2
        print(CIZGI)
        if kacan:
            print("SONUC: KIRMIZI — KACTI: %s" % "; ".join(kacan))
            return 1
        if olculemeyen:
            print("SONUC: YESIL (SINIRLI) — olculebilen her sabotaj ISIRDI; %d OLCULEMEDI (platforma/kullaniciya ozgu)." % len(olculemeyen))
        else:
            print("SONUC: YESIL — tum kollar temiz, %d sabotaj AYRI eksende ISIRDI." % kosulan)
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

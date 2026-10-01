#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — README KANIT BLOGU KAPISI (BITTI maddesi 5).

NEDEN VAR (olculdu 14 Agu 2026)
  Madde 5: "25 Agu yazisinin okuru, depoya gelip README ile sistemi kendi basina
  deneyebilir." Okurun yapacagi sey README'nin "Kanitini kendin kos" blogudur ve
  o blok SAYISAL BEYANLAR tasiyor:
      python3 hafiza.py isir --kok=deneme   # taze projede: 67/67 + 2 SINANMADI, exit 2
      python3 hafiza.py isir --kok=deneme   # derle sonrasi: 69/69, exit 0
  Bu beyanlari HICBIR kapi olcmuyordu. Ustelik ikincisi (`derle` sonrasi isir=0)
  `DURUM.md`in "olculmuyor" diye yazdigi bosluğun ta kendisiydi: README onu IDDIA
  ediyor, hicbir sey dogrulamiyordu. Bir okur yanlis sayiyla karsilassa projenin
  TEK vaadi (olculebilirlik) onun gozunde daha ilk dakikada duserdi.

  Ayni gun iki kez isiran sinif: "belge de bir arayuzdur ve yalan soyleyebilir"
  (`paketle.sh` basligi · `SKILL.md` kurulum akisi). Bu, ucuncu kapisidir.

NE OLCER — DORT AYRI EKSEN
  KAPI-1 BEYAN     : blok AYIKLANABILIR beyan tasiyor mu? Her `python3 hafiza.py`
                     satirinin yorumundan `exit N` cikarilabiliyor mu, ve en az
                     iki `isir` beyani var mi? (README olculebilir olmaktan
                     cikarsa — yorumlar silinirse — kapi KIRMIZI yanar.)
  KAPI-2 GERCEK    : blok KOSULUR ve her beyan GERCEKLE karsilastirilir. Beklenen
                     degerler BLOKTAN OKUNUR, araca YAZILMAZ — "sayi yazilmaz,
                     URETILIR" dersi. README'deki sayi degisirse kapi onu izler;
                     README yanlis sayi yazarsa KIRMIZI yanar.
  KAPI-3 SOZLESME  : README'nin "Cikis kodlari" paragrafindaki `isir` kod KUMESI,
                     motorun kendi bastigi `CIKIS KODLARI:` satiriyla ayni mi.
                     30 Eyl 2026 (ADDITIVE, IS_EMRI_URUN_HAZIRLIK.md KALEM 3): `skill-kur` ve `paket`
                     icin de ayni karsilastirma — motorun `<komut> --help` sonundaki `CIKIS KODLARI:`
                     satiri ile README'deki `skill-kur:` / `paket:` paragraflari. Sebep: README'nin
                     skill-kur sozlesmesinde `3` YOKTU ve hicbir sey bunu olcmuyordu.
  KAPI-4 TAKMA AD  : README'nin "Ingilizce takma adlar" tablosu motorla tutuyor mu?
                     (1 Eki 2026, IS_EMRI_TAKMA_AD_BEYAZ_LISTE.md KALEM 1.) BEKLENEN ESLEME README
                     TABLOSUNDAN AYIKLANIR, motorun `_KOMUT_TAKMA_AD` sozlugunden OKUNMAZ: ayni
                     sozlukten turetilen kapi, sozluk bozulunca birlikte bozulur ve YESIL basar
                     (paylasilan kural = paylasilan korluk). Dort alt eksen, her biri ayri etiketli:
                       [TABLO]    tablo ayiklanabiliyor ve tutarli mi (cekirdek bes komutun takma adi var)
                       [YARDIM]   her satir icin `<ing> --help` ve `<tr> --help` exit 0, ciktilari ayni
                                  ve canonik `usage: hafiza.py <tr>` ile basliyor (ayni alt komut)
                       [KUME]     motorun ust duzey `--help` komut kumesi == README'nin adlari
                                  (belgelenmemis ya da vaat edilip verilmeyen ad yok)
                       [DAVRANIS] iki AYRI kum havuzunda ayni girdi: Turkce ad ve takma ad AYNI exit +
                                  AYNI stdout (yol/tarih/zincir-halkasi normalize) — `isir` dahil, 16 adim;
                                  kanonik taraf her adimda exit 0 vermelidir ve zaman asimi (OLCULEMEDI)
                                  "esit" SAYILMAZ (iki havuz ayni sentinel'i uretir)
                       [BELGE]    `skill/SKILL.md`'deki takma ad satiri README tablosunun KOPYASIDIR: ayni kume mi
                     Her KAPI-4 mutanti atesleyen alt eksenin BEKLENENLE BIREBIR ayni olmasini ister
                     (bagimsiz inceleme 1 Eki 2026: aksi halde [DAVRANIS] olu olsa da 12/12 mutant ISIRDI derdi).
                     SINIRLAR (gizlenmez): beklenti README'den geldigi icin README ve motor AYNI yonde birlikte
                     degisirse KAPI-4 yesil kalir (bunu ADR + Onur kilidi korur); `korunan` yalniz [YARDIM] ile
                     olculur (davranis adimi yok: bir blok isareti kurmayi gerektirir).

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. `t_y3.py` / `t_y42.py` ARTIK BURADA KOSAR (Onur karari, 14 Agu). Gerekcesi
     olculdu: `kanit` isinin HER IKI adimi da `continue-on-error: true` tasiyor,
     yani kirmizilari YUTULUYOR — o adimlar KAPI degil OLCUM. Bu arac onlari
     `continue-on-error`SIZ kosar ve README'nin "20 senaryo"/"58 senaryo"
     beyanlarini cikti sayilariyla karsilastirir.
     Maliyet dusurulmustur: heavy kosucular YALNIZ TEMIZ turda kosar; mutant
     turlari yakalanan ciktiyi YENIDEN KULLANIR — cunku o mutantlar kosucuyu
     degil KARSILASTIRMAYI sinar. Bu bir SINIRDIR ve burada yazilidir:
     mutant, kosucunun kendi davranisini olcmez.
  2. Blokta TANIMADIGI bir satir gorurse ARAC DURUR (OLCULEMEDI). README'ye yeni
     bir adim eklenip kapinin onu sessizce yok saymasi, tam da bu araciin
     onlemek icin var oldugu sey.
  3. Blok depo kokunde degil, `skill/scripts`in GECICI bir kopyasinda kosar
     (depo kirletilmesin). Komutlar ve goreli yollar birebir aynidir.
  4. README'nin ANLATIMINI olcmez (sira, dil, aciklik) — yalnizca olculebilir
     beyanlarini.

CIKIS KODLARI
  0  dort kapi da temiz VE tum mutantlar AYRI eksende ISIRDI
  1  bir kapi kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  olculemedi (README yok, blok yok, taninmayan satir, git yok)
"""
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


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
README = os.path.join(KOK, "README.md")

_BASLIK = re.compile(r"^#+\s*Kan[iı]t[iı]n?[iı]? kendin ko[sş]\s*$", re.M | re.I)
_EXIT = re.compile(r"exit\s+(\d+)")
_ORAN = re.compile(r"(\d+)\s*/\s*(\d+)")
_SINANMADI = re.compile(r"(\d+)\s+SINANMADI")
# motorun kendi hukum satiri
_SONUC = re.compile(r"(\d+)/(\d+) kosulan mutant ISIRIYOR · (\d+) SINANMADI")
_MOTOR_KOD = re.compile(r"CIKIS KODLARI:\s*(.+)")
_KOD = re.compile(r"(\d+)")
# README'nin "Cikis kodlari" paragrafi
_README_ISIR = re.compile(r"`isir`\s*:(.+?)\.", re.S)
_README_SKILL_KUR = re.compile(r"^`skill-kur`\s*:(.+?)(?:\n[ \t]*\n|\Z)", re.S | re.M)   # PARAGRAF: bos satira kadar
_README_PAKET = re.compile(r"^`paket`\s*:(.+?)(?:\n[ \t]*\n|\Z)", re.S | re.M)
_KOD_ARKA = re.compile(r"`(\d+)`")          # README'de kodlar `N` icinde yazilir; prozdaki rakam SAYILMAZ
# kosucularin ozet satirlari: t_y3 "SONUC: 20/20 senaryo ..." · t_y42 "... (toplam 58)"
_KANIT_TOPLAM = re.compile(r"toplam\s+(\d+)")
_KANIT_ORAN = re.compile(r"SONUC:\s*\d+\s*/\s*(\d+)\s+senaryo")
_SENARYO = re.compile(r"(\d+)\s+senaryo")


def kanit_sayisi(cikti):
    """Kosucunun ciktisindan TOPLAM senaryo sayisi; ayiklanamazsa None."""
    m = _KANIT_ORAN.search(cikti) or _KANIT_TOPLAM.search(cikti)
    return int(m.group(1)) if m else None


def blok_bul(metin):
    """"Kanitini kendin kos" basligindan sonraki ILK cit blogu."""
    m = _BASLIK.search(metin)
    if not m:
        return None
    kalan = metin[m.end():]
    i = kalan.find("```")
    if i < 0:
        return None
    j = kalan.find("```", i + 3)
    if j < 0:
        return None
    govde = kalan[i + 3:j]
    return govde.split("\n", 1)[1] if govde.startswith("bash") else govde


def satirlari_coz(blok):
    """Blogun her satirini (tur, komut, beyan) olarak cozer.

    KALEM 1 (IS_EMRI_ISIR_GIT_VE_ORTAM_KAPISI.md, 7 Eyl 2026): README'deki
    `mkdir -p deneme && git init -q deneme` TEK ham satirda IKI komut tasir;
    gercek bir shell bunlari SIRAYLA kosar. Eskiden bu satir bastan `mkdir `
    ile basladigi icin TUMU tek bir MKDIR adimi sayiliyordu ve `&&`den
    SONRAKI `git init` HIC calismadan kayboluyordu -> simule edilen `deneme`
    dizininde gercek `.git` OLUSMUYORDU. Sonucu OLCEN bir mutant olmadigi
    surece bu sessizdi; git'e bagli M-H12g/M-H14g eklenince (KALEM 1)
    `mutant_git`in POZITIF KONTROLU bunu yakaladi ve iki mutant burada
    SESSIZCE SINANMADI'ya dustu — kapi KIRMIZI yandi. Duzeltme: `#` yorumu
    TAM HAM SATIRDAN bir kez ayiklanir, KALAN komut `&&` ile bolunur ve HER
    parca AYRI adim olarak siniflandirilir (gercek shell semantigi budur).

    Taninmayan satir -> ('BILINMEYEN', ham, None). Cagiran yer DURUR."""
    out = []
    for ham in blok.split("\n"):
        s = ham.strip()
        if not s:
            continue
        komut_tam, _, yorum = s.partition("#")
        beyan = None
        if yorum.strip():
            e = _EXIT.search(yorum)
            o = _ORAN.search(yorum)
            sn = _SINANMADI.search(yorum)
            beyan = {"ham": yorum.strip(),
                     "exit": int(e.group(1)) if e else None,
                     "oran": (int(o.group(1)), int(o.group(2))) if o else None,
                     "sinanmadi": int(sn.group(1)) if sn else None,
                     "senaryo": None}
            sy = _SENARYO.search(yorum)
            if sy:
                beyan["senaryo"] = int(sy.group(1))
        parcalar = [p.strip() for p in re.split(r"\s*&&\s*", komut_tam.strip()) if p.strip()]
        for komut in parcalar:
            if komut.startswith("cd "):
                out.append(("CD", komut, beyan))
            elif komut.startswith("mkdir "):
                out.append(("MKDIR", komut, beyan))
            elif "git init" in komut:
                out.append(("GIT", komut, beyan))
            elif re.match(r"python3?\s+hafiza\.py\s", komut):
                out.append(("MOTOR", komut, beyan))
            elif re.match(r"python3?\s+t_y\d+\.py", komut):
                out.append(("KANIT", komut, beyan))
            else:
                out.append(("BILINMEYEN", komut, beyan))
    return out


# ------------------------------------------------------------------- KAPI-1
def kapi1_beyan(adimlar):
    """Blok AYIKLANABILIR beyan tasiyor mu?"""
    bulgu = []
    motor = [(k, b) for t, k, b in adimlar if t == "MOTOR"]
    if not motor:
        bulgu.append("blokta hic `hafiza.py` komutu YOK")
    isirlar = [(k, b) for k, b in motor if " isir " in k + " "]
    beyanli = [b for k, b in isirlar if b and b.get("exit") is not None]
    if len(beyanli) < 2:
        bulgu.append("`isir` icin AYIKLANABILIR `exit N` beyani %d < 2 — README olculebilir "
                     "olmaktan cikti" % len(beyanli))
    for k, b in isirlar:
        if b and b.get("exit") is not None and b.get("oran") is None:
            bulgu.append("beyanda `exit` var ama mutant orani (N/M) YOK: %s" % b["ham"])
    return bulgu


# ------------------------------------------------------------------- KAPI-3
def kapi3_sozlesme(metin, isir_ciktisi):
    """README'nin ilan ettigi `isir` kod kumesi motorunkiyle ayni mi?"""
    m = _README_ISIR.search(metin)
    if not m:
        return ["README'de `isir` cikis kodu paragrafi bulunamadi"]
    belge = set(int(x) for x in _KOD.findall(m.group(1)))
    mm = _MOTOR_KOD.search(isir_ciktisi)
    if not mm:
        return ["motor `CIKIS KODLARI:` satirini basmadi — karsilastirilamaz"]
    gercek = set(int(x) for x in _KOD.findall(mm.group(1)))
    if belge != gercek:
        return ["README %s diyor, motor %s basiyor (fark: %s)"
                % (sorted(belge), sorted(gercek), sorted(belge ^ gercek))]
    return []


_YARDIM_ONBELLEK = {}


def komut_kodlari(kaynak_scripts, komut):
    """Motorun `<komut> --help` sonundaki `CIKIS KODLARI:` satirinin kod KUMESI (set | None)."""
    anahtar = (os.path.abspath(kaynak_scripts), komut)
    if anahtar not in _YARDIM_ONBELLEK:
        p = subprocess.run([sys.executable, "-X", "utf8", "hafiza.py", komut, "--help"],
                           cwd=kaynak_scripts, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        m = _MOTOR_KOD.search(p.stdout.decode("utf-8", "replace"))
        _YARDIM_ONBELLEK[anahtar] = (set(int(x) for x in _KOD.findall(m.group(1)))
                                     if (m and p.returncode == 0) else None)
    return _YARDIM_ONBELLEK[anahtar]


def kapi3_komut_sozlesmesi(metin, kaynak_scripts):
    """README'nin `skill-kur` ve `paket` kod kumeleri motorun `--help` satirlariyla ayni mi? (ADDITIVE)
    SINIR: KUMEYI karsilastirir, kodlarin ANLAMINI degil (1 ile 2'nin anlamlari takas edilse kume ayni kalir)."""
    bulgu = []
    for komut, desen in (("skill-kur", _README_SKILL_KUR), ("paket", _README_PAKET)):
        m = desen.search(metin)
        if not m:
            bulgu.append("README'de `%s` cikis kodu paragrafi bulunamadi" % komut)
            continue
        belge = set(int(x) for x in _KOD_ARKA.findall(m.group(1)))
        gercek = komut_kodlari(kaynak_scripts, komut)
        if gercek is None:
            bulgu.append("motor `%s --help` ciktisinda `CIKIS KODLARI:` satirini basmadi" % komut)
        elif belge != gercek:
            bulgu.append("README `%s` icin %s diyor, motor %s basiyor (fark: %s)"
                         % (komut, sorted(belge), sorted(gercek), sorted(belge ^ gercek)))
    return bulgu


# ------------------------------------------------------------------- KAPI-4
# IS_EMRI_TAKMA_AD_BEYAZ_LISTE.md KALEM 1 (1 Eki 2026). Beklenen esleme README tablosundan ayiklanir (basligin
# docstring'i): motorun `_KOMUT_TAKMA_AD` sozlugu BURADA OKUNMAZ, yalniz motorun DAVRANISI (--help, kosum) olculur.
_TAKMA_BASLIK = re.compile(r"İngilizce takma adlar \(yalnız komut adı; bayraklar Türkçe\)")
_TAKMA_SATIR = re.compile(r"^\|\s*`([a-z][a-z-]*)`\s*\|\s*(?:`([a-z][a-z-]*)`|—[^|]*)\s*\|$")
_TAKMA_AYIRICI = re.compile(r"^\|[\s:|-]+\|$")
_KUME = re.compile(r"\{([^{}\s]+)\}")
# Is emri K1: "en az init≡kur, note≡not, compile≡derle, gate≡kapi, bite≡isir". Bunlar ZORUNLUDUR: README tablosunda
# takma adi yoksa KAPI KIRMIZI. Tablodaki oteki komutlar `_DAVRANIS` adimlarinda geciyorsa ayni sekilde olculur;
# gecmeyenler (korunan) yalniz [YARDIM] ile olculur — bu bir SINIRDIR ve burada yazilidir.
_CEKIRDEK = ("kur", "not", "derle", "kapi", "isir")
_TARIH = re.compile(r"\d{4}-\d{2}-\d{2}(?:-\d{4})?")
_KUM_AD = re.compile(r"takma-ad-kumu-\w{8}")
_HALKA = re.compile(r"(MUHURLENDI: )[0-9A-Fa-f]{16}\.\.\.")
# (komut, arguman sablonu): {P} proje dizini, {K} kum havuzunun koku. Sira README'nin kanit akisini izler
# (kur -> kapi -> not -> derle -> kapi -> isir); ucuz ve yazan komutlar `isir`den SONRA gelir ki `isir`
# README'deki halde (derle sonrasi) kosulsun.
_DAVRANIS = [
    ("kur", ["--kok={P}", "--ad", "Deneme"]),
    ("kapi", ["--kok={P}"]),
    ("not", ["--kok={P}", "--konu=genel-durum", "--metin=ilk not"]),
    ("derle", ["--kok={P}"]),
    ("kapi", ["--kok={P}"]),
    ("isir", ["--kok={P}"]),
    ("surum", []),
    ("karar", ["--kok={P}", "--baslik", "Deneme karari"]),
    ("bolum-kur", ["--kok={P}", "--dene"]),
    ("bloklastir", ["--kok={P}"]),
    ("devral", ["--kok={P}", "--kesif"]),
    ("emekli", ["--kok={P}", "1-2", "--not", "esdegerlik olcumu"]),
    ("muhur", ["--kok={P}", "takma ad esdegerlik olcumu"]),
    ("kapi", ["--kok={P}"]),
    ("paket", ["--cikti={K}/ek.skill"]),
    ("skill-kur", ["--proje={P}"]),
]
_TAKMA_YARDIM = {}
_DAVRANIS_ONBELLEK = {}


def takma_tablosu(metin):
    """(tablo, bulgu): README'nin "Ingilizce takma adlar" tablosu {komut: takma_ad | None}. Baslik YOKSA ya da bir satir
    TANINMIYORSA bulgu doludur (sessiz atlama YOK); baslik yoksa tablo None."""
    m = _TAKMA_BASLIK.search(metin)
    if not m:
        return None, ["[TABLO] README'de 'Ingilizce takma adlar' basligi bulunamadi"]
    satirlar = []
    for ham in metin[m.end():].split("\n"):
        s = ham.strip()
        if s.startswith("|"):
            satirlar.append(s)
        elif satirlar:
            break
    if len(satirlar) < 3 or not _TAKMA_AYIRICI.match(satirlar[1]):
        return None, ["[TABLO] basliktan sonra baslik+ayirici+satir yapisinda tablo YOK"]
    tablo, bulgu, takmalar = {}, [], set()
    for s in satirlar[2:]:
        g = _TAKMA_SATIR.match(s)
        if not g:
            bulgu.append("[TABLO] taninmayan tablo satiri: %s" % s)
            continue
        tr, ing = g.group(1), g.group(2)
        if tr in tablo:
            bulgu.append("[TABLO] `%s` iki satirda" % tr)
        if ing is not None and ing in takmalar:
            bulgu.append("[TABLO] `%s` iki komutun takma adi" % ing)
        takmalar.add(ing)
        tablo[tr] = ing
    bulgu += ["[TABLO] `%s` hem kanonik komut hem takma ad" % x for x in sorted(takmalar & set(tablo))]
    bulgu += ["[TABLO] cekirdek komut `%s` icin takma ad YOK" % k for k in _CEKIRDEK if tablo.get(k) is None]
    return tablo, bulgu


def _takma_yardim(kaynak_scripts, ad):
    """`hafiza.py <ad> --help` -> (exit, cikti); ad bos ise ust duzey `--help`."""
    anahtar = (os.path.abspath(kaynak_scripts), ad)
    if anahtar not in _TAKMA_YARDIM:
        p = subprocess.run([sys.executable, "-X", "utf8", "hafiza.py"] + ([ad] if ad else []) + ["--help"],
                           cwd=kaynak_scripts, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        _TAKMA_YARDIM[anahtar] = (p.returncode, p.stdout.decode("utf-8", "replace"))
    return _TAKMA_YARDIM[anahtar]


def kapi4_yardim(tablo, kaynak_scripts):
    """[YARDIM] her satir: `<tr> --help` ve `<ing> --help` exit 0, ciktilari AYNI, canonik usage'la basliyor."""
    bulgu = []
    for tr, ing in sorted(tablo.items()):
        kt, ct = _takma_yardim(kaynak_scripts, tr)
        if kt != 0:
            bulgu.append("[YARDIM] kanonik `%s --help` exit %d" % (tr, kt))
        if ing is None:
            continue
        ki, ci = _takma_yardim(kaynak_scripts, ing)
        if ki != 0:
            bulgu.append("[YARDIM] README `%s` icin `%s` takma adini vaat ediyor ama `%s --help` exit %d"
                         % (tr, ing, ing, ki))
        elif ci != ct:
            bulgu.append("[YARDIM] `%s --help` ile `%s --help` AYNI alt komutu tarif etmiyor" % (ing, tr))
        elif not ci.startswith("usage: hafiza.py %s" % tr):
            bulgu.append("[YARDIM] `%s --help` canonik `usage: hafiza.py %s` ile baslamiyor" % (ing, tr))
    return bulgu


def kapi4_kume(tablo, kaynak_scripts):
    """[KUME] motorun ust duzey `--help` komut kumesi == README'nin adlari: belgelenmemis takma ad da, vaat edilip
    verilmeyen ad da YOK."""
    kod, c = _takma_yardim(kaynak_scripts, "")
    m = _KUME.search(c) if kod == 0 else None
    if not m:
        return ["[KUME] ust duzey `--help` komut kumesi (`{...}`) ayiklanamadi (exit %d)" % kod]
    motor = set(m.group(1).split(","))
    belge = set(tablo) | {v for v in tablo.values() if v}
    return (["[KUME] motor `%s` adini kabul ediyor, README tablosunda YOK" % x for x in sorted(motor - belge)]
            + ["[KUME] README `%s` diyor, motorun komut kumesinde YOK" % x for x in sorted(belge - motor)])


def _normalle(cikti):
    """Kum havuzu koku (rastgele son ek), tarih/damga ve zincir halkasi karmasi normalize edilir; BASKA HICBIR SEY.
    Halka karmasi SANIYE damgasi tasir (`zincir_halka`: `t` alani hash'e girer): iki havuzda ayni saniyeye dusmesi
    TESADUFTUR; normalize edilmezse `muhur`≡`seal` adimi yalanci kirmizi/yesil verirdi (OLCULDU 1 Eki 2026:
    motor mutanti kosumunda iki havuzun halkalari FARKLI cikti)."""
    cikti = _HALKA.sub(lambda m: m.group(1) + "<HALKA>...", cikti)
    return _TARIH.sub("<TARIH>", _KUM_AD.sub("takma-ad-kumu-X", cikti))


def _takma_kos(kaynak_scripts, sozcuk):
    """TAZE bir kum havuzunda `_DAVRANIS` adimlarini kosar; `sozcuk(komut)` = o adimda YAZILACAK komut adi.
    Doner [(exit, normalize cikti)]. Her cagri KENDI havuzunu kurar (PAYLASILAN KUM HAVUZU dersi)."""
    skill = os.path.dirname(os.path.abspath(kaynak_scripts))
    kok = tempfile.mkdtemp(prefix="takma-ad-kumu-")
    try:
        shutil.copytree(skill, os.path.join(kok, "skill"), ignore=shutil.ignore_patterns("__pycache__", "deneme*"))
        proje = os.path.join(kok, "proje")
        os.makedirs(proje)
        g = subprocess.run(["git", "init", "-q", proje], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if g.returncode != 0:
            raise OSError("git init basarisiz: %s" % g.stdout.decode("utf-8", "replace")[:120])
        calisma = os.path.join(kok, "skill", "scripts")
        sonuc = []
        for komut, arg in _DAVRANIS:
            arg = [a.replace("{P}", proje).replace("{K}", kok) for a in arg]
            try:
                p = subprocess.run([sys.executable, "hafiza.py", sozcuk(komut)] + arg, cwd=calisma,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
                sonuc.append((p.returncode, _normalle(p.stdout.decode("utf-8", "replace"))))
            except subprocess.TimeoutExpired:
                sonuc.append((None, "ZAMAN ASIMI (1800 sn)"))
        return sonuc
    finally:
        shutil.rmtree(kok, ignore_errors=True)


def _ilk_fark(a, b):
    sa, sb = a.split("\n"), b.split("\n")
    for x, y in zip(sa, sb):
        if x != y:
            return "Turkce: %s | Ingilizce: %s" % (x.strip()[:90], y.strip()[:90])
    return "satir sayisi %d != %d" % (len(sa), len(sb))


def kapi4_davranis(tablo, kaynak_scripts):
    """[DAVRANIS] IKI AYRI kum havuzunda ayni girdi: Turkce ad ve takma ad ayni exit + ayni stdout. Iki havuz
    ES ZAMANLI kosar (`isir` pahali). Sonuc motor yolu + esleme icin onbelleklenir: README'nin baska
    yerini bozan mutantlar motoru degistirmedigi icin YENIDEN kosmaz."""
    eksik = sorted({k for k, _ in _DAVRANIS if tablo.get(k) is None})
    if eksik:
        return ["[DAVRANIS] README tablosunda takma adi olmayan komut(lar) davranista olculemez: %s" % ", ".join(eksik)]
    anahtar = (os.path.abspath(kaynak_scripts), tuple(sorted({(k, tablo[k]) for k, _ in _DAVRANIS})))
    if anahtar not in _DAVRANIS_ONBELLEK:
        with ThreadPoolExecutor(max_workers=2) as havuz:
            ft = havuz.submit(_takma_kos, kaynak_scripts, lambda k: k)
            fe = havuz.submit(_takma_kos, kaynak_scripts, lambda k: tablo[k])
            try:
                tr_s, en_s = ft.result(), fe.result()
            except Exception as e:   # noqa: BLE001 — havuz kurulamazsa KIRMIZI + sebebi (sessiz gecis YOK)
                _DAVRANIS_ONBELLEK[anahtar] = ["[DAVRANIS] kum havuzu kurulamadi: %r" % e]
                return list(_DAVRANIS_ONBELLEK[anahtar])
        bulgu = []
        for i, ((komut, _a), (kt, ct), (ke, ce)) in enumerate(zip(_DAVRANIS, tr_s, en_s), 1):
            ad = "adim %d `%s` ≡ `%s`" % (i, komut, tablo[komut])
            if kt is None or ke is None:
                # zaman asimi iki havuzda AYNI sentinel'i uretir: esit sayilirsa OLCULEMEDI yesile yazilirdi
                bulgu.append("[DAVRANIS] %s: OLCULEMEDI (zaman asimi) — olculemeyene 'esit' denmez" % ad)
            elif kt != 0:
                # taze projede her adim 0 doner (olculdu); ikisi de AYNI sekilde cokerse esitlik bos bir kanittir
                bulgu.append("[DAVRANIS] %s: KANONIK taraf exit %s (0 bekleniyor): karsilastirma anlamsiz" % (ad, kt))
            elif (kt, ct) != (ke, ce):
                bulgu.append("[DAVRANIS] %s: exit %s/%s; %s" % (ad, kt, ke, _ilk_fark(ct, ce)))
        _DAVRANIS_ONBELLEK[anahtar] = bulgu
    return list(_DAVRANIS_ONBELLEK[anahtar])


_SKILL_TAKMA = re.compile(r"^İngilizce takma adlar \(.*\):\s*((?:`[a-z][a-z-]*`\s*)+)\.?\s*$", re.M)


def kapi4_belge(tablo, skill_metni):
    """[BELGE] `skill/SKILL.md` gövdesindeki takma ad satiri README tablosunun KOPYASIDIR; ikisi ayni kume mi?
    (Paketle kullaniciya giden SKILL.md'dir: olculmeyen ikinci bir kopya sessizce ayrisirdi.)"""
    m = _SKILL_TAKMA.search(skill_metni or "")
    if not m:
        return ["[BELGE] SKILL.md'de 'Ingilizce takma adlar (...): `ad` ...' satiri bulunamadi"]
    skill = set(re.findall(r"`([a-z][a-z-]*)`", m.group(1)))
    readme = {v for v in tablo.values() if v}
    return (["[BELGE] SKILL.md `%s` diyor, README tablosunda YOK" % x for x in sorted(skill - readme)]
            + ["[BELGE] README `%s` diyor, SKILL.md satirinda YOK" % x for x in sorted(readme - skill)])


def kapi4_takma_ad(metin, kaynak_scripts, skill_metni=None):
    """KAPI-4: README'nin takma ad tablosu motorla ve SKILL.md kopyasiyla tutuyor mu? Bulgular eksen etiketli
    ([TABLO] [YARDIM] [KUME] [DAVRANIS] [BELGE]); eksenler birbirine bagli degil — biri kirmiziyken oteki de kosar
    (ortusen tespit gorunur). `skill_metni` None ise motorun skill/SKILL.md'si diskten okunur."""
    tablo, bulgu = takma_tablosu(metin)
    if tablo is None:
        return bulgu
    if skill_metni is None:
        with open(os.path.join(os.path.dirname(os.path.abspath(kaynak_scripts)), "SKILL.md"),
                  encoding="utf-8", newline="") as f:
            skill_metni = f.read()
    return bulgu + kapi4_yardim(tablo, kaynak_scripts) + kapi4_kume(tablo, kaynak_scripts) \
        + kapi4_davranis(tablo, kaynak_scripts) + kapi4_belge(tablo, skill_metni)


def kapi4_eksen_kumesi(bulgu):
    """Bulgulardaki eksen etiketleri kumesi: ornek {'DAVRANIS', 'KUME', 'YARDIM'}."""
    return frozenset(b[1:b.index("]")] for b in bulgu)


def kapi4_eksenler(bulgu):
    """Ayni kume, sirali ve okunur: 'DAVRANIS+KUME+YARDIM' (bos ise '-')."""
    return "+".join(sorted(kapi4_eksen_kumesi(bulgu))) or "-"


# --------------------------------------------------------------- KAPI-2 (canli)
def kapi2_gercek(adimlar, kaynak_scripts, kanit_onbellek=None):
    """Blogu KOSAR ve her beyani gercekle karsilastirir.

    kanit_onbellek None ise agir kosucular (t_y3/t_y42) KOSAR ve yakalanir;
    dolu ise YENIDEN KULLANILIR (mutant turlari kosucuyu degil KARSILASTIRMAYI
    sinar — bu SINIR araciin basliginda yazilidir).
    Doner: (bulgu, kanit_onbellek, son_isir_ciktisi)"""
    bulgu, son = [], ""
    onbellek = dict(kanit_onbellek) if kanit_onbellek is not None else {}
    yeniden_kos = kanit_onbellek is None
    gecici = tempfile.mkdtemp(prefix="readme-kapisi-")
    try:
        calisma = os.path.join(gecici, "scripts")
        shutil.copytree(kaynak_scripts, calisma,
                        ignore=shutil.ignore_patterns("__pycache__", "deneme"))
        cwd = calisma
        for tur, komut, beyan in adimlar:
            if tur == "CD":
                continue                       # blok zaten `skill/scripts`e giriyor
            if tur == "MKDIR":
                os.makedirs(os.path.join(cwd, komut.split()[-1]), exist_ok=True)
                continue
            if tur == "GIT":
                hedef = os.path.join(cwd, komut.split()[-1])
                os.makedirs(hedef, exist_ok=True)
                p = subprocess.run(["git", "init", "-q", hedef],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if p.returncode != 0:
                    bulgu.append("`git init` basarisiz: %s"
                                 % p.stdout.decode("utf-8", "replace")[:120])
                continue
            if tur == "KANIT":
                if yeniden_kos:
                    p = subprocess.run([sys.executable] + shlex.split(komut)[1:], cwd=cwd,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    onbellek[komut] = {"kod": p.returncode,
                                       "cikti": p.stdout.decode("utf-8", "replace")}
                v = onbellek.get(komut)
                if not v:
                    bulgu.append("`%s` icin kosum kaydi YOK — olculemedi" % komut)
                    continue
                if v["kod"] != 0:
                    bulgu.append("`%s`: exit %d (kosucu KIRMIZI)" % (komut, v["kod"]))
                if beyan and beyan.get("senaryo") is not None:
                    gercek = kanit_sayisi(v["cikti"])
                    if gercek is None:
                        bulgu.append("`%s`: ciktidan senaryo sayisi AYIKLANAMADI "
                                     "(README %d diyor)" % (komut, beyan["senaryo"]))
                    elif gercek != beyan["senaryo"]:
                        bulgu.append("`%s`: README %d senaryo diyor, GERCEK %d"
                                     % (komut, beyan["senaryo"], gercek))
                continue
            # shlex SART: `--metin="ilk not"` ve `--ad "Deneme"` duz split ile bozulur
            # (olculdu: bozuk arguman -> her komut exit 2, arac README'yi suclardi).
            arg = shlex.split(komut)[2:]       # "python3 hafiza.py" sonrasi
            p = subprocess.run([sys.executable, "hafiza.py"] + arg, cwd=cwd,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            c = p.stdout.decode("utf-8", "replace")
            if " isir " in komut + " ":
                son = c
            if not beyan:
                if p.returncode != 0:
                    bulgu.append("`%s` beyansiz ama exit %d dondu" % (komut, p.returncode))
                continue
            if beyan["exit"] is not None and p.returncode != beyan["exit"]:
                bulgu.append("`%s`: README `exit %d` diyor, GERCEK exit %d"
                             % (komut, beyan["exit"], p.returncode))
            m = _SONUC.search(c)
            if beyan["oran"] is not None:
                if not m:
                    bulgu.append("`%s`: README %d/%d diyor ama motor SONUC satirini basmadi"
                                 % (komut, beyan["oran"][0], beyan["oran"][1]))
                elif (int(m.group(1)), int(m.group(2))) != beyan["oran"]:
                    bulgu.append("`%s`: README %d/%d diyor, GERCEK %s/%s"
                                 % (komut, beyan["oran"][0], beyan["oran"][1],
                                    m.group(1), m.group(2)))
            if beyan["sinanmadi"] is not None and m and int(m.group(3)) != beyan["sinanmadi"]:
                bulgu.append("`%s`: README %d SINANMADI diyor, GERCEK %s"
                             % (komut, beyan["sinanmadi"], m.group(3)))
        return bulgu, onbellek, son
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


# --------------------------------------------------------------- MUTANTLAR
def m1_beyan_silinir(s):
    """`exit 2` beyani yorumdan silinir -> KAPI-1 isirmali (KAPI-2 o beyani olcmez)."""
    yeni = s.replace("# taze projede: 67/67 + 2 SINANMADI, exit 2",
                     "# taze projede", 1)
    return yeni if yeni != s else None


def m2_oran_bozulur(s):
    """README yanlis mutant orani yazar -> KAPI-2 isirmali."""
    yeni = s.replace("67/67 + 2 SINANMADI", "66/66 + 2 SINANMADI", 1)
    return yeni if yeni != s else None


def m3_cikis_kodu_bozulur(s):
    """README yanlis cikis kodu yazar -> KAPI-2 isirmali (oranlar dogru kalir)."""
    yeni = s.replace("# derle sonrası: 69/69, exit 0", "# derle sonrası: 69/69, exit 3", 1)
    return yeni if yeni != s else None


def m4_sozlesme_eksilir(s):
    """README `isir` sozlesmesinden bir kod duser -> KAPI-3 isirmali."""
    yeni = s.replace("`2` ölçülemeyen mutant · `4` temiz sürüm zaten FAIL",
                     "`2` ölçülemeyen mutant", 1)
    return yeni if yeni != s else None


def m5_ty3_sayisi(s):
    """README t_y3 icin yanlis senaryo sayisi yazar -> KAPI-2 isirmali."""
    yeni = s.replace("# 20 senaryo, temiz hata", "# 21 senaryo, temiz hata", 1)
    return yeni if yeni != s else None


def m6_ty42_sayisi(s):
    """README t_y42 icin yanlis senaryo sayisi yazar -> KAPI-2 isirmali."""
    yeni = s.replace("# 58 senaryo", "# 59 senaryo", 1)
    return yeni if yeni != s else None


def m7_skill_kur_kodu_dustu(s):
    """README `skill-kur` sozlesmesinden `3` dusmus (BULGU'nun ta kendisi) -> KAPI-3 isirmali."""
    yeni = s.replace("`3` dosya sistemi yazmaya izin vermedi (kurulum tamamlanmadı) ya da beklenmeyen hata (hüküm yok)", "", 1)
    return yeni if yeni != s else None


def m9_kod_ve_nokta_birlikte_dustu(s):
    """`3` VE paragrafin son noktasi birlikte silinir (bagimsiz turun yeniden urettigi kor nokta): eski regex
    komsu `paket` paragrafina tasiyip kapiyi sessizce YESIL basiyordu -> KAPI-3 isirmali."""
    yeni = s.replace(" ·\n`3` dosya sistemi yazmaya izin vermedi (kurulum tamamlanmadı) ya da beklenmeyen hata (hüküm yok).", "", 1)
    return yeni if yeni != s else None


def m8_paket_kodu_bozulur(s):
    """README `paket` sozlesmesinde yanlis kod -> KAPI-3 isirmali (skill-kur satiri dokunulmaz)."""
    yeni = s.replace("`3` dosya sistemi yazmaya izin vermedi (paket üretilmedi)",
                     "`4` dosya sistemi yazmaya izin vermedi (paket üretilmedi)", 1)
    return yeni if yeni != s else None


def _tek(s, eski, yeni):
    """`eski` s'de TAM 1 kez gecmiyorsa None (mutant yanlis yere kurulmasin); gecerse degistirir."""
    return s.replace(eski, yeni, 1) if s.count(eski) == 1 else None


def m_ad1_motorda_silindi(s):
    """MOTOR mutanti: `gate` takma adi motorun sozlugunden silinir; README hala `gate`i vaat ediyor
    -> KAPI-4 isirmali (README'nin baska kapilari motorun alt komut adlarina bakmaz)."""
    return _tek(s, '    "kapi": "gate",\n', "")


def m_ad2_motorda_takas(s):
    """MOTOR mutanti: `gate` ile `bite` yer degistirir (ikisi de VAR, ikisi de YANLIS alt komuta gider; komut
    KUMESI ayni kalir, yalniz [YARDIM] ve [DAVRANIS] gorebilir) -> KAPI-4 isirmali."""
    x = _tek(s, '"kapi": "gate"', '"kapi": "bite"')
    return None if x is None else _tek(x, '"isir": "bite"', '"isir": "gate"')


def m_ad3_readme_olmayan_ad(s):
    """README MOTORDA OLMAYAN bir takma ad vaat eder (`hook` icin `install-hook`) -> KAPI-4 isirmali; motor
    ve cekirdek bes esleme DOKUNULMAZ."""
    return _tek(s, "| `hook` | — (takma ad yok) |", "| `hook` | `install-hook` |")


def m_ad4_motorda_dagitim_dusuyor(s):
    """MOTOR mutanti: `note` takma adi ile cagrilinca komut SESSIZCE exit 0 verip hicbir sey yapmaz (argparse `--help`i
    dagitimdan ONCE isler: [YARDIM] [KUME] goremez) -> yalniz [DAVRANIS] gorebilir."""
    return _tek(s, "    a = ap.parse_args()\n", '    a = ap.parse_args()\n    if a.komut == "note":\n        sys.exit(0)\n')


def m_ad5_readme_cekirdek_dustu(s):
    """README cekirdek komut `kapi`nin takma adini tablodan DUSURUR -> [TABLO] (cekirdek bes komut zorunlu)."""
    return _tek(s, "| `kapi` | `gate` |", "| `kapi` | — (takma ad yok) |")


def m_ad6_motorda_belgesiz_ad(s):
    """MOTOR mutanti: motor README'de OLMAYAN bir takma ad kabul eder (`hook` icin `install-hook`) -> [KUME]'nin
    'motor kabul ediyor, README'de YOK' yonu (README'den motora yon: m_ad3)."""
    return _tek(s, '    "paket": "package",\n}', '    "paket": "package",\n    "hook": "install-hook",\n}')


def m_ad7_skill_kopyasi_ayrisir(s):
    """SKILL.md'deki takma ad satiri (README tablosunun KOPYASI) ayrisir: `gate` -> `check` -> [BELGE]."""
    return _tek(s, "`protect` `gate` `bite`", "`protect` `check` `bite`")


_AD1 = frozenset({"DAVRANIS", "KUME", "YARDIM"})
# (ad, tur, mutasyon, beklenen kapi, KAPI-4 icin TAM beklenen alt-eksen kumesi): tur README ise mutasyon README
# METNINI, MOTOR ise motor kaynagini, SKILL ise SKILL.md metnini bozar. KAPI-4 mutantlarinda atesleyen alt eksenler
# beklenenle BIREBIR ayni olmak zorundadir: "KAPI-4 kirmizi" demek yetmez, her alt eksen KENDI mutantiyla kanitlanir
# (bagimsiz inceleme 1 Eki 2026: [DAVRANIS] olu olsa 12/12 mutant yine ISIRDI diyecekti).
MUTANTLAR = [
    ("M-1 beyan yorumdan silindi", "README", m1_beyan_silinir, "KAPI-1", None),
    ("M-2 README yanlis oran yaziyor", "README", m2_oran_bozulur, "KAPI-2", None),
    ("M-3 README yanlis cikis kodu", "README", m3_cikis_kodu_bozulur, "KAPI-2", None),
    ("M-4 sozlesmeden kod dustu", "README", m4_sozlesme_eksilir, "KAPI-3", None),
    ("M-5 t_y3 senaryo sayisi yanlis", "README", m5_ty3_sayisi, "KAPI-2", None),
    ("M-6 t_y42 senaryo sayisi yanlis", "README", m6_ty42_sayisi, "KAPI-2", None),
    ("M-7 skill-kur sozlesmesinden 3 dustu", "README", m7_skill_kur_kodu_dustu, "KAPI-3", None),
    ("M-8 paket sozlesmesinde yanlis kod", "README", m8_paket_kodu_bozulur, "KAPI-3", None),
    ("M-9 skill-kur 3 ve noktasi birlikte dustu", "README", m9_kod_ve_nokta_birlikte_dustu, "KAPI-3", None),
    ("M-AD-1 motorda `gate` takma adi silindi", "MOTOR", m_ad1_motorda_silindi, "KAPI-4", _AD1),
    ("M-AD-2 motorda gate<->bite yer degistirdi", "MOTOR", m_ad2_motorda_takas, "KAPI-4",
     frozenset({"DAVRANIS", "YARDIM"})),
    ("M-AD-3 README motorda olmayan ad vaat ediyor", "README", m_ad3_readme_olmayan_ad, "KAPI-4",
     frozenset({"BELGE", "KUME", "YARDIM"})),
    ("M-AD-4 motorda `note` dagitimda sessizce dusuyor", "MOTOR", m_ad4_motorda_dagitim_dusuyor, "KAPI-4",
     frozenset({"DAVRANIS"})),
    ("M-AD-5 README cekirdek `kapi` takma adini dusurdu", "README", m_ad5_readme_cekirdek_dustu, "KAPI-4",
     frozenset({"BELGE", "DAVRANIS", "KUME", "TABLO"})),
    ("M-AD-6 motor README'de olmayan ad kabul ediyor", "MOTOR", m_ad6_motorda_belgesiz_ad, "KAPI-4",
     frozenset({"KUME"})),
    ("M-AD-7 SKILL.md takma ad kopyasi ayristi", "SKILL", m_ad7_skill_kopyasi_ayrisir, "KAPI-4",
     frozenset({"BELGE"})),
]


def motor_kopyasi(kaynak_scripts, boz):
    """MOTOR mutanti icin skill/ agacinin GECICI kopyasi: (kok, scripts yolu); mutasyon uygulanamazsa
    (desen motorda TAM 1 kez yok) None. Cagiran `kok`u siler."""
    with open(os.path.join(kaynak_scripts, "hafiza.py"), encoding="utf-8", newline="") as f:
        kaynak = f.read()
    yeni = boz(kaynak)
    if yeni is None or yeni == kaynak:
        return None
    kok = tempfile.mkdtemp(prefix="readme-motor-mutanti-")
    shutil.copytree(os.path.dirname(os.path.abspath(kaynak_scripts)), os.path.join(kok, "skill"),
                    ignore=shutil.ignore_patterns("__pycache__", "deneme*"))
    scripts = os.path.join(kok, "skill", "scripts")
    with open(os.path.join(scripts, "hafiza.py"), "w", encoding="utf-8", newline="") as f:
        f.write(yeni)
    return kok, scripts


_KAPI2_ONBELLEK = {}


def _motor_sha(kaynak_scripts):
    with open(os.path.join(kaynak_scripts, "hafiza.py"), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def hukum(metin, kaynak_scripts, kanit_onbellek=None, skill_metni=None):
    """(k1, k2, k3, k4, onbellek) — blok cozulemezse None doner (OLCULEMEDI). KAPI-4 (iki kum havuzunda
    takma ad davranisi, `isir` dahil) KAPI-2 ile ES ZAMANLI kosar: ikisi de pahali ve birbirinden bagimsiz.
    KAPI-2 (README blogunun gercek kosumu) YALNIZ motor + blok metni DEGISINCE yeniden kosar: yalniz sozlesme
    paragrafini ya da takma ad tablosunu bozan mutantlar kosulacak blogu degistirmez, sonuc ayni olmak zorundadir."""
    blok = blok_bul(metin)
    if blok is None:
        return None
    adimlar = satirlari_coz(blok)
    bilinmeyen = [k for t, k, _ in adimlar if t == "BILINMEYEN"]
    if bilinmeyen:
        return ("BILINMEYEN", bilinmeyen)
    k1 = kapi1_beyan(adimlar)
    anahtar2 = (_motor_sha(kaynak_scripts), blok)
    with ThreadPoolExecutor(max_workers=1) as havuz:
        f4 = havuz.submit(kapi4_takma_ad, metin, kaynak_scripts, skill_metni)
        if kanit_onbellek is not None and anahtar2 in _KAPI2_ONBELLEK:
            k2, son = _KAPI2_ONBELLEK[anahtar2]
            onbellek = dict(kanit_onbellek)
        else:
            k2, onbellek, son = kapi2_gercek(adimlar, kaynak_scripts, kanit_onbellek)
            _KAPI2_ONBELLEK[anahtar2] = (k2, son)
        k4 = f4.result()
    k3 = kapi3_sozlesme(metin, son) + kapi3_komut_sozlesmesi(metin, kaynak_scripts)
    return (k1, k2, k3, k4, onbellek)


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else README
    kaynak = os.path.join(KOK, "skill", "scripts")
    if not os.path.isfile(yol):
        print("SONUC: ÖLÇÜLEMEDİ — README yok: %s" % yol)
        return 2
    if shutil.which("git") is None:
        print("SONUC: ÖLÇÜLEMEDİ — `git` yok; blok `git init` istiyor.")
        return 2
    with open(yol, encoding="utf-8", newline="") as f:
        metin = f.read()

    print("=== README KANIT BLOGU KAPISI === %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    h = hukum(metin, kaynak)
    if h is None:
        print("SONUC: ÖLÇÜLEMEDİ — 'Kanitini kendin kos' blogu bulunamadi.")
        return 2
    if h[0] == "BILINMEYEN":
        print("  BLOK            : TANIMADIGIM SATIR VAR — sessiz atlama YOK")
        for k in h[1]:
            print("      ? %s" % k)
        print("\nSONUC: ÖLÇÜLEMEDİ — blok cozulemedi; araca yeni satir turu ogretilmeli.")
        return 2
    k1, k2, k3, k4, onbellek = h
    with open(os.path.join(os.path.dirname(kaynak), "SKILL.md"), encoding="utf-8", newline="") as f:
        skill_metni = f.read()
    print("  KAPI-1 BEYAN    : %s" % ("YESIL (beyanlar ayiklanabiliyor)" if not k1
                                      else "KIRMIZI — %d bulgu" % len(k1)))
    for x in k1:
        print("      ! %s" % x)
    print("  KAPI-2 GERCEK   : %s" % ("YESIL (README'nin her sayisi GERCEKLE tuttu)" if not k2
                                      else "KIRMIZI — %d bulgu" % len(k2)))
    for x in k2:
        print("      ! %s" % x)
    print("  KAPI-3 SOZLESME : %s" % ("YESIL (README ile motor ayni kod kumesi)" if not k3
                                      else "KIRMIZI — %d bulgu" % len(k3)))
    for x in k3:
        print("      ! %s" % x)
    print("  KAPI-4 TAKMA AD : %s" % ("YESIL (README tablosu motorla tutuyor: yardim · komut kumesi · davranis)"
                                      if not k4 else "KIRMIZI — %d bulgu" % len(k4)))
    for x in k4:
        print("      ! %s" % x)
    for k, v in sorted(onbellek.items()):
        n = kanit_sayisi(v["cikti"])
        print("  KOSUCU          : `%s` exit %d · ciktidan %s senaryo "
              "(`kanit` isindeki kopyasi continue-on-error TASIR; buradaki TASIMAZ)"
              % (k, v["kod"], n if n is not None else "?"))
    if k1 or k2 or k3 or k4:
        print("\nSONUC: KIRMIZI — README'nin beyani gercekle TUTMUYOR.")
        return 1

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    for ad, tur, boz, beklenen, eksenler in MUTANTLAR:
        motor_kok, kaynak_m, metin_m, skill_m = None, kaynak, metin, None
        try:
            if tur == "MOTOR":
                kopya = motor_kopyasi(kaynak, boz)
                motor_kok, kaynak_m = kopya if kopya else (None, None)
            elif tur == "SKILL":
                skill_m = boz(skill_metni)
                if skill_m is None:
                    metin_m = None
            else:
                metin_m = boz(metin)
            if kaynak_m is None or metin_m is None:
                print("  %-34s KURULAMADI (desen %s'de TAM 1 kez yok)"
                      % (ad, {"MOTOR": "motor", "SKILL": "SKILL.md"}.get(tur, "README")))
                kacan += 1
                continue
            b = hukum(metin_m, kaynak_m, onbellek, skill_m)   # agir kosucular (t_y3/t_y42) YENIDEN kosmaz
        finally:
            if motor_kok:
                shutil.rmtree(motor_kok, ignore_errors=True)
        if b is None or b[0] == "BILINMEYEN":
            print("  %-34s -> BLOK COZULEMEDI (mutant kapiyi degil ayirici yi bozdu)" % ad)
            kacan += 1
            continue
        ates = [a for a, v in (("KAPI-1", b[0]), ("KAPI-2", b[1]), ("KAPI-3", b[2]), ("KAPI-4", b[3])) if v]
        # KAPI-4 mutantlarinda hangi ALT eksenin atesledigi de basilir ve BEKLENENLE BIREBIR ayni olmak zorundadir
        # (ortusen tespit gorunur, olu bir alt eksen 'KAPI-4 kirmizi' ortusunun ardinda saklanamaz); KAPI-1/2/3 ise
        # "yesil kaldi" diye AYRI raporlanir: ates listesinde yoklarsa yesildirler.
        ek = "  [KAPI-4 eksenleri: %s]" % kapi4_eksenler(b[3]) if beklenen == "KAPI-4" else ""
        if ates == [beklenen] and eksenler is not None and kapi4_eksen_kumesi(b[3]) != eksenler:
            print("  %-34s -> ISIRDI ama EKSEN FARKLI ✗%s (beklenen: %s)" % (ad, ek, "+".join(sorted(eksenler))))
            kacan += 1
        elif ates == [beklenen]:
            print("  %-34s -> ISIRDI ✓  (%s)%s%s" % (ad, beklenen, ek, "  [KAPI-1/2/3: yesil kaldi]" if ek else ""))
        elif beklenen in ates:
            print("  %-34s -> ISIRDI ama ORTUSTU: %s%s" % (ad, " + ".join(ates), ek))
            kacan += 1
        else:
            print("  %-34s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                  % (ad, beklenen, " + ".join(ates) or "hicbiri"))
            kacan += 1

    if kacan:
        print("\nSONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
              % (kacan, len(MUTANTLAR)))
        return 1
    print("\nSONUC: YESIL — dort kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

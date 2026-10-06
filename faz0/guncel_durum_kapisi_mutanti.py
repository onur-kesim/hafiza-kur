#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — GUNCEL DURUM KAPISI MUTANTI (besli-paket/IS_EMRI_GUNCEL_DURUM_KAPISI.md).

NEDEN VAR (olculdu 8 Eyl 2026, besli-paket/OLCUM_RAPORU_8EYL_DENEME_KAPANIS.md,
Momentum kopyasinda GERCEKTEN OLCULDU)
  Momentum kopyasinda dort gercek `not` yazildi, dordu de exit 0 verdi ve
  "FRAGMAN: gunluk/...md" dedi. Ardindan `derle`:
      ATLANDI (bolum yok: ## GUNCEL DURUM): ...  (x4)
      DERLENDI: 0 fragman islendi ve arsive tasindi.
  `derle` exit 0. Ve `kapi`:
      SONUC: YESIL — olculen her sey gecti.        exit 0
  Kullanici dort not yazdi, arac "kaydedildi" dedi, hicbiri canli deftere
  girmedi, kapi "her sey gecti" dedi. Aracin var olma sebebi kayit tutmak.

  Kok sebep: `devral` `zorunlu_bolumler`i PROJEDE ONCEDEN VAROLAN basliklardan
  turetir (KALEM 1, 6 Eyl 2026 kilidi: "diskteki gercek ustundur" — DEGISTIRILMEZ).
  Momentum'un DURUM.md'sinde `## GUNCEL DURUM` hic yoktu, dolayisiyla H3 onu
  "zorunlu" saymadi ve HIC anmadi. `derle` de hedef bolum yoksa fragmani
  sessizce ATLAYIP exit 0 doner. Iki katman birlikte, bir yapilandirma
  eksigini TAMAMEN gorunmez kilar.

NE OLCER — UC KOL, UC AYRI EKSEN (Onur kilidi: K1+K3 -> "kapi her zaman bulgu
versin" (`devral`a DOKUNULMAZ) · K2 -> "`derle` exit 2 = OLCULEMEDI")
  KAPI-1 (KALEM 1, `_kapi_h17`) — `## GUNCEL DURUM` YOK, henuz HIC not
      yazilmamis taze bir kurulumda BILE: `kapi` bulgu URETIR (fragman sarti
      YOK), cikti bolumu ADLANDIRIR. Fixture Momentum'un kurulum-sonrasi
      haliyle BIREBIR ayni sinif: `devral --esle` ile mevcut basliklardan
      turetilmis bir proje (H3 bunu HIC anmaz, H17 KOSULSUZ anar).
      MUTANT (M-A): bu olcumu sokan mutant (H17 kosulu HER ZAMAN False) ISIRIR.
  KAPI-2 (KALEM 2, `derle`) — bolum YOK + fragman VAR: `derle` exit 2 doner,
      "ATLANDI" satirlari AYNEN basilir, fragmanlar gunluk/'te DURUR (SILINMEZ,
      arsive TASINMAZ).
      MUTANT (M-B): exit'i 0'a donduren mutant ISIRIR.
  KAPI-3 (KONTROL KOLU, yanlis pozitif ekseni AYRI olculur — ortusen tespit
      korlugune dusulmez) — bolum VAR: `kapi` bu eksende TEMIZ (H17 hic
      konusmaz), `derle` exit 0, fragman islenip arsive TASINIR.
      MUTANT (M-C): KALEM 1'in bulgusunu KOSULSUZ ureten mutant (H17 kosulu
      HER ZAMAN True) — bolum VARKEN de FIRE eder — ISIRIR.

K-SATIR (H18) — besli-paket/IS_EMRI_KSATIR_KARARYOLU.md (5 Eki 2026, Onur kilidi), AYNI BETIGE EK KOLLAR
  Olculen vaka (Momentum kopyasi): canli defterde "`SENKRON_SUNUCU_URL` = `main.dart:25`", L25 bugun bir
  import, tanim L31-32 — defter ile kod ayrismisti, hicbir kapi gormedi. H18 numarali maddelerdeki
  backtick'li `yol:N` atfini olcer; `kapi` uyarir (EXIT DEGISMEZ), `derle` ayni listeyi canliya
  `sahip="hafiza-kur"` blogu yazar. YEDI KOL (her biri AYRI etiketli eksen) + 12 SABOTAJ, her sabotaj YALNIZ
  kendi etiketini ateslemeli (baska eksenler kaskad olarak atesleyebilir: BILGI basilir):
    dongu    KONTROL (kayma yok: H18 TUTUYOR, blok yok) · KAYMA (a.py:3 -> 8) · EXIT (kapi exit 0) · BLOK
             (derle sahip=hafiza-kur blogu) · MUHASEBE (kapi + kapi --siki exit 0) · IDEMPOTANS (ayni
             kayma, ikinci derle: blok DEGISMEZ, arsive kopya GIRMEZ) · KALDIRMA (kayma giderildi: blok
             arsive TASINIR, silinmez)
    tanimsiz YANLIS ALARM: tanimlayicisiz madde KAYMA degil OLCULEMEDI
    sahiplik sahip="proje" blogu varken motor ONA DOKUNMAZ, ikinci blok acmaz (is emri KISIT 2)
    kume     H18 dosya budamasi H14'unkiyle AYNI (motor KAYNAGINDAN ast ile okunur)
    cokkopya budanan dizinde cift kopya gozardi, budanmayan nokta-dizinde OLCULEMEDI [DOSYA_COK]
             (beklenti motorun sabitinden DEGIL elle yazili: paylasilan kural = paylasilan korluk)
    gitsiz   .git YOKKEN ayni sonuc; iki kosum bayt-ayni (determinizm)
    aralik   yol:N-M penceresi [N-2, M+2]; satir dosya disi -> OLCULEMEDI [SATIR_DISI]
  H18 `isir` kataloguna GIRMEZ (79/79 · 81/81 sayilari sabit); bu betik onu isirtir.

K-YOL (devral karar dizini) — AYNI betige ek kollar (besli-paket/IS_EMRI_KSATIR_KARARYOLU.md, Onur kilidi)
  Olculen (Momentum): `docs/ADR/` dolu, DURUM.md'de ADR atfi 0, kor okumada KARAR sorulari 0/4. `devral`
  projenin MEVCUT karar dizinini (docs/ADR · docs/adr · docs/decisions · adr · doc/adr; harf duyarsiz) bulur,
  canliya `sahip="hafiza-kur"` blogu (konu `karar-kaynagi`: dizin + dosya SAYISI + dosya ADLARI + ilk `# `
  basligi <=80 kr) yazar, `.hafizarc`a `karar_dizini` kaydeder, ozet satirini basar; `derle` blogu her
  fragman-isleyen kosuda DISKTEN yeniden uretir (dizin silinirse 'YOK (kayitli: ...)' der). DOSYALARA DOKUNULMAZ.
  YEDI KOL: ykontrol (ADR'siz: 'bulunamadi', anahtar/blok/konu YOK) · yadr (YOZET · YRC · YBLOK · YSAYIM · YMASKE ·
  YKONU · YBACKTICK · YDOKUNMA [bayt-bayt, fikstur iceriginden], devral SONRASI derle zinciri: YYENILE ·
  IDEMPOTANS · YKAYIP, her adimda kapi + kapi --siki) · ysahiplik (sahip=proje blok korunur) · ycase (`Docs/Adr`
  gercek yazimla) · ycok (cok aday: ILK kaydedilir, digeri 'baska aday' GORUNUR; baslik yokken blok dosyanin
  USTUNDE: YYER) · ykesif (`--kesif` raporlar, diske HIC yazmaz) · ykacis (proje DISINA bagli dizin OKUNMAZ ama ozette ATLANDI diye GORUNUR; Win junction, POSIX symlink). 16 sabotaj, her biri kendi etiketini ateslemeli.
  SINIR (gizlenmez): kurulu proje (`.hafizarc` var) devral'i REDDEDER; karar dizini yalniz devral anindaki ADR'li
  proje icin kaydedilir. Momentum'da desene uyan 5 dosya + `.gitkeep` var; `.gitkeep` ADR degildir, sayilmaz.
  TERIM: is emri "(iii) sabotajda (ii) KACTI gorunmeli" der; bu betigin sozlugunde o durum ISIRDI'dir
  (kol sabotajli motorda KIRMIZI yanar = kapi kor DEGIL). KACTI = sabotaj kolu kirmizi YAKMADI = kapi KOR.

K-GECIS — AYNI betige ek kol (besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md, 6 Eki 2026, Onur kilidi)
  Olculen (kurulu Momentum): `devral` exit 2 `.hafizarc ZATEN VAR` => mevcut kurulumlar `karar-kaynagi` hic alamiyordu.
  `derle`, `.hafizarc`ta `karar_dizini` ANAHTARI HIC YOKSA K-YOL'un AYNI keşif fonksiyonunu (`_karar_ilk`) BIR KEZ
  kosar, bulursa yazar + `KARAR DIZINI KESFEDILDI: docs/ADR (N) — .hafizarc'a yazildi` der; bulamazsa
  `"karar_dizini": ""` yazar + beyan eder. `""` BILINCLI bos degerdir: sonraki derle taramaz. Mevcut `.hafizarc`
  baytlarina dokunulmaz (anahtar sona eklenir). BIR KOL (`kgecis`): KGKESIF · KGBEYAN · KGBLOK · KGRC · KGTEKRAR
  (ikinci derle ayni, bayt-bayt) · KGYOK · KGBOS; 6 sabotaj (M-G1..M-G6, koşul-ters dahil).

K-ISARET — AYNI betige ek kol (besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md, 6 Eki 2026, Onur kilidi)
  Olculen: `kur`/`devral` yeni kural evine yalniz baslik + "Bu dosya her oturumda yuklenir" yaziyordu; canli defterin
  ADI yoktu => defter yalniz skill tetiklenirse okunuyordu (Cursor/Codex'te hic yol yok). Yeni kural evi 2. satirda
  `> Canli defter: <canli> — her oturum basinda once onu oku (hafiza-kur).` tasir; kural evi ZATEN VARSA dosya
  BAYT-BAYT ayni + cikti `ISARETCI YOK: ... eklemek icin: <satir>` der (motor yazmaz, soyler); `kapi` H19 kural evinde
  canli adi gecmiyorsa UYARIR (exit DEGISMEZ). AGENTS.md YAZILMAZ. BIR KOL (`kisaret`): KIKUR · KISESSIZ · KIKAPI ·
  KIEXIT · KIBAYT · KIONERI · KIDEVRAL; 7 sabotaj (M-I1..M-I7).

K-DURUM — AYNI betige ek kol (besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md, 6 Eki 2026, Onur kilidi)
  Olculen (Momentum kor okuma R1, iki tekrar YANLIS): `karar-kaynagi` blogu TASLAK bir ADR'ye (`Durum: TASLAK v6 —
  KILITLI DEGIL`) kilitlilerle AYNI agirlikta yol veriyordu; okuyucu taslagi karar sandi. Blok artik her ADR satirina
  dosyanin KENDI beyanini ekler: `- ad — baslik — [durum: DEGER]` (ilk 30 satirdaki `Durum`/`Status`, suslerden
  bagimsiz, ya da on-bilgi `durum:`; <=60 kr; yoksa `BEYANSIZ`). Motor YORUMLAMAZ/SIRALAMAZ/otorite SECMEZ.
  BIR KOL (`kdurum`, her biri AYRI etiketli eksen): KDURUM (beyan blokta: `**Durum:**` · on-bilgi · `Status :`) ·
  KKESME (uzun deger <=60) · KPENCERE (L30 icinde TUTAR, L32 sayilmaz) · KBEYANSIZ (anahtarsiz) · KSILINCE (satir
  silinince derle BEYANSIZ) · KMOTOR (motorun kendi `kararlar/` listesi de tasir) + kapi/kapi --siki; 5 sabotaj.

NE OLCMEZ
  K4 (H6 arsiv blogu icerik korlugu) BU DOSYADA DEGIL — Onur kilidiyle AYRI
  is emrine ertelendi (SIRADAKI). `devral`in KENDI davranisi (basligi
  eklememesi) burada DOGRU/DEGISMEZ kabul edilir, sinanmaz — sinanan KAPININ
  bunu YAKALAMASIdir.

CIKIS KODU  0 tum kollar temiz (uc + yedi K-SATIR + yedi K-YOL + bir K-DURUM + bir K-GECIS + bir K-ISARET) VE tum mutantlar/sabotajlar ISIRDI · 1 en az bir kol
            BEKLENMEDIK / mutant KACTI · 2 OLCULEMEDI (git yok, motor
            okunamadi, kurulum basarisiz — kapi hukmu DEGIL)
"""
import ast
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


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="gdkmut", GIT_AUTHOR_EMAIL="gdk@example.invalid",
                GIT_COMMITTER_NAME="gdkmut", GIT_COMMITTER_EMAIL="gdk@example.invalid",
                GIT_CONFIG_NOSYSTEM="1")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def kos(motor, arglar, kok, timeout=120):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args):
    return subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                          env=_GIT_ENV, check=False)


def hal_bolum_yok(motor, kok):
    """Momentum'un kurulum-sonrasi hali: mevcut projenin DURUM.md'sinde
    '## GUNCEL DURUM' HIC YOK; `devral --esle` bunu ONCEDEN VAROLAN
    basliklardan turetir ('devral DEGISMEZ' kilidi, KALEM 1 6 Eyl 2026) —
    H3 bu yuzden bolumu HIC anmaz, kapsam H17'nin KOSULSUZLUGUNU sinar."""
    os.makedirs(kok, exist_ok=True)
    r = subprocess.run(["git", "init", "-q", kok], capture_output=True)
    if r.returncode != 0:
        raise Kurulamadi("git init basarisiz")
    durum = os.path.join(kok, "DURUM.md")
    with open(durum, "w", encoding="utf-8", newline="\n") as f:
        f.write("# DURUM.md\n\n## Kalici dersler\n- ders 1\n\n"
                "## DILIM 3 - ISBIRLIGI\n- calisma\n\n## Bilinen sinirlar\n- sinir 1\n")
    _git(kok, "add", "-A")
    rc_commit = subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false",
                                "commit", "-q", "-m", "ilk"],
                               capture_output=True, env=_GIT_ENV)
    if rc_commit.returncode != 0:
        raise Kurulamadi("git commit basarisiz")
    rc, c = kos(motor, ["devral", "--esle=canli=DURUM.md", "--ad", "GDKMUT"], kok)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    return kok


def hal_bolum_var(motor, kok):
    """KONTROL KOLU (KAPI-3): normal `kur` — '## GUNCEL DURUM' VARSAYILAN
    sablonda zaten vardir, HICBIR SEY elle eklenmez/silinmez."""
    os.makedirs(kok, exist_ok=True)
    rc, c = kos(motor, ["kur", "--ad", "GDKMUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    return kok


_H17_IMZA = "GUNCEL DURUM"           # bulgu metninde bolumu ADLANDIRAN ortak parca
_H17_ETIKET = "[H17]"


def _h17_var_mi(cikti):
    return _H17_ETIKET in cikti and _H17_IMZA in cikti


def kapi1_bolum_yok_taze(motor, taban):
    """KAPI-1: HENUZ HIC not yazilmamis, bolum yok -> kapi bulgu URETMELI
    (fragman sarti YOK — KABUL OLCUTU 3)."""
    kok = hal_bolum_yok(motor, os.path.join(taban, "k1"))
    return kos(motor, ["kapi"], kok)


def kapi2_bolum_yok_fragman_var(motor, taban):
    """KAPI-2: bolum yok + fragman VAR -> `derle` exit 2, ATLANDI satirlari
    basilir, fragman gunluk/'te KALIR (SILINMEZ/tasinmiaz)."""
    kok = hal_bolum_yok(motor, os.path.join(taban, "k2"))
    rc0, c0 = kos(motor, ["not", "--konu=genel-durum",
                          "--metin=guncel durum kapisi mutanti icin ilk kayit"], kok)
    if rc0 != 0:
        raise Kurulamadi("not basarisiz: %s" % c0.strip().split("\n")[-1][:160])
    rc, c = kos(motor, ["derle"], kok)
    return rc, c, kok


def kapi3_bolum_var(motor, taban):
    """KAPI-3 KONTROL KOLU: bolum VAR -> `derle` exit 0, fragman islenip
    arsive tasinir; H17 hic konusmaz (yanlis pozitif yok)."""
    kok = hal_bolum_var(motor, os.path.join(taban, "k3"))
    rc0, c0 = kos(motor, ["not", "--konu=genel-durum",
                          "--metin=guncel durum kapisi mutanti kontrol kolu"], kok)
    if rc0 != 0:
        raise Kurulamadi("not basarisiz: %s" % c0.strip().split("\n")[-1][:160])
    rc, c = kos(motor, ["derle"], kok)
    return rc, c


# --------------------------------------------------------------------- MUTANT
# M-A/M-C AYNI satiri hedefler (`_kapi_h17`'nin kosulu) ama TERS yonlerde
# bozar: M-A hic ATESLEMEZ (False), M-C KOSULSUZ ateşler (True). `_kapi_h17`nin
# GOVDESI (imzasi degil) hedeflenir; `_kapi_govde`deki cagri yeri BU MUTANTLARIN
# HICBIRINDE degismez.
ANKOR_H17_KOSUL = ('    if not any(bas_eslesir(s, "## GUNCEL DURUM") for s in satirlar(y.canli) '
                   'if s.startswith("#")):\n')
YENI_MA = '    if False:      # MUTANT: H17 sokuldu\n'
YENI_MC = '    if True:       # MUTANT: H17 kosulsuz FIRE eder\n'

# M-B: KAPI-2'nin exit 2'sini SOKAR (bolum yok + fragman VAR dali).
ANKOR_MB = ("    kod, cikti = _kapi_kos(kok)\n"
           "    print(cikti.strip())\n"
           "    if not _bolum_var:\n")
YENI_MB = ("    kod, cikti = _kapi_kos(kok)\n"
          "    print(cikti.strip())\n"
          "    if False:      # MUTANT: KALEM 2 exit 2'si sokuldu\n")


def _sabotajli_yaz(kaynak, ankor, yeni, hedef_dizin, ad):
    n = kaynak.count(ankor)
    if n != 1:
        return None, "capa %d yerde gecti (1 olmali): %r" % (n, ankor.strip())
    metin = kaynak.replace(ankor, yeni, 1)
    try:
        compile(metin, "<%s>" % ad, "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(hedef_dizin, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p, None


def _sil(yol):
    """Gecici dizini SIL: Windows'ta salt-okunur git objeleri `ignore_errors=True` ile SESSIZCE kalirdi
    (motordaki `_gecici_sil` ile ayni teknik; kosumdan kosuma %TEMP% birikmesin)."""
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


# ===================================================================== K-SATIR (H18)
# besli-paket/IS_EMRI_KSATIR_KARARYOLU.md (5 Eki 2026, Onur kilidi). OLCULDU (Momentum kopyasi): canli
# defterde "`SENKRON_SUNUCU_URL` = `main.dart:25`" yaziyordu, L25 bugun bir import, tanim L31-32; hicbir
# kapi gormedi. H18 yalniz `canli`daki numarali maddelerin backtick'li `yol:N` atfini olcer (UYARI: exit
# degismez); `derle` ayni listeyi canliya `sahip="hafiza-kur"` blogu olarak yazar. HER KOL AYRI ETIKETLI
# bir eksendir; her sabotaj YALNIZ kendi ekseninin etiketini ateslemelidir (aksi: ORTUSME, kapi kor).
MADDE = "1. `HEDEF` tanimi = `a.py:3`"
A_PY = "# c\n# c\nHEDEF = 1\nx = 2\n"            # HEDEF L3
ONEK5 = "e1\ne2\ne3\ne4\ne5\n"                  # a.py basina 5 satir -> HEDEF L8
NOT_UZUN = "kol icin yeterince uzun bir not metni"
H18_SATIRI = re.compile(r"H18: (\d+) atif · (\d+) KAYMA · (\d+) OLCULEMEDI(?: \[([^\]]*)\])?")
BLOK_ATIF = re.compile(r'<!-- blok konu="atif-kaymasi"([^>]*)-->\n(.*?)\n<!-- /blok -->', re.S)


def _yaz(yol, metin):
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    with io.open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)


def _commit(kok, mesaj):
    _git(kok, "add", "-A")
    subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty",
                    "-m", mesaj], capture_output=True, env=_GIT_ENV)


def hal_satir(motor, kok, madde, dosyalar=None, git=True):
    """kur + dosyalar + `not` ile canliya madde (+ git commit). Fragman HENUZ derlenmedi."""
    os.makedirs(kok, exist_ok=True)
    if git and subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    rc, c = kos(motor, ["kur", "--ad", "ATIF"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    for ad, icerik in (dosyalar or {"a.py": A_PY}).items():
        _yaz(os.path.join(kok, *ad.split("/")), icerik)
    rc, c = kos(motor, ["not", "--konu=genel-durum", "--metin=" + madde], kok)
    if rc != 0:
        raise Kurulamadi("not basarisiz: %s" % c.strip().split("\n")[-1][:160])
    if git:
        _commit(kok, "ilk")
    return kok


def notdemle(motor, kok, konu, metin=NOT_UZUN):
    rc, c = kos(motor, ["not", "--konu=" + konu, "--metin=" + metin], kok)
    if rc != 0:
        raise Kurulamadi("not basarisiz: %s" % c.strip().split("\n")[-1][:160])
    return kos(motor, ["derle"], kok)


def _canli(kok):
    with io.open(os.path.join(kok, "PROJE_HAFIZA.md"), encoding="utf-8") as f:
        return f.read()


def _arsiv(kok):
    d = os.path.join(kok, "arsiv", "hafiza")
    out = ""
    for f in sorted(os.listdir(d)):
        if f.startswith("HAFIZA_") and f.endswith(".md"):
            with io.open(os.path.join(d, f), encoding="utf-8") as h:
                out += h.read()
    return out


def _h18(cikti):
    m = H18_SATIRI.search(cikti)
    return None if not m else (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "")


def ks_dongu(motor, taban, tag):
    """KONTROL -> KAYMA -> EXIT -> BLOK -> MUHASEBE -> IDEMPOTANS -> KALDIRMA (tek fikstur, yedi eksen).
    DONER [(etiket, mesaj)] — BOS liste = hepsi beklendigi gibi."""
    b = []
    kok = hal_satir(motor, os.path.join(taban, tag), MADDE)
    rc, c = notdemle(motor, kok, "sonraki-adim", "madde fragmani islensin diye ilk derle")
    if "DERLENDI: 2 fragman islendi" not in c:      # derle HIC calismadi: kurulum kusuru, eksen degil
        raise Kurulamadi("ilk derle fragmanlari islemedi (exit %s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    if rc != 0:                                    # derle calisti ama kapi hukmu kirmizi: H18 EXIT'i bozmus
        b.append(("EXIT", "kayma YOKKEN bile derle/kapi exit %s (0 olmali)" % rc))
    _commit(kok, "defterler")
    # KONTROL: kayma YOK -> H18 TUTUYOR (sessiz), blok YOK
    rc, c = kos(motor, ["kapi"], kok)
    if _h18(c) != (1, 0, 0, "") or "H18: KAYMA" in c:
        b.append(("KONTROL", "kayma YOKKEN H18 beklenmedik: %r" % (_h18(c),)))
    if "atif-kaymasi" in _canli(kok):
        b.append(("KONTROL", "kayma YOKKEN canliya blok yazilmis"))
    # KAYMA: a.py basina 5 satir -> HEDEF L3'ten L8'e kaydi
    _yaz(os.path.join(kok, "a.py"), ONEK5 + A_PY)
    _commit(kok, "kayma")
    rc, c = kos(motor, ["kapi"], kok)
    if rc != 0:
        b.append(("EXIT", "KAYMA var ama kapi exit %s (0 olmali: uyari, bulgu degil)" % rc))
    if not re.search(r"H18: KAYMA md\.1: a\.py:3 -> 8(?:\D|$)", c) or (_h18(c) or (0, 0))[1] != 1:
        b.append(("KAYMA", "KAYMA satiri 'md.1: a.py:3 -> 8' ciktida YOK: %r" % (_h18(c),)))
    rc, c = notdemle(motor, kok, "acik-kararlar")
    blok = BLOK_ATIF.search(_canli(kok))
    if rc != 0 or not blok or 'sahip="hafiza-kur"' not in blok.group(1) \
            or "md.1: a.py:3 -> 8" not in blok.group(2):
        b.append(("BLOK", "derle exit=%s; sahip=hafiza-kur 'atif-kaymasi' blogu (md.1: a.py:3 -> 8) YOK" % rc))
    rc1, _ = kos(motor, ["kapi"], kok)
    rc2, _ = kos(motor, ["kapi", "--siki"], kok)
    if rc1 != 0 or rc2 != 0:
        b.append(("MUHASEBE", "blok yazildiktan sonra kapi exit=%s · kapi --siki exit=%s (0/0 olmali)" % (rc1, rc2)))
    # IDEMPOTANS: ayni kayma, yeni fragman -> blok DEGISMEZ, arsive kopya GIRMEZ
    _commit(kok, "blok")
    rc, c = notdemle(motor, kok, "sonraki-adim", "ikinci derle ayni kayma ile")
    n_blok = len(re.findall(r'<!-- blok konu="atif-kaymasi"', _canli(kok)))
    if "'atif-kaymasi' blogu" in c or n_blok != 1 or 'konu="atif-kaymasi"' in _arsiv(kok):
        b.append(("IDEMPOTANS", "ayni kayma ile derle blogu YENIDEN yazdi (canli blok=%d, arsivde kopya=%s)"
                  % (n_blok, 'konu="atif-kaymasi"' in _arsiv(kok))))
    # KALDIRMA: kayma kodda giderildi -> blok arsive TASINIR (silinmez), kapi yesil
    _commit(kok, "blok2")
    _yaz(os.path.join(kok, "a.py"), A_PY)
    _commit(kok, "kayma giderildi")
    rc, c = notdemle(motor, kok, "acik-kararlar", "kayma giderildikten sonra derle")
    rc2, _ = kos(motor, ["kapi", "--siki"], kok)
    if "atif-kaymasi" in _canli(kok) or _arsiv(kok).count('konu="atif-kaymasi"') != 1 or rc != 0 or rc2 != 0:
        b.append(("KALDIRMA", "kayma giderildi ama blok canlida KALDI / arsive TASINMADI (derle=%s, siki=%s, "
                  "arsivde=%d)" % (rc, rc2, _arsiv(kok).count('konu="atif-kaymasi"'))))
    return b


def ks_tanimsiz(motor, taban):
    """YANLIS ALARM ekseni: maddede tanimlayici YOK -> KAYMA degil OLCULEMEDI; blok yazilmaz."""
    b = []
    kok = hal_satir(motor, os.path.join(taban, "ks_t"), "1. Yalniz `a.py:3` anildi, tanimlayici yok.",
                    {"a.py": ONEK5 + A_PY})
    rc, c = notdemle(motor, kok, "sonraki-adim")
    rk, ck = kos(motor, ["kapi"], kok)
    if _h18(ck) != (1, 0, 1, "TANIMLAYICI_YOK:1") or "atif-kaymasi" in _canli(kok) or rk != 0:
        b.append(("TANIMSIZ", "tanimlayicisiz madde: H18=%r, blok var=%s, exit=%s (beklenen 1 atif · 0 KAYMA · "
                  "1 OLCULEMEDI [TANIMLAYICI_YOK:1], blok yok, exit 0)"
                  % (_h18(ck), "atif-kaymasi" in _canli(kok), rk)))
    return b


def ks_sahiplik(motor, taban):
    """SAHIPLIK: ayni konuda sahip=proje blogu varsa motor ONA DOKUNMAZ ve ikinci blok ACMAZ; sinyal kapi'da kalir."""
    b = []
    kok = hal_satir(motor, os.path.join(taban, "ks_s"), MADDE, {"a.py": ONEK5 + A_PY})
    rc, c = kos(motor, ["not", "--konu=atif-kaymasi", "--yeni-konu=kullanicinin kendi konusu",
                        "--metin=KULLANICI METNI dokunulmamali"], kok)
    if rc != 0:
        raise Kurulamadi("not (atif-kaymasi) basarisiz: %s" % c.strip().split("\n")[-1][:160])
    rc, c = kos(motor, ["derle"], kok)
    metin = _canli(kok)
    bloklar = BLOK_ATIF.findall(metin)
    rk, ck = kos(motor, ["kapi"], kok)
    if (rc != 0 or len(bloklar) != 1 or 'sahip="proje"' not in bloklar[0][0]
            or "KULLANICI METNI dokunulmamali" not in bloklar[0][1] or "Motor (derle, H18)" in metin
            or rk != 0 or "H18: KAYMA" not in ck):
        b.append(("SAHIPLIK", "sahip=proje blok korunmadi: derle=%s blok=%d kapi=%s KAYMA-kapida=%s"
                  % (rc, len(bloklar), rk, "H18: KAYMA" in ck)))
    return b


def ks_kume(motor_metin):
    """KUME: H18'in dosya agaci budamasi H14'unkiyle AYNI (iki tanim ayrisamaz). Motor KAYNAGINDAN okunur."""
    h14 = atif = None
    for d in ast.walk(ast.parse(motor_metin)):
        if isinstance(d, ast.FunctionDef) and d.name == "_h14_adaylar":
            for x in ast.walk(d):
                if (isinstance(x, ast.Assign) and isinstance(x.targets[0], ast.Name)
                        and x.targets[0].id == "haric"):
                    h14 = ast.literal_eval(x.value)
        if isinstance(d, ast.Assign) and isinstance(d.targets[0], ast.Name) and d.targets[0].id == "_ATIF_HARIC":
            atif = ast.literal_eval(d.value)
    if h14 is None or atif is None or h14 != atif:
        return [("KUME", "_ATIF_HARIC (%r) != H14 haric (%r)" % (atif, h14))]
    return []


MADDE2 = "1. `HEDEF` = `a.py:3`\n2. `HEDEF2` = `b.py:3`"
DOSYA_CIFT = {"a.py": A_PY, "node_modules/a.py": A_PY, "b.py": A_PY.replace("HEDEF", "HEDEF2"),
              ".dart_tool/b.py": A_PY.replace("HEDEF", "HEDEF2")}


def ks_cokkopya(motor, taban):
    """BUDANAN dizinde cift kopya GOZARDI edilir (node_modules/a.py), BUDANMAYAN nokta-dizinde cift kopya
    (.dart_tool/b.py) OLCULEMEDI [DOSYA_COK] olur. Beklenti motorun sabitinden DEGIL elle yazilidir
    (paylasilan kural = paylasilan korluk)."""
    kok = hal_satir(motor, os.path.join(taban, "ks_c"), MADDE2, DOSYA_CIFT)
    notdemle(motor, kok, "sonraki-adim")
    rk, ck = kos(motor, ["kapi"], kok)
    if _h18(ck) != (2, 0, 1, "DOSYA_COK:1") or rk != 0:
        return [("COKKOPYA", "H18=%r exit=%s (beklenen 2 atif · 0 KAYMA · 1 OLCULEMEDI [DOSYA_COK:1])"
                 % (_h18(ck), rk))]
    return []


def ks_gitsiz(motor, taban):
    """GITSIZ + DETERMINIZM: .git YOKKEN H18 ayni sonucu verir; iki kosum bayt-ayni."""
    kok = hal_satir(motor, os.path.join(taban, "ks_g"), MADDE2, DOSYA_CIFT, git=False)
    notdemle(motor, kok, "sonraki-adim")
    r1, c1 = kos(motor, ["kapi"], kok)
    r2, c2 = kos(motor, ["kapi"], kok)
    s1 = [x for x in c1.splitlines() if "H18:" in x]
    if _h18(c1) != (2, 0, 1, "DOSYA_COK:1") or s1 != [x for x in c2.splitlines() if "H18:" in x]:
        return [("GITSIZ", "git'siz projede H18=%r (iki kosum ayni=%s); beklenen 2 atif · 0 KAYMA · 1 OLCULEMEDI "
                 "[DOSYA_COK:1]" % (_h18(c1), s1 == [x for x in c2.splitlines() if "H18:" in x]))]
    return []


A_ARALIK = "# c\n" * 9 + "HEDEF = 1\nx = 2\n"       # HEDEF L10
MADDE_ARALIK = "1. `HEDEF` = `a.py:5-9`\n2. `HEDEF` = `a.py:99`"


def ks_aralik(motor, taban):
    """yol:N-M penceresi [N-2, M+2]: HEDEF L10, atif 5-9 -> TUTUYOR (N tek basina KAYMA olurdu); a.py:99 -> SATIR_DISI."""
    kok = hal_satir(motor, os.path.join(taban, "ks_a"), MADDE_ARALIK, {"a.py": A_ARALIK})
    notdemle(motor, kok, "sonraki-adim")
    rk, ck = kos(motor, ["kapi"], kok)
    if _h18(ck) != (2, 0, 1, "SATIR_DISI:1") or rk != 0:
        return [("ARALIK", "H18=%r exit=%s (beklenen 2 atif · 0 KAYMA · 1 OLCULEMEDI [SATIR_DISI:1])"
                 % (_h18(ck), rk))]
    return []


# ===================================================================== K-YOL (devral karar dizini)
# besli-paket/IS_EMRI_KSATIR_KARARYOLU.md (5 Eki 2026, Onur kilidi "devral ADR yolunu tasir"). OLCULDU
# (Momentum): `docs/ADR/` dolu, DURUM.md'de ADR atfi 0, kor okumada KARAR sorulari 0/4. `devral` projenin
# MEVCUT karar dizinini bulur, canliya YOL tasiyan `sahip="hafiza-kur"` blogu (konu `karar-kaynagi`) yazar,
# `.hafizarc`a `karar_dizini` kaydeder; `derle` blogu diskten yeniden uretir. Dosyalara DOKUNULMAZ.
DURUM_ILK = "# DURUM.md\n\n## Kalici dersler\n- ders 1\n"
# derle dongusunun ve H6/H17'nin ISTEDIGI bolumleri devral ANINDA zaten tasiyan canli: `bolum-kur` GEREKMEZ
# (`kapi --siki` bolum-kur basliklarini BEYANSIZ sayar — DURUM.md bilinen sinirlar; o sinir K-YOL'un DEGIL).
DURUM_BOLUMLU = ("# DURUM.md\n\n## GUNCEL DURUM\n- durum\n\n## SABIT CERCEVE\n- ders 1\n\n"
                 "## ARSIV DIZINI\n")
ADR_DOSYALARI = {
    "docs/ADR/0001-ilk.md": "# ADR 0001 — Ilk karar\n\ngovde bir\n",
    "docs/ADR/0002-ikinci.md": "# ADR 0002 — Ikinci karar\n",
    "docs/ADR/ADR-003-ucuncu.md": "# Ucuncu karar\n",
    "docs/ADR/0004-asla-kural.md": "# ASLA yapilmayacaklar listesi\n",
    "docs/ADR/0005-backtick.md": "# ADR `yok_dosya.py` baslik\n",
    "docs/ADR/README.md": "# ADR dizini\n",
    "docs/ADR/.gitkeep": "",
    "docs/ADR/arsiv/0009-eski.md": "# eski karar\n",
}
BLOK_KARAR = re.compile(r'<!-- blok konu="karar-kaynagi"([^>]*)-->\n(.*?)\n<!-- /blok -->', re.S)
KARAR_OZET = re.compile(r"  karar dizini      : (.+)")
ARANAN = "bulunamadi (aranan: docs/ADR, docs/adr, docs/decisions, adr, doc/adr)"


def hal_yol(motor, kok, dosyalar, canli=DURUM_ILK):
    """git + DURUM.md + dosyalar + commit; sonra `devral --esle canli=DURUM.md`. DONER (rc, cikti)."""
    os.makedirs(kok, exist_ok=True)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    _yaz(os.path.join(kok, "DURUM.md"), canli)
    for ad, icerik in dosyalar.items():
        _yaz(os.path.join(kok, *ad.split("/")), icerik)
    _commit(kok, "ilk")
    return kos(motor, ["devral", "--esle=canli=DURUM.md", "--ad", "YOL"], kok)


def _rc_oku(kok):
    with io.open(os.path.join(kok, ".hafizarc"), encoding="utf-8") as f:
        return json.load(f)


def _agac_sha(kok, alt):
    out = {}
    for r0, _d, f0 in os.walk(os.path.join(kok, *alt.split("/"))):
        for f in f0:
            with open(os.path.join(r0, f), "rb") as h:
                out[os.path.relpath(os.path.join(r0, f), kok).replace("\\", "/")] = hashlib.sha256(h.read()).hexdigest()
    return out


def _kapi_etiketi(c):
    """`kapi` kirmizisini HANGI kapinin yaktigina gore etiketle (her sabotaj kendi eksenini ateslesin)."""
    for tag, et in (("[H10]", "YKONU"), ("[H4]", "YBACKTICK"), ("[H7]", "YMASKE"), ("[H11]", "YH11")):
        if tag in c:
            return et
    return "YKAPI"


def _kapilar_yesil(motor, kok, ek=""):
    """kapi + kapi --siki: (etiket, mesaj) listesi (BOS = ikisi de exit 0)."""
    b = []
    rc, c = kos(motor, ["kapi"], kok)
    if rc != 0:
        b.append((_kapi_etiketi(c), "kapi exit %s%s: %s" % (rc, ek, " | ".join(
            x.strip() for x in c.splitlines() if x.strip().startswith("[H"))[:200])))
    rc2, c2 = kos(motor, ["kapi", "--siki"], kok)
    if rc2 != 0 and rc == 0:
        b.append(("MUHASEBE", "kapi --siki exit %s%s" % (rc2, ek)))
    return b


def ky_kontrol(motor, taban):
    """YANLIS ALARM: dizin VAR ama ADR desenli dosya YOK (README.md + .gitkeep) -> 'bulunamadi', blok/anahtar YOK."""
    b = []
    kok = os.path.join(taban, "ky_k")
    rc, c = hal_yol(motor, kok, {"docs/ADR/README.md": "# ADR\n", "docs/ADR/.gitkeep": ""})
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    m = KARAR_OZET.search(c)
    if not m or m.group(1).strip() != ARANAN:
        b.append(("YKONTROL", "ADR'siz projede ozet satiri %r (beklenen %r)" % (m and m.group(1), ARANAN)))
    if "karar_dizini" in _rc_oku(kok) or "karar-kaynagi" in _canli_devral(kok) or _konu_var(kok, "karar-kaynagi"):
        b.append(("YKONTROL", "ADR'siz projede .hafizarc anahtari / blok / konu satiri YAZILMIS"))
    return b


def _canli_devral(kok):
    with io.open(os.path.join(kok, "DURUM.md"), encoding="utf-8") as f:
        return f.read()


def _konu_var(kok, konu):
    with io.open(os.path.join(kok, "KONULAR.md"), encoding="utf-8") as f:
        return re.search(r"^\|\s*%s\s*\|" % re.escape(konu), f.read(), re.M) is not None


def ky_adr(motor, taban, tag="ky_a"):
    """YBLOK/YRC/YOZET/YSAYIM/YMASKE/YKONU/YBACKTICK/YDOKUNMA + devral SONRASI derle zinciri:
    YYENILE · IDEMPOTANS · YKAYIP (+ MUHASEBE). Tek fikstur."""
    b = []
    kok = os.path.join(taban, tag)
    rc, c = hal_yol(motor, kok, ADR_DOSYALARI, DURUM_BOLUMLU)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    # Beklenen ozet motordan DEGIL fikstur iceriginden (paylasilan kural = paylasilan korluk): devral
    # sirasinda dokunulursa bile yakalanir.
    sha0 = {ad: hashlib.sha256(ic.encode("utf-8")).hexdigest() for ad, ic in ADR_DOSYALARI.items()}
    m = KARAR_OZET.search(c)
    if not m or m.group(1).strip() != "docs/ADR (5 dosya)":
        b.append(("YOZET", "devral ozet satiri %r (beklenen 'docs/ADR (5 dosya)')" % (m and m.group(1),)))
    if _rc_oku(kok).get("karar_dizini") != "docs/ADR":
        b.append(("YRC", ".hafizarc karar_dizini = %r (beklenen 'docs/ADR')" % _rc_oku(kok).get("karar_dizini")))
    blok = BLOK_KARAR.search(_canli_devral(kok))
    govde = blok.group(2) if blok else ""
    if not blok or 'sahip="hafiza-kur"' not in blok.group(1) or "docs/ADR (5 dosya)" not in govde:
        b.append(("YBLOK", "canlida sahip=hafiza-kur 'karar-kaynagi' blogu (docs/ADR + 5 dosya) YOK"))
    elif not all(x in govde for x in ("0001-ilk.md — ADR 0001 — Ilk karar", "0002-ikinci.md", "0005-backtick.md",
                                      "ADR-003-ucuncu.md")):
        b.append(("YBLOK", "blokta beklenen dosya adi/baslik satirlari eksik: %r" % govde[:300]))
    if blok and any(x in govde for x in (".gitkeep", "README.md", "0009-eski")):
        b.append(("YSAYIM", ".gitkeep / README.md / alt dizin dosyasi sayilmis: %r" % govde[:300]))
    if blok and "ASLA yapilmayacaklar" in govde:      # `TASLAK` basligi `ASLA`yi sozcuk ici tasir: marker DEGIL
        b.append(("YMASKE", "kalici-kural isareti tasiyan baslik blokta GORUNUYOR"))
    if not _konu_var(kok, "karar-kaynagi"):
        b.append(("YKONU", "KONULAR.md'de 'karar-kaynagi' satiri YOK"))
    _commit(kok, "devral")
    b += _kapilar_yesil(motor, kok)
    # ---- YENILE: yeni ADR dosyasi + motorun kendi karari -> derle blogu diskten yeniden uretir ----------
    _yaz(os.path.join(kok, "docs", "ADR", "0006-yeni.md"), "# ADR 0006 — Yeni karar\n")
    sha0["docs/ADR/0006-yeni.md"] = hashlib.sha256(b"# ADR 0006 \xe2\x80\x94 Yeni karar\n").hexdigest()
    rc, c = kos(motor, ["karar", "--baslik", "Motor karari"], kok)
    if rc != 0:
        raise Kurulamadi("karar basarisiz: %s" % c.strip().split("\n")[-1][:160])
    _commit(kok, "yeni adr")
    rc, c = notdemle(motor, kok, "sonraki-adim")
    blok = BLOK_KARAR.search(_canli_devral(kok))
    govde = blok.group(2) if blok else ""
    if (rc != 0 or "docs/ADR (6 dosya)" not in govde or "0006-yeni.md" not in govde
            or "motorun kendi karar dizini" not in govde or "0001-motor-karari.md" not in govde
            or _arsiv(kok).count('konu="karar-kaynagi"') != 1):
        b.append(("YYENILE", "derle blogu diskten yeniden URETMEDI (exit=%s, arsivde eski blok=%d): %r"
                  % (rc, _arsiv(kok).count('konu="karar-kaynagi"'), govde[:200])))
    b += _kapilar_yesil(motor, kok, " (yenileme sonrasi)")
    # ---- IDEMPOTANS: degisiklik YOK -> blok yeniden yazilmaz, arsive kopya girmez ---------------------
    _commit(kok, "yenilendi")
    rc, c = notdemle(motor, kok, "acik-kararlar", "ikinci derle ayni karar dizini ile")
    if "'karar-kaynagi' blogu" in c or _arsiv(kok).count('konu="karar-kaynagi"') != 1:
        b.append(("IDEMPOTANS", "ayni karar dizini ile derle blogu YENIDEN yazdi (arsivde=%d)"
                  % _arsiv(kok).count('konu="karar-kaynagi"')))
    # ---- DOKUNMA: ADR dosyalari bayt-bayt ayni -----------------------------------------------------
    if _agac_sha(kok, "docs/ADR") != sha0:
        b.append(("YDOKUNMA", "docs/ADR dosyalari DEGISTI (devral/derle projenin kendi dosyasina dokunmamali)"))
    # ---- KAYIP: dizin silindi -> blok 'YOK (kayitli: docs/ADR)' der, SESSIZCE dusmez -----------------
    _commit(kok, "idempotans")
    _sil(os.path.join(kok, "docs", "ADR"))
    _commit(kok, "dizin silindi")
    rc, c = notdemle(motor, kok, "sonraki-adim", "dizin silindikten sonra derle")
    blok = BLOK_KARAR.search(_canli_devral(kok))
    govde = blok.group(2) if blok else ""
    if rc != 0 or "YOK (kayitli: docs/ADR)" not in govde or "0001-ilk.md" in govde:
        b.append(("YKAYIP", "dizin silindi ama blok 'YOK (kayitli: docs/ADR)' DEMEDI (exit=%s): %r" % (rc, govde[:200])))
    b += _kapilar_yesil(motor, kok, " (dizin silindikten sonra)")
    return b


def ky_sahiplik(motor, taban):
    """SAHIPLIK: ayni konuda sahip=proje blogu varsa devral ONA DOKUNMAZ, ikinci blok ACMAZ."""
    canli = ("# DURUM.md\n\n## Kalici dersler\n"
             '<!-- blok konu="karar-kaynagi" guncel="2026-01-01" kaynak="-" sahip="proje" -->\n'
             "KULLANICI karar notu dokunulmamali\n<!-- /blok -->\n")
    kok = os.path.join(taban, "ky_s")
    rc, c = hal_yol(motor, kok, {"docs/ADR/0001-ilk.md": "# ADR 0001 — Ilk\n"}, canli)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    bloklar = BLOK_KARAR.findall(_canli_devral(kok))
    if (len(bloklar) != 1 or 'sahip="proje"' not in bloklar[0][0]
            or "KULLANICI karar notu dokunulmamali" not in bloklar[0][1]
            or "Motor (devral/derle)" in _canli_devral(kok)):
        return [("SAHIPLIK", "sahip=proje 'karar-kaynagi' blogu korunmadi (blok sayisi=%d)" % len(bloklar))]
    return []


def ky_case(motor, taban):
    """BUYUK/KUCUK HARF: `Docs/Adr` bulunur ve diskteki GERCEK yazimiyla kaydedilir (platformdan bagimsiz)."""
    kok = os.path.join(taban, "ky_c")
    rc, c = hal_yol(motor, kok, {"Docs/Adr/0001-ilk.md": "# ADR 0001 — Ilk\n"})
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    m = KARAR_OZET.search(c)
    if _rc_oku(kok).get("karar_dizini") != "Docs/Adr" or not m or m.group(1).strip() != "Docs/Adr (1 dosya)":
        return [("YCASE", "Docs/Adr bulunamadi/gercek yazimla kaydedilmedi: rc=%r ozet=%r"
                 % (_rc_oku(kok).get("karar_dizini"), m and m.group(1)))]
    return []


def ky_cok(motor, taban):
    """COK ADAY: docs/ADR ve adr ikisi de ADR tasiyor -> ILK aday kaydedilir, digeri GORUNUR ('baska aday')."""
    kok = os.path.join(taban, "ky_m")
    rc, c = hal_yol(motor, kok, {"docs/ADR/0001-a.md": "# a\n", "adr/0001-b.md": "# b\n"})
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    m = KARAR_OZET.search(c)
    if _rc_oku(kok).get("karar_dizini") != "docs/ADR" or not m \
            or m.group(1).strip() != "docs/ADR (1 dosya) · baska aday: adr":
        return [("YCOK", "birden cok aday: rc=%r ozet=%r" % (_rc_oku(kok).get("karar_dizini"), m and m.group(1)))]
    satirlar_ = _canli_devral(kok).split("\n")
    ilk_bas = next((i for i, x in enumerate(satirlar_) if x.startswith("## ")), len(satirlar_))
    blok_i = next((i for i, x in enumerate(satirlar_) if x.startswith('<!-- blok konu="karar-kaynagi"')), None)
    if blok_i is None or blok_i > ilk_bas:
        return [("YYER", "`## GUNCEL DURUM` YOKKEN blok dosyanin USTUNDE (ilk bolumden once) degil: blok satiri=%r, "
                 "ilk bolum=%d" % (blok_i, ilk_bas))]
    return []


def _dizin_baglantisi(link, hedef):
    """Proje DISINA bagli dizin: Windows'ta JUNCTION (yetki gerekmez), POSIX'te symlink. Kurulamazsa Kurulamadi."""
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", link, hedef], capture_output=True)
        if r.returncode != 0:
            raise Kurulamadi("junction kurulamadi: %s" % (r.stdout + r.stderr)[:160])
    else:
        try:
            os.symlink(hedef, link, target_is_directory=True)
        except OSError as e:
            raise Kurulamadi("symlink kurulamadi: %s" % e)


def ky_kacis(motor, taban):
    """KACIS: docs/ADR proje DISINA baglanmis (junction/symlink) -> OKUNMAZ, blok/anahtar YOK ama
    SESSIZCE de dusmez: ozet satiri 'ATLANDI (proje DISINA bagli, okunmadi)' der."""
    kok = os.path.join(taban, "ky_x", "proje")
    disarda = os.path.join(taban, "ky_x", "disarda")
    _yaz(os.path.join(disarda, "0001-x.md"), "# ADR 0001 — dis\n")
    os.makedirs(kok, exist_ok=True)
    _dizin_baglantisi(os.path.join(kok, "docs", "ADR"), disarda)
    _yaz(os.path.join(kok, "DURUM.md"), DURUM_ILK)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    _commit(kok, "ilk")
    rc, c = kos(motor, ["devral", "--esle=canli=DURUM.md", "--ad", "YOL"], kok)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    m = KARAR_OZET.search(c)
    if (not m or "ATLANDI (proje DISINA bagli, okunmadi): docs/ADR" not in m.group(1)
            or "karar_dizini" in _rc_oku(kok) or "karar-kaynagi" in _canli_devral(kok)
            or "0001-x.md" in _canli_devral(kok)):
        return [("YKACIS", "proje DISINA bagli docs/ADR: ozet=%r rc-anahtari=%s blok=%s" % (
            m and m.group(1), "karar_dizini" in _rc_oku(kok), "karar-kaynagi" in _canli_devral(kok)))]
    return []


def ky_kesif(motor, taban):
    """KESIF (kuru prova): `devral --kesif` karar dizinini RAPORLAR ve diske HIC yazmaz."""
    kok = os.path.join(taban, "ky_e")
    os.makedirs(kok, exist_ok=True)
    _yaz(os.path.join(kok, "DURUM.md"), DURUM_ILK)
    for ad, icerik in ADR_DOSYALARI.items():
        _yaz(os.path.join(kok, *ad.split("/")), icerik)
    onceki = _agac_sha(kok, ".")
    rc, c = kos(motor, ["devral", "--kesif", "--esle=canli=DURUM.md"], kok)
    m = KARAR_OZET.search(c)
    if rc != 0 or not m or m.group(1).strip() != "docs/ADR (5 dosya)" or _agac_sha(kok, ".") != onceki \
            or os.path.exists(os.path.join(kok, ".hafizarc")):
        return [("YKESIF", "devral --kesif: exit=%s ozet=%r yazim=%s" % (
            rc, m and m.group(1), _agac_sha(kok, ".") != onceki or os.path.exists(os.path.join(kok, ".hafizarc"))))]
    return []


# ===================================================================== K-DURUM (ADR durum satiri)
# besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md (6 Eki 2026, Onur kilidi). OLCULDU (Momentum kor okuma R1, iki
# tekrar YANLIS): blok TASLAK ADR'ye kilitlilerle AYNI agirlikta yol veriyordu. `karar-kaynagi` her ADR'nin KENDI
# `Durum`/`Status` beyanini (ilk 30 satir; on-bilgi `durum:` dahil) `[durum: ...]` olarak tasir, yoksa `BEYANSIZ`.
# Beklenti FIKSTUR iceriginden elle yazilidir (paylasilan kural = paylasilan korluk); motor yorumlamaz.
KD_ADR = {
    "docs/ADR/0001-kilitli.md": "# ADR 0001 — Kilitli\n\n- **Durum:** ✅ **KİLİTLİ (v3)**\n",
    "docs/ADR/0002-onbilgi.md": "---\ndurum: kabul\n---\n# ADR 0002 — On bilgi\n",
    "docs/ADR/0003-taslak.md": "# ADR 0003 — Taslak\n> Status : **Proposed** — KILITLI DEGIL\n",
    "docs/ADR/0004-uzun.md": "# ADR 0004 — Uzun\nDurum: " + "u" * 80 + "\n",
    "docs/ADR/0005-beyansiz.md": "# ADR 0005 — Beyansiz\nbir metin, anahtar yok\n",
    "docs/ADR/0006-pencere-disi.md": "# ADR 0006 — Pencere disi\n" + "x\n" * 30 + "Durum: kabul\n",      # L32
    "docs/ADR/0007-pencere-ici.md": "# ADR 0007 — Pencere ici\n" + "x\n" * 28 + "Durum: kabul\n",       # L30
}
KD_BEKLENEN = (
    "0001-kilitli.md — ADR 0001 — Kilitli — [durum: ✅ KİLİTLİ (v3)]",
    "0002-onbilgi.md — ADR 0002 — On bilgi — [durum: kabul]",
    "0003-taslak.md — ADR 0003 — Taslak — [durum: Proposed — KILITLI DEGIL]",
    "0004-uzun.md — ADR 0004 — Uzun — [durum: " + "u" * 59 + "…]",
    "0005-beyansiz.md — ADR 0005 — Beyansiz — [durum: BEYANSIZ]",
    "0006-pencere-disi.md — ADR 0006 — Pencere disi — [durum: BEYANSIZ]",
    "0007-pencere-ici.md — ADR 0007 — Pencere ici — [durum: kabul]",
)


def _kd_satirlar(kok):
    blok = BLOK_KARAR.search(_canli_devral(kok))
    return [x[2:] for x in (blok.group(2) if blok else "").splitlines() if x.startswith("- ")]


def kd_durum(motor, taban):
    """DEVRAL -> her ADR'nin durumu blokta (KDURUM) · uzun deger <=60 kirpilir (KKESME) · ilk 30 satirdan SONRAKI
    beyan sayilmaz (KPENCERE) · anahtarsiz `BEYANSIZ` (KBEYANSIZ) · DURUM SATIRI SILININCE derle BEYANSIZ yapar
    (KSILINCE) · motorun kendi `kararlar/` listesi de tasir (KMOTOR) · kapi + kapi --siki yesil."""
    b = []
    kok = os.path.join(taban, "kd")
    rc, c = hal_yol(motor, kok, KD_ADR, DURUM_BOLUMLU)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    sat = _kd_satirlar(kok)
    for beklenen in KD_BEKLENEN:
        if beklenen not in sat:
            et = ("KKESME" if "uzun" in beklenen else "KPENCERE" if "pencere-disi" in beklenen else
                  "KBEYANSIZ" if "BEYANSIZ" in beklenen else "KDURUM")
            b.append((et, "blokta beklenen satir YOK: %r (blok satirlari: %r)" % (beklenen, sat[:9])))
    _commit(kok, "devral")
    b += _kapilar_yesil(motor, kok)
    # ---- SILINCE: durum satiri silinir -> derle blogu diskten yeniden uretir, BEYANSIZ der -------------
    _yaz(os.path.join(kok, "docs", "ADR", "0001-kilitli.md"), "# ADR 0001 — Kilitli\n")
    _commit(kok, "durum silindi")
    rc, c = notdemle(motor, kok, "sonraki-adim", "durum satiri silindikten sonra derle")
    sat = _kd_satirlar(kok)
    if rc != 0 or "0001-kilitli.md — ADR 0001 — Kilitli — [durum: BEYANSIZ]" not in sat:
        b.append(("KSILINCE", "durum satiri silindi ama blok BEYANSIZ demedi (exit=%s): %r" % (rc, sat[:2])))
    # ---- MOTOR: motorun kendi kararlar/ dizini de beyani tasir ----------------------------------------
    rc, c = kos(motor, ["karar", "--baslik", "Motor karari"], kok)
    if rc != 0:
        raise Kurulamadi("karar basarisiz: %s" % c.strip().split("\n")[-1][:160])
    _commit(kok, "motor karari")
    rc, c = notdemle(motor, kok, "acik-kararlar", "motor karari eklendikten sonra derle")
    if rc != 0 or "0001-motor-karari.md — Motor karari — [durum: onerildi]" not in _kd_satirlar(kok):
        b.append(("KMOTOR", "motorun kendi karari blokta durumuyla YOK (exit=%s): %r" % (rc, _kd_satirlar(kok)[-3:])))
    b += _kapilar_yesil(motor, kok, " (durum silindikten sonra)")
    return b


# ===================================================================== K-GECIS (kurulu projede kesif)
# besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md (6 Eki 2026, Onur kilidi). OLCULDU (kurulu Momentum): `devral`
# exit 2 `.hafizarc ZATEN VAR` => mevcut kurulumlar `karar-kaynagi` hic alamiyordu. `derle`, `.hafizarc`ta
# `karar_dizini` ANAHTARI HIC YOKSA keşfi (K-YOL'un AYNI fonksiyonu) BIR KEZ kosar, sonucu (bulunamazsa `""`) yazar
# ve beyan eder; `""` BILINCLI bos degerdir, dokunulmaz. Beklenti FIKSTUR iceriginden (motordan degil).
KG_ADR = {"docs/ADR/0001-ilk.md": "# ADR 0001 — Ilk\nDurum: kabul\n",
          "docs/ADR/0002-ikinci.md": "# ADR 0002 — Ikinci\nDurum: taslak\n"}


def kg_hazir(motor, kok, adr):
    """git + `kur` (kurulu proje: `.hafizarc`ta `karar_dizini` ANAHTARI YOK) [+ docs/ADR] + commit."""
    os.makedirs(kok, exist_ok=True)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    rc, c = kos(motor, ["kur", "--ad", "GECIS"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    if adr:
        for ad, icerik in KG_ADR.items():
            _yaz(os.path.join(kok, *ad.split("/")), icerik)
    _commit(kok, "ilk")


def _rc_ham(kok):
    with io.open(os.path.join(kok, ".hafizarc"), encoding="utf-8", newline="") as f:
        return f.read()


def kg_gecis(motor, taban):
    """ANAHTARSIZ kurulu proje + ADR: ilk derle KESFEDER (KGKESIF: .hafizarc'a yazar · KGBEYAN: cikti beyani ·
    KGBLOK: karar-kaynagi blogu AYNI derle'de · KGRC: mevcut baytlar AYNEN, yalniz anahtar eklenir) ·
    ikinci derle ayni disk => cikti beyansiz, .hafizarc bayt-bayt AYNI (KGTEKRAR) · ADR'SIZ proje: `""` yazilir
    ve beyan edilir (KGYOK) · `""` varken ADR gelse de keşif CALISMAZ (KGBOS) · kapi + kapi --siki yesil."""
    b = []
    kok = os.path.join(taban, "kg_a")
    kg_hazir(motor, kok, True)
    eski = _rc_ham(kok)
    if "karar_dizini" in eski:
        raise Kurulamadi("fikstur kurulu projede karar_dizini ANAHTARI zaten var")
    rc, c = notdemle(motor, kok, "genel-durum")
    yeni = _rc_ham(kok)
    beklenen = eski.rstrip()[:-1].rstrip() + ',\n  "karar_dizini": "docs/ADR"\n}' + eski[len(eski.rstrip()):]
    if rc != 0:
        raise Kurulamadi("derle basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    if "KARAR DIZINI KESFEDILDI: docs/ADR (2) — .hafizarc'a yazildi" not in c:
        b.append(("KGBEYAN", "derle KESFEDILDI beyanini basmadi: %r" % c[-300:]))
    try:
        anahtar = json.loads(yeni).get("karar_dizini")
    except ValueError:
        anahtar = "GECERSIZ JSON"
    if anahtar != "docs/ADR":
        b.append(("KGKESIF", ".hafizarc karar_dizini = %r (beklenen 'docs/ADR')" % (anahtar,)))
    elif yeni != beklenen:
        b.append(("KGRC", ".hafizarc mevcut baytlari DEGISTI/yeniden bicimlendi (beklenen yalniz anahtar eklenmesi)"))
    blok = BLOK_KARAR.search(_canli(kok))
    sat = [x[2:] for x in (blok.group(2) if blok else "").splitlines() if x.startswith("- ")]
    if "0001-ilk.md — ADR 0001 — Ilk — [durum: kabul]" not in sat or "0002-ikinci.md — ADR 0002 — Ikinci — [durum: taslak]" not in sat:
        b.append(("KGBLOK", "ayni derle'de karar-kaynagi blogu (2 ad) yazilmadi: %r" % sat[:4]))
    b += _kapilar_yesil(motor, kok, " (kesif sonrasi)")
    rc, c = notdemle(motor, kok, "acik-kararlar", "ikinci derle ayni disk")
    if "KARAR DIZINI" in c or _rc_ham(kok) != yeni:
        b.append(("KGTEKRAR", "anahtar VARKEN ikinci derle tekrar kesfetti/yazdi (exit=%s)" % rc))
    # ---- ADR'SIZ proje: bulunamazsa `""` yazilir + beyan; sonra ADR gelse de keşif CALISMAZ -----------------
    kok2 = os.path.join(taban, "kg_b")
    kg_hazir(motor, kok2, False)
    eski2 = _rc_ham(kok2)
    rc, c = notdemle(motor, kok2, "genel-durum")
    yeni2 = _rc_ham(kok2)
    beklenen2 = eski2.rstrip()[:-1].rstrip() + ',\n  "karar_dizini": ""\n}' + eski2[len(eski2.rstrip()):]
    if "KARAR DIZINI YOK" not in c or "(bir daha aranmaz)" not in c or yeni2 != beklenen2:
        b.append(("KGYOK", "ADR'siz projede `\"karar_dizini\": \"\"` yazilmadi/beyan edilmedi (exit=%s): %r"
                  % (rc, c[-240:])))
    b += _kapilar_yesil(motor, kok2, " (bulunamadi sonrasi)")
    _commit(kok2, "bos yazildi")
    for ad, icerik in KG_ADR.items():
        _yaz(os.path.join(kok2, *ad.split("/")), icerik)
    _commit(kok2, "adr geldi")
    rc, c = notdemle(motor, kok2, "acik-kararlar", "ADR geldi ama anahtar bilincli bos")
    if "KARAR DIZINI" in c or _rc_ham(kok2) != yeni2 or "karar-kaynagi" in _canli(kok2):
        b.append(("KGBOS", "`\"\"` bilincli bos degerken ADR gelince keşif CALISTI (exit=%s, blok=%s)"
                  % (rc, "karar-kaynagi" in _canli(kok2))))
    return b


# ===================================================================== K-ISARET (kural evi -> canli isaretci)
# besli-paket/IS_EMRI_ADRDURUM_GECIS_ISARETCI.md (6 Eki 2026, Onur kilidi). OLCULDU: `kur`/`devral` yeni kural evine
# yalniz baslik + "Bu dosya her oturumda yuklenir" yaziyordu; canli defterin ADI yoktu => defter yalniz skill
# tetiklenirse okunuyordu. Yeni kural evi 2. satirda isaretci tasir; kural evi ZATEN VARSA dosya BAYT-BAYT ayni kalir
# ve cikti ONERI satiri basar; `kapi` (H19) kural evinde canli adi gecmiyorsa UYARIR (cikis kodu DEGISMEZ).
# Beklenen metinler FIKSTURDEN elle yazilidir (motordan degil).
KI_SATIR = "> Canli defter: %s — her oturum basinda once onu oku (hafiza-kur)."
KI_VAR = "# Proje kurallari\nbu dosya projenin kendi kural evi; canli deftere yol vermiyor\n"


def _ki_oku(kok, ad="CLAUDE.md"):
    with io.open(os.path.join(kok, ad), "rb") as f:
        return f.read()


def ki_isaret(motor, taban):
    """KIKUR: taze `kur` kural evinin 2. satirinda isaretci VAR · KISESSIZ: `kapi` H19 basmaz · KIKAPI: isaretci
    satiri SILININCE `kapi` H19 uyarir · KIEXIT: uyari cikis kodunu DEGISTIRMEZ · KIBAYT: mevcut kural evli
    `devral`/`kur` dosyayi BAYT-BAYT ayni birakir · KIONERI: o halde cikti `ISARETCI YOK ... eklemek icin: <satir>` der ·
    KIDEVRAL: devral YENI kural evine isaretci yazar."""
    b = []
    # ---- taze kur -----------------------------------------------------------------------------------
    kok = os.path.join(taban, "ki_a")
    os.makedirs(kok, exist_ok=True)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    rc, c = kos(motor, ["kur", "--ad", "ISARET"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    sat = _ki_oku(kok).decode("utf-8").split("\n")
    if len(sat) < 2 or sat[1] != KI_SATIR % "PROJE_HAFIZA.md":
        b.append(("KIKUR", "taze kur: kural evi 2. satiri %r (beklenen %r)" % (sat[1:2], KI_SATIR % "PROJE_HAFIZA.md")))
    _commit(kok, "ilk")
    r0, c0 = kos(motor, ["kapi"], kok)
    if "H19" in c0 or r0 != 0:
        b.append(("KISESSIZ", "isaretci VARKEN kapi H19 bastı / exit=%s: %r" % (r0, [x for x in c0.splitlines() if "H19" in x])))
    # ---- isaretci silinir -----------------------------------------------------------------------------
    _yaz(os.path.join(kok, "CLAUDE.md"), "\n".join(sat[:1] + sat[2:]))
    _commit(kok, "isaretci silindi")
    r1, c1 = kos(motor, ["kapi"], kok)
    uyari = [x.strip() for x in c1.splitlines() if "H19" in x]
    if len(uyari) != 1 or not uyari[0].startswith("· H19: kural evi (CLAUDE.md) canli defterin adini (PROJE_HAFIZA.md) anmiyor") \
            or ("eklemek icin: " + KI_SATIR % "PROJE_HAFIZA.md") not in uyari[0]:
        b.append(("KIKAPI", "isaretci silindi: kapi H19 uyarisi %r" % (uyari,)))
    if r1 != r0 or "SONUC: YESIL — olculen her sey gecti." not in c1:
        b.append(("KIEXIT", "H19 uyarisi cikis kodunu/hukmu DEGISTIRDI: exit %s -> %s" % (r0, r1)))
    # ---- mevcut kural evli devral ---------------------------------------------------------------------
    kok2 = os.path.join(taban, "ki_b")
    rc, c = hal_yol(motor, kok2, {"CLAUDE.md": KI_VAR}, DURUM_BOLUMLU)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    if _ki_oku(kok2) != KI_VAR.encode("utf-8"):
        b.append(("KIBAYT", "mevcut kural evli devral CLAUDE.md'yi DEGISTIRDI"))
    if ("ISARETCI YOK: CLAUDE.md canli deftere isaret etmiyor — eklemek icin: " + KI_SATIR % "DURUM.md") not in c:
        b.append(("KIONERI", "devral ISARETCI YOK onerisini basmadi: %r" % [x for x in c.splitlines() if "ISARET" in x]))
    # ---- mevcut kural evli kur ------------------------------------------------------------------------
    kok3 = os.path.join(taban, "ki_c")
    os.makedirs(kok3, exist_ok=True)
    _yaz(os.path.join(kok3, "CLAUDE.md"), KI_VAR)
    if subprocess.run(["git", "init", "-q", kok3], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    rc, c = kos(motor, ["kur", "--ad", "ISARET", "--yine-de"], kok3)   # mevcut icerik: `kur` yine-de ister
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    if _ki_oku(kok3) != KI_VAR.encode("utf-8"):
        b.append(("KIBAYT", "mevcut kural evli kur CLAUDE.md'yi DEGISTIRDI"))
    if ("ISARETCI YOK: CLAUDE.md canli deftere isaret etmiyor — eklemek icin: " + KI_SATIR % "PROJE_HAFIZA.md") not in c:
        b.append(("KIONERI", "kur ISARETCI YOK onerisini basmadi: %r" % [x for x in c.splitlines() if "ISARET" in x]))
    # ---- devral YENI kural evi ------------------------------------------------------------------------
    kok4 = os.path.join(taban, "ki_d")
    rc, c = hal_yol(motor, kok4, {}, DURUM_BOLUMLU)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    sat4 = _ki_oku(kok4).decode("utf-8").split("\n")
    if len(sat4) < 2 or sat4[1] != KI_SATIR % "DURUM.md":
        b.append(("KIDEVRAL", "devral yeni kural evi 2. satiri %r (beklenen %r)" % (sat4[1:2], KI_SATIR % "DURUM.md")))
    return b


# ===================================================================== P1 (taslak/karar ayrimi)
# besli-paket/IS_EMRI_P1_TASLAK_KARAR_AYRIMI.md (6 Eki 2026, Onur kilidi sik (a)). OLCULDU (Momentum kor okuma R1 iki
# tekrar YANLIS): durum etiketi okuyucuya ULASTI ama taslagin icerigi yine karar diye aktarildi. `karar-kaynagi` ADR
# satirlarini DORT SINIF grubunda verir (GECERLI > TASLAK > GECERSIZ > SINIFLANAMADI basliklari HER ZAMAN, sayiyla);
# sinif SABIT sozlukten, ham `[durum: ...]` AYNEN kalir; suphede GECERLI DEGIL. Beklentiler FIKSTURDEN elle yazilidir.
KP_BASLIK = (("GECERLI", "GECERLI KARARLAR ("), ("TASLAK", "KARAR DEGIL - TASLAK/BEKLEYEN ("),
             ("GECERSIZ", "GECERSIZ ("), ("SINIFLANAMADI", "SINIFLANAMADI ("))


def _kp_adr(durumlar, pre="docs/ADR/"):
    """{yol: icerik}: `durumlar` = [(no, ad, 'Durum degeri' ya da None)] -> `# ADR n` + (varsa) `Durum: deger`."""
    return {"%s%04d-%s.md" % (pre, no, ad): "# ADR %d\n%s" % (no, ("Durum: %s\n" % d) if d is not None else "")
            for no, ad, d in durumlar}


def _kp_gruplar(kok):
    """canli `karar-kaynagi` blogu -> {sinif: (baslik_satiri, [satirlar])} (sinif = KP_BASLIK sirasiyla)."""
    blok = BLOK_KARAR.search(_canli_devral(kok))
    out, kur = {}, None
    for x in (blok.group(2) if blok else "").splitlines():
        for sinif, on in KP_BASLIK:
            if x.startswith(on):
                out[sinif] = (x, [])
                kur = sinif
        if x.startswith("- ") and kur and not x.startswith("- karar dizini") and not x.startswith("- motorun"):
            out[kur][1].append(x[2:])
    return out


def _kp_devral(motor, kok, durumlar, ek=None):
    dosyalar = _kp_adr(durumlar)
    dosyalar.update(ek or {})
    rc, c = hal_yol(motor, kok, dosyalar, DURUM_BOLUMLU)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit=%s): %s" % (rc, c.strip().split("\n")[-1][:160]))
    return c, _kp_gruplar(kok)


def _kp_ad(g, sinif, no):
    return [x for x in g.get(sinif, ("", []))[1] if x.startswith("%04d-" % no)]


def kp_sinif(motor, taban):
    """PSINIF: her sinifin ADR'si KENDI grubunda (accepted · proposed · superseded by 0002 · partially implemented),
    ham `[durum: ...]` AYNEN · POZET: derle/devral cikti satiri `KARAR SINIFI: ...`."""
    b = []
    c, g = _kp_devral(motor, os.path.join(taban, "kp_s"),
                      [(1, "a", "accepted"), (2, "b", "proposed"), (3, "c", "superseded by 0002"),
                       (4, "d", "partially implemented")])
    for no, sinif, ham in ((1, "GECERLI", "accepted"), (2, "TASLAK", "proposed"), (3, "GECERSIZ", "superseded by 0002"),
                           (4, "SINIFLANAMADI", "partially implemented")):
        sat = _kp_ad(g, sinif, no)
        if len(sat) != 1 or not sat[0].endswith("[durum: %s]" % ham):
            b.append(("PSINIF", "ADR %d `%s` grubunda degil ya da ham beyan degisti: grup=%r" % (no, sinif, sat)))
    if "KARAR SINIFI: GECERLI 1 · TASLAK 1 · GECERSIZ 1 · SINIFLANAMADI 1" not in c:
        b.append(("POZET", "devral cikti satiri `KARAR SINIFI: GECERLI 1 · TASLAK 1 · GECERSIZ 1 · SINIFLANAMADI 1` YOK"))
    return b


def kp_oncelik(motor, taban):
    """PONCELIK: `TASLAK v6 — KİLİTLİ DEĞİL` · `GÖVDE YAZILDI — KİLİT BEKLİYOR` · `kabul bekliyor` -> UCU DE TASLAK
    (TASLAK, GECERLI'nin USTUNDE; `kilit`/`kabul` koku tasisalar da karar DEGIL)."""
    c, g = _kp_devral(motor, os.path.join(taban, "kp_o"),
                      [(1, "a", "TASLAK v6 — KİLİTLİ DEĞİL"), (2, "b", "GÖVDE YAZILDI — KİLİT BEKLİYOR"),
                       (3, "c", "kabul bekliyor")])
    kotu = [no for no in (1, 2, 3) if len(_kp_ad(g, "TASLAK", no)) != 1]
    return [("PONCELIK", "TASLAK olmasi gereken ADR'ler baska grupta: %r (GECERLI=%r)"
             % (kotu, g.get("GECERLI", ("", []))[1][:3]))] if kotu else []


def ks_hepsi(motor, taban, motor_metin, tag, yalniz=None, yaz_=False):
    """K-SATIR + K-YOL + K-DURUM + K-GECIS + K-ISARET kollari (ya da `yalniz` verilen KOL adlari) -> [(etiket, mesaj)]."""
    kollar = (("K-SATIR", "dongu", lambda: ks_dongu(motor, taban, tag + "d")),
              ("K-SATIR", "tanimsiz", lambda: ks_tanimsiz(motor, os.path.join(taban, tag + "t"))),
              ("K-SATIR", "sahiplik", lambda: ks_sahiplik(motor, os.path.join(taban, tag + "s"))),
              ("K-SATIR", "kume", lambda: ks_kume(motor_metin)),
              ("K-SATIR", "cokkopya", lambda: ks_cokkopya(motor, os.path.join(taban, tag + "c"))),
              ("K-SATIR", "gitsiz", lambda: ks_gitsiz(motor, os.path.join(taban, tag + "g"))),
              ("K-SATIR", "aralik", lambda: ks_aralik(motor, os.path.join(taban, tag + "a"))),
              ("K-YOL", "ykontrol", lambda: ky_kontrol(motor, os.path.join(taban, tag + "yk"))),
              ("K-YOL", "yadr", lambda: ky_adr(motor, os.path.join(taban, tag + "ya"))),
              ("K-YOL", "ysahiplik", lambda: ky_sahiplik(motor, os.path.join(taban, tag + "ys"))),
              ("K-YOL", "ycase", lambda: ky_case(motor, os.path.join(taban, tag + "yc"))),
              ("K-YOL", "ycok", lambda: ky_cok(motor, os.path.join(taban, tag + "ym"))),
              ("K-YOL", "ykesif", lambda: ky_kesif(motor, os.path.join(taban, tag + "ye"))),
              ("K-YOL", "ykacis", lambda: ky_kacis(motor, os.path.join(taban, tag + "yx"))),
              ("K-DURUM", "kdurum", lambda: kd_durum(motor, os.path.join(taban, tag + "kd"))),
              ("K-GECIS", "kgecis", lambda: kg_gecis(motor, os.path.join(taban, tag + "kg"))),
              ("K-ISARET", "kisaret", lambda: ki_isaret(motor, os.path.join(taban, tag + "ki"))),
              ("P1", "psinif", lambda: kp_sinif(motor, os.path.join(taban, tag + "p1"))),
              ("P1", "poncelik", lambda: kp_oncelik(motor, os.path.join(taban, tag + "p2"))))
    b = []
    for grup, ad, kol in kollar:
        if yalniz is None or ad in yalniz:
            sonuc = kol()
            if yaz_:
                print("  %s/%-9s: %s" % (grup, ad, "TEMIZ" if not sonuc else
                                         "BEKLENMEDIK (%s)" % ", ".join(sorted({e for e, _ in sonuc}))))
            b += sonuc
    return b


# Her sabotaj YALNIZ kendi ekseninin etiketini ateslemeli (BIREBIR): (ad, ankor, yeni, etiket, kollar).
# Ankor motorda TAM 1 kez gecmeli (aksi OLCULEMEDI). "ISIRDI" = sabotajli motorda o eksen KIRMIZI.
KS_SABOTAJLAR = (
    ("M-S1 atif KAYMASI gorulmez", 'KAYMA',
     '    return "KAYMA", ",".join(str(i) for i in yer[:5]) + (",…" if len(yer) > 5 else "")\n',
     '    return "TUTUYOR", None      # MUTANT\n', ("dongu",)),
    ("M-S2 yanlis alarm (pencere yok sayilir)", 'KONTROL',
     '    if any(desen.search(s) for s in sat[max(0, bas - 3):son + 2]):\n',
     '    if False:      # MUTANT\n', ("dongu",)),
    ("M-S3 tanimlayicisiz madde KAYMA sayilir", 'TANIMSIZ',
     '    if not tanimlar:\n        return "OLCULEMEDI", "TANIMLAYICI_YOK"\n',
     '    if not tanimlar:\n        return "KAYMA", "0"      # MUTANT\n', ("tanimsiz",)),
    ("M-S4 derle blogu yazmaz", 'BLOK',
     '    L = _motor_blogu_esitle(y, rc, L, ertele, eklenen, _ATIF_KONU, _ATIF_KONU_ACIKLAMA,\n'
     '                            _atif_blok_govdesi(kayma))\n',
     '    pass      # MUTANT\n', ("dongu",)),
    ("M-S5 H18 bulgusu F'ye girer (exit degisir)", 'EXIT',
     '    _kapi_h18(N, kok, y)\n', '    _kapi_h18(F, kok, y)      # MUTANT\n', ("dongu",)),
    ("M-S6 sahip=proje blogu ezilir", 'SAHIPLIK',
     '    if bul == "BOZUK" or (bul and bul[2].get("sahip") != "hafiza-kur"):\n        return L\n',
     '    if bul == "BOZUK":\n        return L      # MUTANT\n', ("sahiplik", "ysahiplik")),
    ("M-S7 ayni icerikte blok yeniden yazilir", 'IDEMPOTANS',
     '    if bul and govde is not None and _motor_blok_ayni(L, bul, govde):\n        return L\n',
     '    if False:      # MUTANT\n        return L\n', ("dongu", "yadr")),
    ("M-S8 giderilen kaymada blok KALIR", 'KALDIRMA',
     '    if not kayma:\n        return None\n',
     '    if not kayma:\n        return ["> kayma yok"]      # MUTANT\n', ("dongu",)),
    ("M-S9 budama kumesi H14'unkinden AYRISIR", 'KUME',
     '_ATIF_HARIC = {".git", "node_modules", "__pycache__", ".venv", "arsiv", "gunluk", "dist", "build"}\n',
     '_ATIF_HARIC = {".git", "__pycache__", ".venv", "arsiv", "gunluk", "dist", "build"}      # MUTANT\n',
     ("kume", "cokkopya")),
    ("M-S10 yeni satirlar BEYAN edilmez", 'MUHASEBE',
     '    eklenen.extend(yeni)\n', '    pass      # MUTANT\n', ("dongu",)),
    ("M-S11 dosya agaci git'ten okunur", 'GITSIZ',
     '    for r0, d0, f0 in os.walk(kok):\n'
     '        d0[:] = sorted(d for d in d0 if d not in _ATIF_HARIC)\n'
     '        for f in sorted(f0):\n'
     '            idx.setdefault(f, []).append(_rel(os.path.join(r0, f), kok))\n',
     '    for x in subprocess.run(["git", "-C", kok, "ls-files", "-z"],\n'
     '                            capture_output=True).stdout.decode("utf-8", "replace").split("\\0"):\n'
     '        if x:\n'
     '            idx.setdefault(x.rsplit("/", 1)[-1], []).append(x)      # MUTANT\n', ("gitsiz",)),
    ("M-S12 yol:N-M araligi yok sayilir", 'ARALIK',
     '        out.append((no, t, m.group(1), bas, int(m.group(3) or bas), tan))\n',
     '        out.append((no, t, m.group(1), bas, bas, tan))      # MUTANT\n', ("aralik",)),
    # ---- K-YOL ----------------------------------------------------------------------------------
    ("M-Y1 karar dizini KESFI kapali", 'YBLOK',
     '    out, gorulen, atlanan = [], set(), []\n    for aday in _KARAR_ADAYLARI:\n',
     '    out, gorulen, atlanan = [], set(), []\n    for aday in ():      # MUTANT\n', ("yadr",)),
    ("M-Y2 bos dizin (ADR'siz) 'bulundu' sayilir", 'YKONTROL',
     '        if not adlar:\n            continue\n',
     '        if False:      # MUTANT\n            continue\n', ("ykontrol",)),
    ("M-Y3 .hafizarc'a yol YAZILMAZ", 'YRC',
     "    rc.update(_devral_karar_rc(karar_dizini))   # K-YOL: ADR'siz projede BOS -> .hafizarc bayt-bayt eskisi\n",
     '    pass      # MUTANT\n', ("yadr",)),
    ("M-Y4 silinen dizinde blok SESSIZCE kalir", 'YKAYIP',
     '    govde = _karar_blok_govdesi(y, kd) if kd else None\n    if govde is not None:\n',
     '    govde = _karar_blok_govdesi(y, kd) if (kd and os.path.isdir(os.path.join(y.kok, *kd.split("/")))) '
     'else None      # MUTANT\n    if govde is not None:\n', ("yadr",)),
    ("M-Y5 devral ozet satiri basilmaz", 'YOZET',
     '    karar_dizini = devir_karar_ozeti(kok)       # K-YOL: projenin KENDI karar dizini (dosyalara dokunulmaz)\n',
     '    karar_dizini = (_karar_dizinleri(kok)[0] or [("", [])])[0][0]      # MUTANT\n', ("yadr",)),
    ("M-Y6 konu KONULAR.md'ye eklenmez", 'YKONU',
     '    _devral_karar_konusu(y, rc)                 # K-YOL: DEVIR halkasindan ONCE (politika dosyasi yukte)\n',
     '    pass      # MUTANT\n', ("yadr",)),
    ("M-Y7 kural isaretli baslik maskelenmez", 'YMASKE',
     '    ok = [s for s in govde if not kural_isareti_var(s, rc["kural_isaretleri"])]\n',
     '    ok = list(govde)      # MUTANT\n', ("yadr",)),
    ("M-Y8 baslikta backtick etkisizlestirilmez", 'YBACKTICK',
     '            t = unicodedata.normalize("NFC", m.group(1)).replace("`", "\'").replace("](", "] (")\n',
     '            t = unicodedata.normalize("NFC", m.group(1))      # MUTANT\n', ("yadr",)),
    ("M-Y9 derle blogu diskten yenilemez", 'YYENILE',
     '    if govde is not None:\n        _karar_sinif_yaz()\n        L = _motor_blogu_esitle(y, rc, L, ertele, eklenen, _KARAR_KONU, _KARAR_KONU_ACIKLAMA, govde)\n',
     '    if False:      # MUTANT\n        _karar_sinif_yaz()\n        L = _motor_blogu_esitle(y, rc, L, ertele, eklenen, _KARAR_KONU, _KARAR_KONU_ACIKLAMA, govde)\n',
     ("yadr",)),
    ("M-Y10 ADR dosyalarina DOKUNULUR", 'YDOKUNMA',
     '        dur = _karar_durum(os.path.join(d, ad))\n',
     '        dur = _karar_durum(os.path.join(d, ad))\n'
     '        with open(os.path.join(d, ad), "ab") as f:\n            f.write(b"\\n")      # MUTANT\n',
     ("yadr",)),
    ("M-Y11 dizin adi harf-duyarli aranir", 'YCASE',
     '                        if x.lower() == parca.lower() and os.path.isdir(os.path.join(yol, x)))\n',
     '                        if x == parca and os.path.isdir(os.path.join(yol, x)))      # MUTANT\n', ("ycase",)),
    ("M-Y12 cok adayda SON aday secilir", 'YCOK',
     '    rel, adlar = bulunan[0]\n', '    rel, adlar = bulunan[-1]      # MUTANT\n', ("ycok",)),
    ("M-Y13 --kesif karar dizinini raporlamaz", 'YKESIF',
     '        devir_karar_ozeti(kok)\n', '        pass      # MUTANT\n', ("ykesif",)),
    ("M-Y14 ADR deseni .gitkeep/README'yi de sayar", 'YSAYIM',
     '_KARAR_AD = re.compile(r"^(?:\\d{4}-.+|ADR-.+)\\.md$", re.I)\n',
     '_KARAR_AD = re.compile(r".+", re.I)      # MUTANT\n', ("yadr",)),
    ("M-Y15 baslik yokken blok DOSYA SONUNA yazilir", 'YYER',
     '    k = 1 if (L and L[0].startswith("# ")) else 0\n    while k < len(L) and L[k].startswith(">"):\n'
     '        k += 1\n    return k\n', '    return len(L)      # MUTANT\n', ("ycok",)),
    ("M-Y16 proje DISINA bagli dizin okunur", 'YKACIS',
     '        if kok_disina_mi(kok, os.path.join(kok, *rel.split("/"))):\n            atlanan.append(rel)\n'
     '            continue\n',
     '        if False:      # MUTANT\n            atlanan.append(rel)\n            continue\n', ("ykacis",)),
    # ---- K-DURUM ----------------------------------------------------------------------------------
    ("M-D1 durum cikarimi kapali (hep BEYANSIZ)", 'KDURUM',
     '        m = _KARAR_DURUM_ANAHTAR.match(s.rstrip("\\r"))\n',
     '        m = None      # MUTANT\n', ("kdurum",)),
    ("M-D2 beyansiz ADR bos birakilir", 'KBEYANSIZ',
     '    return " — [durum: BEYANSIZ]"\n', '    return ""      # MUTANT\n', ("kdurum",)),
    ("M-D3 uzun durum kirpilmaz", 'KKESME',
     '            if len(v) > _KARAR_DURUM_TAVAN:\n',
     '            if False:      # MUTANT\n', ("kdurum",)),
    ("M-D4 ilk 30 satir siniri yok", 'KPENCERE',
     '.split("\\n")[:_KARAR_DURUM_PENCERE]', '.split("\\n")      # MUTANT', ("kdurum",)),
    ("M-D5 motorun kendi kararinda durum yok", 'KMOTOR',
     '            dur = _karar_durum(os.path.join(y.kararlar, k["dosya"]))\n',
     '            dur = ""      # MUTANT\n', ("kdurum",)),
    # ---- K-GECIS ----------------------------------------------------------------------------------
    ("M-G1 kurulu projede keşif kapali", 'KGKESIF',
     '    rel, adlar, ek = _karar_ilk(y.kok)\n    rc["karar_dizini"] = rel\n',
     '    rel, adlar, ek = "", [], ""      # MUTANT\n    rc["karar_dizini"] = rel\n', ("kgecis",)),
    ("M-G2 bilincli bos deger anahtar yok sayilir", 'KGBOS',
     '    if "karar_dizini" in rc:\n        return\n', '    if rc.get("karar_dizini"):      # MUTANT\n        return\n', ("kgecis",)),
    ("M-G3 kesif beyan EDILMEZ", 'KGBEYAN',
     '        print("KARAR DIZINI KESFEDILDI: %s (%d)%s — .hafizarc\'a yazildi" % (rel, adet, ek))\n',
     '        pass      # MUTANT\n', ("kgecis",)),
    ("M-G4 bulunamazsa `\"\"` YAZILMAZ (her derle yeniden tarar)", 'KGYOK',
     '    ertele.insert(0, (_karar_rc_yaz, (rel, len(adlar), ek)))\n',
     '    if rel:      # MUTANT\n        ertele.insert(0, (_karar_rc_yaz, (rel, len(adlar), ek)))\n', ("kgecis",)),
    ("M-G6 anahtar kosulu TERS (yalniz anahtar VARKEN tarar)", 'KGKESIF',
     '    if "karar_dizini" in rc:\n        return\n', '    if "karar_dizini" not in rc:      # MUTANT\n        return\n', ("kgecis",)),
    ("M-G5 .hafizarc yeniden bicimlenir/siralanir", 'KGRC',
     '    yaz(p, "%s%s\\n  \\"karar_dizini\\": %s\\n%s"\n'
     '        % (once, "" if once.endswith("{") else ",", json.dumps(rel, ensure_ascii=False), t[son:]))\n',
     '    yaz(p, json.dumps(dict(json.loads(t), karar_dizini=rel), ensure_ascii=False, indent=4) + "\\n")      # MUTANT\n',
     ("kgecis",)),
    # ---- K-ISARET ---------------------------------------------------------------------------------
    ("M-I1 kur yeni kural evine isaretci yazmaz", 'KIKUR',
     '                     % (ad, _ISARETCI % rc["canli"]))\n',
     '                     % (ad, "> (isaretci yok)"))      # MUTANT\n', ("kisaret",)),
    ("M-I2 devral yeni kural evine isaretci yazmaz", 'KIDEVRAL',
     '                     % (rc["ad"], _ISARETCI % rc["canli"]))\n',
     '                     % (rc["ad"], "> (isaretci yok)"))      # MUTANT\n', ("kisaret",)),
    ("M-I3 kapi H19 kontrolu kapali", 'KIKAPI',
     '    if not _isaretci_var(oku(y.kural), canli):\n', '    if False:      # MUTANT\n', ("kisaret",)),
    ("M-I4 H19 uyarisi cikis kodunu degistirir", 'KIEXIT',
     '    _kapi_h18(N, kok, y)\n', '    _kapi_h18(F, kok, y)      # MUTANT\n', ("kisaret",)),
    ("M-I5 mevcut kural evinde oneri basilmaz", 'KIONERI',
     '    if os.path.realpath(y.kural) != os.path.realpath(y.canli) and not _isaretci_var(oku(y.kural), rc["canli"]):\n',
     '    if False:      # MUTANT\n', ("kisaret",)),
    ("M-I6 mevcut kural evine isaretci YAZILIR", 'KIBAYT',
     '              % (rc["kural_evi_dosya"], _ISARETCI % rc["canli"]))\n',
     '              % (rc["kural_evi_dosya"], _ISARETCI % rc["canli"]))\n'
     '        yaz(y.kural, oku(y.kural) + (_ISARETCI % rc["canli"]) + "\\n")      # MUTANT\n', ("kisaret",)),
    ("M-I7 isaretci VARKEN de H19 konusur (yanlis pozitif)", 'KISESSIZ',
     '    if not _isaretci_var(oku(y.kural), canli):\n', '    if True:      # MUTANT\n', ("kisaret",)),
    ('M-P1a siniflama kapali (hepsi GECERLI)', 'PSINIF',
     '    return next((sinif for sinif, desen in _SINIF_DESEN if desen.search(t)), "SINIFLANAMADI")\n',
     '    return "GECERLI"      # MUTANT\n', ('psinif',)),
    ('M-P1b KARAR SINIFI ozet satiri basilmaz', 'POZET',
     '    if _KARAR_SINIF_SON[0]:\n',
     '    if False:      # MUTANT\n', ('psinif',)),
    ("M-P1c GECERLI sozlugu TASLAK'tan once denenir", 'PONCELIK',
     '    return next((sinif for sinif, desen in _SINIF_DESEN if desen.search(t)), "SINIFLANAMADI")\n',
     '    return next((sinif for sinif, desen in reversed(_SINIF_DESEN) if desen.search(t)), "SINIFLANAMADI")      # MUTANT\n', ('poncelik',)),
)


def ks_sabotajlar(s, taban):
    """K-SATIR sabotajlari: -> (kacan_adlar, olculemedi_mesaji_ya_da_None). Ortusme (baska eksenin de
    atesledigi) BILGI olarak basilir; kapiyi kor saymaz ama GORUNUR kilinir."""
    kacan = []
    for sira, (ad, etiket, ankor, yeni, kollar) in enumerate(KS_SABOTAJLAR, 1):
        d = tempfile.mkdtemp(prefix="ks_mut%d_" % sira, dir=taban)
        sab, hata = _sabotajli_yaz(s, ankor, yeni, d, "ks%d" % sira)
        if sab is None:
            return kacan, "%s: %s" % (ad, hata)
        with io.open(sab, encoding="utf-8", newline="") as f:
            sab_metin = f.read()
        try:
            atesler = {e for e, _ in ks_hepsi(sab, d, sab_metin, "m", yalniz=kollar)}
        except Kurulamadi as e:
            return kacan, "%s: %s" % (ad, e)
        if etiket in atesler:
            ort = sorted(atesler - {etiket})
            print("  %-42s -> ISIRDI ✓  (%s%s)" % (ad, etiket, ("; ortusme: " + ", ".join(ort)) if ort else ""))
        else:
            print("  %-42s -> KACTI ✗  (%s ekseni sabotajda da TEMIZ — kol bu olcumu HIC OLCMUYOR; atesleyen: %s)"
                  % (ad, etiket, ", ".join(sorted(atesler)) or "hicbiri"))
            kacan.append(ad)
    return kacan, None


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok (bu batarya `devral --esle` icin git ister).")
        return 2

    print(CIZGI)
    print("GUNCEL DURUM KAPISI MUTANTI — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="guncel_durum_kapisi_")
    try:
        b = []

        # ---- KAPI-1 ----------------------------------------------------
        try:
            k1, c1 = kapi1_bolum_yok_taze(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-1 bolum YOK (taze)   OLCULEMEDI: %s" % e)
            return 2
        var1 = _h17_var_mi(c1)
        print("  KAPI-1 bolum YOK (taze)   : kapi exit=%s · [H17] VAR=%s" % (k1, var1))
        if k1 == 0:
            b.append("KAPI-1: kapi exit 0 — bolum yokken YESIL olmamali")
        if not var1:
            b.append("KAPI-1: [H17] bulgusu (bolumu ADLANDIRAN) ciktida YOK")

        # ---- KAPI-2 ----------------------------------------------------
        try:
            k2, c2, kok2 = kapi2_bolum_yok_fragman_var(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-2 bolum YOK+fragman  OLCULEMEDI: %s" % e)
            return 2
        atlandi_var = "ATLANDI" in c2
        gunluk2 = os.path.join(kok2, "gunluk")   # y.gunluk (BEKLEYEN, henuz arsivlenmemis)
        fragman_kaldi = os.path.isdir(gunluk2) and any(
            f.endswith(".md") for f in os.listdir(gunluk2))
        print("  KAPI-2 bolum YOK+fragman  : derle exit=%s · ATLANDI=%s · fragman gunluk'te KALDI=%s"
              % (k2, atlandi_var, fragman_kaldi))
        if k2 != 2:
            b.append("KAPI-2: derle exit %s (2 bekleniyordu — isir'in 'OLCULEMEDI' dili)" % k2)
        if not atlandi_var:
            b.append("KAPI-2: 'ATLANDI' satiri ciktida YOK")
        if not fragman_kaldi:
            b.append("KAPI-2: fragman gunluk/'te KALMADI — SILINMIS/tasinmis olabilir")

        # ---- KAPI-3 (KONTROL KOLU) --------------------------------------
        try:
            k3, c3 = kapi3_bolum_var(yol, taban)
        except Kurulamadi as e:
            print("  KAPI-3 bolum VAR (kontrol) OLCULEMEDI: %s" % e)
            return 2
        var3 = _h17_var_mi(c3)
        islendi3 = "DERLENDI: 1 fragman islendi" in c3
        print("  KAPI-3 bolum VAR (kontrol): derle exit=%s · [H17] VAR=%s · 1 fragman islendi=%s"
              % (k3, var3, islendi3))
        if k3 != 0:
            b.append("KAPI-3: derle exit %s (0 bekleniyordu — bolum VARKEN bugunku davranis)" % k3)
        if var3:
            b.append("KAPI-3: [H17] bolum VARKEN de FIRE etti (yanlis pozitif)")
        if not islendi3:
            b.append("KAPI-3: fragman islenmedi (bolum VARKEN 1 fragman islenmeli)")

        # ---- K-SATIR (H18) KOLLARI -----------------------------------------
        try:
            ks = ks_hepsi(yol, taban, s, "k", yaz_=True)
        except Kurulamadi as e:
            print("  K-SATIR kollari           OLCULEMEDI: %s" % e)
            return 2
        b += ["K-SATIR/%s: %s" % (e, m) for e, m in ks]

        for x in b:
            print("      ! %s" % x)
        if b:
            print("\nSONUC: KIRMIZI — temiz surumun kollari BEKLENMEDIK.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = []

        # ---- M-A ---------------------------------------------------------
        mdirA = tempfile.mkdtemp(prefix="mutantA_", dir=taban)
        sabA, hataA = _sabotajli_yaz(s, ANKOR_H17_KOSUL, YENI_MA, mdirA, "mutantA")
        if sabA is None:
            print("  M-A H17 kosulu sokulur (False)   OLCULEMEDI: %s" % hataA)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kA, cA = kapi1_bolum_yok_taze(sabA, os.path.join(taban, "tA"))
        except Kurulamadi as e:
            print("  M-A H17 kosulu sokulur (False)   OLCULEMEDI: %s" % e)
            return 2
        if not _h17_var_mi(cA):
            print("  M-A H17 kosulu sokulur (False)   -> ISIRDI ✓  (bolum YOKKEN [H17] "
                  "ARTIK cikmiyor)")
        else:
            print("  M-A H17 kosulu sokulur (False)   -> KACTI ✗  ([H17] hala cikiyor — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-A")

        # ---- M-B ---------------------------------------------------------
        mdirB = tempfile.mkdtemp(prefix="mutantB_", dir=taban)
        sabB, hataB = _sabotajli_yaz(s, ANKOR_MB, YENI_MB, mdirB, "mutantB")
        if sabB is None:
            print("  M-B derle exit 2'si sokulur      OLCULEMEDI: %s" % hataB)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kB, cB, _ = kapi2_bolum_yok_fragman_var(sabB, os.path.join(taban, "tB"))
        except Kurulamadi as e:
            print("  M-B derle exit 2'si sokulur      OLCULEMEDI: %s" % e)
            return 2
        if kB != 2:
            print("  M-B derle exit 2'si sokulur      -> ISIRDI ✓  (exit artik %s — "
                  "'OLCULEMEDI' sozlesmesi kayboldu)" % kB)
        else:
            print("  M-B derle exit 2'si sokulur      -> KACTI ✗  (exit hala 2 — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-B")

        # ---- M-C ---------------------------------------------------------
        mdirC = tempfile.mkdtemp(prefix="mutantC_", dir=taban)
        sabC, hataC = _sabotajli_yaz(s, ANKOR_H17_KOSUL, YENI_MC, mdirC, "mutantC")
        if sabC is None:
            print("  M-C H17 kosulsuz FIRE eder (True) OLCULEMEDI: %s" % hataC)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        try:
            kC, cC = kapi3_bolum_var(sabC, os.path.join(taban, "tC"))
        except Kurulamadi as e:
            print("  M-C H17 kosulsuz FIRE eder (True) OLCULEMEDI: %s" % e)
            return 2
        if _h17_var_mi(cC):
            print("  M-C H17 kosulsuz FIRE eder (True) -> ISIRDI ✓  (bolum VARKEN de "
                  "[H17] cikti — yanlis pozitif ekseni olculuyor)")
        else:
            print("  M-C H17 kosulsuz FIRE eder (True) -> KACTI ✗  ([H17] hala sessiz — "
                  "kapi bu olcumu HIC OLCMUYOR)")
            kacan.append("M-C")

        # ---- K-SATIR sabotajlari -------------------------------------------
        print("\n--- K-SATIR / K-YOL SABOTAJLARI (her biri YALNIZ kendi ekseninde ISIRMALI) ---")
        ks_kacan, ks_hata = ks_sabotajlar(s, taban)
        if ks_hata:
            print(CIZGI)
            print("SONUC: OLCULEMEDI — K-SATIR sabotaji kurulamadi (arac kusuru, kapi kor DEGIL): %s" % ks_hata)
            return 2
        kacan += ks_kacan

        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %s beklendigi gibi olculmedi." % ", ".join(kacan))
            return 1
        print("SONUC: YESIL — uc kol + yedi K-SATIR + yedi K-YOL + bir K-DURUM + bir K-GECIS + bir K-ISARET kolu temiz, uc mutant + %d "
              "K-SATIR/K-YOL/K-DURUM/K-GECIS/K-ISARET sabotaji AYRI eksende ISIRDI." % len(KS_SABOTAJLAR))
        return 0
    finally:
        _sil(taban)


if __name__ == "__main__":
    sys.exit(main())

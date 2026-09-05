#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H9 KESME MUTANTI (M-Y4) — `_kapi_h9`nun "git deposu OKUNAMADI" hukmu, git'in
ilk satirini KIRPMADAN mi basiyor? (kalem5-tarama/IS_EMRI_SIK_A.md D2, Onur
kilidi SIK A, 19 Agu 2026 · dayanak: kalem5-tarama/KALEM5_KESME_TARAMASI.md)

NEDEN VAR
  `olculemedi_kesme_mutanti.py`nin (M-Y3, D1) ikiz kardesi: AYNI kalibin
  ikinci uyesi. `hafiza.py` satir ~3956, git alt-surecinin stderr'inin ILK
  SATIRINI `[:120]` ile kesiyordu; o satir (`fatal: ...`) sik sik KOK
  DIZININ YOLUNU tasir. Kok uzunsa yol KIRPILIR, kullanici HANGI DIZIN
  oldugunu YARIM gorur.

NE OLCER — CIFT KOLLU (M-Y3 ile AYNI kalip; POSIX SARTI YOK, UC PLATFORMDA KAPI)
    M-Y4 UZUN KOL : kok >= 170 karakter. Motora ESKI kesme ([:120]) GERI
                    enjekte edilir; H9 satiri KIRPILMALI (kapanis tirnagi
                    `'` ile BITMEMELI) — kapi kusuru DOGRU yakaladi (ISIRDI).
    M-Y4 KISA KOL : kok "kisa" — AMA bu ARTIK bir VARSAYIM DEGIL, bir OLCUM
                    (20 Agu 2026 duzeltmesi, asagidaki 🔴 nota bak). Kolun
                    KENDI ON SARTI ("kirpilmamis H9 mesaji esigin altinda
                    mi") sabotajsiz/duzeltilmis motorla ONCE OLCULUR; ancak
                    saglaniyorsa sabotaj kosulur ve KEHANET (satir kapanis
                    tirnagi `'` ile BITMELI — KACIS BEKLENEN) sinanir. On
                    sart SAGLANMIYORSA kol OLCULEMEDI doner, ASLA BEKLENMEDIK
                    DONMEZ — kor kolun ON SARTININ sinamadigi bir hal, bir
                    kusur BULGUSU degildir.

  🔴 DUZELTME 1 (Onur kilidi 20 Agu 2026, Cowork CI 32250138848 + yerel
  yeniden uretim): KISA KOL "kok kisa = mkdtemp varsayilani" VARSAYIMINI
  tasiyordu. `tempfile.mkdtemp()`nin varsayilan tabani PLATFORMA GORE COK
  FARKLI: Linux ~24 karakter (mesaj 24+53=77, esik 120'nin ALTINDA — kor
  kalir, DOGRU), macOS ~68 karakter (mesaj 68+53=121, esik 120'nin
  USTUNDE — KIRPILIR, kor kol kor KALMAZ). CI'da `H9 kesme mutanti
  (macos-latest)` bu yuzden KIRMIZI yandi: `1/2 kol - 1 beklenmedik`.
  UZUN KOL YESILDI — yani ε₂ tetikleyicisinin KENDISI macOS'ta calisiyor;
  kusur yalniz KISA KOL'un ON SART VARSAYIMINDAYDI.
  Kok'u KENDIMIZ kisa kurmak TEK BASINA YETMEZ: macOS `/tmp`yi
  `/private/tmp`e cozer ve git REALPATH basar (M-A8 dersiyle AYNI mayin —
  H16-KESME-DUZELTME-BRIEF.md). Bu yuzden BIRINCI duzeltme kok'u KISALTMAK
  DEGIL, kolun ON SARTINI dogrudan OLCMEKTIR: duzeltilmis motorla (sabotaj
  YOK) ayni kok/ortamda H9 satiri BIR KEZ kosulur, mesaj uzunlugu esikle
  (dinamik olarak `_SABOTAJLI`den okunur, sabit YAZILMAZ) karsilastirilir.
  Ilk yazimda esikten TUREYEN bir PAY (`esik // 10`) ile bir "guvenli sinir"
  belirleniyordu; bu DUZELTME 3'te KALDIRILDI (asagiya bak, CI #83) —
  karsilastirma simdi DOGRUDAN esige karsi: asilirsa OLCULEMEDI (exit 2),
  asilmazsa sabotaj kosulur.

  🔴 DUZELTME 2 (Onur kilidi 20 Agu 2026, SIK (a) — "kisa tabani KUR"):
  DUZELTME 1 DOGRUYDU ve yalanci kirmiziyi bitirdi — dogrulandi (kok 66-170
  arasi butun ara degerler exit 2, 0 beklenmedik). AMA "exit 2 de sifirdan
  farkli" ve `h9_kesme_mutanti` isinde `continue-on-error` YOK ⇒ macOS
  KALICI KIRMIZI kalirdi (dogru kirmizi, ama hala kirmizi). Cozum
  DUZELTME 1'i GEREKSIZ KILMAZ, ONA EKLENIR: KISA KOL artik KENDI kisa
  tabanini `_kisa_taban_ac()` ile ACAR (POSIX literal `/tmp` altinda,
  varsa) — `mkdtemp(dir=...)` acikca `dir` verilince TMPDIR/TMP/TEMP ortam
  degiskenlerini YOK SAYAR. OLCULDU (Linux): dis TMPDIR 48/110/150 iken
  bile kok hep ~22 kaliyor, 2/2 exit 0. macOS icin bu bir TAHMINdir (kok
  ~33, mesaj ~86 — esigin (120) altinda BEKLENIYOR); ON SART OLCUMU
  (DUZELTME 1) GEREKSIZ OLMAZ — GERCEK OTORITE odur, kisa taban yalnizca
  on sartin cogu ortamda kendiliginden saglanmasini KOLAYLASTIRIR.
  🔴 DOGRULANDI (CI #83 `32374821806`, is `macos-latest`): SUCCESS —
  `_kisa_taban_ac()` `/private/tmp` realpath'ine RAGMEN calisti, bu
  tahmin TUTTU.

  🔴 DUZELTME 3 (Onur kilidi 20 Agu 2026, CI #83 `32374821806`, is
  `96443570144` KIRMIZI): `windows-latest`de ON SART OLCUMU "112 > guvenli
  sinir=108 (esik=120-pay=12)" icin OLCULEMEDI dondu — AMA 112 < 120:
  gercek sabotaj KIRPMAZDI, kol DOGRU olcerdi. Reddeden fiziksel esik
  DEGIL, PAY'in KENDISIYDI. ON SART, sabotajin kullanacagi AYNI kokte
  AYNI mesaji olcuyor (H9 satiri) — ikisi arasindaki TEK fark kesmenin
  kendisi (`[:120]`); ARADA GURULTU YOK, bu yuzden pay HICBIR SEYI
  KORUMUYORDU, yalniz 109-120 bandini (Windows'un varsayilan kok/
  kullanici-adi uzunlugu tam bu bantta) yalanci OLCULEMEDI'ye
  CEVIRIYORDU. DUZELTME: `pay` KALDIRILDI, karsilastirma FIZIKLE AYNI:
  `mesaj_uzunlugu > esik` ⇒ OLCULEMEDI, `<= esik` ⇒ kol kosar (Cowork
  olcumu: mesaj 119→exit 0, 120(=esik)→exit 0, 121→exit 2, 122→exit 2,
  123→exit 2 — `[:120]` TAM 120 karakterlik dizgeyi kesmez, esikte
  ölçüt birebir dogru). 🔴 PAY GERI EKLENMEZ: on sart GURULTUSUZ oldugu
  icin (ayni kok, ayni ortam, TEK degisken kesmenin kendisi) fiziksel
  esikten daha KATI bir olcut hicbir seyi korumaz, yalniz yalanci-
  kirmizi uretir — sonraki tur "guvenlik payi ekleyeyim" DEMESIN.

  🔴 DUZELTME 4 (Onur kilidi 5 Eylul 2026, IS_EMRI_H9_KESME_CAPA.md — kaynak
  capasi KALEM 1'in stderr-isaret duzeltmesiyle ESKIDI, Cowork bulut Linux
  motor `37908e38` ile OLCTU): `hafiza.py`nin H9 dalindaki
  `_sb = (r.stderr or _rg.stderr or "").strip().split("\n")[0]` satiri
  `_sb = _ilk_satir_isaretli((r.stderr or _rg.stderr or "").strip())`e
  degisti (B6 SIK beta, IS_EMRI_H9_STDERR_ISARET.md) — eski capa metni
  dosyada ARTIK 0 kez geciyordu, sabotaj kendi muhafazasiyla ARAC KUSURU
  verirdi (KALEM A: capa TASINDI, davranis AYNI — sabotaj hala kuyruga
  `[:120]` ekler/cikarir, `_ilk_satir_isaretli(...)`nin KENDISI DOKUNULMAZ).

  🔴 Capa tasimasi TEK BASINA YETMEDI (denendi, Cowork, 1/2 kol beklenmedik):
  kol capasi `satir.rstrip().endswith("'")` hala satirin TEK SATIRLIK
  oldugunu VARSAYIYORDU. `_ilk_satir_isaretli` COK SATIRLI govdenin (git'in
  dubious-ownership stderr'i OLCULEN HER ZAMAN 4 satirdir) SONUNA
  " (+N satir: stderr)" ekleyince satir ARTIK `'` ile degil `)` ile bitiyor
  — M-Y3'un (olculemedi_kesme_mutanti.py) BIREBIR AYNI mayini, AYNI sinifin
  UCUNCU ISIRISI (B6→M-Y3→h9_kesme). DUZELTME (KALEM B): M-Y3'teki
  `_b6_isaretini_ayikla()` bu dosyaya KENDI KOPYASI olarak eklendi (Onur
  kilidi: motordan ya da diger mutanttan IMPORT EDILMEZ — kum havuzu
  izolasyonu ilkesi, mutant dosyalari birbirinden BAGIMSIZ kalir) — `'`
  sinamasindan ONCE isaret AYIKLANIR, `'` sonu ISARETSIZ govde uzerinde
  olculur. `in` KULLANILMADI (M-Y3 §2 dersi: govdede baska yerde gecen bir
  dizgeyi `in` ile aramak mutanti SESSIZCE KOR yapar).

  🔴 KOPYANIN BEDELI (KALEM C): isaret deseni artik IKI mutant dosyasinda
  (bu dosya ve olculemedi_kesme_mutanti.py) AYRI AYRI yazili — biri
  guncellenip digeri unutulursa SESSIZ KORLUK dogar (doktrin md.3: engellemek
  degil GIZLENEMEZ KILMAK). `_isaret_deseni_canli_dogrula()` bu riski
  gizlemez: deseni SABIT bir dizgeye degil, CANLI (duzeltilmis) motorun
  urettigi GERCEK bir H9 satirina karsi sinar; desen eslesmezse `AracKusuru`
  firlatir (main()'in ustteki try/except'i yakalar, exit 3) — sessizce
  "isaret yok" saymaz. Desen eslesirse/H9 satiri hic uretilmezse (ortam
  sinirlamasi) SESSIZCE gecer — bir KAPIDIR, SONUC'a kayit ACMAZ, K1'in
  "2/2 kol" sayimini SISIRMEZ.

  🔴 ESIK KAYMASI (KALEM D, sayi degil FORMUL): isaret govdenin SONUNA
  eklendigi icin kirpilmamis mesaj uzunlugu 19 karakter (isaretin boyu,
  " (+N satir: stderr)") UZADI — kritik kok uzunlugu (mesaj=esik donum
  noktasi) AYNI MIKTARDA ASAGI kaydi (M-Y3'teki 121→102 kaymasinin AYNI
  fizigi). Kisa kolun ON SART OLCUMU (my4_kisa_kol, DUZELTME 1) zaten
  DINAMIKTIR (`_h9_mesaj_govdesi` govdeyi, isaretiyle BIRLIKTE, OLCER) —
  kod bu yuzden DEGISMEDI, yalniz olculen deger KAYDI DEGISTI (kritik kok,
  kisa kolun marji) — bkz. kalem5-tarama/OLCUM_RAPORU_H9_KESME_CAPA.md.

  🔴 DUZELTME 5 (Onur kilidi 5 Eylul 2026, IS_EMRI_H9_KISA_TABAN_WIN.md, EK-2):
  DUZELTME 4'un actigi eslik kaymasi (kritik kok 67→48) `_kisa_taban_ac()`'in
  Windows dalini ISIRIYOR — o dal `/tmp` yoksa (POSIX-disi) DOGRUDAN GENEL
  `tempfile.mkdtemp()`e duserdi, kisaltma hic DENENMEZDI. Builder'in yerel
  Windows makinesinde OLCULDU: genel varsayilan kok ~53 karakter, kritik 48'in
  USTUNDE ⇒ KISA KOL ÖLÇÜLEMEDİ (kusur DEGIL, ama `windows-latest` CI'da da
  AYNI riski tasiyordu — bkz. OLCUM_RAPORU_H9_KESME_CAPA.md §3). DUZELTME:
  `_kisa_taban_ac()`'in POSIX dali (`if os.name == "posix" ...`) BAYT-BAYT
  DOKUNULMADI — yalniz genel-varsayilan SATIRI, CALISMA ZAMANINDA aday
  OLCEN `_kisa_taban_ac_win()`e yonlendirildi (bkz. asagida). Adaylar
  (RUNNER_TEMP · TEMP/TMP · bunlarin 8.3 kisa adi · zaten var olan sistem
  gecici dizini) SABITLENMEZ, HER BIRI var/dizin/yazilabilir/OLUSACAK-kok-
  uzunlugu icin OLCULUR; EN KISASI kazanir, kaybedenler HEMEN silinir.
  Hicbir aday kurulamazsa GENEL `mkdtemp()`e duser — ON SART OLCUMU
  (my4_kisa_kol, DEGISMEDI) o zaman DURUSTCE OLCULEMEDI der; "basarili gibi"
  hicbir sey GOSTERILMEZ. Kazanan aday + kok uzunlugu kayda YAZILIR (KALEM 2)
  — bir sonraki tur kodu okumadan CIKTIDAN okuyabilsin diye.

URETIM TARIFI (SIK EPSILON, 19 Agu 2026 Onur kilidi — birebir OLCULDU)
  git init + commit -> `kur` -> defterler commit'lenir -> `kapi`, git'in KENDI
  sahiplik denetimi `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` ile tetiklenmis olarak
  kosulur. Git `fatal: detected dubious ownership in repository at '<KOK>'`
  verir (exit 128); hem `log` hem `rev-parse --git-dir` duser -> `_kapi_h9`nun
  OKUNAMADI dali kosar. Olculmus imza: kisa kokte 72 karakter (H9 satiri 98),
  uzun kokte 252 (H9 satiri 278).

  🔴 NEDEN `chown` DEGIL (19 Agu 2026, CI #80 `32236392253` ISIRDI): eski tarif
  `chown -R nobody <KOK>` idi. `chown` ile BASKA kullaniciya sahiplik devri
  POSIX'te ROOT ister; GitHub runner'i `runner` kullanicisidir, root DEGILDIR
  -> UC PLATFORMDA DA "kum havuzu kurulamadi" (exit 2). Arac DURUST davrandi;
  kusur ORTAM VARSAYIMINDAYDI. `GIT_TEST_ASSUME_DIFFERENT_OWNER` AYNI mesaji
  uretir, ROOT/sudo GEREKTIRMEZ ve DOSYA SISTEMINE DOKUNMAZ.

  🔴 KALAN ACIK RISK (gizlenmez): degisken git'in KENDI TEST kancasidir; upstream
  kaldirirsa ya da runner'da kuresel `safe.directory` onu etkisizlestirirse mesaj
  URETILMEZ. O halde bu arac SESSIZCE GECMEZ: H9 OKUNAMADI satirini bulamaz ve
  OLCULEMEDI (exit 2) doner — OLCULDU (bkz. asagidaki kuresel-ayar bagisikligi).
  Kuresel ayar bagisikligi icin `GIT_CONFIG_GLOBAL/SYSTEM=os.devnull` +
  `GIT_CONFIG_NOSYSTEM=1` de gecirilir; `safe.directory=*` tanimliyken bile
  iki kol da BEKLENDIGI GIBI olctu.

CAPA (H16-KESME-DUZELTME-BRIEF.md §5 dersi): motora KOD PARCACIGIYLA anchor
atilir, satir NUMARASIYLA DEGIL.

CIKIS KODLARI (proje sozlesmesi)
  0  iki kolun IKISI DE BEKLENDIGI GIBI (KISA icin 'beklenen' KACIStir) VE
     isaret deseni CANLI motorla eslesiyor (KALEM C, DUZELTME 4)
  1  en az bir kol BEKLENMEDIK cikti verdi
  2  OLCULEMEDI (BEKLENMEDIK yoksa) — tetikleyici mesaji uretmediyse DAHIL
  3  ARAC KUSURU (sabotaj hedefi bulunamadi, kum havuzu kurulamadi, isaret
     deseni CANLI motorun urettigiyle eslesmiyor)
"""
import ctypes
import os
import re
import shutil
import subprocess
import sys
import tempfile


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
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []          # (ad, durum, ayrinti)


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


# --------------------------------------------------------------- SABOTAJ (D2)
# KALEM 1'in TERSİ (D2): duzeltilmis motora `[:120]` kesmesini GERI enjekte
# eder. 🔴 CAPA TASINDI (Onur kilidi 5 Eylul 2026, IS_EMRI_H9_KESME_CAPA.md
# KALEM A): KALEM 1 hafiza.py'nin bu satirini `.split("\n")[0]`den
# `_ilk_satir_isaretli(...)`e degistirdi (B6 SIK beta) — eski capa metni
# ARTIK 0 kez geciyordu, sabotaj kendi muhafazasiyla ARAC KUSURU verirdi
# (Cowork bulut Linux, motor `37908e38`, OLCULDU). `_ilk_satir_isaretli(...)`
# cagrisinin KENDISI DOKUNULMAZ — yalniz kuyruktaki `[:120]` eklenir/cikarilir
# (davranis AYNI, hedef metin GUNCEL).
_DUZELTILMIS = '_sb = _ilk_satir_isaretli((r.stderr or _rg.stderr or "").strip())'
_SABOTAJLI = '_sb = _ilk_satir_isaretli((r.stderr or _rg.stderr or "").strip())[:120]'


def _sabotajli_motor(hedef_dizin):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(_DUZELTILMIS)
    if n != 1:
        raise AracKusuru(
            "sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse SABOTAJ "
            "DA DEGISMELIDIR (kalem5-tarama/IS_EMRI_SIK_A.md D2, hafiza.py "
            "_kapi_h9())." % n)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(_DUZELTILMIS, _SABOTAJLI, 1))
    return p


def _kos(motor, arglar, saniye=120, env=None):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    if env:
        o.update(env)
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.stdout


_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="h9-mut", GIT_AUTHOR_EMAIL="h9-mut@example.invalid",
    GIT_COMMITTER_NAME="h9-mut", GIT_COMMITTER_EMAIL="h9-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")


def _kok_hedef_uzunlukta(taban_dizini, hedef_uzunluk):
    """bkz. olculemedi_kesme_mutanti.py._kok_hedef_uzunlukta — AYNI mantik,
    dolgu HEX OLMAYAN ("zq" tekrari)."""
    on_ek = os.path.join(taban_dizini, "")
    gerekli = hedef_uzunluk - len(on_ek)
    if gerekli < 1:
        return None
    dolgu = ("zq" * ((gerekli // 2) + 1))[:gerekli]
    kok = on_ek + dolgu
    os.makedirs(kok, exist_ok=True)
    return kok


# 🔴 AD, YAPILAN ISI SOYLER (M-A8 dersi: adi "realpath maskesi" olup KESMEYI olcen
# bir mutant, maskeyi hic olcmedigini UC AY gizledi). Burada sahiplik DEVREDILMEZ;
# git'in sahiplik DENETIMI supheli hale getirilir. Ad da onu soyler.
_OLCUM_ORTAMI = {
    "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1",   # tetikleyici (root/sudo GEREKMEZ)
    "GIT_CONFIG_NOSYSTEM": "1",               # kuresel/sistem `safe.directory`
    "GIT_CONFIG_GLOBAL": os.devnull,          # bagisikligi — OLCULDU: `*` tanimli
    "GIT_CONFIG_SYSTEM": os.devnull,          # olsa bile iki kol da olcuyor
}


def _sahipligi_supheli_kil():
    """SIK EPSILON: dosya sistemine DOKUNMAZ, kullanici/izin DEGISTIRMEZ.
    Git'in kendi sahiplik denetimi cevre degiskeniyle tetiklenir; uretilen mesaj
    `chown` tarifiyle BIREBIR AYNIDIR (olculdu 19 Agu 2026, git 2.43.0)."""
    return dict(_OLCUM_ORTAMI)


def _kum_havuzu_kur(motor, kok):
    """Uretim tarifi (IS_EMRI_SIK_A.md §4, OLCULDU): git init+commit -> kur ->
    defterler commit'lenir -> depo BASKA kullaniciya devredilir. Motora
    DOKUNMAZ, yalniz komut satirindan cagirir."""
    os.makedirs(kok, exist_ok=True)
    _git(kok, "init", "-q")
    rc, c = _kos(motor, ["kur", "--ad", "Y4", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, c[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "taban",
        env=dict(os.environ, **_GIT_ORTAM))


def _h9_satiri(cikti):
    return next((s for s in cikti.splitlines() if "H9: git deposu OKUNAMADI" in s), None)


_H9_ONEK = "H9: git deposu OKUNAMADI: "


def _h9_mesaj_govdesi(satir):
    """H9 satirindaki, KESMENIN GERCEKTEN uygulandigi parca — `_h9_onek`den
    SONRAKI kisim (bkz. hafiza.py _kapi_h9: `[:120]` `_sb`ye uygulanir,
    "H9: git deposu OKUNAMADI: " oneki SONRADAN eklenir). `startswith`
    DEGIL `split`: basili satir "  ? " ile GIRINTILIDIR (main()'in `O`
    listesi basma bicimi), satir ONEKLE BASLAMAZ — yalniz ICERIR."""
    parca = satir.split(_H9_ONEK, 1)
    return parca[1] if len(parca) == 2 else satir


def _sabotaj_esigi():
    """`_SABOTAJLI` dizgesinden kesme esigini (bugun 120) OKUR — sabit
    YAZILMAZ, sabotaj degisirse bu da otomatik degisir (H16-KESME-DUZELTME-
    BRIEF.md §5 capa dersiyle AYNI ilke: kod parcaciginin KENDISINDEN oku,
    ayri bir sabit YAZMA)."""
    m = re.search(r"\[:(\d+)\]", _SABOTAJLI)
    if not m:
        raise AracKusuru("sabotaj esigi _SABOTAJLI dizgesinden okunamadi (desen degisti mi?)")
    return int(m.group(1))


# --------------------------------------------------------------- B6 ISARETI (KALEM B)
# (IS_EMRI_H9_KESME_CAPA.md KALEM B, Onur kilidi 5 Eylul 2026): olculemedi_
# kesme_mutanti.py._b6_isaretini_ayikla ile AYNI mantik — KENDI KOPYASI.
# Onur kilidi: motordan ya da diger mutanttan IMPORT EDILMEZ, ortak faz0
# modulu ACILMAZ (kum havuzu izolasyonu ilkesi: mutant dosyalari birbirinden
# BAGIMSIZ kalir). `_ilk_satir_isaretli` (hafiza.py) COK SATIRLI govdenin
# SONUNA " (+N satir: stderr)" ekler; bu ayiklanmadan `'` bitis sinamasi
# YAPILAMAZ (M-Y3 mayininin AYNISI, bkz. DUZELTME 4).
_B6_ISARET = r"\s*\(\+\d+ satir: stderr\)$"


def _b6_isaretini_ayikla(govde):
    """B6'nin hukum satirinin SONUNA ekledigi " (+N satir: stderr)" isaretini
    AYIKLAR (varsa). Isaret AYRI bir katmandir — kirpilma olcumu ISARETSIZ
    govde uzerinde yapilir; boylece B6 (satiri UZATAN) ile bu capa (satirin
    SONUNU olcen) birbirinin KORLUGUNU URETMEZ. `"'" in govde` YAZILMAZ:
    kok yolu govdenin ORTASINDA da tek tirnak tasiyabilir (M-Y3 §2 dersiyle
    AYNI: `in` govdede baska yerde gecen bir diziyi yakalar, mutanti SESSIZCE
    KOR yapar) — yalniz SON, regex ile ayiklanip/olculur.

    Doner: (isaretsiz_govde, isaret_ayiklandi_mi: bool)."""
    yeni, n = re.subn(_B6_ISARET, "", govde, count=1)
    return yeni, (n > 0)


def _my4_kol(taban, ad, hedef_uzunluk, beklenen_kirpilmamis):
    try:
        esik = _sabotaj_esigi()
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, str(e))
        return
    alt = os.path.join(taban, "u" if hedef_uzunluk else "k")
    os.makedirs(alt, exist_ok=True)
    if hedef_uzunluk:
        kok = _kok_hedef_uzunlukta(alt, hedef_uzunluk)
        if kok is None:
            _kayit(ad, OLCULEMEDI, "hedef uzunluk (%d) bu ortamda kurulamadi" % hedef_uzunluk)
            return
    else:
        kok = os.path.join(alt, "kk")
        os.makedirs(kok, exist_ok=True)
    try:
        _kum_havuzu_kur(MOTOR, kok)
    except AracKusuru as e:
        _kayit(ad, OLCULEMEDI, "kum havuzu kurulamadi: %s" % e)
        return
    sab_dizin = os.path.join(alt, "sab")
    os.makedirs(sab_dizin, exist_ok=True)
    motor_sab = _sabotajli_motor(sab_dizin)
    rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok],
                 env=_sahipligi_supheli_kil())
    satir = _h9_satiri(c)
    if satir is None:
        _kayit(ad, OLCULEMEDI,
              "H9 OKUNAMADI satiri bulunamadi (kok uzunlugu=%d, exit=%s) — "
              "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ olabilir "
              "(surum/platform). SESSIZ GECIS DEGIL, OLCULEMEDI. Ham cikti kuyrugu:\n%s"
              % (len(kok), rc, c[-500:]))
        return
    govde, isaret_ayiklandi = _b6_isaretini_ayikla(satir.rstrip())
    kirpilmamis = govde.endswith("'")
    dogru = (kirpilmamis == beklenen_kirpilmamis)
    _kayit(ad, BEKLENDIGI_GIBI if dogru else BEKLENMEDIK,
          "kok uzunlugu=%d | sabotajli motor ([:%d] geri) | B6 isareti ayiklandi "
          "mi=%s | isaretsiz govde kapanis tirnagi (') ile bitiyor "
          "(kirpilmamis)=%s (beklenen: %s)\n      satir: %s"
          % (len(kok), esik, "VAR" if isaret_ayiklandi else "yok",
             "VAR" if kirpilmamis else "yok",
             "VAR" if beklenen_kirpilmamis else "yok", satir.strip()))


def my4_uzun_kol(taban):
    try:
        # olculemedi_kesme_mutanti.py ile ayni ders: 200 Windows'ta MAX_PATH'e
        # carpiyordu (git commit'in .git/objects yazimi); 170 mesaj esigini
        # (>120) rahatca asiyor. Bu kol zaten POSIX-disi platformda hic
        # kosmuyor (main() basinda OLCULEMEDI), ama Linux/macOS icin de
        # tutarli tek sabit deger tercih edildi.
        _my4_kol(taban,
                "M-Y4 UZUN KOL: kok>=170, sabotajli motor H9 satirini KIRPMALI (ISIRMALI)",
                170, False)
    except AracKusuru as e:
        _kayit("M-Y4 UZUN KOL", OLCULEMEDI, str(e))


_SON_KISA_TABAN_KAYNAGI = None
# IS_EMRI_H9_KISA_TABAN_WIN.md KALEM 2: `_kisa_taban_ac_win()`nin KAZANDIGI
# adayin ETIKETINI + kok uzunlugunu buraya yazar. Salt-okunur bir yan-kanal —
# `_kisa_taban_ac()`nin DAVRANISINI ETKILEMEZ, yalniz KAYIT icin okunur
# (`_kisa_taban_kaynagi()` araciligiyla). POSIX dalina (dokunulmayan) hicbir
# YAZMA EKLENMEDI — o durumda kaynak DONEN YOLUN ONEKINDEN cikarilir.


def _win_8_3_kisa_ad(yol):
    """Windows 8.3 kisa ad (`GetShortPathNameW`) — bazi birimlerde/dizinlerde
    KAPALI olabilir (`fsutil 8dot3name`), yol MEVCUT OLMAYABILIR, ya da bu
    islev POSIX'te HIC YOK (`ctypes.windll` yalniz Windows'ta bulunur).
    Hicbir HALDE istisna DISARI SIZMAZ — basarisizlikta None doner, aday
    SESSIZCE DUSER (IS_EMRI_H9_KISA_TABAN_WIN.md KALEM 1: "cagrinin basarisiz
    olabilecegini hesaba kat")."""
    try:
        buf = ctypes.create_unicode_buffer(260)
        n = ctypes.windll.kernel32.GetShortPathNameW(yol, buf, len(buf))
        if n == 0 or n > len(buf):
            return None
        return buf.value
    except Exception:
        return None


def _win_yazilabilir_mi(dizin):
    """Aday dizinin GERCEKTEN yazilabilir olup olmadigini DENER (yaz-sil) —
    varligi/dizin olmasi YETMEZ (ornek: sistem gecici dizini yonetici
    GEREKTIREBILIR). Basarisizlikta istisna FIRLATILMAZ, False doner — aday
    sessizce DUSER, hata FIRLATILMAZ (IS_EMRI_H9_KISA_TABAN_WIN.md KALEM 1).
    Denemenin KENDISI VAR OLAN dizinin icinde bir DOSYADIR — KISIT 4 (yeni
    ust duzey dizin ACILMAZ) burada ihlal EDILMEZ: yeni dizin YOK, VAR OLAN
    dizinin icinde acilip HEMEN silinen bir dosya var."""
    try:
        fd, yol = tempfile.mkstemp(prefix=".h16km_yazilabilir_", dir=dizin)
        os.close(fd)
        os.remove(yol)
        return True
    except OSError:
        return False


def _kisa_taban_ac_win():
    """IS_EMRI_H9_KISA_TABAN_WIN.md KALEM 1 (Onur kilidi 5 Eylul 2026):
    `_kisa_taban_ac()`'in POSIX-disi (esas olarak Windows) dali icin kisa
    taban ADAYLARI CALISMA ZAMANINDA OLCULUR — hicbir aday/sira SABITLENMEZ:
      - `RUNNER_TEMP` (GitHub Actions Windows runner'i verir — VAR OLDUGU
        VARSAYILMAZ, OLCULUR)
      - `TEMP` / `TMP` — VE bunlarin 8.3 KISA ADI (`_win_8_3_kisa_ad`; cagri
        basarisiz olabilir, o zaman bu tek aday sessizce DUSER)
      - zaten VAR OLAN sistem gecici dizini (`%SystemRoot%\\Temp`) — YENI
        YARATILMAZ, yalniz ZATEN VARSA denenir (KISIT 4)
    Her aday icin: var mi -> dizin mi -> GERCEKTEN yazilabilir mi (`_win_
    yazilabilir_mi`, deneme yaz-sil) -> `tempfile.mkdtemp(dir=aday)` ile
    OLUSACAK kok KAC KARAKTER — TAHMIN EDILMEZ, GERCEKTEN acilir (rastgele
    son ek uzunlugu CPython surumune gore degisebilecegi VARSAYILMAZ).
    Kaybeden adaylarin actigi dizinler HEMEN silinir (KALEM 3: kullanicinin
    makinesinde dizin BIRAKILMAZ). Kazanan `_SON_KISA_TABAN_KAYNAGI`ya
    yazilir (KALEM 2) ve DONDURULUR.

    🔴 Hicbir aday kurulamazsa (hepsi yok/yazilamiyor/mkdtemp basarisiz)
    GENEL `tempfile.mkdtemp(prefix="h16km_")`e DUSULUR — bu durumda ON SART
    OLCUMU (my4_kisa_kol, DEGISMEDI) kok'un esigin USTUNDE oldugunu dogru
    sekilde ÖLÇÜLEMEDİ olarak raporlar; burada "basarili gibi" hicbir sey
    GOSTERILMEZ (KISIT, KALEM 1 sonu: "Ön şartı 'sağlanmış gibi' gösterecek
    hiçbir şey yapılmaz")."""
    global _SON_KISA_TABAN_KAYNAGI
    etiketli_adaylar = []
    v = os.environ.get("RUNNER_TEMP")
    if v:
        etiketli_adaylar.append(("RUNNER_TEMP", v))
    for ad in ("TEMP", "TMP"):
        v = os.environ.get(ad)
        if v:
            etiketli_adaylar.append((ad, v))
            kisa = _win_8_3_kisa_ad(v)
            if kisa and os.path.normcase(os.path.normpath(kisa)) != \
                    os.path.normcase(os.path.normpath(v)):
                etiketli_adaylar.append(("%s (8.3 kisa ad)" % ad, kisa))
    sistem_root = os.environ.get("SystemRoot") or os.environ.get("SYSTEMROOT")
    if sistem_root:
        etiketli_adaylar.append(("SystemRoot\\Temp", os.path.join(sistem_root, "Temp")))

    gorulen = set()
    kazanan = None   # (uzunluk, yol, etiket)
    for etiket, taban in etiketli_adaylar:
        anahtar = os.path.normcase(os.path.normpath(taban))
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        if not os.path.isdir(taban) or not _win_yazilabilir_mi(taban):
            continue
        try:
            yol = tempfile.mkdtemp(prefix="h16km_", dir=taban)
        except OSError:
            continue
        if kazanan is None or len(yol) < kazanan[0]:
            if kazanan is not None:
                shutil.rmtree(kazanan[1], ignore_errors=True)
            kazanan = (len(yol), yol, etiket)
        else:
            shutil.rmtree(yol, ignore_errors=True)

    if kazanan is not None:
        _SON_KISA_TABAN_KAYNAGI = "%s (kok=%d)" % (kazanan[2], kazanan[0])
        return kazanan[1]
    _SON_KISA_TABAN_KAYNAGI = "genel mkdtemp() varsayilani (hicbir aday kurulamadi)"
    return tempfile.mkdtemp(prefix="h16km_")


def _kisa_taban_ac():
    """KISA KOL icin GENEL `mkdtemp` yerine KISA bir taban acar (20 Agu 2026
    ikinci duzeltme, Onur kilidi SIK (a) — kisa tabani KUR). POSIX'te
    literal `/tmp` altinda (varsa): `tempfile.mkdtemp(dir=...)` acikca
    `dir` verilince TMPDIR/TMP/TEMP ortam degiskenlerini YOK SAYAR, bu
    yuzden disaridan enjekte edilmis UZUN bir TMPDIR (baska bir aracin
    testi, ya da enjeksiyon) KISA KOL'u ARTIK ETKILEMEZ. OLCULDU (Linux):
    dis TMPDIR 48/110/150 iken bile bu yolla kok hep ~22 karakter kaliyor.

    🔴 GARANTI DEGIL, IYILESTIRME: macOS `/tmp`yi `/private/tmp`e
    REALPATH'ler (M-A8 mayini, H16-KESME-DUZELTME-BRIEF.md) — bu TAHMIN idi
    (kok ~33, mesaj ~86, esigin altinda BEKLENIYORDU); CI #83 `32374821806`
    macos-latest'te SUCCESS ile DOGRULADI. Bu yuzden kisa taban ON SART
    OLCUMUNU GEREKSIZ KILMAZ — ölçüm hala OTORITEDIR, kisa taban yalnizca
    cogu ortamda on sartin KENDILIGINDEN saglanmasini kolaylastiran bir
    on-hazirliktir.

    🔴 POSIX-disi (esas olarak Windows) dal 5 Eylul 2026'da (IS_EMRI_H9_
    KISA_TABAN_WIN.md, EK-2) GENISLETILDI — asagidaki POSIX `if` blogu
    BAYT-BAYT DOKUNULMADI (K5), yalniz eski "GENEL varsayilana duser" satiri
    `_kisa_taban_ac_win()`'e yonlendirildi: o fonksiyon Windows'a ozgu
    adaylari (RUNNER_TEMP/TEMP/TMP/8.3/sistem gecici dizini) CALISMA
    ZAMANINDA olcup EN KISASINI secer (bkz. `_kisa_taban_ac_win` docstring'i).
    `/tmp` yoksa (POSIX-disi/Windows) artik KOR bir GENEL varsayilana degil,
    OLCULEN bu adaylara duser; hicbiri kurulamazsa GENEL varsayilana duser."""
    if os.name == "posix" and os.path.isdir("/tmp"):
        try:
            return tempfile.mkdtemp(prefix="h16km_", dir="/tmp")
        except OSError:
            pass
    return _kisa_taban_ac_win()


def _kisa_taban_kaynagi(kisa_taban):
    """KAYIT icin salt-okunur bir ETIKET (IS_EMRI_H9_KISA_TABAN_WIN.md
    KALEM 2) — `_kisa_taban_ac()`'in DAVRANISINI ETKILEMEZ. POSIX dalina
    (dokunulmayan) hicbir yazma EKLENMEDIGI icin o durumda kaynak, DONEN
    YOLUN ONEKINDEN cikarilir (`/tmp` ile basliyorsa); Windows dalinda
    `_kisa_taban_ac_win()`'in yazdigi `_SON_KISA_TABAN_KAYNAGI` OKUNUR."""
    if kisa_taban.replace("\\", "/").startswith("/tmp/"):
        return "/tmp (POSIX)"
    return _SON_KISA_TABAN_KAYNAGI or "bilinmiyor"


def my4_kisa_kol():
    """20 Agu 2026: UC duzeltme BIRLIKTE calisir.
    (1) "kisa kok" bir VARSAYIM DEGIL, bir OLCUMDUR (ilk duzeltme):
        `tempfile.mkdtemp()`nin GENEL varsayilan tabani Linux'ta ~24,
        macOS'ta ~68 karakterdir — macOS'ta mesaj (68+53=121) esigi (120)
        ASAR ve kor kol kor KALMAZ (CI 32250138848, Onur kilidi). Kolun
        KENDI ON SARTI ("kirpilmamis H9 mesaji esigin altinda mi")
        sabotajsiz/duzeltilmis motorla ONCE OLCULUR; ancak SAGLANIYORSA
        sabotaj kosulur. Saglanmiyorsa OLCULEMEDI (exit 2) doner — ASLA
        BEKLENMEDIK: bir kusur BULGUSU degil, bu ortamda olculemeyen bir
        ON SARTTIR.
    (2) Kisa taban artik AYRICA KURULUYOR (ikinci duzeltme, `_kisa_taban_ac`):
        ON SART OLCUMU DOGRUdur ama "exit 2 de sifirdan farkli" ve
        `h9_kesme_mutanti` isinde `continue-on-error` YOK — yalanci kirmizi
        DURUST kirmiziya donse de macOS KALICI KIRMIZI kalirdi. Kok'u
        `/tmp` altinda BIZ kisa kurmak (1)'i GEREKSIZ KILMAZ — (1) hala
        OTORITEDIR, (2) yalnizca cogu ortamda on sartin kendiliginden
        saglanmasini kolaylastirir. (macOS `/private/tmp` REALPATH riski
        bir TAHMINdi; CI #83 `32374821806` SUCCESS ile DOGRULADI.)
    (3) ON SART karsilastirmasinda PAY YOK (ucuncu duzeltme, CI #83 is
        `96443570144` windows-latest KIRMIZI): esikten TUREYEN bir pay
        (`esik // 10`) mesaj=112'yi esik=120'nin ALTINDAYKEN bile
        OLCULEMEDI'ye ceviriyordu — sabotaj GERCEKTE kirpmazdi. On sart
        GURULTUSUZ oldugu icin (sabotajin AYNI kokte AYNI mesaji, tek
        fark kesmenin kendisi) pay hicbir seyi korumuyordu; simdi
        `mesaj_uzunlugu > esik` FIZIGIN KENDISI.
    (4) 5 Eylul 2026 (IS_EMRI_H9_KESME_CAPA.md KALEM B/D): `mesaj_uzunlugu`
        ARTIK B6'nin isaretini (" (+N satir: stderr)", 19 karakter) DE
        SAYAR — `_h9_mesaj_govdesi(satir0)` govdeyi isaretiyle BIRLIKTE
        oker, formul (2)'deki gibi DEGISMEDI; yalniz kritik kok uzunlugu bu
        19 karakter kadar ASAGI kaydi (kalem5-tarama/OLCUM_RAPORU_H9_KESME_
        CAPA.md'de OLCULDU, buraya SAYI YAZILMAZ). KEHANET sinamasi da
        ARTIK isareti `_b6_isaretini_ayikla()` ile AYIKLAYIP govde uzerinde
        `'` bitisine bakar (asagida) — DUZELTME 4/KALEM B, M-Y3 ile AYNI
        mayinin AYNI dersi."""
    ad = "M-Y4 KISA KOL (KOR KOL): kisa kokte AYNI sabotaj GORUNMEZ KALMALI (KACMASI BEKLENEN)"
    try:
        kisa_taban = _kisa_taban_ac()
    except OSError as e:
        _kayit(ad, OLCULEMEDI, "kisa taban acilamadi: %s" % e)
        return
    # KALEM 2 (IS_EMRI_H9_KISA_TABAN_WIN.md): hangi adayin kazandigi + kok
    # uzunlugu — bir sonraki tur bunu KODU OKUMADAN, CIKTIDAN okuyabilsin.
    kisa_taban_kaynagi = _kisa_taban_kaynagi(kisa_taban)
    try:
        alt = os.path.join(kisa_taban, "k")
        os.makedirs(alt, exist_ok=True)
        kok = os.path.join(alt, "kk")
        os.makedirs(kok, exist_ok=True)
        try:
            esik = _sabotaj_esigi()
            _kum_havuzu_kur(MOTOR, kok)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "on sart hazirlanamadi (kisa taban kaynagi=%s): %s"
                  % (kisa_taban_kaynagi, e))
            return

        # --- ON SART OLCUMU: duzeltilmis (sabotajsiz) motorla BIR KEZ kos -----
        env = _sahipligi_supheli_kil()
        rc0, c0 = _kos(MOTOR, ["kapi", "--kok=" + kok], env=env)
        satir0 = _h9_satiri(c0)
        if satir0 is None:
            _kayit(ad, OLCULEMEDI,
                  "on sart OLCULEMEDI: duzeltilmis motorla H9 OKUNAMADI satiri "
                  "bulunamadi (kok uzunlugu=%d, exit=%s) — "
                  "GIT_TEST_ASSUME_DIFFERENT_OWNER bu git yapisinda ETKISIZ olabilir "
                  "(surum/platform). Ham cikti kuyrugu:\n%s" % (len(kok), rc0, c0[-500:]))
            return
        mesaj_uzunlugu = len(_h9_mesaj_govdesi(satir0))
        # DUZELTME 3 (20 Agu 2026, CI #83): PAY YOK — on sart GURULTUSUZ
        # (sabotajin kullanacagi AYNI kokte AYNI mesaji olcer, TEK degisken
        # kesmenin kendisi), bu yuzden karsilastirma DOGRUDAN fizikle AYNI:
        # sabotaj `[:esik]` KIRPAR ancak mesaj esigi ASARSA. Bir PAY EKLEMEK
        # yalniz yalanci-kirmizi uretir (Windows CI #83, mesaj=112<esik=120
        # gercekte kirpilmazdi) — pay BURAYA GERI EKLENMEZ.
        if mesaj_uzunlugu > esik:
            _kayit(ad, OLCULEMEDI,
                  "ON SART SAGLANMIYOR (bu ortamda kisa kol OLCULEMEZ — kusur "
                  "BULGUSU DEGIL): kirpilmamis H9 mesaj uzunlugu=%d > esik=%d. "
                  "kisa taban kaynagi=%s | kok uzunlugu=%d, kok=%s\n"
                  "      ham (sabotajsiz) satir: %s"
                  % (mesaj_uzunlugu, esik, kisa_taban_kaynagi, len(kok), kok,
                     satir0.strip()))
            return

        # --- ON SART SAGLANDI: simdi sabotaji kos, KEHANETI sina --------------
        sab_dizin = os.path.join(alt, "sab")
        os.makedirs(sab_dizin, exist_ok=True)
        try:
            motor_sab = _sabotajli_motor(sab_dizin)
        except AracKusuru as e:
            _kayit(ad, OLCULEMEDI, "sabotajli motor kurulamadi: %s" % e)
            return
        rc, c = _kos(motor_sab, ["kapi", "--kok=" + kok], env=env)
        satir = _h9_satiri(c)
        if satir is None:
            _kayit(ad, OLCULEMEDI,
                  "sabotajli kosumda H9 OKUNAMADI satiri bulunamadi (kok uzunlugu=%d, "
                  "exit=%s) — on sart olcumunde VARDI, sabotajli kosumda YOK: "
                  "tutarsizlik. Ham cikti kuyrugu:\n%s" % (len(kok), rc, c[-500:]))
            return
        govde, isaret_ayiklandi = _b6_isaretini_ayikla(satir.rstrip())
        kirpilmamis = govde.endswith("'")
        _kayit(ad, BEKLENDIGI_GIBI if kirpilmamis else BEKLENMEDIK,
              "kisa taban=%s | kisa taban kaynagi=%s | ON SART OLCULDU: "
              "kirpilmamis mesaj uzunlugu=%d (esik=%d) | sabotajli motor "
              "([:%d] geri) | B6 isareti ayiklandi mi=%s | isaretsiz govde "
              "kapanis tirnagi (') ile bitiyor (kirpilmamis)=%s "
              "(beklenen: VAR)\n      kok uzunlugu=%d, kok=%s"
              % (kisa_taban, kisa_taban_kaynagi, mesaj_uzunlugu, esik, esik,
                 "VAR" if isaret_ayiklandi else "yok",
                 "VAR" if kirpilmamis else "yok", len(kok), kok))
    finally:
        shutil.rmtree(kisa_taban, ignore_errors=True)


# --------------------------------------------------------------- KALEM C: CANLI DOGRULAMA
def _isaret_deseni_canli_dogrula(taban):
    """KALEM C (IS_EMRI_H9_KESME_CAPA.md, Onur kilidi 5 Eylul 2026): isaret
    deseni (`_B6_ISARET`) artik IKI mutant dosyasinda (bu dosya ve
    olculemedi_kesme_mutanti.py) AYRI AYRI yazili — biri guncellenip digeri
    unutulursa SESSIZ KORLUK dogar (biçim degisirse hangi kollar AYNI ANDA
    duser: KISA KOL, UZUN KOL ve M-Y3'un uc kolunun TAMAMI). Kum havuzu
    PAYLASILMAZ ilkesine uyup KENDI izole kokunde CANLI, duzeltilmis
    (sabotajsiz) motoru kosturur ve deseni SABIT bir dizgeye degil, motorun
    GERCEKTEN urettigi bir H9 satirina karsi sinar.

    - Kum havuzu kurulamazsa / H9 satiri HIC uretilmezse (dubious-ownership
      bu git yapisinda/platformda tetiklenmedi): SESSIZCE GECER, SONUC'a
      KAYIT ACMAZ — ayni ortam sinirlamasi zaten my4_uzun_kol/my4_kisa_kol
      TARAFINDAN KENDI OLCULEMEDI kayitlarinda raporlanir; burada TEKRAR
      raporlamak K1'in "2/2 kol" sayimini ANLAMSIZCA sisirir (bu fonksiyon
      bir KOL DEGIL, bir KAPIDIR).
    - H9 satiri URETILDI (yani dubious-ownership vakasi GERCEKTEN tetiklendi)
      ama isaret YOKSA: git'in dubious-ownership stderr'i OLCULEN (dosya
      basi URETIM TARIFI) HER ZAMAN COK SATIRLIDIR (4 satir) — duzeltilmis
      motorda `_ilk_satir_isaretli` govdeye isareti EKLEMIS OLMALIYDI.
      Eklemediyse desen/motor UYUSMUYOR demektir (kopya BAYATLADI) —
      `AracKusuru` FIRLATILIR (main()'in ustteki try/except'i yakalar,
      exit 3): sessizce "isaret yok" SAYILMAZ (K5 kehaneti: deseni kasten
      boz, kos, ARAC KUSURU gor)."""
    alt = os.path.join(taban, "k4")
    os.makedirs(alt, exist_ok=True)
    kok = os.path.join(alt, "kk")
    os.makedirs(kok, exist_ok=True)
    try:
        _kum_havuzu_kur(MOTOR, kok)
    except AracKusuru:
        return   # ortam kum havuzu kuramadi — my4_uzun_kol/my4_kisa_kol AYNI
                 # sinirlamayi KENDI kollarinda OLCULEMEDI olarak raporlar.
    rc, c = _kos(MOTOR, ["kapi", "--kok=" + kok], env=_sahipligi_supheli_kil())
    satir = _h9_satiri(c)
    if satir is None:
        return   # GIT_TEST_ASSUME_DIFFERENT_OWNER ETKISIZ (surum/platform) —
                 # ayni sinirlama my4_uzun_kol/my4_kisa_kol'da AYRICA OLCULUR.
    govde = _h9_mesaj_govdesi(satir)
    _, isaret_var = _b6_isaretini_ayikla(govde.rstrip())
    if not isaret_var:
        raise AracKusuru(
            "isaret deseni (_B6_ISARET) CANLI motorun urettigi H9 satiriyla "
            "eslesmedi — 'H9: git deposu OKUNAMADI' vakasinin stderr'i bu git "
            "surumunde/platformda TEK SATIRA mi dustu, yoksa _ilk_satir_isaretli "
            "isaretin BICIMINI mi degistirdi? Desen (bu dosyada VE olculemedi_"
            "kesme_mutanti.py'de AYRI yazili) GUNCELLENMELI. Ham satir: %s"
            % satir.strip())


def main():
    print("=" * 82)
    print("H9 KESME MUTANTI (M-Y4) — _kapi_h9 OKUNAMADI hukmu kirpilmadan mi basiyor?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="h16km_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        try:
            # KALEM C (IS_EMRI_H9_KESME_CAPA.md): isaret deseni CANLI motora
            # karsi ONCE dogrulanir — desen bayatsa asagidaki iki kol da
            # YANLIS (BEKLENDIGI-GIBI/BEKLENMEDIK degil, cop) sonuc uretebilir;
            # erken ARAC KUSURU bunu SESSIZCE gecirmez.
            _isaret_deseni_canli_dogrula(taban)
            my4_uzun_kol(taban)
            my4_kisa_kol()
        except AracKusuru as e:
            print("\nARAC KUSURU: %s" % e)
            return 3
        print()
        for ad, durum, ayrinti in SONUC:
            print("  %-16s %s" % (durum, ad))
            print("  %-16s   %s" % ("", ayrinti))
        print(CIZGI)
        beklenmedik = sum(1 for _, d, _ in SONUC if d == BEKLENMEDIK)
        olculemedi = sum(1 for _, d, _ in SONUC if d == OLCULEMEDI)
        gibi = len(SONUC) - beklenmedik - olculemedi
        print("SONUC: %d/%d kol BEKLENDIGI GIBI - %d beklenmedik - %d olculemedi"
              % (gibi, len(SONUC), beklenmedik, olculemedi))
        if beklenmedik:
            return 1
        if olculemedi:
            return 2
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

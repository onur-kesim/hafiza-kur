#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — GORUNURLUK MUTANTI (dort kapi + bes mutant) — BITTI md.9.

NEDEN VAR (kaynak: md9-BRIEF.md, olculdu 16 Agu 2026, yedi gercek/sentetik
agac, salt okuma, cikis 2 / diske sifir bayt): `devral` `canli` bulamayip
DURDUGUNDA motor TANIDIGI dosyalari envantere ADIYLA basiyor, sonra AYNI
ekranda `canli=<dosya>` YER TUTUCUSU birakiyordu — bildigi seyi hukmune
KOYMUYORDU (trpc'de yedi `.cursor/rules/*.mdc` boyle basildi, hepsi
`kural_evi`). Dahasi CIFT DEFTERI onlemek icin DURMUS arac, taninmis
dosyalar ekranda dururken 2. SIRADA ikinci defter acmayi ONERIYORDU — mesru
olmayan bir yolu ONCE gosteriyordu.

TASLAK OLCUT DORDUNCU KEZ ISIRDI: "taninan dosya varsa adlarini komutta
bas" `memory-bank/` agacinda OLCULDU ve DELIKTI — alti dosyanin ALTISI da
TANINIYOR (`disarida` rolunde), o olcut durgun `projectbrief.md`'yi (22
depoda ort. 1.868 B durgun tanitim metni) "canli defter" diye ONERIRDI ve
16 Agu kapsam kararini (`MEMORY-BANK/*` -> `disarida` KALIR) DELERDI.
⇒ md.9: aday listesi KAPSAM ICI rollerle sinirlanir (`disarida` DISI);
kapsam disi birakilanlarin SAYISI aciklakca yazilir (sessiz kirpma yasak,
doktrin 2: olculemeyene/atlanana "temiz" denmez).

NE OLCER — DORT KAPI, HER BIRININ KENDI CERRAHI MUTANTI (Onur kilidi 16 Agu)
  Gerekce (DURUM.md dersi): "ortusen tespit korlugu maskeler" — iki kapi
  ayni mutanti yakaliyorsa mutant ikisini de olcuyor sanilir, oysa birini
  hic olcmuyor olabilir. Senaryolar TEK DEGISKENLE ayrisir, hepsi git
  init'li, hepsinde README.md:
    s_ici   : CLAUDE.md + DURUM.md    -> 2 kapsam ici (kural_evi + gunluk)
    s_disi  : memory-bank/ (6 dosya)  -> 6 disarida, kapsam ici YOK
    s_karma : ikisi birden            -> 1 kapsam ici + 6 kapsam disi

  KAPI-1 AD      (s_ici)  : GERCEK dosya adiyla (canli=CLAUDE.md VE
                             canli=DURUM.md) kilitleme komutu basilir;
                             `canli=<dosya>` YER TUTUCUSU hic gecmez.
  KAPI-2 SIRA    (s_ici)  : "Gercekten YENI defter ac" secenegi, SON gercek
                             (yer tutucusuz) kilitleme komutundan SONRA
                             gelir. Secenegin hic olmamasi da KIRMIZI (mesru
                             yol gizlenmez); gercek kilitleme komutu hic
                             yoksa (md.9 ONCESI hal) da KIRMIZI.
  KAPI-3 KAPSAM  (s_disi) : (i) `canli=memory-bank/...` hic gecmez,
                             (ii) "gercek defteri OLABILIR" hic gecmez.
  KAPI-4 KIRPMA  (s_karma): `canli=CLAUDE.md` GECER VE kapsam disi sayi (6)
                             + "listelenmedi" hukumde gecer (sessiz kirpma
                             yasak).

  Arac, "beklenen kapi yanmadiysa" bunu ayrica kirmizi sayar — mutant baska
  bir seyi olcuyorsa o kapi hala kor olabilir. M-1 ve M-3'un YAN ETKIYLE
  baska kapilari da yakmasi KABUL EDILIR, cunku o kapilarin kendi cerrahi
  isirganlari ayrica vardir.

NE OLCMEZ (SINIR — gizlenmez)
  1. Onerilen adayin DOGRU aday oldugu olculmez (trpc'deki yedi `.mdc`den
     hangisinin canli defter olmasi GEREKTIGI acilmadi — brief §10.3).
  2. `.hafizarc` kayitli KURULU proje hali (`--kesif` teshis yolu) bu
     kapilarin disinda; bu kapilar devir HENUZ YAPILMAMIS agac olcer.
  3. Devralma SONRASI kapi/isir hukmu olculmez (ayri eksen, ayri arac).

ZORUNLU OLCUM MEKANIGI (md.8'in bedeli odenmis iki dersi, hukum_ayrimi_mutanti.py)
  1. stdout/stderr AYRI yakalanir — stderr=subprocess.STDOUT YASAK (CI #61/62).
  2. Yol maskelemesi DESENLE yapilir (esitlik degil), maskelemenin
     GERCEKLESTIGI ayrica dogrulanir (`<KOK>` yoksa karsilastirma guvenilmez
     -> o KAPI kirmizi sayilir).
  3. KAPI-2 SATIR SIRASINI olctugu icin `re.sub(r"\\s+", " ", blok)` YAPILMAZ.
  4. Kapi, md.9 ONCESI motorda KIRMIZI yanmalidir — ELDE OLCULDU: dort
     kapinin dordu de o motora karsi kirmizi yandi (bu dosyanin CI'daki
     ilk kosumu DEGIL, gelistirme sirasindaki elle dogrulama).
  5. git yoksa / motor okunamazsa / mutant kurulamazsa OLCULEMEDI (cikis 2),
     sessiz PASS yok.

CIKIS KODLARI
  0  dort kapi da temiz VE 5/5 mutant ISIRDI
  1  bir kapi kirmizi ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi, git yok) — sessiz PASS yok
"""
import io
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
            pass


VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")

MB_DOSYALARI = ("activeContext.md", "productContext.md", "progress.md",
                "projectbrief.md", "systemPatterns.md", "techContext.md")


def _git_var():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except OSError:
        return False


def kur_senaryo(taban, ad, claude=False, durum=False, mb=False):
    """s_ici / s_disi / s_karma — TEK DEGISKEN: hangi dosyalar var. Hepsi
    ayni README.md'yi tasir, boylece fark BASKA bir seyden gelemez."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    subprocess.run(["git", "init", "-q", "."], cwd=kok,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with io.open(os.path.join(kok, "README.md"), "w", encoding="utf-8") as f:
        f.write("# proje\n")
    if claude:
        with io.open(os.path.join(kok, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write("# claude\n")
    if durum:
        with io.open(os.path.join(kok, "DURUM.md"), "w", encoding="utf-8") as f:
            f.write("# durum\n")
    if mb:
        d = os.path.join(kok, "memory-bank")
        os.makedirs(d)
        for x in MB_DOSYALARI:
            with io.open(os.path.join(d, x), "w", encoding="utf-8") as f:
                f.write("# %s\n" % x)
    return kok


def kos(motor, kok):
    """stdout ve stderr AYRI yakalanir — BIRLESTIRILMEZ.

    Ayni sinif hukum_ayrimi_mutanti.py'de CI #61/#62'yi uretti: `oldur()`
    stderr'e tamponsuz, envanter `print()` ile stdout'a boru arkasinda blok
    tamponlu yazar; birlestirmek iki blogu senaryoya gore FARKLI karistirir
    ve kapi KOR olur."""
    p = subprocess.run([sys.executable, motor, "devral", "--kok=" + kok],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def durma_blogu(hata, kok):
    """Hukum blogu = ilk `HATA:` satirindan sonu. Yol DESENLE maskelenir.

    md.8'in bedeli odenmis dersi: esitlik tabanli maskeleme motorun
    abspath'inin bir karakter kaymasiyla sessizce basarisiz olabilir.
    Desenle sil; maskelemenin GERCEKLESTIGI CAGIRAN tarafindan ayrica
    dogrulanir (`_maskelendi_mi`).
    KAPI-2 SATIR SIRASINI olctugu icin whitespace NORMALIZE EDILMEZ — satir
    yapisi bozulursa sira hic olculemez."""
    i = hata.find("HATA:")
    if i < 0:
        return None
    blok = hata[i:]
    blok = re.sub(r'--kok="[^"]*"', '--kok="<KOK>"', blok)
    return blok.replace(kok, "<KOK>").replace(kok.replace(os.sep, "/"), "<KOK>")


def _maskelendi_mi(blok):
    return "<KOK>" in blok


def diske_yazildi_mi(kok):
    for x in (".hafizarc", "PROJE_HAFIZA.md", "arsiv"):
        if os.path.exists(os.path.join(kok, x)):
            return x
    return None


def _durdu_ve_blok(motor, kok):
    """Ortak on-kosum: DURDU mu, diske yazdi mi, blok MASKELENDI mi?
    Donen (b, blok): `blok` None ise cagiran kapi hemen `return b` etmeli."""
    b = []
    kod, _std, hata = kos(motor, kok)
    if kod == 0:
        return (["cikis 0 — durma kurali hic ateslenmedi"], None)
    yazildi = diske_yazildi_mi(kok)
    if yazildi:
        b.append("DURDU ama diske yazdi (%s)" % yazildi)
    blok = durma_blogu(hata, kok)
    if blok is None:
        return (b + ["cikis %d ama `HATA:` blogu YOK" % kod], None)
    if not _maskelendi_mi(blok):
        return (b + ["yol MASKELENEMEDI — karsilastirma guvenilmez, kapi kor kalirdi"], None)
    return (b, blok)


def kapi_1_ad(motor, taban):
    """AD: s_ici'de canli=CLAUDE.md VE canli=DURUM.md gecer; yer tutucu gecmez."""
    kok = kur_senaryo(taban, "s_ici", claude=True, durum=True)
    b, blok = _durdu_ve_blok(motor, kok)
    if blok is None:
        return b
    if "canli=CLAUDE.md" not in blok:
        b.append("canli=CLAUDE.md hukumde YOK")
    if "canli=DURUM.md" not in blok:
        b.append("canli=DURUM.md hukumde YOK")
    if "canli=<dosya>" in blok:
        b.append("canli=<dosya> YER TUTUCUSU hala geciyor")
    return b


def kapi_2_sira(motor, taban):
    """SIRA: s_ici'de 'Gercekten YENI defter ac' SON gercek kilitleme
    komutundan SONRA gelir; secenegin hic olmamasi da KIRMIZI."""
    kok = kur_senaryo(taban, "s_ici", claude=True, durum=True)
    b, blok = _durdu_ve_blok(motor, kok)
    if blok is None:
        return b
    satirlar = blok.split("\n")
    kilit_i = [i for i, s in enumerate(satirlar)
               if "Var olan defteri KILITLE" in s and "canli=<dosya>" not in s]
    yeni_i = [i for i, s in enumerate(satirlar) if "Gercekten YENI defter" in s]
    if not yeni_i:
        b.append("'Gercekten YENI defter ac' secenegi HIC YOK — mesru yol gizlendi")
    elif not kilit_i:
        b.append("GERCEK (dosya adli) kilitleme komutu YOK")
    elif yeni_i[0] < max(kilit_i):
        b.append("'Gercekten YENI defter ac', SON gercek kilitleme komutundan ONCE")
    return b


def kapi_3_kapsam(motor, taban):
    """KAPSAM: s_disi'de hicbir `disarida` dosyasi komutla ONERILMEZ."""
    kok = kur_senaryo(taban, "s_disi", mb=True)
    b, blok = _durdu_ve_blok(motor, kok)
    if blok is None:
        return b
    if "canli=memory-bank/" in blok:
        b.append("canli=memory-bank/... KOMUTLA ONERILDI (kapsam disi aday oldu)")
    if "gercek defteri OLABILIR" in blok:
        b.append("\"...gercek defteri OLABILIR\" cumlesi GECTI (kapsam disi icin celiskili)")
    return b


def kapi_4_kirpma(motor, taban):
    """KIRPMA: s_karma'da canli=CLAUDE.md GECER ve kapsam disi SAYI (6) +
    'listelenmedi' SESSIZCE KIRPILMAZ."""
    kok = kur_senaryo(taban, "s_karma", claude=True, mb=True)
    b, blok = _durdu_ve_blok(motor, kok)
    if blok is None:
        return b
    if "canli=CLAUDE.md" not in blok:
        b.append("canli=CLAUDE.md hukumde YOK")
    if "6" not in blok or "listelenmedi" not in blok:
        b.append("kapsam disi SAYI (6) + 'listelenmedi' YOK — SESSIZ KIRPMA")
    return b


KAPILAR = (
    ("KAPI-1 AD", kapi_1_ad),
    ("KAPI-2 SIRA", kapi_2_sira),
    ("KAPI-3 KAPSAM", kapi_3_kapsam),
    ("KAPI-4 KIRPMA", kapi_4_kirpma),
)


def hukum(motor, taban_ust):
    """Her kapi KENDI izole senaryo agacinda kosar (taban_ust altinda ayri
    alt dizinler) — birinin diske yazdigi bir sey digerini kirletmesin."""
    sonuc = {}
    for ad, fn in KAPILAR:
        alt = os.path.join(taban_ust, ad.split()[0].lower().replace("-", "_"))
        os.makedirs(alt, exist_ok=True)
        sonuc[ad] = fn(motor, alt)
    return sonuc


# --------------------------------------------------------------- MUTANTLAR
# Motorun KAYNAGINDA str.replace; her biri `_tek_yerde` ile doGrulanir.
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n"
                         % (n, hedef[:70]))
        return False
    return True


def m1_yer_tutucu_geri_gelir(s):
    """M-1: aday komutlarinda GERCEK dosya adi yerine `<dosya>` yer tutucusu
    yazilir — md.9 ONCESI halin ta kendisi. KAPI-1'i isirmali."""
    hedef = ('    secenek = [("Var olan defteri KILITLE : python hafiza.py devral "\n'
             '                "--esle canli=%s --kok=\\"%s\\"" % (e[0], kok)) for e in ici]\n')
    yeni = ('    secenek = [("Var olan defteri KILITLE : python hafiza.py devral "\n'
            '                "--esle canli=<dosya> --kok=\\"%s\\"" % (kok,)) for e in ici]\n')
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m2_yeni_defter_basa_alinir(s):
    """M-2: "YENI defter ac" satiri secenek listesinin BASINA alinir —
    taninmis dosyalar ekranda dururken ikinci defteri ilk siraya cikarir.
    KAPI-2'yi isirmali."""
    hedef = '    secenek.append("Gercekten YENI defter ac : python hafiza.py devral "\n'
    yeni = '    secenek.insert(0, "Gercekten YENI defter ac : python hafiza.py devral "\n'
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m3_disarida_filtresi_kalkar(s):
    """M-3: `disarida` filtresi kaldirilir — kapsam disi dosyalar da
    komutla onerilen aday olur. KAPI-3'u isirmali."""
    hedef = '    ici = [e for e in envanter if e[1] not in DEVIR_KAPSAM_DISI_ROLLER]\n'
    yeni = '    ici = [e for e in envanter]  # MUTANT: disarida filtresi kaldirildi\n'
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m4_ucuncu_dal_olu_kod_olur(s):
    """M-4: `_md8_ayrim`in ucuncu dali (hepsi `disarida`) OLU KOD olur —
    envanter varsa hep "biri gercek defteri OLABILIR" cumlesi doner, kapsam
    disi-yalniz halde bile. KAPI-3'u isirmali."""
    hedef = '                  if ici else\n'
    yeni = '                  if True else\n'
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m5_kirpma_satiri_susturulur(s):
    """M-5: kapsam disi sayi satiri SESSIZCE bastirilir. KAPI-4'u isirmali."""
    hedef = ('    if ici and disi:                 '
             '# md.9-c: SESSIZ KIRPMA YASAK — sayi yazilir\n')
    yeni = '    if False:                 # MUTANT: kapsam disi sayi satiri susturuldu\n'
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


MUTANTLAR = [
    ("M-1 yer tutucu geri gelir", m1_yer_tutucu_geri_gelir, "KAPI-1 AD"),
    ("M-2 YENI defter basa alinir", m2_yeni_defter_basa_alinir, "KAPI-2 SIRA"),
    ("M-3 disarida filtresi kalkar", m3_disarida_filtresi_kalkar, "KAPI-3 KAPSAM"),
    ("M-4 ucuncu dal olu kod olur", m4_ucuncu_dal_olu_kod_olur, "KAPI-3 KAPSAM"),
    ("M-5 kirpma satiri susturulur", m5_kirpma_satiri_susturulur, "KAPI-4 KIRPMA"),
]


def main():
    _cikti_kodlamasini_guvenceye_al()
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    yol = os.path.abspath(yol)
    print("=== GORUNURLUK MUTANTI (4 kapi + 5 mutant) === motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    if not _git_var():
        print("SONUC: OLCULEMEDI — `git` yok; senaryolar git'li agac ister.")
        return 2
    try:
        kaynak = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    taban = tempfile.mkdtemp(prefix="md9_temiz_")
    try:
        temiz = hukum(yol, taban)
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    kirmizi_kapi = 0
    for ad, _fn in KAPILAR:
        b = temiz[ad]
        if b:
            kirmizi_kapi += 1
            print("  %-15s: KIRMIZI" % ad)
            for x in b:
                print("      - %s" % x)
        else:
            print("  %-15s: YESIL" % ad)

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    olculemeyen = 0
    for ad, fn, beklenen_kapi in MUTANTLAR:
        bozuk = fn(kaynak)
        if bozuk is None or bozuk == kaynak:
            print("  %-32s -> OLCULEMEDI (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        d = tempfile.mkdtemp(prefix="md9_mut_")
        try:
            sahte = os.path.join(d, "hafiza.py")
            with io.open(sahte, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            t2 = os.path.join(d, "senaryolar")
            sonuc = hukum(sahte, t2)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        # "beklenen kapi yanmadiysa" AYRICA kirmizi: baska bir kapiyi
        # yakalamis olmasi (yan etki) beklenen kapinin ISIRDIGI anlamina
        # gelmez — mutant kendi hedef kapisini kacirmis olabilir.
        yan_etki = sorted(k for k, b in sonuc.items() if b and k != beklenen_kapi)
        if sonuc[beklenen_kapi]:
            ek = ("  (yan etki: %s de yandi — kabul)" % ", ".join(yan_etki)) if yan_etki else ""
            print("  %-32s -> ISIRDI (%s)%s" % (ad, beklenen_kapi, ek))
        else:
            ek = ("  (baska kapi(lar) yandi ama bu KAPIYI olcmuyor: %s)"
                  % ", ".join(yan_etki)) if yan_etki else ""
            print("  %-32s -> KACTI — beklenen kapi (%s) YANMADI%s"
                  % (ad, beklenen_kapi, ek))
            kacan += 1

    if olculemeyen:
        print("\nSONUC: OLCULEMEDI — %d mutant kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    if kirmizi_kapi or kacan:
        print("\nSONUC: KIRMIZI — kirmizi kapi %d/4 · kacan mutant %d/%d"
              % (kirmizi_kapi, kacan, len(MUTANTLAR)))
        return 1
    print("\nSONUC: YESIL — 4/4 kapi temiz, %d/%d mutant ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

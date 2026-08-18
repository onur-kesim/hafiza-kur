#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALTIN KUME GENISLEMESI MUTANTI — HATA ve KESILME kayitlari ISIRIYOR MU?

NEDEN BU DOSYA VAR
  Faz C `_kapi_govde`'yi 16 kapi fonksiyonuna boldu ve bir kusur URETTI: kapilar
  hukum listesini DONDURUNCE, bir kapi yarida SystemExit atarsa o ana kadarki
  bulgu KAYBOLUYORDU. Hukum FAIL(2 bulgu)/exit 1 iken FAIL(1 bulgu)/exit 3'e
  dondu — yani "olculmus bir kirmizi" "hukum yok"a donustu.

  UC ESDEGERLIK AYAGI DA BUNU GORMEDI. Sebep olculdu: altin kumenin 10 olcumunun
  10'u exit 0'di. Kanit YALNIZ YESIL YOLU kapsiyordu. Bir esdegerlik kumesinde
  BASARISIZLIK ve KESILME halleri yoksa o kume KORDUR.

  Kume alti hal ile genisletildi (11 hal x 2 komut = 22 olcum). DOKTRIN 1
  aciktir: "olculmeyen kapinin hukmu YOKTUR" — kayitlarin ISIRDIGI
  KANITLANMALIDIR. Bu dosya onu YARISTIRARAK olcer:

      ESKI KUME (yalniz 5 yesil hal)  -> kusur ENJEKTE EDILINCE de FARK YOK  (KOR)
      YENI KUME (11 hal)              -> FARK VAR + EXIT DEGISTI 1 -> 3      (ISIRDI)

  Ikisi AYNI hukmu veriyorsa genisleme KORDUR ve mutant KACTI der.

  ESKI KUME AYRI BIR DOSYADAN OKUNMAZ: yeni kumeden 5 yesil hal SUZULEREK
  uretilir. Boylece "genislemeden ONCEKI kume bunu gorur muydu?" sorusu, bayat
  bir dosyaya degil AYNI KOSUMA dayanir.

ORTAM URETIMI — referans KOSUM ANINDA temiz motordan alinir
  Bu mutant commit'li `altin_kapi.json`'a BAKMAZ. Referansi kosum aninda temiz
  motordan uretir, sonra kusuru enjekte eder. Sebep: bayat bir referans bu
  mutanti SAHTE KIRMIZI yakar ve mutant kendi olcecegi seyi olcemez.
  (fazC_bolme_mutanti.py ile ayni ev usulu.)

  🔴 ENJEKSIYON URUNUN GERCEK BIR SURUMU DEGILDIR. Burada olculen sey "motor bu
  kusuru tasiyor mu" DEGIL, "kume bu SINIFI gorur mu"dur. Motorun kendi hukmunu
  `--karsilastir` CI isi olcer; bu dosya onun YERINE GECMEZ.

ALTI MUTANT — her biri AYRI bir korumayi olcer
  M-B1 KAPSAM AYRISMASI : kusur enjekte edilince ESKI kapsam FARK YOK der AMA
                          YENI kapsam FARK VAR der. Iki sart BIRLIKTE arandi —
                          yalniz birincisi arandiginda kol KOSULSUZ yesil
                          veriyordu (bagimsiz denetci curuttu, olculdu).
  M-B2 YENI KUME ISIRIR : ayni kusurda YENI kume FARK VAR der ve EXIT DEGISTI
                          1 -> 3'u karisik hallerde ADLANDIRIR.
  M-B3 YANLIS POZITIF   : temiz motor + YENI kume -> FARK YOK. Genisleme kumeye
                          kararsizlik (flaky kayit) sokmuyor.
  M-B4 KESILME METNI    : "HUKUM YOK" satiri silinirse YENI kume gorur, ESKI
                          kume gormez. Saf kesilme hallerini (h7/h8/h9) olcer.
  M-B5 OLCUM KAYBOLDU   : bir hal HALLER'den DUSURULURSE karsilastirma bunu
                          KAYIP diye ilan eder, sessizce atlamaz (ADDITIVE kilidi).
  M-B6 ILAN EDILEN KESME: 12 satirdan uzun fark listesinde "N SATIR FARKI DAHA
                          GIZLENDI" satiri basilir. Sessiz kap yok.

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
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")

# Genislemeden ONCEKI hal kumesi. Bu liste DEGISMEZ: "eski kume neyi gorurdu"
# sorusunun anlami, o gunku kapsamdir.
ESKI_HALLER = ("h1_taze", "h2_fragman", "h3_derlenmis", "h4_kararli", "h5_gitli")

ISIRDI = "ISIRDI"
KACTI = "KACTI"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []


class AracKusuru(Exception):
    pass


def _degistir(metin, eski, yeni, etiket):
    """Tek eslesme + SATIR SINIRI guvencesi (fazA/fazB/fazC ile ayni ev usulu:
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


# ------------------------------------------------- MOTORA ENJEKTE EDILEN KUSURLAR

def yama_kismi_cikti_dusur(m):
    """FAZ C KUSURUNUN TAM SEKLI: kapi yarida kesilince o ana kadarki bulgu
    silinir. Sonuc: FAIL(2)/exit 1 -> FAIL(1)/exit 3. Tek satirlik enjeksiyon,
    cunku kusur de tek satirlik bir garanti kaybiydi."""
    # H16-KESME-DUZELTME-BRIEF.md KALEM 1 (18 Agu 2026, hafiza.py:3326):
    # `kesildi[:160]` -> `kesildi` (kesme kaldirildi). Hedef dize O DEGISIKLIGE
    # gore GUNCELLENDI — bu mutantin OLCTUGU sey (kismi cikti/`del F[:]`)
    # kesmeyle ILGISIZ, yalniz ANKOR satiri kaynakla birebir eslesmeli.
    return _degistir(
        m,
        '        F.append("[KAPI] OLCUM YARIDA KESILDI: %s" % kesildi)\n',
        '        del F[:]   # MUTANT: KISMI CIKTI GARANTISI DUSURULDU\n'
        '        F.append("[KAPI] OLCUM YARIDA KESILDI: %s" % kesildi)\n',
        "mutant/kismi-cikti")


def yama_hukum_yok_satirini_sil(m):
    """Kesilme hallerinin en bilgi tasiyan satirini susturur. Cikis kodu AYNI
    kalir (3); degisen yalniz METIN. Cikis koduna bakan bir kume bunu goremez —
    altin kume CIKTIYI da kilitledigi icin gormeli."""
    return _degistir(
        m,
        '            print("  -> HUKUM YOK: olcum tamamlanamadi (cikis kodu 3).")\n',
        '',
        "mutant/hukum-yok-satiri")


BAS_ISARET = "    # >>> GENISLEME BASI"
SON_ISARET = "    # <<< GENISLEME SONU\n"


def yama_yalniz_eski_haller(m):
    """ARACI genislemeden ONCEKI kapsama dondurur: HALLER'den alti yeni hal
    CIKARILIR. Bu yama SART: referansi suzmek YETMEZ. Arac 11 hal uretip
    referansta 10 kayit bulursa fazlaliklar 'YENI OLCUM' diye FARK sayilir ve
    kol yanlislikla 'gordu' der. Olculdu: yamasiz kolda exit=1 geliyordu —
    yani mutant korlugu gostermek yerine kendi kurulum hatasini olcuyordu."""
    i = m.find(BAS_ISARET)
    j = m.find(SON_ISARET)
    if i < 0 or j < 0 or j < i:
        raise AracKusuru(
            "mutant/yalniz-eski-haller: GENISLEME isaretleri bulunamadi "
            "(bas=%d son=%d). altin_cikti.py'de isaretler silindiyse MUTANT DA "
            "DEGISMELIDIR." % (i, j))
    if m.count(BAS_ISARET) != 1 or m.count(SON_ISARET) != 1:
        raise AracKusuru("mutant/yalniz-eski-haller: isaretler tek gecmiyor "
                         "(bas=%d son=%d)" % (m.count(BAS_ISARET), m.count(SON_ISARET)))
    return m[:i] + m[j + len(SON_ISARET):]


# ------------------------------------------------- ARACA ENJEKTE EDILEN KUSURLAR

def yama_hal_dusur(m):
    """h11'i HALLER'den cikarir: karsilastirma bunu KAYIP diye ilan etmeli."""
    return _degistir(
        m,
        '    ("h11_karisik_cok", [], False, [("kural_yanlis_ev", KURAL_SAYISI),\n'
        '                                    ("gecersiz_utf8", "KONULAR.md")]),\n',
        '',
        "mutant/hal-dusurme")


def yama_kesme_ilanini_sok(m):
    """Kesme ilanini geri alir: 12 satirdan sonrasi SESSIZCE dusurulur."""
    return _degistir(
        m,
        '        kesik = len(out) - 12\n',
        '        kesik = 0   # MUTANT: KESME ILANI SOKULU\n',
        "mutant/kesme-ilani")


# --------------------------------------------------------------- ALTYAPI

def agac_kur(taban, ad, motor_yamalari=(), arac_yamalari=()):
    """Yamalanmis ARAC + yamalanmis MOTOR ile calisir bir agac. Referans
    yazilmaz; cagiran `referans_yaz` ile koyar."""
    kok = os.path.join(taban, ad)
    os.makedirs(os.path.join(kok, "faz0"))
    os.makedirs(os.path.join(kok, "skill", "scripts"))
    for kaynak, yamalar, hedef in (
            (MOTOR, motor_yamalari, os.path.join(kok, "skill", "scripts", "hafiza.py")),
            (ARAC, arac_yamalari, os.path.join(kok, "faz0", "altin_cikti.py"))):
        metin = open(kaynak, encoding="utf-8").read()
        for y in yamalar:
            metin = y(metin)
        try:
            ast.parse(metin)
        except SyntaxError as e:
            raise AracKusuru("yamalanmis %s PARSE EDILEMIYOR (satir %s: %s)"
                             % (os.path.basename(kaynak), e.lineno, e.msg))
        with open(hedef, "w", encoding="utf-8", newline="\n") as f:
            f.write(metin)
    return kok


def referans_yaz(kok, kume):
    p = os.path.join(kok, "faz0", "ref.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"kume": kume}, f, ensure_ascii=False, indent=2)
    return p


def kos(kok, arglar, saniye=900):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run(
            [sys.executable, "-X", "utf8", os.path.join(kok, "faz0", "altin_cikti.py")]
            + arglar, capture_output=True, timeout=saniye, env=o,
            text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def temiz_referans(taban):
    """Referansi KOSUM ANINDA temiz motordan uretir (bayat dosyaya guvenmez)."""
    kok = agac_kur(taban, "referans_ureteci")
    p = os.path.join(taban, "temiz_ref.json")
    rc, c = kos(kok, ["--kaydet", p])
    if rc != 0:
        raise AracKusuru("temiz referans uretilemedi (exit=%s): %s" % (rc, c[-300:]))
    return json.load(open(p, encoding="utf-8"))["kume"]


def suz_eski(kume):
    """Genislemeden ONCEKI kapsam: yalniz bes yesil hal."""
    return [k for k in kume if k["hal"] in ESKI_HALLER]


def imza(cikti):
    return {
        "fark_yok": "FARK YOK" in cikti,
        "exit_farki": cikti.count("EXIT DEGISTI"),
        "exit_1_3": cikti.count("EXIT DEGISTI: 1 -> 3"),
        "kayip": cikti.count("OLCUM KAYBOLDU"),
        "gizlendi": cikti.count("SATIR FARKI DAHA GIZLENDI"),
        "hukum_yok_satiri": cikti.count("HUKUM YOK: olcum tamamlanamadi"),
        "davranis_degisti": "davranis DEGISTI" in cikti,
        "traceback": "Traceback (most recent call last)" in cikti,
    }


def kayit(ad, hukum, ayrinti):
    SONUC.append((ad, hukum, ayrinti))


# --------------------------------------------------------------- MUTANTLAR

def _kismi_cikti_kollari(taban, referans):
    """M-B1 ve M-B2 AYNI enjekte edilmis agaci paylasir; degisen yalniz KUME."""
    yeni_kok = agac_kur(taban, "kismi_yeni",
                        motor_yamalari=[yama_kismi_cikti_dusur])
    eski_kok = agac_kur(taban, "kismi_eski",
                        motor_yamalari=[yama_kismi_cikti_dusur],
                        arac_yamalari=[yama_yalniz_eski_haller])
    e = referans_yaz(eski_kok, suz_eski(referans))
    y = referans_yaz(yeni_kok, referans)
    return kos(eski_kok, ["--karsilastir", e]), kos(yeni_kok, ["--karsilastir", y])


def mb1_mb2_kismi_cikti(taban, referans):
    (e_rc, e_c), (y_rc, y_c) = _kismi_cikti_kollari(taban, referans)
    if e_rc is None or y_rc is None:
        kayit("M-B1/M-B2 kismi cikti", OLCULEMEDI,
              "zaman asimi (eski=%s yeni=%s)" % (e_rc, y_rc))
        return
    ei, yi = imza(e_c), imza(y_c)
    # 🔴 BU KOL AYRISMAYI OLCER, TEK BASINA "FARK YOK"U DEGIL. Bagimsiz denetci
    # ilk halini CURUTTU: olcut yalniz "eski kapsam FARK YOK der" idi ve bu, kusur
    # ENJEKTE EDILMESE DE dogruydu — yani kol KOSULSUZ yesil veriyordu (tautoloji).
    # Olculdu: enjeksiyon etkisizlestirildiginde (del F[:] -> pass) M-B1 hala ISIRDI
    # diyordu, M-B2/M-B6 ise KACTI. Bir mutant kolunun hukmu, olctugu kusurun VAR
    # OLMASINA bagli olmak ZORUNDADIR.
    kayit("M-B1 KAPSAM AYRISMASI: eski kapsam GORMEZ iken yeni kapsam GORUR",
          ISIRDI if (e_rc == 0 and ei["fark_yok"]
                     and y_rc == 1 and yi["davranis_degisti"]) else KACTI,
          "FAZ C kusuru motora ENJEKTE EDILDI | ESKI kapsam (5 yesil hal, 10 olcum): "
          "exit=%s 'FARK YOK'=%s | YENI kapsam (11 hal, 22 olcum): exit=%s "
          "'davranis DEGISTI'=%s (beklenen: 0/VAR -> 1/VAR. Ikisi de FARK YOK "
          "derse enjeksiyon ETKISIZ demektir ve bu kol KACTI der.)"
          % (e_rc, "VAR" if ei["fark_yok"] else "yok",
             y_rc, "VAR" if yi["davranis_degisti"] else "yok"))
    kayit("M-B2 YENI KUME ISIRIR: karisik haller EXIT DEGISTI 1 -> 3 diyor",
          ISIRDI if (y_rc == 1 and yi["davranis_degisti"] and yi["exit_1_3"] >= 2
                     and not yi["traceback"]) else KACTI,
          "ayni enjeksiyon · kume=11 hal (22 olcum) | exit=%s 'davranis DEGISTI'=%s "
          "'EXIT DEGISTI: 1 -> 3' sayisi=%s (beklenen: 1/VAR/>=2 — h10 ve h11, "
          "iki komutla dort kayit)"
          % (y_rc, "VAR" if yi["davranis_degisti"] else "yok", yi["exit_1_3"]))


def mb3_yanlis_pozitif(taban, referans):
    ad = "M-B3 YANLIS POZITIF YOK: temiz motor + genis kume -> FARK YOK"
    kok = agac_kur(taban, "temiz_kol")
    p = referans_yaz(kok, referans)
    rc, c = kos(kok, ["--karsilastir", p])
    if rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    i = imza(c)
    kayit(ad, ISIRDI if (rc == 0 and i["fark_yok"] and not i["traceback"]) else KACTI,
          "DOKUNULMAMIS motor · 22 olcum | exit=%s 'FARK YOK'=%s traceback=%s "
          "(beklenen: 0/VAR/yok — hata ve kesilme kayitlari KARARSIZ degil)"
          % (rc, "VAR" if i["fark_yok"] else "yok", "VAR" if i["traceback"] else "yok"))


def mb4_kesilme_metni(taban, referans):
    ad = "M-B4 KESILME METNI: 'HUKUM YOK' satiri silinirse YENI kume gorur"
    y_kok = agac_kur(taban, "metin_yeni", motor_yamalari=[yama_hukum_yok_satirini_sil])
    e_kok = agac_kur(taban, "metin_eski", motor_yamalari=[yama_hukum_yok_satirini_sil],
                     arac_yamalari=[yama_yalniz_eski_haller])
    y_rc, y_c = kos(y_kok, ["--karsilastir", referans_yaz(y_kok, referans)])
    e_rc, e_c = kos(e_kok, ["--karsilastir", referans_yaz(e_kok, suz_eski(referans))])
    if y_rc is None or e_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (yeni=%s eski=%s)" % (y_rc, e_rc))
        return
    yi, ei = imza(y_c), imza(e_c)
    # Cikis kodu DEGISMEZ (3 kalir); degisen yalniz METIN. Kume ciktiyi da
    # kilitledigi icin gormeli, eski kume ise o halleri HIC icermiyor.
    kayit(ad, ISIRDI if (y_rc == 1 and yi["davranis_degisti"] and yi["exit_farki"] == 0
                         and e_rc == 0 and ei["fark_yok"]) else KACTI,
          "'HUKUM YOK' satiri motordan SILINDI | YENI: exit=%s 'davranis DEGISTI'=%s "
          "EXIT-farki=%s | ESKI: exit=%s 'FARK YOK'=%s (beklenen: 1/VAR/0 -> 0/VAR; "
          "EXIT-farki 0 olmali cunku kusur SALT METINSEL)"
          % (y_rc, "VAR" if yi["davranis_degisti"] else "yok", yi["exit_farki"],
             e_rc, "VAR" if ei["fark_yok"] else "yok"))


def mb5_olcum_kayboldu(taban, referans):
    ad = "M-B5 OLCUM KAYBOLDU: hal DUSURULURSE karsilastirma KAYIP ilan eder"
    kok = agac_kur(taban, "hal_dusuk", arac_yamalari=[yama_hal_dusur])
    p = referans_yaz(kok, referans)          # referans 11 hal, arac 10 hal uretir
    rc, c = kos(kok, ["--karsilastir", p])
    if rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    i = imza(c)
    kayit(ad, ISIRDI if (rc == 1 and i["kayip"] == 2 and not i["traceback"]) else KACTI,
          "h11 HALLER'den SOKULDU (arac 20 olcum uretir, referans 22) | exit=%s "
          "'OLCUM KAYBOLDU' sayisi=%s (beklenen: 1/2 — h11'in iki komutu; "
          "0 cikarsa dusen hal SESSIZCE yutuluyor demektir)"
          % (rc, i["kayip"]))


def mb6_kesme_ilani(taban, referans):
    ad = "M-B6 ILAN EDILEN KESME: 12'den uzun fark listesinde GIZLENEN sayisi basilir"
    tam = agac_kur(taban, "kesme_tam", motor_yamalari=[yama_kismi_cikti_dusur])
    sok = agac_kur(taban, "kesme_sokuk", motor_yamalari=[yama_kismi_cikti_dusur],
                   arac_yamalari=[yama_kesme_ilanini_sok])
    t_rc, t_c = kos(tam, ["--karsilastir", referans_yaz(tam, referans)])
    s_rc, s_c = kos(sok, ["--karsilastir", referans_yaz(sok, referans)])
    if t_rc is None or s_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi (tam=%s sokuk=%s)" % (t_rc, s_rc))
        return
    ti, si = imza(t_c), imza(s_c)
    # Iki kol AYNI hukmu verir (exit 1). Ayrisan sey yalniz IZ: kac satirin
    # gizlendigi. fazB/altin_olcut'taki "iz kilidi" ile ayni ders.
    kayit(ad, ISIRDI if (t_rc == 1 and s_rc == 1 and ti["gizlendi"] >= 1
                         and si["gizlendi"] == 0) else KACTI,
          "kismi-cikti enjeksiyonu (uzun fark listesi uretir) | TAM: exit=%s "
          "'GIZLENDI' satiri=%s | SOKUK: exit=%s 'GIZLENDI' satiri=%s "
          "(beklenen: 1/>=1 -> 1/0; hukum AYNI kalmali, yoksa mutant hukmu "
          "degil izi olcemez)"
          % (t_rc, ti["gizlendi"], s_rc, si["gizlendi"]))


def main():
    print("=" * 82)
    print("ALTIN KUME GENISLEMESI MUTANTI — hata/kesilme kayitlari ISIRIYOR mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  arac     : %s" % ARAC)
    print("  motor    : %s" % MOTOR)
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="altin_kume_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        try:
            referans = temiz_referans(taban)
        except AracKusuru as e:
            print("\nARAC KUSURU: %s" % e)
            return 3
        eski_n, yeni_n = len(suz_eski(referans)), len(referans)
        print("  referans : KOSUM ANINDA temiz motordan uretildi — %d olcum" % yeni_n)
        print("             (genislemeden onceki kapsam: %d olcum)" % eski_n)
        if yeni_n <= eski_n:
            print("\nARAC KUSURU: kume genislememis (%d <= %d) — bu mutantin "
                  "olcecegi sey YOK." % (yeni_n, eski_n))
            return 3
        print()
        for f in (mb1_mb2_kismi_cikti, mb3_yanlis_pozitif, mb4_kesilme_metni,
                  mb5_olcum_kayboldu, mb6_kesme_ilani):
            try:
                f(taban, referans)
            except AracKusuru as e:
                print("\nARAC KUSURU: %s" % e)
                return 3
        say = {ISIRDI: 0, KACTI: 0, OLCULEMEDI: 0}
        for ad, hukum, ayrinti in SONUC:
            say[hukum] += 1
            print("  %-10s %s" % (hukum, ad))
            print("  %-10s   %s" % ("", ayrinti))
        print()
        print("OLCUMUN SINIRI (hukum degil):")
        print("  - ENJEKSIYON URUNUN GERCEK BIR SURUMU DEGILDIR. Burada olculen sey")
        print("    'kume bu SINIFI gorur mu'dur, 'motor bu kusuru tasiyor mu' DEGIL.")
        print("  - Referans kosum aninda uretilir; commit'li altin_kapi.json'un")
        print("    kendisi bu mutantin KAPSAMI DISINDADIR (onu --karsilastir isi olcer).")
        print("  - `kapi` komutunun DEGER KUMESI {0, 1, 3}: exit 2 motorun kendi")
        print("    sozlesmesinde `oldur()`un verdigi TEMIZ KULLANIM/GIRDI hukmudur")
        print("    (hafiza.py: `def oldur(msg, kod=2)`) ve cmd_kapi icinde hic")
        print("    `oldur()`/`sys.exit` YOKTUR — her kapi istisnasi exit 3 e doner.")
        print("    exit 130 (SIGINT) ise proje HALI degil, harici SINYAL gerektirir.")
        print("    Yani bu iki kod bir KAPSAM BOSLUGU degil, olculen komutun deger")
        print("    kumesinde OLMAYAN kodlardir. `oldur()` yolu BASKA komutlarla")
        print("    olculur (ornek: `isir` taze projede exit 2 verir).")
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — AYRISMA MUTANTI (uc kapi + uc mutant, ORTUSMESIZ) — BITTI md.7.

NEDEN VAR (olculdu 15 Agu 2026)
  md.7'nin ilk lafzi "iki dosya AYNI rolu iddia ederse KIRMIZI" idi. KOD YAZILMADAN
  alti gercek agac seklinde olculdu: DORDUNDE kirmizi yaniyor ve UCU MESRU
  (`CLAUDE.md`+`AGENTS.md` = iki ajanin kural evi · dort kural evi · `memory-bank/`
  tasarimi geregi cok dosyali). Yani lafiz KIRMIZIYI DEGERSIZLESTIRIRDI.
  Ikinci lafiz "ayni `konu` canli ile arsivde FARKLI govdeyle" idi; o da olculdu ve
  SAGLIKLI AKISTA atesliyordu: `derle` eski blogu arsive TASIR, ayni konu iki yerde
  durur ve govdeler ZORUNLU olarak farklidir (arsiv eski surumu tutar). Ustelik
  "arsivdeki satir elle degistirildi" hali H1 tarafindan ZATEN yakalaniyor
  (`[H1] 1 satir KAYIP` + `[H1-KOVA] sahte beyan`, cikis 1) — yeni kapi gereksizdi.
  Geriye OLCULEBILIR ve ZARARLI tek hal kaldi ve md.7 ona indirildi.

NE OLCER — UC AYRI YUZEY, UC AYRI SENARYO
  KAPI-A1 (SAHIPLIK YAZILIYOR) — `kur` ile taze proje
      Motorun URETTIGI her canli blok `sahip="hafiza-kur"` tasir. `sahip` ICERIGIN
      kaynagini soyler, ISARETI KOYANI degil: `derle`/`bloklastir` `sahip="proje"`
      yazar, cunku govde kullanicinindir.

  KAPI-A2 (SAHIPSIZLIK GORUNUR) — bir blogun `sahip` alani silinmis proje
      `kapi` ciktisinda `H10-SAHIP` OLCULEMEDI satiri basilmali. Bu bir FAIL
      DEGILDIR: eski defterlerde alan yoktur ve bu hata degil, OLCULEMEZLIKTIR.
      Sessiz sahiplenme yasak — bir blok "kimin" diye sorulamiyorsa iki defterin
      ayristigi da soylenemez.

  KAPI-C (COKLU CANLI KAPISI) — uc kollu
      C1 iki `canli` adayi -> `devral` cikis != 0, DISKE TEK BAYT yazmaz, mesaj
         `--esle` ister  ·  C2 `--esle canli=` kilidi akisi ACAR (cikis 0)  ·
      C3 tek aday -> cikis 0 (ADDITIVE; kural asiri ateslemiyor).
      Bugune kadar motor UYARIYOR sonra ilkini secip cikis 0 veriyordu (olculdu).

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. `sahip="proje"` yolunun (`derle`/`bloklastir`) AYRI mutanti YOK; KAPI-A1
     yalniz `kur` seklini olcer. Alan oralarda da yaziliyor ama ISIRTILMIYOR.
  2. Kural evi (`CLAUDE.md`·`AGENTS.md`·`memory-bank/`) KAPSAM DISI: motor oraya
     YAZMAZ (`SKILL.md` §2). Dosyalar arasi icerik ayrismasi bu turda OLCULMEZ.
  3. `sahip` degerinin DOGRULUGU olculmez (blok gercekten motorun mu?) — yalniz
     alanin VARLIGI ve yoklugunun GORUNURLUGU olculur.

CIKIS KODLARI
  0  uc kapi da temiz VE 3/3 mutant AYRI eksende ISIRDI
  1  bir kapi kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  OLCULEMEDI (motor okunamadi, mutant kurulamadi) — sessiz PASS verilmez
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
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
_BLOK = re.compile(r'^<!--\s*blok\s+(.*?)-->', re.M)
CANLI = "# A\n\n## GUNCEL DURUM\n\n- bir\n"


def kos(motor, *arg):
    p = subprocess.Popen([sys.executable, motor] + list(arg),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode if p.communicate() else None, p


def cagir(motor, *arg):
    p = subprocess.Popen([sys.executable, motor] + list(arg),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cikti = p.communicate()[0].decode("utf-8", "replace")
    return p.returncode, cikti


def yeni_kok(taban, **dosyalar):
    kok = tempfile.mkdtemp(prefix="ayr_", dir=taban)
    for ad, icerik in dosyalar.items():
        with io.open(os.path.join(kok, ad), "w", encoding="utf-8", newline="") as f:
            f.write(icerik)
    return kok


def blok_ozleri(p):
    try:
        s = io.open(p, encoding="utf-8", newline="").read()
    except OSError:
        return None
    return _BLOK.findall(s)


# ------------------------------------------------------------------ KAPI-A1
def kapi_a1(motor, taban):
    kok = tempfile.mkdtemp(prefix="a1_", dir=taban)
    kod, _ = cagir(motor, "kur", "--kok=" + kok)
    b = []
    if kod != 0:
        b.append("`kur` cikis %d (0 bekleniyordu)" % kod)
    oz = blok_ozleri(os.path.join(kok, "PROJE_HAFIZA.md"))
    if oz is None:
        return [("A1", "canli hafiza okunamadi")]
    if not oz:
        b.append("`kur` HIC blok yazmadi — kapi olcecek sey bulamaz")
    sahipsiz = [o for o in oz if "sahip=" not in o]
    if sahipsiz:
        b.append("%d/%d blokta `sahip=` YOK: %s"
                 % (len(sahipsiz), len(oz), sahipsiz[0][:60]))
    yabanci = [o for o in oz if 'sahip="hafiza-kur"' not in o and "sahip=" in o]
    if yabanci:
        b.append("`kur` blogu 'hafiza-kur' DISINDA sahiple yazdi: %s" % yabanci[0][:60])
    return [("A1", x) for x in b]


# ------------------------------------------------------------------ KAPI-A2
ESKI_DEFTER = ("# Eski Proje\n> Son guncelleme: 2026-08-15\n\n## GUNCEL DURUM\n"
               '<!-- blok konu="genel-durum" guncel="2026-08-15" kaynak="-" -->\n'
               "- eski defterden gelen satir\n<!-- /blok -->\n")


def kapi_a2(motor, taban):
    # SENARYO GERCEK VAKADIR: `sahip` alani OLMAYAN ESKI bir defter DEVRALINIR.
    # (Ilk yazimda `kur`dan sonra dosya ELLE kirpiliyordu; o zaman cipa ile dosya
    # ayrisiyor ve H1 "satir KAYIP" diyordu -> kapi KENDI senaryosu yuzunden
    # kirmizi yaniyordu. Olculdu ve senaryo duzeltildi: sahipsizlik DEVIR ANINDA
    # zaten oradaysa cipa da onu kapsar ve H1 temiz kalir.)
    kok = yeni_kok(taban, **{"PROJE_HAFIZA.md": ESKI_DEFTER})
    kod, _ = cagir(motor, "devral", "--esle", "canli=PROJE_HAFIZA.md", "--kok=" + kok)
    if kod != 0:
        return [("A2", "senaryo kurulamadi: `devral` cikis %d" % kod)]
    oz = blok_ozleri(os.path.join(kok, "PROJE_HAFIZA.md")) or []
    if not [o for o in oz if "sahip=" not in o]:
        return [("A2", "senaryo kurulamadi: sahipsiz blok kalmadi")]
    kod2, cikti = cagir(motor, "kapi", "--kok=" + kok)
    b = []
    if "H10-SAHIP" not in cikti:
        b.append("sahipsiz blok var ama `H10-SAHIP` OLCULEMEDI satiri BASILMADI "
                 "(sessiz sahiplenme)")
    if kod2 != 0:
        b.append("sahipsizlik FAIL uretti (cikis %d) — OLCULEMEDI bir HATA DEGILDIR" % kod2)
    return [("A2", x) for x in b]


# ------------------------------------------------------------------- KAPI-C
def _yazildi(kok):
    return sorted(x for x in (".hafizarc", "arsiv", "gunluk", "kararlar")
                  if os.path.exists(os.path.join(kok, x)))


def kapi_c(motor, taban):
    b = []
    # C1 — iki `canli` adayi: DUR, yazma, `--esle` iste
    kok = yeni_kok(taban, **{"PROJE_HAFIZA.md": CANLI, "MEMORY.md": CANLI})
    kod, cikti = cagir(motor, "devral", "--kok=" + kok)
    if kod == 0:
        b.append("C1: iki `canli` adayi varken cikis 0 — motor sessizce birini secti")
    if "--esle" not in cikti:
        b.append("C1: mesaj `--esle` istemiyor (kullaniciya cikis yolu verilmedi)")
    art = _yazildi(kok)
    if art:
        b.append("C1: DURMASINA RAGMEN yazdi: %s" % ", ".join(art))
    # C2 — kullanici kilidi akisi ACAR
    kok = yeni_kok(taban, **{"PROJE_HAFIZA.md": CANLI, "MEMORY.md": CANLI})
    kod, _ = cagir(motor, "devral", "--esle", "canli=MEMORY.md", "--kok=" + kok)
    if kod != 0:
        b.append("C2: `--esle canli=MEMORY.md` ile de DURDU (cikis %d) — kilit acmiyor" % kod)
    # C3 — tek aday: ADDITIVE
    kok = yeni_kok(taban, **{"PROJE_HAFIZA.md": CANLI})
    kod, _ = cagir(motor, "devral", "--kok=" + kok)
    if kod != 0:
        b.append("C3: TEK aday varken cikis %d — kural ASIRI atesliyor "
                 "(mevcut projeler kirilir)" % kod)
    return [("C", x) for x in b]


def hukum(motor, taban):
    return kapi_a1(motor, taban), kapi_a2(motor, taban), kapi_c(motor, taban)


# --------------------------------------------------------------- MUTANTLAR
def _tek_yerde(s, hedef):
    n = s.count(hedef)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali): %r\n" % (n, hedef[:60]))
        return False
    return True


def m1_sahip_alani_silinir(s):
    """`kur` sablonundan `sahip` alanlari silinir -> KAPI-A1 isirmali.

    Ekseni: SAHIPLIK YAZILIYOR. KAPI-A2 senaryosu alani zaten KENDISI siliyor
    (satir yine basilir) ve KAPI-C senaryolari `kur` sablonunu HIC yazmaz
    (C1 durur, C2/C3 mevcut dosyayi kullanir) => ortusmez."""
    yeni = s.replace(' sahip="hafiza-kur" -->', " -->")
    return yeni if yeni != s else None


def m2_olculemedi_bastirilir(s):
    """`H10-SAHIP` OLCULEMEDI satiri bastirilir -> KAPI-A2 isirmali.

    Ekseni: GORUNURLUK. `kur` hala `sahip=` yaziyor (A1 yesil), cikis kodlari
    degismiyor (C yesil) => ortusmez."""
    hedef = "    sahipsiz = [oz.get(\"konu\", \"?\") for _, _, oz in bl if not oz.get(\"sahip\")]\n"
    yeni = "    sahipsiz = []      # MUTANT: sessiz sahiplenme\n"
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


def m3_coklu_canli_kapisi_sokulur(s):
    """Coklu `canli` kosulu ULASILMAZ yapilir -> KAPI-C isirmali.

    Bu, motorun 15 Agu oncesi halidir: UYAR, sonra ilkini SEC, cikis 0 ver.
    Ekseni: DURMA. A1/A2 `kur` yolunda kosar, `devral`a hic girmez => ortusmez."""
    hedef = "    if a.canli is None and not esleme.get(\"canli\") and len(adaylar) > 1:\n"
    yeni = "    if a.canli is None and not esleme.get(\"canli\") and len(adaylar) > 99:\n"
    return s.replace(hedef, yeni, 1) if _tek_yerde(s, hedef) else None


MUTANTLAR = [
    ("M-1 `sahip` alani silinir", m1_sahip_alani_silinir, "KAPI-A1"),
    ("M-2 OLCULEMEDI bastirilir", m2_olculemedi_bastirilir, "KAPI-A2"),
    ("M-3 coklu canli kapisi sokulur", m3_coklu_canli_kapisi_sokulur, "KAPI-C"),
]


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    print(CIZGI)
    print("AYRISMA MUTANTI (md.7) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="ayrisma_")
    try:
        a1, a2, c = hukum(yol, taban)
        for ad, bulgu, ne in (("KAPI-A1 SAHIPLIK  ", a1, "`kur` bloklari sahip=hafiza-kur"),
                              ("KAPI-A2 GORUNURLUK", a2, "sahipsiz blok OLCULEMEDI basiyor"),
                              ("KAPI-C  COKLU CANLI", c, "C1 durdu+yazmadi · C2 kilit acti · C3 additive")):
            print("  %s: %s" % (ad, "YESIL (%s)" % ne if not bulgu
                                else "KIRMIZI — %d bulgu" % len(bulgu)))
            for _, x in bulgu:
                print("      ! %s" % x)
        if a1 or a2 or c:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = 0
        for ad, boz, beklenen in MUTANTLAR:
            bozuk = boz(s)
            if bozuk is None or bozuk == s:
                print("  %-34s KURULAMADI (mutant uygulanamadi)" % ad)
                kacan += 1
                continue
            mdir = tempfile.mkdtemp(prefix="mutant_", dir=taban)
            mp = os.path.join(mdir, "hafiza.py")
            with io.open(mp, "w", encoding="utf-8", newline="") as f:
                f.write(bozuk)
            ma1, ma2, mc = hukum(mp, taban)
            ates = [x for x, v in (("KAPI-A1", ma1), ("KAPI-A2", ma2), ("KAPI-C", mc)) if v]
            if ates == [beklenen]:
                print("  %-34s -> ISIRDI ✓  (%s)" % (ad, beklenen))
            elif beklenen in ates:
                print("  %-34s -> ISIRDI ama ORTUSTU: %s" % (ad, " + ".join(ates)))
                kacan += 1
            else:
                print("  %-34s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                      % (ad, beklenen, " + ".join(ates) or "hicbiri"))
                kacan += 1
        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
                  % (kacan, len(MUTANTLAR)))
            return 1
        print("SONUC: YESIL — uc kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
              % (len(MUTANTLAR), len(MUTANTLAR)))
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

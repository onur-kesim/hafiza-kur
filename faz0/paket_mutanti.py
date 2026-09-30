#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — PAKET MUTANTI (motorun `paket` komutu + `paketle.sh`in iki kapisi gercekten isiriyor mu?).

NEDEN VAR (olculdu 14 Agu 2026)
  `paketle.sh` bir SHA256 kapisi OLDUGUNU soyluyordu ama kapi OLUYDU:
  kontrol `[ -n "$BEYAN" ]` ile korunuyordu ve `SKILL.md`de 64'luk hex SIFIRDI
  (olculdu: `grep -coE '[0-9A-F]{64}' skill/SKILL.md` -> 0), yani `if` HIC
  girilmiyordu. Ustelik `SKILL.md` sat. 245-249 SHA yazmamayi OLCULMUS bir
  dersle savunuyor ("bayatlar; iki surum boyunca gorulmedi") — yani betigin
  BASLIGI ile belgenin KARARI carpisiyordu ve kod sessizce belgenin tarafini
  tutuyordu. Sinif IKINCI kez isirdi (1: LISANS, 10 Agu): "SKILL.md beyani ile
  paketin gercegi tutmuyor, kimse olcmuyor."

  Ayrica olculdu: `capraz.yml`de `paketle` ve `.skill` icin SIFIR esleme —
  paketleme, madde 4'un ve madde 2(ii)'nin dayandigi TEK yuzey, hic kosmuyordu.

30 EYL 2026 (besli-paket/IS_EMRI_URUN_HAZIRLIK.md KALEM 1): `.skill` URETIMI `zip` komutundan
  motorun `paket` alt komutuna (stdlib zipfile) TASINDI; `paketle.sh` onu CAGIRIR ve iki kapisi
  AYNEN kalir. Bu, mutantlarin da yeni uretici uzerinde yeniden kurulmasini gerektirdi: eski M-1
  (`zip -l`) ve M-2 (`-x references/*`) artik olmayan bir komutu sabote ediyordu.

NE OLCER — BES AYRI EKSEN (kapilar `paketle.sh`in icinde yasar, burasi ISIRMAYI olcer)
  KAPI-1 MOTOR BIT-BIT : zip'ten geri cikarilan `scripts/hafiza.py` kaynakla ayni mi
  KAPI-2 ENVANTER      : `skill/` altindaki filtre-disi her dosya pakette var mi
                         (ve pakette FAZLA dosya yok mu)
  DETERMINIZM          : ayni kaynaktan iki uretim BAYT-BIRBIRINE esit mi (sabit tarih/izin/
                         sira/sikistirma). Iki uretim arasinda 2 sn'den fazla BEKLENIR: zip'in
                         tarih cozunurlugu 2 sn'dir, bekleme olmadan "simdiki tarih" kusuru
                         iki uretimi ayni saniyeye dusurup GIZLENIRDI.
  IC OLCUM             : `paket` komutunun KENDI uretim-sonrasi olcumu bozuk ureticiyi yakaliyor
                         mu, ve yakalayinca paketi BIRAKMIYOR mu (exit 1, dosya YOK). Olcum uye
                         SIRASINI ve sabit alanlari (tarih/sistem/izin/saklanmis giris) da denetler:
                         iki uretimi karsilastirmak bunlari GORMEZ (ayni makinede ikisi de ayni bozuktur).
  BAGLANTI             : kaynakta DIZIN BAGLANTISI (symlink/junction) varsa `paket` REDDEDER (exit 2,
                         dosya YOK). `os.walk` bagli dizini izlemez; eski `zip -r` izliyordu. Reddetmese
                         paket references/'i SESSIZCE dusururdu ve iki KAPI da YESIL basardi (ikisi de
                         ayni yuruyusu kullanir) — bagimsiz tur 30 Eyl 2026'da yeniden uretildi.

  KAPI-1/2 ORTUSMEZ ve biri otekinin yerine GECMEZ: motor bit-bit dogru olup `references/`
  tumden dusebilir (LISANS sinifi); ya da butun dosyalar yerinde olup motorun baytlari satir-sonu
  cevrimiyle bozulabilir (`.gitattributes` `* -text` dersinin paketleme karsiligi).

  🔴 IC OLCUM, KAPI-1/2'NIN YERINE GECMEZ: M-1 ureticiyi bozarken komutun kendi olcumunu de
  sokerek KAPI-1'in BAGIMSIZ ısırdığını olcer. Komutun olcumu yalniz SUZULMUS KAYNAGA bakar; suzgecin
  kendisi bozulursa (M-2) ikisi de ayni yanlis kumeyi "dogru" sayar — o kusuru yalniz KAPI-2'nin
  BAGIMSIZ `beklenen()` listesi gorur.

MUTANTLAR — hepsi GERCEK ariza, uydurma degil (hedef dizge motorda TAM 1 kez gecmeli, degilse
KURULAMADI — h14_bolme dersi)
  M-1 satir-sonu cevrimi (uretici LF->CRLF yazar + komutun olcumu sokuk) -> KAPI-1 isirmali, KAPI-2 yesil
      (eski karsiligi `zip -l`: hafiza.py 259.228 -> 264.431 bayt, 5.203 satirin LF'i CRLF)
  M-2 suzgec `references`i dusurur (paylasilan suzgec bozulur)           -> KAPI-2 isirmali, KAPI-1 yesil
      (eski karsiligi `-x 'references/*'`: alti `references/*.md` paketten duser)
  M-3 determinizm sokulur (date_time = simdi)                            -> DETERMINIZM isirmali;
      iki kapi KOR: paket gecerli, eksiksiz, bit-bit — yalniz tekrar uretilemez
  M-4 uretici LF->CRLF yazar, komutun olcumu ACIK                        -> IC OLCUM isirmali:
      exit != 0, `hafiza-kur.skill` YOK, KAPI satiri YOK (kapilara hic ulasilmaz)
  M-5 uye sirasi tersine doner (sorted(reverse=True))                    -> IC OLCUM isirmali
      (iki uretim yine BAYT-ESIT, iki KAPI yine YESIL: sirayi yalniz komutun kendi olcumu gorur)
  M-6 create_system 3 -> 0 (Windows'un varsayilani)                      -> IC OLCUM isirmali
  M-7 dizin baglantisi reddi sokulur                                     -> BAGLANTI isirmali:
      baglantili kaynakta `paket` exit 0 verir (temiz motor exit 2 + dosya YOK)

NE OLCMEZ (hukum degil, SINIR)
  0. Platformlar arasi SHA ESITLIGINI CI'da olcmez: DETERMINIZM ayni makinede iki uretimi karsilastirir;
     Windows 3.12/3.14 ile WSL 3.14'te paketin AYNI SHA verdigi 30 Eyl 2026'da elle olculdu (macOS olculmedi).
     create_system/sira gibi platforma bagli sapmalari IC OLCUM'un (vi) ayagi on kosul olarak yakalar.
  1. Paketin KURULUP KOSTUGUNU olcmez — o `faz0/paketten_kos.py`in isidir.
  2. claude.ai'nin paketi KABUL ETTIGINI olcmez (hesaba yukleme yok; olculdu 30 Eyl 2026'da, `zip`
     CIKTISIYLA — Python zipfile ciktisiyla kabul ayri bir olcumdur).
  3. `paketle.sh`in kendi `set -eu` disi yollari olculmedi.
  4. Aciklama sinirini (500) olcmez — o `faz0/aciklama_siniri_mutanti.py`in isidir.

CIKIS KODLARI
  0  temiz agac iki kapidan da gecti, determinizm temiz VE tum mutantlar AYRI eksende ISIRDI
  1  temiz agac kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  olculemedi (calisan bash yok, dosya yok) — sessiz PASS verilmez
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time


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
BEKLEME = 2.2          # zip tarih cozunurlugu 2 sn

_K1 = re.compile(r"^KAPI-1 MOTOR BIT-BIT\s*:\s*(\w+)", re.M)
_K2 = re.compile(r"^KAPI-2 ENVANTER\s*:\s*(\w+)", re.M)


def bash_bul():
    """Calisan bir POSIX bash (yol | None). Windows'ta System32'deki bash.exe WSL baslaticisidir ve
    dagitim yoksa CALISMAZ: once Git'in bash'i aranir; her aday `echo` ile SINANIR."""
    adaylar = []
    if os.name == "nt" and shutil.which("git"):
        d = os.path.dirname(os.path.abspath(shutil.which("git")))
        for _ in range(4):
            adaylar += [os.path.join(d, "bin", "bash.exe"), os.path.join(d, "usr", "bin", "bash.exe")]
            d = os.path.dirname(d)
    if shutil.which("bash"):
        adaylar.append(shutil.which("bash"))
    for a in adaylar:
        if not os.path.isfile(a):
            continue
        try:
            r = subprocess.run([a, "-c", "echo hk-ok"], capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if r.returncode == 0 and r.stdout.strip() == "hk-ok":
            return a
    return None


def kum_havuzu(hedef):
    """`skill/` + `paketle.sh`i yalin bir dizine kopyalar (depo kirletilmez)."""
    shutil.copytree(os.path.join(KOK, "skill"), os.path.join(hedef, "skill"))
    shutil.copy2(os.path.join(KOK, "paketle.sh"), os.path.join(hedef, "paketle.sh"))
    os.chmod(os.path.join(hedef, "paketle.sh"), 0o755)


def motor_yolu(dizin):
    return os.path.join(dizin, "skill", "scripts", "hafiza.py")


def kos(bash, dizin):
    """`paketle.sh`i kosar; (cikis_kodu, KAPI-1 hali, KAPI-2 hali, ham cikti)."""
    p = subprocess.run([bash, "paketle.sh"], cwd=dizin,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    c = p.stdout.decode("utf-8", "replace")
    m1, m2 = _K1.search(c), _K2.search(c)
    return p.returncode, (m1.group(1) if m1 else None), (m2.group(1) if m2 else None), c


def uret(dizin, cikti):
    """Motorun `paket` komutunu DOGRUDAN kosar; (cikis_kodu, ham cikti)."""
    p = subprocess.run([sys.executable, motor_yolu(dizin), "paket", "--cikti", cikti],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def oku(yol):
    with open(yol, "rb") as f:
        return f.read()


def iki_uretim_esit(dizin):
    """Iki uretim BEKLEMEYLE (> zip tarih cozunurlugu) bayt-esit mi? (esit_mi | None, ayrinti)"""
    a, b = os.path.join(dizin, "uretim-a.skill"), os.path.join(dizin, "uretim-b.skill")
    k1, c1 = uret(dizin, a)
    time.sleep(BEKLEME)
    k2, c2 = uret(dizin, b)
    if k1 != 0 or k2 != 0:
        return None, "uretim exit %s/%s: %s" % (k1, k2, (c1 if k1 else c2).strip()[-120:])
    return oku(a) == oku(b), ""


# ------------------------------------------------------------------ MUTANTLAR
# Her mutant: (ad, [(eski, yeni), ...], beklenen eksen). `eski` motor metninde TAM 1 kez gecmeli.
_URETICI_CRLF = ('                veri = f.read()\n',
                 '                veri = f.read().replace(b"\\n", b"\\r\\n")\n')
_OLCUM_SOK = ('        ayak = _paket_olc(kd, gecici, sha_k)\n', '        ayak = None\n')
MUTANTLAR = [
    ("M-1 satir-sonu cevrimi (uretici + sokuk olcum)", [_URETICI_CRLF, _OLCUM_SOK], "KAPI-1"),
    ("M-2 suzgec references'i dusuruyor",
     [('_SKILL_KUR_HARIC_DIZIN = ("deneme", "__pycache__")',
       '_SKILL_KUR_HARIC_DIZIN = ("deneme", "__pycache__", "references")')], "KAPI-2"),
    ("M-3 determinizm sokuldu (date_time = simdi)",
     [('_PAKET_TARIH = (1980, 1, 1, 0, 0, 0)', '_PAKET_TARIH = __import__("time").localtime()[:6]')],
     "DETERMINIZM"),
    ("M-4 uretici bozuk, komutun olcumu acik", [_URETICI_CRLF], "IC-OLCUM"),
    ("M-5 uye sirasi tersine doner", [("for rel in sorted(kd):", "for rel in sorted(kd, reverse=True):")], "IC-OLCUM"),
    ("M-6 create_system 3 -> 0", [("zi.create_system = 3", "zi.create_system = 0")], "IC-OLCUM"),
    ("M-7 dizin baglantisi reddi sokuldu", [("    if baglanti:" + chr(10), "    if False:" + chr(10))], "BAGLANTI"),
]


def mutant_uygula(dizin, degisiklikler):
    """Motor kopyasina dizge sabotajlari uygular. None = uygulandi; str = KURULAMADI sebebi."""
    yol = motor_yolu(dizin)
    with open(yol, encoding="utf-8", newline="") as f:
        s = f.read()
    for eski, yeni in degisiklikler:
        n = s.count(eski)
        if n != 1:
            return "hedef dizge motorda %d kez geciyor (1 olmali): %r" % (n, eski[:60])
        s = s.replace(eski, yeni, 1)
    compile(s, "<mutant>", "exec")
    with open(yol, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    return None


def baglanti_kur(d):
    """`skill/references`i `d/dis/references`e giden bir DIZIN BAGLANTISINA cevirir (POSIX symlink, Windows
    junction — ikisi de ayricalik istemez). None = kuruldu; str = KURULAMADI sebebi (OLCULEMEDI)."""
    hedef, yol = os.path.join(d, "dis", "references"), os.path.join(d, "skill", "references")
    os.makedirs(os.path.dirname(hedef))
    shutil.move(yol, hedef)
    try:
        if os.name == "nt":
            r = subprocess.run(["cmd", "/c", "mklink", "/J", yol, hedef], capture_output=True)
            if r.returncode != 0:
                return "junction kurulamadi: %s" % r.stdout.decode("cp850", "replace").strip()[:80]
        else:
            os.symlink(hedef, yol, target_is_directory=True)
    except OSError as e:
        return "symlink kurulamadi: %s" % e
    if not os.path.isdir(yol):
        return "baglanti dizin olarak acilmiyor"
    return None


def baglanti_hukmu(bash, d, mutant):
    """BAGLANTI ekseni: temiz motor -> exit 2 + paket YOK + 'dizin baglantisi' mesaji; mutant -> bu hukmun
    DISINA ciktiysa ISIRDI. (durum, aciklama); kurulamazsa ('OLCULEMEDI', sebep)."""
    sebep = baglanti_kur(d)
    if sebep:
        return "OLCULEMEDI", sebep
    rc, _k1, _k2, ham = kos(bash, d)
    paket_var = os.path.exists(os.path.join(d, "hafiza-kur.skill"))
    temiz_hukum = rc == 2 and not paket_var and "dizin baglantisi" in ham
    if mutant:
        return (("KACTI", "baglanti reddi hala calisiyor") if temiz_hukum else
                ("ISIRDI", "BAGLANTI · baglantili kaynakta paket exit %s ile URETILDI (temiz motor exit 2)" % rc))
    return (("TAMAM", "exit 2 · paket YOK · 'dizin baglantisi' mesaji") if temiz_hukum
            else ("SAPTI", "exit %s · paket var mi: %s" % (rc, paket_var)))


def hukum(beklenen, bash, d):
    """Mutant tek bir eksende isirdi mi? (durum, aciklama): durum ISIRDI | ORTUSTU | KACTI."""
    if beklenen == "BAGLANTI":
        return baglanti_hukmu(bash, d, True)
    rc, k1, k2, ham = kos(bash, d)
    ates = [a for a, h in (("KAPI-1", k1), ("KAPI-2", k2)) if h == "KIRMIZI"]
    if beklenen in ("KAPI-1", "KAPI-2"):
        if rc == 0:
            return "KACTI", "paket exit 0 ile URETILDI"
        if ates == [beklenen]:
            return "ISIRDI", "%s · exit %s" % (beklenen, rc)
        if beklenen in ates:
            return "ORTUSTU", "ISIRDI ama ORTUSTU: %s" % " + ".join(ates)
        return "KACTI", "beklenen %s, atesleyen: %s (exit %s)" % (beklenen, " + ".join(ates) or "hicbiri", rc)
    if beklenen == "IC-OLCUM":
        kalan = [x for x in os.listdir(d) if x.startswith("hafiza-kur.skill")]
        if rc != 0 and not kalan and k1 is None and k2 is None and "PAKET OLCUMU TUTMADI" in ham:
            return "ISIRDI", "IC-OLCUM · exit %s · paket YOK · KAPI satiri YOK" % rc
        return "KACTI", "exit %s · kalan dosya: %s · KAPI-1=%s KAPI-2=%s" % (rc, kalan or "yok", k1, k2)
    # DETERMINIZM: iki kapi KOR kalmali (paket gecerli), fark yalniz iki uretim arasinda gorunmeli
    if rc != 0 or ates:
        return "ORTUSTU", "kapilar atesledi (exit %s, %s) — bu mutant kapilarin DISINDA olmaliydi" % (
            rc, " + ".join(ates) or "hicbiri")
    esit, ayr = iki_uretim_esit(d)
    if esit is None:
        return "KACTI", ayr
    return ("KACTI", "iki uretim BAYT-ESIT kaldi (determinizm kusuru gorunmedi)") if esit else (
        "ISIRDI", "DETERMINIZM · iki kapi yesil, iki uretim %.1f sn arayla bayt-FARKLI" % BEKLEME)


def main():
    bash = bash_bul()
    if bash is None:
        print("SONUC: ÖLÇÜLEMEDİ — calisan `bash` yok (paketle.sh bash ister; `zip` artik GEREKMEZ).")
        return 2
    if not os.path.isfile(os.path.join(KOK, "paketle.sh")):
        print("SONUC: ÖLÇÜLEMEDİ — paketle.sh yok.")
        return 2

    print("=== PAKET MUTANTI === kok: %s · platform: %s" % (os.path.basename(KOK), sys.platform))
    gecici = tempfile.mkdtemp(prefix="paket-mutanti-")
    try:
        temiz = os.path.join(gecici, "temiz")
        os.makedirs(temiz)
        kum_havuzu(temiz)
        rc, k1, k2, ham = kos(bash, temiz)
        print("  TEMIZ AGAC      : exit=%s · KAPI-1=%s · KAPI-2=%s" % (rc, k1, k2))
        if rc != 0 or k1 != "YESIL" or k2 != "YESIL":
            print("\n--- paketle.sh ciktisi ---\n%s" % ham.strip())
            print("\nSONUC: KIRMIZI — temiz agac kendi kapisini gecemedi.")
            return 1
        esit, ayr = iki_uretim_esit(temiz)
        paketle_ayni = oku(os.path.join(temiz, "uretim-a.skill")) == oku(os.path.join(temiz, "hafiza-kur.skill"))
        print("  DETERMINIZM     : iki uretim (%.1f sn arayla) %s · paketle.sh paketi ile %s"
              % (BEKLEME, "bayt-ESIT" if esit else "bayt-FARKLI%s" % (" (%s)" % ayr if ayr else ""),
                 "AYNI" if paketle_ayni else "FARKLI"))
        if not esit or not paketle_ayni:
            print("\nSONUC: KIRMIZI — temiz agacta paket determinist degil ya da paketle.sh motorun ciktisindan farkli.")
            return 1

        bd = os.path.join(gecici, "temiz-baglanti")
        os.makedirs(bd)
        kum_havuzu(bd)
        bdurum, bacik = baglanti_hukmu(bash, bd, False)
        print("  BAGLANTI        : %s · %s" % (bdurum, bacik))
        if bdurum == "SAPTI":
            print("\nSONUC: KIRMIZI — temiz motor dizin baglantili kaynagi REDDETMEDI.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = 0
        olculemeyen = 0
        for ad, degisiklikler, beklenen in MUTANTLAR:
            d = os.path.join(gecici, ad.split()[0])
            os.makedirs(d)
            kum_havuzu(d)
            sebep = mutant_uygula(d, degisiklikler)
            if sebep:
                print("  %-46s KURULAMADI (%s)" % (ad, sebep))
                kacan += 1
                continue
            durum, acik = hukum(beklenen, bash, d)
            if durum == "ISIRDI":
                print("  %-46s -> ISIRDI ✓  (%s)" % (ad, acik))
            elif durum == "OLCULEMEDI":
                print("  %-46s -> OLCULEMEDI (%s)" % (ad, acik))
                olculemeyen += 1
            else:
                print("  %-46s -> %s ✗  (%s)" % (ad, "KACTI" if durum == "KACTI" else "ORTUSTU", acik))
                kacan += 1

        if kacan:
            print("\nSONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
                  % (kacan, len(MUTANTLAR)))
            return 1
        if olculemeyen or bdurum == "OLCULEMEDI":
            print("\nSONUC: OLCULEMEDI — BAGLANTI ekseni kurulamadi (symlink/junction): sessiz PASS verilmez.")
            return 2
        print("\nSONUC: YESIL — iki kapi da temiz, determinizm temiz, %d/%d mutant AYRI eksende ISIRDI."
              % (len(MUTANTLAR), len(MUTANTLAR)))
        return 0
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

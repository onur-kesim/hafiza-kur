#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — DEVRAL POLITIKA MUTANTI (devral GIRIS KAPISI, KALEM 1 — 26 Eyl 2026).

NEDEN VAR (olculdu: Cowork, temiz Linux, uid 1001, pallets/click; yerelde
Windows'ta, yetkisiz kullaniciyla tekrarlandi)
  `devral --esle canli=PROJE_HAFIZA.md` YENI defteri sablondan yaziyordu (8 gercek
  `## ` basligi) ama `.hafizarc > zorunlu_bolumler` BOS kaliyordu: liste, dosya
  YAZILMADAN once taranan basliklardan geliyordu ve yeni defterde okunacak baslik
  yoktu. Zincir (her halkasi olculdu): bos liste -> H3 fiilen olu -> H15 kalici
  FAIL -> `kapi` hic yesillenmiyor -> `isir` exit 4. Yani aracin vitrini olan KOR
  KAPI PROTOKOLU yabancinin elinde HIC kosmuyordu; tek cikis `politika_gerekce`
  beyaniydi — gevsetmeyi ARAC yapmisti, kullaniciya imzalatiyordu.
  Duzeltme (SIK A): liste yazim bittikten SONRA diskten turetilir
  (`_devral_zorunlu_diskten`).

NE OLCER — UC KAPI, YALNIZ POLITIKA EKSENI (hepsi GERCEK subprocess; fikstur:
tanidik defteri OLMAYAN, en az bir commit'li git deposu)
  KAPI-A  devral --esle canli=PROJE_HAFIZA.md sonrasi, ELLE DUZENLEME YOK:
          (a) zorunlu_bolumler BOS DEGIL · (b) diskteki `## ` basliklarinin
          BIREBIR (susleriyle, sirali) kopyasi · (c) belgelenen akista defter
          commit'lenince `kapi` exit 0 ve ciktida [H15] YOK
  KAPI-B  H3 SILAHLI: turetilen bir baslik canlidan silinince `kapi` o basligi
          ADIYLA [H3] olarak basar (liste kapiyi silahsizlandirmiyor)
  KAPI-C  UC UCA VITRIN: not -> derle -> `kapi` exit 0 -> `isir` exit 0 ve
          kosulan her mutant ISIRIYOR

MUTANTLAR (hafiza.py kaynagina textual sabotaj)
  P-1  turetim cagrisi sokulur (26 Eyl oncesi davranis: liste bos kalir)
  P-2  ELENEN SIK B: liste kur'un SABIT varsayilanindan kopyalanir (iki kaynak)

ORTUSME OLCUMU (is emri kabul 3 — ortusen tespit korlugu maskeler)
  Bu kapi, KARDES kapinin (faz0/devral_teshis_mutanti.py, MESAJ ekseni)
  mutantlari altinda YESIL KALMALIDIR — kalmazsa iki eksen ortusuyordur. Ayrica
  CIFT MUTANT: P-1, kardesin M-1'i ile BIRLIKTE uygulandiginda (yani MESAJ
  duzeltmesi de sokulmusken) bu kapi yine ISIRMALIDIR.

NE OLCMEZ
  1. TRIYAJ mesaji (kardes kapinin ekseni).
  2. H9/H14'un devralmadaki davranisi (H14 13 Eyl'de "dogru davranis" diye
     kilitlendi; fikstur bu yuzden projesi BUGUN commit'lenmis bir depodur).
  3. `kur` yolu (bu duzeltme ona dokunmaz; bayt-esitligi ayrica olculdu).

CIKIS KODLARI
  0  uc kapi temiz, her mutant ISIRDI, ortusme YOK
  1  bir kapi KIRMIZI · bir mutant KACTI · ortusme VAR
  2  OLCULEMEDI (git yok, motor okunamadi, mutant/fikstur kurulamadi) — sessiz PASS yok

KULLANIM
  python faz0/devral_politika_mutanti.py [motor]
  POZITIF KONTROL: duzeltmeden ONCEKI motorla kosulunca kapilar KIRMIZI yanar ve
  mutant capalari 0 kez gecer (olculdu, commit mesajinda).
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill", "scripts", "hafiza.py")
CANLI = "PROJE_HAFIZA.md"
_GIT_KIMLIK = ["-c", "user.name=olcum", "-c", "user.email=olcum@example.invalid",
               "-c", "commit.gpgsign=false"]


class Kurulamadi(Exception):
    """Fikstur KURULUMU basarisiz (git, devral, not, derle) — KAPI HUKMU DEGILDIR."""


def kos(motor, *argv, kok=None):
    """`_kapi_metni` ile AYNI cagri kalibi: -X utf8 + PYTHONIOENCODING=utf-8."""
    cmd = [sys.executable, "-X", "utf8", motor] + list(argv)
    if kok is not None:
        cmd.append("--kok=" + kok)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *argv):
    r = subprocess.run(["git"] + _GIT_KIMLIK + list(argv), cwd=kok,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise Kurulamadi("git %s basarisiz (exit %d): %s"
                         % (" ".join(argv), r.returncode, (r.stdout + r.stderr)[:200]))


def _commit(kok, mesaj):
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "--allow-empty", "-m", mesaj)


def disk_basliklari(kok):
    """Motorun devral taramasiyla AYNI kural: `## ` ile baslayan satir, rstrip."""
    with io.open(os.path.join(kok, CANLI), encoding="utf-8", newline="") as f:
        return [s.rstrip() for s in f.read().split("\n") if s.startswith("## ")]


def rc_listesi(kok):
    try:
        with io.open(os.path.join(kok, ".hafizarc"), encoding="utf-8") as f:
            return json.load(f).get("zorunlu_bolumler")
    except (OSError, ValueError) as e:
        raise Kurulamadi(".hafizarc okunamadi: %s" % e)


def devralinmis_proje(motor, taban, ad):
    """Tanidik defteri OLMAYAN, commit'li bir git deposu + YENI canli ile devral."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    with io.open(os.path.join(kok, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# ornek proje\n\nHafiza defteri OLMAYAN gercekci bir depo.\n")
    _git(kok, "init", "-q", ".")
    _commit(kok, "ilk commit")
    k, c = kos(motor, "devral", "--esle", "canli=" + CANLI, kok=kok)
    if k != 0:
        raise Kurulamadi("devral basarisiz (exit %d): %s" % (k, c[-300:]))
    return kok, c


# ================================================================== KAPILAR

def kapi_a(motor, taban):
    """(a) liste bos degil · (b) diskteki basliklarin birebir kopyasi ·
    (c) defter commit'lenince kapi exit 0, [H15] yok."""
    kok, _ = devralinmis_proje(motor, taban, "kapi_a")
    b = []
    rc = rc_listesi(kok)
    disk = disk_basliklari(kok)
    if not rc:
        b.append("(a) zorunlu_bolumler BOS (%r) — H3 fiilen olu, H15 kalici FAIL" % (rc,))
    elif rc != disk:
        b.append("(b) zorunlu_bolumler diskteki basliklarin BIREBIR kopyasi DEGIL "
                 "(liste %d: %r · disk %d: %r)" % (len(rc), rc[:3], len(disk), disk[:3]))
    _commit(kok, "hafiza defteri")        # belgelenen akis: defter commit'lenir (H9)
    k, c = kos(motor, "kapi", kok=kok)
    if "[H15]" in c:
        b.append("(c) kapi [H15] basiyor: %s" % _satir(c, "[H15]"))
    if k != 0:
        b.append("(c) kapi exit %d (0 bekleniyordu): %s" % (k, _sonuc(c)))
    return b


def kapi_b(motor, taban):
    """Turetilen baslik (diskteki 3. `## `) silinince [H3] onu ADIYLA basar."""
    kok, _ = devralinmis_proje(motor, taban, "kapi_b")
    disk = disk_basliklari(kok)
    if len(disk) < 3:
        raise Kurulamadi("canlida 3'ten az `## ` basligi var (%d) — H3 kolu kurulamaz"
                         % len(disk))
    hedef = disk[2]
    p = os.path.join(kok, CANLI)
    with io.open(p, encoding="utf-8", newline="") as f:
        L = f.read().split("\n")
    L = [s for s in L if s.rstrip() != hedef]
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L))
    k, c = kos(motor, "kapi", kok=kok)
    beklenen = "[H3] zorunlu bolum YOK: " + hedef
    if beklenen not in c:
        return ["turetilen baslik silindi ama kapi '%s' BASMADI (exit %d): %s"
                % (beklenen, k, _sonuc(c))]
    return []


_ISIR_OZET = re.compile(r"SONUC: (\d+)/(\d+) kosulan mutant ISIRIYOR")


def kapi_c(motor, taban):
    """Uc uca: not -> derle -> kapi exit 0 -> isir exit 0, kosulan her mutant ISIRIYOR."""
    kok, _ = devralinmis_proje(motor, taban, "kapi_c")
    _commit(kok, "hafiza defteri")
    k, c = kos(motor, "not", "--konu=genel-durum", "--metin=ilk olcum notu", kok=kok)
    if k != 0:
        raise Kurulamadi("not basarisiz (exit %d): %s" % (k, c[-200:]))
    k, c = kos(motor, "derle", kok=kok)
    if k != 0:
        # HUKUMDUR, kurulum hatasi DEGIL: `derle` kendi sonunda `kapi` kosar ve FAIL
        # gorurse exit 1 verir (olculdu: P-1 altinda H15). Kurulamadi saymak bu
        # isirigi OLCULEMEDI'ye gomuyordu (ilk yazimda boyle oldu, olculdu).
        return ["derle exit %d (0 bekleniyordu; derle sonunda kapi kosar): %s"
                % (k, _sonuc(c))]
    _commit(kok, "ilk derleme")
    k, c = kos(motor, "kapi", kok=kok)
    if k != 0:
        return ["not+derle sonrasi kapi exit %d (0 bekleniyordu): %s" % (k, _sonuc(c))]
    k, c = kos(motor, "isir", kok=kok)
    m = _ISIR_OZET.search(c)
    b = []
    if k != 0:
        b.append("isir exit %d (0 bekleniyordu): %s" % (k, _satir(c, "SONUC") or c[-200:]))
    if not m or m.group(1) != m.group(2):
        b.append("isir ozeti 'N/N kosulan mutant ISIRIYOR' DEGIL: %s"
                 % (_satir(c, "SONUC") or "(ozet yok)"))
    return b


def _satir(c, parca):
    for s in c.split("\n"):
        if parca in s:
            return s.strip()[:200]
    return ""


def _sonuc(c):
    return _satir(c, "SONUC") or c.strip().split("\n")[-1][:200]


KAPILAR = (("KAPI-A", kapi_a, "yeni canli: liste diskten, birebir, kapi exit 0"),
           ("KAPI-B", kapi_b, "turetilen baslik silinince [H3] adiyla"),
           ("KAPI-C", kapi_c, "uc uca: not+derle, kapi 0, isir 0"))


# ================================================================= MUTANTLAR

def _degistir(s, eski, yeni, etiket):
    n = s.count(eski)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [%s]: %r\n"
                         % (n, etiket, eski[:70]))
        return None
    return s.replace(eski, yeni, 1)


def p1_turetim_sokulur(s):
    """26 Eyl oncesi davranis: yazim sonrasi turetim HIC cagrilmaz, yeni canlida
    liste bos kalir -> KAPI-A/B/C ISIRMALI."""
    return _degistir(s, "    _devral_zorunlu_diskten(kok, canli_p, rc)\n",
                     "    pass  # MUTANT P-1: yazim sonrasi turetim SOKULDU\n", "P-1")


def p2_elenen_sik_b(s):
    """ELENEN SIK B: liste diskten degil kur'un SABIT varsayilanindan gelir (iki
    kaynak; dosyada diakritikli, listede ASCII) -> KAPI-A (b) ISIRMALI."""
    return _degistir(s,
                     '    _yazim_sonrasi = [s.rstrip() for s in satirlar(canli_p) '
                     'if s.startswith("## ")]\n',
                     '    _yazim_sonrasi = list(VARSAYILAN_RC["zorunlu_bolumler"])'
                     '  # MUTANT P-2: ELENEN SIK B\n', "P-2")


MUTANTLAR = [
    ("P-1  yazim sonrasi turetim sokulur (liste bos)", p1_turetim_sokulur),
    ("P-2  ELENEN SIK B (kur'un sabit listesi)", p2_elenen_sik_b),
]


# ===================================================================== main

def _git_var():
    return shutil.which("git") is not None


def hukum(motor):
    """Uc kapiyi kosar: ({ad: [bulgu]}, olculemeyen_sayisi, [not])."""
    sonuc, olculemeyen, notlar = {}, 0, []
    for ad, fn, _ne in KAPILAR:
        taban = tempfile.mkdtemp(prefix="devral_politika_")
        try:
            sonuc[ad] = fn(motor, taban)
        except Kurulamadi as e:
            sonuc[ad] = None
            olculemeyen += 1
            notlar.append("%s OLCULEMEDI — %s" % (ad, e))
        finally:
            shutil.rmtree(taban, ignore_errors=True)
    return sonuc, olculemeyen, notlar


def _kirmizi(sonuc):
    return [ad for ad, b in sonuc.items() if b]


def _sahte_motor(kaynak, d):
    try:
        compile(kaynak, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(d, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(kaynak)
    return p, None


def _mutant_hukmu(kaynak, fonklar):
    """Kaynaga fonklari SIRAYLA uygular ve kapilari kosar.
    Doner: (kirmizi_kapilar | None, aciklama). Kirmizi VARKEN olculemeyen
    kapilar da aciklamada ADIYLA doner — sessizce dusmez."""
    bozuk = kaynak
    for fn in fonklar:
        bozuk = fn(bozuk) if bozuk is not None else None
    if bozuk is None or bozuk == kaynak:
        return None, "mutant KURULAMADI (capa)"
    d = tempfile.mkdtemp(prefix="devral_politika_mut_")
    try:
        sahte, hata = _sahte_motor(bozuk, d)
        if sahte is None:
            return None, hata
        sonuc, olc, notlar = hukum(sahte)
        kir = _kirmizi(sonuc)
        if olc and not kir:
            return None, "; ".join(notlar)[:200]
        olcmeyen = [ad for ad, b in sonuc.items() if b is None]
        return kir, ("; OLCULEMEDI: %s" % ", ".join(olcmeyen)) if olcmeyen else ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _kardes_mutantlari():
    """MESAJ ekseninin mutantlari (tek kaynak: kardes betik)."""
    try:
        import devral_teshis_mutanti as kardes     # faz0/ sys.path[0]'dadir
    except ImportError as e:
        return None, str(e)
    return kardes.MUTANTLAR, None


def main():
    _cikti_kodlamasini_guvenceye_al()
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN_MOTOR)
    print("=== DEVRAL POLITIKA MUTANTI (KALEM 1) === motor: %s · platform: %s"
          % (motor, sys.platform))
    if not _git_var():
        print("SONUC: OLCULEMEDI — git yok; fikstur commit'li git deposu ister.")
        return 2
    try:
        kaynak = io.open(motor, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2

    olculemeyen = 0
    sonuc, olc, notlar = hukum(motor)
    olculemeyen += olc
    for ad, _fn, ne in KAPILAR:
        b = sonuc[ad]
        durum = "OLCULEMEDI" if b is None else ("KIRMIZI" if b else "YESIL (%s)" % ne)
        print("  %-7s: %s" % (ad, durum))
        for x in b or []:
            print("      - %s" % x)
    for n in notlar:
        print("      ! %s" % n)
    kirmizi = len(_kirmizi(sonuc))

    print("\n--- MUTANT SINAMASI (kendi ekseni: POLITIKA) ---")
    kacan = 0
    for ad, fn in MUTANTLAR:
        kir, aciklama = _mutant_hukmu(kaynak, [fn])
        if kir is None:
            print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
            olculemeyen += 1
        elif kir:
            print("  %-48s -> ISIRDI (%s%s)" % (ad, ", ".join(kir), aciklama))
        else:
            print("  %-48s -> KACTI (uc kapi da KOR)" % ad)
            kacan += 1

    print("\n--- ORTUSME OLCUMU (kardes eksen: MESAJ — bu kapi YESIL KALMALI) ---")
    ortusen, olculen = 0, 0
    kardes, hata = _kardes_mutantlari()
    if kardes is None:
        print("  kardes betik yuklenemedi: %s -> OLCULEMEDI" % hata)
        olculemeyen += 1
    else:
        for ad, fn in kardes:
            kir, aciklama = _mutant_hukmu(kaynak, [fn])
            if kir is None:
                print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
                olculemeyen += 1
                continue
            olculen += 1
            if kir:
                print("  %-48s -> ORTUSME: bu kapi da yandi (%s%s)"
                      % (ad, ", ".join(kir), aciklama))
                ortusen += 1
            else:
                print("  %-48s -> ayri eksen (bu kapi YESIL kaldi)" % ad)
        # CIFT MUTANT: MESAJ duzeltmesi de sokulmusken bu kapi hala ISIRIYOR mu?
        ad = "CIFT  P-1 + kardes M-1 (mesaj duzeltmesi de yok)"
        kir, aciklama = _mutant_hukmu(kaynak, [p1_turetim_sokulur, kardes[0][1]])
        if kir is None:
            print("  %-48s -> OLCULEMEDI (%s)" % (ad, aciklama))
            olculemeyen += 1
        elif kir:
            print("  %-48s -> ISIRDI (%s%s)" % (ad, ", ".join(kir), aciklama))
        else:
            print("  %-48s -> KACTI (tespit kardes duzeltmeye BAGLI)" % ad)
            kacan += 1
    print("  ortusme: %d / %d OLCULEN kardes mutant (toplam %d)"
          % (ortusen, olculen, len(kardes or [])))

    print()
    if kacan or ortusen:
        print("SONUC: KIRMIZI — %d mutant KACTI, %d ortusme." % (kacan, ortusen))
        return 1
    if kirmizi:
        print("SONUC: KIRMIZI — %d kapi temiz motorda kirmizi (mutant sinamasindan ONCE)."
              % kirmizi)
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem kosulamadi/kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    print("SONUC: YESIL — uc kapi temiz, her mutant ISIRDI, ortusme YOK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

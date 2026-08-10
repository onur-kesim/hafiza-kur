#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ B SENARYOLARI — yaz() atomiklestirmesi ISIRIYOR MU?

KAPSAM (Faz B kararlari, oturum 2026-08-10):
  1. Yalniz `yaz()` (truncate yolu). Append defter yazimlari BU TURDA ELLENMEDI.
  2. Hedef salt-okunur ise: REDDET + temiz teshis + cikis yolu. Izin ASILMAZ.
  3. Dayaniklilik: fsync(dosya) + os.replace. DIZIN fsync'lenmez -> ani guc
     kesintisi sinifi OLCULMEDI ve "kapandi" DENMEZ (asagida SINIR olarak basilir).
  4. Yeni dosyanin modu: hedef varsa HEDEFIN modu kopyalanir, yoksa umask.
  5. Hardlink: atomik yazilir (BAG KOPAR) ve yol_on_kontrol'un UYARI METNI bu
     gercege gore duzeltilmistir. Metin ile davranis ayrisirsa B-B5 isirir.

HER DUZELTMEYE AYRI SENARYO, HER SENARYOYA AYRI SABOTAJ.
  TEMIZ   : duzeltilmis hafiza.py    -> beklenen davranis GORULMELI
  SABOTAJ : duzeltme sokulmus kopya  -> ESKI KUSUR yeniden URETILMELI
  Yalnizca ikisi de tutarsa senaryo ISIRDI der.

COKME URETME YOLU (fazA dersi): cokme, IZIN MODELIYLE degil ENJEKSIYONLA uretilir.
`os.chmod` Windows'ta dizinlerde etkisizdir; izinle cokme ureten senaryo aracin
degil ORTAMIN hukmunu olcer. Enjeksiyon her iki kolda da AYNI MANTIKSAL NOKTAYA
konur: "yazma basladi, icerik yerlesmeden kesildi".

CIKIS KODLARI (proje sozlesmesi)
  0 her senaryo ISIRDI · 1 en az biri KACTI · 2 en az biri OLCULEMEDI
  3 ARAC KUSURU (senaryolar kurulamadi)
"""
import os
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

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "skill", "scripts", "hafiza.py")

SONUC = []
SINIRLAR = []
ROOT = hasattr(os, "geteuid") and os.geteuid() == 0


class SenaryoKurulamadi(Exception):
    pass


def kayit(ad, isirdi, ayrinti):
    SONUC.append((ad, isirdi, ayrinti))


def _degistir(metin, eski, yeni, etiket):
    """Tek eslesmeli degistirme + SATIR SINIRI guvencesi (fazA'daki ile ayni ders:
    girinti tasiyan bir desen satirin ORTASINA eslesirse yamalanmis kopya bozulur ve
    senaryo ARACI degil KENDI YAMASINI olcer)."""
    n = metin.count(eski)
    if n != 1:
        raise SenaryoKurulamadi(
            "%s sabotaji: hedef metin %d kez gecti (1 olmali). Duzeltme tasindiysa "
            "SABOTAJ DA TASINMALI." % (etiket, n))
    i = metin.index(eski)
    if eski[:1] in (" ", "\t") and i != 0 and metin[i - 1] != "\n":
        raise SenaryoKurulamadi(
            "%s sabotaji: desen girinti tasiyor ama eslesme SATIR BASINDA degil "
            "(alt-dize eslesmesi) — yamalanmis kopya bozulur." % etiket)
    return metin.replace(eski, yeni, 1)


# --------------------------------------------------------------- ENJEKSIYON
# Iki kolda AYNI mantiksal nokta: hedef yazmaya acildi, icerik HENUZ yerlesmedi.

ENJ = ("            if os.environ.get(\"FAZB_KES\"):\n"
       "                raise OSError(5, \"FAZB enjekte edilen kesinti\")\n")


def enj_temiz(m):
    """Atomik yolda: mkstemp acildi, f.write(s) HENUZ kosmadi."""
    return _degistir(
        m,
        "        with os.fdopen(fd, \"w\", encoding=\"utf-8\", newline=\"\\n\") as f:\n"
        "            f.write(s)\n",
        "        with os.fdopen(fd, \"w\", encoding=\"utf-8\", newline=\"\\n\") as f:\n"
        + ENJ +
        "            f.write(s)\n",
        "enjeksiyon/temiz")


# --------------------------------------------------------------- SABOTAJLAR

ESKI_YAZ_GOVDE = (
    "def yaz(p, s):\n"
    "    os.makedirs(os.path.dirname(p) or \".\", exist_ok=True)\n"
    "    with open(p, \"w\", encoding=\"utf-8\", newline=\"\\n\") as f:\n"
    "        if os.environ.get(\"FAZB_KES\"):\n"
    "            raise OSError(5, \"FAZB enjekte edilen kesinti\")\n"
    "        f.write(s)\n")

YENI_YAZ_GOVDE = (
    "def yaz(p, s):\n"
    "    os.makedirs(os.path.dirname(p) or \".\", exist_ok=True)\n"
    "    _yazma_on_kontrol(p)\n")


def sab_bb1(m):
    """B-B1: atomiklik SOKULUR — v2.5.0 oncesi truncate-write geri gelir."""
    i = m.index(YENI_YAZ_GOVDE)
    j = m.index("def satirlar(p):", i)
    return m[:i] + ESKI_YAZ_GOVDE + "\n\n" + m[j:]


def sab_bb2(m):
    """B-B2: izin kapisi SOKULUR — os.replace 0444'u sessizce asar."""
    return _degistir(m, "    _yazma_on_kontrol(p)\n", "", "B-B2/izin kapisi")


def sab_bb3(m):
    """B-B3: hedefin modunu kopyalama SOKULUR — mkstemp varsayilani (0600) kalir."""
    return _degistir(
        m,
        "            mod = stat.S_IMODE(os.stat(p).st_mode)   # IZIN KAYMASI YOK\n",
        "            pass\n",
        "B-B3/mod kopyasi")


def sab_bb4(m):
    """B-B4: gecici dosya temizligi SOKULUR — .part artigi kalir."""
    return _degistir(
        m,
        "            try:\n                os.unlink(tmp)\n            except OSError:\n                pass\n",
        "            pass\n",
        "B-B4/artik temizligi")


def sab_bb5(m):
    """B-B5: hardlink UYARI METNI v2.4.1 haline dondurulur (davranis AYNI kalir).
    Yani sabotaj kolunda metin 'oradaki adi da degistirir' derken os.replace bagi
    KOPARIR — belge ile davranis AYRISIR."""
    return _degistir(
        m,
        "            \"UYARI: %d dosyanin proje DISINDA da bir adi var (hardlink). Arac ATOMIK\\n\"\n"
        "            \"  yazar (gecici dosya + os.replace), yani BAG KOPAR: proje DISINDAKI ad\\n\"\n"
        "            \"  ESKI icerikte KALIR ('cp -al' ile alinmis yedek artik GUNCELLENMEZ).\\n\"\n",
        "            \"UYARI: %d dosyanin proje DISINDA da bir adi var (hardlink). Bu dosyalara\\n\"\n"
        "            \"  yazmak oradaki adi da degistirir (ornek: 'cp -al' ile alinmis bir yedek).\\n\"\n",
        "B-B5/uyari metni")


# --------------------------------------------------------------- ALTYAPI

def motor_kur(hedef, sabotaj=None, ek_yama=None):
    try:
        os.makedirs(hedef, exist_ok=True)
        metin = open(KAYNAK, encoding="utf-8").read()
        if ek_yama:
            metin = ek_yama(metin)
        if sabotaj:
            metin = sabotaj(metin)
        try:
            import ast as _ast
            _ast.parse(metin)
        except SyntaxError as e:
            # Y-4 dersi: yamalanmis kopya parse edilemiyorsa olculen sey ARAC degil
            # YAMANIN KENDISIDIR. Bu ARAC KUSURUDUR, "KACTI" DEGIL.
            raise SenaryoKurulamadi(
                "yamalanmis motor PARSE EDILEMIYOR (satir %s: %s)" % (e.lineno, e.msg))
        p = os.path.join(hedef, "hafiza.py")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(metin)
        os.chmod(p, os.stat(p).st_mode | stat.S_IWUSR)
    except OSError as e:
        raise SenaryoKurulamadi("motor kurulamadi: %s" % e)
    return p


def kos(motor, arglar, cwd=None, ortam_ek=None, saniye=180):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    o.pop("FAZB_KES", None)
    if ortam_ek:
        o.update(ortam_ek)
    try:
        r = subprocess.run([sys.executable, motor] + arglar,
                           cwd=cwd, capture_output=True, timeout=saniye, env=o)
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or b"").decode("utf-8", "replace") + \
                         (r.stderr or b"").decode("utf-8", "replace")


def proje_kur(motor, kok):
    os.makedirs(kok, exist_ok=True)
    rc, c = kos(motor, ["kur", "--kok=" + kok])
    if rc != 0:
        raise SenaryoKurulamadi("proje kurulamadi (exit=%s): %s" % (rc, c[-300:]))
    return kok


def konular(kok):
    return os.path.join(kok, "KONULAR.md")


def yeni_konu_yaz(motor, kok, konu="fazb-yeni-konu", ortam_ek=None):
    """KONULAR.md'yi yaz() uzerinden YENIDEN YAZDIRAN komut.

    OLCULDU (bu senaryo dosyasinin ilk surumunde ISIRDI): `--yeni-konu` KONULAR.md'yi
    yalnizca konu SOZLUKTE YOKKEN yazar. Ilk surum var olan `genel-durum` konusunu
    veriyordu; dal hic kosmadi ve BES senaryonun besi de sessizce hukumsuz kaldi
    (temiz ve sabotaj kollari AYNI ciktiyi verdi). Konu adi YENI olmak ZORUNDADIR."""
    return kos(motor, ["not", "--kok=" + kok, "--konu=" + konu,
                       "--yeni-konu=Faz B olcum konusu", "--metin=faz B olcum notu"],
               ortam_ek=ortam_ek)


def part_artiklari(kok):
    return [f for f in os.listdir(kok) if f.startswith(".hafiza_yaz_")]


# --------------------------------------------------------------- SENARYOLAR

def s_bb1(taban):
    """B-B1: yazim kesilirse hedef ESKI icerigini KORUYOR mu?"""
    ad = "B-B1 kesilen yazim hedefi YARIM birakmiyor"
    try:
        sonuc = {}
        for kol, sab, enj in (("temiz", None, enj_temiz), ("sabotaj", sab_bb1, None)):
            d = os.path.join(taban, "bb1_" + kol)
            motor = motor_kur(d, sabotaj=sab, ek_yama=enj)
            kok = proje_kur(motor, os.path.join(d, "p"))
            onceki = open(konular(kok), encoding="utf-8").read()
            if not onceki.strip():
                raise SenaryoKurulamadi("KONULAR.md bos kuruldu — olcum dayanagi yok")
            rc, c = yeni_konu_yaz(motor, kok, ortam_ek={"FAZB_KES": "1"})
            sonrasi = open(konular(kok), encoding="utf-8").read()
            sonuc[kol] = (onceki == sonrasi, len(sonrasi), rc,
                          "Traceback" in c, len(part_artiklari(kok)))
    except (SenaryoKurulamadi, OSError) as e:
        kayit(ad, None, "kurulamadi: %s" % e)
        return
    t_ayni, t_n, t_rc, t_tb, t_part = sonuc["temiz"]
    s_ayni, s_n, s_rc, s_tb, s_part = sonuc["sabotaj"]
    isirdi = t_ayni and (not t_tb) and t_part == 0 and (not s_ayni) and s_n == 0
    kayit(ad, isirdi,
          "TEMIZ: icerik korundu=%s (%d bayt) exit=%s ham-traceback=%s .part artigi=%d | "
          "SABOTAJ: korundu=%s (%d bayt) exit=%s"
          % (t_ayni, t_n, t_rc, "VAR" if t_tb else "yok", t_part, s_ayni, s_n, s_rc))


def s_bb2(taban):
    """B-B2: salt-okunur hedefte REDDEDIYOR mu, yoksa izni asiyor mu?"""
    ad = "B-B2 salt-okunur hedefte izin ASILMIYOR"
    if ROOT:
        SINIRLAR.append("B-B2 root olarak kosuldu: os.access 0444'te de True doner, "
                        "izin dali OLCULEMEZ. Root OLMAYAN kullanicida kosulmali.")
        kayit(ad, None, "root (uid 0) — izin dali olculemez")
        return
    try:
        sonuc = {}
        for kol, sab in (("temiz", None), ("sabotaj", sab_bb2)):
            d = os.path.join(taban, "bb2_" + kol)
            motor = motor_kur(d, sabotaj=sab)
            kok = proje_kur(motor, os.path.join(d, "p"))
            hedef = konular(kok)
            onceki = open(hedef, encoding="utf-8").read()
            os.chmod(hedef, 0o444)
            rc, c = yeni_konu_yaz(motor, kok)
            try:
                sonrasi = open(hedef, encoding="utf-8").read()
            except OSError as e:
                raise SenaryoKurulamadi("hedef okunamadi: %s" % e)
            os.chmod(hedef, 0o644)
            sonuc[kol] = (onceki == sonrasi, rc, "SALT-OKUNUR" in c,
                          "CIKIS YOLU" in c, "Traceback" in c)
    except (SenaryoKurulamadi, OSError) as e:
        kayit(ad, None, "kurulamadi: %s" % e)
        return
    t_ayni, t_rc, t_msg, t_yol, t_tb = sonuc["temiz"]
    s_ayni, s_rc, _, _, _ = sonuc["sabotaj"]
    isirdi = t_ayni and t_msg and t_yol and (not t_tb) and t_rc == 2 and (not s_ayni)
    kayit(ad, isirdi,
          "TEMIZ: dosya degismedi=%s exit=%s SALT-OKUNUR=%s CIKIS-YOLU=%s ham-traceback=%s | "
          "SABOTAJ (izin kapisi sokulu): dosya degismedi=%s exit=%s"
          % (t_ayni, t_rc, "VAR" if t_msg else "YOK", "VAR" if t_yol else "YOK",
             "VAR" if t_tb else "yok", s_ayni, s_rc))


def s_bb3(taban):
    """B-B3: hedefin izin bitleri atomik yazimdan SONRA ayni mi?"""
    ad = "B-B3 hedefin izin bitleri korunuyor"
    if os.name == "nt":
        SINIRLAR.append("B-B3 Windows'ta OLCULEMEZ: POSIX mod bitleri tasinmaz.")
        kayit(ad, None, "windows — mod bitleri anlamsiz")
        return
    try:
        sonuc = {}
        for kol, sab in (("temiz", None), ("sabotaj", sab_bb3)):
            d = os.path.join(taban, "bb3_" + kol)
            motor = motor_kur(d, sabotaj=sab)
            kok = proje_kur(motor, os.path.join(d, "p"))
            hedef = konular(kok)
            os.chmod(hedef, 0o640)
            rc, c = yeni_konu_yaz(motor, kok)
            sonuc[kol] = (stat.S_IMODE(os.stat(hedef).st_mode), rc)
    except (SenaryoKurulamadi, OSError) as e:
        kayit(ad, None, "kurulamadi: %s" % e)
        return
    t_mod, t_rc = sonuc["temiz"]
    s_mod, s_rc = sonuc["sabotaj"]
    isirdi = t_mod == 0o640 and s_mod != 0o640 and t_rc == 0
    kayit(ad, isirdi,
          "TEMIZ: 0o640 -> %s exit=%s | SABOTAJ (mod kopyasi sokulu): 0o640 -> %s"
          % (oct(t_mod), t_rc, oct(s_mod)))


def s_bb4(taban):
    """B-B4: basarisiz yazim GECICI DOSYA ARTIGI birakiyor mu?"""
    ad = "B-B4 basarisiz yazim .part artigi birakmiyor"
    try:
        sonuc = {}
        for kol, sab in (("temiz", None), ("sabotaj", sab_bb4)):
            d = os.path.join(taban, "bb4_" + kol)
            motor = motor_kur(d, sabotaj=sab, ek_yama=enj_temiz)
            kok = proje_kur(motor, os.path.join(d, "p"))
            rc, c = yeni_konu_yaz(motor, kok, ortam_ek={"FAZB_KES": "1"})
            sonuc[kol] = (len(part_artiklari(kok)), rc)
    except (SenaryoKurulamadi, OSError) as e:
        kayit(ad, None, "kurulamadi: %s" % e)
        return
    t_n, t_rc = sonuc["temiz"]
    s_n, s_rc = sonuc["sabotaj"]
    isirdi = t_n == 0 and s_n >= 1
    kayit(ad, isirdi,
          "TEMIZ: %d artik exit=%s | SABOTAJ (temizlik sokulu): %d artik exit=%s"
          % (t_n, t_rc, s_n, s_rc))


def s_bb5(taban):
    """B-B5: hardlink UYARISI ile GERCEK DAVRANIS ayni seyi mi soyluyor?

    Olculen sey bir metin degil, METIN ILE DAVRANISIN TUTARLILIGIDIR: os.replace
    bagi KOPARIR; uyari bunu soylemiyorsa belge yalan soyluyordur (CLAUDE.md:
    "belge de bir arayuzdur ve yalan soyleyebilir")."""
    ad = "B-B5 hardlink uyarisi GERCEGI soyluyor"
    if not hasattr(os, "link"):
        SINIRLAR.append("B-B5 OLCULEMEDI: os.link bu platformda yok.")
        kayit(ad, None, "os.link yok")
        return
    try:
        sonuc = {}
        for kol, sab in (("temiz", None), ("sabotaj", sab_bb5)):
            d = os.path.join(taban, "bb5_" + kol)
            motor = motor_kur(d, sabotaj=sab)
            kok = proje_kur(motor, os.path.join(d, "p"))
            hedef = konular(kok)
            onceki = open(hedef, encoding="utf-8").read()
            dis = os.path.join(d, "disarideki_ad.md")     # proje AGACININ DISINDA
            try:
                os.link(hedef, dis)
            except (OSError, NotImplementedError) as e:
                raise SenaryoKurulamadi("hardlink kurulamadi: %s" % e)
            rc, c = yeni_konu_yaz(motor, kok)
            dis_icerik = open(dis, encoding="utf-8").read()
            ic_icerik = open(hedef, encoding="utf-8").read()
            bag_koptu = (dis_icerik == onceki) and (ic_icerik != onceki)
            metin_kopmayi_soyluyor = ("BAG KOPAR" in c) or ("ESKI icerikte KALIR" in c)
            metin_yansimayi_soyluyor = "oradaki adi da degistirir" in c
            sonuc[kol] = (bag_koptu, metin_kopmayi_soyluyor,
                          metin_yansimayi_soyluyor, rc, "hardlink" in c)
    except (SenaryoKurulamadi, OSError) as e:
        kayit(ad, None, "kurulamadi: %s" % e)
        return
    t_kop, t_dogru, t_yanlis, t_rc, t_uyari = sonuc["temiz"]
    s_kop, s_dogru, s_yanlis, s_rc, s_uyari = sonuc["sabotaj"]
    # TEMIZ: bag kopar VE metin kopmayi soyler.  SABOTAJ: bag yine kopar ama metin
    # "yansir" der -> TUTARSIZ. Ikisi de gorulmezse senaryo hukum vermiyor demektir.
    isirdi = (t_kop and t_dogru and not t_yanlis and t_uyari
              and s_kop and s_yanlis and not s_dogru)
    kayit(ad, isirdi,
          "TEMIZ: bag koptu=%s metin 'KOPAR' diyor=%s uyari basildi=%s exit=%s | "
          "SABOTAJ (eski metin): bag koptu=%s metin 'yansir' diyor=%s"
          % (t_kop, t_dogru, t_uyari, t_rc, s_kop, s_yanlis))


# --------------------------------------------------------------- RAPOR

def main():
    print("=" * 82)
    print("FAZ B SENARYOLARI — yaz() atomiklestirmesi ISIRIYOR mu?")
    print("  python : %s" % sys.version.split()[0])
    print("  motor  : %s" % KAYNAK)
    print("  uid    : %s" % ("root (0)" if ROOT else "root DEGIL"))
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="fazB_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        for f in (s_bb1, s_bb2, s_bb3, s_bb4, s_bb5):
            f(taban)
        print()
        isiran = kacan = olculemeyen = 0
        for ad, isirdi, ayrinti in SONUC:
            if isirdi is None:
                d = "OLCULEMEDI"; olculemeyen += 1
            elif isirdi:
                d = "ISIRDI    "; isiran += 1
            else:
                d = "KACTI     "; kacan += 1
            print("  %s %-46s | %s" % (d, ad, ayrinti))
        SINIRLAR.append(
            "DIZIN GIRDISI fsync'LENMEZ: surec cokmesi ve yarim yazim OLCULDU (B-B1), "
            "ani GUC KESINTISINDE adin kaybi OLCULMEDI. 'Kapandi' DENMEZ.")
        SINIRLAR.append(
            "Append yazimlari (_ZINCIR.jsonl, canli hafiza, tasinma defteri) Faz B "
            "KAPSAMI DISINDADIR; atomik DEGILDIR ve bu tur OLCULMEDI.")
        print()
        print("OLCUMUN SINIRI (hukum degil):")
        for n in SINIRLAR:
            print("  - %s" % n)
        print()
        print("-" * 82)
        print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)"
              % (isiran, kacan, olculemeyen, len(SONUC)))
        if kacan:
            return 1
        if olculemeyen:
            return 2
        return 0
    finally:
        for kk, dd, ff in os.walk(taban):
            for x in dd + ff:
                try:
                    os.chmod(os.path.join(kk, x), 0o755)
                except OSError:
                    pass
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

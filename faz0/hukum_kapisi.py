#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HUKUM KAPISI — "kosucu hukmunu BASTI mi?" (yesil tike anlam iade eder)

NEYI OLCER — VE NEYI OLCMEZ
  OLCER : beklenen hukum satirlarinin ciktida VAR olup olmadigini.
  OLCMEZ: o hukumlerin yesil olup olmadigini. Bu ayrim bilinclidir.
          Bu kapinin yakaladigi sinif "hukum KAYBOLDU"dur, "hukum kirmizi" degil.

NEDEN VAR (Y-2, olculdu: CI run #2)
  capraz.yml'de her adim `continue-on-error: true` ile kosuyordu (Faz 0'da
  bilerek). windows-latest py3.11 ve py3.13'te t_y42 58 senaryonun TAMAMINI
  kostu, sonra rapor dongusunun ILK satirinda UnicodeEncodeError ile coktu ve
  58 hukmun tamami basilmadan kayboldu. GitHub bunu yuttu: is YESIL gorundu,
  API'de adimin `conclusion` alani bile "success" dondu (continue-on-error
  gercek sonucu `outcome`ta saklar). Yani capraz olcumun 1/3'u kordu ve bu
  korluk YESIL TIK olarak raporlaniyordu.

  Bu kapi `continue-on-error` OLMADAN kosar. Bir kosucunun hukmu kaybolursa is
  KIRMIZI olur. Faz 0'in "olc, duzeltme" bayragi digersadimlarda kalabilir;
  hukmun VARLIGI pazarlik konusu degildir.

BEKLENEN HUKUMLER
  t_y3   : SONUC: 20/20 senaryo TEMIZ HATA veriyor
  isir(1): SONUC: 79/79 kosulan mutant ISIRIYOR      (derle ONCESI)
  isir(2): SONUC: 81/81 kosulan mutant ISIRIYOR      (derle SONRASI)
  t_y42  : SONUC: N gecti - M kaldi - K olculemedi
  Desenler kasten ASCII'dir: koruma `errors="replace"` ile devreye girdiginde
  '-' ayraci '?' olarak basilabilir; kapi bu yuzden ayracin kendisine bakmaz.

KANIT KOLLARI (`--kanit`, Y1, Onur kilidi 4 Eki 2026) — `kapi`nin KENDI hukmu
  Bu kapi yukarida kosucularin hukmunun BASILIP basilmadigina bakar. `kapi` komutunun
  KENDI hukmu de sessiz yalan soyleyebiliyordu (olculdu 29 Eyl,
  OLCUM_RAPORU_29EYL_KALAN18_ERISIM.md §3): bir `fail()` basligi olurse
    Y1  erken donus (H6 `HAFIZA DIZINI YOK` / H- `CANLI HAFIZA YOK`) "hicbir kapi
        kosmadi" demesine ragmen hukum duz `YESIL` ciktisi veriyordu (exit 0).
  Her vaka icin UC parca (log gerekmez, `--kanit` tek basina kosar):
    POZITIF KONTROL : sabotajsiz motor + vaka -> ESKI davranis (FAIL, etiketli, SONUC
                      satiri eskisiyle ayni bicimde).
    KOL             : basligi `None` yapilmis motor (faz0/sabotaj.py'nin yontemi) + ayni
                      vaka -> `YESIL (SINIRLI)` exit 0, `--kapsam-zorla` exit 5.
    MUTANT          : duzeltmenin KENDISI sokulur (`O.append` satiri) -> ayni vaka eski
                      belirtiyi gostermeli (duz `YESIL`), yani KOL bu mutanti GORUR
                      (ISIRDI).
  Vakalar: Y1-a canli hafiza silinmis (H- basligi `None`) · Y1-b hafiza dizini silinmis
  (H6 basligi `None`).

KULLANIM
  python3 faz0/hukum_kapisi.py hukum.log
  python3 faz0/hukum_kapisi.py hukum.log --bekle=t_y3,isir1,isir2,t_y42
  python3 faz0/hukum_kapisi.py --kanit

CIKIS KODLARI
  0  beklenen her hukum BASILDI  (--kanit: her satir BEKLENDIGI GIBI)
  1  en az bir hukum KAYIP -> olcum kayboldu, is KIRMIZI  (--kanit: BEKLENMEDIK)
  2  kullanim hatasi / log okunamadi  (--kanit: OLCULEMEDI / ARAC KUSURU)
"""
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

BEKLENEN = [
    ("t_y3", "t_y3   — 20 temiz hata senaryosu",
     re.compile(r"^SONUC: 20/20 senaryo TEMIZ HATA", re.M)),
    ("isir1", "isir   — derle ONCESI mutant kosumu",
     re.compile(r"^SONUC: 79/79 kosulan mutant ISIRIYOR", re.M)),
    ("isir2", "isir   — derle SONRASI TAM kosum",
     re.compile(r"^SONUC: 81/81 kosulan mutant ISIRIYOR", re.M)),
    ("t_y42", "t_y42  — 58 davranis senaryosu",
     re.compile(r"^SONUC: \d+ gecti", re.M)),
]


def main(argv):
    if "--kanit" in argv[1:]:
        return kanit_main()
    if len(argv) < 2:
        print("kullanim: hukum_kapisi.py <log dosyasi> [--bekle=a,b,c]  |  hukum_kapisi.py --kanit")
        return 2
    p = argv[1]
    istenen = None
    for a in argv[2:]:
        if a.startswith("--bekle="):
            istenen = {s.strip() for s in a.split("=", 1)[1].split(",") if s.strip()}
    if not os.path.isfile(p):
        print("HUKUM KAPISI: log dosyasi YOK: %s" % p)
        print("  Bu da bir kayiptir: kosucular hic kosmamis ya da cikti hic yakalanmamis.")
        return 1
    with open(p, encoding="utf-8", errors="replace") as f:
        metin = f.read()

    print("=" * 78)
    print("HUKUM KAPISI — kosucular hukmunu BASTI mi?")
    print("  log      : %s (%d bayt)" % (p, len(metin.encode("utf-8", "replace"))))
    print("=" * 78)

    kayip = []
    for anahtar, ad, desen in BEKLENEN:
        if istenen is not None and anahtar not in istenen:
            print("  ATLANDI    %-38s | --bekle listesinde yok" % ad)
            continue
        m = desen.search(metin)
        if m:
            satir = metin[m.start():metin.find("\n", m.start())
                          if metin.find("\n", m.start()) != -1 else len(metin)]
            print("  BASILDI    %-38s | %s" % (ad, satir.strip()[:60]))
        else:
            print("  KAYIP      %-38s | hukum satiri ciktida YOK" % ad)
            kayip.append(ad)

    print("-" * 78)
    if kayip:
        print("SONUC: %d HUKUM KAYIP — olcum kayboldu, is KIRMIZI." % len(kayip))
        print("  Kaybolan bir hukum 'gecti' DEGILDIR; 'olculemedi'dir (doktrin 2).")
        print("  Ilk bakilacak yer: UnicodeEncodeError (Y-2 sinifi) ve zaman asimi.")
        return 1
    print("SONUC: beklenen her hukum BASILDI.")
    print("  NOT: bu kapi hukumlerin YESIL oldugunu SOYLEMEZ, sadece KAYBOLMADIGINI.")
    return 0


# ----------------------------------------------------------------------------
# KANIT KOLLARI (--kanit) — Y1 / Y2 · yukaridaki kosucu-hukum denetiminden BAGIMSIZ
# ----------------------------------------------------------------------------
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
_TIRE = chr(0x2014)

# Motorun Y1/Y2 satirlari — MUTANT bunlari sokucu; hedef motorda TAM 1 kez gecmeli
# (gecmezse ARAC KUSURU: motor degistiyse SABOTAJ DA DEGISMELIDIR).
_Y1_H6 = ('        O.append("KAPILAR KOSMADI: arsiv dizini cozulemedi (erken donus) ' + _TIRE
          + ' sonraki tum kapilar OLCULMEDI")\n')
_Y1_H = ('        O.append("KAPILAR KOSMADI: canli hafiza dosyasi cozulemedi (erken donus) '
         + _TIRE + ' sonraki tum kapilar OLCULMEDI")\n')

_ESKI_SONUC = re.compile(r"^SONUC: FAIL \(\d+ bulgu\)$")


class AracKusuru(Exception):
    """Kanit duzenegi kurulamadi (hedef dizge/cagri bulunamadi). Kapi hukmu DEGIL."""


class Kurulamadi(Exception):
    """Bu platformda vaka kurulamiyor (ornegin hardlink). Kapi hukmu DEGIL."""


def _fail_cagrisi(kaynak, fonksiyon, etiket, parca=None):
    """`fonksiyon` icindeki TEK `fail(<etiket>, ...)` cagrisinin konumu (ast: kolonlar
    UTF-8 BAYT ofsetidir). `parca` verilirse mesaj sabitlerinden biri onu icermeli."""
    bulunan = []
    for fn in ast.walk(ast.parse(kaynak)):
        if not (isinstance(fn, ast.FunctionDef) and fn.name == fonksiyon):
            continue
        for c in ast.walk(fn):
            if not (isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                    and c.func.id == "fail" and c.args
                    and isinstance(c.args[0], ast.Constant) and c.args[0].value == etiket):
                continue
            sabitler = [n.value for a in c.args[1:] for n in ast.walk(a)
                        if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            if parca is None or any(parca in s for s in sabitler):
                bulunan.append(c)
    if len(bulunan) != 1:
        raise AracKusuru("%s icinde fail(%r%s) %d kez gecti (1 olmali)"
                         % (fonksiyon, etiket, "" if parca is None else ", ..%s.." % parca,
                            len(bulunan)))
    c = bulunan[0]
    return c.lineno, c.col_offset, c.end_lineno, c.end_col_offset


def _baslik_oldur(kaynak, konum):
    """faz0/sabotaj.py `sabote_et`in yontemi: fail(...) cagrisi `None` olur."""
    ls, col, le, ecol = konum
    L = kaynak.split("\n")
    bas = L[ls - 1].encode("utf-8")[:col].decode("utf-8")
    kuyruk = L[le - 1].encode("utf-8")[ecol:].decode("utf-8")
    L[ls - 1:le] = [bas + "None" + kuyruk]
    yeni = "\n".join(L)
    compile(yeni, "<kanit-sabotaj>", "exec")
    return yeni


def _degistir(kaynak, hedef, yerine, ad):
    n = kaynak.count(hedef)
    if n != 1:
        raise AracKusuru("%s: hedef dizge %d kez gecti (1 olmali) — motor degistiyse SABOTAJ DA "
                         "DEGISMELIDIR: %r" % (ad, n, hedef.strip()[:60]))
    yeni = kaynak.replace(hedef, yerine, 1)
    compile(yeni, "<kanit-mutant>", "exec")
    return yeni


def _yaz(yol, metin):
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return yol


def _kos(motor, arglar, kok):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok=" + kok],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=300, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _sonuc_satiri(c):
    s = re.findall(r"^SONUC: .*$", c, re.M)
    return s[-1] if s else "(SONUC satiri YOK)"


def _sablon(gecici):
    p = os.path.join(gecici, "sablon")
    os.makedirs(p)
    for arglar in (["kur", "--ad", "KANIT"],
                   ["not", "--konu=genel-durum", "--metin=hukum kanit sablonu"],
                   ["derle"]):
        rc, c = _kos(MOTOR, arglar, p)
        if rc != 0:
            raise AracKusuru("sablon proje kurulamadi (%s exit=%s): %s" % (arglar[0], rc, c[-200:]))
    rc, c = _kos(MOTOR, ["kapi"], p)
    if rc != 0:
        raise AracKusuru("sablon proje `kapi`yi gecmiyor (exit=%s): %s" % (rc, _sonuc_satiri(c)))
    return p


def _canli(p):
    return os.path.join(p, "PROJE_HAFIZA.md")


def _s_canli_sil(p):
    os.remove(_canli(p))


def _s_dizin_sil(p):
    shutil.rmtree(os.path.join(p, "arsiv", "hafiza"))


# (ad, vaka kurucu, fonksiyon, fail etiketi, mesaj parcasi, tur, MUTANTIN sokecegi satir)
KANIT_VAKALARI = [
    ("Y1-a canli hafiza SILINMIS", _s_canli_sil, "_kapi_govde", "H-", None, "y1", _Y1_H),
    ("Y1-b hafiza DIZINI silinmis", _s_dizin_sil, "_kapi_govde", "H6", None, "y1", _Y1_H6),
]


def _proje(yer, ad, sablon, kurucu):
    p = os.path.join(yer, ad)
    shutil.copytree(sablon, p)
    kurucu(p)
    return p


def _pozitif_tamam(etiket, rc, c):
    s = _sonuc_satiri(c)
    return rc == 1 and ("[%s]" % etiket) in c and bool(_ESKI_SONUC.match(s))


def _kol_tamam(tur, motor, p):
    """Duzeltilmis motor + basligi `None` vaka: (tamam, eski_belirti, ayrinti)."""
    rc, c = _kos(motor, ["kapi"], p)
    s = _sonuc_satiri(c)
    rz, _ = _kos(motor, ["kapi", "--kapsam-zorla"], p)
    tamam = (rc == 0 and s.startswith("SONUC: YESIL (SINIRLI)") and "KAPILAR KOSMADI" in c
             and rz == 5)
    eski = rc == 0 and s.startswith("SONUC: YESIL ") and "SINIRLI" not in s
    return tamam, eski, "exit=%s/%s · %s" % (rc, rz, s[:70])


def _vaka(gecici, sablon, kaynak, vaka):
    ad, kurucu, fonk, etiket, parca, tur, hedef = vaka
    yer = os.path.join(gecici, re.sub(r"\W", "_", ad))
    os.makedirs(yer)
    try:
        p = _proje(yer, "pozitif", sablon, kurucu)
    except Kurulamadi as e:
        return [(ad + " / POZITIF KONTROL", OLCULEMEDI, str(e)),
                (ad + " / KOL", OLCULEMEDI, str(e)),
                (ad + " / MUTANT", OLCULEMEDI, str(e))]
    satir = []
    # 1) POZITIF KONTROL — sabotajsiz motor: eski davranis, etiketli, SONUC bicimi ayni
    rc, c = _kos(MOTOR, ["kapi"], p)
    if _pozitif_tamam(etiket, rc, c):
        satir.append((ad + " / POZITIF KONTROL", BEKLENDIGI_GIBI,
                      "exit=%s · [%s] etiketli · %s" % (rc, etiket, _sonuc_satiri(c)[:48])))
    else:
        satir.append((ad + " / POZITIF KONTROL", BEKLENMEDIK,
                      "sabotajsiz motorda beklenen eski davranis YOK: exit=%s · %s"
                      % (rc, _sonuc_satiri(c)[:70])))
    # 2) KOL — basligi None motor
    sab = _baslik_oldur(kaynak, _fail_cagrisi(kaynak, fonk, etiket, parca))
    m_kol = _yaz(os.path.join(yer, "kol.py"), sab)
    tamam, _, ayr = _kol_tamam(tur, m_kol, _proje(yer, "kol", sablon, kurucu))
    satir.append((ad + " / KOL", BEKLENDIGI_GIBI if tamam else BEKLENMEDIK,
                  ayr if tamam else "duzeltme belirtisi YOK: " + ayr))
    # 3) MUTANT — duzeltmenin kendisi sokulur: KOL bunu GORMELI
    mut = _degistir(sab, hedef, "", ad)
    m_mut = _yaz(os.path.join(yer, "mutant.py"), mut)
    tamam, eski, ayr = _kol_tamam(tur, m_mut, _proje(yer, "mutant", sablon, kurucu))
    if tamam:
        satir.append((ad + " / MUTANT", BEKLENMEDIK, "KACTI: duzeltme sokulunce de KOL tamam — " + ayr))
    elif eski:
        satir.append((ad + " / MUTANT", BEKLENDIGI_GIBI, "ISIRDI: eski belirti geri geldi — " + ayr))
    else:
        satir.append((ad + " / MUTANT", OLCULEMEDI, "ne duzeltme ne eski belirti: " + ayr))
    return satir


def kanit_main():
    if not os.path.isfile(MOTOR):
        print("KANIT: motor YOK: %s" % MOTOR)
        return 2
    gecici = tempfile.mkdtemp(prefix="hukumkanit_")
    kayit = []
    try:
        try:
            with open(MOTOR, encoding="utf-8", newline="") as f:
                kaynak = f.read()
            sablon = _sablon(gecici)
            for vaka in KANIT_VAKALARI:
                kayit.extend(_vaka(gecici, sablon, kaynak, vaka))
        except AracKusuru as e:
            print("ARAC KUSURU (OLCULEMEDI, kapi hukmu DEGIL): %s" % e)
            return 2
        except subprocess.TimeoutExpired as e:
            print("OLCULEMEDI: zaman asimi: %s" % e)
            return 2
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    print("=" * 78)
    print("HUKUM KAPISI --kanit — `kapi`nin KENDI hukmu (Y1: erken donus)")
    print("=" * 78)
    for ad, durum, ayr in kayit:
        print("  %-44s %-16s %s" % (ad, durum, ayr))
    print("-" * 78)
    bek = sum(1 for _, d, _ in kayit if d == BEKLENDIGI_GIBI)
    print("SONUC: %d/%d satir BEKLENDIGI GIBI" % (bek, len(kayit)))
    if any(d == BEKLENMEDIK for _, d, _ in kayit):
        return 1
    if any(d == OLCULEMEDI for _, d, _ in kayit):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — SABIT TARIH DESEN YASAGI (Cowork is emri "ayrisma FIKSTUR ZAMAN BOMBASI",
KALEM 2 — 26 Eyl 2026).

NEDEN VAR (UCUNCU ISIRIK)
  Bir olcum fiksturune `Son guncelleme: <sabit tarih>` yazmak bir ZAMAN BOMBASIDIR:
  H12'nin bayatlik tavani (30 gun) doldugu gun, fikstur KENDI senaryosu yuzunden
  kirmizi yanar ve kapinin olcmek istedigi eksen yerine TAKVIMI olcer. Olculdu:
  faz0/ayrisma_mutanti.py'nin A2 fiksturu 2026-08-15 tasiyordu, 14 Eyl'de patladi
  (ayrisma_kapisi uc platformda push'ta KIRMIZI olacakti). Fikstur artik tarihini
  kosum anindan turetiyor; bu kapi sinifi MEKANIK olarak yasaklar.

NE OLCER — DESEN YASAGI, BAYATLIK OLCUMU DEGIL
  faz0/ ve skill/scripts/ altindaki KOSAN dosyalarda (*.py, *.sh) bir dize
  sabitinin icinde `Son guncelleme: <tarih>` (H12'nin cozdugu bicimler: YYYY-AA-GG
  · GG.AA.YYYY · GG/AA/YYYY · "G Ay YYYY") bulunursa KIRMIZI. Zamana HIC bakmaz:
  "N gunden eski" karsilastirmasi YAPMAZ (6 Eyl'de olculdu — "capa son kosumdan
  eskiyse kirmizi" olcutu SONSUZ KIRMIZI veriyordu). Sabit tarih BUGUN taze de
  olsa yasaktir, cunku yarin taze olmayacaktir.
  *.py dosyalari AST ile taranir: YALNIZ kod dize sabitleri (f-dize parcalari
  dahil); YORUMLAR ve DOCSTRING'LER haric — ham metin taramasi hafiza.py'deki
  bir yorumda (sat. ~250, H12 kisaltma korlugunun tarihcesi) SAHTE kirmizi
  verirdi (olculdu; yol_ayraci_kapisi'nin "yorum ile kodu ayirt etmiyor" sinifi).
  *.sh dosyalarinda `#` ile baslayan satirlar atlanir.

KOLLAR
  KAPI-1  gercek agac: hic bulgu YOK, hic OLCULEMEDI YOK
  KAPI-YP YANLIS POZITIF: ayni tarih YORUMDA ve DOCSTRING'de -> bulgu YOK
MUTANTLAR (agacin kopyasina; her biri KENDI dosyasinda yakalanmali)
  M-1  ayrisma fiksturune sabit tarih GERI konur (a4cb48f4'teki blok birebir)
  M-2  skill/scripts'te f-dize icinde GG.AA.YYYY
  M-3  faz0'da "Son güncelleme: G Ay YYYY" (Turkce harf + ay kisaltmasi)
  M-4  *.sh dosyasinda yorum OLMAYAN satirda

NE OLCMEZ (gizlenmez)
  1. Tarih bir DEGISKENDEN gelirse (`x = "2026-08-15"` sonra `"... %s" % x`) bu
     kapi GORMEZ: bu bir desen yasagidir, veri akisi analizi degil.
  2. Blok `guncel="..."` ozniteligi taranmaz: H12 baslik satirini okur; t_y42 ve
     h10_bolme_mutanti bu ozniteligi sabit tasir ve yesildir (Cowork olcumu).
  3. *.md / *.json dosyalari (kosmayan belge ve veri) taranmaz.

CIKIS KODLARI
  0  KAPI-1 ve KAPI-YP temiz, 4/4 mutant KENDI dosyasinda yakalandi
  1  gercek agacta sabit tarih VAR · YP kolu yandi · bir mutant KACTI
  2  OLCULEMEDI (dosya okunamadi/ayristirilamadi, mutant kurulamadi)

KULLANIM
  python faz0/sabit_tarih_mutanti.py [taranacak_kok]
  POZITIF KONTROL: a4cb48f4 agaci verilince KAPI-1 faz0/ayrisma_mutanti.py'de
  KIRMIZI yanar (olculdu, commit mesajinda).
"""
import ast
import io
import os
import re
import shutil
import sys
import tempfile


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


VARSAYILAN_KOK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KOKLER = ("faz0", "skill/scripts")
UZANTILAR = (".py", ".sh")

# H12'nin (tarih_coz) cozdugu bicimler; ay adi harfle (Turkce dahil) yazilir.
DESEN = re.compile(r"Son\s+g[uü]ncelleme\s*:\s*"
                   r"(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[./]\d{1,2}[./]\d{4}"
                   r"|\d{1,2}\s+[^\W\d_]+\.?\s+\d{4})", re.I)


class Olculemedi(Exception):
    """Dosya okunamadi / ayristirilamadi — sessizce ATLANMAZ."""


def _docstring_dugumleri(agac):
    ids = set()
    for n in ast.walk(agac):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if (n.body and isinstance(n.body[0], ast.Expr)
                    and isinstance(n.body[0].value, ast.Constant)
                    and isinstance(n.body[0].value.value, str)):
                ids.add(id(n.body[0].value))
    return ids


def py_bulgulari(metin, ad):
    try:
        agac = ast.parse(metin, filename=ad)
    except SyntaxError as e:
        raise Olculemedi("%s ayristirilamadi: %s" % (ad, e))
    doc = _docstring_dugumleri(agac)
    out = []
    for n in ast.walk(agac):
        if not isinstance(n, ast.Constant) or id(n) in doc:
            continue
        v = n.value
        if isinstance(v, bytes):
            v = v.decode("utf-8", "replace")
        if isinstance(v, str):
            m = DESEN.search(v)
            if m:
                out.append((n.lineno, m.group(0)))
    return out


def sh_bulgulari(metin):
    out = []
    for i, s in enumerate(metin.split("\n"), 1):
        if s.lstrip().startswith("#"):
            continue
        m = DESEN.search(s)
        if m:
            out.append((i, m.group(0)))
    return out


def dosyalar(kok):
    for d in KOKLER:
        tam = os.path.join(kok, *d.split("/"))
        if not os.path.isdir(tam):
            raise Olculemedi("taranacak dizin YOK: %s" % tam)
        for f in sorted(os.listdir(tam)):
            if f.endswith(UZANTILAR) and os.path.isfile(os.path.join(tam, f)):
                yield d + "/" + f, os.path.join(tam, f)


def tara(kok):
    """Doner: ([(goreli_yol, satir, eslesme)], [olculemeyen])."""
    bulgu, olcmeyen, n = [], [], 0
    for rel, p in dosyalar(kok):
        n += 1
        try:
            metin = io.open(p, encoding="utf-8", newline="").read()
        except (OSError, UnicodeDecodeError) as e:
            olcmeyen.append("%s okunamadi: %s" % (rel, e))
            continue
        try:
            b = py_bulgulari(metin, rel) if rel.endswith(".py") else sh_bulgulari(metin)
        except Olculemedi as e:
            olcmeyen.append(str(e))
            continue
        bulgu += [(rel, s, m) for s, m in b]
    if n == 0:
        olcmeyen.append("taranacak KOSAN dosya bulunamadi (%s)" % ", ".join(KOKLER))
    return bulgu, olcmeyen


# ================================================================= MUTANTLAR
# Sabit tarihler kosumda KURULUR: bu dosyanin KENDI kaynaginda desen gecmez
# (kapi kendi dosyasini da tarar).

def _t(*p):
    return "-".join(p)


_BASLIK = "Son guncelleme: "
_M1_YENI_BLOK = (
    '_FIKSTUR_TARIHI = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()\n'
    'ESKI_DEFTER = (("# Eski Proje\\n> Son guncelleme: %s\\n\\n## GUNCEL DURUM\\n"\n'
    '                \'<!-- blok konu="genel-durum" guncel="%s" kaynak="-" -->\\n\'\n'
    '                "- eski defterden gelen satir\\n<!-- /blok -->\\n\\n## ARSIV DIZINI\\n")\n'
    '               % (_FIKSTUR_TARIHI, _FIKSTUR_TARIHI))\n')


def _m1_eski_blok():
    t = _t("2026", "08", "15")
    return ('ESKI_DEFTER = ("# Eski Proje\\n> ' + _BASLIK + t + '\\n\\n## GUNCEL DURUM\\n"\n'
            '               \'<!-- blok konu="genel-durum" guncel="' + t + '" kaynak="-" -->\\n\'\n'
            '               "- eski defterden gelen satir\\n<!-- /blok -->\\n\\n## ARSIV DIZINI\\n")\n')


def m1_ayrisma_geri(metin):
    n = metin.count(_M1_YENI_BLOK)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [M-1]\n" % n)
        return None
    return metin.replace(_M1_YENI_BLOK, _m1_eski_blok(), 1)


def m2_fdize(metin):
    return metin + '\n_BOMBA = f"> %s%s · {__name__}"\n' % (_BASLIK, ".".join(("15", "08", "2026")))


def m3_turkce_ay(metin):
    return metin + '\n_BOMBA = "> Son g%sncelleme: 15 A%su 2026 · x"\n' % ("ü", "ğ")


def m4_sh(metin):
    return metin + '\necho "%s%s" > /dev/null\n' % (_BASLIK, _t("2026", "08", "15"))


MUTANTLAR = [
    ("M-1  ayrisma fiksturune sabit tarih GERI", "faz0/ayrisma_mutanti.py", m1_ayrisma_geri),
    ("M-2  skill/scripts f-dize GG.AA.YYYY", "skill/scripts/t_y42.py", m2_fdize),
    ("M-3  faz0 'Son güncelleme: G Ay YYYY'", "faz0/tarih_kisaltma_mutanti.py", m3_turkce_ay),
    ("M-4  *.sh yorum olmayan satir", "faz0/ortam_olcum.sh", m4_sh),
]


def yp_yorum_docstring(metin):
    """YANLIS POZITIF KOLU: ayni desen YORUMDA ve DOCSTRING'de -> bulgu OLMAMALI."""
    t = _t("2026", "08", "15")
    return (metin + "\n# ornek yorum: > " + _BASLIK + t + "\n"
            "def _yp_ornek():\n    \"\"\"Ornek docstring: > " + _BASLIK + t + "\"\"\"\n"
            "    return 0\n")


# ===================================================================== main

def _kopya(kok):
    d = tempfile.mkdtemp(prefix="sabit_tarih_")
    for rel, p in dosyalar(kok):
        hedef = os.path.join(d, *rel.split("/"))
        os.makedirs(os.path.dirname(hedef), exist_ok=True)
        shutil.copyfile(p, hedef)
    return d


def _kopyada_tara(kok, rel, fn):
    """Doner: (hedef dosyadaki bulgular | None, aciklama)."""
    d = _kopya(kok)
    try:
        p = os.path.join(d, *rel.split("/"))
        if not os.path.isfile(p):
            return None, "hedef dosya YOK: %s" % rel
        metin = io.open(p, encoding="utf-8", newline="").read()
        yeni = fn(metin)
        if yeni is None or yeni == metin:
            return None, "mutant KURULAMADI (capa)"
        with io.open(p, "w", encoding="utf-8", newline="") as f:
            f.write(yeni)
        bulgu, olcmeyen = tara(d)
        if olcmeyen:
            return None, "; ".join(olcmeyen)[:200]
        return [b for b in bulgu if b[0] == rel], ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    _cikti_kodlamasini_guvenceye_al()
    kok = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_KOK
    print("=== SABIT TARIH DESEN YASAGI === kok: %s · platform: %s" % (kok, sys.platform))
    try:
        bulgu, olcmeyen = tara(kok)
    except Olculemedi as e:
        print("SONUC: OLCULEMEDI — %s" % e)
        return 2
    n = sum(1 for _ in dosyalar(kok))
    print("  taranan KOSAN dosya: %d (%s · %s)" % (n, " + ".join(KOKLER), "/".join(UZANTILAR)))
    kirmizi = 0
    olculemeyen = len(olcmeyen)
    if bulgu:
        kirmizi += 1
        print("  KAPI-1  : KIRMIZI — %d sabit tarih (ZAMAN BOMBASI):" % len(bulgu))
        for rel, s, m in bulgu:
            print("      - %s:%d  %r" % (rel, s, m))
    else:
        print("  KAPI-1  : YESIL (kod dize sabitlerinde sabit `Son guncelleme` tarihi YOK)")
    for x in olcmeyen:
        print("      ! OLCULEMEDI — %s" % x)

    yp, aciklama = _kopyada_tara(kok, "faz0/ayrisma_mutanti.py", yp_yorum_docstring)
    if yp is None:
        print("  KAPI-YP : OLCULEMEDI (%s)" % aciklama)
        olculemeyen += 1
    elif yp and not [b for b in bulgu if b[0] == "faz0/ayrisma_mutanti.py"]:
        print("  KAPI-YP : KIRMIZI — yorum/docstring BULGU sayildi: %s" % yp)
        kirmizi += 1
    elif yp:
        print("  KAPI-YP : OLCULEMEDI (hedef dosya zaten bulgu tasiyor; ayrim olculemez)")
        olculemeyen += 1
    else:
        print("  KAPI-YP : YESIL (yorumdaki ve docstring'deki tarih bulgu DEGIL)")

    print("\n--- MUTANT SINAMASI (her biri KENDI dosyasinda yakalanmali) ---")
    kacan = 0
    for ad, rel, fn in MUTANTLAR:
        b, aciklama = _kopyada_tara(kok, rel, fn)
        if b is None:
            print("  %-42s -> OLCULEMEDI (%s)" % (ad, aciklama))
            olculemeyen += 1
        elif b:
            print("  %-42s -> ISIRDI (%s:%d)" % (ad, rel, b[0][1]))
        else:
            print("  %-42s -> KACTI (%s taranmadi ya da desen kor)" % (ad, rel))
            kacan += 1

    print()
    if kirmizi or kacan:
        print("SONUC: KIRMIZI — %d kapi kolu kirmizi, %d mutant KACTI." % (kirmizi, kacan))
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem olculemedi; sessiz PASS verilmez." % olculemeyen)
        return 2
    print("SONUC: YESIL — sabit tarih YOK, YP kolu temiz, %d/%d mutant ISIRDI."
          % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

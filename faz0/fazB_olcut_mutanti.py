#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ B OLCUT MUTANTI — §5 duzeltmesi (B-B2'nin ikiye bolunmesi) ISIRIYOR MU?

NEDEN BU DOSYA VAR
  CI #9'da fazB_senaryolari.py windows'ta "KACTI" dedi; urun kusursuzdu. Bunu
  UYGULANMAZ sinifi kapatti. Ama artefakt elle okununca asil kusurun SINIFTA
  degil OLCUTTE oldugu gorundu: eski B-B2 kapinin IKI vaadini tek olcuye
  sikistiriyordu ve Windows'ta o olcut KORDU.

  Duzeltme B-B2'yi ikiye bolmek oldu. Fakat DOKTRIN 1 aciktir: "olculmeyen
  kapinin hukmu YOKTUR". Bir OLCUT duzeltmesi de bir kapidir ve isirdigi
  KANITLANMALIDIR. Sorun sudur: yeni olcutun katkisi YALNIZ Windows benzeri bir
  ortamda gorunur — POSIX'te eski olcut de ISIRDI der, yani duzeltme burada
  KENDI KORLUGUNU tekrarlar.

  Bu yuzden mutant ORTAMI URETIR: os.replace'in salt-okunur hedefin uzerine
  yazmayi REDDETTIGI bir motor kopyasi (Windows'un olculmus davranisi) POSIX'te
  enjekte edilir. O ortamda:
      ESKI OLCUT ("dosya DEGISTI mi")      -> sabotaj kusur uretemez -> UYGULANMAZ
      YENI OLCUT ("TESHIS SINIFI degisti mi") -> sinif duser        -> ISIRDI
  Ikisi AYNI hukmu veriyorsa duzeltme KORDUR ve mutant KACTI der.

  🔴 URETILEN ORTAM GERCEK WINDOWS DEGILDIR. Burada olculen sey "hafiza.py
  Windows'ta ne yapar" DEGIL, "yeni olcut, os.replace reddedince eski olcutun
  goremedigi seyi goruyor mu"dur. Windows'un kendi hukmu CI'da olculur; bu
  dosya onun YERINE GECMEZ (bir prob ORTAMI mi ARACI mi olcuyor — CLAUDE.md).

IKI MUTANT
  M-1 OLCUT   : yukaridaki ayrisma gorunuyor mu.
  M-2 IZ KILIDI: bir hukum SABOTAJ IZI basmadan verilirse ARAC KUSURU (exit 3)
                 olmali ve ham traceback KACMAMALI. Iz istege bagli olsaydi,
                 olcut yanlisligi yine gizlenirdi — CI #9'un teshisi tam bu iz
                 olmadigi icin bir tur gecikti.

CIKIS KODLARI (proje sozlesmesi)
  0 olculen her mutant ISIRDI · 1 en az biri KACTI · 2 OLCULEMEDI · 3 ARAC KUSURU
"""
import os
import re
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
SENARYO = os.path.join(KOK, "faz0", "fazB_senaryolari.py")
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")

ISIRDI = "ISIRDI"
KACTI = "KACTI"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []
ROOT = hasattr(os, "geteuid") and os.geteuid() == 0


class AracKusuru(Exception):
    pass


def _degistir(metin, eski, yeni, etiket):
    """Tek eslesme + SATIR SINIRI guvencesi (fazA/fazB ile ayni ders: girintili
    bir desen satirin ORTASINA eslesirse yamalanmis kopya ARACI degil YAMAYI
    olcer)."""
    n = metin.count(eski)
    if n != 1:
        raise AracKusuru("%s: hedef metin %d kez gecti (1 olmali). Kaynak "
                         "degistiyse MUTANT DA DEGISMELIDIR." % (etiket, n))
    i = metin.index(eski)
    if eski[:1] in (" ", "\t") and i != 0 and metin[i - 1] != "\n":
        raise AracKusuru("%s: desen girinti tasiyor ama eslesme SATIR BASINDA "
                         "degil (alt-dize eslesmesi)." % etiket)
    return metin.replace(eski, yeni, 1)


# --------------------------------------------------------------- ORTAM URETIMI
# os.replace'in salt-okunur hedefi REDDETTIGI hal. Windows'ta olculmus davranis
# (CI #9), burada POSIX'te enjekte edilir.
WIN_ENJ = (
    "        if os.path.lexists(p) and not os.access(p, os.W_OK):\n"
    "            raise PermissionError(13, \"WINDOWS-BENZERI: os.replace "
    "salt-okunur hedefe yazmaz\")\n")


def yama_win_benzeri(m):
    """Senaryo dosyasinin motor_kur cagrisina, os.replace'i kisitlayan bir ek
    yama BAGLAR. Yalniz B-B2 kolunu (_bb2_olc) etkiler."""
    m = _degistir(
        m,
        "def _bb2_olc(taban):\n",
        "def _win_benzeri_replace(m):\n"
        "    return _degistir(\n"
        "        m,\n"
        "        \"        os.replace(tmp, p)\\n\",\n"
        "        %r + \"        os.replace(tmp, p)\\n\",\n"
        "        \"mutant/win-benzeri\")\n"
        "\n"
        "\n"
        "def _bb2_olc(taban):\n" % (WIN_ENJ,),
        "mutant/win-fonksiyonu")
    # 🔴 DESEN _bb2_olc'A OZGU OLMALI: ilk dort satiri s_bb5 ile BIREBIR AYNI
    # (olculdu — mutant "2 kez gecti" deyip kendini durdurdu). Ayirt eden satir
    # `os.chmod(hedef, 0o444)`. Ortusen desen, ortusen tespit kadar korlestirir.
    return _degistir(
        m,
        "            motor = motor_kur(d, sabotaj=sab)\n"
        "            kok = proje_kur(motor, os.path.join(d, \"p\"))\n"
        "            hedef = konular(kok)\n"
        "            onceki = open(hedef, encoding=\"utf-8\").read()\n"
        "            os.chmod(hedef, 0o444)\n",
        "            motor = motor_kur(d, sabotaj=sab, ek_yama=_win_benzeri_replace)\n"
        "            kok = proje_kur(motor, os.path.join(d, \"p\"))\n"
        "            hedef = konular(kok)\n"
        "            onceki = open(hedef, encoding=\"utf-8\").read()\n"
        "            os.chmod(hedef, 0o444)\n",
        "mutant/win-baglama")


def yama_eski_olcut(m):
    """B-B2b'yi §5 ONCESI olcute dondurur: 'TESHIS SINIFI degisti mi' yerine
    'dosya DEGISTI mi'. Bolunmenin katkisi tam olarak buradadir."""
    return _degistir(
        m,
        "        sabotaj_uretti=s[\"sinif\"] != \"SALT-OKUNUR-TESHIS\",\n",
        "        sabotaj_uretti=s[\"degisti\"],\n",
        "mutant/eski-olcut")


def yama_izi_sok(m):
    """B-B2b hukum verirken IZ BASMAZ. Iz kilidi isiriyorsa exit 3 gelmeli."""
    return _degistir(
        m,
        "                   s[\"sinif\"], \"VAR\" if s[\"yol\"] else \"yok\", s[\"rc\"]),\n"
        "        muhtemel_sebep=\"kapi sokulunce de SALT-OKUNUR teshisi basildi (%s): teshisi \"\n"
        "                       \"ureten sey kapi DEGIL baska bir yol olabilir\" % sys.platform,\n"
        "        izler=(t[\"iz\"], s[\"iz\"]))\n",
        "                   s[\"sinif\"], \"VAR\" if s[\"yol\"] else \"yok\", s[\"rc\"]),\n"
        "        muhtemel_sebep=\"kapi sokulunce de SALT-OKUNUR teshisi basildi (%s): teshisi \"\n"
        "                       \"ureten sey kapi DEGIL baska bir yol olabilir\" % sys.platform)\n",
        "mutant/iz-sokme")


# --------------------------------------------------------------- ALTYAPI

def agac_kur(taban, ad, yamalar):
    """Yamalanmis senaryo dosyasi + DOKUNULMAMIS motor ile calisir bir agac."""
    kok = os.path.join(taban, ad)
    os.makedirs(os.path.join(kok, "faz0"))
    os.makedirs(os.path.join(kok, "skill", "scripts"))
    shutil.copy2(MOTOR, os.path.join(kok, "skill", "scripts", "hafiza.py"))
    metin = open(SENARYO, encoding="utf-8").read()
    for y in yamalar:
        metin = y(metin)
    try:
        import ast
        ast.parse(metin)
    except SyntaxError as e:
        raise AracKusuru("yamalanmis senaryo PARSE EDILEMIYOR (satir %s: %s)"
                         % (e.lineno, e.msg))
    hedef = os.path.join(kok, "faz0", "fazB_senaryolari.py")
    with open(hedef, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return hedef


def kos(betik, saniye=900):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, betik], capture_output=True,
                           timeout=saniye, env=o)
    except subprocess.TimeoutExpired:
        return None, "ZAMAN ASIMI (%d sn)" % saniye
    return r.returncode, (r.stdout or b"").decode("utf-8", "replace") + \
                         (r.stderr or b"").decode("utf-8", "replace")


def hukmu_bul(cikti, senaryo_adi):
    """Bir senaryonun HUKUM kelimesini rapor satirindan okur. Satir yoksa None —
    'yok' ile 'gecti' KARISTIRILMAZ."""
    for satir in cikti.splitlines():
        if senaryo_adi in satir:
            m = re.match(r"\s*(ISIRDI|KACTI|UYGULANMAZ|OLCULEMEDI)\s", satir)
            if m:
                return m.group(1)
    return None


def kayit(ad, hukum, ayrinti):
    SONUC.append((ad, hukum, ayrinti))


# --------------------------------------------------------------- MUTANTLAR

def m1_olcut(taban):
    """Windows-benzeri ortamda YENI olcut goruyor, ESKI olcut goremiyor mu?"""
    ad = "M-1 B-B2 bolunmesi: yeni olcut, eski olcutun goremedigini goruyor"
    if ROOT:
        kayit(ad, OLCULEMEDI, "root (uid 0) — salt-okunur dali olculemez, "
                              "senaryo kendini OLCULEMEDI ilan eder")
        return
    try:
        yeni = agac_kur(taban, "yeni_olcut", [yama_win_benzeri])
        eski = agac_kur(taban, "eski_olcut", [yama_win_benzeri, yama_eski_olcut])
    except AracKusuru as e:
        kayit(ad, OLCULEMEDI, "yama kurulamadi: %s" % e)
        return
    y_rc, y_c = kos(yeni)
    e_rc, e_c = kos(eski)
    if y_rc is None or e_rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    y_b = hukmu_bul(y_c, "B-B2b")
    e_b = hukmu_bul(e_c, "B-B2b")
    y_a = hukmu_bul(y_c, "B-B2a")
    if y_b is None or e_b is None:
        kayit(ad, OLCULEMEDI,
              "B-B2b hukum satiri BULUNAMADI (yeni=%s eski=%s) — kayip hukum "
              "'gecti' degildir" % (y_b, e_b))
        return
    kayit(ad, ISIRDI if (y_b == "ISIRDI" and e_b == "UYGULANMAZ") else KACTI,
          "WINDOWS-BENZERI ortam (os.replace salt-okunuru reddediyor) | "
          "YENI olcut B-B2b=%s (exit=%s) · ESKI olcut B-B2b=%s (exit=%s) | "
          "ayni ortamda B-B2a=%s (izin dali orada olculemez — beklenen)"
          % (y_b, y_rc, e_b, e_rc, y_a))


def m2_iz_kilidi(taban):
    """Izsiz hukum ARAC KUSURU (exit 3) mu, yoksa sessizce gecer mi?"""
    ad = "M-2 iz kilidi: izsiz hukum ARAC KUSURU sayiliyor"
    try:
        izsiz = agac_kur(taban, "izsiz", [yama_izi_sok])
    except AracKusuru as e:
        kayit(ad, OLCULEMEDI, "yama kurulamadi: %s" % e)
        return
    rc, c = kos(izsiz)
    if rc is None:
        kayit(ad, OLCULEMEDI, "zaman asimi")
        return
    mesaj = "SABOTAJ IZI BASMADI" in c
    tb = "Traceback (most recent call last)" in c
    kayit(ad, ISIRDI if (rc == 3 and mesaj and not tb) else KACTI,
          "IZ SOKULU: exit=%s ARAC-KUSURU mesaji=%s ham-traceback=%s "
          "(beklenen: exit=3 · mesaj VAR · traceback yok)"
          % (rc, "VAR" if mesaj else "YOK", "VAR" if tb else "yok"))


def main():
    print("=" * 82)
    print("FAZ B OLCUT MUTANTI — §5 duzeltmesi ISIRIYOR mu?")
    print("  python   : %s" % sys.version.split()[0])
    print("  platform : %s (os.name=%s)" % (sys.platform, os.name))
    print("  senaryo  : %s" % SENARYO)
    print("  uid      : %s" % ("root (0)" if ROOT else "root DEGIL"))
    print("=" * 82)
    try:
        taban = tempfile.mkdtemp(prefix="fazB_olcut_")
    except OSError as e:
        print("\nARAC KUSURU: gecici dizin acilamadi: %s" % e)
        return 3
    try:
        for f in (m1_olcut, m2_iz_kilidi):
            try:
                f(taban)
            except AracKusuru as e:
                print("\nARAC KUSURU: %s" % e)
                return 3
        print()
        say = {ISIRDI: 0, KACTI: 0, OLCULEMEDI: 0}
        for ad, hukum, ayrinti in SONUC:
            say[hukum] += 1
            print("  %-10s %-58s" % (hukum, ad))
            print("  %-10s   %s" % ("", ayrinti))
        print()
        print("OLCUMUN SINIRI (hukum degil):")
        print("  - Uretilen ortam GERCEK WINDOWS DEGILDIR; os.replace reddi enjekte")
        print("    edilmistir. Windows'un kendi hukmu CI'da olculur, burada DEGIL.")
        print("  - M-1 yalniz B-B2b'yi olcer; oteki senaryolarin olcutleri bu")
        print("    mutantin KAPSAMI DISINDADIR.")
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

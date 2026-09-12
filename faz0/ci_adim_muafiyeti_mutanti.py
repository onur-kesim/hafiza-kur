#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — CI ADIM MUAFIYETI MUTANTI (besli-paket/IS_EMRI_CI_OLU_KOD.md, KALEM A).

NEDEN VAR (olculdu, kod yazilmadan ONCE kosularak — CI #104/#105, Windows kolu)
  `.github/workflows/capraz.yml`deki `ortam_sinifi_mutanti` isinin adimi, motor
  `faz0/ortam_sinifi_mutanti.py` OLCULEMEDI (exit 2) dondugunde bu durumu
  BASARILI saymak icin bir MUAFIYET tasiyordu:

      set -o pipefail
      python faz0/ortam_sinifi_mutanti.py 2>&1 | tee ortam-sinifi-cikti.txt
      ec="${PIPESTATUS[0]}"
      if [ "$ec" = "2" ]; then ... exit 0; fi
      exit "$ec"

  GitHub Actions'ta `shell: bash` varsayilani **`bash --noprofile --norc -eo
  pipefail {0}`**dir — `-e` ZATEN ACIK. Boru `exit 2` dondurunce `-e` betigi
  O SATIRDA oldurur; `ec="${PIPESTATUS[0]}"` satirina HIC ULASILMAZ, muafiyet
  HICBIR ZAMAN calismaz. OLCULDU (bu dosya yazilmadan once, duz `bash`
  ile DEGIL, `bash --noprofile --norc -eo pipefail` ile, sentetik bir
  `python` koltuk degnegiyle): duz `bash adim.sh` kusuru YENIDEN URETEMEZ
  (NOT: satiri basilir, exit 0); GERCEK bayraklarla kusur REPRODUCE olur
  (NOT: satiri YOK, adim dogrudan exit 2 ile oluyor). Duzeltme: `set +e` ile
  borudan ONCE `-e`'yi gecici KAPATMAK, `ec=`yi OKUMAK, sonra `set -e` ile
  GERI ACMAK.

  Bu dosya BUNU yazili bir kapiya baglar — mutantsiz birakilirsa ayni kusur
  FARK EDILMEDEN geri gelebilir (tam da CI #104/#105'te oldugu gibi).

NE OLCER — UC KAPI (adim metni `.github/workflows/capraz.yml`den CIKARILIR
ve GERCEK GitHub bayraklariyla, `python` yerine PATH'e konan bir stub ile,
gecici bir dizinde kosulur — asla duz `bash <dosya>` ile DEGIL; bu, hatanin
KENDISI oldugu icin bu kapinin TEK can alici seçimidir)
  KAPI-1  stub exit=0 (temiz)       -> adim exit 0
  KAPI-2  stub exit=2 (OLCULEMEDI)  -> adim exit 0 VE ciktida "NOT:" satiri VAR
  KAPI-3  stub exit=1 (gercek kirmizi) -> adim exit 1 (muafiyet GERCEK kirmiziyi
          YUTMAMALI — KAPI-2 ile AYRI eksen, ortusen tespit korlugune dusmemek icin)

NE OLCMEZ
  1. `faz0/ortam_sinifi_mutanti.py`nin KENDI mantigi (ayri dosyanin ayri kapisi).
  2. Adimin disindaki baska CI islerinin `-e`/pipefail davranisi.

CIKIS KODLARI
  0  uc kapi de temiz VE M-1/M-2/M-3 ucu de ISIRDI
  1  bir kapi KIRMIZI ya da bir mutant KACTI (kapi kor)
  2  OLCULEMEDI (workflow okunamadi, adim metni bulunamadi, bash yok) —
     ve kirmizi/kacan YOK
"""
import io
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


VARSAYILAN_WORKFLOW = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", ".github", "workflows", "capraz.yml")


class Kurulamadi(Exception):
    """Test KURULUMU basarisiz (adim bulunamadi, bash yok) — KAPI HUKMU DEGILDIR."""


# ==================================================== adim metnini cikarma
# CAPA UYARISI: bu desen `ortam_sinifi_mutanti:` is kimligine (stabil) ve bir
# SONRAKI adimin adina (`ortam sinifi mutanti ciktisi`) ANKORLANIR. Adim
# bloğu BULUNAMAZSA OLCULEMEDI yazilir, sessiz PASS VERILMEZ.
_ADIM_DESENI = re.compile(
    r"ortam_sinifi_mutanti:.*?run: \|\n(.*?)\n      - name: ortam sinifi mutanti ciktisi",
    re.S)


def _adim_metnini_cikar(yaml_metni):
    m = _ADIM_DESENI.search(yaml_metni)
    return m.group(1) if m else None


_STUB_PYTHON = (
    "#!/usr/bin/env bash\n"
    "echo \"STUB: sentetik cikti (exit istenen=$CI_ADIM_STUB_EXIT)\"\n"
    "exit \"${CI_ADIM_STUB_EXIT:-0}\"\n"
)


def _adim_kos(adim_metni, stub_exit, calisma_dizini):
    """Adim metnini GERCEK GitHub bayraklariyla kosar: `bash --noprofile
    --norc -eo pipefail <dosya>`. `python`, PATH'e konan ve istenen cikis
    kodunu donen bir koltuk degnegidir. Duz `bash <dosya>` KULLANILMAZ —
    bu, hatanin kendisini (eksik `-e`) GIZLERDI (olculdu, bu dosyanin
    docstring'inde kayitli)."""
    bash_yolu = shutil.which("bash")
    if not bash_yolu:
        raise Kurulamadi("bash yok -- adim GERCEK bash'le sinanamadi")
    stub_dir = os.path.join(calisma_dizini, "stub")
    os.makedirs(stub_dir, exist_ok=True)
    stub_p = os.path.join(stub_dir, "python")
    with io.open(stub_p, "w", encoding="utf-8", newline="\n") as f:
        f.write(_STUB_PYTHON)
    os.chmod(stub_p, 0o755)
    adim_p = os.path.join(calisma_dizini, "adim.sh")
    with io.open(adim_p, "w", encoding="utf-8", newline="\n") as f:
        f.write(adim_metni + "\n")
    env = dict(os.environ)
    env["CI_ADIM_STUB_EXIT"] = str(stub_exit)
    env["PATH"] = stub_dir + os.pathsep + env.get("PATH", "")
    # OLCULDU: Windows/Git-Bash '\' argumanlarda kacis karakteri gibi
    # yutulabiliyor -- bash'e VERILEN dosya yolu her zaman '/' ile yazilir.
    adim_p_bash = adim_p.replace("\\", "/")
    r = subprocess.run([bash_yolu, "--noprofile", "--norc", "-eo", "pipefail", adim_p_bash],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=calisma_dizini, env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def kapi_adim_muafiyeti(adim, taban):
    """`adim`: `ortam_sinifi_mutanti` isinin run-blogu metni (ZATEN
    CIKARILMIS/ISOLE EDILMIS olmali — bkz. main()). Mutantlar bu KUCUK,
    ISOLE metni degistirir; TAM capraz.yml'i degil. Gerekce (olculdu):
    `ci_adim_muafiyeti_mutanti` isi KENDISI de AYNI `set +e`/`exit "$ec"`
    kalibini tasidigi icin, mutasyonu TAM DOSYAYA uygulamak `_degistir`'in
    "capa 1 yerde gecti" guvencesini KIRAR (iki is, ayni satir) -- isole
    metinde bu carpisma YOK."""
    bulgular = []

    d1 = os.path.join(taban, "kapi1")
    os.makedirs(d1)
    kod, c = _adim_kos(adim, 0, d1)
    if kod != 0:
        bulgular.append("KAPI-1: stub exit=0 (temiz) iken adim exit %d (beklenen 0): %s"
                         % (kod, c[:200]))

    d2 = os.path.join(taban, "kapi2")
    os.makedirs(d2)
    kod, c = _adim_kos(adim, 2, d2)
    if kod != 0:
        bulgular.append("KAPI-2: stub exit=2 (OLCULEMEDI) iken adim exit %d (beklenen 0) -- "
                         "muafiyet dali calismamis olabilir: %s" % (kod, c[:300]))
    elif "NOT:" not in c:
        bulgular.append("KAPI-2: adim exit 0 ama ciktida 'NOT:' satiri YOK (muafiyet dali "
                         "hic calismamis, baska bir yoldan exit 0'a dusmus olabilir): %s"
                         % c[:300])

    d3 = os.path.join(taban, "kapi3")
    os.makedirs(d3)
    kod, c = _adim_kos(adim, 1, d3)
    if kod != 1:
        bulgular.append("KAPI-3: stub exit=1 (GERCEK kirmizi) iken adim exit %d (beklenen 1) "
                         "-- muafiyet GERCEK kirmiziyi YUTMUS olabilir: %s" % (kod, c[:300]))

    return bulgular


# ================================================================ MUTANTLAR

def _degistir(s, eski, yeni, etiket):
    n = s.count(eski)
    if n != 1:
        sys.stdout.write("      ! capa %d yerde gecti (1 olmali) [%s]: %r\n"
                         % (n, etiket, eski[:70]))
        return None
    return s.replace(eski, yeni, 1)


_M1_ESKI = "          set +e\n"
_M1_YENI = "          :  # MUTANT: 'set +e' SOKULDU\n"


def m1_set_pe_sokulur(adim):
    """BUGUNKU KUSURUN TA KENDISI: `-e` boru sirasinda KAPATILMAZ -> GERCEK
    GitHub bayraklariyla, exit=2 donen boru betigi ORACIKTA oldurur, muafiyet
    dali HIC CALISMAZ -> KAPI-2 ISIRMALI."""
    return _degistir(adim, _M1_ESKI, _M1_YENI, "M-1")


_M2_ESKI = (
    "          if [ \"$ec\" = \"2\" ]; then\n"
    "            echo \"NOT: exit 2 = OLCULEMEDI (bu platformda/kullanicida POSIX dizin izni\" \\\n"
    "                 \"zorlanamiyor — KAPI-B GERCEK kolu icin beklenen; KIRMIZI/KACAN DEGIL).\" \\\n"
    "                 \"Adim BASARILI sayilir.\"\n"
    "            exit 0\n"
    "          fi\n"
)
_M2_YENI = "          :  # MUTANT: muafiyet blogu SOKULDU\n"


def m2_muafiyet_blogu_sokulur(adim):
    """Muafiyet blogunun TAMAMI kaldirilir -> exit=2 artik HICBIR ZAMAN 0'a
    donmez -> KAPI-2 ISIRMALI."""
    return _degistir(adim, _M2_ESKI, _M2_YENI, "M-2")


# NOT: izole `adim` metninin SON satiridir -- `_adim_metnini_cikar` sondaki
# "\n      - name: ..." kismini AYIRICI olarak kullandigi icin, yakalanan
# grupta bu satirin kendi SONUNDA yeni satir karakteri YOKTUR.
_M3_ESKI = "          exit \"$ec\""
_M3_YENI = "          exit 0  # MUTANT: GERCEK kirmizi de YUTULUYOR"


def m3_gercek_kirmizi_yutulur(adim):
    """Son satir `exit 0`a cevrilir -> GERCEK bir kirmizi (exit=1) de
    yutulur -> KAPI-3 ISIRMALI (KAPI-2 ile AYRI eksen: muafiyetin dogru
    CALISMASI ile muafiyetin ASIRI GENIS olmasi ayni kusur DEGILDIR)."""
    return _degistir(adim, _M3_ESKI, _M3_YENI, "M-3")


MUTANTLAR = [
    ("M-1  'set +e' sokulur (bugunku kusurun ta kendisi)", m1_set_pe_sokulur),
    ("M-2  muafiyet blogu sokulur", m2_muafiyet_blogu_sokulur),
    ("M-3  GERCEK kirmizi de yutulur", m3_gercek_kirmizi_yutulur),
]


# ===================================================================== main

def main():
    _cikti_kodlamasini_guvenceye_al()
    yaml_yolu = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(VARSAYILAN_WORKFLOW)
    print("=== CI ADIM MUAFIYETI MUTANTI === workflow: %s · platform: %s"
          % (yaml_yolu, sys.platform))

    try:
        yaml_metni = io.open(yaml_yolu, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — workflow okunamadi: %s" % e)
        return 2

    adim = _adim_metnini_cikar(yaml_metni)
    if adim is None:
        print("SONUC: OLCULEMEDI — adim metni (ortam_sinifi_mutanti run bloğu) "
              "capraz.yml icinde BULUNAMADI")
        return 2

    olculemeyen = 0
    kirmizi = 0

    taban = tempfile.mkdtemp(prefix="ciadim_kapi_")
    try:
        b = kapi_adim_muafiyeti(adim, taban)
        print("  KAPI-1/2/3  : %s" % ("KIRMIZI" if b else "YESIL"))
        for x in b:
            print("      - %s" % x)
        if b:
            kirmizi += 1
    except Kurulamadi as e:
        print("  KAPI-1/2/3  : OLCULEMEDI — %s" % e)
        olculemeyen += 1
    finally:
        shutil.rmtree(taban, ignore_errors=True)

    print("\n--- MUTANT SINAMASI (izole adim metnine textual sabotaj) ---")
    kacan = 0
    for ad, fn in MUTANTLAR:
        bozuk = fn(adim)
        if bozuk is None or bozuk == adim:
            print("  %-46s -> OLCULEMEDI (mutant KURULAMADI)" % ad)
            olculemeyen += 1
            continue
        taban_m = tempfile.mkdtemp(prefix="ciadim_mut_")
        try:
            b_mut = kapi_adim_muafiyeti(bozuk, taban_m)
        except Kurulamadi as e:
            print("  %-46s -> OLCULEMEDI (%s)" % (ad, e))
            olculemeyen += 1
            continue
        finally:
            shutil.rmtree(taban_m, ignore_errors=True)
        if b_mut:
            print("  %-46s -> ISIRDI" % ad)
        else:
            print("  %-46s -> KACTI (KAPI KOR)" % ad)
            kacan += 1

    print()
    if kacan:
        print("SONUC: KIRMIZI — %d mutant KACTI (kapi kor)." % kacan)
        return 1
    if kirmizi:
        print("SONUC: KIRMIZI — adim kendisi kirmizi (mutant sinamasindan ONCE)." )
        return 1
    if olculemeyen:
        print("SONUC: OLCULEMEDI — %d kalem kosulamadi/kurulamadi; sessiz PASS verilmez."
              % olculemeyen)
        return 2
    print("SONUC: YESIL — uc kapi de temiz, her mutant ISIRDI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

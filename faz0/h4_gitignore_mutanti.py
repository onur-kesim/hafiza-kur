#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — H4 GITIGNORE MUTANTI (KALEM 2, besli-paket/IS_EMRI_DEVRAL.md).

NEDEN VAR (olculdu 6 Eyl 2026, Momentum kopyasi, git DAHIL)
  `_h4_havuz` git'in bildigini ELLE TAKLIT EDIYORDU: yalniz sabit
  `.git, node_modules, __pycache__, .venv` disliyordu. OLCULDU: `main.dart.js`
  agacta 7 yerde vardi ve H4 "OLU BAGLANTI — ayni adli baska dosya var ama yol
  tutmuyor" dedi; ama `.gitignore` okundugunda `.dart_tool/` VE derleme
  wwwroot'u ORADAYDI — yedi kopyanin YEDISI de git tarafindan yok sayiliyordu,
  hicbiri izlenmiyordu. Bu, kapali "gitfile korlugu"nun (`.git`i elle DIZIN
  sanmak) BIREBIR kardesi: cozum orada da burada da AYNI KALIP — "git'e sordur".

NE OLCER
  KAPI-A (POZITIF KONTROL + MUTANT EKSENI) — `.gitignore`'lu bir dizindeki
      kopya HAVUZA GIRMEZ: beyan edilen yol artik "hicbir yerde yok" (OLU,
      aciklamasiz), "yol tutmuyor" / "TASINMIS" DEGIL. Bu bir GEVSETME degil
      TERSINE DARALTMADIR (bulgu KAYBOLMUYOR, GEREKCESI dogruluyor).
  KAPI-B (GIT YOK KORUNUR) — git'siz agacta AYNI dizin duzeni eski (sabit
      liste) davranisini AYNEN uretir: kopya bulunur (TASINMIS/yol tutmuyor).
  KAPI-C (IZLENEN DOSYA KORUNUR) — `.gitignore`'da OLMAYAN, GERCEKTEN izlenen
      (commit'li) bir dosya havuzdan haric TUTULMAZ — kapi kor edilmiyor.
  KAPI-D (besli-paket KALEM B, 6 Eyl 2026, Onur kilidi 20:30 — DOSYA EKSENI,
      AYRI KOL): KAPI-A/B/C UCU DE yoksayilan DIZIN ekseninde kurulmustu; bu
      "ORTUSEN TESPIT KORLUGU" KALEM 2'nin yarim kaldigini (dosya dongusu
      `haric_git`'e karsi suzulmuyordu) GORMEDI. KAPI-D izlenen bir dizinin
      ICINDEKI TEK bir `.gitignore`'lu DOSYAYI (dizin degil) sinar:
      (1) POZITIF KONTROL: o dosya havuza GIRMEZ, hukum "hicbir yerde yok".
      (2) MUTANT: dosya suzgeci sokulur -> eski cumle geri gelir (ISIRIR).
      (3) 2-EK KORUNUR: yoksayilan DOSYA'nin varligi, beyan edilen yolu F'den
          O'ya TASIMAZ (ayni agacta kapi hala FAIL/exit 1).
      (4) IZLENEN DOSYA KORUNUR: `.gitignore`'da OLMAYAN kardes dosya (ayni
          dizinde) havuzda KALIR — dosya suzgeci KOMSU dosyalari silahsizlandirmaz.
  KAPI-E (besli-paket IS_EMRI_2EK_KOLU.md KALEM 1, 6 Eyl 2026, Onur kilidi
      22:4x — F/O AYRIMI, AYRI KOL): KAPI-D tek basina IKI ekseni birden
      tasiyordu (`rapor.log=OLU_ACIKLAMASIZ · gercek.md=YOL_TUTMUYOR`) ve KALEM
      B'nin mutant olcutu (3) "2-EK KORUNUR" icin AYRI kol YOKTU — ORTUSEN
      TESPIT KORLUGU (bu paket boyunca IKINCI kez: KALEM 2'nin dosya ekseni ve
      `gitfile` capasindan sonra). AYNI agacta (`h_ignore_dosya`), KAPI-D'nin
      iki iddiasini TEKRARLAMADAN, F/O ayrimini olcer:
      - dosya-tabanli beyan (`belgeler/rapor.log`) F'de KALIR, O'ya KAYMAZ.
      - dizin-tabanli beyan (`.git/index.lock`) AYNI kosumda O'DA GORUNUR.
      Ikisi tek agacta yan yana olculur ki kolun NEYI ayirt ettigi gizlenemesin.
      MUTANT (M-3): 2-EK'in "ilk bilesen" (dizin siniri) ayrimi, DOSYA ADI
      (basename) uzerinden yapilan bir esleme ile BOZULUR — boyle bir
      karisiklikta `belgeler/rapor.log`, GERCEKTEN yoksayilan `notlar/
      rapor.log` ile SADECE ADLARI ORTAK oldugu icin ayirt edilemez olur ve
      YANLISLIKLA O'ya kayar (gercek bir OLU BAGLANTI GIZLENIR). Pozitif
      kontrol: bugunku (duzeltmeden onceki) motorda KAPI-E YESIL, M-3 ISIRIR.

NE OLCMEZ
  Performans (`check-ignore` toplu/tek surec) BURADA olculmez — davranissal
  DEGIL, uygulama detayidir; kod incelemesiyle dogrulanir.

CIKIS KODU  0 bes kapi da temiz VE uc mutant da ISIRDI · 1 kapi kirmizi / mutant KACTI
            2 OLCULEMEDI (git yok, motor okunamadi, senaryo kurulamadi)
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
            try:
                akis.reconfigure(errors="replace")
            except Exception:
                pass


_cikti_kodlamasini_guvenceye_al()

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78

HAZIRLIK = [["not", "--konu=genel-durum", "--tur=durum", "--metin=h4 gitignore mutanti icin ilk kayit"],
            ["derle"]]

_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="h4gitmut", GIT_AUTHOR_EMAIL="h4git@example.invalid",
                GIT_COMMITTER_NAME="h4gitmut", GIT_COMMITTER_EMAIL="h4git@example.invalid",
                GIT_CONFIG_NOSYSTEM="1")


def kos(motor, arglar, kok):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *args):
    return subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                          env=_GIT_ENV, check=False)


def _commit_et(kok, mesaj="taban"):
    _git(kok, "add", "-A")
    _git(kok, "-c", "commit.gpgsign=false", "commit", "-q", "-m", mesaj)


def _dosya(kok, rel, icerik):
    p = os.path.join(kok, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(icerik)


def _ekle(kok, satirlar):
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write("\n" + "\n".join(satirlar) + "\n")


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kenarin olculdugu anlamina GELMEZ."""


def hal_kur(motor, ad, tip, taban):
    kok = os.path.join(taban, ad)
    os.makedirs(kok, exist_ok=True)
    if tip != "git_yok":
        subprocess.run(["git", "init", "-q", kok], capture_output=True, check=False)
    rc, c = kos(motor, ["kur", "--ad", "H4GITMUT"], kok)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s): %s" % (ad, c.strip().split("\n")[-1][:120]))
    for adim in HAZIRLIK:
        rc, c = kos(motor, adim, kok)
        if rc != 0:
            raise Kurulamadi("%s adimi basarisiz (%s): %s"
                             % (adim[0], ad, c.strip().split("\n")[-1][:120]))

    if tip == "ignore_olu":
        # Momentum vakasinin KUCUK OLCEGI: '.dart_tool/'/wwwroot yerine 'build/'.
        # build/web/main.dart.js YOKSAYILIR (.gitignore); beyan `web/main.dart.js`
        # dizin BILESENI "web" ile ORTAK oldugu icin ESKI kodda TASINMIS/yol
        # tutmuyor sayilirdi — git'e sorulunca kopya havuza HIC GIRMEMELI.
        _dosya(kok, ".gitignore", "build/\n")
        _dosya(kok, "build/web/main.dart.js", "// derleme artefakti\n")
        _ekle(kok, ["Dosya: `web/main.dart.js`."])
    elif tip == "git_yok":
        # git init YOK (yukarida atlandi). Ayni dizin duzeni ama SABIT liste
        # 'build'u haric TUTMAZ -> kopya BULUNMALI (eski davranis BIREBIR).
        _dosya(kok, "build/web/main.dart.js", "// derleme artefakti\n")
        _ekle(kok, ["Dosya: `web/main.dart.js`."])
    elif tip == "izlenen":
        # .gitignore'da OLMAYAN, GERCEKTEN commit'li bir dosya: `arsiv/` altinda
        # oldugu icin zaten TASINMIS sayilir — git-yoksayma DEGISIKLIGI bunu
        # haric TUTMAMALI (kapi kor edilmiyor).
        _dosya(kok, "arsiv/belgeler/rapor.md", "# eski rapor\n")
        _commit_et(kok)
        _ekle(kok, ["Rapor burada: `belgeler/rapor.md`."])
    elif tip == "ignore_dosya":
        # besli-paket KALEM B (6 Eyl 2026, Onur kilidi 20:30) — is emrinden
        # BIREBIR minimal vaka: izlenen bir DIZIN (`notlar/`) icinde TEK bir
        # dosya git-ignore'lu (`*.log`), kardes dosya izleniyor. KALEM 2
        # yalniz `d0` (alt DIZIN) listesini `haric_git`e karsi suzuyordu; bu
        # tek dosya (`notlar/rapor.log`) hicbir dizin filtresine UGRAMADAN
        # havuza girmeye devam ediyordu.
        _dosya(kok, ".gitignore", "*.log\n")
        _dosya(kok, "notlar/rapor.log", "gizli log\n")
        _dosya(kok, "notlar/gercek.md", "gercek not\n")
        _commit_et(kok)      # rapor.log yoksayili oldugu icin commit'e GIRMEZ
        # besli-paket IS_EMRI_2EK_KOLU.md KALEM 1 (6 Eyl 2026, Onur kilidi 22:4x):
        # AYNI agacta DIZIN-tabanli bir beyan da eklenir (`.git/index.lock` —
        # gercek Tuzak Avcisi vakasinin KUCUK OLCEGI). KAPI-E ikisini YAN YANA
        # olcer: dosya-tabanli beyan F'de KALMALI, dizin-tabanli beyan O'DA
        # GORUNMELI — kolun NEYI ayirt ettigi tek agacta gizlenemez.
        _ekle(kok, ["Olu baglanti denemesi: `belgeler/rapor.log`.",
                    "Izlenen dosya beyani: `belgeler/gercek.md`.",
                    "Havuz disi dizin denemesi: `.git/index.lock`."])
    else:
        raise Kurulamadi("bilinmeyen hal tipi: %s" % tip)
    return kok


HALLER = [
    ("h_ignore_olu", "ignore_olu"),
    ("h_git_yok", "git_yok"),
    ("h_izlenen", "izlenen"),
    ("h_ignore_dosya", "ignore_dosya"),
]


def haller_kur(motor_temiz, taban):
    return {ad: hal_kur(motor_temiz, ad, tip, taban) for ad, tip in HALLER}


def kume_olc(motor, kokler, hedef_taban):
    out = {}
    for ad, kaynak_kok in kokler.items():
        kok = os.path.join(hedef_taban, ad)
        shutil.copytree(kaynak_kok, kok)
        rc, c = kos(motor, ["kapi"], kok)
        out[ad] = (rc, c)
    return out


def _h4_satiri(cikti):
    for d in [s.strip() for s in cikti.split("\n")]:
        if d.startswith("[H4]") or d[:12].find("H4:") >= 0:
            return d
    return None


def _siniflandirma(satir):
    if not satir:
        return "YOK"
    if "hicbir yerde yok" in satir:
        return "OLU_ACIKLAMASIZ"
    if "TASINMIS" in satir:
        return "TASINMIS"
    if "yol tutmuyor" in satir:
        return "YOL_TUTMUYOR"
    return "DIGER"


def _yol_siniflandir(cikti, yol):
    """KAPI-D/M-2 icin: `_h4_satiri` yalniz ILK H4 satirini yakalar — bir
    agacta BIRDEN FAZLA H4 bulgusu varsa (KAPI-D'de oldugu gibi) YANLIS yolun
    siniflandirmasini donebilir (alfabetik sirada `belgeler/gercek.md`,
    `belgeler/rapor.log`den ONCE gelir). Bu yuzden BELIRLI bir yolu tasiyan
    H4 satirini arar."""
    for satir in [s.strip() for s in cikti.split("\n")]:
        if yol in satir and (satir.startswith("[H4]") or satir[:12].find("H4:") >= 0):
            return _siniflandirma(satir)
    return "YOK"


def hukum(motor, taban):
    """Her hal icin (kod, H4 satiri, siniflandirma, HAM cikti) doner. Sonuncu
    alan (ham cikti) KAPI-D'nin AYNI agacta IKI ayri H4 bulgusunu (dosya
    ekseni + 2-EK'in F kaldigi) birlikte dogrulamasi icin gerekli — tek
    satirlik `_h4_satiri` yalniz ILK H4 satirini yakalar. `taban` HER cagriya
    OZEL (mkdtemp) olmalidir — iki ayri motor (temiz/mutant) ayni dizin
    agacini PAYLASMAZ."""
    kokler = haller_kur(motor, os.path.join(taban, "kaynak"))
    olcum = kume_olc(motor, kokler, os.path.join(taban, "olc"))
    out = {}
    for ad, tip in HALLER:
        kod, cikti = olcum[ad]
        satir = _h4_satiri(cikti)
        out[ad] = (kod, satir, _siniflandirma(satir), cikti)
    return out


# --------------------------------------------------------------------- MUTANT
# `_h4_havuz`in tek cagri yeri (`havuz = _h4_havuz(kok)`) ve imzasi
# (`_h4_havuz(kok)`) FAZ C bolme mutantlarinin (h4_bolme_mutanti.py,
# fazC_bolucu_h4.py) capasidir ve DEGISTIRILMEZ. KALEM 2'nin sorgusu
# `_h4_havuz` GOVDESI icindedir; mutant o govdedeki TEK satiri hedefler.
ANKOR = "    haric_git = _h4_git_yoksayilanlar(kok)\n"
YENI = "    haric_git = set()      # MUTANT: git'e hic sorulmuyor\n"


def sokulmus_motor(kaynak, hedef_dizin):
    n = kaynak.count(ANKOR)
    if n != 1:
        return None, "capa %d yerde gecti (1 olmali): %r" % (n, ANKOR.strip())
    metin = kaynak.replace(ANKOR, YENI, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        return None, "sabotajli motor derlenmiyor: %s" % e
    p = os.path.join(hedef_dizin, "hafiza.py")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p, None


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok (bu batarya git'e SORDURMAYI olcer).")
        return 2

    print(CIZGI)
    print("H4 GITIGNORE MUTANTI (KALEM 2) — motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    print(CIZGI)

    taban = tempfile.mkdtemp(prefix="h4_gitignore_")
    try:
        try:
            h = hukum(yol, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2

        b = []
        kod, satir, sinif, _ = h["h_ignore_olu"]
        print("  KAPI-A .gitignore'lu kopya : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if kod == 0:
            b.append("KAPI-A: kapi YESIL — beklenen [H4] OLU bulgusu YOK")
        elif sinif != "OLU_ACIKLAMASIZ":
            b.append("KAPI-A: siniflandirma %r (beklenen OLU_ACIKLAMASIZ — 'hicbir yerde yok')" % sinif)

        kod, satir, sinif, _ = h["h_git_yok"]
        print("  KAPI-B git yok             : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if sinif == "OLU_ACIKLAMASIZ":
            b.append("KAPI-B: git YOKKEN de 'hicbir yerde yok' — sabit liste davranisi BOZULDU")
        elif sinif not in ("TASINMIS", "YOL_TUTMUYOR"):
            b.append("KAPI-B: siniflandirma %r (beklenen TASINMIS/YOL_TUTMUYOR — eski davranis)" % sinif)

        kod, satir, sinif, _ = h["h_izlenen"]
        print("  KAPI-C izlenen dosya       : kod=%s · %s" % (kod, satir or "(H4 satiri YOK)"))
        if sinif != "TASINMIS":
            b.append("KAPI-C: izlenen dosya TASINMIS bulunmadi (%r) — kapi KOR edilmis olabilir" % sinif)

        kod, satir, sinif, cikti = h["h_ignore_dosya"]
        rapor_sinif = _yol_siniflandir(cikti, "belgeler/rapor.log")
        gercek_sinif = _yol_siniflandir(cikti, "belgeler/gercek.md")
        print("  KAPI-D yoksayilan DOSYA    : kod=%s · rapor.log=%s · gercek.md=%s"
              % (kod, rapor_sinif, gercek_sinif))
        if kod != 1:
            b.append("KAPI-D: kapi exit %s (1/FAIL bekleniyordu — 2-EK'in O'ya kaydirmasi DEGIL)" % kod)
        if rapor_sinif != "OLU_ACIKLAMASIZ":
            b.append("KAPI-D: 'belgeler/rapor.log' siniflandirmasi %r (beklenen "
                     "OLU_ACIKLAMASIZ — 'hicbir yerde yok'; dosya suzgeci calismiyor olabilir)"
                     % rapor_sinif)
        if "[H4] OLU BAGLANTI: belgeler/rapor.log" not in cikti:
            b.append("KAPI-D (2-EK): 'belgeler/rapor.log' F listesinde DEGIL — "
                     "yoksayilan dosyanin varligi beyani yanlislikla O'ya tasimis olabilir")
        if gercek_sinif not in ("TASINMIS", "YOL_TUTMUYOR"):
            b.append("KAPI-D: izlenen kardes dosya ('belgeler/gercek.md' -> notlar/gercek.md) "
                     "siniflandirmasi %r — havuzdan haric tutulmus olabilir (dosya suzgeci "
                     "komsuyu da siliyor)" % gercek_sinif)

        # ------------------------------------------------------------- KAPI-E
        # besli-paket IS_EMRI_2EK_KOLU.md KALEM 1 (6 Eyl 2026, Onur kilidi
        # 22:4x): KAPI-D tek basina IKI ekseni birden tasiyordu (dosya-ekseni
        # HAVUZA GIRME + izlenen kardes) ve KALEM B'nin mutant olcutu (3)
        # "2-EK KORUNUR" icin AYRI kol yoktu — ORTUSEN TESPIT KORLUGU. KAPI-E
        # AYNI agacta (h_ignore_dosya) F/O ayrimini AYRICA, KAPI-D'nin iki
        # iddiasini TEKRARLAMADAN olcer: dosya-tabanli beyan F'de KALIR (O'ya
        # KAYMAZ), dizin-tabanli beyan (`.git/index.lock`) AYNI kosumda O'DA
        # GORUNUR — kolun neyi ayirt ettigi tek agacta GIZLENEMEZ.
        lock_sinif_F = "[H4] OLU BAGLANTI: belgeler/rapor.log" in cikti
        rapor_O_da_mi = re.search(r"\?\s*H4:\s*belgeler/rapor\.log\b", cikti) is not None
        lock_O_da_mi = re.search(r"\?\s*H4:\s*\.git/index\.lock\b.*OLCULEMEDI", cikti) is not None
        lock_F_de_mi = "[H4] OLU BAGLANTI: .git/index.lock" in cikti
        print("  KAPI-E F/O ayrimi          : rapor.log F=%s/O=%s · .git/index.lock F=%s/O=%s"
              % (lock_sinif_F, rapor_O_da_mi, lock_F_de_mi, lock_O_da_mi))
        if not lock_sinif_F:
            b.append("KAPI-E: 'belgeler/rapor.log' F listesinde YOK (2-EK yanlislikla "
                     "dosya-tabanli beyani da O'ya kaydirmis olabilir)")
        if rapor_O_da_mi:
            b.append("KAPI-E: 'belgeler/rapor.log' O listesinde DE GORUNUYOR — "
                     "yoksayilan DOSYA'nin varligi beyani F'den O'ya TASIMIS")
        if not lock_O_da_mi:
            b.append("KAPI-E: '.git/index.lock' (dizin tabanli) O'da GORUNMUYOR — "
                     "AYNI kosumda kontrol grubu olcemedi")
        if lock_F_de_mi:
            b.append("KAPI-E: '.git/index.lock' YANLISLIKLA F listesinde — "
                     "kapi oraya HIC BAKMADIGI halde 'hicbir yerde yok' diyor")

        for x in b:
            print("      ! %s" % x)
        if b:
            print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
            return 1

        print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
        kacan = []

        mdir = tempfile.mkdtemp(prefix="mutant1_", dir=taban)
        sab, hata = sokulmus_motor(s, mdir)
        if sab is None:
            print("  M-1 git sorgusu sokulur           OLCULEMEDI: %s" % hata)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        mh = hukum(sab, os.path.join(taban, "mutant1"))
        mkod, msatir, msinif, _ = mh["h_ignore_olu"]
        if msinif != "OLU_ACIKLAMASIZ":
            print("  M-1 git sorgusu sokulur           -> ISIRDI ✓  (kopya geri geldi: %s)"
                  % (msatir or "(H4 satiri YOK)"))
        else:
            print("  M-1 git sorgusu sokulur           -> KACTI ✗  (sorgu sokulunce de ayni "
                  "hukum cikti — kapi bunu HIC OLCMUYOR)")
            kacan.append("M-1")

        # M-2 (besli-paket KALEM B, MUTANT madde 2): DOSYA suzgeci sokulur ->
        # eski cumle ("yol tutmuyor") geri gelmeli. `_h4_havuz`in imzasi/tek
        # cagri yeri DEGISMEZ; mutant yalniz govdedeki YENI dosya-suzme
        # bloğunu hedefler.
        ANKOR2 = ('            _rel_f = _rel(os.path.join(r0, f), kok)\n'
                  '            if _rel_f in haric_git:\n'
                  '                continue\n'
                  '            havuz.setdefault(f, []).append(_rel_f)\n')
        YENI2 = '            havuz.setdefault(f, []).append(_rel(os.path.join(r0, f), kok))\n'
        n2 = s.count(ANKOR2)
        if n2 != 1:
            print("  M-2 dosya suzgeci sokulur         OLCULEMEDI: capa %d yerde gecti "
                  "(1 olmali)" % n2)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        metin2 = s.replace(ANKOR2, YENI2, 1)
        try:
            compile(metin2, "<mutant2>", "exec")
        except SyntaxError as e:
            print("  M-2 dosya suzgeci sokulur         OLCULEMEDI: sabotajli motor "
                  "derlenmiyor: %s" % e)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        mdir2 = tempfile.mkdtemp(prefix="mutant2_", dir=taban)
        sab2 = os.path.join(mdir2, "hafiza.py")
        with io.open(sab2, "w", encoding="utf-8", newline="\n") as f:
            f.write(metin2)
        mh2 = hukum(sab2, os.path.join(taban, "mutant2"))
        _, _, _, cikti2 = mh2["h_ignore_dosya"]
        # 🔴 `_h4_satiri` DEGIL: agacta IKI H4 bulgusu var, alfabetik sirada
        # 'belgeler/gercek.md' 'belgeler/rapor.log'dan ONCE gelir — yanlis
        # yolun siniflandirmasini KAYDIRIRDI. `belgeler/rapor.log`u ACIKCA ara.
        m2sinif = _yol_siniflandir(cikti2, "belgeler/rapor.log")
        if m2sinif == "YOL_TUTMUYOR":
            print("  M-2 dosya suzgeci sokulur         -> ISIRDI ✓  (eski cumle geri geldi: "
                  "'belgeler/rapor.log' artik YOL_TUTMUYOR)")
        else:
            print("  M-2 dosya suzgeci sokulur         -> KACTI ✗  ('belgeler/rapor.log' "
                  "siniflandirmasi %r — kapi bunu HIC OLCMUYOR)" % m2sinif)
            kacan.append("M-2")

        # M-3 (besli-paket IS_EMRI_2EK_KOLU.md KALEM 1, MUTANT madde d): 2-EK'in
        # DIZIN sinirini (ilk bilesen) yok sayip DOSYA ADI (basename) uzerinden
        # esleyen bir "TAM AD" karsilastirmasina bozulur. Boyle bir karisiklikta
        # `belgeler/rapor.log` (baska bir dizinde, ama AYNI ADLA anilan) ile
        # `notlar/rapor.log` (GERCEKTEN yoksayilan) ayirt edilemez olur ve ilki
        # YANLISLIKLA O'ya kayar — gercek bir OLU BAGLANTI bulgusu GIZLENIR.
        # `_h4_havuz`in imzasi/cagri yeri DEGISMEZ; motor DEGISMEZ (yalniz bu
        # dosyada, gecici olarak, bellekte sokulur).
        ANKOR3 = ('        _haric = _H4_HARIC_SON[0]\n'
                  '        for _p in [p for p in eksik if p.split("/", 1)[0] in _haric]:\n'
                  '            O.append("H4: %s havuz disinda (yoksayilan dizin) — OLCULEMEDI" % _p)\n'
                  '        eksik = [p for p in eksik if p.split("/", 1)[0] not in _haric]\n')
        YENI3 = ('        _haric = _H4_HARIC_SON[0]\n'
                  '        _haric_ad = {h.rsplit("/", 1)[-1] for h in _haric}  '
                  '# MUTANT: ilk bilesen yerine TAM AD (basename)\n'
                  '        for _p in [p for p in eksik if p.rsplit("/", 1)[-1] in _haric_ad]:\n'
                  '            O.append("H4: %s havuz disinda (yoksayilan dizin) — OLCULEMEDI" % _p)\n'
                  '        eksik = [p for p in eksik if p.rsplit("/", 1)[-1] not in _haric_ad]\n')
        n3 = s.count(ANKOR3)
        if n3 != 1:
            print("  M-3 2-EK ayrimi ilk-bilesen->AD    OLCULEMEDI: capa %d yerde gecti "
                  "(1 olmali)" % n3)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        metin3 = s.replace(ANKOR3, YENI3, 1)
        try:
            compile(metin3, "<mutant3>", "exec")
        except SyntaxError as e:
            print("  M-3 2-EK ayrimi ilk-bilesen->AD    OLCULEMEDI: sabotajli motor "
                  "derlenmiyor: %s" % e)
            print(CIZGI)
            print("SONUC: OLCULEMEDI — mutant kurulamadi (arac kusuru, kapi kor DEGIL).")
            return 2
        mdir3 = tempfile.mkdtemp(prefix="mutant3_", dir=taban)
        sab3 = os.path.join(mdir3, "hafiza.py")
        with io.open(sab3, "w", encoding="utf-8", newline="\n") as f:
            f.write(metin3)
        mh3 = hukum(sab3, os.path.join(taban, "mutant3"))
        _, _, _, cikti3 = mh3["h_ignore_dosya"]
        m3_kayan = re.search(r"\?\s*H4:\s*belgeler/rapor\.log\b.*OLCULEMEDI", cikti3) is not None
        if m3_kayan:
            print("  M-3 2-EK ayrimi ilk-bilesen->AD    -> ISIRDI ✓  ('belgeler/rapor.log' "
                  "F'den O'ya kaydi: basename cakismasi 'notlar/rapor.log' ile gizlendi)")
        else:
            print("  M-3 2-EK ayrimi ilk-bilesen->AD    -> KACTI ✗  ('belgeler/rapor.log' hala "
                  "F'de — kapi bu ayrimi HIC OLCMUYOR)")
            kacan.append("M-3")

        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %s beklendigi gibi olculmedi." % ", ".join(kacan))
            return 1
        print("SONUC: YESIL — bes kapi da temiz, uc mutant da AYRI eksende ISIRDI.")
        return 0
    finally:
        shutil.rmtree(taban, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

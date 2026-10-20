#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GITATTRIBUTES UYARI MUTANTI — `kapi` H21: satir sonu korumasinin YOKLUGU gizlenemez mi, ve yalniz UYARI mi?
(besli-paket/IS_EMRI_GITATTRIBUTES_MUHUR.md KALEM 2, 18 Eki 2026; hukum sinifi UYARI = Onur kilidi 18 Eki 23:31)

GUNCELLEME (20 Eki 2026, H21 SESSIZLIK — besli-paket/IS_EMRI_H21_SESSIZLIK.md): depo-degil ve izlenmeyen-yol dallari ARTIK SESSIZ DEGIL (Onur: "h21 duzeltmesini
yapalim"); o iki dalin halleri ve sabotajlari (eski M-GA5, M-GA6) `faz0/h21_sessizlik_mutanti.py`ye tasindi (M-S2, M-S3 olarak TERS yone cevrildi).
Bu dosya KALAN bes hali ve dort sabotaji sinar; hepsi dogrulugunu korur.

NE OLCER — bes HAL, her biri `kapi` ciktisindaki `H21` satirlariyla ve cikis koduyla yargilanir:
    KORUMASIZ   git deposu, defterler commit'li, `.gitattributes` YOK   -> TEK `· H21: satir sonu cevrimi ... bozabilir` satiri (UYARI kanali)
    KORUMALI    ayni, `kur`un yazdigi blok VAR                           -> H21 SATIRI YOK; cikis kodu KORUMASIZ ile AYNI (UYARI exit'i degistirmez)
    KENDI       kullanici `.gitattributes`'i `* -text` (blok yok)        -> H21 SATIRI YOK (koruma baska kuraldan; yanlis alarm yok)
    GACOMMITSIZ blok calisma agacinda VAR ama commit'e GIRMEDI               -> TEK `· H21: .gitattributes commit'lenmemis` (klon korumasiz); exit AYNI
    GITYOK      `.git` VAR ama git calistirilamiyor (PATH bos)           -> TEK `H21: OLCULEMEDI` satiri (sessiz PASS yok)
  SAGLAM motorda hepsi YESIL; asagidaki dort sabotajin HER BIRI KENDI halinde KIRMIZI yakmalidir (yanlis sebeple isirmak sayilmaz):
    M-GA3 CHECK-ATTR KOR                `git check-attr` okumasi her yola `unset` der      -> KORUMASIZ
    M-GA4 OLCULEMEDI SUSAR              git yokken OLCULEMEDI satiri basilmaz               -> GITYOK
    M-GA11 UYARI KIRMIZIYA TERFI        uyarilar F (hata) kanalina yazilir: cikis kodu degisir -> KORUMASIZ (exit)
    M-GA13 COMMIT DENETIMI YOK          calisma agacindaki blok koruma sayilir (commit'siz)  -> GACOMMITSIZ

NE OLCMEZ
  Mevcut Linux/macOS projelerinin ilk gercek kullanimdaki gurultu orani (Onur kilidi: UYARI, kirmiziya bogmamak icin). `check-attr`in
  `core.autocrlf` AYARINI degil yalniz OZNITELIGI okudugu (iki ayri ekseni: oznitelik proje korumasidir, ayar kullanicinin makinesidir).

KULLANIM    python3 faz0/gitattributes_uyari_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve dort mutantin HEPSI kendi halinde KIRMIZI yakti · 1 saglam kirmizi/mutant KACTI · 2 OLCULEMEDI
"""
import os
import shutil
import stat
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

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARSAYILAN_MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 84
HALLER = ["KORUMASIZ", "KORUMALI", "KENDI", "GACOMMITSIZ", "GITYOK"]


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin saglam/kor oldugu anlamina GELMEZ."""


def git_ortami(taban):
    g = os.path.join(taban, "gitconfig-global")
    if not os.path.isfile(g):
        with open(g, "w", encoding="utf-8", newline="\n") as f:
            f.write("[user]\n\tname = gauyr\n\temail = gauyr@example.invalid\n[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n")
    haric = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT")   # baska deponun ortami sizmasin
    ortam = dict((k, v) for k, v in os.environ.items() if k not in haric)
    return dict(ortam, GIT_CONFIG_GLOBAL=g, PYTHONIOENCODING="utf-8")


def git(ortam, *args, cwd=None):
    r = subprocess.run(["git"] + list(args), cwd=cwd, env=ortam, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:140]))
    return r.stdout


def kos(motor, arglar, kok, ortam):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok", kok], env=ortam, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _agaci_sil(yol):
    def _ac_ve_sil(fn, p, *_):
        try:
            os.chmod(p, stat.S_IWRITE)
            fn(p)
        except OSError:
            pass
    if sys.version_info >= (3, 12):
        shutil.rmtree(yol, onexc=_ac_ve_sil)
    else:
        shutil.rmtree(yol, onerror=_ac_ve_sil)


def proje(motor, taban, ortam, ad, git_baslat=True):
    k = os.path.join(taban, ad)
    os.makedirs(k)
    if git_baslat:
        git(ortam, "init", "-q", k)
    rc, c = kos(motor, ["kur", "--ad", "GAUYR"], k, ortam)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (%s, exit %s): %s" % (ad, rc, c.strip().split("\n")[-1][:140]))
    return k


def komitle(ortam, k):
    git(ortam, "add", "-A", cwd=k)
    git(ortam, "commit", "-q", "-m", "taban", cwd=k)


def ga_sil(k):
    p = os.path.join(k, ".gitattributes")
    if os.path.isfile(p):
        os.remove(p)


def gozle(motor, taban):
    """-> {hal: (exit, [H21 satirlari])} — halleri kurar, `kapi` kosar."""
    os.makedirs(taban, exist_ok=True)
    ortam = git_ortami(taban)
    kokler = {}
    k = proje(motor, taban, ortam, "korumasiz")
    ga_sil(k)
    komitle(ortam, k)
    kokler["KORUMASIZ"] = k
    k = proje(motor, taban, ortam, "korumali")
    komitle(ortam, k)
    kokler["KORUMALI"] = k
    k = proje(motor, taban, ortam, "kendi")
    with open(os.path.join(k, ".gitattributes"), "w", encoding="utf-8", newline="\n") as f:
        f.write("* -text\n")
    komitle(ortam, k)
    kokler["KENDI"] = k
    k = proje(motor, taban, ortam, "gacommitsiz")          # blok calisma agacinda VAR ama commit'e GIRMEDI: klon korumasiz kalir
    git(ortam, "add", "-A", cwd=k)
    git(ortam, "reset", "-q", "--", ".gitattributes", cwd=k)
    git(ortam, "commit", "-q", "-m", "taban (.gitattributes haric)", cwd=k)
    kokler["GACOMMITSIZ"] = k
    k = proje(motor, taban, ortam, "gityok")
    ga_sil(k)
    komitle(ortam, k)
    kokler["GITYOK"] = k
    bos_yol = os.path.join(taban, "bos-yol")
    os.makedirs(bos_yol, exist_ok=True)
    gozlem = {}
    for hal, kok in kokler.items():
        e = ortam
        if hal == "GITYOK":                                # git calistirilamiyor: PATH git'siz bir dizine cevrilir
            e = dict(ortam, PATH=bos_yol)
        rc, c = kos(motor, ["kapi"], kok, e)
        gozlem[hal] = (rc, [x.strip() for x in c.split("\n") if "H21" in x])
    return gozlem


def ihlaller(g):
    """-> [(hal, mesaj)] — bos liste = YESIL. Saglam/sabotajli motor AYNI fonksiyonla yargilanir."""
    out = []
    rc0, s0 = g["KORUMASIZ"]
    if len(s0) != 1 or not s0[0].startswith("· H21: satir sonu cevrimi") or "bozabilir" not in s0[0]:
        out.append(("KORUMASIZ", "TEK `· H21: satir sonu cevrimi ... bozabilir` UYARI satiri beklenir: %r" % s0))
    rc1, s1 = g["KORUMALI"]
    if s1:
        out.append(("KORUMALI", "koruma VARKEN H21 satiri basildi: %r" % s1))
    if rc0 != rc1:
        out.append(("KORUMASIZ", "UYARI cikis kodunu DEGISTIRDI (korumasiz %s != korumali %s)" % (rc0, rc1)))
    if g["KENDI"][1]:
        out.append(("KENDI", "koruma baska kuraldan VARKEN H21 satiri basildi: %r" % g["KENDI"][1]))
    s5 = g["GITYOK"][1]
    if len(s5) != 1 or not s5[0].startswith("· H21: OLCULEMEDI"):
        out.append(("GITYOK", "TEK `H21: OLCULEMEDI` satiri beklenir (sessiz PASS yok): %r" % s5))
    rc6, s6 = g["GACOMMITSIZ"]
    if len(s6) != 1 or not s6[0].startswith("· H21: .gitattributes commit'lenmemis"):
        out.append(("GACOMMITSIZ", "blok commit'siz: TEK `H21: .gitattributes commit'lenmemis` satiri beklenir: %r" % s6))
    if rc6 != rc1:
        out.append(("GACOMMITSIZ", "UYARI cikis kodunu DEGISTIRDI (commit'siz %s != korumali %s)" % (rc6, rc1)))
    return out


# ad, aciklama, hedef hal(ler), [(eski, yeni)]. `eski` motorda TAM 1 kez gecmelidir.
MUTANTLAR = [
    ("M-GA3 CHECK-ATTR KOR", "`git check-attr` okumasi her yola `unset` der", {"KORUMASIZ"},
     [("    deger = dict((parca[i], parca[i + 2]) for i in range(0, len(parca) - 2, 3))\n",
       "    deger = dict((parca[i], \"unset\") for i in range(0, len(parca) - 2, 3))   # MUTANT\n")]),
    ("M-GA4 OLCULEMEDI SUSAR", "git yokken OLCULEMEDI satiri basilmaz", {"GITYOK"},
     [("        N.append(\"H21: OLCULEMEDI (git calistirilamiyor, %s)",
       "        _x = (\"H21: OLCULEMEDI (git calistirilamiyor, %s)")]),
    ("M-GA11 UYARI KIRMIZIYA TERFI", "uyarilar F (hata) kanalina yazilir: cikis kodu degisir", {"KORUMASIZ"},
     [("    _kapi_uyarilar(N, kok, y)\n", "    _kapi_uyarilar(F, kok, y)   # MUTANT\n")]),
    ("M-GA13 COMMIT DENETIMI YOK", "calisma agacindaki blok koruma sayilir (klonun gorecegi commit'li surum degil)", {"GACOMMITSIZ"},
     [("    cdizin = _h21_commitsiz_dizin(kok, top) if (izlenen and not acik) else None\n", "    cdizin = None   # MUTANT\n")]),
]


def sabotajli_motor(kaynak, degisimler, hedef_dizin):
    metin = kaynak
    for eski, yeni in degisimler:
        n = metin.count(eski)
        if n != 1:
            raise Kurulamadi("hedef dizge %d kez gecti (1 olmali): %r" % (n, eski[:60]))
        metin = metin.replace(eski, yeni, 1)
    try:
        compile(metin, "<mutant>", "exec")
    except SyntaxError as e:
        raise Kurulamadi("sabotajli motor derlenmiyor: %s" % e)
    p = os.path.join(hedef_dizin, "hafiza.py")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return p


def main():
    motor = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_MOTOR
    if not os.path.isfile(motor):
        print("OLCULEMEDI: motor yok: %s" % motor)
        return 2
    if not shutil.which("git"):
        print("OLCULEMEDI: git yok — haller kurulamaz.")
        return 2
    kaynak = open(motor, encoding="utf-8").read()
    print(CIZGI)
    print("GITATTRIBUTES UYARI MUTANTI — H21 satir sonu korumasi yoklugu gizlenemez, ama yalniz UYARI · platform: %s" % sys.platform)
    print("motor: %s" % motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="gauyr_")
    try:
        try:
            g = gozle(motor, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        for hal in HALLER:
            print("  %-10s exit %s · %s" % (hal, g[hal][0], (g[hal][1][0][:100] if g[hal][1] else "(H21 satiri yok)")))
        temiz = ihlaller(g)
        print("  SAGLAM MOTOR (%d hal)            %s" % (len(HALLER), "YESIL" if not temiz else "KIRMIZI"))
        for hal, m in temiz:
            print("      ! %-10s %s" % (hal, m[:170]))
        if temiz:
            print(CIZGI)
            print("SONUC: KIRMIZI — saglam motor kapiyi gecemedi.")
            return 1
        isirdi, kacti, olculemedi = [], [], []
        for ad, aciklama, hedef, degisim in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisim, d)
                ih = ihlaller(gozle(sab, os.path.join(d, "hal")))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-36s OLCULEMEDI  %s" % (ad, e))
                continue
            haller = {h for h, _ in ih}
            if hedef & haller:
                isirdi.append(ad)
                print("  +  %-36s ISIRDI      hedef hal: %s · tum ihlal halleri: %s"
                      % (ad, ",".join(sorted(hedef & haller)), ",".join(sorted(haller))))
            elif ih:
                kacti.append(ad)
                print("  !  %-36s YANLIS SEBEP ihlal %s var ama HEDEF hal (%s) susuyor" % (ad, ",".join(sorted(haller)), ",".join(sorted(hedef))))
            else:
                kacti.append(ad)
                print("  !  %-36s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
            sys.stdout.flush()
    finally:
        _agaci_sil(taban)
    print(CIZGI)
    print("SONUC: %d isirdi - %d kacti - %d olculemedi (toplam %d)" % (len(isirdi), len(kacti), len(olculemedi), len(MUTANTLAR)))
    if olculemedi:
        print("  OLCULEMEDI ARAC KUSURUDUR — 'kapi saglam' DEMEK DEGILDIR.")
        return 2
    if kacti:
        print("  KACAN mutant = bu kapinin KOR oldugu yapi.")
        return 1
    print("  Saglam motor YESIL, dort sabotajin hepsi KENDI halinde KIRMIZI: H21 olculuyor ve yalniz UYARI.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

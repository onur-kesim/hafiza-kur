#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HOOK MUTANTI — `hafiza.py hook --kur` ile kurulan pre-commit, kapi KIRMIZI
iken commit'i GERCEKTEN durduruyor mu?
(besli-paket/IS_EMRI.md KALEM 5, Onur kilidi 6 Eylul 2026)

NEDEN VAR (BELGE-KOD CELISKISI, olculdu 6 Eylul 2026)
  `SKILL.md` §1 tablosu KAPILI kademe icin "Zorlayici: Otomatik kapi + git hook"
  diyordu; §9 "Git hook bunu kismen zorlar, tamamen degil" diye ekliyordu;
  `references/sablonlar.md` elle kurulacak bir `pre-commit` sablonu veriyordu.
  Ama MOTORDA hook ureten hicbir kod YOKTU — olculdu: `hafiza.py` icinde "hook"
  gecen satir sayisi SIFIR. Yani belge bir otomatiklestirme VAAT EDIYOR, kod
  VERMIYORDU. Bu deponun kendi kapaginda tekrar eden sinif: "belge de bir
  arayuzdur ve yalan soyleyebilir".

  🔴 KURARKEN DIKKAT EDILEN IKI SEY (ikisi de bu projenin OLCULMUS dersi):
   (a) `.git` DIZIN SANILMAZ. hooks dizini `git rev-parse --git-path hooks` ile
       GIT'IN KENDISINE sordurulur. worktree / `--separate-git-dir` / submodule
       calisma agacinda `.git` bir METIN DOSYASIDIR (4 Eyl 2026 gitfile
       korlugu) ve `core.hooksPath` yalniz bu yolla dogru cozulur.
   (b) VAR OLAN HOOK EZILMEZ. Baskasinin hook'unu sessizce degistirmek, aracin
       "hicbir satir silinmez, tasinir" ilkesiyle carpisir.

NE OLCER (BES KOL; Y3'UN IKI KOLU asagida)
  Sabotaj, yazilan hook govdesindeki `exit 1`i `exit 0`a cevirir: hook KOSAR,
  kirmiziyi BASAR, ama commit'i DURDURMAZ — "gorunurde calisan, fiilen etkisiz
  koruma" sinifi. (chmod'u dusuren bir sabotaj SECILMEDI: executable biti
  Windows'ta anlamsizdir, o mutant platforma gore FARKLI sey olcerdi.)

  1. POZITIF KONTROL : sabotajSIZ hook + KIRMIZI kapi -> `git commit` REDDEDILIR.
  2. MUTANT          : sabotajLI hook + AYNI vaka -> commit GECER (⇒ ISIRDI).
  3. HOOK KORUNUR    : var olan hook uzerine `hook --kur` -> DURUR ve dosyanin
                       SHA'si DEGISMEZ (ezme yok).
  4. YANLIS-POZITIF  : sabotajSIZ hook + YESIL kapi -> commit GECER. Hook her
                       commit'i durdursaydi koruma degil kilit olurdu.
  5. GITFILE         : `--separate-git-dir` ile kurulmus agacta hook, git'in
                       BILDIRDIGI hooks dizinine yazilir (`.git` bir METIN
                       DOSYASI oldugu halde). Elle `.git/hooks` kuran bir arac
                       burada HIC CALISMAYAN bir yere yazar ve fark etmez.

  🔴 PLATFORM SINIRI: 1. kol POZITIF KONTROLDUR. Bir platformda `sh` hook'lari
  hic kosmuyorsa commit reddedilmez; bu bir KUSUR degil ORTAM sinirdir ve kol
  OLCULEMEDI doner (BEKLENMEDIK degil) — "olculemeyene temiz denmez, ama
  olculemedi de FAIL degildir". O halde 2. kol da OLCULEMEDI'ye duser: pozitif
  kontrolu olmayan bir mutant, kendi basina hukum veremez.

Y3 — `isir` HOOK'LU PROJEDE (Onur kilidi 4 Eki 2026) · IKI KOL DAHA
  `hook --kur`un pre-commit'i, `isir`in mutant kopyasina `.git` ile GIDER ve kopyadaki
  `git commit`i durdurur: M-H12g/M-H14g/M-H9 KURULAMADI olur, `isir` hook'lu projede
  81/81 yerine 78/78 + 3 SINANMADI (exit 2) verir (olculdu 4 Eki, Windows + Linux;
  commit'siz projede yalniz M-H12g/M-H14g — hook kapiyi "henuz commit yok" dalinda
  gecirir). Duzeltme: mutant kopyasindaki HER git cagrisi kum havuzundaki BOS bir
  `core.hooksPath` ile kosar (motor: `cmd_isir._git_hooksuz`).
  6. ISIR HOOK'LU  : git'li, commit'li, `derle` kosulmus, hook KURULU projede `isir` ->
                     exit 0 ve `81/81` (hook'suz projedekiyle AYNI). Hook'un bu
                     projede gercekten KOSTUGU, `isir`den sonra ayri bir kirmizi-kapi
                     commit denemesiyle ispatlanir; kosmuyorsa kol OLCULEMEDI'dir.
  7. M-Y3 MUTANT   : motorda `core.hooksPath` eki SOKULUR (`_git_hooksuz` duz
                     `["git", "-C", h]` doner) -> AYNI proje `isir` exit 2 ve TAM
                     {M-H12g, M-H14g, M-H9} KURULAMADI (78/78 + 3) verir (⇒ ISIRDI).
                     81/81 verirse mutant KACTI: 6. kol hook'u HIC olcmuyordur.

CIKIS KODLARI: 0 yedi kol da beklendigi gibi · 1 BEKLENMEDIK · 2 OLCULEMEDI ·
3 ARAC KUSURU
"""
import hashlib
import os
import re
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
MOTOR = os.path.join(KOK, "skill", "scripts", "hafiza.py")
CIZGI = "-" * 82

BEKLENDIGI_GIBI = "BEKLENDIGI-GIBI"
BEKLENMEDIK = "BEKLENMEDIK"
OLCULEMEDI = "OLCULEMEDI"
SONUC = []

_GIT_ORTAM = dict(
    GIT_AUTHOR_NAME="hk-mut", GIT_AUTHOR_EMAIL="hk-mut@example.invalid",
    GIT_COMMITTER_NAME="hk-mut", GIT_COMMITTER_EMAIL="hk-mut@example.invalid",
    GIT_CONFIG_NOSYSTEM="1")

_DUZELTILMIS = '''  echo "HAFIZA KAPISI KIRMIZI — commit durduruldu."
  exit 1
}'''
_SABOTAJLI = '''  echo "HAFIZA KAPISI KIRMIZI — commit durduruldu."
  exit 0
}'''


# Y3 sabotaji: `cmd_isir._git_hooksuz`un `core.hooksPath` eki SOKULUR.
_Y3_DUZELTILMIS = '        return ["git", "-c", "core.hooksPath=" + bos, "-C", h]'
_Y3_SABOTAJLI = '        return ["git", "-C", h]'
_ISIR_SONUC = re.compile(r"^SONUC: (\d+)/(\d+) kosulan mutant ISIRIYOR.*?(\d+) SINANMADI", re.M)
_ISIR_KURULAMADI = re.compile(r"^  (M-\S+)\s.*-> KURULAMADI", re.M)
_Y3_BEKLENEN_KURULAMAYAN = ["M-H12g", "M-H14g", "M-H9"]


class AracKusuru(Exception):
    pass


def _kayit(ad, durum, ayrinti):
    SONUC.append((ad, durum, ayrinti))


def _sabotajli_motor(hedef, duzeltilmis=_DUZELTILMIS, sabotajli=_SABOTAJLI,
                     yer="HOOK_GOVDESI"):
    metin = open(MOTOR, encoding="utf-8").read()
    n = metin.count(duzeltilmis)
    if n != 1:
        raise AracKusuru("sabotaj hedefi %d kez gecti (1 olmali). Motor degistiyse "
                         "SABOTAJ DA DEGISMELIDIR (hafiza.py %s)." % (n, yer))
    with open(hedef, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin.replace(duzeltilmis, sabotajli, 1))
    return hedef


def _kos(motor, arglar, saniye=180):
    o = dict(os.environ)
    o["PYTHONIOENCODING"] = "utf-8"
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar,
                           capture_output=True, timeout=saniye, env=o,
                           text=True, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return None, "", "ZAMAN ASIMI"
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git(kok, *args, **kw):
    r = subprocess.run(["git", "-C", kok] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, **_GIT_ORTAM))
    if not kw.get("hosgor") and r.returncode != 0:
        raise AracKusuru("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:200]))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def _kum_havuzu(motor, kok, ayri_gitdir=None):
    os.makedirs(kok, exist_ok=True)
    if ayri_gitdir:
        os.makedirs(ayri_gitdir, exist_ok=True)
        r = subprocess.run(["git", "init", "-q", "--separate-git-dir", ayri_gitdir, kok],
                           capture_output=True, text=True,
                           env=dict(os.environ, **_GIT_ORTAM))
        if r.returncode != 0:
            raise AracKusuru("git init --separate-git-dir: " + (r.stderr or "")[:200])
    else:
        _git(kok, "init", "-q")
    rc, c, e = _kos(motor, ["kur", "--ad", "HK", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("kur basarisiz (exit=%s): %s" % (rc, (c + e)[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "ilk")
    return kok


def _kapiyi_kirmizi_yap(kok):
    """Canli hafizadan BASELINE bir satir silinir -> [H1] KAYIP."""
    p = os.path.join(kok, "PROJE_HAFIZA.md")
    L = open(p, encoding="utf-8", newline="").read().splitlines(True)
    for i, s in enumerate(L):
        g = s.strip()
        if g and not g.startswith("#") and not g.startswith(">") and len(g) > 12:
            del L[i]
            break
    else:
        raise AracKusuru("silinecek anlamli satir bulunamadi")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))


def _kapi_kirmizi_mi(motor, kok):
    rc, _, _ = _kos(motor, ["kapi", "--kok=" + kok])
    return rc not in (0, None)


def _commit_dene(kok):
    """Bir dosya degistirilir ve commit DENENIR. Doner: (kabul_edildi, cikti)"""
    with open(os.path.join(kok, "deneme.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write("satir\n")
    _git(kok, "add", "-A")
    rc, c = _git(kok, "commit", "-m", "hook denemesi", hosgor=True)
    return rc == 0, c


# ------------------------------------------------------------------ KOLLAR
def _kol_kirmizi(motor, kok, ad, durmasi_bekleniyor):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "hook kurulamadi: %s" % (c + e).strip()[:120])
    _kapiyi_kirmizi_yap(kok)
    if not _kapi_kirmizi_mi(motor, kok):
        return _kayit(ad, OLCULEMEDI, "kapi KIRMIZI yapilamadi (senaryo kurulamadi)")
    kabul, cikti = _commit_dene(kok)
    if durmasi_bekleniyor:
        if not kabul:
            return _kayit(ad, BEKLENDIGI_GIBI, "commit REDDEDILDI (hook calisti)")
        return _kayit(ad, OLCULEMEDI,
                      "commit GECTI — bu ortamda `sh` hook'lari kosmuyor olabilir "
                      "(PLATFORM SINIRI, kusur hukmu VERILMEZ)")
    if kabul:
        return _kayit(ad, BEKLENDIGI_GIBI, "commit GECTI (kusur geri geldi ⇒ ISIRDI)")
    _kayit(ad, BEKLENMEDIK, "commit REDDEDILDI — sabotaja ragmen durdu")


def _kol_hook_korunur(motor, kok, ad):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "ilk hook kurulamadi")
    m = re.search(r"HOOK KURULDU: (.+)", c)
    if not m:
        return _kayit(ad, OLCULEMEDI, "hook yolu ciktidan cozulemedi")
    hedef = m.group(1).strip()
    with open(hedef, "a", encoding="utf-8", newline="\n") as f:
        f.write("# kullanicinin kendi satiri\n")
    once = _sha(hedef)
    rc2, c2, e2 = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    sonra = _sha(hedef)
    if rc2 != 0 and once == sonra:
        return _kayit(ad, BEKLENDIGI_GIBI, "DURDU (exit=%s) ve dosya DEGISMEDI" % rc2)
    _kayit(ad, BEKLENMEDIK,
           "exit=%s, dosya %s" % (rc2, "DEGISMEDI" if once == sonra else "EZILDI"))


def _kol_yesil(motor, kok, ad):
    _kum_havuzu(motor, kok)
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, OLCULEMEDI, "hook kurulamadi")
    if _kapi_kirmizi_mi(motor, kok):
        return _kayit(ad, OLCULEMEDI, "kapi ZATEN kirmizi — yesil kol kurulamadi")
    kabul, cikti = _commit_dene(kok)
    if kabul:
        return _kayit(ad, BEKLENDIGI_GIBI, "yesil kapida commit GECTI")
    _kayit(ad, BEKLENMEDIK, "yesil kapida commit REDDEDILDI: %s" % cikti.strip()[:120])


def _kol_gitfile(motor, kok, gitdir, ad):
    _kum_havuzu(motor, kok, ayri_gitdir=gitdir)
    if os.path.isdir(os.path.join(kok, ".git")):
        return _kayit(ad, OLCULEMEDI, ".git DIZIN cikti — gitfile senaryosu kurulamadi")
    rc, c, e = _kos(motor, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        return _kayit(ad, BEKLENMEDIK, "gitfile agacinda hook kurulamadi: %s"
                      % (c + e).strip()[:120])
    m = re.search(r"HOOK KURULDU: (.+)", c)
    hedef = m.group(1).strip() if m else ""
    gercek = os.path.realpath(os.path.join(gitdir, "hooks", "pre-commit"))
    if hedef and os.path.realpath(hedef) == gercek and os.path.isfile(gercek):
        return _kayit(ad, BEKLENDIGI_GIBI, "hook AYRI gitdir'e yazildi")
    _kayit(ad, BEKLENMEDIK, "hook %r yazildi, beklenen %r" % (hedef, gercek))


def _hookta_isir(proje_motoru, isir_motoru, kok):
    """Y3 projesi: git'li, COMMIT'li, `derle` kosulmus ve hook KURULU; `isir` kosulur.
    Doner: (isir_exit, isir_cikti). Proje ve hook `proje_motoru` ile kurulur (hook'un
    gomulu motor yolu = gercek motor), `isir` `isir_motoru` ile kosar (mutantta sabotajli).
    `isir` projeyi DEGISTIRMEZ (kopya uzerinde calisir)."""
    _kum_havuzu(proje_motoru, kok)
    for arglar in (["not", "--kok=" + kok, "--konu=genel-durum", "--metin=hook isir"],
                   ["derle", "--kok=" + kok]):
        rc, c, e = _kos(proje_motoru, arglar)
        if rc != 0:
            raise AracKusuru("%s basarisiz (exit=%s): %s" % (arglar[0], rc, (c + e)[-300:]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "derle sonrasi (hook'tan ONCE)")
    rc, c, e = _kos(proje_motoru, ["hook", "--kur", "--kok=" + kok])
    if rc != 0:
        raise AracKusuru("hook kurulamadi (exit=%s): %s" % (rc, (c + e)[-300:]))
    rc, c, e = _kos(isir_motoru, ["isir", "--kok=" + kok], saniye=900)
    if rc is None:
        raise AracKusuru("isir ZAMAN ASIMI (900 sn)")
    return rc, c + e


def _hook_kosuyor_mu(motor, kok):
    """Hook BU projede gercekten kosuyor mu? Kapi kirmiziya cevrilir, commit DENENIR;
    commit reddedilirse hook kosuyordur. `isir`den SONRA cagrilir (projeyi kirletir)."""
    _kapiyi_kirmizi_yap(kok)
    if not _kapi_kirmizi_mi(motor, kok):
        raise AracKusuru("kapi KIRMIZI yapilamadi (hook-kosuyor-mu sinamasi kurulamadi)")
    kabul, _ = _commit_dene(kok)
    return not kabul


def _isir_ozeti(rc, cikti):
    """(bicim, kurulamayanlar, ozet): `isir` ciktisindan hukum parcalari."""
    m = _ISIR_SONUC.search(cikti)
    kur = sorted(set(_ISIR_KURULAMADI.findall(cikti)))
    bicim = "%s/%s + %s SINANMADI" % (m.group(1), m.group(2), m.group(3)) if m else "SONUC satiri YOK"
    return m, kur, "isir exit=%s · %s · KURULAMADI=%s" % (rc, bicim, ",".join(kur) or "yok")


def _kol_isir_hookta(proje_motoru, isir_motoru, kok, ad, mutant):
    rc, cikti = _hookta_isir(proje_motoru, isir_motoru, kok)
    m, kur, ozet = _isir_ozeti(rc, cikti)
    if not mutant:
        sonuc_tamam = (rc == 0 and m is not None and m.group(1) == "81" == m.group(2)
                       and m.group(3) == "0" and not kur)
        beklenmedik = "hook'lu projede isir 81/81 DEGIL: " + ozet
    else:
        sonuc_tamam = (rc == 2 and m is not None and m.group(1) == m.group(2)
                       and kur == sorted(_Y3_BEKLENEN_KURULAMAYAN))
        if rc == 0 and m is not None and m.group(1) == "81":
            beklenmedik = ("M-Y3 KACTI: `core.hooksPath` eki sokulunce de isir 81/81 — "
                           "6. kol hook'un etkisini HIC OLCMUYOR: " + ozet)
        else:
            beklenmedik = ("sabotajda beklenen 78/78 + TAM {M-H12g, M-H14g, M-H9} "
                           "KURULAMADI (exit 2) degil: " + ozet)
    if not sonuc_tamam:
        return _kayit(ad, BEKLENMEDIK, beklenmedik)
    # Sonuc beklenen gibi — AMA hook bu ortamda KOSMUYORSA sonuc bir ISPAT degildir.
    if not _hook_kosuyor_mu(proje_motoru, kok):
        return _kayit(ad, OLCULEMEDI,
                      "sonuc beklenen gibi ama hook bu projede KOSMUYOR (kirmizi kapida commit "
                      "GECTI) — PLATFORM SINIRI, hukum VERILMEZ: " + ozet)
    _kayit(ad, BEKLENDIGI_GIBI, ("hook KOSARKEN " if not mutant else "sabotajda ISIRDI: ") + ozet)


def _sil(yol):
    """Betigin KENDI gecici dizinini (`hkm_*`) SIL — git objeleri Windows'ta salt-okunur oldugu icin
    `rmtree(ignore_errors=True)` hepsini %TEMP%'te birakiyordu (W1, olculdu 4 Eki 2026: kosum basina 1
    `hkm_*` + 8 `hafiza_isir_*`). Hata gelince girdiyi yazilabilir yapip yeniden dener; yine olmazsa stderr'e
    TEK satir. Kokun USTUNE ve sembolik baglantiya chmod YOK. Motorun `_gecici_sil`inden BAGIMSIZ kopya."""
    yol = os.path.normpath(yol)

    def onar(fonk, p, *_):
        hedef = [p] if not os.path.islink(p) else []
        if os.path.dirname(p).startswith(yol):
            hedef.append(os.path.dirname(p))
        for h in hedef:
            try:
                os.chmod(h, stat.S_IRWXU)
            except OSError:
                pass
        try:
            fonk(p)
        except OSError:
            pass
    shutil.rmtree(yol, **({"onexc": onar} if sys.version_info >= (3, 12) else {"onerror": onar}))
    if os.path.lexists(yol):
        print("GECICI DIZIN SILINEMEDI: %s" % yol, file=sys.stderr)


def main():
    if not os.path.isfile(MOTOR):
        print("ARAC KUSURU: motor yok: %s" % MOTOR)
        return 3
    if not shutil.which("git"):
        print("ARAC KUSURU: git yok")
        return 3
    gecici = tempfile.mkdtemp(prefix="hkm_")
    try:
        try:
            sab = _sabotajli_motor(os.path.join(gecici, "sab.py"))
            _kol_kirmizi(MOTOR, os.path.join(gecici, "a"), "1. POZITIF KONTROL", True)
            _kol_kirmizi(sab, os.path.join(gecici, "b"), "2. MUTANT", False)
            _kol_hook_korunur(MOTOR, os.path.join(gecici, "c"), "3. HOOK KORUNUR")
            _kol_yesil(MOTOR, os.path.join(gecici, "d"), "4. YANLIS-POZITIF")
            _kol_gitfile(MOTOR, os.path.join(gecici, "e"),
                         os.path.join(gecici, "e_gitdir"), "5. GITFILE")
            _kol_isir_hookta(MOTOR, MOTOR, os.path.join(gecici, "f"), "6. ISIR HOOK'LU", False)
            sab_y3 = _sabotajli_motor(os.path.join(gecici, "sab_y3.py"), _Y3_DUZELTILMIS,
                                      _Y3_SABOTAJLI, "cmd_isir._git_hooksuz")
            _kol_isir_hookta(MOTOR, sab_y3, os.path.join(gecici, "g"), "7. M-Y3 MUTANT", True)
        except AracKusuru as ex:
            print("ARAC KUSURU: %s" % ex)
            return 3
    finally:
        _sil(gecici)

    print("=" * 82)
    print("HOOK MUTANTI — kurulan pre-commit kirmizi kapida commit'i durduruyor mu?")
    print("=" * 82)
    for ad, durum, ayrinti in SONUC:
        print("  %-22s %-16s %s" % (ad, durum, ayrinti))
    print(CIZGI)
    bek = sum(1 for _, d, _ in SONUC if d == BEKLENDIGI_GIBI)
    print("SONUC: %d/%d kol BEKLENDIGI GIBI" % (bek, len(SONUC)))
    if any(d == BEKLENMEDIK for _, d, _ in SONUC):
        return 1
    if any(d == OLCULEMEDI for _, d, _ in SONUC):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

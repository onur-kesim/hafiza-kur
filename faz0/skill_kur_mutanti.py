#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — SKILL-KUR OLCERI (besli-paket/IS_EMRI_SKILL_KUR.md, 30 Eyl 2026): `skill-kur` KOPYALAYIP
OLCUYOR mu, ve o olcum KENDI MUTANTLARINI yakaliyor mu?

NEDEN VAR
  `skill-kur` kullanicinin ev dizinine yazar. "Kurdum" demesi yetmez: kopya bit-bit mi, envanter
  paketle.sh ile ayni mi, var olan FARKLI kurulum ezilmiyor mu, yedek gercekten yedek mi, gecici
  dizin `skills/` altinda (Claude Code'un yukleyecegi yerde) mi birakiliyor — bunlari HICBIR sey
  olcmuyordu. Bu betik gercek motoru SAHTE bir ev dizininde kosar ve her davranisi ayri kolla olcer.

GERCEK EV DIZINI KORUNUR: her alt surecte `HOME` ve `USERPROFILE` (Windows `expanduser` USERPROFILE
okur) gecici dizine ayarlanir; kaynak skill/ agaci da depodan KOPYALANIR (kaynaga `deneme/`,
`__pycache__/` gibi artik enjekte edilir, depo kirlenmez).

KOLLAR (gercek motor, sahte HOME)
  K-TAZE        bos HOME -> exit 0; kurulu envanter == suzulmus kaynak (her dosya bayt-esit); kurulu
                motorun `surum` SHA'si == kaynak; `.claude/` altinda gecici artik YOK
  K-AYNI        ikinci kosum -> exit 0 "ZATEN KURULU"; hedefteki HICBIR dosyanin bayti/mtime'i degismedi
  K-FARKLI      kurulu hafiza.py'ye 1 bayt -> exit 2; hedef bayt-birebir ayni; iki SHA basildi
  K-GUNCELLE    ayni durum + `--guncelle` -> exit 0; yedekte eski kurulum bayt-birebir (1 baytlik
                degisiklik dahil); `skills/` altinda hafiza-kur DISINDA klasor YOK
  K-PROJE       `--proje` -> `<kok>/.claude/skills/hafiza-kur/`; sahte HOME'a HIC yazilmadi;
                olmayan `--proje` -> exit 2
  K-ENV         kaynaga `scripts/deneme/x.md`, `scripts/__pycache__/y.pyc`, `.gizli`,
                `references/.gizli_dizin/z.md` enjekte -> kurulumda YOK; kurulu envanter paketle.sh'in
                zip envanteriyle AYNI. Calisan `bash` yoksa (paketle.sh artik `zip` ISTEMEZ; motorun `paket`
                komutunu cagirir) o ALT-OLCUM "OLCULEMEDI" basilir ve sonuc
                "YESIL (SINIRLI)" olur (sessiz yesil DEGIL); `--zip-zorla` ile exit 2
  K-MOTORYALNIZ motor tek basina bir dizine kopyalanip oradan kosulur -> exit 2, HOME'a yazilmadi
  K-SALTOKUNUR  (besli-paket/IS_EMRI_URUN_HAZIRLIK.md KALEM 4, 30 Eyl 2026) dosya sistemi yazmaya izin
                vermeyince -> exit 3; mesaj ENGEL OLAN dizini (`.claude` ya da `.claude/skills`) soyler,
                genel yakalayicinin ILGISIZ satirlarini (`kapi` onerisi · VAR OLMAYAN gecici dizine
                chmod) BASMAZ. DORT kol: A1/A2 ENJEKSIYONLA (her platformda: `mkdtemp` / son rename
                EACCES atar) · B/C GERCEK salt-okunur dizinle (yalniz POSIX + root DEGILKEN; aksi
                halde o ALT-OLCUM "OLCULEMEDI" basilir, sonuc "YESIL (SINIRLI)" olur)

MUTANTLAR (motor KOPYASINDA dizge sabotaji; hedef dizge motorda TAM 1 kez gecmeli, degilse
OLCULEMEDI — h14_bolme dersi). Her mutantin BEKLENEN kolu KIRMIZI yanmali:
  M-SK-OLCUM  olcum sokulur + kopyaya bozulma enjekte edilir      -> K-TAZE
  M-SK-EZME   catisma kontrolu sokulur (farkli kurulum sessizce degisir) -> K-FARKLI
  M-SK-YEDEK  yedege tasima yerine SILME                            -> K-GUNCELLE
  M-SK-SUZGEC suzgecten `deneme` cikarilir                          -> K-ENV
  M-SK-YER    yedek `skills/` ALTINA alinir (Claude Code orada SKILL.md bulani yukler) -> K-GUNCELLE
  M-SK-GENEL  `skill-kur`un dosya sistemi yakalayicisi sokulur (genel yakalayiciya duser)  -> K-SALTOKUNUR
  M-SK-RENAME son rename'in izin hatasi exit 3 yerine ESKI "olcum tutmadi" exit 1 olur    -> K-SALTOKUNUR
POZITIF KONTROL: temiz motorda tum kollar YESIL olmali; degilse mutant hukmu ANLAMSIZDIR -> exit 2.

CIKIS  0 yesil + tum mutantlar ISIRDI · 1 bir mutant KACTI · 2 OLCULEMEDI (pozitif kontrol tutmadi,
       capa yok, `--zip-zorla` + calisan bash yok) — sessiz PASS YOK
KULLANIM  python faz0/skill_kur_mutanti.py [motor] [--zip-zorla]
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

VARSAYILAN_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill",
                                "scripts", "hafiza.py")
KOK_DEPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIZGI = "-" * 84
YEDEK_AD = "hafiza-kur-yedek"


def _cikti_kodlamasini_guvenceye_al():   # Y-2 KORUMASI
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


class Olculemedi(Exception):
    """Duzenegin KENDISI kurulamadi — kapi/komut hukmu DEGIL."""


# ----------------------------------------------------------------- YARDIMCILAR
def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def kos(motor, args, home, cwd=None):
    """Motoru SAHTE ev dizininde kosar. Gercek HOME/USERPROFILE'a HIC dokunulmaz."""
    env = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env, cwd=cwd, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def agac(dizin):
    """{goreli yol: (sha, mtime_ns)} — SUZULMEMIS tum dosyalar."""
    out = {}
    for r0, _d, f0 in os.walk(dizin):
        for f in f0:
            p = os.path.join(r0, f)
            out[os.path.relpath(p, dizin).replace(os.sep, "/")] = (sha(p), os.stat(p).st_mtime_ns)
    return out


def bayt_agaci(dizin):
    return {r: v[0] for r, v in agac(dizin).items()}


def yeni_home(taban, ad):
    h = os.path.join(taban, ad)
    os.makedirs(h)
    return h


def skill_kopya(hedef, kaynak_skill, motor_metni=None):
    """Depodaki skill/ agacinin KOPYASI (artiklar haric); istenirse motor SABOTAJLI metinle degistirilir."""
    shutil.copytree(kaynak_skill, hedef, ignore=shutil.ignore_patterns("__pycache__", "deneme", ".*"))
    if motor_metni is not None:
        with open(os.path.join(hedef, "scripts", "hafiza.py"), "w", encoding="utf-8", newline="\n") as f:
            f.write(motor_metni)
    return os.path.join(hedef, "scripts", "hafiza.py")


def suzulmus(dizin):
    """paketle.sh -x kurali: nokta ile baslayan her sey, `deneme`, `__pycache__` DISI dosyalar."""
    out = {}
    for r0, d0, f0 in os.walk(dizin):
        d0[:] = [d for d in d0 if d not in ("deneme", "__pycache__") and not d.startswith(".")]
        for f in f0:
            if not f.startswith("."):
                p = os.path.join(r0, f)
                out[os.path.relpath(p, dizin).replace(os.sep, "/")] = sha(p)
    return out


def _yaz(p, icerik=b"x"):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(icerik)


def enjekte_et(skill_dir):
    """Kaynaga paketle.sh'in SUZDUGU artiklar."""
    _yaz(os.path.join(skill_dir, "scripts", "deneme", "x.md"))
    _yaz(os.path.join(skill_dir, "scripts", "__pycache__", "y.pyc"))
    _yaz(os.path.join(skill_dir, ".gizli"))
    _yaz(os.path.join(skill_dir, "references", ".gizli_dizin", "z.md"))
    _yaz(os.path.join(skill_dir, "scripts", ".nokta"))


def hedef_yolu(home):
    return os.path.join(home, ".claude", "skills", "hafiza-kur")


def yedekler(home):
    d = os.path.join(home, ".claude", YEDEK_AD)
    return sorted(os.path.join(d, x, "hafiza-kur") for x in os.listdir(d)) if os.path.isdir(d) else []


def surum_sha(motor, home):
    k, c = kos(motor, ["surum"], home)
    m = re.search(r"^sha256\s+([0-9A-Fa-f]{64})", c, re.M)
    return m.group(1).upper() if (k == 0 and m) else None


# ------------------------------------------------------------------------ KOLLAR
# Her kol: (durum, ayrinti, sinirli). durum: YESIL | KIRMIZI. sinirli: False ya da OLCULEMEDI kalan
# alt-olcumun etiketi ("zip" = K-ENV'in zip envanteri · "salt" = K-SALTOKUNUR'un gercek-izin kollari).
def _yesil(hata, ok="tamam"):
    return ("KIRMIZI", "; ".join(hata), False) if hata else ("YESIL", ok, False)


def kol_taze(ctx):
    home = yeni_home(ctx["taban"], "taze")
    k, c = kos(ctx["motor"], ["skill-kur"], home)
    hata = []
    if k != 0:
        hata.append("exit %d (0 bekleniyordu): %s" % (k, c.strip().splitlines()[-1][:80] if c.strip() else ""))
    hedef = hedef_yolu(home)
    if not os.path.isdir(hedef):
        return ("KIRMIZI", "hedef olusmadi", False)
    if bayt_agaci(hedef) != suzulmus(ctx["skill"]):
        hata.append("kurulu envanter/bayt != suzulmus kaynak")
    if surum_sha(os.path.join(hedef, "scripts", "hafiza.py"), home) != sha(ctx["motor"]):
        hata.append("kurulu motorun `surum` SHA'si kaynaktan farkli")
    if sorted(os.listdir(os.path.join(home, ".claude"))) != ["skills"]:
        hata.append(".claude/ altinda gecici artik: %s" % sorted(os.listdir(os.path.join(home, ".claude"))))
    return _yesil(hata, "%d dosya, envanter+bayt+surum SHA esit, artik yok" % len(bayt_agaci(hedef)))


def kol_ayni(ctx):
    home = yeni_home(ctx["taban"], "ayni")
    kos(ctx["motor"], ["skill-kur"], home)
    once, ust_once = agac(hedef_yolu(home)), sorted(os.listdir(os.path.join(home, ".claude")))
    k, c = kos(ctx["motor"], ["skill-kur"], home)
    hata = []
    if k != 0 or "ZATEN KURULU" not in c:
        hata.append("exit %d / 'ZATEN KURULU' basilmadi" % k)
    if agac(hedef_yolu(home)) != once:
        hata.append("hedefte bir dosyanin bayti/mtime'i DEGISTI")
    if sorted(os.listdir(os.path.join(home, ".claude"))) != ust_once:
        hata.append(".claude/ icerigi degisti")
    return _yesil(hata, "ZATEN KURULU, %d dosyanin bayti+mtime'i ayni" % len(once))


def _farkli_hazirla(ctx, ad):
    home = yeni_home(ctx["taban"], ad)
    kos(ctx["motor"], ["skill-kur"], home)
    with open(os.path.join(hedef_yolu(home), "scripts", "hafiza.py"), "ab") as f:
        f.write(b"#")
    return home


def kol_farkli(ctx):
    home = _farkli_hazirla(ctx, "farkli")
    once = agac(hedef_yolu(home))
    k, c = kos(ctx["motor"], ["skill-kur"], home)
    hata = []
    if k != 2:
        hata.append("exit %d (2 bekleniyordu)" % k)
    if agac(hedef_yolu(home)) != once:
        hata.append("hedef DEGISTI (bayt-birebir ayni kalmaliydi)")
    shalar = set(re.findall(r"\b[0-9A-F]{64}\b", c))
    if len(shalar) != 2:
        hata.append("iki farkli SHA basilmadi (%d)" % len(shalar))
    if os.path.isdir(os.path.join(home, ".claude", YEDEK_AD)):
        hata.append("`--guncelle` yokken yedek olustu")
    return _yesil(hata, "exit 2, hedef bayt-birebir ayni, iki SHA basildi")


def kol_guncelle(ctx):
    home = _farkli_hazirla(ctx, "guncelle")
    eski = bayt_agaci(hedef_yolu(home))
    k, c = kos(ctx["motor"], ["skill-kur", "--guncelle"], home)
    hata = []
    if k != 0:
        hata.append("exit %d (0 bekleniyordu)" % k)
    yd = yedekler(home)
    if len(yd) != 1 or not os.path.isdir(yd[0]) or bayt_agaci(yd[0]) != eski:
        hata.append("yedekte eski kurulum bayt-birebir DEGIL (yedek=%d)" % len(yd))
    if sorted(os.listdir(os.path.join(home, ".claude", "skills"))) != ["hafiza-kur"]:
        hata.append("skills/ altinda hafiza-kur DISINDA klasor: %s"
                    % sorted(os.listdir(os.path.join(home, ".claude", "skills"))))
    if bayt_agaci(hedef_yolu(home)) != suzulmus(ctx["skill"]):
        hata.append("yeni kurulum kaynakla ayni degil")
    return _yesil(hata, "yedek bayt-birebir (1 baytlik degisiklik dahil), skills/ tek klasor, yeni kurulum esit")


def kol_proje(ctx):
    home, proje = yeni_home(ctx["taban"], "proje_home"), yeni_home(ctx["taban"], "proje_kok")
    k, _c = kos(ctx["motor"], ["skill-kur", "--proje", proje], home)
    hata = []
    hedef = os.path.join(proje, ".claude", "skills", "hafiza-kur")
    if k != 0 or bayt_agaci(hedef) != suzulmus(ctx["skill"]):
        hata.append("exit %d / <proje>/.claude/skills/hafiza-kur/ kaynakla esit degil" % k)
    if os.listdir(home):
        hata.append("sahte HOME'a YAZILDI: %s" % os.listdir(home))
    k2, _ = kos(ctx["motor"], ["skill-kur", "--proje", os.path.join(ctx["taban"], "yok_dizin")], home)
    if k2 != 2:
        hata.append("olmayan --proje exit %d (2 bekleniyordu)" % k2)
    return _yesil(hata, "proje hedefi dogru, HOME'a HIC yazilmadi, olmayan --proje exit 2")


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


def zip_envanteri(ctx):
    """paketle.sh'i injekte edilmis kaynakla kosar. (zip DOSYA envanteri | None, sebep): None =
    bu platformda kosulamiyor (calisan bash yok ya da paketle.sh paket uretmedi) — bu bir
    SINIRLI durumudur; yalniz `--zip-zorla` (CI ubuntu) onu sert hataya cevirir."""
    bash = bash_bul()
    if not bash:
        return None, "calisan bash yok"
    d = os.path.join(ctx["taban"], "paketle")
    os.makedirs(d)
    shutil.copy(os.path.join(KOK_DEPO, "paketle.sh"), d)
    shutil.copytree(ctx["skill_enjekte"], os.path.join(d, "skill"))
    r = subprocess.run([bash, "paketle.sh"], cwd=d, capture_output=True, text=True, timeout=300,
                       encoding="utf-8", errors="replace")
    z = os.path.join(d, "hafiza-kur.skill")
    if not os.path.isfile(z):
        return None, "paketle.sh paket uretmedi (exit %d)" % r.returncode
    with zipfile.ZipFile(z) as zf:
        return {n for n in zf.namelist() if not n.endswith("/")}, ""


def kol_env(ctx):
    home = yeni_home(ctx["taban"], "env")
    k, _c = kos(ctx["motor_enjekte"], ["skill-kur"], home)
    hedef = hedef_yolu(home)
    hata = []
    if k != 0 or not os.path.isdir(hedef):
        return ("KIRMIZI", "exit %d, hedef yok" % k, False)
    kurulu = set(bayt_agaci(hedef))
    for artik in ("scripts/deneme/x.md", "scripts/__pycache__/y.pyc", ".gizli",
                  "references/.gizli_dizin/z.md", "scripts/.nokta"):
        if artik in kurulu:
            hata.append("suzulmesi gereken artik KURULDU: %s" % artik)
    z, sebep = zip_envanteri(ctx)
    sinirli = "zip" if z is None else False
    if z is not None and z != kurulu:
        hata.append("kurulu envanter paketle.sh zip envanterinden FARKLI (yalniz kurulu: %s · yalniz zip: %s)"
                    % (sorted(kurulu - z)[:3], sorted(z - kurulu)[:3]))
    if hata:
        return ("KIRMIZI", "; ".join(hata), sinirli)
    return ("YESIL", "artiklar suzuldu; zip envanteri: %s" % ("AYNI" if z is not None else
            "OLCULEMEDI (%s)" % sebep), sinirli)


def kol_motoryalniz(ctx):
    home = yeni_home(ctx["taban"], "solo_home")
    solo = os.path.join(ctx["taban"], "solo_dizin", "x")
    os.makedirs(solo)
    shutil.copy(ctx["motor"], os.path.join(solo, "hafiza.py"))
    k, c = kos(os.path.join(solo, "hafiza.py"), ["skill-kur"], home)
    hata = []
    if k != 2 or "skill dizini degil" not in c:
        hata.append("exit %d (2 + 'skill dizini degil' bekleniyordu)" % k)
    if os.listdir(home):
        hata.append("sahte HOME'a YAZILDI")
    return _yesil(hata, "exit 2 'kaynak skill dizini degil', HOME'a yazilmadi")


# Enjeksiyon sarmalayicisi: motoru `runpy` ile ayni `__main__` yolundan kosar (yani `_guvenli_calistir`
# dahil) ama bir dosya sistemi cagrisini EACCES ile dusurur. Izin MODELIYLE degil ENJEKSIYONLA:
# `os.chmod` Windows'ta dizinlerde etkisizdir ve root'ta izin hic ates etmez (fazA dersi).
ENJEKSIYON = '''import errno, os, runpy, sys, tempfile
_mod, _motor = os.environ["HK_ENJEKTE"], sys.argv[1]
if _mod == "mkdtemp":
    def _engelli(*a, **k):
        raise PermissionError(errno.EACCES, "Permission denied",
                              os.path.join(k.get("dir") or ".", ".hafiza-kur-kur-enjekte"))
    tempfile.mkdtemp = _engelli
else:
    _gercek = os.replace
    def _engelli(src, dst, *a, **k):
        if os.path.basename(dst) == "hafiza-kur" and os.path.basename(os.path.dirname(dst)) == "skills":
            raise PermissionError(errno.EACCES, "Permission denied", src, None, dst)
        return _gercek(src, dst, *a, **k)
    os.replace = _engelli
sys.argv = [_motor] + sys.argv[2:]
runpy.run_path(_motor, run_name="__main__")
'''


def kos_enjekte(ctx, mod, home):
    """Motoru ENJEKSIYON sarmalayicisiyla kosar (`mod`: mkdtemp | replace). (kod, cikti)."""
    yol = os.path.join(ctx["taban"], "enjekte.py")
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENJEKSIYON)
    env = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONIOENCODING="utf-8", HK_ENJEKTE=mod)
    r = subprocess.run([sys.executable, "-X", "utf8", yol, ctx["motor"], "skill-kur"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
                       timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def fs_hukmu_hatalari(ad, k, c, engel):
    """Dosya sistemi hukmunun 5 sartini olcer: exit 3 · ENGEL OLAN dizin adi · `kapi` onerisi YOK ·
    VAR OLMAYAN gecici dizine chmod YOK · ham traceback YOK."""
    hata = []
    if k != 3:
        hata.append("%s: exit %d (3 bekleniyordu): %s" % (ad, k, c.strip().splitlines()[-1][:70] if c.strip() else ""))
    if os.path.normcase(os.path.normpath(engel)) not in os.path.normcase(c):
        hata.append("%s: engel olan dizin gosterilmedi (%s)" % (ad, engel))
    if "hafiza.py kapi" in c:
        hata.append("%s: ILGISIZ `kapi` onerisi basildi" % ad)
    if ".hafiza-kur-kur-" in c:
        hata.append("%s: VAR OLMAYAN gecici dizine chmod onerisi basildi" % ad)
    if "Traceback" in c:
        hata.append("%s: ham traceback" % ad)
    return hata


def gercek_izin_uygulanir(taban):
    """chmod 0555 bu ortamda gercekten YAZMAYI engelliyor mu? (Windows/root: hayir -> None)"""
    if os.name != "posix" or not hasattr(os, "geteuid") or os.geteuid() == 0:
        return "POSIX degil ya da root"
    d = os.path.join(taban, "izin_sondaji")
    os.makedirs(d)
    os.chmod(d, 0o555)
    try:
        with open(os.path.join(d, "x"), "w"):
            return "chmod 0555 yazmayi ENGELLEMEDI"
    except OSError:
        return None
    finally:
        os.chmod(d, 0o755)


def kol_saltokunur(ctx):
    hata = []
    # A1/A2: ENJEKSIYON (her platform). A1: `.claude` icinde gecici dizin acilamaz · A2: son rename
    # `skills/` icine yapilamaz. Gercek ev dizinine degil SAHTE HOME'a bakar.
    h1 = yeni_home(ctx["taban"], "salt_a1")
    taban1 = os.path.join(h1, ".claude")
    os.makedirs(taban1)
    k, c = kos_enjekte(ctx, "mkdtemp", h1)
    hata += fs_hukmu_hatalari("A1", k, c, taban1)
    if os.listdir(taban1):
        hata.append("A1: `.claude/` icinde artik var: %s" % os.listdir(taban1))
    h2 = yeni_home(ctx["taban"], "salt_a2")
    skills2 = os.path.join(h2, ".claude", "skills")
    os.makedirs(skills2)
    k, c = kos_enjekte(ctx, "replace", h2)
    hata += fs_hukmu_hatalari("A2", k, c, skills2)
    if os.listdir(skills2) or sorted(os.listdir(os.path.dirname(skills2))) != ["skills"]:
        hata.append("A2: hedefte/`.claude/` icinde artik var")
    # B/C: GERCEK salt-okunur dizin (yalniz POSIX + root degilken)
    sebep = gercek_izin_uygulanir(ctx["taban"])
    if sebep is None:
        for ad, alt in (("B", ".claude"), ("C", os.path.join(".claude", "skills"))):
            h = yeni_home(ctx["taban"], "salt_" + ad.lower())
            ro = os.path.join(h, alt)
            os.makedirs(ro)
            os.chmod(ro, 0o555)
            try:
                k, c = kos(ctx["motor"], ["skill-kur"], h)
            finally:
                os.chmod(ro, 0o755)
            hata += fs_hukmu_hatalari(ad, k, c, ro)
    if hata:
        return ("KIRMIZI", "; ".join(hata), False)
    if sebep:
        return ("YESIL", "A1+A2 enjeksiyon: exit 3, engel olan dizin gosterildi, `kapi`/chmod-gecici satiri YOK · "
                "B+C gercek salt-okunur: OLCULEMEDI (%s)" % sebep, "salt")
    return ("YESIL", "A1+A2 enjeksiyon ve B+C gercek salt-okunur dizin: exit 3, engel olan dizin gosterildi, "
            "`kapi`/chmod-gecici satiri YOK", False)


KOLLAR = [("K-TAZE", kol_taze), ("K-AYNI", kol_ayni), ("K-FARKLI", kol_farkli),
          ("K-GUNCELLE", kol_guncelle), ("K-PROJE", kol_proje), ("K-ENV", kol_env),
          ("K-MOTORYALNIZ", kol_motoryalniz), ("K-SALTOKUNUR", kol_saltokunur)]

# ----------------------------------------------------------------------- MUTANTLAR
# (ad, aciklama, eski, yeni, BEKLENEN kol)
MUTANTLAR = [
    ("M-SK-OLCUM", "olcum sokulur + kopyaya bozulma enjekte edilir",
     "        ayak = _skill_kur_olc(kd, kopya, sha_k)\n",
     '        with open(os.path.join(kopya, "scripts", "hafiza.py"), "ab") as _f:\n'
     '            _f.write(b"#")\n        ayak = None\n', "K-TAZE"),
    ("M-SK-EZME", "catisma kontrolu sokulur (farkli kurulum sessizce degisir)",
     "    if guncelle:\n        return None\n", "    return None\n", "K-FARKLI"),
    ("M-SK-YEDEK", "yedege tasima yerine SILME",
     "    os.replace(hedef, yol)\n", "    shutil.rmtree(hedef)\n", "K-GUNCELLE"),
    ("M-SK-SUZGEC", "suzgecten `deneme` cikarilir",
     '_SKILL_KUR_HARIC_DIZIN = ("deneme", "__pycache__")', '_SKILL_KUR_HARIC_DIZIN = ("__pycache__",)',
     "K-ENV"),
    ("M-SK-YER", "yedek `skills/` ALTINA alinir",
     'os.path.join(taban, "hafiza-kur-yedek")', 'os.path.join(taban, "skills", "hafiza-kur-yedek")',
     "K-GUNCELLE"),
    ("M-SK-GENEL", "dosya sistemi yakalayicisi sokulur (genel yakalayiciya duser)",
     '        return _dosya_sistemi_hukmu("skill-kur", _engel_dizin(e), "baska bir kokle dene: --proje <kok>")\n',
     "        raise\n", "K-SALTOKUNUR"),
    ("M-SK-RENAME", "son rename'in izin hatasi eski 'olcum tutmadi' exit 1 olur",
     '            if getattr(e, "errno", None) in _FS_ENGEL_KODLARI:\n                raise ',
     '            if False:\n                raise ', "K-SALTOKUNUR"),
]


def bir_kez(metin, eski):
    n = metin.count(eski)
    if n != 1:
        raise Olculemedi("hedef dizge motorda %d kez geciyor (1 olmali): %r" % (n, eski[:60]))
    return metin


def kollari_kos(kaynak_skill, motor_metni, taban, zip_zorla):
    """Tum kollari (motor_metni None = temiz motor) AYRI skill kopyalarinda kosar."""
    skill = os.path.join(taban, "skill")
    motor = skill_kopya(skill, kaynak_skill, motor_metni)
    enj = os.path.join(taban, "skill_enjekte")
    motor_enj = skill_kopya(enj, kaynak_skill, motor_metni)
    enjekte_et(enj)
    ctx = {"taban": taban, "skill": skill, "motor": motor, "skill_enjekte": enj, "motor_enjekte": motor_enj}
    sonuc = []
    for ad, fn in KOLLAR:
        try:
            durum, ayr, sinirli = fn(ctx)
        except Olculemedi as e:
            durum, ayr, sinirli = "OLCULEMEDI", str(e), False
        except Exception as e:                                    # noqa: BLE001 — kol coktu = kirmizi degil, OLCULEMEDI
            durum, ayr, sinirli = "OLCULEMEDI", "%s: %s" % (type(e).__name__, str(e)[:100]), False
        sonuc.append((ad, durum, ayr, sinirli))
    return sonuc


SINIR_NOTU = {
    "zip": "\n  SINIRLI: K-ENV'in zip envanteri karsilastirmasi OLCULEMEDI (calisan bash yok); "
           "CI ubuntu kolu `--zip-zorla` ile olcer.",
    "salt": "\n  SINIRLI: K-SALTOKUNUR'un GERCEK salt-okunur kollari (B/C) OLCULEMEDI (POSIX degil ya da "
            "root); A1/A2 enjeksiyon kollari olculdu, gercek-izin kollarini CI ubuntu/macOS olcer.",
}


def main():
    _cikti_kodlamasini_guvenceye_al()
    zip_zorla = "--zip-zorla" in sys.argv
    poz = [a for a in sys.argv[1:] if not a.startswith("--")]
    motor = os.path.abspath(poz[0] if poz else VARSAYILAN_MOTOR)
    if not os.path.isfile(motor):
        print("SONUC: OLCULEMEDI — motor yok: %s" % motor)
        return 2
    kaynak_skill = os.path.dirname(os.path.dirname(motor))
    metin = open(motor, encoding="utf-8", newline="").read()
    print(CIZGI)
    print("SKILL-KUR OLCERI · motor %s · platform %s · calisan bash: %s" % (
        motor, sys.platform, "VAR" if bash_bul() else "YOK"))
    print(CIZGI)
    gercek_home = os.path.expanduser("~")
    onceki = sorted(os.listdir(os.path.join(gercek_home, ".claude", "skills"))) \
        if os.path.isdir(os.path.join(gercek_home, ".claude", "skills")) else None

    taban0 = tempfile.mkdtemp(prefix="skill_kur_olcer_")
    try:
        print("POZITIF KONTROL (temiz motor, %d kol):" % len(KOLLAR))
        temiz = kollari_kos(kaynak_skill, None, os.path.join(taban0, "temiz"), zip_zorla)
        for ad, durum, ayr, _s in temiz:
            print("  %-14s %-10s %s" % (ad, durum, ayr))
        if any(d != "YESIL" for _, d, _, _ in temiz):
            print("\nSONUC: OLCULEMEDI — pozitif kontrol tutmadi (temiz motorda kirmizi/olculemeyen kol); "
                  "mutant hukumleri ANLAMSIZ, mutantlar KOSULMADI.")
            return 2
        sinirli = sorted({s for _, _, _, s in temiz if s})
        if "zip" in sinirli and zip_zorla:
            print("\nSONUC: OLCULEMEDI — `--zip-zorla` verildi ama calisan bash yok (K-ENV zip karsilastirmasi).")
            return 2

        print("\nMUTANTLAR (her biri BEKLENEN kolu KIRMIZI yakmali):")
        isirdi, kacti, olculemedi = [], [], []
        for ad, acik, eski, yeni, beklenen in MUTANTLAR:
            try:
                sab = bir_kez(metin, eski).replace(eski, yeni, 1)
                compile(sab, "<mutant>", "exec")
                kollar = kollari_kos(kaynak_skill, sab, os.path.join(taban0, ad), zip_zorla)
            except (Olculemedi, SyntaxError) as e:
                olculemedi.append(ad)
                print("  %-12s OLCULEMEDI: %s" % (ad, e))
                continue
            kirmizi = [k for k, d, _, _ in kollar if d != "YESIL"]
            if beklenen in kirmizi:
                isirdi.append(ad)
                print("  %-12s ISIRDI ✓  %s -> KIRMIZI: %s" % (ad, acik, ",".join(kirmizi)))
            else:
                kacti.append(ad)
                print("  %-12s KACTI ✗  %s -> beklenen %s YESIL kaldi (kirmizi: %s)"
                      % (ad, acik, beklenen, ",".join(kirmizi) or "yok"))
    finally:
        shutil.rmtree(taban0, ignore_errors=True)

    sonra = sorted(os.listdir(os.path.join(gercek_home, ".claude", "skills"))) \
        if os.path.isdir(os.path.join(gercek_home, ".claude", "skills")) else None
    print(CIZGI)
    if sonra != onceki:
        print("SONUC: KIRMIZI — GERCEK ev dizinindeki skills/ degisti (%s -> %s): olcer sahte HOME'u asti!"
              % (onceki, sonra))
        return 1
    print("GERCEK ev dizini skills/ olcum oncesi/sonrasi AYNI (%s)." % (onceki,))
    if olculemedi:
        print("SONUC: OLCULEMEDI — %d mutant kurulamadi: %s" % (len(olculemedi), ", ".join(olculemedi)))
        return 2
    if kacti:
        print("SONUC: KIRMIZI — %d mutant KACTI: %s" % (len(kacti), ", ".join(kacti)))
        return 1
    print("SONUC: %s — %d kol yesil, %d/%d mutant ISIRDI (%s)%s"
          % ("YESIL (SINIRLI)" if sinirli else "YESIL", len(KOLLAR), len(isirdi), len(MUTANTLAR),
             ", ".join(isirdi), "".join(SINIR_NOTU[x] for x in sinirli)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

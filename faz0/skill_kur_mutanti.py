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
  K-COP         (besli-paket/IS_EMRI_TAKMA_AD_BEYAZ_LISTE.md KALEM 2, 1 Eki 2026) kaynakta BEYAZ LISTE DISI cop
                (`scripts/deneme_b4e/…`, `deneme2/…`, `references/notlar.txt`, `scripts/alt/y.py`, `SKILL.md.bak`
                …) varken `skill-kur` -> exit 0; kurulan envanter == beyaz liste (BU harness'in kendi okuyusu:
                `SKILL.md` · `references/*.md` · `scripts/*.py`, motorun sabitlerine BAKILMAZ); her cop icin
                `DISARIDA BIRAKILDI: <rel> (beyaz liste disi)` satiri (ne eksik ne fazla); `__pycache__`/nokta
                dosyalari icin satir YOK. Ayrica KURULU hedefe cop sizmissa (eski kara liste doneminden kalan
                kurulum) `skill-kur` CATISMA (exit 2) der, `--guncelle` yedekleyip temizini kurar; kaynakta DIZIN BAGLANTISI
                (symlink/junction) varsa REDDEDER (exit 2, HOME'a yazmaz): `DISARIDA` satirlari STDOUT'tan ve LISTE olarak okunur
  K-MOTORYALNIZ motor tek basina bir dizine kopyalanip oradan kosulur -> exit 2, HOME'a yazilmadi
  K-SALTOKUNUR  (besli-paket/IS_EMRI_URUN_HAZIRLIK.md KALEM 4, 30 Eyl 2026) dosya sistemi yazmaya izin
                vermeyince -> exit 3; mesaj ENGEL OLAN dizini (`.claude` ya da `.claude/skills`) soyler,
                genel yakalayicinin ILGISIZ satirlarini (`kapi` onerisi · VAR OLMAYAN gecici dizine
                chmod) BASMAZ. ALTI kol: A1/A2/A3 ENJEKSIYONLA (her platformda: `mkdtemp` / son rename /
                yedege tasima EACCES atar; A3'te ayrica `os.access(skills, W_OK)` sahte False) · B/C/D GERCEK salt-okunur dizinle (yalniz POSIX + root DEGILKEN; aksi
                halde o ALT-OLCUM "OLCULEMEDI" basilir, sonuc "YESIL (SINIRLI)" olur); D = var olan
                FARKLI kurulum + salt-okunur skills/ + `--guncelle` (eski kurulum SAGLAM kalmali)

MUTANTLAR (motor KOPYASINDA dizge sabotaji; hedef dizge motorda TAM 1 kez gecmeli, degilse
OLCULEMEDI — h14_bolme dersi). Her mutantin BEKLENEN kolu KIRMIZI yanmali:
  M-SK-OLCUM  olcum sokulur + kopyaya bozulma enjekte edilir      -> K-TAZE
  M-SK-EZME   catisma kontrolu sokulur (farkli kurulum sessizce degisir) -> K-FARKLI
  M-SK-YEDEK  yedege tasima yerine SILME                            -> K-GUNCELLE
  M-SK-BEYAZ  beyaz liste sokulur (her dosya beyaz: yuruyus + yalniz __pycache__/nokta kara listesi) -> K-COP
              (eski `M-SK-SUZGEC` "suzgecten `deneme` cikarilir" bu mutantla BIRLESTI: beyaz listede `deneme`
              diye bir kural kalmadi; ayni sokum K-ENV'i de kirmizi yakar, ikisi de beklenen)
  M-SK-BAGLANTI  `skill-kur`un kaynakta dizin baglantisi reddi sokulur (eksik kurulum sessizce exit 0) -> K-COP
  M-SK-HEDEF  KURULU hedefin envanteri de beyaz listeyle suzulur (eski kurulumdaki cop gorunmez) -> K-COP
  M-SK-YER    yedek `skills/` ALTINA alinir (Claude Code orada SKILL.md bulani yukler) -> K-GUNCELLE
  M-SK-GENEL  `skill-kur`un dosya sistemi yakalayicisi sokulur (genel yakalayiciya duser)  -> K-SALTOKUNUR
  M-SK-RENAME son rename'in izin hatasi exit 3 yerine ESKI "olcum tutmadi" exit 1 olur    -> K-SALTOKUNUR
  M-SK-ENGEL  engel dizin secimi sokulur: `--guncelle` + salt-okunur skills/ iken YAZILABILIR yedek
              dizini "engel" diye gosterilir (bagimsiz tur 30 Eyl 2026 bunu elle yeniden uretti)  -> K-SALTOKUNUR
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
    """{goreli yol: sha}: BEYAZ listenin BU harness'in kendi okuyusuyla beklenen kumesi (`beyaz_beklenen`; motorun
    sabitlerine BAKMAZ). Eskiden paketle.sh'in kara listesi (`deneme` tam ad) idi: kaynakta `deneme_x/` varken dogru
    calisan motoru KIRMIZI gosterirdi (bagimsiz inceleme 1 Eki 2026)."""
    return {r: sha(os.path.join(dizin, *r.split("/"))) for r in beyaz_beklenen(dizin)}


def _yaz(p, icerik=b"x"):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(icerik)


# K-COP: beyaz liste DISI cop (her biri icin `DISARIDA BIRAKILDI:` satiri BEKLENIR; `scripts/deneme/` dahil: beyaz
# listede `deneme` istisnasi YOK) ve GURULTU (nokta/__pycache__: satir YOK).
COP_DOSYALAR = ("scripts/deneme_b4e/arsiv/PROJE_HAFIZA.md", "scripts/deneme2/arsiv/PROJE_HAFIZA.md",
                "scripts/deneme/k.md", "references/notlar.txt", "scripts/yan.sh", "scripts/alt/y.py",
                "SKILL.md.bak", "notlar/x.md")
GURULTU_DOSYALAR = ("scripts/__pycache__/y.pyc", ".gizli", "references/.gizli_dizin/z.md", "scripts/.nokta")
_DISARIDA = re.compile(r"^DISARIDA BIRAKILDI: (.+) \(beyaz liste disi\)$", re.M)


def cop_enjekte_et(skill_dir):
    for rel in COP_DOSYALAR + GURULTU_DOSYALAR:
        _yaz(os.path.join(skill_dir, *rel.split("/")))


def beyaz_beklenen(skill_dir):
    """BEYAZ listenin BU harness'in kendi okuyusuyla beklenen kumesi (motorun sabitlerine BAKMAZ): kokte
    `SKILL.md`, `references/*.md` ve `scripts/*.py` (tek seviye). Temiz kopyadan okunur."""
    out = {"SKILL.md"}
    for alt, uzanti in (("references", ".md"), ("scripts", ".py")):
        out |= {alt + "/" + f for f in os.listdir(os.path.join(skill_dir, alt))
                if f.endswith(uzanti) and not f.startswith(".")}
    return out


def disarida_beklenen(skill_dir):
    """Beyaz liste DISINDA kalan, nokta/__pycache__ OLMAYAN dosyalar (BU harness'in kendi yuruyusu): `DISARIDA
    BIRAKILDI:` satirlarinin tam kumesi. Liste olarak karsilastirilir (tekrar da hata)."""
    bek, out = beyaz_beklenen(skill_dir), []
    for r0, d0, f0 in os.walk(skill_dir):
        d0[:] = [d for d in d0 if d != "__pycache__" and not d.startswith(".")]
        for f in f0:
            if not f.startswith("."):
                rel = os.path.relpath(os.path.join(r0, f), skill_dir).replace(os.sep, "/")
                if rel not in bek:
                    out.append(rel)
    return sorted(out)


def dizin_baglantisi(yol, hedef):
    """`yol`u `hedef`e giden DIZIN BAGLANTISI yapar (POSIX symlink, Windows junction — ayricalik istemez).
    None = kuruldu; str = KURULAMADI sebebi."""
    try:
        if os.name == "nt":
            r = subprocess.run(["cmd", "/c", "mklink", "/J", yol, hedef], capture_output=True)
            if r.returncode != 0:
                return "junction kurulamadi: %s" % r.stdout.decode("cp850", "replace").strip()[:80]
        else:
            os.symlink(hedef, yol, target_is_directory=True)
    except OSError as e:
        return "symlink kurulamadi: %s" % e
    return None if os.path.isdir(yol) else "baglanti dizin olarak acilmiyor"


def kos_ayri(motor, args, home):
    """`kos` gibi ama stdout ve stderr AYRI: `DISARIDA BIRAKILDI:` satirlari STDOUT'a basilmali (is emri)."""
    env = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env, timeout=300)
    return r.returncode, r.stdout or "", r.stderr or ""


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


def kol_cop(ctx):
    home = yeni_home(ctx["taban"], "cop")
    k, c, _e = kos_ayri(ctx["motor_cop"], ["skill-kur"], home)
    hedef = hedef_yolu(home)
    if k != 0 or not os.path.isdir(hedef):
        return ("KIRMIZI", "exit %d, hedef yok (cop varken kurulum exit 0 vermeliydi)" % k, False)
    hata = []
    kurulu, bek = set(bayt_agaci(hedef)), beyaz_beklenen(ctx["skill"])
    if kurulu != bek:
        hata.append("kurulu envanter beyaz listeden FARKLI (fazla: %s · eksik: %s)"
                    % (sorted(kurulu - bek)[:3], sorted(bek - kurulu)[:3]))
    bildirilen, beklenen = sorted(_DISARIDA.findall(c)), disarida_beklenen(ctx["skill_cop"])
    if bildirilen != beklenen:
        hata.append("STDOUT'taki DISARIDA satirlari beklenenden FARKLI (bildirilmeyen: %s · fazladan/tekrar: %s)"
                    % (sorted(set(beklenen) - set(bildirilen))[:3],
                       sorted(x for x in set(bildirilen) if bildirilen.count(x) > beklenen.count(x) or x not in beklenen)[:3]))
    gurultu = [g for g in GURULTU_DOSYALAR if g in c]
    if gurultu:
        hata.append("gurultu dosyasi icin DISARIDA satiri basildi: %s" % gurultu[:2])
    # KURULU hedefe cop sizmis (eski kara liste doneminden kalan kurulum): FARKLI kurulum sayilmali
    _yaz(os.path.join(hedef, "scripts", "deneme_b4e", "arsiv", "PROJE_HAFIZA.md"))
    once = agac(hedef)
    k2, c2 = kos(ctx["motor_cop"], ["skill-kur"], home)
    if k2 != 2 or "CATISMA" not in c2:
        hata.append("kurulu hedefte cop varken `skill-kur` exit %d (2 + CATISMA bekleniyordu): ZATEN KURULU demek sizintiyi gizler" % k2)
    if agac(hedef) != once:
        hata.append("CATISMA'da hedef DEGISTI")
    k3, _c3 = kos(ctx["motor_cop"], ["skill-kur", "--guncelle"], home)
    yd = yedekler(home)
    if k3 != 0 or set(bayt_agaci(hedef)) != bek:
        hata.append("`--guncelle` sonrasi kurulu envanter beyaz liste DEGIL (exit %d)" % k3)
    if len(yd) != 1 or "scripts/deneme_b4e/arsiv/PROJE_HAFIZA.md" not in bayt_agaci(yd[0]):
        hata.append("yedek, sizmis copu SAKLAMADI (silme yok kurali)")
    # KAYNAKTA dizin baglantisi (beyaz listedeki `references/` bir baglanti): `skill-kur` REDDETMELI (exit 2), eksik
    # kurulumu exit 0 ile "KURULDU" DEMEMELI ve HOME'a hicbir sey yazmamali (`paket` ile ayni; bagimsiz inceleme bulgusu)
    sinirli = False
    bd = os.path.join(ctx["taban"], "cop_bagli")
    shutil.copytree(ctx["skill"], os.path.join(bd, "skill"))
    ref, dis = os.path.join(bd, "skill", "references"), os.path.join(bd, "dis_references")
    shutil.move(ref, dis)
    sebep = dizin_baglantisi(ref, dis)
    if sebep:
        sinirli = "bag"
    else:
        hb = yeni_home(ctx["taban"], "cop_bagli_home")
        kb, cb, _eb = kos_ayri(os.path.join(bd, "skill", "scripts", "hafiza.py"), ["skill-kur"], hb)
        if kb != 2 or "dizin baglantisi" not in cb:
            hata.append("kaynakta dizin baglantisi varken `skill-kur` exit %d (2 + 'dizin baglantisi' bekleniyordu): "
                        "eksik kurulum SESSIZCE kurulur" % kb)
        if os.listdir(hb):
            hata.append("dizin baglantili kaynakta `skill-kur` HOME'a YAZDI: %s" % os.listdir(hb))
    if hata:
        return ("KIRMIZI", "; ".join(hata), sinirli)
    return ("YESIL", "cop varken %d dosya kuruldu (= beyaz liste) · %d cop icin STDOUT'ta DISARIDA satiri (ne eksik ne fazla) · "
                     "gurultu sessiz · kurulu hedefteki cop CATISMA, --guncelle yedekler · dizin baglantisi: %s"
            % (len(kurulu), len(bildirilen), "REDDEDILDI (exit 2)" if not sebep else "OLCULEMEDI (%s)" % sebep), sinirli)


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
elif _mod == "yedek":
    _gercek, _erisim0 = os.replace, os.access
    def _engelli(src, dst, *a, **k):
        if os.path.basename(src) == "hafiza-kur" and os.path.basename(os.path.dirname(os.path.dirname(dst))) == "hafiza-kur-yedek":
            raise PermissionError(errno.EACCES, "Permission denied", src, None, dst)
        return _gercek(src, dst, *a, **k)
    def _erisim(yol, mod, *a, **k):
        if mod == os.W_OK and os.path.basename(os.path.normpath(str(yol))) == "skills":
            return False
        return _erisim0(yol, mod, *a, **k)
    os.replace, os.access = _engelli, _erisim
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


def kos_enjekte(ctx, mod, home, komut=("skill-kur",)):
    """Motoru ENJEKSIYON sarmalayicisiyla kosar (`mod`: mkdtemp | replace | yedek). (kod, cikti)."""
    yol = os.path.join(ctx["taban"], "enjekte.py")
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENJEKSIYON)
    env = dict(os.environ, HOME=home, USERPROFILE=home, PYTHONIOENCODING="utf-8", HK_ENJEKTE=mod)
    r = subprocess.run([sys.executable, "-X", "utf8", yol, ctx["motor"]] + list(komut),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
                       timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def fs_hukmu_hatalari(ad, k, c, engel):
    """Dosya sistemi hukmunun 5 sartini olcer: exit 3 · ENGEL OLAN dizin adi · `kapi` onerisi YOK ·
    VAR OLMAYAN gecici dizine chmod YOK · ham traceback YOK."""
    hata = []
    if k != 3:
        hata.append("%s: exit %d (3 bekleniyordu): %s" % (ad, k, c.strip().splitlines()[-1][:70] if c.strip() else ""))
    satirlar = [os.path.normcase(x.strip()) for x in c.splitlines()]
    if os.path.normcase("Engel olan yer: %s" % os.path.normpath(engel)) not in satirlar:
        hata.append("%s: `Engel olan yer: %s` SATIRI yok" % (ad, engel))
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
    # A3: var olan FARKLI kurulum + `--guncelle`: yedege tasima EACCES atar ve `skills/` yazilamaz gorunur
    # (her platformda; engel dizin SECIMI: yazilabilir yedek dizini DEGIL `skills/` gosterilmeli)
    h3 = _farkli_hazirla(ctx, "salt_a3")
    skills3, eski3 = os.path.join(h3, ".claude", "skills"), bayt_agaci(hedef_yolu(h3))
    k, c = kos_enjekte(ctx, "yedek", h3, ("skill-kur", "--guncelle"))
    hata += fs_hukmu_hatalari("A3", k, c, skills3)
    if bayt_agaci(hedef_yolu(h3)) != eski3:
        hata.append("A3: var olan kurulum DEGISTI")
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
        # D: var olan FARKLI kurulum + salt-okunur skills/ + `--guncelle`: rename hedef dizine yapilamaz;
        # ENGEL `skills/`tir (yedek dizini yazilabilirdir — yanlis dizin gostermek kolay hata), eski kurulum SAGLAM
        hd = _farkli_hazirla(ctx, "salt_d")
        skills_d = os.path.join(hd, ".claude", "skills")
        eski_d = bayt_agaci(hedef_yolu(hd))
        os.chmod(skills_d, 0o555)
        try:
            k, c = kos(ctx["motor"], ["skill-kur", "--guncelle"], hd)
        finally:
            os.chmod(skills_d, 0o755)
        hata += fs_hukmu_hatalari("D", k, c, skills_d)
        if bayt_agaci(hedef_yolu(hd)) != eski_d:
            hata.append("D: var olan kurulum DEGISTI (`--guncelle` + izin hatasi)")
    if hata:
        return ("KIRMIZI", "; ".join(hata), False)
    if sebep:
        return ("YESIL", "A1+A2+A3 enjeksiyon: exit 3, engel olan yer dogru, `kapi`/chmod-gecici satiri YOK · "
                "B+C+D gercek salt-okunur: OLCULEMEDI (%s)" % sebep, "salt")
    return ("YESIL", "A1+A2+A3 enjeksiyon ve B+C+D gercek salt-okunur dizin: exit 3, `Engel olan yer:` satiri dogru, "
            "`kapi`/chmod-gecici satiri YOK, D'de eski kurulum saglam", False)


KOLLAR = [("K-TAZE", kol_taze), ("K-AYNI", kol_ayni), ("K-FARKLI", kol_farkli),
          ("K-GUNCELLE", kol_guncelle), ("K-PROJE", kol_proje), ("K-ENV", kol_env), ("K-COP", kol_cop),
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
    ("M-SK-BEYAZ", "beyaz liste sokulur (her dosya beyaz sayilir)",
     "def _skill_kur_beyaz_mi(rel):",
     "def _skill_kur_beyaz_mi(rel):\n    return True\n\n\ndef _skill_kur_beyaz_mi_eski(rel):", "K-COP"),
    ("M-SK-BAGLANTI", "skill-kur dizin baglantisi reddi sokulur (eksik kurulum sessizce exit 0)",
     "    bagli = _paket_baglantilar(kaynak)\n    if bagli:\n", "    bagli = _paket_baglantilar(kaynak)\n    if False:\n", "K-COP"),
    ("M-SK-HEDEF", "kurulu hedefin envanteri de beyaz listeyle suzulur (eski kurulumdaki cop gorunmez)",
     "        hd = _skill_kur_tum(hedef)\n", "        hd = _skill_kur_dosyalar(hedef)\n", "K-COP"),
    ("M-SK-YER", "yedek `skills/` ALTINA alinir",
     'os.path.join(taban, "hafiza-kur-yedek")', 'os.path.join(taban, "skills", "hafiza-kur-yedek")',
     "K-GUNCELLE"),
    ("M-SK-GENEL", "dosya sistemi yakalayicisi sokulur (genel yakalayiciya duser)",
     '        return _dosya_sistemi_hukmu("skill-kur", _engel_dizin(e), ipucu)\n',
     "        raise\n", "K-SALTOKUNUR"),
    ("M-SK-RENAME", "son rename'in izin hatasi eski 'olcum tutmadi' exit 1 olur",
     '            if getattr(e, "errno", None) in _FS_ENGEL_KODLARI:\n                raise ',
     '            if False:\n                raise ', "K-SALTOKUNUR"),
    ("M-SK-ENGEL", "engel dizin secimi (yazilamayan ust dizin dongusu) sokulur -> yanlis dizin gosterilir",
     "        if os.path.isdir(d) and not os.access(d, os.W_OK):\n            return d\n",
     "        if False:\n            return d\n", "K-SALTOKUNUR"),
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
    cop = os.path.join(taban, "skill_cop")
    motor_cop = skill_kopya(cop, kaynak_skill, motor_metni)
    cop_enjekte_et(cop)
    ctx = {"taban": taban, "skill": skill, "motor": motor, "skill_enjekte": enj, "motor_enjekte": motor_enj,
           "motor_cop": motor_cop, "skill_cop": cop}
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
    "bag": "\n  SINIRLI: K-COP'un dizin baglantisi alt-olcumu OLCULEMEDI (symlink/junction kurulamadi); "
           "CI ubuntu/macOS (symlink) ve Windows (junction) kolu olcer.",
    "zip": "\n  SINIRLI: K-ENV'in zip envanteri karsilastirmasi OLCULEMEDI (calisan bash yok); "
           "CI ubuntu kolu `--zip-zorla` ile olcer.",
    "salt": "\n  SINIRLI: K-SALTOKUNUR'un GERCEK salt-okunur kollari (B/C/D) OLCULEMEDI (POSIX degil ya da "
            "root); A1/A2/A3 enjeksiyon kollari olculdu, gercek-izin kollarini CI ubuntu/macOS olcer.",
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

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
                zip envanteriyle AYNI. `bash`+`zip` yoksa o ALT-OLCUM "OLCULEMEDI" basilir ve sonuc
                "YESIL (SINIRLI)" olur (sessiz yesil DEGIL); `--zip-zorla` ile exit 2
  K-MOTORYALNIZ motor tek basina bir dizine kopyalanip oradan kosulur -> exit 2, HOME'a yazilmadi

MUTANTLAR (motor KOPYASINDA dizge sabotaji; hedef dizge motorda TAM 1 kez gecmeli, degilse
OLCULEMEDI — h14_bolme dersi). Her mutantin BEKLENEN kolu KIRMIZI yanmali:
  M-SK-OLCUM  olcum sokulur + kopyaya bozulma enjekte edilir      -> K-TAZE
  M-SK-EZME   catisma kontrolu sokulur (farkli kurulum sessizce degisir) -> K-FARKLI
  M-SK-YEDEK  yedege tasima yerine SILME                            -> K-GUNCELLE
  M-SK-SUZGEC suzgecten `deneme` cikarilir                          -> K-ENV
  M-SK-YER    yedek `skills/` ALTINA alinir (Claude Code orada SKILL.md bulani yukler) -> K-GUNCELLE
POZITIF KONTROL: temiz motorda tum kollar YESIL olmali; degilse mutant hukmu ANLAMSIZDIR -> exit 2.

CIKIS  0 yesil + 5/5 mutant ISIRDI · 1 bir mutant KACTI · 2 OLCULEMEDI (pozitif kontrol tutmadi,
       capa yok, `--zip-zorla` + zip yok) — sessiz PASS YOK
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
# Her kol: (durum, ayrinti, sinirli). durum: YESIL | KIRMIZI. sinirli: alt-olcum OLCULEMEDI mi.
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


def zip_envanteri(ctx):
    """paketle.sh'i injekte edilmis kaynakla kosar. (zip DOSYA envanteri | None, sebep): None =
    bu platformda kosulamiyor (bash/zip/python3 yok ya da paketle.sh paket uretmedi) — bu bir
    SINIRLI durumudur; yalniz `--zip-zorla` (CI ubuntu) onu sert hataya cevirir."""
    eksik = [k for k in ("bash", "zip", "python3") if not shutil.which(k)]
    if eksik:
        return None, "%s yok" % "/".join(eksik)
    d = os.path.join(ctx["taban"], "paketle")
    os.makedirs(d)
    shutil.copy(os.path.join(KOK_DEPO, "paketle.sh"), d)
    shutil.copytree(ctx["skill_enjekte"], os.path.join(d, "skill"))
    r = subprocess.run(["bash", "paketle.sh"], cwd=d, capture_output=True, text=True, timeout=300,
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
    sinirli = z is None
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


KOLLAR = [("K-TAZE", kol_taze), ("K-AYNI", kol_ayni), ("K-FARKLI", kol_farkli),
          ("K-GUNCELLE", kol_guncelle), ("K-PROJE", kol_proje), ("K-ENV", kol_env),
          ("K-MOTORYALNIZ", kol_motoryalniz)]

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
    print("SKILL-KUR OLCERI · motor %s · platform %s · bash/zip: %s" % (
        motor, sys.platform, "VAR" if (shutil.which("bash") and shutil.which("zip")) else "YOK"))
    print(CIZGI)
    gercek_home = os.path.expanduser("~")
    onceki = sorted(os.listdir(os.path.join(gercek_home, ".claude", "skills"))) \
        if os.path.isdir(os.path.join(gercek_home, ".claude", "skills")) else None

    taban0 = tempfile.mkdtemp(prefix="skill_kur_olcer_")
    try:
        print("POZITIF KONTROL (temiz motor, 7 kol):")
        temiz = kollari_kos(kaynak_skill, None, os.path.join(taban0, "temiz"), zip_zorla)
        for ad, durum, ayr, _s in temiz:
            print("  %-14s %-10s %s" % (ad, durum, ayr))
        if any(d != "YESIL" for _, d, _, _ in temiz):
            print("\nSONUC: OLCULEMEDI — pozitif kontrol tutmadi (temiz motorda kirmizi/olculemeyen kol); "
                  "mutant hukumleri ANLAMSIZ, mutantlar KOSULMADI.")
            return 2
        sinirli = any(s for _, _, _, s in temiz)
        if sinirli and zip_zorla:
            print("\nSONUC: OLCULEMEDI — `--zip-zorla` verildi ama bash/zip yok (K-ENV zip karsilastirmasi).")
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
    print("SONUC: %s — 7 kol yesil, %d/%d mutant ISIRDI (%s)%s"
          % ("YESIL (SINIRLI)" if sinirli else "YESIL", len(isirdi), len(MUTANTLAR), ", ".join(isirdi),
             "\n  SINIRLI: K-ENV'in zip envanteri karsilastirmasi OLCULEMEDI (bash/zip yok); "
             "CI ubuntu kolu `--zip-zorla` ile olcer." if sinirli else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

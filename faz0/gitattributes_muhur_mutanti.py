#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GITATTRIBUTES MUHUR MUTANTI — `kur`/`devral` muhurlu dosyalari satir sonu cevriminden KORUYOR mu, DOGRU koruyor mu?
(besli-paket/IS_EMRI_GITATTRIBUTES_MUHUR.md KALEM 1, 18 Eki 2026)

NEDEN VAR (OLCULDU 18 Eki 2026, Windows 11, `core.autocrlf=true`, hafiza.py 6EA0A2ED)
  hafiza.py defterleri BAYT-TAM hash'ler; git checkout LF'i CRLF'e cevirir; ayni depo ikinci kez klonlaninca `kapi`
  exit 1 (`[H0] CIPA BOZULDU` + 9x `defter MUHURSUZ degismis`). Sinif UCUNCU kez isirdi. `kur` ve `devral` kokteki
  `.gitattributes`'a isaretli blok yazar (`# hafiza-kur BASLA` ... `# hafiza-kur BITIR`): `<arsiv dizini>/** -text` +
  her politika dosyasi icin `<ad> -text`. Kurallar SABIT liste degil, MUHURLU KUMEDEN turetilir.

NE OLCER — on bir HAL, her biri bagimsiz bir ORAKELe (bu dosyada elle yazili beklenen kural listesi) karsi:
    KUR        taze git deposunda `kur` -> blok VAR, TEK, kurallar beklenenle ESIT
    TEKRAR     ikinci `kur` -> dosya BAYT-BIREBIR ayni, `ZATEN VAR` beyan edilir
    MEVCUT     kullanicinin `.gitattributes`'i VAR (son satirsonu yok) -> mevcut baytlar ONEK olarak AYNEN kalir, blok eklenir
    MEVCUT_CRLF ayni, CRLF'li dosya -> onek bayt-birebir, eklenen blok CRLF
    ASISTAN    `kur --asistan agents` -> AGENTS.md MUHURLU DEGIL => kurala GIRMEZ
    BAG        `.gitattributes` git sembolik bagi (index 120000) -> YAZILMAZ, hal beyan edilir, elle eklenecek satirlar basilir
    SALTOKU    `.gitattributes` salt-okunur (yazilabilirlik YAZIMDAN ONCE olculur) -> YAZILMAZ, `SALT-OKUNUR` beyani + elle eklenecek satirlar
    NS         arsiv dizini FARKLI ad alaninda (`.hafizarc hafiza_dizini`) -> kural O ad alanindan TUREMIS olmali
    DEVRAL     `devral --esle canli=DURUM.md` -> blok yazilir
    IKLON      GERCEK ikinci klon (`faz0/ikinci_klon_kapisi.py`, core.autocrlf=true) -> `kapi` exit 0     [yalniz M-GA1/M-GA2 icin kosulur]
    IKLON_NS   ayni, farkli ad alaninda                                                                    [yalniz M-GA2 icin kosulur]
  SAGLAM motorda hepsi YESIL; asagidaki yedi sabotajin HER BIRI KENDI halinde KIRMIZI yakmalidir (yanlis sebeple isirmak sayilmaz):
    M-GA1 BLOK YAZIMI KAPALI         `_gitattributes_uygula` hicbir sey yazmaz            -> KUR · IKLON
    M-GA2 LISTE SABIT                kurallar eski 4 satira cakili (ad alani gormez)      -> NS · IKLON_NS
    M-GA7 ASISTAN DOSYASI GIRER      `AGENTS.md` muhurlu kumeye sokulur                   -> ASISTAN
    M-GA8 BLOK DISINA DOKUNUR        ekleme yerine dosyanin USTUNE yazar                  -> MEVCUT
    M-GA9 IKINCI KOSUM TEKRAR YAZAR  blok-var denetimi yok -> her `kur` bir blok daha      -> TEKRAR
    M-GA10 GIT BAGI KORUNMAZ         index 120000 denetimi yok -> duz dosyaya yazar        -> BAG
    M-GA12 SALT-OKUNUR OLCULMEZ      yazilabilirlik yazimdan ONCE olculmez (yazim dener) -> SALTOKU

NE OLCMEZ
  macOS/Linux'ta `core.autocrlf=true` simulasyonu `-c`/GIT_CONFIG_GLOBAL ile yapilir; GERCEK Windows dosya sistemi yalniz Windows bacaginda. Dosya
  sembolik bagi (islink) Windows hesabinda yetkisiz olabilir => BAG halinde yalniz git bagi (index 120000) kurulur. `core.autocrlf=input`, Git LFS
  ve kullanicinin blogu elle silmesi bu kapinin DISINDADIR (DURUM.md siniri).

KULLANIM    python3 faz0/gitattributes_muhur_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve yedi mutantin HEPSI kendi halinde KIRMIZI yakti
            1 saglam motorda kirmizi YA DA bir mutant KACTI/yanlis sebeple isirdi
            2 OLCULEMEDI (git yok, hal kurulamadi, anchor tutmadi, arac hatasi)
"""
import json
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
IKLON = os.path.join(KOK, "faz0", "ikinci_klon_kapisi.py")
CIZGI = "-" * 84

# ORAKEL: motorun sabitlerinden BAGIMSIZ, elle yazili beklenen kural listesi (sirasiyla).
POLITIKA = [".hafizarc", "KONULAR.md", "SAKLAMA_PLANI.md"]


def beklenen(dizin="arsiv/hafiza"):
    return [dizin + "/**"] + POLITIKA


BAS, SON = "# hafiza-kur BASLA", "# hafiza-kur BITIR"
HALLER = ["KUR", "TEKRAR", "MEVCUT", "MEVCUT_CRLF", "ASISTAN", "BAG", "SALTOKU", "NS", "DEVRAL", "IKLON", "IKLON_NS"]


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin saglam/kor oldugu anlamina GELMEZ."""


def git_ortami(taban):
    """Gercek global config'e dokunulmaz; kimlik gecici dosyadan."""
    g = os.path.join(taban, "gitconfig-global")
    if not os.path.isfile(g):
        with open(g, "w", encoding="utf-8", newline="\n") as f:
            f.write("[user]\n\tname = gamut\n\temail = gamut@example.invalid\n[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n")
    return dict(os.environ, GIT_CONFIG_GLOBAL=g, PYTHONIOENCODING="utf-8")


def git(ortam, *args, cwd=None, girdi=None):
    r = subprocess.run(["git"] + list(args), cwd=cwd, env=ortam, capture_output=True, input=girdi, timeout=300)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).decode("utf-8", "replace").strip()[:140]))
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


def _oku_b(kok, ad=".gitattributes"):
    p = os.path.join(kok, ad)
    if not os.path.isfile(p):
        return None
    with open(p, "rb") as f:
        return f.read()


def _yaz_b(kok, ad, ham):
    with open(os.path.join(kok, ad), "wb") as f:
        f.write(ham)


def blok_coz(ham):
    """-> (BASLA sayisi, BITIR sayisi, kurallar) — blok icindeki `<desen> -text` satirlari."""
    if ham is None:
        return 0, 0, []
    ls = [x.strip() for x in ham.decode("utf-8", "replace").splitlines()]
    kurallar, icinde = [], False
    for x in ls:
        if x == BAS:
            icinde = True
        elif x == SON:
            icinde = False
        elif icinde and x.endswith(" -text") and not x.startswith("#"):
            kurallar.append(x[:-6])
    return ls.count(BAS), ls.count(SON), kurallar


def yeni_proje(taban, ad, ortam, git_baslat=True):
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if git_baslat:
        git(ortam, "init", "-q", kok)
    return kok


def kur(motor, kok, ortam, *ek):
    rc, c = kos(motor, ["kur", "--ad", "GAMUT"] + list(ek), kok, ortam)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))
    return c


# ---------------------------------------------------------------------------------- HALLER (gozlem toplar)
def hal_kur_(motor, taban, ortam):
    k = yeni_proje(taban, "kur", ortam)
    c = kur(motor, k, ortam)
    return {"ham": _oku_b(k), "cikti": c, "kok": k}


def hal_tekrar(motor, taban, ortam):
    k = yeni_proje(taban, "tekrar", ortam)
    kur(motor, k, ortam)
    once = _oku_b(k)
    c = kur(motor, k, ortam)
    return {"once": once, "sonra": _oku_b(k), "cikti": c}


def hal_mevcut(motor, taban, ortam, crlf):
    k = yeni_proje(taban, "mevcut_crlf" if crlf else "mevcut", ortam)
    eol = b"\r\n" if crlf else b"\n"
    onek = eol.join([b"*.png binary", b"# kullanici kurali", b"*.sh text eol=lf"])      # SON SATIR SONU YOK (zor hal)
    _yaz_b(k, ".gitattributes", onek)
    c = kur(motor, k, ortam)
    return {"onek": onek, "ham": _oku_b(k), "cikti": c, "eol": eol}


def hal_asistan(motor, taban, ortam):
    k = yeni_proje(taban, "asistan", ortam)
    c = kur(motor, k, ortam, "--asistan", "agents")
    return {"ham": _oku_b(k), "cikti": c, "agents": os.path.isfile(os.path.join(k, "AGENTS.md"))}


def hal_bag(motor, taban, ortam):
    """P3.1 K1 kalibi: `core.symlinks=false` checkout'unda git bagi (index 120000) DUZ DOSYA gorunur."""
    k = yeni_proje(taban, "bag", ortam)
    ham = b"hedef.txt"
    _yaz_b(k, ".gitattributes", ham)
    sha = git(ortam, "hash-object", "-w", "--stdin", cwd=k, girdi=ham).decode().strip()
    git(ortam, "update-index", "--add", "--cacheinfo", "120000,%s,.gitattributes" % sha, cwd=k)
    c = kur(motor, k, ortam)
    return {"ham": ham, "sonra": _oku_b(k), "cikti": c}


def hal_saltoku(motor, taban, ortam):
    """Salt-okunur `.gitattributes`: yazilabilirlik YAZIMDAN ONCE olculur (hal etiketi `SALT-OKUNUR`; yazim denenip `YAZILAMADI` olmaz)."""
    k = yeni_proje(taban, "saltoku", ortam)
    ham = b"*.png binary\n"
    _yaz_b(k, ".gitattributes", ham)
    p = os.path.join(k, ".gitattributes")
    os.chmod(p, stat.S_IREAD)
    try:
        if os.access(p, os.W_OK):
            raise Kurulamadi("SALTOKU: salt-okunur bayragi bu hesapta etkisiz (root?) — hal OLCULEMEDI")
        c = kur(motor, k, ortam)
        return {"ham": ham, "sonra": _oku_b(k), "cikti": c}
    finally:
        os.chmod(p, stat.S_IWRITE | stat.S_IREAD)


def hal_ns(motor, taban, ortam):
    k = yeni_proje(taban, "ns", ortam)
    kur(motor, k, ortam)
    rcp = os.path.join(k, ".hafizarc")
    with open(rcp, encoding="utf-8") as f:
        d = json.load(f)
    d["hafiza_dizini"] = "kayit/hafiza"
    with open(rcp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.makedirs(os.path.join(k, "kayit"))
    shutil.move(os.path.join(k, "arsiv", "hafiza"), os.path.join(k, "kayit", "hafiza"))
    if os.path.isfile(os.path.join(k, ".gitattributes")):          # sabotajli motor hic yazmamis olabilir
        os.remove(os.path.join(k, ".gitattributes"))
    c = kur(motor, k, ortam)
    return {"ham": _oku_b(k), "cikti": c}


def hal_devral(motor, taban, ortam):
    k = yeni_proje(taban, "devral", ortam)
    with open(os.path.join(k, "DURUM.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# Proje\n\n## GUNCEL DURUM\nbir\n\n## SONRAKI ADIM\niki\n")
    with open(os.path.join(k, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# Proje esaslari\n")
    rc, c = kos(motor, ["devral", "--esle", "canli=DURUM.md"], k, ortam)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))
    return {"ham": _oku_b(k), "cikti": c}


def hal_iklon(motor, ad_alani=None):
    arg = [sys.executable, "-X", "utf8", IKLON, "--motor", motor] + (["--ad-alani", ad_alani] if ad_alani else [])
    r = subprocess.run(arg, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    return {"rc": r.returncode, "cikti": (r.stdout or "") + (r.stderr or "")}


def gozle(motor, taban, iklon, iklon_ns):
    """Motoru her halde kosturur -> {hal: gozlem}. Kurulamazsa Kurulamadi firlatir."""
    os.makedirs(taban, exist_ok=True)
    ortam = git_ortami(taban)
    g = {"KUR": hal_kur_(motor, taban, ortam), "TEKRAR": hal_tekrar(motor, taban, ortam),
         "MEVCUT": hal_mevcut(motor, taban, ortam, False), "MEVCUT_CRLF": hal_mevcut(motor, taban, ortam, True),
         "ASISTAN": hal_asistan(motor, taban, ortam), "BAG": hal_bag(motor, taban, ortam),
         "SALTOKU": hal_saltoku(motor, taban, ortam), "NS": hal_ns(motor, taban, ortam), "DEVRAL": hal_devral(motor, taban, ortam)}
    if iklon:
        g["IKLON"] = hal_iklon(motor)
    if iklon_ns:
        g["IKLON_NS"] = hal_iklon(motor, "kayit/hafiza")
    return g


# ---------------------------------------------------------------------------------- KAPI (hal basina ihlal)
def _blok_ihlali(ham, bek):
    b, s, kurallar = blok_coz(ham)
    out = []
    if ham is None:
        return [".gitattributes YAZILMADI"]
    if (b, s) != (1, 1):
        out.append("blok sayisi BASLA/BITIR = %d/%d (1/1 olmali)" % (b, s))
    if kurallar != bek:
        out.append("kurallar %r != beklenen %r" % (kurallar, bek))
    return out


def ihlaller(g):
    """-> [(hal, mesaj)] — bos liste = YESIL. Saglam/sabotajli motor AYNI fonksiyonla yargilanir."""
    out = []

    def ekle(hal, liste):
        out.extend((hal, m) for m in liste)

    k = g["KUR"]
    ekle("KUR", _blok_ihlali(k["ham"], beklenen()) + ([] if "GITATTRIBUTES YAZILDI" in k["cikti"] else ["cikti `GITATTRIBUTES YAZILDI` demiyor"]))
    t = g["TEKRAR"]
    ekle("TEKRAR", ([] if t["once"] == t["sonra"] else ["ikinci `kur` dosyayi DEGISTIRDI (bayt farki)"]) +
         ([] if "ZATEN VAR" in t["cikti"] else ["cikti `ZATEN VAR` demiyor"]))
    for ad in ("MEVCUT", "MEVCUT_CRLF"):
        m = g[ad]
        ham, onek = m["ham"] or b"", m["onek"]
        liste = []
        if not ham.startswith(onek):
            liste.append("mevcut baytlar ONEK olarak KORUNMADI (blok disina dokunuldu)")
        else:
            liste += _blok_ihlali(ham, beklenen())
            ek = ham[len(onek):]
            if m["eol"] == b"\r\n" and ek.replace(b"\r\n", b"").count(b"\n"):
                liste.append("CRLF'li dosyaya eklenen blokta CRLF'siz satir var")
            if b"EKLENDI" not in m["cikti"].encode("utf-8"):
                liste.append("cikti `EKLENDI` demiyor")
        ekle(ad, liste)
    a = g["ASISTAN"]
    _, _, ak = blok_coz(a["ham"])
    ekle("ASISTAN", ([] if a["agents"] else ["`--asistan agents` AGENTS.md yazmadi (duzenek)"]) +
         ([] if not any("AGENTS" in x for x in ak) else ["AGENTS.md muhurlu degil ama kurala GIRDI: %r" % ak]))
    bg = g["BAG"]
    ekle("BAG", ([] if bg["sonra"] == bg["ham"] else ["git bagi (index 120000) YAZILDI: %r" % (bg["sonra"] or b"")[:60]]) +
         ([] if "GITATTRIBUTES SEMBOLIK BAG (git)" in bg["cikti"] else ["cikti `SEMBOLIK BAG (git)` demiyor"]) +
         ([] if "    arsiv/hafiza/** -text" in bg["cikti"] else ["elle eklenecek satirlar BASILMADI"]))
    sk = g["SALTOKU"]
    ekle("SALTOKU", ([] if sk["sonra"] == sk["ham"] else ["salt-okunur dosya DEGISTI"]) +
         ([] if "GITATTRIBUTES SALT-OKUNUR" in sk["cikti"] else ["cikti `SALT-OKUNUR` demiyor (yazim denenmis olabilir)"]) +
         ([] if "    arsiv/hafiza/** -text" in sk["cikti"] else ["elle eklenecek satirlar BASILMADI"]))
    ekle("NS", _blok_ihlali(g["NS"]["ham"], beklenen("kayit/hafiza")))
    ekle("DEVRAL", _blok_ihlali(g["DEVRAL"]["ham"], beklenen()))
    for ad in ("IKLON", "IKLON_NS"):
        if ad in g and g[ad]["rc"] != 0:
            ekle(ad, ["gercek ikinci klonda `kapi` YESIL degil (gate exit %s)" % g[ad]["rc"]])
    return out


# ---------------------------------------------------------------------------------- MUTANTLAR
# ad, aciklama, beklenen hal(ler), [(eski, yeni)], iklon, iklon_ns. `eski` motorda TAM 1 kez gecmelidir.
MUTANTLAR = [
    ("M-GA1 BLOK YAZIMI KAPALI", "`_gitattributes_uygula` hicbir sey yazmaz", {"KUR", "IKLON"},
     [("    desenler, atlanan = _ga_kurallar(y)\n    hal, p = _ga_hal(y.kok)\n",
       "    return                       # MUTANT: blok yazimi kapali\n    desenler, atlanan = _ga_kurallar(y)\n    hal, p = _ga_hal(y.kok)\n")],
     True, False),
    ("M-GA2 LISTE SABIT", "kurallar eski 4 satira cakili (ad alanini gormez)", {"NS", "IKLON_NS"},
     [("    return desenler, atlanan\n\n\ndef _ga_blok(desenler):",
       "    return [\"arsiv/hafiza/**\", \".hafizarc\", \"KONULAR.md\", \"SAKLAMA_PLANI.md\"], atlanan   # MUTANT\n\n\ndef _ga_blok(desenler):")],
     False, True),
    ("M-GA7 ASISTAN DOSYASI GIRER", "`AGENTS.md` muhurlu kumeye sokulur", {"ASISTAN"},
     [("    yollar += [os.path.join(y.kok, pd) for pd in POLITIKA_DOSYALARI]\n    return [_rel(p, y.kok) for p in yollar]",
       "    yollar += [os.path.join(y.kok, pd) for pd in POLITIKA_DOSYALARI] + [os.path.join(y.kok, \"AGENTS.md\")]   # MUTANT\n"
       "    return [_rel(p, y.kok) for p in yollar]")], False, False),
    ("M-GA8 BLOK DISINA DOKUNUR", "ekleme (`ab`) yerine dosyanin USTUNE yazar (`wb`)", {"MEVCUT"},
     [("    with open(p, \"ab\") as f:\n        f.write(ayrac + eol.join(x.encode(\"utf-8\") for x in blok) + eol)\n    return \"EKLENDI\"\n",
       "    with open(p, \"wb\") as f:   # MUTANT\n        f.write(ayrac + eol.join(x.encode(\"utf-8\") for x in blok) + eol)\n    return \"EKLENDI\"\n")],
     False, False),
    ("M-GA9 IKINCI KOSUM TEKRAR YAZAR", "blok-var denetimi yok -> her `kur` bir blok daha ekler", {"TEKRAR"},
     [("    if _GA_BAS in ls and _GA_SON in ls:\n        return \"ZATEN VAR\", p\n    if _GA_BAS in ls or _GA_SON in ls:\n"
       "        return \"YARIM BLOK\", p\n", "")], False, False),
    ("M-GA10 GIT BAGI KORUNMAZ", "index 120000 denetimi yok -> duz dosya sanilip yazilir", {"BAG"},
     [("    if _asistan_git_modu(kok, _GA_AD) == \"120000\":", "    if False:   # MUTANT")], False, False),
    ("M-GA12 SALT-OKUNUR OLCULMEZ", "yazilabilirlik yazimdan ONCE olculmez (yazim denenir)", {"SALTOKU"},
     [("    return (\"EKLENECEK\" if os.access(p, os.W_OK) else \"SALT-OKUNUR\"), p\n",
       "    return \"EKLENECEK\", p   # MUTANT\n")], False, False),
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
    print("GITATTRIBUTES MUHUR MUTANTI — muhurlu kume satir sonu cevriminden korunuyor mu? · platform: %s" % sys.platform)
    print("motor: %s" % motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="gamut_")
    try:
        try:
            temiz = ihlaller(gozle(motor, os.path.join(taban, "temiz"), True, True))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        print("  SAGLAM MOTOR (%d hal)            %s" % (len(HALLER), "YESIL" if not temiz else "KIRMIZI"))
        for hal, m in temiz:
            print("      ! %-11s %s" % (hal, m[:170]))
        if temiz:
            print(CIZGI)
            print("SONUC: KIRMIZI — saglam motor kapiyi gecemedi.")
            return 1
        isirdi, kacti, olculemedi = [], [], []
        for ad, aciklama, hedef, degisim, iklon, iklon_ns in MUTANTLAR:
            d = os.path.join(taban, ad.split()[0])
            os.makedirs(d, exist_ok=True)
            try:
                sab = sabotajli_motor(kaynak, degisim, d)
                ih = ihlaller(gozle(sab, os.path.join(d, "hal"), iklon, iklon_ns))
            except Kurulamadi as e:
                olculemedi.append(ad)
                print("  ?  %-30s OLCULEMEDI  %s" % (ad, e))
                continue
            haller = {h for h, _ in ih}
            if hedef & haller:
                isirdi.append(ad)
                print("  +  %-30s ISIRDI      hedef hal: %s · tum ihlal halleri: %s"
                      % (ad, ",".join(sorted(hedef & haller)), ",".join(sorted(haller))))
            elif ih:
                kacti.append(ad)
                print("  !  %-30s YANLIS SEBEP ihlal %s var ama HEDEF hal (%s) susuyor" % (ad, ",".join(sorted(haller)), ",".join(sorted(hedef))))
            else:
                kacti.append(ad)
                print("  !  %-30s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
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
    print("  Saglam motor YESIL, yedi sabotajin hepsi KENDI halinde KIRMIZI: muhur korumasi olculuyor.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — ASISTAN DOSYALARI MUTANTI (besli-paket/IS_EMRI_P3_ASISTAN_DOSYALARI.md, KALEM 1 + KALEM 2).

NEDEN VAR (Onur kilidi 17 Eki 2026): Claude DISI asistanlar (Codex/Gemini/Cursor/Copilot) deftere yol bulsun diye `kur`/`devral --asistan`
dort dosyaya (AGENTS.md · GEMINI.md · .cursor/rules/hafiza-kur.mdc · .github/copilot-instructions.md) sona isaretli blok yazar. OPT-IN:
bayraksiz TEK BAYT yazilmaz. Bu betik motorun bu sozlesmesini OLCER ve her sozlesme maddesini bozan sabotajin YAKALANDIGINI sinar.

KOLLAR (etiket = eksen): DOGUM (bos projede dort dosya, .mdc frontmatter) · BAYRAKSIZ (bayraksiz kur hicbir sey yazmaz) · ONEK (mevcut AGENTS.md
oneki bayt-birebir, blok SONDA) · CRLF (BOM+CRLF dosya: onek AYNEN, eklenen satir sonu CRLF) · IKINCI (ikinci kosum bayt-esit, tek blok) ·
SEMBOLIK (baglanti dizinine yazilmaz) · YARIM (yarim blok yazilmaz) · CAKISMA (yabanci hafiza-kur.mdc yazilmaz) · ANAHTAR (bilinmeyen
anahtar exit 2, hicbir sey yazilmaz) · KESIF (`devral --kesif --asistan` TEK BAYT yazmaz) · GRAPHIFY (Graphify `## graphify` ve
`graphify.mdc` bayt-birebir).
SABOTAJLAR (hepsi YAKALANMALI): bayraksiz yazim · dosyanin BASINA ekleme · ikinci blok · sembolik bagi izleme · CRLF dusurme · --kesif'te yazma.

CIKIS KODU  0 tum kollar temiz VE tum sabotajlar ISIRDI · 1 kol BEKLENMEDIK ya da sabotaj KACTI · 2 OLCULEMEDI (git yok / motor okunamadi)
"""
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tempfile

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
DOSYALAR = ("AGENTS.md", "GEMINI.md", ".cursor/rules/hafiza-kur.mdc", ".github/copilot-instructions.md")
BAS, SON = b"<!-- hafiza-kur:asistan -->", b"<!-- /hafiza-kur:asistan -->"
_GIT = dict(os.environ, GIT_AUTHOR_NAME="ast", GIT_AUTHOR_EMAIL="a@example.invalid", GIT_COMMITTER_NAME="ast",
            GIT_COMMITTER_EMAIL="a@example.invalid", GIT_CONFIG_NOSYSTEM="1")


class Kurulamadi(Exception):
    pass


def kos(motor, kok, *args):
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(args) + ["--kok", kok], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"), timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def yeni_proje(taban, ad, dosyalar=None):
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    if subprocess.run(["git", "init", "-q", kok], capture_output=True).returncode != 0:
        raise Kurulamadi("git init basarisiz")
    for rel, ham in (dosyalar or {}).items():
        p = os.path.join(kok, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(ham)
    return kok


def oku_b(kok, rel):
    with open(os.path.join(kok, *rel.split("/")), "rb") as f:
        return f.read()


def manifest(kok):
    out = {}
    for r0, d, f0 in os.walk(kok):
        d[:] = [x for x in d if x != ".git"]
        for f in f0:
            p = os.path.join(r0, f)
            with open(p, "rb") as h:
                out[os.path.relpath(p, kok).replace("\\", "/")] = hashlib.sha256(h.read()).hexdigest()
    return out


def kur(motor, kok, *ek):
    rc, c = kos(motor, kok, "kur", "--ad", "AST", "--yine-de", *ek)
    return rc, c


def k_dogum_bayraksiz(motor, taban):
    b = []
    k = yeni_proje(taban, "dogum")
    rc, c = kur(motor, k, "--asistan")
    if rc != 0 or any(not os.path.isfile(os.path.join(k, *r.split("/"))) for r in DOSYALAR):
        b.append(("DOGUM", "bos projede dort dosya dogmali: exit=%s %r" % (rc, c[-200:])))
    else:
        mdc = oku_b(k, ".cursor/rules/hafiza-kur.mdc")
        if not mdc.startswith(b"---\ndescription:") or b"alwaysApply: true" not in mdc or oku_b(k, "AGENTS.md").count(BAS) != 1:
            b.append(("DOGUM", ".mdc frontmatter (description + alwaysApply) ve tek blok beklenir: %r" % mdc[:120]))
    k2 = yeni_proje(taban, "bayraksiz")
    kur(motor, k2)
    if any(os.path.exists(os.path.join(k2, *r.split("/"))) for r in DOSYALAR) or os.path.isdir(os.path.join(k2, ".cursor")):
        b.append(("BAYRAKSIZ", "`--asistan` YOKKEN asistan dosyasi/dizini yazilmis"))
    return b


def k_onek_crlf(motor, taban):
    b = []
    agents = b"# Mevcut kural\nsatir bir"                      # son satirda newline YOK
    gem = b"\xef\xbb\xbfbir\r\niki\r\n"
    k = yeni_proje(taban, "onek", {"AGENTS.md": agents, "GEMINI.md": gem})
    kur(motor, k, "--asistan", "agents,gemini")
    a2, g2 = oku_b(k, "AGENTS.md"), oku_b(k, "GEMINI.md")
    if not a2.startswith(agents) or a2.find(BAS) < len(agents) or a2.count(BAS) != 1:
        b.append(("ONEK", "mevcut AGENTS.md oneki bayt-birebir kalmali, blok SONDA olmali: %r" % a2[:80]))
    ek = g2[len(gem):]
    if not g2.startswith(gem) or b"\r\n" not in ek or ek.replace(b"\r\n", b"").count(b"\n"):
        b.append(("CRLF", "BOM+CRLF dosya: onek AYNEN, eklenen satir sonlari CRLF olmali: %r" % g2[-60:]))
    return b


def k_ikinci_yarim_cakisma(motor, taban):
    b = []
    k = yeni_proje(taban, "ikinci")
    kur(motor, k, "--asistan")
    once = manifest(k)
    kur(motor, k, "--asistan")
    sonra = manifest(k)
    farkli = [r for r in DOSYALAR + (".hafizarc",) if once.get(r) != sonra.get(r)]
    if farkli or oku_b(k, "AGENTS.md").count(BAS) != 1:
        b.append(("IKINCI", "ikinci kosum bayt-esit olmali (tek blok): fark=%r" % farkli))
    yar = BAS + b"\n> yarim\n"
    k2 = yeni_proje(taban, "yarim", {"AGENTS.md": yar})
    rc, c = kur(motor, k2, "--asistan", "agents")
    if oku_b(k2, "AGENTS.md") != yar or "YARIM BLOK" not in c:
        b.append(("YARIM", "yarim blok yazilmamali + `YARIM BLOK` beyani: %r" % c[-160:]))
    yab = b"yabanci kural\n"
    k3 = yeni_proje(taban, "cakisma", {".cursor/rules/hafiza-kur.mdc": yab})
    rc, c = kur(motor, k3, "--asistan", "cursor")
    if oku_b(k3, ".cursor/rules/hafiza-kur.mdc") != yab or "CAKISMA" not in c:
        b.append(("CAKISMA", "isaretimizi tasimayan hafiza-kur.mdc yazilmamali + CAKISMA beyani: %r" % c[-160:]))
    return b


def _baglanti(link, hedef):
    try:
        os.symlink(hedef, link, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    if sys.platform == "win32":
        return subprocess.run(["cmd", "/c", "mklink", "/J", link, hedef], capture_output=True).returncode == 0
    return False


def k_sembolik(motor, taban):
    k = yeni_proje(taban, "sembolik")
    disari = os.path.join(taban, "disari")
    os.makedirs(disari)
    if not _baglanti(os.path.join(k, ".github"), disari):
        print("      (SEMBOLIK kolu OLCULEMEDI: baglanti kurulamadi — bu platformda yetki yok)")
        return []
    rc, c = kur(motor, k, "--asistan", "copilot")
    if os.listdir(disari) or "SEMBOLIK BAG" not in c:
        return [("SEMBOLIK", "baglanti dizinine (proje DISI) yazilmamali + `SEMBOLIK BAG` beyani: disari=%r %r" % (os.listdir(disari), c[-160:]))]
    return []


def k_git_bag(motor, taban):
    """GITBAG (P3.1 K1): `core.symlinks=false` checkout'unda git bagi (index 120000) DUZ DOSYA olur (icerik = hedef yolu); yazilmamali.
    M-A4'ten AYRI eksen: o `islink`i, bu index modunu olcer. Duzenek: index'e 120000 girdisi + diskte duz dosya."""
    k = yeni_proje(taban, "gitbag")
    ham = b"hedef.md"
    h = subprocess.run(["git", "-C", k, "hash-object", "-w", "--stdin"], input=ham, capture_output=True)
    sha = h.stdout.decode().strip()
    with open(os.path.join(k, "AGENTS.md"), "wb") as f:
        f.write(ham)
    if h.returncode != 0 or subprocess.run(["git", "-C", k, "update-index", "--add", "--cacheinfo", "120000,%s,AGENTS.md" % sha],
                                           capture_output=True, env=_GIT).returncode != 0:
        raise Kurulamadi("git index'e 120000 girdisi eklenemedi")
    rc, c = kur(motor, k, "--asistan", "agents")
    if oku_b(k, "AGENTS.md") != ham or "SEMBOLIK BAG (git)" not in c:
        return [("GITBAG", "index modu 120000 olan dosya (diskte duz) yazilmamali + `SEMBOLIK BAG (git)` beyani: %r %r"
                 % (oku_b(k, "AGENTS.md")[:60], c[-160:]))]
    return []


def k_anahtar_kesif_graphify(motor, taban):
    b = []
    k = yeni_proje(taban, "anahtar")
    rc, c = kur(motor, k, "--asistan", "agents,bilinmez")
    if rc != 2 or "agents, gemini, cursor, copilot" not in c or os.path.exists(os.path.join(k, "AGENTS.md")) \
            or os.path.exists(os.path.join(k, ".hafizarc")):
        b.append(("ANAHTAR", "bilinmeyen anahtar: exit 2 + gecerli liste + HICBIR yazim: exit=%s %r" % (rc, c[-160:])))
    k2 = yeni_proje(taban, "kesif", {"DURUM.md": b"# DURUM\n\n## GUNCEL DURUM\n- x\n", "CLAUDE.md": b"# kural\n"})
    once = manifest(k2)
    rc, c = kos(motor, k2, "devral", "--kesif", "--esle=canli=DURUM.md", "--asistan")
    if rc != 0 or manifest(k2) != once or any(os.path.exists(os.path.join(k2, *r.split("/"))) for r in DOSYALAR) \
            or "YAZILACAK" not in c:
        b.append(("KESIF", "`--kesif`: hallerini basar, TEK BAYT yazmaz: exit=%s %r" % (rc, c[-200:])))
    gr = {"AGENTS.md": b"# Proje\n\n## graphify\nGraphify kurali\n", ".cursor/rules/graphify.mdc": b"---\nalwaysApply: true\n---\ngraphify\n"}
    k3 = yeni_proje(taban, "graphify", gr)
    kur(motor, k3, "--asistan")
    if oku_b(k3, ".cursor/rules/graphify.mdc") != gr[".cursor/rules/graphify.mdc"] or not oku_b(k3, "AGENTS.md").startswith(gr["AGENTS.md"]):
        b.append(("GRAPHIFY", "Graphify bolumu/graphify.mdc bayt-birebir korunmali"))
    return b


def _h19(c):
    return sorted(x.strip() for x in c.splitlines() if "H19: asistan dosyasi (" in x)


def k_h19(motor, taban):
    """H19KOL (KALEM 2): listedeki her dosya AYRI satir, exit DEGISMEZ, listede olmayan dosya icin ses YOK."""
    b = []
    k0 = yeni_proje(taban, "h19taban")
    kur(motor, k0, "--asistan")
    e0, c0 = kos(motor, k0, "kapi")
    if _h19(c0):
        b.append(("H19KOL", "saglam kurulumda asistan satiri OLMAMALI: %r" % _h19(c0)))
    for anahtar, rel in (("agents", DOSYALAR[0]), ("gemini", DOSYALAR[1]), ("cursor", DOSYALAR[2]), ("copilot", DOSYALAR[3])):
        k = yeni_proje(taban, "h19_" + anahtar)
        kur(motor, k, "--asistan")
        p = os.path.join(k, *rel.split("/"))
        with open(p, "wb") as f:
            f.write(b"# bozuk: isaret yok\n")
        e1, c1 = kos(motor, k, "kapi")
        if len(_h19(c1)) != 1 or ("(%s)" % rel) not in _h19(c1)[0]:
            b.append(("H19KOL", "yalniz %s icin TEK satir beklenir: %r" % (rel, _h19(c1))))
        if e1 != e0:
            b.append(("H19EXIT", "H19 UYARIDIR, cikis kodu DEGISMEZ: taban=%s bozuk=%s" % (e0, e1)))
    kc = yeni_proje(taban, "h19canli")                      # isaret VAR ama canli defterin adi yok
    kur(motor, kc, "--asistan", "gemini")
    pg = os.path.join(kc, "GEMINI.md")
    with open(pg, "wb") as f:
        f.write(oku_b(kc, "GEMINI.md").replace(b"PROJE_HAFIZA.md", b"X.md"))
    if len(_h19(kos(motor, kc, "kapi")[1])) != 1:
        b.append(("H19KOL", "isaret var ama canli adi yok: TEK satir beklenir"))
    ki = yeni_proje(taban, "h19iki")                        # iki bozuk dosya: IKI ayri satir (dosya ayrimi kaybolmaz)
    kur(motor, ki, "--asistan")
    for rel in (DOSYALAR[0], DOSYALAR[3]):
        with open(os.path.join(ki, *rel.split("/")), "wb") as f:
            f.write(b"# bozuk\n")
    if len(_h19(kos(motor, ki, "kapi")[1])) != 2:
        b.append(("H19KOL", "iki bozuk dosya: IKI ayri H19 satiri beklenir"))
    k2 = yeni_proje(taban, "h19liste")                      # listede OLMAYAN bozuk AGENTS.md: ses YOK
    kur(motor, k2, "--asistan", "cursor")
    with open(os.path.join(k2, "AGENTS.md"), "wb") as f:
        f.write(b"# bozuk\n")
    if _h19(kos(motor, k2, "kapi")[1]):
        b.append(("H19LISTE", "listede olmayan dosya icin ses OLMAMALI"))
    return b


KOLLAR = (k_dogum_bayraksiz, k_onek_crlf, k_ikinci_yarim_cakisma, k_sembolik, k_git_bag, k_anahtar_kesif_graphify, k_h19)

# (ad, etiket, ankor, yeni): ankor motorda TAM 1 kez gecmeli
SABOTAJLAR = (
    ("M-A1 bayraksiz yazim (`--asistan` yokken de dort dosya yazilir)", "BAYRAKSIZ",
     '    v = getattr(a, "asistan", None)\n', '    v = getattr(a, "asistan", None) or "*"      # MUTANT\n'),
    ("M-A2 mevcut dosyanin BASINA ekleme", "ONEK",
     '    with open(p, "ab") as f:\n        f.write(ek + eol.join(x.encode("utf-8") for x in blok) + eol)\n',
     '    with open(p, "wb") as f:      # MUTANT\n        f.write(eol.join(x.encode("utf-8") for x in blok) + eol + ham)\n'),
    ("M-A3 ikinci blok (blok denetimi yok: tekrar kosumda yeniden eklenir)", "IKINCI",
     '    if bas >= 0 and son > bas:\n        return "ZATEN VAR", p\n    if bas >= 0 or son >= 0:\n        return "YARIM BLOK", p\n',
     '    pass      # MUTANT\n'),
    ("M-A4 sembolik bagi izleme (baglanti dizinine yazilir)", "SEMBOLIK",
     '    if _asistan_bagli(kok, p):\n        return "SEMBOLIK BAG", p\n', '    if False:      # MUTANT\n        return "SEMBOLIK BAG", p\n'),
    ("M-A7 git index modu (120000) kontrolu KAPALI", "GITBAG",
     '    if os.path.lexists(p) and _asistan_git_modu(kok, rel) == "120000":\n',
     '    if False:      # MUTANT\n'),
    ("M-A5 CRLF/satir sonu dusurulur (hep LF)", "CRLF",
     '    eol = b"\\r\\n" if n_crlf and n_crlf >= ham.count(b"\\n") - n_crlf else b"\\n"\n', '    eol = b"\\n"      # MUTANT\n'),
    ("M-A6 `--kesif` yazar", "KESIF",
     '            print("  asistan %-8s : %s -> %s" % (anahtar, rel, _asistan_hal(kok, anahtar, rel, kural)[0]))\n',
     '            h_, p_ = _asistan_hal(kok, anahtar, rel, kural)      # MUTANT\n'
     '            print("  asistan %-8s : %s -> %s" % (anahtar, rel, h_))\n'
     '            if h_ in ("YAZILACAK", "EKLENECEK"):\n                _asistan_yaz_dosya(p_, anahtar, "PROJE_HAFIZA.md")\n'),
    ("M-H1 H19 asistan dali KAPALI", "H19KOL",
     '    _kapi_asistan(N, y)                         # P3: asistan dosyalari (listede olanlar) AYRI satir\n', '    pass      # MUTANT\n'),
    ("M-H2 H19 asistan satirlari TEK satirda birlesir", "H19KOL",
     '    for x in uyari:\n        N.append(x)\n', '    if uyari:      # MUTANT\n        N.append(" | ".join(uyari))\n'),
    ("M-H3 H19 asistan uyarisi cikis kodunu 1'e cikarir", "H19EXIT",
     '    for x in uyari:\n        N.append(x)\n', '    for x in uyari:\n        N.append(x)\n    if uyari:      # MUTANT\n        sys.exit(1)\n'),
)


def calistir(motor, taban, ad):
    b = []
    for kol in KOLLAR:
        b += kol(motor, os.path.join(taban, ad + kol.__name__))
    return b


def main():
    yol = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN)
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: OLCULEMEDI — motor okunamadi: %s" % e)
        return 2
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok.")
        return 2
    print(CIZGI)
    print("ASISTAN MUTANTI — motor: %s · platform: %s" % (os.path.basename(yol), sys.platform))
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="asistan_")
    try:
        try:
            temiz = calistir(yol, taban, "t_")
        except Kurulamadi as e:
            print("SONUC: OLCULEMEDI — duzenek kurulamadi: %s" % e)
            return 2
        for et, m in temiz:
            print("      ! %s: %s" % (et, m))
        print("  kollar: %s" % ("TEMIZ" if not temiz else "BEKLENMEDIK"))
        if temiz:
            print("\nSONUC: KIRMIZI — temiz motorun kollari BEKLENMEDIK.")
            return 1
        print("\n--- SABOTAJLAR (her biri KENDI ekseninde ISIRMALI) ---")
        kacan = []
        for sira, (ad, etiket, ankor, yeni) in enumerate(SABOTAJLAR, 1):
            if s.count(ankor) != 1:
                print("SONUC: OLCULEMEDI — capa %d yerde (1 olmali): %s" % (s.count(ankor), ad))
                return 2
            d = os.path.join(taban, "m%d" % sira)
            os.makedirs(d)
            sab = os.path.join(d, "hafiza.py")
            with io.open(sab, "w", encoding="utf-8", newline="") as f:
                f.write(s.replace(ankor, yeni))
            try:
                atesler = {e for e, _ in calistir(sab, d, "s_")}
            except Kurulamadi as e:
                print("SONUC: OLCULEMEDI — %s: %s" % (ad, e))
                return 2
            if etiket in atesler:
                print("  %-60s -> ISIRDI ✓  (%s)" % (ad[:60], etiket))
            else:
                print("  %-60s -> KACTI ✗  (%s ekseni sabotajda TEMIZ; atesleyen: %s)" % (ad[:60], etiket, ",".join(sorted(atesler)) or "hicbiri"))
                kacan.append(ad)
        print(CIZGI)
        if kacan:
            print("SONUC: KAPI KOR — %s" % "; ".join(kacan))
            return 1
        print("SONUC: YESIL — 13 kol temiz, %d sabotaj AYRI eksende ISIRDI." % len(SABOTAJLAR))
        return 0
    finally:
        def onar(fonk, p, *_):
            try:
                os.chmod(p, 0o700)
                fonk(p)
            except OSError:
                pass
        shutil.rmtree(taban, **({"onexc": onar} if sys.version_info >= (3, 12) else {"onerror": onar}))


if __name__ == "__main__":
    sys.exit(main())

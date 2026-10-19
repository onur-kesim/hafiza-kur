#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H14 DEVRALMA MUTANTI — taze `devral`da H14 ILERIDE: KAYITLI muafiyet yalniz UC kosul BIRLIKTE tutarsa mi veriliyor?
(besli-paket/IS_EMRI_H14_DEVRALMA_KAYITLI_MUAFIYET.md KALEM 1+2, 19 Eki 2026; Onur kilidi 07:37 "kayitli muafiyet olur")

NEDEN VAR (OLCULDU 19 Eki 2026, Momentum d4b5417 + `devral`)
  Taze `devral`da hafiza damgasi = bugun, uyuyan projenin son degisikligi eski => ilk `kapi` HER ZAMAN
  `[H14] hafiza tarihi proje dosyalarindan 40 gun ILERIDE — tutarsiz` FAIL (sebepsiz kirmizi). Duz sure muafiyeti REDDEDILDI
  (o pencerede UYDURMA damgayi gizler). Cozum: `devral` devralma olayini MUHURLU kayda yazar (DEVIR zincir halkasinin `ek`i:
  `devralma_tarihi` + `proje_son_t`); H14 ILERIDE kolu UC kosul birlikte tutarsa FAIL yerine UYARI basar:
      (a) muhurlu devralma kaydi var · (b) damga devralma gununu gecmemis · (c) proje o gunden beri degismemis
  Biri tutmazsa bugunku FAIL BIREBIR. GERIDE ve es kollarina dokunulmaz. Cikis kodu YALNIZ bu kolda FAIL->UYARI degisir.

NE OLCER — alti HAL (her biri `kapi` H14 satirlariyla yargilanir; hepsi AYNI uyuyan proje iskeletinden, 40 gun eski):
    TAZE          `devral` + commit (bugun)                      -> TEK `· [H14] UYARI devralma ani: proje 40 gundur uyuyor (devral <bugun>);
                                                                    proje degisince ya da damga ilerleyince normal hukum doner`, [H14] FAIL YOK,
                                                                    `SONUC: YESIL` + exit 0 (H14 exit'i 1 yapmiyor)
    KAYITSIZ      `kur` ile kurulmus uyuyan proje (kayit YOK)    -> bugunku FAIL (ILERIDE) BIREBIR, UYARI YOK
    SAHTE         KAYITSIZ + elle eklenmis DEVIR halkasi (muhur  -> FAIL (kayit muhur disi: halka KIRIK, kayit SAYILMAZ)
                  disi, hash tutmuyor)
    DAMGA         `devral` 3 gun ONCE (saat kaydirilarak), sonra  -> FAIL (kosul b: damga devralma gununu gecti)
                  bugun yalniz `not`+`derle` (proje DEGISMEDI)
    PROJE_COMMIT  TAZE + proje dosyasi GERIYE tarihli commit      -> FAIL geri gelir (kosul c, git commit yolu)
    PROJE_MTIME   TAZE + izlenmeyen yeni proje dosyasi (mtime)    -> FAIL geri gelir (kosul c, mtime yolu)
  SAGLAM motorda hepsi YESIL; asagidaki bes sabotajin HER BIRI KENDI halinde KIRMIZI yakmalidir (hedef hal TAMAMI isirmali):
    M-DV1 KAYIT YAZIMI KAPALI        `devral` `devralma_tarihi` yazmaz                   -> TAZE
    M-DV2 MUHUR DISI KAYIT KABUL     zincir dogrulamasi atlanir (elle eklenen kayit gecer) -> SAHTE
    M-DV3 DAMGA KOSULU KALKAR        (b) yok: damga ilerlese de muafiyet surer             -> DAMGA
    M-DV4 COMMIT YOLU KORLESIR       (c) commit-tarihi kolunda atlanir                     -> PROJE_COMMIT
    M-DV5 PROJE KOSULU HER ZAMAN DOGRU (c) her zaman tutar                                 -> PROJE_MTIME

NE OLCMEZ
  Elle yeniden HESAPLANMIS (hash'i tutan) sahte halka — zincir ANAHTARSIZDIR (SKILL.md/README bilinen sinir). `kur` ile kurulan uyuyan proje
  muafiyet ALMAZ (KAYITSIZ hali bunu sabitler). Eski motorla devral'lanmis proje (kayit yok) muafiyet almaz. Ayni gun yapilan proje degisikligi
  H14'te `es` verir (normal hukum) — FAIL geri gelmesi icin degisikligin tarihi damganin `gecikme` gunden gerisinde kalmalidir.

KULLANIM    python3 faz0/h14_devralma_mutanti.py [motor.py]
CIKIS KODU  0 saglam YESIL ve bes mutantin HEPSI kendi halinde KIRMIZI yakti · 1 saglam kirmizi / mutant KACTI · 2 OLCULEMEDI
"""
import datetime as _dt
import json
import os
import re
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
GUN = 40                      # uyuyan projenin yasi: `hafiza_gecikme_gun` (2) her yonde RAHATCA asilir
HALLER = ["TAZE", "KAYITSIZ", "SAHTE", "DAMGA", "PROJE_COMMIT", "PROJE_MTIME"]

# `devral` N gun ONCE yapilmis gibi kosmak icin SAAT KAYDIRICI (yalniz OLCUM aleti; motorun `_dt` modulu sarilir, giris noktasi AYNI).
_SAAT = (
    "import atexit, datetime as real, importlib.util, sys, types\n"
    "geri = int(sys.argv[1]); motor = sys.argv[2]\n"
    "d = real.timedelta(days=geri)\n"
    "class FD(real.date):\n"
    "    @classmethod\n"
    "    def today(cls):\n"
    "        return real.date.today() - d\n"
    "class FDT(real.datetime):\n"
    "    @classmethod\n"
    "    def now(cls, tz=None):\n"
    "        return real.datetime.now(tz) - d\n"
    "shim = types.SimpleNamespace(**{n: getattr(real, n) for n in dir(real) if not n.startswith('__')})\n"
    "shim.date = FD; shim.datetime = FDT\n"
    "spec = importlib.util.spec_from_file_location('hz', motor); m = importlib.util.module_from_spec(spec)\n"
    "sys.modules['hz'] = m; spec.loader.exec_module(m); m._dt = shim\n"
    "sys.argv = [motor] + sys.argv[3:]\n"
    "atexit.register(m.kilit_birak); m._guvenli_calistir()\n"
)


class Kurulamadi(Exception):
    """Duzenegin KENDISI kurulamadi. Kapinin saglam/kor oldugu anlamina GELMEZ."""


def git_ortami(taban):
    g = os.path.join(taban, "gitconfig-global")
    if not os.path.isfile(g):
        with open(g, "w", encoding="utf-8", newline="\n") as f:
            f.write("[user]\n\tname = h14dv\n\temail = h14dv@example.invalid\n[init]\n\tdefaultBranch = main\n[commit]\n\tgpgsign = false\n")
    haric = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT")   # baska deponun ortami sizmasin
    ortam = dict((k, v) for k, v in os.environ.items() if k not in haric)
    return dict(ortam, GIT_CONFIG_GLOBAL=g, PYTHONIOENCODING="utf-8")


def git(ortam, kok, *args, tarih=None):
    e = dict(ortam)
    if tarih:
        e["GIT_AUTHOR_DATE"] = e["GIT_COMMITTER_DATE"] = "%sT12:00:00" % tarih.isoformat()
    r = subprocess.run(["git"] + list(args), cwd=kok, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        raise Kurulamadi("git %s: %s" % (args[0], (r.stderr or r.stdout).strip()[:140]))
    return r.stdout


def kos(motor, arglar, kok, ortam, gun_geri=0):
    on = [sys.executable, "-X", "utf8"] + (["-c", _SAAT, str(gun_geri), motor] if gun_geri else [motor])
    r = subprocess.run(on + arglar + ["--kok", kok], env=ortam, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
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


DURUM = "\n".join(["# Sentetik uyuyan proje", "",
                   "## GUNCEL DURUM", "uyuyan proje", "", "## SONRAKI ADIM", "devral", "", "## ACIK KARARLAR", "yok", "",
                   "## SABIT CERCEVE", "cerceve", "", "## KIRMIZI CIZGILER", "yok", "", "## KARAR GUNLUGU", "yok", "", "## ARSIV DIZINI", "yok", ""])
CLAUDE = "# Sentetik\n> Canli defter: DURUM.md - her oturum basinda once onu oku (hafiza-kur).\n"


def iskelet(taban, ad, ortam):
    """Uyuyan proje: git deposu, kod.py + DURUM.md + CLAUDE.md GUN gun once commit'li. -> (kok, eski commit ct)."""
    kok = os.path.join(taban, ad)
    os.makedirs(kok)
    git(ortam, kok, "init", "-q")
    for dosya, icerik in (("kod.py", "DEGER = 1\n"), ("DURUM.md", DURUM), ("CLAUDE.md", CLAUDE)):
        with open(os.path.join(kok, dosya), "w", encoding="utf-8", newline="\n") as f:
            f.write(icerik)
    git(ortam, kok, "add", "-A")
    git(ortam, kok, "commit", "-q", "-m", "eski", tarih=_dt.date.today() - _dt.timedelta(days=GUN))
    ct = int(git(ortam, kok, "show", "-s", "--format=%ct", "HEAD").strip())
    return kok, ct


def commitle(ortam, kok, mesaj, tarih=None):
    git(ortam, kok, "add", "-A")
    git(ortam, kok, "commit", "-q", "-m", mesaj, tarih=tarih or _dt.date.today())


def devral_et(motor, kok, ortam, gun_geri=0):
    rc, c = kos(motor, ["devral", "--esle", "canli=DURUM.md"], kok, ortam, gun_geri)
    if rc != 0:
        raise Kurulamadi("devral basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))


def sahte_halka_ekle(kok, ct):
    """Muhur DISI kayit: son halkaya BAGLI, DEVIR turunde, devralma kaydi tasiyan ama HASH'i tutmayan elle halka."""
    zincir = os.path.join(kok, "arsiv", "hafiza", "_ZINCIR.jsonl")
    satirlar = [x for x in open(zincir, encoding="utf-8").read().split("\n") if x.strip()]
    son = json.loads(satirlar[-1])
    sahte = {"t": _dt.datetime.now().isoformat(timespec="seconds"), "tur": "DEVIR", "gerekce": "elle eklendi (sahte)", "yuk": son["yuk"],
             "ek": {"devralma_tarihi": _dt.date.today().isoformat(), "proje_son_t": ct}, "onceki": son["halka"], "halka": "0" * 64}
    with open(zincir, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(sahte, ensure_ascii=False) + "\n")


def kapi(motor, kok, ortam):
    rc, c = kos(motor, ["kapi"], kok, ortam)
    return rc, c


def h14_coz(c):
    """-> (uyari satirlari, FAIL satirlari, SONUC satiri). UYARI N kanalinda (`· ` onekli), FAIL oneksiz `[H14]`."""
    uyari, fail, sonuc = [], [], ""
    for s in c.split("\n"):
        t = s.strip()
        if t.startswith("· [H14] UYARI devralma ani"):
            uyari.append(t)
        elif t.startswith("[H14]"):
            fail.append(t)
        elif t.startswith("SONUC"):
            sonuc = t
    return uyari, fail, sonuc


def gozle(motor, taban):
    """-> {hal: (exit, uyari, fail, sonuc)}. Halleri KURAR (devral dahil: sabotaj `devral`i da bozabilir), `kapi` kosar."""
    os.makedirs(taban, exist_ok=True)
    ortam = git_ortami(taban)
    bugun = _dt.date.today()
    kokler = {}
    k, _ = iskelet(taban, "taze", ortam)                                   # TAZE
    devral_et(motor, k, ortam)
    commitle(ortam, k, "devral")
    kokler["TAZE"] = k
    k, ct = iskelet(taban, "kayitsiz", ortam)                              # KAYITSIZ (`kur`: kayit yok)
    rc, c = kos(motor, ["kur", "--ad", "H14DV", "--yine-de"], k, ortam)      # DURUM.md TANINIR: beyanli gevseklik (zincire duser)
    if rc != 0:
        raise Kurulamadi("kur basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))
    commitle(ortam, k, "kur")
    kokler["KAYITSIZ"] = k
    k2 = os.path.join(taban, "sahte")                                      # SAHTE: KAYITSIZ'in kopyasi + elle halka
    shutil.copytree(k, k2)
    sahte_halka_ekle(k2, ct)
    kokler["SAHTE"] = k2
    k, _ = iskelet(taban, "damga", ortam)                                  # DAMGA: devral 3 gun ONCE, bugun yalniz `not`
    devral_et(motor, k, ortam, gun_geri=3)
    commitle(ortam, k, "devral (3 gun once)", tarih=bugun - _dt.timedelta(days=3))
    rc, c = kos(motor, ["not", "--konu=genel-durum", "--tur=durum", "--metin=devralmadan sonra yalniz not (proje degismedi)"], k, ortam)
    if rc != 0:
        raise Kurulamadi("not basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))
    rc, c = kos(motor, ["derle"], k, ortam)                                # derle damgayi BUGUNE tasir (devralma gununden SONRA)
    if rc not in (0, 1):                                                   # exit 1 = derleme YAZILDI ama icindeki kapi FAIL (H14 ILERIDE donmus: beklenen)
        raise Kurulamadi("derle basarisiz (exit %s): %s" % (rc, c.strip().split("\n")[-1][:140]))
    commitle(ortam, k, "yalniz not+derle")
    kokler["DAMGA"] = k
    k, _ = iskelet(taban, "proje_commit", ortam)                           # PROJE_COMMIT: geriye tarihli proje commit'i
    devral_et(motor, k, ortam)
    commitle(ortam, k, "devral")
    with open(os.path.join(k, "kod.py"), "a", encoding="utf-8", newline="\n") as f:
        f.write("DEGER = 2   # devralmadan sonra degisti\n")
    commitle(ortam, k, "proje degisti", tarih=bugun - _dt.timedelta(days=20))
    kokler["PROJE_COMMIT"] = k
    k, _ = iskelet(taban, "proje_mtime", ortam)                            # PROJE_MTIME: izlenmeyen yeni dosya (mtime yolu)
    devral_et(motor, k, ortam)
    commitle(ortam, k, "devral")
    yeni = os.path.join(k, "yeni.py")
    with open(yeni, "w", encoding="utf-8", newline="\n") as f:
        f.write("YENI = 1\n")
    ts = _dt.datetime.combine(bugun - _dt.timedelta(days=20), _dt.time(12, 0)).timestamp()
    os.utime(yeni, (ts, ts))
    kokler["PROJE_MTIME"] = k
    out = {}
    for hal, kok in kokler.items():
        rc, c = kapi(motor, kok, ortam)
        u, f, s = h14_coz(c)
        out[hal] = (rc, u, f, s)
    return out


_UYARI = re.compile(r"^· \[H14\] UYARI devralma ani: proje (\d+) gundur uyuyor \(devral (\d{4}-\d{2}-\d{2})\); "
                    r"proje degisince ya da damga ilerleyince normal hukum doner$")


def ihlaller(g):
    """-> [(hal, mesaj)] — bos liste = YESIL. Saglam/sabotajli motor AYNI fonksiyonla yargilanir."""
    out = []
    rc, u, f, s = g["TAZE"]
    m = _UYARI.match(u[0]) if len(u) == 1 else None
    if not m or int(m.group(1)) != GUN or m.group(2) != _dt.date.today().isoformat():
        out.append(("TAZE", "TEK `[H14] UYARI devralma ani: proje %d gundur uyuyor (devral %s); ...` beklenir: uyari=%r fail=%r"
                    % (GUN, _dt.date.today().isoformat(), u, f)))
    if f:
        out.append(("TAZE", "taze devralda [H14] FAIL basildi: %r" % f))
    if rc != 0 or not s.startswith("SONUC: YESIL"):
        out.append(("TAZE", "H14 exit'i degistirmemeli: kapi exit %s, %r (tum kapi YESIL beklenir)" % (rc, s)))
    for hal in ("KAYITSIZ", "SAHTE", "DAMGA", "PROJE_COMMIT", "PROJE_MTIME"):
        rc, u, f, s = g[hal]
        if u:
            out.append((hal, "muafiyet VERILMEMELIYDI ama UYARI basildi: %r" % u))
        if len(f) != 1 or "ILERIDE" not in f[0]:
            out.append((hal, "bugunku FAIL (`[H14] ... ILERIDE`) BIREBIR beklenir: %r" % f))
        if rc != 1:
            out.append((hal, "FAIL varken kapi exit 1 olmali (exit %s, %r)" % (rc, s)))
    return out


# ad, aciklama, hedef hal(ler), [(eski, yeni)]. `eski` motorda TAM 1 kez gecmelidir.
MUTANTLAR = [
    ("M-DV1 KAYIT YAZIMI KAPALI", "`devral` `devralma_tarihi` yazmaz (kapi kaydin varligini olcmeli)", {"TAZE"},
     [("    kayit[\"devralma_tarihi\"] = bugun()\n", "    pass   # MUTANT\n")]),
    ("M-DV2 MUHUR DISI KAYIT KABUL", "zincir dogrulamasi atlanir (elle eklenen kayit gecer)", {"SAHTE"},
     [("        if not os.path.isfile(y.zincir) or any(not h.startswith(\"~\") for h in zincir_dogrula(y)):\n            return None\n",
       "        if not os.path.isfile(y.zincir):   # MUTANT\n            return None\n")]),
    ("M-DV3 DAMGA KOSULU KALKAR", "(b) yok: damga devralma gununu gecse de muafiyet surer", {"DAMGA"},
     [("    if t_son > tarih:\n        return None\n", "    pass   # MUTANT\n")]),
    ("M-DV4 COMMIT YOLU KORLESIR", "(c) git commit tarihi kolunda atlanir", {"PROJE_COMMIT"},
     [("    if en_yeni_f is None or en_yeni_t != proje_son:\n        return None\n",
       "    if en_yeni_f is None or (en_yeni_t != proje_son and en_yeni_f != \"(commit'li dosyalar)\"):   # MUTANT\n        return None\n")]),
    ("M-DV5 PROJE KOSULU HER ZAMAN DOGRU", "(c) her zaman tutar (proje degismis olsa da)", {"PROJE_MTIME"},
     [("    if en_yeni_f is None or en_yeni_t != proje_son:\n        return None\n", "    pass   # MUTANT\n")]),
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
    print("H14 DEVRALMA MUTANTI — taze devralda H14 ILERIDE: kayitli muafiyet yalniz UC kosul birlikte · platform: %s" % sys.platform)
    print("motor: %s" % motor)
    print(CIZGI)
    taban = tempfile.mkdtemp(prefix="h14dv_")
    try:
        try:
            g = gozle(motor, os.path.join(taban, "temiz"))
        except Kurulamadi as e:
            print("OLCULEMEDI: haller kurulamadi: %s" % e)
            return 2
        for hal in HALLER:
            rc, u, f, s = g[hal]
            print("  %-13s exit %s · %-6s · %s" % (hal, rc, "UYARI" if u else "FAIL" if f else "(H14 satiri yok)", (u or f or [""])[0][:100]))
        temiz = ihlaller(g)
        print("  SAGLAM MOTOR (%d hal)            %s" % (len(HALLER), "YESIL" if not temiz else "KIRMIZI"))
        for hal, m in temiz:
            print("      ! %-13s %s" % (hal, m[:170]))
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
                print("  ?  %-34s OLCULEMEDI  %s" % (ad, e))
                continue
            haller = {h for h, _ in ih}
            if hedef <= haller:
                isirdi.append(ad)
                print("  +  %-34s ISIRDI      hedef hal: %s · tum ihlal halleri: %s" % (ad, ",".join(sorted(hedef)), ",".join(sorted(haller))))
            elif ih:
                kacti.append(ad)
                print("  !  %-34s YANLIS SEBEP ihlal %s var ama HEDEF hal (%s) susuyor" % (ad, ",".join(sorted(haller)), ",".join(sorted(hedef))))
            else:
                kacti.append(ad)
                print("  !  %-34s KACTI       kapi YESIL kaldi -> bu sabotaj OLCULMUYOR: %s" % (ad, aciklama))
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
    print("  Saglam motor YESIL, bes sabotajin hepsi KENDI halinde KIRMIZI: devralma muafiyeti yalniz UC kosul birlikte tutunca veriliyor.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as e:      # zaman asimi / kopyalama hatasi: ARAC kusuru
        print("OLCULEMEDI: arac hatasi (%s: %s) — kapi hukmu YOK." % (type(e).__name__, e))
        sys.exit(2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — KARAR ADRES DEFTERI KABUL KAPISI (besli-paket/IS_EMRI_P4_KARAR_ADRES_DEFTERI.md, KALEM 3).

NEDEN VAR (olculdu 12 Eki 2026, Momentum d4b5417; besli-paket/OLCUM_RAPORU_07EKIM_E2_KOR_OKUMA.md)
  Kor okumada KARAR sorularinin cevabi Momentum'da YAZILIYDI, eksik olan ADRESTI (hafiza-kur 0,00 · Graphify 1,42). `derle` artik
  karar kaynagi basina ADRES (dosya:satir) + BIREBIR ALINTI yaziyor (KALEM 1-2). Bu kapi onu MEKANIK olcer: dort ALTIN kararin
  (kor okumada sorulan gerekce/bedel/alternatif sorulari) en az UCU `karar-kaynagi` blogunda ADRESLENMIS olmali.

NE OLCER
  Momentum'un dort altin kaynaginin YAPISINI (dosya adi, satir numarasi, baslik/satir ici bicim) FIXTURE olarak kurar (Momentum CI'da
  YOK; ham Momentum sonucu `--momentum <dizin>` ile ayrica olculur), `devral --esle canli=DURUM.md,kural=CLAUDE.md` + `derle` kosar ve
  blogta her altin icin "gosterir" hukmu verir. "Gosterir" = ayni dosyaya isaret eden bir adresin satiri altin araligin ICINDE
  (R3 icin ayrica alintida `COEP`). Esik (P4.1): 4 altinin 4'u. Fixture kurulamazsa ya da blok yoksa KIRMIZI (BOS YESIL YOK).
    R1 IS-EMRI-o83-kimlik.md:44-45           satir ici `*Gerekce: ...*`
    R2 docs/ADR/0002-senkron-mekanigi.md:193-196   `*Gerekce:*` + `*Kabul edilen odunlesim ...*`
    R3 docs/ADR/0004-web-capraz-koken-izolasyonu.md:66-71   `🔴 **...gerekcesi COEP BLOKLAMASI DEGILDIR.**` ALINTISI (COEP gecmeli)
    R4 IS-EMRI-o86-D.md:51-57 (+ 4-7)        `### 2.3 Neden ...` basligi ya da L7 `Gerekcesi §2.3'te ...` alintisi
  KAPININ KENDI ISIRIGI: ayni olcum dort sabotajli motorla KOSULUR, dordunde de KIRMIZI olmalidir (yesil kalirsa kapi KOR, exit 1):
  M-Z1 satir numarasi kayar · M-K1 `IS-EMRI-*` deseni duser · M-Z18 satir ici sinif 3 (`🔴`/`**` + gerekce) KAPALI (R3'un L66 alintisi
  kaybolur: yalniz L54 basligi artik YETMEZ) · M-Z25 eski sira (KALEM 2: GEREKCESIZ kayitlar alintilanin onune gecer, R4 butceden duser).

CIKIS KODU  0 temiz motor 4/4 VE dort sabotajli motorda KIRMIZI · 1 temiz motor < 4/4 ya da kapi KOR · 2 OLCULEMEDI (git yok, duzenek
            kurulamadi)
KULLANIM    python faz0/karar_adres_kapisi.py [motor.py] [--momentum <Momentum dizini>]
"""
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

for _a in (sys.stdout, sys.stderr):
    try:
        _a.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AYNI = os.path.dirname(os.path.abspath(__file__))
VARSAYILAN = os.path.join(AYNI, "..", "skill", "scripts", "hafiza.py")
CIZGI = "-" * 78
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="p4kapi", GIT_AUTHOR_EMAIL="p4@example.invalid",
                GIT_COMMITTER_NAME="p4kapi", GIT_COMMITTER_EMAIL="p4@example.invalid", GIT_CONFIG_NOSYSTEM="1")
# (kod, dosya, [(a, b), ...] aralik adaylari, adreste GECMESI gereken metin ya da None). P4.1: R3 icin yalniz `## 3. GEREKCE` basligi (L54) YETMEZ —
# aralik 66-71 icinde ve `COEP` iceren ALINTI sarttir; R4 icin L7 alintisi ya da L51 basligi (aralik 4-7 ya da 51-57).
ALTIN = (("R1", "IS-EMRI-o83-kimlik.md", ((44, 45),), None), ("R2", "docs/ADR/0002-senkron-mekanigi.md", ((193, 196),), None),
         ("R3", "docs/ADR/0004-web-capraz-koken-izolasyonu.md", ((66, 71),), "COEP"), ("R4", "IS-EMRI-o86-D.md", ((51, 57), (4, 7)), None))
ESIK = 4
ADRES = re.compile(r"^  (?:gerekce|bedel|alternatif) (\S+?):(\d+) (.*)$", re.M)
BLOK = re.compile(r'<!-- blok konu="karar-kaynagi"[^>]*-->\n(.*?)\n<!-- /blok -->', re.S)


class Kurulamadi(Exception):
    pass


def _sil(yol):
    """Gecici dizini SIL (Windows'ta salt-okunur git objeleri: yazilabilir yapip yeniden dener; artik birakmaz)."""
    def onar(fonk, p, *_):
        try:
            os.chmod(p, 0o700)
            fonk(p)
        except OSError:
            pass
    shutil.rmtree(yol, **({"onexc": onar} if sys.version_info >= (3, 12) else {"onerror": onar}))


def _dosya(satirlar, toplam):
    """{satir_no: metin} + dolgu -> dosya metni (TAM `toplam` satir; dolgu satirlari anahtar tasimaz)."""
    return "\n".join(satirlar.get(i, "dolgu satiri %d." % i) for i in range(1, toplam + 1)) + "\n"


def fixture():
    """Dort altinin yapisi (dosya adi + satir konumu + bicim)."""
    r1 = {1: "# IS-EMRI-o83 — kimlik cekirdegi", 43: "2. **Uclar:** `POST /v1/auth/register`.",
          44: "3. **Parola hash'i:** ASP.NET Core'un **yerlesik** `PasswordHasher<T>`i kullanilir.",
          45: "   *Gerekçe: yeni bağımlılık getirmez ⇒ lisans + CVE kapısı açılmaz.* BCrypt/Argon2 paketi ekleme."}
    r2 = {1: "# ADR 0002 — Senkron mekanigi", 3: "Durum: Kabul edildi",
          193: "**K2-I1 — Istemci uzlastirma rolu: SUNUCU-OTORITER, TEK RESOLVER. [PAZARLIKSIZ]**",
          194: "Flutter istemcisi **kendi HLC/CRDT resolver'ini TASIMAZ.**",
          195: "*Gerekçe:* ikinci bir resolver, ikinci bir doğruluk kaynağı demektir ve bu projede o sınıf hatanın maliyeti ölçüldü.",
          196: "*Kabul edilen ödünleşim (adlandırıldı):* sunucu farklı karar verirse istemcide geri-alma/titreme görülebilir."}
    r3 = {1: "# ADR 0004 — Web Çapraz-Köken İzolasyonu", 3: "Durum: Kabul edildi", 15: "## 1. BAĞLAM — iskeletin sorusu",
          27: "## 2. KARAR (üç madde)", 54: "## 3. GEREKÇE — yalnız ölçülmüş olan",
          66: "🔴 **`--no-web-resources-cdn`'in gerekçesi COEP BLOKLAMASI DEĞİLDİR.** `gstatic` 8 Ağu 2026 09:50",
          67: "UTC'de de cross-origin-resource-policy: cross-origin gönderiyordu.", 71: "yüklenirdi. Bayrağın ölçülmüş değeri başkadır.",
          77: "## 4. REDDEDİLEN ALTERNATİFLER (her biri ölçülmüş gerekçeyle)", 130: "## 7. SONUÇLAR ve BEYAN EDİLMİŞ BEDELLER"}
    r4 = {1: "# IS-EMRI-o86-D — katilim-sonrasi gecmis (backfill) · SUNUCU-ONLY", 3: "`MOD: NORMAL` · Yazan: Cowork",
          4: "**Kilit K-o89/1 [Onur, 5 Eyl]:** A sikki — uyelik aninda resync borcu.",
          5: "**Kilit K-o89/2 [Cowork olcumu, ayni gun]:** borcun BICIMI tuketilen bayrak DEGIL,",
          7: "Gerekcesi §2.3'te; tuketilen bayrak coklu cihazda sessiz kaybediyordu.",
          33: "### 1.2 NEDEN — onceki bayrak", 51: '### 2.3 Neden "tuketilen bayrak" DEGIL',
          52: "Bayrak bir kez true donup temizlenseydi: ayni kullanicinin IKINCI cihazi"}
    d = {"IS-EMRI-o83-kimlik.md": _dosya(r1, 50), "docs/ADR/0002-senkron-mekanigi.md": _dosya(r2, 200),
         "docs/ADR/0004-web-capraz-koken-izolasyonu.md": _dosya(r3, 140), "IS-EMRI-o86-D.md": _dosya(r4, 60),
         "DURUM.md": "# DURUM\n\n## GUNCEL DURUM\n- durum\n\n## SABIT CERCEVE\n- ders 1\n\n## ARSIV DIZINI\n",
         "CLAUDE.md": "# kural evi\n- kural\n"}
    # gercek Momentum'un gurultusu: alanli doldurma kayitlari (butce yolu kosar; altin kaynaklar siralamada ONLARIN ARASINDA)
    for i in range(10):
        d["IS-EMRI-o84-f%02d.md" % i] = _dosya({1: "# IS-EMRI-o84-f%02d — doldurma kaydi" % i, 3: "## Neden — doldurma %d" % i,
                                                  5: "*Gerekçe: doldurma kaydi %d, ADRES defteri butce yolunu kosar.*" % i}, 8)
    # GEREKCESIZ doldurma (dosya adi siralamasinda R4'ten ONCE): dogru sirada alintili kayitlarin ARKASINA duser; eski sirada butceyi yer
    for i in range(48):
        d["IS-EMRI-o85-g%02d.md" % i] = "# Bos doldurma %02d — alan yok\n\nsade metin\n" % i
    return d


def _kos(motor, kok, *arglar):
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", motor] + list(arglar) + ["--kok", kok], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=ortam, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _git(kok, *a):
    return subprocess.run(["git", "-C", kok, "-c", "commit.gpgsign=false"] + list(a), capture_output=True, env=_GIT_ENV)


def kur_ve_derle(motor, kok, dosyalar=None):
    """kok'u (fixture ya da kopya) hazirla -> `devral` + `derle` -> karar-kaynagi blogunun govdesi (str)."""
    if dosyalar is not None:
        for ad, ic in dosyalar.items():
            y = os.path.join(kok, *ad.split("/"))
            os.makedirs(os.path.dirname(y), exist_ok=True)
            with io.open(y, "w", encoding="utf-8", newline="\n") as f:
                f.write(ic)
        if _git(kok, "init", "-q").returncode != 0:
            raise Kurulamadi("git init basarisiz")
        _git(kok, "add", "-A")
        _git(kok, "commit", "-q", "--allow-empty", "-m", "ilk")
    rc, c = _kos(motor, kok, "devral", "--esle=canli=DURUM.md,kural=CLAUDE.md", "--ad", "P4")
    if rc != 0:
        raise Kurulamadi("devral exit=%s: %s" % (rc, c.strip().split("\n")[-1][:200]))
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "--allow-empty", "-m", "devral")
    _kos(motor, kok, "derle")        # blogu `devral` yazar; `derle` fragmansizken blogu DEGISTIRMEZ (idempotans) — yine de kosulur
    with io.open(os.path.join(kok, "DURUM.md"), encoding="utf-8") as f:
        m = BLOK.search(f.read())
    return m.group(1) if m else ""


def hukum(kok, blok):
    """-> ([(kod, yol, aralik, gosterir, kanit)], gosteren_sayi). "Gosterir" = ayni dosyaya isaret eden bir adres altin araliklardan
    birinin ICINDE ve (varsa) adresin alinti/baslik metni zorunlu sozcugu icerir. Baslik-bolum kurali YOK (P4.1)."""
    adres = [(y, int(n), r) for y, n, r in ADRES.findall(blok)]
    out = []
    for kod, yol, araliklar, must in ALTIN:
        kanit = next(((y, n) for y, n, r in adres
                      if y == yol and any(a <= n <= b for a, b in araliklar) and (must is None or must in r)), None)
        out.append((kod, yol, araliklar, kanit is not None, kanit))
    return out, sum(1 for x in out if x[3])


def _yaz_tablo(t, n):
    for kod, yol, araliklar, g, kanit in t:
        print("  %-3s %-52s %-10s  %s" % (kod, yol, ",".join("%d-%d" % x for x in araliklar),
                                          ("GOSTERIR  (%s:%d)" % kanit) if g else "GOSTERMEZ"))
    print("  altin eslesme: %d/%d (esik %d)" % (n, len(t), ESIK))


def olc_fixture(motor, tmp):
    kok = os.path.join(tmp, "f")
    os.makedirs(kok)
    blok = kur_ve_derle(motor, kok, fixture())
    if not blok.strip():
        raise Kurulamadi("karar-kaynagi blogu YOK (fixture): BOS YESIL verilmez")
    t, n = hukum(kok, blok)
    return t, n, blok


def _sabotajli_motor(motor, tmp, onek):
    """Harness'in KS_SABOTAJLAR girdisini (ad `onek`le baslar) motorun kopyasina uygular -> yol. Capa 1 kez gecmeli."""
    spec = importlib.util.spec_from_file_location("gdk_kapi", os.path.join(AYNI, "guncel_durum_kapisi_mutanti.py"))
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    ad, _et, ankor, yeni, _kol = next(x for x in h.KS_SABOTAJLAR if x[0].startswith(onek + " "))
    s = io.open(motor, encoding="utf-8", newline="").read()
    if s.count(ankor) != 1:
        raise Kurulamadi("sabotaj capasi %d yerde (1 olmali): %s" % (s.count(ankor), ad))
    y = os.path.join(tmp, "hafiza_%s.py" % onek.replace("-", ""))
    with io.open(y, "w", encoding="utf-8", newline="") as f:
        f.write(s.replace(ankor, yeni))
    return y, ad


def main():
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    motor = os.path.abspath(arg[0] if arg else VARSAYILAN)
    mom = next((a[len("--momentum="):] for a in sys.argv[1:] if a.startswith("--momentum=")), None)
    if not shutil.which("git"):
        print("SONUC: OLCULEMEDI — git yok.")
        return 2
    print(CIZGI)
    print("KARAR ADRES DEFTERI KABUL KAPISI — motor: %s · platform: %s" % (os.path.basename(motor), sys.platform))
    print(CIZGI)
    tmp = tempfile.mkdtemp(prefix="p4kapi_")
    try:
        try:
            if mom:
                kopya = os.path.join(tmp, "momentum")
                shutil.copytree(mom, kopya)
                blok = kur_ve_derle(motor, kopya)
                print("--- HAM karar-kaynagi BLOGU (Momentum kopyasi) ---")
                print(blok)
                print("--- altin eslesme tablosu (Momentum) ---")
                t, n = hukum(kopya, blok)
                _yaz_tablo(t, n)
                print("  blok: %d bayt" % len(blok.encode("utf-8")))
                return 0 if n >= ESIK else 1
            t, n, blok = olc_fixture(motor, tmp)
            _yaz_tablo(t, n)
            if n < ESIK:
                print("\nSONUC: KIRMIZI — altin eslesme %d/%d (esik %d)." % (n, len(t), ESIK))
                return 1
            kor = []
            for onek in ("M-Z1", "M-K1", "M-Z18", "M-Z25"):
                y, ad = _sabotajli_motor(motor, tmp, onek)
                os.makedirs(os.path.join(tmp, onek))
                try:
                    _t, ns, _b = olc_fixture(y, os.path.join(tmp, onek))
                except Kurulamadi as e:
                    ns = -1
                    print("  sabotaj %s: motor kosusu basarisiz (%s) -> KIRMIZI sayilir" % (onek, e))
                durum = "KIRMIZI (ISIRDI)" if ns < ESIK else "YESIL (KACTI)"
                print("  sabotaj %-5s %-60s -> %d/4 %s" % (onek, ad[:60], max(ns, 0), durum))
                if ns >= ESIK:
                    kor.append(onek)
            if kor:
                print("\nSONUC: KAPI KOR — sabotajli motorda YESIL kaldi: %s" % ", ".join(kor))
                return 1
            print("\nSONUC: YESIL — altin %d/4, sabotajli dort motorda kapi KIRMIZI." % n)
            return 0
        except Kurulamadi as e:
            print("SONUC: OLCULEMEDI — %s" % e)
            return 2
    finally:
        _sil(tmp)


if __name__ == "__main__":
    sys.exit(main())

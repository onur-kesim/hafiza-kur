#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ 0 — WINDOWS DALI MUTANTI (uc kapi + dort mutant).

NEDEN VAR (olculdu 14 Agu 2026)
  `hafiza.py`'de `sys.platform == "win32"` yalnizca IKI yerde geciyor (sat. 899
  ve 4877) ve bu iki dal `faz0/` ile `capraz.yml`'de HIC ANILMIYOR. Yani motorun
  platforma OZGU tek yuzeyi, hicbir mutantla olculmuyordu. Ortak batarya uc
  platformda kosuyor olmak bunu KAPATMAZ: batarya POSIX'te de gecer, cunku
  bataryanin gordugu davranis platformdan bagimsiz olan davranistir.

  Ikisi de "gecmis kusurun yamasi"dir; yani sokulurse ESKI KUSUR geri gelir:
    DAL A  `_surec_yasiyor` -> `_surec_yasiyor_win`  (Y-1)
           Windows'ta `os.kill(pid, 0)` VARLIK SINAMAZ (signal.CTRL_C_EVENT == 0).
           Dal sokulurse teshis HER ZAMAN "pid YASIYOR" der; bayat kilit asla
           taninmaz, B4-1'in sizan kilidi Windows'ta hic temizlenemez.
    DAL B  `_boru_koptu_mu` win32 kolu                (Y-3)
           Windows'ta kirik boru `BrokenPipeError` degil ham `OSError` EINVAL(22)
           atar. Dal sokulurse `kapi | head` KIRMIZI hukmu YUTAR (exit 120 / 3).

NE OLCER — UC AYRI YUZEY
  KAPI-1 (ENVANTER, depo metni, uc platformda)
      Motordaki her platform dali (`sys.platform == "win32"`, `os.name == "nt"`,
      `platform.system()`) BILINEN_YUZEYLER'den birinin govdesinde olmali.
      Kural fonksiyon ADIYLA taniml, MUAFIYET LISTESI YOK.
      Ne yakalar: "ucuncu bir platform dali dogdu ve mutanti yok" — yani bu
      aracin KENDI kapsaminin bayatlamasi. Eksik dali KOVALAMAZ (o KAPI-2'nin
      isi); boylece KAPI-2 ile ORTUSMEZ.

  KAPI-2 (DAVRANIS, birim + simulasyon, uc platformda)
      H-a  YONLENDIRME : `_surec_yasiyor` win32'de win dalina GIDER, POSIX'te GITMEZ.
      H-b  AYRIM       : `_surec_yasiyor_win` 'var' · 'yok' · 'bilmiyorum'u AYIRIR
                         (hata 5 -> True · hata 87 -> False · 259 -> True ·
                          baska cikis kodu -> False · ctypes yok -> None).
      H-c  BORU        : EINVAL win32'de boru kopmasi SAYILIR, POSIX'te SAYILMAZ
                         (D-1: POSIX'te EINVAL bambaska bir seydir, yutmak gercek
                          hatayi gizler); EPIPE her iki platformda sayilir.

  KAPI-3 (CANLI, GERCEK ctypes, YALNIZ gercek win32'de)
      Kendi pid'i -> True · bitmis cocuk pid -> False. win32 disinda OLCULEMEDI
      der; YESIL DEMEZ. Simulasyon CI'nin windows isinin YERINE GECMEZ.

NE OLCMEZ (hukum degil, SINIR — gizlenmez)
  1. DAL B'nin TUMDEN silinmesinin ayri mutanti YOK. H-c'nin win32 kolu onu
     yakalar (tek kapi), ama "her duzeltmeye ayri mutant" olcutunu tam
     karsilamaz. M-4 bilincli olarak D-1 eksenini (kosulsuzluk) secti.
  2. H-b'nin bes halinden yalniz 259 halinin mutanti var; 5/87/None kollari
     TEMIZ motorda SINANIR ama mutantla ISIRTILMAZ.
  3. STILL_ACTIVE 259 ayni zamanda gecerli bir cikis kodudur; tam 259 ile cikmis
     surec 'yasiyor' gorunur. Motorun bilinen siniri, bu arac onu olcmez.
  4. Simulasyon gercek Windows'u olcmez. Gercek hukum KAPI-3'ten ve CI'nin
     windows-latest isinden gelir.

CIKIS KODLARI
  0  uc kapi da temiz (KAPI-3 win32 disinda OLCULEMEDI) VE 4/4 mutant AYRI eksende ISIRDI
  1  bir kapi kirmizi, ya da bir mutant KACTI/ORTUSTU (kapi kor)
  2  olculemedi (motor okunamadi, govde bulunamadi) — sessiz PASS verilmez
"""
import errno as _errno
import io
import os
import re
import subprocess
import sys


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

# 🔴 Y-2 DERSI (14 Agu 2026, CI #41): kardes arac `yol_ayraci_kapisi.py` bu blok
#    OLMADAN yazildi ve windows-latest'te "ISIRDI ✓" satirindaki U+2713 yuzunden
#    UnicodeEncodeError ile COKTU — kapilari olcerken KENDI ciktisinda. Ayrim
#    Turkce/Ingilizce DEGIL, UTF-8 / eski kod sayfasidir. Bu blok silinmez.

VARSAYILAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "skill", "scripts", "hafiza.py")

# Platform dalinin MESRU olarak yasayabilecegi govdeler. Kural ADLA taniml.
BILINEN_YUZEYLER = ("_surec_yasiyor", "_boru_koptu_mu")

# Platform dalinin butun idiomlari — biri otekiyle GIZLENEMESIN diye.
_PLATFORM = re.compile(r'sys\.platform\s*==\s*["\']win32["\']'
                       r'|os\.name\s*==\s*["\']nt["\']'
                       r'|platform\.system\s*\(\s*\)')

_BASLIK = re.compile(r"^(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", re.M)


def govde_haritasi(s):
    """her ust-seviye def/class icin (ad, baslangic, bitis).

    `class` da haritalanir: yalniz `def` haritalayan kardes arac, bir sinifin
    icindeki satiri bir onceki fonksiyona YAZAR ve sahiplik yanlis cikar."""
    m = [(x.group(1), x.start()) for x in _BASLIK.finditer(s)]
    out = []
    for i, (ad, b) in enumerate(m):
        son = m[i + 1][1] if i + 1 < len(m) else len(s)
        out.append((ad, b, son))
    return out


def sahip(harita, i):
    for ad, b, e in harita:
        if b <= i < e:
            return ad
    return "<modul>"


def govde_metni(s, ad):
    """`ad` fonksiyonunun KAYNAK METNI (import YOK — yan etki yok)."""
    i = s.find("\ndef %s(" % ad)
    if i < 0:
        raise LookupError("%s bulunamadi" % ad)
    harita = govde_haritasi(s)
    for a, b, e in harita:
        if a == ad and b >= i:
            return s[b:e]
    raise LookupError("%s govdesi kesilemedi" % ad)


# ------------------------------------------------------------------- KAPI-1
def kapi1_envanter(s):
    """Listelenmemis bir govdede platform dali var mi?"""
    harita = govde_haritasi(s)
    kacaklar = []
    for mm in _PLATFORM.finditer(s):
        i = mm.start()
        ad = sahip(harita, i)
        if ad not in BILINEN_YUZEYLER:
            kacaklar.append((s.count("\n", 0, i) + 1, ad, mm.group(0)))
    return kacaklar


# --------------------------------------------------------- SAHTE ORTAM (K-2)
class _SahteSys(object):
    def __init__(self, platform):
        self.platform = platform


class _SahteOs(object):
    """os yerine gecen ince kabuk: yalniz `kill` verir ve cagriyi KAYDEDER."""

    def __init__(self, atilacak=None):
        self.kill_cagrildi = False
        self._atilacak = atilacak

    def kill(self, pid, sig):
        self.kill_cagrildi = True
        if self._atilacak is not None:
            raise self._atilacak


class _Fn(object):
    """oznitelik atanabilen cagrilabilir (k32.OpenProcess.restype = ... icin)."""

    def __init__(self, f):
        self._f = f

    def __call__(self, *a, **k):
        return self._f(*a, **k)


class _CUlong(object):
    def __init__(self, v=0):
        self.value = v


def sahte_ctypes(handle=1, son_hata=0, gec_ok=True, cikis=259, patlat=False):
    """`_surec_yasiyor_win`in dokundugu ctypes yuzeyinin TAMAMI, sahtesi."""

    def _gec(h, kod_nesnesi):
        kod_nesnesi.value = cikis
        return gec_ok

    k32 = type("K32", (object,), {})()
    k32.OpenProcess = _Fn(lambda a, b, c: handle)
    k32.CloseHandle = _Fn(lambda h: None)
    k32.GetExitCodeProcess = _Fn(_gec)

    def _windll(ad, use_last_error=False):
        if patlat:
            raise OSError("bu platformda WinDLL yok")
        return k32

    return type("Ctypes", (object,), {
        "WinDLL": staticmethod(_windll),
        "get_last_error": staticmethod(lambda: son_hata),
        "c_void_p": object, "c_int": object, "c_ulong": _CUlong,
        "POINTER": staticmethod(lambda t: t),
        "byref": staticmethod(lambda x: x),
    })()


def _yukle(kaynak_govde, ns_ekstra, sahte_modul=None, modul_adi="ctypes"):
    """govdeyi YALIN ad alaninda kur; istenirse `import X`i sahtesine baglar."""
    import builtins as _b
    ns = dict(ns_ekstra)
    if sahte_modul is not None:
        gercek = _b.__import__

        def _imp(ad, *a, **k):
            if ad == modul_adi:
                return sahte_modul
            return gercek(ad, *a, **k)
        yerli = dict(_b.__dict__)
        yerli["__import__"] = _imp
        ns["__builtins__"] = yerli
    exec(compile(kaynak_govde, "<govde>", "exec"), ns)
    return ns


# ------------------------------------------------------------------- KAPI-2
def kapi2_davranis(s):
    """H-a · H-b · H-c — her hal TEK bir seyi olcer."""
    bulgu = []
    try:
        g_yasiyor = govde_metni(s, "_surec_yasiyor")
        g_win = govde_metni(s, "_surec_yasiyor_win")
        g_boru = govde_metni(s, "_boru_koptu_mu")
    except LookupError as e:
        return [("H-*", "ÖLÇÜLEMEDİ: %s" % e)]

    # ---- H-a YONLENDIRME: win32'de win dalina GIDER, POSIX'te GITMEZ
    try:
        for plat, beklenen in (("win32", "WIN-DALI"), ("linux", True)):
            sos = _SahteOs()
            ns = _yukle(g_yasiyor, {
                "sys": _SahteSys(plat), "os": sos,
                "_surec_yasiyor_win": lambda pid: "WIN-DALI",
            })
            g = ns["_surec_yasiyor"](4242)
            if g != beklenen:
                bulgu.append(("H-a", "%s: beklenen %r, gelen %r" % (plat, beklenen, g)))
            elif plat == "win32" and sos.kill_cagrildi:
                bulgu.append(("H-a", "win32'de POSIX os.kill YINE cagrildi"))
    except Exception as e:                                   # noqa: BLE001
        bulgu.append(("H-a", "COKTU: %s" % e))

    # ---- H-b AYRIM: var · yok · bilmiyorum AYRI AYRI
    haller = (
        ("hata 5 (erisim yok) -> VAR", dict(handle=0, son_hata=5), True),
        ("hata 87 (pid yok)   -> YOK", dict(handle=0, son_hata=87), False),
        ("cikis 259 STILL_ACTIVE -> VAR", dict(handle=7, cikis=259), True),
        ("cikis 0 (bitmis)    -> YOK", dict(handle=7, cikis=0), False),
        ("ctypes yok -> OLCULEMEDI", dict(patlat=True), None),
        ("sorgu basarisiz -> OLCULEMEDI", dict(handle=7, gec_ok=False), None),
        ("hata 999 (bilinmez) -> OLCULEMEDI", dict(handle=0, son_hata=999), None),
    )
    for ad, kw, beklenen in haller:
        try:
            ns = _yukle(g_win, {"sys": _SahteSys("win32"), "os": _SahteOs()},
                        sahte_modul=sahte_ctypes(**kw))
            g = ns["_surec_yasiyor_win"](4242)
            if g is not beklenen:
                bulgu.append(("H-b", "%s: beklenen %r, gelen %r" % (ad, beklenen, g)))
        except Exception as e:                               # noqa: BLE001
            bulgu.append(("H-b", "%s: COKTU: %s" % (ad, e)))

    # ---- H-c BORU: EINVAL YALNIZ win32'de boru kopmasidir (D-1)
    try:
        boru = {}
        for plat in ("win32", "linux"):
            ns = _yukle(g_boru, {"sys": _SahteSys(plat), "_errno": _errno})
            boru[plat] = ns["_boru_koptu_mu"]
        e_inval = OSError(_errno.EINVAL, "Invalid argument")
        e_pipe = OSError(_errno.EPIPE, "Broken pipe")
        e_nospc = OSError(_errno.ENOSPC, "No space left")
        sinav = (
            ("win32", e_inval, True, "EINVAL win32'de boru kopmasi SAYILMADI"),
            ("linux", e_inval, False, "EINVAL POSIX'te YUTULDU (D-1 ihlali)"),
            ("win32", e_pipe, True, "EPIPE win32'de sayilmadi"),
            ("linux", e_pipe, True, "EPIPE POSIX'te sayilmadi"),
            ("win32", e_nospc, False, "ENOSPC (disk dolu) YUTULDU"),
            ("linux", e_nospc, False, "ENOSPC (disk dolu) YUTULDU"),
        )
        for plat, hata, beklenen, mesaj in sinav:
            if boru[plat](hata) is not beklenen:
                bulgu.append(("H-c", mesaj))
        e_win = OSError(0, "kirik")
        e_win.winerror = 109
        if boru["win32"](e_win) is not True:
            bulgu.append(("H-c", "winerror 109 win32'de sayilmadi"))
    except Exception as e:                                   # noqa: BLE001
        bulgu.append(("H-c", "COKTU: %s" % e))
    return bulgu


# ------------------------------------------------------------------- KAPI-3
def kapi3_canli(s, kaynak_govde=None):
    """GERCEK ctypes, GERCEK pid. win32 disinda None (= OLCULEMEDI) doner."""
    if sys.platform != "win32":
        return None
    try:
        g = kaynak_govde if kaynak_govde is not None else govde_metni(s, "_surec_yasiyor_win")
        ns = _yukle(g, {"sys": sys, "os": os})
        f = ns["_surec_yasiyor_win"]
    except Exception as e:                                   # noqa: BLE001
        return [("K3", "yuklenemedi: %s" % e)]
    bulgu = []
    try:
        if f(os.getpid()) is not True:
            bulgu.append(("K3", "kendi pid'i YASIYOR olarak olculmedi"))
    except Exception as e:                                   # noqa: BLE001
        bulgu.append(("K3", "kendi pid'inde COKTU: %s" % e))
    try:
        p = subprocess.Popen([sys.executable, "-c", "pass"])
        p.wait()
        if f(p.pid) is not False:
            bulgu.append(("K3", "bitmis cocuk pid %d YOK olarak olculmedi" % p.pid))
    except Exception as e:                                   # noqa: BLE001
        bulgu.append(("K3", "bitmis cocukta COKTU: %s" % e))
    return bulgu


# --------------------------------------------------------------- MUTANTLAR
# DORT AYRI EKSEN. Ikisi ayni hukmu ateslerse ORTUSEN TESPIT KORLUGU olur ve bir
# eksen olculmemis kalir; beklenti asagida YAZILIDIR ve tutmazsa kirmizi yanar.
def m1_listelenmemis_yuzey(s):
    """UCUNCU bir platform dali dogar, mutanti yoktur -> KAPI-1 isirmali.

    Davranisi degistirmez: yeni govdeyi KAPI-2 hic yuklemez. Bu mutant bu aracin
    KENDI kapsaminin bayatlamasini olcer."""
    i = s.find("\ndef _surec_yasiyor(")
    if i < 0:
        return None
    ek = ('\n\ndef _yeni_platform_yuzeyi(x):\n'
          '    if sys.platform == "win32":\n'
          '        return 1\n'
          '    return 0\n')
    return s[:i] + ek + s[i:]


def m2_yonlendirme_yok(s):
    """DAL A sokulur: win32 de POSIX os.kill'e duser -> KAPI-2/H-a isirmali (Y-1 geri gelir)."""
    hedef = '    if sys.platform == "win32":\n        return _surec_yasiyor_win(pid)\n'
    return s.replace(hedef, "", 1) if hedef in s else None


def m3_her_handle_yasiyor(s):
    """DAL A'nin AYRIMI bozulur: her acilabilen handle 'YASIYOR' -> KAPI-2/H-b isirmali.

    H-a'yi ATESLEMEZ (yonlendirme yerinde). Gercek win32'de KAPI-3'u de kirmizi
    yakar; bu ORTUSME degil, KAPI-3'un KOR OLMADIGININ kanitidir (asagida ayri
    raporlanir, ortusme sayimina GIRMEZ)."""
    yeni, n = re.subn(r"return _kod\.value == 259", "return True", s, count=1)
    return yeni if n else None


def m4_einval_kosulsuz(s):
    """DAL B'nin KOSULU sokulur: EINVAL her platformda yutulur -> KAPI-2/H-c isirmali.

    D-1 ekseni. m2 ile ortusmez: m2 'dal yok', m4 'dal her yerde'."""
    hedef = '    if sys.platform == "win32":\n        if kod == _errno.EINVAL:'
    yeni = '    if True:      # MUTANT: kosul sokuldu\n        if kod == _errno.EINVAL:'
    return s.replace(hedef, yeni, 1) if hedef in s else None


MUTANTLAR = [
    ("M-1 listelenmemis platform dali", m1_listelenmemis_yuzey, "KAPI-1"),
    ("M-2 win yonlendirmesi yok (Y-1)", m2_yonlendirme_yok, "KAPI-2/H-a"),
    ("M-3 her handle YASIYOR", m3_her_handle_yasiyor, "KAPI-2/H-b"),
    ("M-4 EINVAL kosulsuz yutulur (D-1)", m4_einval_kosulsuz, "KAPI-2/H-c"),
]


def hukum(s):
    return kapi1_envanter(s), kapi2_davranis(s)


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        s = io.open(yol, encoding="utf-8", newline="").read()
    except OSError as e:
        print("SONUC: ÖLÇÜLEMEDİ — motor okunamadi: %s" % e)
        return 2

    print("=== WINDOWS DALI MUTANTI === motor: %s · platform: %s"
          % (os.path.basename(yol), sys.platform))
    k1, k2 = hukum(s)
    if k2 and k2[0][0] == "H-*":
        print("  KAPI-2 DAVRANIS : %s" % k2[0][1])
        print("\nSONUC: ÖLÇÜLEMEDİ — motor govdesi kesilemedi.")
        return 2

    print("  KAPI-1 ENVANTER : %s"
          % ("YESIL (platform dali yalniz %s icinde)" % " · ".join(BILINEN_YUZEYLER)
             if not k1 else "KIRMIZI — %d listelenmemis dal" % len(k1)))
    for satir, ad, metin in k1:
        print("      ! satir %d, `%s` icinde: %s" % (satir, ad, metin))
    print("  KAPI-2 DAVRANIS : %s" % ("YESIL (H-a · H-b · H-c gecti)" if not k2 else
                                      "KIRMIZI — %d hal" % len(k2)))
    for hal, ne in k2:
        print("      ! %s: %s" % (hal, ne))

    k3 = kapi3_canli(s)
    if k3 is None:
        print("  KAPI-3 CANLI    : ÖLÇÜLEMEDİ (bu platform win32 degil) — YESIL DEGIL")
    else:
        print("  KAPI-3 CANLI    : %s" % ("YESIL (gercek ctypes: kendi pid VAR, bitmis cocuk YOK)"
                                          if not k3 else "KIRMIZI — %d hal" % len(k3)))
        for _, ne in k3:
            print("      ! %s" % ne)

    if k1 or k2 or k3:
        print("\nSONUC: KIRMIZI — temiz surum kapiyi gecemedi.")
        return 1

    print("\n--- MUTANT SINAMASI (kapinin var olmasi ISIRDIGI anlamina gelmez) ---")
    kacan = 0
    for ad, boz, beklenen in MUTANTLAR:
        bozuk = boz(s)
        if bozuk is None or bozuk == s:
            print("  %-36s KURULAMADI (mutant uygulanamadi)" % ad)
            kacan += 1
            continue
        b1, b2 = hukum(bozuk)
        ates = (["KAPI-1"] if b1 else []) + ["KAPI-2/" + h for h, _ in b2]
        if beklenen in ates and len(set(ates)) == 1:
            print("  %-36s -> ISIRDI ✓  (%s)" % (ad, beklenen))
        elif beklenen in ates:
            print("  %-36s -> ISIRDI ama ORTUSTU: %s"
                  % (ad, " + ".join(sorted(set(ates)))))
            kacan += 1
        else:
            print("  %-36s -> KACTI ✗  (beklenen %s, atesleyen: %s)"
                  % (ad, beklenen, " + ".join(sorted(set(ates))) or "hicbiri"))
            kacan += 1

    # KAPI-3 kendi mutanti: gercek win32'de M-3 KAPI-3'u de kirmizi yakmali.
    # Ortusme sayimina GIRMEZ; KAPI-3'un kor OLMADIGINI olcer (doktrin 1).
    if sys.platform == "win32":
        bozuk = m3_her_handle_yasiyor(s)
        try:
            g = govde_metni(bozuk, "_surec_yasiyor_win")
            k3m = kapi3_canli(bozuk, kaynak_govde=g)
        except LookupError as e:
            k3m = [("K3", "govde kesilemedi: %s" % e)]
        if k3m:
            print("  %-36s -> KAPI-3 de KIRMIZI ✓ (canli kapi kor degil)" % "M-3 (KAPI-3 kendi sinamasi)")
        else:
            print("  %-36s -> KAPI-3 KOR ✗ (M-3 canli kapida hic isirmadi)" % "M-3 (KAPI-3 kendi sinamasi)")
            kacan += 1
    else:
        print("  %-36s -> ÖLÇÜLEMEDİ (win32 degil)" % "M-3 (KAPI-3 kendi sinamasi)")

    if kacan:
        print("\nSONUC: KAPI KOR — %d/%d mutant beklendigi gibi olculmedi."
              % (kacan, len(MUTANTLAR)))
        return 1
    if k3 is None:
        print("\nSONUC: YESIL SINIRLI — KAPI-1/KAPI-2 temiz, %d/%d mutant AYRI eksende ISIRDI; "
              "KAPI-3 OLCULEMEDI (win32 degil)." % (len(MUTANTLAR), len(MUTANTLAR)))
    else:
        print("\nSONUC: YESIL — uc kapi da temiz, %d/%d mutant AYRI eksende ISIRDI."
              % (len(MUTANTLAR), len(MUTANTLAR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

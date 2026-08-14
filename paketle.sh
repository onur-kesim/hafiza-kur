#!/usr/bin/env bash
# =============================================================================
# skill/ -> hafiza-kur.skill
#
# Paket, `skill/` dizininin zip'idir. Motorun İKİNCİ BİR KOPYASI YOKTUR:
# `skill/scripts/hafiza.py` tek gerçek kaynaktır (H5 doktrini — "aktif sürüm
# hangisi" sorusunun iki cevabı olamaz).
#
# ÜRETİLEN PAKET ÖLÇÜLÜR (14 Ağu 2026'da düzeltildi — aşağıdaki ders):
#   KAPI-1 MOTOR BIT-BIT : zip'ten geri çıkarılan `scripts/hafiza.py`, kaynakla
#                          BİT-BİT aynı mı? (satır-sonu çevirimi, yanlış dosya,
#                          bozuk sıkıştırma buradan yakalanır)
#   KAPI-2 ENVANTER      : `skill/` altındaki filtre-dışı HER dosya pakette var mı
#                          ve pakette FAZLADAN dosya var mı? (LİSANS sınıfı)
# İkisi de kırmızıysa paket ÜRETİLMİŞ SAYILMAZ: betik exit 1 verir.
# Kapıların gerçekten ısırdığı `faz0/paket_mutanti.py` ile kanıtlanır.
#
# 🔴 DERS (bu betiğin kendi etinde, 14 Ağu 2026 — sınıf İKİNCİ kez ısırdı):
#   Eski başlık "SKILL.md'deki SHA256 beyanıyla tutmazsa DURUR" diyordu. Ama
#   `SKILL.md` sat. 245-249 tam tersini, üstelik ÖLÇÜLMÜŞ bir dersle söylüyor:
#   "Sürüm, satır sayısı ve SHA buraya YAZILMAZ — bayatlar. Bir kez yazıldı ve
#   bayatladı; kimse ölçmediği için iki sürüm boyunca görülmedi."  Kontrol
#   `[ -n "$BEYAN" ]` ile korunduğu için ölçüldü: SKILL.md'de 64'lük hex SIFIR
#   → `if` HİÇ girilmiyordu. Yani ölü olan mantık değil, BAŞLIK YALANDI.
#   Doğru çözüm beyanı geri getirmek DEĞİL (o karar ölçülmüştü) — beyanı bırakıp
#   ÜRETİLEN PAKETİ ölçmek. Beyan bayatlar; ölçüm bayatlamaz.
#   İlk ısırık: LİSANS (10 Ağu). Aynı sınıf: "SKILL.md beyanı ile paketin gerçeği
#   tutmuyor, kimse ölçmüyor."  Artık CI'da mekanik koşuyor (`capraz.yml`).
# =============================================================================
set -eu

KOK="$(cd "$(dirname "$0")" && pwd)"
cd "$KOK"

[ -d skill ] || { echo "HATA: skill/ yok"; exit 2; }
command -v zip >/dev/null || { echo "HATA: zip komutu yok"; exit 2; }
command -v python3 >/dev/null || { echo "HATA: python3 yok"; exit 2; }

GERCEK="$(python3 -c "import hashlib;print(hashlib.sha256(open('skill/scripts/hafiza.py','rb').read()).hexdigest().upper())")"
echo "hafiza.py SHA256 (kaynak): $GERCEK"

rm -f hafiza-kur.skill
( cd skill && zip -q -r -X "../hafiza-kur.skill" . -x '.*' -x '*/.*' -x '*/deneme/*' -x '*/__pycache__/*' )

# --- KAPILAR: uretilen paket olculur (beyan degil) --------------------------
set +e
python3 - "$KOK" <<'PY'
import hashlib, os, sys, zipfile

kok = sys.argv[1]
paket = os.path.join(kok, "hafiza-kur.skill")
kaynak_dizin = os.path.join(kok, "skill")

# `paketle.sh`in -x filtreleri BURADA da uygulanir; iki liste AYNI kuraldan turer.
HARIC_DIZIN = ("deneme", "__pycache__")


def beklenen():
    out = set()
    for r0, d0, f0 in os.walk(kaynak_dizin):
        d0[:] = [d for d in d0 if d not in HARIC_DIZIN and not d.startswith(".")]
        for f in f0:
            if f.startswith("."):
                continue
            rel = os.path.relpath(os.path.join(r0, f), kaynak_dizin)
            out.add(rel.replace(os.sep, "/"))
    return out


try:
    z = zipfile.ZipFile(paket)
except Exception as e:                                        # noqa: BLE001
    print("KAPI-1 MOTOR BIT-BIT : OLCULEMEDI (paket acilamadi: %s)" % e)
    print("KAPI-2 ENVANTER      : OLCULEMEDI")
    sys.exit(2)

icindekiler = {a for a in z.namelist() if not a.endswith("/")}

# KAPI-1 — motor BIT-BIT
kaynak = open(os.path.join(kaynak_dizin, "scripts", "hafiza.py"), "rb").read()
k1 = []
try:
    paketteki = z.read("scripts/hafiza.py")
except KeyError:
    k1.append("pakette scripts/hafiza.py YOK")
else:
    a = hashlib.sha256(kaynak).hexdigest().upper()
    b = hashlib.sha256(paketteki).hexdigest().upper()
    if a != b:
        k1.append("SHA TUTMUYOR kaynak=%s paket=%s (bayt %d vs %d)"
                  % (a[:16], b[:16], len(kaynak), len(paketteki)))

# KAPI-2 — envanter (eksik VE fazla)
bek = beklenen()
eksik = sorted(bek - icindekiler)
fazla = sorted(icindekiler - bek)
k2 = (["EKSIK: " + x for x in eksik] + ["FAZLA: " + x for x in fazla])

print("KAPI-1 MOTOR BIT-BIT : %s" % ("YESIL" if not k1 else "KIRMIZI"))
for x in k1:
    print("    ! %s" % x)
print("KAPI-2 ENVANTER      : %s (%d dosya)"
      % ("YESIL" if not k2 else "KIRMIZI", len(bek)))
for x in k2:
    print("    ! %s" % x)
sys.exit(1 if (k1 or k2) else 0)
PY
KAPI_RC=$?
set -e

if [ "$KAPI_RC" -ne 0 ]; then
  echo
  echo "DURDU: uretilen paket kapiyi gecemedi (kod $KAPI_RC). Paket GECERSIZ."
  echo "  -- 'belge de bir arayuzdur ve yalan soyleyebilir' (A-2'nin dersi);"
  echo "     bu yuzden BEYAN degil PAKET olculur."
  exit 1
fi

echo
echo "PAKET: $KOK/hafiza-kur.skill"
unzip -l hafiza-kur.skill | tail -n +4 | head -n -2 | awk '{print "  " $4}'

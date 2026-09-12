#!/usr/bin/env bash
# =============================================================================
# FAZ 0 — ORTAM SINIFI OLCUMU
#
# Fable 5, 4. tur denetimi §9:
#   "Kor noktan bir dusunce hatasi degil, BIR ORTAM EKSIGI -- ve bu, belge
#    okuyarak asla bulunamaz. useradd ve mount -t tmpfs toplam iki komut."
#
# Uc YUKSEK bulgunun ucu de yalniz bu kosullarda gorunuyor:
#   B4-1  ENOSPC'te kilit KALICI siziyor          -> dolu disk (tmpfs 600k)
#   B4-3  yarida kesilen derle -> kalici yanlis-kirmizi -> salt-okunur canli dosya
#   B4-4  izin hatasi "ARAC KUSURU" diye teshis   -> root OLMAYAN kullanici
#
# BU BETIK KODA DOKUNMAZ. Yalniz olcer.
# Root gerektirir (mount + useradd).  Kullanim:  sudo bash faz0/ortam_olcum.sh
#
# Cikis kodu: 0 = uc bulgunun UCU DE KAPANMIS (beklenen: v2.5.0 sonrasi)
#             1 = en az biri hala uretilebiliyor (beklenen: v2.4.1'de)
#             2 = OLCULEMEDI (root degil / mount yok / useradd yok)
# =============================================================================
set -u

MOTOR="${MOTOR:-skill/scripts/hafiza.py}"
CIZGI="------------------------------------------------------------------------------"
URETILEN=0
OLCULEMEYEN=0

bilgi() { printf '%s\n' "$*"; }
basl()  { printf '\n%s\n== %s\n%s\n' "$CIZGI" "$*" "$CIZGI"; }

if [ "$(id -u)" != "0" ]; then
  bilgi "OLCULEMEDI: bu betik root gerektirir (mount + useradd)."
  exit 2
fi
if [ ! -f "$MOTOR" ]; then
  bilgi "OLCULEMEDI: motor bulunamadi: $MOTOR  (MOTOR=... ile yol verebilirsin)"
  exit 2
fi

MOTOR_MUTLAK="$(cd "$(dirname "$MOTOR")" && pwd)/$(basename "$MOTOR")"
bilgi "motor : $MOTOR_MUTLAK"
bilgi "sha256: $(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().upper())" "$MOTOR_MUTLAK")"
bilgi "python: $(python3 -V 2>&1)"

# =============================================================================
basl "B4-1  ENOSPC'te kilit KALICI siziyor mu?"
# =============================================================================
KUCUK=/mnt/faz0_kucuk
mkdir -p "$KUCUK"
if ! mount -t tmpfs -o size=600k tmpfs "$KUCUK" 2>/dev/null; then
  bilgi "  OLCULEMEDI: tmpfs baglanamadi."
  OLCULEMEYEN=$((OLCULEMEYEN + 1))
else
  mkdir -p "$KUCUK/p" && git init -q "$KUCUK/p" 2>/dev/null
  python3 "$MOTOR_MUTLAK" kur   --kok="$KUCUK/p" >/dev/null 2>&1
  python3 "$MOTOR_MUTLAK" not   --kok="$KUCUK/p" --konu=genel-durum --metin="ilk not metni" >/dev/null 2>&1
  python3 "$MOTOR_MUTLAK" derle --kok="$KUCUK/p" >/dev/null 2>&1

  dd if=/dev/zero of="$KUCUK/dolgu" bs=1k count=10000 2>/dev/null   # diski TAM doldur
  bilgi "  disk doluyken muhur:"
  python3 "$MOTOR_MUTLAK" muhur --kok="$KUCUK/p" "disk dolu iken muhurleme denemesi" 2>&1 | head -2 | sed 's/^/    /'
  rm -f "$KUCUK/dolgu"                                             # yer ac

  KALAN="$(find "$KUCUK/p" -name .kilit 2>/dev/null | wc -l)"
  bilgi "  disk bosaldiktan sonra kalan .kilit sayisi: $KALAN"

  SONRA="$(python3 "$MOTOR_MUTLAK" not --kok="$KUCUK/p" --konu=genel-durum --metin="deneme-metni" 2>&1 | head -1)"
  bilgi "  sonraki yazma       : $SONRA"

  if [ "$KALAN" != "0" ]; then
    bilgi "  >>> B4-1 URETILDI: kilit sizdi, proje kalici yazmaya kapali."
    URETILEN=$((URETILEN + 1))
  else
    bilgi "  >>> B4-1 KAPANMIS: kalan kilit yok."
  fi
  umount "$KUCUK" 2>/dev/null
fi

# =============================================================================
basl "B4-3  Yarida kesilen derle -> KALICI yanlis-kirmizi mi?"
basl_devam=1
# =============================================================================
if ! id faz0kul >/dev/null 2>&1; then
  useradd -m -u 4242 faz0kul >/dev/null 2>&1 || true
fi
if ! id faz0kul >/dev/null 2>&1; then
  bilgi "  OLCULEMEDI: root olmayan kullanici acilamadi."
  OLCULEMEYEN=$((OLCULEMEYEN + 2))
else
  ALAN=/tmp/faz0_alan
  rm -rf "$ALAN" && mkdir -p "$ALAN" && cp "$MOTOR_MUTLAK" "$ALAN/hafiza.py" && chmod -R 777 "$ALAN"

  cat > "$ALAN/b43.sh" <<'ICBETIK'
cd /tmp/faz0_alan
rm -rf r5 && mkdir r5 && git init -q r5
python3 hafiza.py kur   --kok=r5 >/dev/null 2>&1
python3 hafiza.py not   --kok=r5 --konu=genel-durum --metin="ilk not metni" >/dev/null 2>&1
python3 hafiza.py derle --kok=r5 >/dev/null 2>&1
python3 hafiza.py not   --kok=r5 --konu=genel-durum --metin="ikinci not metni" >/dev/null 2>&1
chmod 444 r5/PROJE_HAFIZA.md                       # canliya yazilamaz
python3 hafiza.py derle --kok=r5 >/dev/null 2>&1   # yarida kesilir
chmod 644 r5/PROJE_HAFIZA.md                       # kullanici sorunu duzeltir
python3 hafiza.py derle --kok=r5 >/dev/null 2>&1   # aracin onerdigi tek makul hamle
python3 hafiza.py kapi  --kok=r5 2>&1 | grep -cE '^\s*\[H1'
echo "FRAGMAN=$(ls r5/gunluk 2>/dev/null | wc -l)"
ICBETIK
  chmod 777 "$ALAN/b43.sh"

  CIKTI="$(su faz0kul -c "bash $ALAN/b43.sh" 2>&1)"
  H1SAY="$(printf '%s' "$CIKTI" | grep -oE '^[0-9]+$' | head -1)"
  FRG="$(printf '%s' "$CIKTI" | sed -n 's/^FRAGMAN=//p')"
  bilgi "  duzeltme + yeniden derle SONRASI [H1] bulgu sayisi: ${H1SAY:-?}"
  bilgi "  kalan fragman                                     : ${FRG:-?}"
  if [ "${H1SAY:-0}" != "0" ]; then
    bilgi "  >>> B4-3 URETILDI: kirmizi KALICI, arac ici cikis yok."
    URETILEN=$((URETILEN + 1))
  else
    bilgi "  >>> B4-3 KAPANMIS: yeniden derle YESIL'e dondurdu."
  fi

  # ===========================================================================
  basl "B4-4  Izin hatasi 'ARAC KUSURU' diye mi teshis ediliyor?"
  # ===========================================================================
  cat > "$ALAN/b44.sh" <<'ICBETIK'
cd /tmp/faz0_alan

# KALEM A (besli-paket/IS_EMRI_B4E_OLCEN_TARAF.md, Onur kilidi 12 Eyl 2026
# "SIK D = A + C"): B4-4 siniflandirmasi artik TEK fonksiyonda yasar -- hem
# bu betik icinden hem DISARIDAN (faz0/ortam_sinifi_mutanti.py'nin kendi bash
# alt-surecinden, sentetik $out/$e/$c ile) cagrilabilir; boylece sinif GERCEK
# koddan dogrulanir, Python tarafinda bir TAKLIT'ten degil.
#
# CAPA CARPISMASI UYARISI (12 Eyl kilidi, sat. 1d): A2 satirindaki grep
# cagrisi ve ardindan gelen t= atamasi BIREBIR KORUNUR --
# `faz0/ortam_sinifi_mutanti.py`nin `_grep_desenini_oku` fonksiyonu ve M-D
# mutanti TAM BU SEKLE baglidir (kendi capasini burada, YORUMDA, TEKRARLAMA --
# ayni dizeyi ikinci yerde geciren bu YORUMUN KENDISI olur, tam da bu uyarinin
# soyledigi hatayi isler; olculdu). A1/A3/A4 AYRI, additive satirlardir; asagidaki
# A2 satirinin SEKLI degisirse ikisi de (KAPI-D + M-D) KIRILIR.
_b44_sinifla() {
  local out="$1" e="$2" c="$3"
  local ihlal="" t="" pozitif=0 beklenen="2"
  # A1 -- SON CARE IZI YASAK: ibareden BAGIMSIZ imza (sat. 1c). `_yaz_hata`
  # (hafiza.py'nin genel son-care dali) HER ZAMAN "Tam iz:" ya da "(iz dosyasi
  # yazilamadi)" satirlarindan birini basar -- baslik cumlesi yeniden yazilsa
  # ya da ibare kaldirilsa BILE bu iz kalir.
  if printf '%s' "$out" | grep -qE 'Tam iz:|\(iz dosyasi yazilamadi\)'; then
    ihlal="A1(son-care-izi)"
  fi
  # A2 -- IBARE YASAK (MEVCUT, KORUNUR -- satir BIREBIR; yukaridaki uyariyi oku).
  if printf '%s' "$out" | grep -q "ARAC KUSURUDUR"; then t="ARAC-KUSURU(yanlis)"; else t="ortam-teshisi(dogru)"; fi
  if [ "$t" = "ARAC-KUSURU(yanlis)" ] && [ -z "$ihlal" ]; then
    ihlal="A2(ibare)"
  fi
  # A3 -- POZITIF KANIT ZORUNLU: motor SESSIZCE basarili olursa (izin hatasi
  # hic uretilmezse) A1 ve A2 sessiz kalir; en az bir TEMIZ kalibin GORULMESI
  # zorunludur. Ucu da motorun "Bu bir ARAC KUSURU DEGIL"/"ARAC kusuru degil"
  # soylemini tasir (DOSYA/DIZIN/son-ag-EACCES kaliplarinin UCUNDE de bu
  # kapanis cumlesi var); lead-in ifadeye (DIZIN YAZILAMAZ / DOSYA SALT-OKUNUR/
  # IZIN-DOSYA SISTEMI HATASI) BAGLANMAZ -- bu, lead-in METNI degisirse A3'un
  # KIRILMAMASI icin bilincli bir genisletmedir (ayni capa-carpismasi riski).
  if printf '%s' "$out" | grep -q "ARAC KUSURU DEGIL"; then pozitif=1; fi
  if printf '%s' "$out" | grep -q "ARAC kusuru degil"; then pozitif=1; fi
  if [ "$pozitif" = "0" ] && [ -z "$ihlal" ]; then
    ihlal="A3(pozitif-kanit-yok)"
  fi
  # A4 -- CIKIS KODU: muhur=3 (kilit_al on-kontrolu kod=3 doner), digerleri=2.
  [ "$c" = "muhur" ] && beklenen="3"
  if [ "$e" != "$beklenen" ] && [ -z "$ihlal" ]; then
    ihlal="A4(cikis-kodu:beklenen=$beklenen,gercek=$e)"
  fi
  if [ -n "$ihlal" ]; then
    printf 'ARAC-KUSURU(yanlis) [%s]' "$ihlal"
  else
    printf '%s' "$t"
  fi
}

# Sentetik sinama modu: `bash b44.sh --sinifla <out> <exit> <komut>` fonksiyonu
# GERCEK senaryo kurmadan dogrudan cagirir (faz0/ortam_sinifi_mutanti.py bunu
# kullanir). Argumansiz cagri NORMAL dort-kollu olcumu kosar (degismedi).
if [ "${1:-}" = "--sinifla" ]; then
  _b44_sinifla "$2" "$3" "$4"
  exit 0
fi

for s in "muhur:arsiv/hafiza" "not:gunluk" "karar:kararlar" "kur:."; do
  c="${s%%:*}"; d="${s##*:}"
  rm -rf z && mkdir z && git init -q z
  if [ "$c" != "kur" ]; then python3 hafiza.py kur --kok=z >/dev/null 2>&1; fi
  chmod 555 "z/$d" 2>/dev/null
  case "$c" in
    muhur) out="$(python3 hafiza.py muhur --kok=z 'izin denemesi gerekcesi' 2>&1)";;
    not)   out="$(python3 hafiza.py not --kok=z --konu=genel-durum --metin='izin denemesi metni' 2>&1)";;
    karar) out="$(python3 hafiza.py karar --kok=z --baslik='izin denemesi' 2>&1)";;
    kur)   out="$(python3 hafiza.py kur --kok=z 2>&1)";;
  esac
  e=$?
  chmod 755 "z/$d" 2>/dev/null
  t="$(_b44_sinifla "$out" "$e" "$c")"
  printf '    %-6s %-14s exit=%s  %s\n' "$c" "$d" "$e" "$t"
done
ICBETIK
  chmod 777 "$ALAN/b44.sh"
  B44="$(su faz0kul -c "bash $ALAN/b44.sh" 2>&1)"
  printf '%s\n' "$B44"
  YANLIS="$(printf '%s' "$B44" | grep -c 'ARAC-KUSURU')"
  bilgi "  yanlis teshis sayisi: $YANLIS / 4"
  if [ "$YANLIS" != "0" ]; then
    bilgi "  >>> B4-4 URETILDI: izin sinifi arac kusuru sanilyor."
    URETILEN=$((URETILEN + 1))
  else
    bilgi "  >>> B4-4 KAPANMIS."
  fi
fi

# =============================================================================
basl "OZET"
# =============================================================================
bilgi "  uretilebilen bulgu : $URETILEN"
bilgi "  olculemeyen        : $OLCULEMEYEN"
if [ "$OLCULEMEYEN" != "0" ] && [ "$URETILEN" = "0" ]; then
  bilgi "  HUKUM: OLCULEMEDI — 'kapandi' DEMEK YASAK."
  exit 2
fi
if [ "$URETILEN" != "0" ]; then
  bilgi "  HUKUM: en az bir YUKSEK bulgu HALA URETILEBILIYOR."
  exit 1
fi
bilgi "  HUKUM: uc YUKSEK bulgunun ucu de kapanmis."
exit 0

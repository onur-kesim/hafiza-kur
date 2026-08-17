# ADR — H16 YAPI kapısının uygulama kısıtı (§8) DÜŞÜRÜLDÜ

**Tarih:** 17 Ağustos 2026 · **Karar:** Onur (Cowork oturumu, ölçüm sonrası kilit)
**Ölçüm ortamı:** bulut Linux, CPython 3.11, **root** · HEAD `526d6001` ·
`skill/scripts/hafiza.py` SHA256 `81798E30…` (5.567 satır)
**Kapsam:** yalnız `YAPI_KAPISI_TASARIM.md` §8'in uygulama sırası kısıtı ve onun
açtığı üç yan karar. Tasarımın §4 (onaylı tasarım) ve §6 (mutant listesi)
**DEĞİŞMEDİ.**

---

## 1. BAĞLAM — iki belge çelişiyordu

`YAPI_KAPISI_TASARIM.md` §8 (12 Ağu 2026):

> Bu tasarım **alt-bölme bittikten sonra** uygulanır. […] Kalan alt-bölme:
> `_kapi_h1` · `_kapi_h14` → sonra `cmd_devral` · `cmd_derle` · `zincir_dogrula` ·
> `cmd_bloklastir` · `_kapi_h4`.

`CLAUDE.md` §5 (14 Ağu 2026, Onur kilidi):

> **KESİLDİ 14 Ağu 2026:** `cmd_*` bölmeleri ve kalan CC borcu. […]
> Gerekçe: hiçbir BİTTİ maddesi CC'ye bağlı değil. Açmak ADR ister.

İki gün arayla yazılmış iki belge, birbirini görmeden. Sonuç: H16 **hiç
bitmeyecek** bir ön koşula bağlanmıştı. Bu, kısıtın kendisinin bir karar değil,
bir **kaza** hâline gelmesidir.

## 2. ÖLÇÜM — kısıtın her iki gerekçesi de konusuz

### 2.1 Ön koşulun kapı ayağı BİTTİ

| fonksiyon | bugünkü hâl | delege ettiği alt fonksiyonlar |
|---|---|---|
| `_kapi_h1` @3643 | **bölünmüş** (8 satır gövde) | `_h1_beyan` · `_h1_gercek` · `_h1_fark` · `_h1_kova` |
| `_kapi_h14` @4482 | **bölünmüş** (12 satır gövde) | `_h14_git_durumu` · `_h14_adaylar` · `_h14_en_yeni` · `_h14_hukum` |
| `_kapi_h4` @3766 | **bölünmüş** (10 satır gövde) | `_h4_adaylar` · `_h4_havuz` · `_h4_siniflandir` · `_h4_hukum` |

§8'in saydığı **kapı** kalemlerinin üçü de bölünmüş. Kalan dört kalem
(`cmd_devral` · `cmd_derle` · `zincir_dogrula` · `cmd_bloklastir`) `cmd_*`/zincir
sınıfındadır ve `CLAUDE.md` §5 ile **kesilmiştir**.

### 2.2 Birinci gerekçe düştü — ağ zaten cmd_* için gerilmemişti

§8'in gerekçesi: *"altın küme yalnız `kapi` komutunu kaydediyor; bit-bit
eşdeğerlik ağı yalnız `_kapi_*` fonksiyonlarını koruyor, üzerinde yürünmeden
harcanmamalı."*

Ölçüldü: `faz0/altin_kapi.json` = 22 kayıt, **komut dağılımı `kapi` ×11 +
`kapi --siki` ×11**, başka komut yok. Yani ağ `cmd_devral`/`cmd_derle`/
`zincir_dogrula`/`cmd_bloklastir` bölmelerini **hiç korumuyordu**. Kalan bölme
listesi tam da o dört kalemden ibaret olduğuna göre, ağ H16 için **saklanacak
bir yürüyüş** taşımıyor.

### 2.3 İkinci gerekçe düştü — atıf karışması için iki değişken gerekir

§8'in ikinci gerekçesi: *"bölme sürerken eklenirse, bir regresyon çıktığında
'bölme mi, kapı mı' ayrılamaz."* Bölme sürmüyor (§2.1). Tek değişken kalır.

### 2.4 Ağ BUGÜN sağlam — taban ölçüldü, beyan değil

| kabul ölçütü | tasarımın beklediği | **17 Ağu ölçümü** |
|---|---|---|
| (a) `altin_cikti.py --karsilastir` | FARK YOK (22) | **FARK YOK, 22 ölçüm, exit 0** |
| (b) `altin_cikti.py --kendini-sina` | ISIRDI, exit 0 | **ISIRDI (12 fark kaydı), exit 0** |
| (d) `fazC_bolme_mutanti.py` | 6 / 0 | **6 ısırdı · 0 kaçtı** |
| (e) `altin_kapi_mutanti.py` | 6 / 0 | **6 ısırdı · 0 kaçtı** |
| (f) `altin_olcut_mutanti.py` | 7 / 0 | **7 ısırdı · 0 kaçtı** |
| (g) `t_y3.py` | 20/20 | **20/20 TEMİZ HATA** |
| (g) `t_y42.py` | 0 kaldı | **56 geçti · 0 kaldı · 1 yavaş · 1 ölçülemedi** |

Beş gün ve dört BİTTİ maddesi (md.7–md.10) sonra sayılar **tasarımın yazdığı
yerde durmuş**. Ağ gerilmiş hâlde teslim alınıyor.

## 3. BULGU TAZE — 11 hâl yeniden koşuldu

Tasarımın §1 tablosu 12 Ağu'da 4.878 satırlık motorda ölçülmüştü. Bugünkü motor
689 satır daha uzun. **Kum havuzunda (`/tmp`, bağlı klasöre dokunulmadan)
11 hâlin tamamı yeniden koşuldu:**

| hâl | 12 Ağu | **17 Ağu** |
|---|---|---|
| `y0_temiz` — KONTROL 1 | exit 0 | **exit 0** |
| `y1_kararlar_dosya` | exit 0 | **exit 0** |
| `y2_kararlar_yok` | exit 0 | **exit 0** |
| `y3_gunluk_dosya` | exit 0 | **exit 0** |
| `y4_gunluk_yok` | exit 0 | **exit 0** |
| `y5_ars_gunluk_dosya` | exit 0 | **exit 0** |
| `y6_arsiv_dosya` — KONTROL 2 | exit 1 · `[H6]` | **exit 1 · `[H6]`** |
| `y7_kararlar_kacis` | exit 0 | **exit 0** |
| `y8_gunluk_kacis` | exit 0 | **exit 0** |
| `y9_h_kacis` | exit 3 · KESİLME | **exit 3 · KESİLME** |
| `y10_ic_link` — KONTROL 3 | exit 0 | **exit 0** |

11/11 birebir. **İki kontrol kolu da doğru davrandı** ⇒ prob kör değil, yeşiller
anlamlı. `y9`un exit 3'ü hâlâ canlı ⇒ §4.4'ün sözleşme değişikliği hâlâ gerekli.

### 3.1 Görünmezlik — ölçüm ilkin KENDİ SAYACINI kirletti

İlk koşumda `kararlar`/`gunluk` grep sayacı **1** verdi ve "hüküm gizli" iddiası
zayıflamış göründü. Ham çıktı gözle okununca sebebi çıktı: sayaç, kapının değil
**ölçüm aracının** izini sayıyordu — hâl adı (`y1_kararlar_dosya`) kum havuzu
dizin adına konmuştu ve `kok:` başlığında basılıyordu.

Dizin adları nötrleştirilip (`p00`…`p10`) kök yolu **desenle** maskelenince
(eşitlikle değil — `DURUM.md` dersi) sayaç **0**'a döndü: kırmızı olması gereken
hiçbir kolda kusurlu dizinin adı geçmiyor. Tasarımın *"hüküm yalnız yanlış değil,
GİZLİ"* iddiası **tazedir**.

> Bu, `DURUM.md`'deki "ölçüm aleti de yalan söyler" sınıfının yeni bir örneğidir:
> **ölçüm aracının kendi adlandırması, ölçtüğü metne sızabilir.** Kalıp: sayaç
> ile senaryo adı arasında ortak kelime bırakma.

### 3.2 YENİ — kusur `--kok` ile koşulduğunda TAMAMEN izsiz

Tasarımda yok, bu turda ölçüldü. `cwd` proje kökü iken sabotaj çıktıda **iki
dolaylı iz** bırakıyor: `H9: … calisma agacinda 1 degisiklik` (temizde 0) ve
`H14` satırının değişmesi. İkisi de kusuru **adlandırmıyor**, hüküm yine `YEŞİL`.

Ama `hafiza.py --kok <proje> kapi` biçiminde, proje dışından koşulduğunda git
bulunamadığı için o iki satır da sabitleniyor ve çıktı temiz projeyle **bit-bit
aynı** oluyor. Yani **git'siz projede ya da dışarıdan koşumda sabotaj sıfır iz
bırakır.** Bu, boşluğun ciddiyetini artırır ve H16'nın gerekçesini güçlendirir.

## 4. KARAR

1. **§8 uygulama sırası kısıtı DÜŞÜRÜLDÜ.** H16 YAPI kapısı uygulanabilir.
   Tasarımın §4 (onaylı tasarım), §6 (10 hâl + 9 mutant) ve §7 (kabul ölçütü)
   **aynen yürürlüktedir.**
2. **Kapsam 4 dizinde KALIR** (`y.h` · `y.gunluk` · `y.gunluk_ars` · `y.kararlar`).
   §9.2'nin açtığı soru (`arsiv/hafiza/` altındaki `v2/`, `.kilit`, politika
   yolları) **ayrı iştir** ve bu ADR ile kapatılmaz — gizlenmeden açık kalır.
3. **`--help` metni AYNI TURDA düzeltilir** (§9.8): iki yerde `H0..H13` →
   gerçek aralık. Altın kümeyi etkilemez (küme `kapi` çıktısını ölçer, `--help`i
   değil) — ama bu bir **iddiadır** ve (a) maddesiyle kanıtlanır.
4. **Kapsam envanteri AYNI TURDA yeniden üretilir** ve okuma notu düzeltilir (§5).

## 5. 🔴 ADR'NİN AÇTIĞI YENİ ÖLÇÜM — kapsam envanteri BAYAT

Kabul ölçütü (i) *"`sabotaj.py` kapsam envanteri: `fail()` 61 → 61+N"* diyor.
Bu ölçüt bugünkü tabanı olmadan koşulamaz, çünkü **taban bayat:**

- `faz0/KAPSAM_ENVANTERI_OKUMA_NOTU.md`, `kapsam_envanteri_9b72160a.json`'ı
  **"✅ GÜNCEL"** diye işaretliyor.
- Ölçüldü: o dosyadaki 61 kaydın `lineno` alanının bugünkü motorda **yalnız 4'ü**
  gerçekten bir `fail("…")` çağrısına denk geliyor. **57'si kaymış** —
  md.6→md.10 turları satırları kaydırdı.
- Bugünkü motorda `fail("…")` çağrı sayısı **yine 61**. Yani sayı aynı, **eşleme
  ölü**. Kapsam iddiası bugün ölçülemez hâlde.
- Dosyanın `motor` alanı bir **yol** yazıyor (`/tmp/hk/skill/scripts/hafiza.py`),
  SHA değil; kimlik yalnız dosya adında. Okuma notunun *"kimliksiz"* diye
  ayıpladığı kusurun bir kalıntısı güncel dosyada da duruyor.

**Sınıf üçüncü kez ısırdı.** Okuma notunun kendi dersi *"bağlam kazandırmak,
güncelliği kazandırmaz"* idi; bugünkü ek şu: **güncellik İŞARETİ de bayatlar —
"✅ GÜNCEL" bir ölçüm değil, bir tarihtir.** Kural (`CLAUDE.md` İŞLEYİŞ §8'e
göre CI'da koşmalı ya da tek cümle olmalı):

> Bir artefakta "GÜNCEL" yazan her satırın yanında, o güncelliği **o an**
> ölçen komut durur; komut yoksa işaret yazılmaz.

## 6. SONUÇLAR (bedeli dürüstçe)

- **Kazanılan:** H16 bloke değil; ağ gerilmiş, taban ölçülmüş hâlde teslim.
- **Ödenen:** `cmd_*` bölme borcu kapanmadan bir kapı ekleniyor. Bu bilinçlidir:
  `CLAUDE.md` §5 o borcu zaten kesti ve hiçbir BİTTİ maddesi ona bağlı değil.
- **Riskli kalan:** §9.2 kapsam sorusu açık; §9.3 (Windows/macOS) yalnız CI'da
  ölçülecek; bu ADR'nin bütün yerel ölçümleri **root** ile koşuldu — kabul
  ölçütü non-root ister, o hüküm CI'ya aittir.

## 7. NE ÖLÇÜLEMEDİ

1. **Kapının kendisi.** Kod yazılmadı; §7'nin hiçbir maddesi H16'lı motorda
   koşulmadı. Buradaki taban, **H16'sız** motorun tabanıdır.
2. **Non-root davranışı.** Kaçış sınıfı root ile ölçüldü; symlink/izin
   davranışı non-root'ta ayrışabilir. CI hükmüdür.
3. **Windows / macOS.** Hiçbir kol o platformlarda koşmadı (junction, reparse
   point, `os.symlink` izni, NFD).
4. **Altın kümenin kaydedildiği motor.** `altin_kapi.json` üst düzeyinde
   **hiçbir meta yok** — hangi motordan kaydedildiği kümeden okunamıyor.
   "`a1fc24bb`'den kaydedildi" cümlesi bugün **belgeye dayalıdır, artefakta
   değil.** (Ayrı, küçük bir kimlik kusuru; §5'in sınıfıyla akraba.)
5. **`kararlar/` silinmiş → `derle` exit 1** (2 değil) tutarsızlığı — tasarım
   §9.6'da açılmıştı, bu turda da bakılmadı.
6. **Boşluğun ürün etkisi.** Gerçek projelerde `kararlar/`in düz dosya veya
   dışarı linkli olma sıklığı hâlâ ölçülmedi.

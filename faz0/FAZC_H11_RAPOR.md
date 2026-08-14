# FAZ C — `_kapi_h11` ALT-BÖLMESİ (14 Ağustos 2026)

**Faz C'nin SON kapı bölmesi.** Bu turdan sonra `_kapi_*` ailesinde CC 20 tavanının
üstünde fonksiyon KALMADI.

| | önce | sonra |
|---|---|---|
| motor SHA256 | `61283ff7d755ffc7…` | `9b72160ae6e10bbe…` |
| satır | 5091 | 5132 |
| fonksiyon | 196 | 200 |
| CC > 20 | 7 | **6** |
| ihlal (birleşik) | 10 | **9** |
| `_kapi_h11` | CC 23 · 48 satır | CC 5 · 12 satır |

Kalan CC>20'nin **tamamı `cmd_*` sınıfı**: `cmd_devral` 88 · `cmd_derle` 63 ·
`zincir_dogrula` 40 · `cmd_bloklastir` 39 · `cmd_kur` 27 · `cmd_emekli` 24.

## Bölme

| parça | sorusu | CC | kanal |
|---|---|---|---|
| `_h11_numara(F, ks)` | no tekrarı · numara boşluğu | 5 | F |
| `_h11_govde(F, k, m)` | `durum: kabul` ama gövde boş | 3 | F |
| `_h11_baglanti(F, ks, harita)` | yerine-geçme çifti tutarlı mı | 10 | F |
| `_h11_canli_link(F, y, harita)` | canlı hafızanın karar linkleri | 4 | F |
| `_kapi_h11(F, N, O, y)` (ince) | yükle · çağır · say · döndür | 5 | N |

**KANAL KAPISI ölçümü** (üreteç her koşumda AST ile ölçer): dört parçanın dördü de
yalnız `F` kullanıyor, dördünün de imzası `F` taşıyor. `N` yalnız ince ebeveynde.

### 🔴 `O` kanalı hiç kullanılmıyor — bulgu, DÜZELTİLMEDİ
H11 `ÖLÇÜLEMEDİ` kanalını hiç basmıyor. Oysa "yerine-gecen SAYI DEGIL ('abc')"
bir ölçülemedi hâli sayılabilirdi: veri okunamadığı için hüküm verilemiyor, ama
`FAIL` basılıyor. Bu bölme **ADDITIVE**'dir ve davranışa dokunmaz; bulgu buraya
yazıldı, düzeltme ayrı bir karar.

### 🔴 SIRA KISITI — tasarımı bu belirledi
BAĞLANTI ve GÖVDE kontrolleri özgün kodda **aynı `for k in ks` döngüsündeydi.**
GÖVDE'yi ayrı bir döngüye almak `F` listesindeki hüküm sırasını
*(her ADR için: bağlantı, gövde)* yerine *(tüm bağlantılar, sonra tüm gövdeler)*
yapardı. Bu, altın kümenin **bit-bit** eşdeğerlik kapısını kırardı.

Kümenin bunu fark etmemesine güvenmek de bir kumar olurdu — üstelik aşağıda
ölçüldüğü gibi altın küme H11'i zaten hiç görmüyor. Bu yüzden `_h11_govde`
**BAĞLANTI döngüsünün içinden** çağrılıyor; sıra birebir korunuyor.

## Kenarlar ve mutantlar — 14 hal · 9 mutant · **9 ISIRDI · 0 KAÇTI**

On dört halin **on dördü ayrık imza** üretiyor: H11'in on bir `fail()` çağrısının
her biri kendi haline sahip, artı temiz · karar-yok · H12-dönüş hâlleri.
Örtüşen hal kullanılmadı — iki hüküm aynı halde ateşlenirse mutant ikisini de
ölçüyor sanılır, oysa birini hiç ölçmüyor olabilir.

```
  hal sayisi / ayrik imza        14 / 14
  TEMIZ KOL (ayni motor 2 kez)   FARK YOK

  +  M-H11a KANAL F numara      ISIRDI   2 olcum: bosluk,tekrar        ALTIN: KOR
  +  M-H11b KANAL F baglanti    ISIRDI   7 olcum                       ALTIN: KOR
  +  M-H11c KANAL F govde       ISIRDI   1 olcum: kabul_bos            ALTIN: KOR
  +  M-H11d KANAL F link        ISIRDI   2 olcum                       ALTIN: KOR
  +  M-H11e KENAR harita->bag   ISIRDI   3 olcum                       ALTIN: KOR
  +  M-H11f KENAR harita->lnk   ISIRDI   1 olcum                       ALTIN: KOR
  +  M-H11g KENAR ks->numara    ISIRDI   2 olcum                       ALTIN: KOR
  +  M-H11h KENAR ks->baglanti  ISIRDI   7 olcum                       ALTIN: KOR
  +  M-H11i DONUS ks            ISIRDI   1 olcum: h12_sapmasi          ALTIN: KOR
```

`harita` kenarının **iki tüketicisi** var (`_h11_baglanti`, `_h11_canli_link`) ve
ikisi **ayrı ayrı** koparıldı (`M-H11e`, `M-H11f`). Tek mutant kullanılsaydı
biri hiç ölçülmemiş olabilirdi — projenin kendi dersi: *örtüşen tespit körlüğü
maskeler.*

`M-H11i` dönüş kenarını ölçer: `return ks` → `return []`. `h_h12_sapmasi` hâlinde
bir KARAR, canlı bloktan daha yeni **tek** kayıttır (`acilis-protokolu` bloğunun
arkasında fragman yoktur), dolayısıyla dönüş boşalınca H12'nin CANLI BAYAT hükmü
sessizce kaybolur. `return None` yerine `return []` seçildi: `None` çökerdi,
`[]` sessizdir — sessiz olan daha zor mutanttır.

## 🔴 ALTIN KÜME DOKUZ MUTANTIN DOKUZUNA DA KÖR (9/9)

Şimdiye kadarki en kötü oran. Karşılaştırma: H14 5/7 · H12 5/7 · H4 6/6 · H10 6/6.

**Bağımsız ikinci ölçüm aynı şeyi söylüyor:** kapsam envanterine göre H11'in on bir
`fail()` çağrısından **10'u KAPSAMSIZ** (1 KAPSAMLI). İki farklı araç, aynı sonuç:
H11 bu depoda başka hiçbir ölçümün dokunmadığı bir bölge.

Sonuç: `h11_kenar_mutanti` işi H11 için **tek ölçümdür**, örtüşen yedeği yoktur.
CI işinde `continue-on-error` kesinlikle yok.

## EŞDEĞERLİK VE REGRESYON — hepsi kendi koşumumla

| ölçüm | sonuç |
|---|---|
| altın küme (22 ölçüm, bit-bit) | **FARK YOK** |
| hüküm haritası | 61 → 61, sıra→kapı eşlemesi AYNI |
| sabotaj diferansiyeli | 61/61 `(kapı, hüküm)` dizisi **AYNI** · 21 KAPSAMLI / 40 KAPSAMSIZ değişmedi |
| `t_y3` | 20/20 TEMİZ HATA |
| `t_y42` (root olmayan `olcum`) | 58 geçti · 0 kaldı · **0 yavaş** (55,9 sn) |
| `isir` (taze proje) | 34/34 ISIRIYOR · 2 SINANMADI (derle koşulmamış) |
| `h12_bolme_mutanti` (regresyon) | 7/7 ISIRDI, 0 KAÇTI |
| `ci_kapsam_kapisi` | h11 işi eklenmeden **KIRMIZI**, eklendikten sonra 7/7 YEŞİL |

Süreler (bulut Linux, 4 işçi): h11 kenar mutantı **49 sn** · sabotaj tam koşum
**2 dk 34 sn** · t_y42 **56 sn**.

## CI kapsam kapısı ilk gerçek vakasında ateşledi

Yazıldıktan bir tur sonra: `faz0/h11_bolme_mutanti.py` diske indi, `capraz.yml`'e
iş henüz eklenmemişti. Kapı:

```
HUKUM: KIRMIZI — 1 bolme mutantinin CI isi YOK: h11_bolme_mutanti.py
```

İş eklendikten sonra 7/7 yeşil. Kapı bir tatbikatta değil, **gerçek bir vakada**
ısırdı.

## AÇIK KALAN

- H11'in `O` kanalını hiç kullanmaması (yukarıda) — düzeltme kararı verilmedi.
- `M-H11a`/`M-H11g` ve `M-H11b`/`M-H11h` çiftleri aynı halleri tetikliyor: her
  kenar ölçülüyor ama hangi kenarın koptuğunu haller ayırt edemiyor. Ölçüm
  eksikliği değil, çözünürlük sınırı — kayda geçti.
- Sıradaki sınıf `cmd_*`: gözlem yüzeyi ŞIK D (etki imzası + sözleşme hal kapısı),
  `cmd_kur` ile başlanacak, **önce harness sonra bölme**.

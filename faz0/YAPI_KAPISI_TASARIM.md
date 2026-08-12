# H16 YAPI KAPISI — ÖLÇÜM + ONAYLI TASARIM

**Tarih:** 12 Ağustos 2026 · **Ortam:** bulut Linux, Python 3.11, `hafiza.py`
SHA `480cbd52…640` (4878 satır) üzerinde, cihazdaki çalışma ağacına DOKUNULMADAN.
**Durum:** tasarım ONAYLI, **kod YAZILMADI.** Uygulama sırası §8'de kısıtlı.

> Bu belge bir düzeltmenin **gerekçe defteridir**, uygulama raporu değildir.
> Uygulandığında §7'nin altına gerçek çıktı satırları eklenecek.

---

## 1. BULGU — `kapi` bozuk proje yapısına YEŞİL diyor

Taze projeler kuruldu (`hafiza.py kur`), tek bir yapı bozması yapıldı, `kapi` ve
karşılaştırma için `derle` koşuldu. Kontrol kolları dâhil.

### 1.1 DİZİN SINIFI — "dizin olması gereken yol dizin değil / yok"

| sabotaj | `kapi` | `derle` |
|---|---|---|
| `kararlar/` düz dosya | **exit 0 · YEŞİL (SINIRLI)** | exit 2 · `DIZIN OLMASI GEREKEN YOL DIZIN DEGIL` |
| `kararlar/` silinmiş | **exit 0** | exit 1 |
| `gunluk/` düz dosya | **exit 0** | exit 2 · `DIZIN OLMASI GEREKEN YOL DIZIN DEGIL` |
| `gunluk/` silinmiş | **exit 0** | exit 2 · `FRAGMAN DIZINI YOK` |
| `arsiv/hafiza/gunluk/` düz dosya | **exit 0** | exit 2 · `DIZIN OLMASI GEREKEN YOL DIZIN DEGIL` |
| `arsiv/` düz dosya — **KONTROL** | exit 1 · FAIL `[H6]` ✓ | exit 2 · `HAFIZA DIZINI YOK` |

### 1.2 KAÇIŞ SINIFI — "dizin proje ağacının DIŞINA bağlı"

| sabotaj | `kapi` |
|---|---|
| `kararlar/` → proje **dışına** sembolik link | **exit 0 · YEŞİL (SINIRLI)** |
| `gunluk/` → proje **dışına** sembolik link | **exit 0 · YEŞİL (SINIRLI)** |
| `arsiv/hafiza` → proje **dışına** sembolik link | **exit 3 · HÜKÜM YOK** — `[KAPI] OLCUM YARIDA KESILDI: DIZIN PROJE DISINA BAGLI` |
| `kararlar/` → proje **içine** link — **KONTROL** | exit 0 ✓ doğru; kaçış yok, kusur yok |

İki kontrol kolu da beklendiği gibi davrandı → prob kör değil, yeşiller anlamlı.

**Görünmezlik ayrıca ölçüldü:** kırmızı olması gereken kolların **hiçbirinde**
`kapi`'nin stdout+stderr çıktısında `kararlar` ya da `gunluk` kelimesi geçmiyor
(grep sayımı **0**). Yani hüküm yalnız yanlış değil, **gizli**. Bu, doktrinin
3. maddesinin (*"hedef engellemek değil, GİZLENEMEZ KILMAK"*) tam tersidir.

### 1.3 🔴 §3'teki kusur SINIFI ZATEN CANLI — tahmin değil, ölçüm

`arsiv/hafiza` kaçış hâli (§1.2, 3. satır) gösteriyor ki, `kapi`'nin **baktığı tek
dizinde bile** kusur "ölçülmüş kırmızı" değil, **"hüküm yok"** üretiyor. §3'te
*"naif düzeltme bunu doğurur"* diye yazdığım sınıf, `y.h` için bugün **yürürlükte**.
Bu, düzeltmenin `fail()` yolunu seçmesinin gerekçesini teoriden çıkarıp ölçüme bağlar.

### 1.4 Önceki DEVİR'e göre YENİ olan hâller

Önceki DEVİR üç hâl sayıyordu (`kararlar/` düz dosya · `kararlar/` silinmiş ·
`gunluk/` düz dosya). Bu turda **beş hâl daha** ölçüldü:
`gunluk/` silinmiş · `arsiv/hafiza/gunluk/` düz dosya · üç kaçış hâli.
`arsiv/hafiza/gunluk/` hâli arşiv ağacının **İÇİNDEDİR** — dolayısıyla
*"arsiv/ dolaylı olarak korunuyor"* savunması da eksiktir.

---

## 2. KÖK SEBEP — tek satır, kaynakta görünüyor

```python
# _kapi_govde @2951   (yani `kapi` komutunun ta kendisi)
yol_on_kontrol(y, dizinler=(y.h,), dosyalar=_korunacak_dosyalar(y, rc), sessiz=True)

# zincir_on_kontrol @1007 · cmd_kur @1589 · cmd_devral @2701
yol_on_kontrol(y, dizinler=(y.h, y.gunluk, y.gunluk_ars, y.kararlar), ...)
```

`kapi` dört dizinin **birine** bakıyor. Boşluğun tamamı eksik üç dizindir:
`y.gunluk` · `y.gunluk_ars` · `y.kararlar`. Hem dizin sınıfı hem kaçış sınıfı
o üç dizin için **hiç sorulmuyor**.

`arsiv/` hâlinin yakalanması **dolaylıdır**: `arsiv/` düz dosya olunca
`arsiv/hafiza` yolu kaybolur, `_kapi_govde`'nin `if not os.path.isdir(y.h)`
erken çıkışı `[H6] HAFIZA DIZINI YOK` yazar. Sınıfı sorgulayan bir kapı yoktur;
çocuğunu arayan bir kontrol vardır.

**Motor sınıfı BİLİYOR** — `derle` aynı bozmada temiz hata veriyor. Bilgi
üründe var, **ÖLÇÜM KAPISINDA yok.** Bu, CLAUDE.md §3'teki *"korumayı ürüne
koydun; ÖLÇÜM ARACINA koydun mu?"* dersinin yeni bir örneğidir — bu kez ters
yönde: koruma üründe, kapıda değil.

---

## 3. 🔴 NAİF DÜZELTME ÖLÇÜLDÜ VE YANLIŞ

*"`kapi`'nin `dizinler=` tuple'ını dörde çıkar"* çözümü **çalışmaz**:

`yol_on_kontrol` bozuk/kaçan dizinde `oldur(msg, kod=2)` çağırır → `SystemExit(2)`.
`cmd_kapi` bunu yakalar (kendi kesilme sözleşmesi gereği) →
`[KAPI] OLCUM YARIDA KESILDI` → başka bulgu olmadığı için **exit 3 / HÜKÜM YOK**.
Üstelik bu kontrol kapılardan **ÖNCE** koştuğu için **16 kapının hiçbiri koşmaz.**

Yani sessiz yeşil, "hüküm yok"a dönüşür. Kapsam boşluğu **kapanmaz, yer değiştirir**
ve yanına 16 kapılık bir ölçüm kaybı ekler. §1.3 bunun **bugün gerçekleştiğini**
gösteriyor.

**Sonuç:** düzeltme `fail()` ile RAPORLAMALI, `oldur()` ile DURDURMAMALI.
Bu, mutant M-Y4 ile kilitlenir (§6).

---

## 4. ONAYLI TASARIM — H16 YAPI, temizde SESSİZ

Onaylanan şıklar (12 Ağu 2026, Onur):

1. **Yeni bağımsız kapı: `_kapi_h16(F, N, O, y)` — ad: `H16 YAPI`.**
2. **Temiz projede HİÇBİR SATIR BASMAZ.** Yalnız kırılınca `fail()` yazar.
3. **Silinmiş dizin = düz dosya = FAIL.** İkisi de exit 1. Ayrı metin, aynı hüküm.
   *(Bu madde iki kez soruldu ve iki kez FAIL olarak kilitlendi.)*
4. **Kaçış (proje dışına link) de FAIL** — dört dizinin dördü için.
5. **`y.h` kaçışı exit 3 → exit 1'e çevrilir.** Gerekçe ve maliyet §4.4'te.

### 4.1 Kapsam — dört dizin, üç hâl

| dizin | dizin değil | hiç yok | proje dışına kaçış |
|---|---|---|---|
| `y.h` (`arsiv/hafiza`) | H16 FAIL | **H6'da KALIR** (§4.3) | **H16 FAIL** — bugün exit 3 (§4.4) |
| `y.gunluk` (`gunluk/`) | H16 FAIL | H16 FAIL | H16 FAIL |
| `y.gunluk_ars` (`arsiv/hafiza/gunluk/`) | H16 FAIL | H16 FAIL | H16 FAIL |
| `y.kararlar` (`kararlar/`) | H16 FAIL | H16 FAIL | H16 FAIL |

Kaçış ölçütü `kok_disina_mi(y.kok, yol)`'dur — `yol_on_kontrol`'ün kendi
`_kacis` yardımcısıyla **aynı fonksiyon**. İkinci bir kaçış tanımı yazılmaz
(B-2/B-3'ün "TEK TANIM" kuralı).

### 4.2 "Temizde sessiz" neden meşru — ölçülmüş emsal

Temiz projede `kapi` şu kapılardan **hiç satır basmıyor** (ölçüldü):
**H1 · H3 · H4 · H6 · H7.** Desen dosyada zaten var, icat edilmiyor.

Bedeli dürüstçe yazılır: kullanıcı temiz çıktıda H16'nın koştuğunu **göremez**.
Karşılığı §5'te ölçülen ağ tasarrufudur. Bu bir **ödünç**tür, bedava değildir:
alt-bölme bittikten ve altın küme yeniden kaydedildikten sonra H16'nın temizde
konuşur hâle getirilmesi **ayrıca değerlendirilmelidir** (açık iş).

### 4.3 🔴 ADDITIVE KALMA KISITI — H6 erken çıkışı SÖKÜLMEZ

`_kapi_govde`'deki `if not os.path.isdir(y.h): fail("H6", "HAFIZA DIZINI YOK…"); return`
**yerinde kalır.** H16 onu devralmaz, çoğaltmaz, öne geçmez.

Gerekçe: `arsiv/` düz dosya hâli bugün `[H6]` ile exit 1 veriyor ve bu
**altın kümenin kayıtlı davranışıdır**. H16 bu yolu değiştirirse küme kırılır —
yani tam olarak kaçınmak istediğimiz maliyet doğar. H16 o erken çıkıştan
**sonra** koşar.

Sonuç: `y.h`'nin YOK hâli H6'da, DİZİN DEĞİL ve KAÇIŞ hâlleri H16'da ölçülür.
Bu bir **örtüşme değil, sınır**; ve M-Y7 ile sınanır.

### 4.4 🔴 SÖZLEŞME DEĞİŞİKLİĞİ — `y.h` kaçışı: exit 3 → exit 1

Bugün `arsiv/hafiza` proje dışına linkliyken `kapi` **exit 3 (HÜKÜM YOK)** veriyor
(§1.2). Onaylanan tasarım bunu **exit 1 (ölçülmüş kırmızı)** yapar.

**Neden meşru:**
- "Hüküm yok" burada **yanlış** bir hükümdür: ölçüm yapılamamış değil, kusur
  **bulunmuştur** — kapı sadece onu bir bulgu olarak yazmıyor, bir kesilme
  olarak yazıyor.
- Dört dizin aynı kurala tabi olur; sınıf **SINIRDA** kapanır, tek tek yüzeyler
  sarılarak değil (CLAUDE.md §3).

**Maliyeti ölçüldü:** altın kümenin üç exit-3 hâli —
`h7_kesilme` (PROJE_HAFIZA.md UTF-8 değil) · `h8_kesilme_dizin` (PROJE_HAFIZA.md
**düzenli dosya değil** — *dosya* sınıfı) · `h9_kesilme_erken` (_CIPA.json UTF-8
değil) — **hiçbiri dizin kaçışı değildir.** Bu değişiklik kümedeki hiçbir kaydı
etkilemez. `h8_kesilme_dizin` adı yanıltıcıdır; içeriği okundu, dosya sınıfıdır.

**Karşılığında zorunlu:** kümeye **yeni bir hâl** eklenir (`y_h_kacis`, exit 1) ve
ayrı mutant yazılır (M-Y9). Sözleşme değişikliği ölçüsüz bırakılmaz.

---

## 5. ALTIN KÜME ETKİSİ — ölçüldü

`faz0/altin_kapi.json` yapısı (12 Ağu 2026 itibarıyla):

```
11 hâl × 2 komut = 22 ölçüm · komutlar YALNIZ: `kapi` ve `kapi --siki`
exit dağılımı: 0 (×10) · 1 (×6) · 3 (×6)
```

### 5.1 🔴 ÖNCEKİ DEVİR'İN MALİYET TAHMİNİ YANLIŞ — düzeltiliyor

Önceki DEVİR: *"FAIL hâlinde YALNIZ bulguyu basıyor."* **Yanlış.**

`cmd_kapi` kaynağında notlar (`N`) ve ölçülemedi (`O`) **her durumda** basılır;
`if F:` bloğu ondan SONRA gelir. `altin_kapi.json`'daki `h6_fail` kaydı bunu
doğruluyor: 12 not satırı + 3 bulgu, 977 karakter.

**Doğru maliyet:** temizde bir `·` satırı basan yeni bir kapı, **10 değil,
22 referansın TAMAMINI** geçersiz kılar.

Onaylanan şık (temizde sessiz) bu maliyeti **sıfırlar** — ve bu, uygulamada
kanıtlanması gereken bir iddiadır, dilek değil: kabul ölçütünün (a) maddesi
budur.

---

## 6. AYRI MUTANT — `faz0/yapi_kapisi_mutanti.py` (yazılacak)

*"Her düzeltmeye AYRI mutant. Mutantsız düzeltme kör kalır."*

Mutant kendi proje hâllerini kurar, referansı koşum anında temiz motordan alır,
kusurları tek tek enjekte eder. **Hepsi ISIRMALI; kaçan varsa kapı kördür.**

### 6.1 Proje hâlleri (10)

| hâl | beklenen |
|---|---|
| `y0_temiz` — **KONTROL 1** | exit 0 · çıktı bölme öncesiyle **bit-bit aynı** |
| `y1_kararlar_dosya` | exit 1 · `[H16]` **ve** `kararlar` |
| `y2_kararlar_yok` | exit 1 · `[H16]` **ve** `kararlar` |
| `y3_gunluk_dosya` | exit 1 · `[H16]` **ve** `gunluk` |
| `y4_gunluk_yok` | exit 1 · `[H16]` **ve** `gunluk` |
| `y5_ars_gunluk_dosya` | exit 1 · `[H16]` |
| `y6_arsiv_dosya` — **KONTROL 2** | exit 1 · bulgu **`[H6]`** kalmalı, `[H16]` DEĞİL (§4.3) |
| `y7_kararlar_kacis` | exit 1 · `[H16]` **ve** gerçek hedef yolu çıktıda |
| `y8_gunluk_kacis` | exit 1 · `[H16]` |
| `y9_h_kacis` | exit 1 · `[H16]` — **bugün exit 3** (§4.4); kümeye eklenecek hâl |
| `y10_ic_link` — **KONTROL 3** | exit 0 · proje İÇİNE link kusur DEĞİL |

### 6.2 Motor mutantları (9)

| mutant | ne bozar | ısırmazsa ne öğreniriz |
|---|---|---|
| **M-Y1 KAPI DÜŞÜRME** | `_kapi_h16` çağrısını dağıtımdan sil | kapı hiç ölçülmüyor |
| **M-Y2 KAPSAM DARALTMA** | H16'nın dizin listesini `(y.h,)`'ye indir | bugünkü boşluğun ta kendisi geri gelir ve görünmez |
| **M-Y3 SİLİNMİŞ→NOT** | "yok" dalını `fail` yerine `not` yap | exit 1→0; onaylanan hüküm sessizce gevşer |
| **M-Y4 `oldur` DÖNÜŞÜ** | `fail()` yerine `oldur()` çağır | §3'teki naif düzeltme sınıfı geri sızar (exit 1→3) |
| **M-Y5 TEMİZDE KONUŞ** | H16'ya temizde bir `not` ekle | altın küme FARK vermeli; vermezse §5'in kilidi yok |
| **M-Y6 gunluk_ars DÜŞÜR** | yalnız `y.gunluk_ars`'ı listeden çıkar | §1.4'teki yeni hâl tek başına ölçülmüyor demektir |
| **M-Y7 SINIR KAYMASI** | H16'yı H6 erken çıkışının ÖNÜNE al | `y6_arsiv_dosya` kolu `[H6]`→`[H16]`'ya döner → küme kırılır |
| **M-Y8 KAÇIŞ DÜŞÜRME** | `kok_disina_mi` çağrısını H16'dan çıkar | kaçış sınıfı hiç ölçülmüyor (y7/y8/y9 üçü birden kaçar) |
| **M-Y9 KAÇIŞTA `oldur`** | yalnız `y.h` kaçışını eski `oldur` yoluna geri koy | §4.4'ün sözleşme değişikliği geri alınır, kimse görmez |

**M-Y5 · M-Y7 · M-Y9 birer ÖLÇÜT mutantıdır** — kapının değil, *kapının maliyet
ve sözleşme iddialarının* ısırıp ısırmadığını ölçerler. Üçü de zorunludur; onlar
olmadan "altın kümeye dokunmadı" ve "sözleşme bilinçli değişti" cümleleri birer
dilektir.

**Örtüşen tespit körlüğü uyarısı:** M-Y2 ile M-Y6, M-Y8 ile M-Y9 aynı hâli
yakalayabilir. Mutant, her mutant için **hangi hâllerin** fark verdiğini tek tek
yazmalı; "ısırdı" yetmez, **kaç ölçümde** ısırdığı yazılmalı (FAZC kalıbı).

---

## 7. KABUL ÖLÇÜTÜ — hepsi geçmeden iş bitmiş sayılmaz

Non-root kullanıcıyla, bu sırayla:

```
a) faz0/altin_cikti.py --karsilastir faz0/altin_kapi.json   -> FARK YOK (22 ölçüm)  🔴 en kritik
b) faz0/altin_cikti.py --kendini-sina                       -> ISIRDI, exit 0
c) faz0/yapi_kapisi_mutanti.py                              -> 9 ısırdı / 0 kaçtı
d) faz0/fazC_bolme_mutanti.py                               -> 6 ısırdı / 0 kaçtı
e) faz0/altin_kapi_mutanti.py                               -> 6 ısırdı / 0 kaçtı
f) faz0/altin_olcut_mutanti.py                              -> 7 ısırdı / 0 kaçtı
g) t_y3.py 20/20 · isir 34/34 ve 36/36 · t_y42.py 0 kaldı
h) faz0/hukum_kapisi.py hukum.log                           -> exit 0
i) sabotaj.py kapsam envanteri: fail() 61 -> 61+N (N = H16'nın fail sayısı)
   ve DİĞER 61'in kapı/hüküm eşlemesi DEĞİŞMEMİŞ
j) altın kümeye `y9_h_kacis` hâli EKLENMİŞ ve exit 1 kaydedilmiş (§4.4)
```

(a) tek başına en kritik maddedir: **temizde sessizlik iddiasının kanıtı odur.**
(i) additive kalmanın, (j) sözleşme değişikliğinin kanıtıdır.

---

## 8. 🔴 UYGULAMA SIRASI — KISITLI

Bu tasarım **alt-bölme bittikten sonra** uygulanır. Sıra keyfi değil, ölçülmüş:

Altın küme **yalnız `kapi` komutunu** kaydediyor; yani bit-bit eşdeğerlik ağı
**yalnız `_kapi_*` fonksiyonlarını** koruyor. Ağ, bölme öncesi motordan
(`a1fc24bb`) kaydedilmiştir ve **üzerinde yürünmeden harcanmamalıdır.**

H16 temizde sessiz olduğu için ağı *teorik olarak* harcamaz — ama bu iddia
(a) maddesiyle **kanıtlanana kadar** iddiadır. Bölme sürerken eklenirse, bir
regresyon çıktığında "bölme mi, kapı mı" ayrılamaz. Önce alt-bölme, sonra kapı.

Kalan alt-bölme: `_kapi_h1` · `_kapi_h14` → sonra
`cmd_devral` · `cmd_derle` · `zincir_dogrula` · `cmd_bloklastir` · `_kapi_h4`.
Sıralama ölçütü için bkz. `ADR_CC_OLCUTU.md` (kabul edildi: kendi gövde CC'si).

---

## 9. NE ÖLÇÜLEMEDİ

Bu bölüm boş olamaz.

1. **Düzeltmenin kendisi.** Kod yazılmadı, hiçbir kabul ölçütü koşulmadı.
   Buradaki her "beklenen" bir **tahmindir**, ölçüm değil.
2. **Sınıfın kapsamı.** `arsiv/hafiza/` altındaki diğer yollar (`v2/`, `.kilit`,
   politika dosyaları) aynı sınıfa açık mı — **bakılmadı.** Yalnız `gunluk`
   denendi. Derinlik ile kapsam ayrı iki sorudur; burada yalnız derinlik ölçüldü.
3. **Windows / macOS.** Hiçbir kol o platformlarda koşmadı. "Düz dosya ≠ dizin"
   ve "kaçış linki" ayrımları orada aynı davranmayabilir (junction, reparse
   point, `os.symlink` izni, NFD).
4. **Dosya hâlleri.** Yalnız DİZİN sınıfı ölçüldü. `_korunacak_dosyalar`
   yolundaki dosya bozmaları bu turda denenmedi (`h7/h8/h9` kümede zaten var).
5. **Hardlink kolu.** `yol_on_kontrol`'ün `cok_adli` yolu (proje dışında ikinci
   ad) H16 kapsamına alınmadı ve ölçülmedi; bugün `H-LINK` bulgusu olarak
   ayrıca işleniyor.
6. **`kararlar/` silinmiş → `derle` exit 1** (2 değil, stderr'da tek satır yok) —
   nedeni araştırılmadı. Ayrı bir küçük tutarsızlık olabilir.
7. **CC sayıları** projenin kendi aracıyla değil, ayrı bir AST sayacıyla ölçüldü
   (bkz. `ADR_CC_OLCUTU.md`). Sıralama güvenilir, mutlak sayı değil.
8. **`hafiza.py --help`** "kapi H0..H13 kapilarini kosar" diyor; gerçekte
   H0–H15 var. H16 eklenince bu metin **üç kez** yanlış olur. Ölçüldü,
   kapatılmadı — düzeltme H16 ile aynı turda yapılmalı.
9. **Boşluğun ÜRÜN etkisi.** Gerçek projelerde `kararlar/`in düz dosya ya da
   dışarı linkli olması ne sıklıkla oluyor — hiç ölçülmedi. Sınıf gerçek,
   frekansı bilinmiyor.

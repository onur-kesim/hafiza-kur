# FAZ C — `_kapi_govde` BÖLMESİ · ÖLÇÜM RAPORU

**Tarih:** 11 Ağustos 2026 · **Ortam:** bulut Linux, Python 3.11.15, root olmayan
kullanıcı (`olcum`), 2 CPU. Windows/macOS bu raporda **ÖLÇÜLMEDİ** (CI'ya kalır).

| | SHA256 | satır | `fail()` |
|---|---|---|---|
| bölme ÖNCESİ | `a1fc24bb…62d` | 4764 | 61 |
| bölme SONRASI | `480cbd52…640` | 4878 | 61 |

Bölme öncesi ağaç: HEAD `41b23ac`.

---

## 1. NE YAPILDI

`_kapi_govde` (745 satır, CC 284) kapı başına **16 ayrı fonksiyona** bölündü:
`_kapi_h0 … _kapi_h15`, dosyada **çalışma sırasıyla** (…H13, **H15, H14** — H15
H14'ten önce koşar, bu çıktı sözleşmesidir). `_kapi_govde` geriye yalnız ortak
bağlamı, iki erken çıkış kapısını ve 16 çağrılık düz bir diziyi bırakır.

Gövdeler **elle yeniden yazılmadı**: `faz0/fazC_bolucu.py` satırları birebir
taşır. Üreteç girdisinin SHA'sını kapıda sınar ve `fail()` sıra→kapı eşlemesinin
değişmediğini yazmadan önce doğrular.

**Yeniden üretilebilirlik (ölçüldü):** üreteç bölme öncesi motora yeniden
uygulandığında teslim edilen dosyanın **birebir aynısını** üretir
(`sha256 = 480cbd52…640`). Araya elle tek bir düzeltme sızmamıştır.

### 1.1 Bölümler arası veri: üç kenar, imzada görünür

Ölçülen gerçek bağımlılık (yukarı-açık kullanım analizi) yalnız üç kenar:

| taşınan | üretici → tüketici | neden yeniden hesaplanmadı |
|---|---|---|
| `bl` | H10 → H12 | `canli_bloklar()` ikinci kez tam tarama; B-6 (300k satırda kapı < 8 sn) zaten sınırda |
| `ks` | H11 → H12 | `adr_listesi()` ikinci kez tam tarama |
| `t_son` | H12 → H14 | — |

Geri kalan her şey `kok · rc · y · siki`.

### 1.2 🔴 ONAYLI TASARIMDAN SAPMA — ölçümle zorunlu kılındı

Onaylanan tasarım *"her kapı `(bulgular, notlar, olculemedi)` **döndürür**"*
diyordu. O biçim üretildi, ölçüldü ve **GERİ ALINDI.**

**Kusur:** bir kapı yarıda `SystemExit` atarsa (H0 önce `CIPA BOZULDU` yazar,
sonra *aynı kapıda* `_ZINCIR.jsonl` geçersiz UTF-8 çıkıp `oldur()` çalışır),
kapının o ana kadar topladığı bulgu **yerel listede kalır ve kaybolur**.

Kod enjeksiyonu **yok** — gerçek bir bozuk dosya girdisiyle üretildi:

```
bölme öncesi   : SONUC: FAIL (2 bulgu) · [H0] CIPA BOZULDU var · exit 1
saf-dönüş hâli : SONUC: FAIL (1 bulgu) · [H0] KAYIP            · exit 3
```

**Ölçülmüş bir KIRMIZI, "hüküm yok"a dönüşüyordu.** `cmd_kapi` kendi
docstring'inde bunun tersini garanti eder: *"ne olursa olsun O ANA KADAR
TOPLANAN hüküm basılır"* ve *"gerçek bir kapı bulgusu VARSA 1 döner"*.
`kapi || dur` diyen bir sarmalayıcı, ölçülmüş bir tahrifatı "hüküm yok"
sanacaktı.

Saflık bir **tercih**, o garanti bir **korumadır** — ve korumalar kanıtsız
sökülmez. Kapılar artık `F/N/O`'yu **parametre olarak alır** ve doğrudan yazar;
bölme öncesiyle aynı liste nesnesi, aynı anda dolar. Bu, kapıları "saf" olmaktan
çıkarır; gerekçesi kodun içinde, `_kapi_govde`'deki KAPILAR bloğunda yazılıdır.

**Bu kusuru bulan üretici değil, bağımsız denetçi ajandır.** Üreticinin ilk
teslimi üç eşdeğerlik ayağını da geçiyordu — üçü de bu sınıfı ölçmüyordu.

---

## 2. EŞDEĞERLİK — ÜÇ AYAK

| ayak | ölçüt | sonuç |
|---|---|---|
| (a) | `altin_cikti.py --karsilastir faz0/altin_kapi.json` | **FARK YOK** (10 ölçüm, bit-bit) |
| (b) | `grep -c "fail(" skill/scripts/hafiza.py` | **61** (değişmedi) · AST sayımı da **61** |
| (c) | `sabotaj.py` kapsam envanteri | **61/61 aynı** — satır no hariç `kapi · hukum · kacan · exit · kacanlar` alanlarının tamamı; 21 KAPSAMLI / 40 KAPSAMSIZ |

Ayrıca `altin_cikti.py --kendini-sina` → **ISIRDI** (araç kör değil).

### 2.1 (b) ayağı hakkında — ölçüt kırılgan

`grep -c "fail("` bir **metin aramasıdır**. İlk üretimde sayı 61 yerine **63**
çıktı; fark, üretecin yazdığı **iki yorum satırıydı**. Ölçüt kendi prozamla
kaydı. Asıl değişmez olan `sabotaj.py`'nin AST sayımıdır; grep onun kaba
vekilidir. Üreteç artık yorum metninde bu dizgeden kaçınır.

---

## 3. BÖLMEYE ÖZGÜ MUTANT — `faz0/fazC_bolme_mutanti.py`

Eşdeğerlik kapısının **bölmeye özgü** kusurları gördüğü kanıtlanmadan bölme
teslim edilemez ("ölçülmeyen kapının hükmü yoktur"). Bu dosya kendi proje
hâllerini kurar, referansı koşum anında temiz motordan alır ve altı kusuru tek
tek enjekte eder.

**Hâller (5) × komut (2) = 10 ölçüm.** İkisi bilerek eklendi:

- `h_bl` / `h_ks` — H12'nin **CANLI BAYAT** dalını ateşler.
- `h_kesilme` — kapı-içi kesilme (§1.2). Ayrıca **mutlak ölçüt**: çıktıda
  `[H0] CIPA BOZULDU` VAR ve `exit == 1`. Diferansiyele bağlı değildir.
- `h_arsiv` — arşivde dizinde olmayan dosya; H6'yı ateşler.

```
TEMIZ KOL (aynı motor 2 kez)   FARK YOK
KESILME SOZLESMESI (temiz)     TUTUYOR
  + M-C1 SIRA              ISIRDI   8 ölçümde fark
  + M-C2 KENAR t_son       ISIRDI   8 ölçümde fark
  + M-C3 KENAR bl          ISIRDI   4 ölçümde fark
  + M-C4 KENAR ks          ISIRDI   2 ölçümde fark
  + M-C5 BULGU KAYBI       ISIRDI  10 ölçümde fark · sözleşme BOZULDU
  + M-C6 KAPI DUSURME      ISIRDI   2 ölçümde fark
SONUC: 6 ısırdı - 0 kaçtı - 0 ölçülemedi
```

**Diferansiyel mod** (`--karsilastir-motor <bölme öncesi>`): 10 ölçüm,
**FARK YOK**, kesilme sözleşmesi TUTUYOR.

### 3.1 Bu mutantın kendi tarihi — iki kez KAÇTI, iki kez hâl eklendi

- İlk hâlinde M-C3/M-C4 **altın kümeye** soruyordu ve **KAÇTI**: altın kümenin
  beş hâli H12'nin CANLI BAYAT dalına hiç uğramıyor. `h_bl`/`h_ks` eklendi.
- Sonra M-C6 **KAÇTI**: H6 sağlıklı projede hiçbir şey basmaz (3 `fail()`,
  0 not), dolayısıyla dağıtımdan silinmesi görünmüyordu. `h_arsiv` eklendi.

Her ikisi de "örtüşen tespit körlüğü maskeler" dersinin aynısıdır.

---

## 4. REGRESYON — TAM KAPI KOŞUMU

Bölme öncesi (taban) ve sonrası aynı komutlarla koşuldu.

| koşum | taban | bölme sonrası |
|---|---|---|
| `t_y3` | 20/20 TEMİZ HATA · exit 0 | aynı |
| `t_y42` | 58 senaryo · exit 0 | aynı |
| `isir` (taze + `derle` sonrası) | 36/36 ısırıyor · exit 0 | aynı |
| `hukum_kapisi` | exit 0 | aynı |
| `y2_mutant` · `y4_mutant` | 2/0/0 · exit 0 | aynı |
| `fazA_senaryolari` | 6/0/0 · exit 0 | aynı |
| `fazB_senaryolari` | 6/0/0/0 · exit 0 | aynı |
| `fazB_olcut_mutanti` | 2/0/0 · exit 0 | aynı |
| `boru_probu` | exit 0 (tuzak yok) | aynı |
| `sabotaj.py` | 21 KAPSAMLI / 40 KAPSAMSIZ | **aynı** |

`t_y42`'nin B-6 senaryosu (300k satırda `kapi < 8 sn`) bu makinede koşuma göre
GEÇTİ/YAVAŞ arasında oynuyor — **kalibrasyonsuz mutlak duvar saati**, bilinen
test kusuru (Faz F). Bölmeye atfedilemez; iki yönde de ölçüldü.

---

## 5. KARMAŞIKLIK — bağlamıyla

`_kapi_govde`: **CC 284 → 5** · 745 satır → 48 satır.

Ama **toplam karmaşıklık düşmedi, taşındı** (bağımsız denetçinin ölçümü):
blok sayısı 114 → 131, toplam CC 1133 → 1151 (+18, yeni fonksiyon başlıkları).
Kazanç *dağılımdadır*: en kötü tek fonksiyon 284 → 88.

**Hedef (CLAUDE.md §5: >80 satır yok, CC>20 yok) BU TURDA TUTMUYOR.** Bölünen
16 kapının **6'sı** hâlâ eşiğin üstünde:

| | `_kapi_h1` | `_kapi_h14` | `_kapi_h4` | `_kapi_h10` | `_kapi_h12` | `_kapi_h11` |
|---|---|---|---|---|---|---|
| CC | **57** | **35** | **32** | **27** | **25** | **23** |
| satır | **128** | **106** | 63 | **82** | 47 | 49 |

Dosyanın en kötü fonksiyonu artık `_kapi_govde` değil: **`cmd_devral` (CC 88)**
ve **`cmd_isir` (700 satır, CC 17 — uzun ama düz)**. Bu, bu turda **bilinçli
olarak kapsam dışıydı** (onaylanan şık: "yalnız düz bölme").

---

## 6. NE ÖLÇÜLEMEDİ

Bu bölüm boş olamaz.

1. **Windows / macOS.** Hiçbir ölçüm o platformlarda koşulmadı; CRLF yolu
   (`fazC_bolucu.py` içinde var) hiç çalışmadı. CI'ya kalır.
2. **40 KAPSAMSIZ `fail()`'in bölme sonrası çıktısı.** Bu 61 hükmün 40'ını
   hiçbir mutant ateşlemiyor ve hiçbir ölçüm hâli oraya uğramıyor. Metinleri
   veya sıraları değişse **hiçbir kapı görmez**. Bu bölmeden ÖNCE de böyleydi
   (envanter değişmedi), ama "eşdeğerlik kanıtlandı" cümlesi o 40 hükmü
   **kapsamaz**.
3. **Altın küme yalnız yeşil yolu ölçüyor** (10/10 ölçüm exit 0). FAIL, kesilme
   ve exit 1/2/3 dalları `altin_kapi.json`'ın dışındadır. Bu tur referansa
   dokunulmadı (bilinçli); genişletme Faz C indikten SONRA yapılmalı.
4. **`isir`'da H9 için mutant yok** (`M-H9 → SINANMADI`). "36/36" ifadesi
   H9'un hiç ölçülmediğini gizler. Bölme öncesi de böyleydi.
5. **Kapı-içi kesilme sınıfının kapsamı.** H0 için kanıtlandı ve kapatıldı;
   aynı sınıfa açık diğer kapılar (H1, H5, H10, H11, H12, H13 — ilk `fail()`
   sonrası ölümcül çağrı içerenler) tek tek üretilmedi. Sınıf kapandı, **kapsamı
   ölçülmedi**.
6. **Normalleştirme fazla geniş:** `\b[0-9A-Fa-f]{16,}\b` deseni 16+ haneli
   **ondalık sayıları** da `<SHA>` yapar. Yalnız böyle bir sayıda görünen bir
   davranış farkı hem `altin_cikti` hem `fazC_bolme_mutanti` için görünmezdir.
7. **300k satır ölçeğinde bölme maliyeti.** Küçük fikstürde medyan fark
   %-1,0 (gürültü içinde); B-6 ölçeğinde kontrollü tekrarlı karşılaştırma
   yapılmadı.
8. **`SystemExit` dışı istisnalarda davranış** fiilen koşularak
   karşılaştırılmadı.

---

## 7. SIRADAKİ İŞ (öneri, karar Onur'da)

1. `faz0/fazC_bolme_mutanti.py` için CI işi (`capraz.yml`). 🔴 `capraz.yml`
   değişirse **İş Portföyü'ne bildirim yükümlülüğü** vardır.
2. Altın kümeye FAIL ve kesilme hâllerini ekleyip `altin_kapi.json`'ı **Faz C
   indikten sonra** yeniden kaydetmek (bugünkü referans bölme öncesidir ve
   dokunulmadı).
3. `_kapi_h1` (CC 57) ve `_kapi_h14` (CC 35) alt-bölmesi; ardından `cmd_devral`
   (CC 88), `cmd_derle` (63), `zincir_dogrula` (41).
4. `_RE_SHA` desenini daraltmak (§6.6) ve daralttıktan sonra `--kendini-sina`'yı
   yeniden koşmak.

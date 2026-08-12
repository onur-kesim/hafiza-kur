# FAZ C ALT-BÖLME — `_kapi_h1` · ÖLÇÜM RAPORU

**Tarih:** 12 Ağustos 2026 · **Ortam:** bulut Linux, Python 3.11.15, root olmayan
kullanıcı (`olcum`), 2 CPU. Windows/macOS bu raporda **ÖLÇÜLMEDİ** (CI'ya kalır).

| | SHA256 | satır | `fail()` | fonksiyon |
|---|---|---|---|---|
| bölme ÖNCESİ | `480cbd52…640` | 4878 | 61 | 176 |
| bölme SONRASI | `b954e0cb…ec5` | 4930 | 61 | 181 |

Bölme öncesi ağaç: HEAD `7d8e8bb`. Girdi motorunun SHA'sı, üretecin kendi
kapısında doğrulandı (`BEKLENEN_SHA`).

---

## 1. NE YAPILDI

`_kapi_h1` (126 satır, CC 54, 9 hüküm) **beş parçaya** bölündü. Parçalar
kapının kendi yerinde ve **koşum sırasında** durur; ince `_kapi_h1` en sona konur.

| yeni fonksiyon | kaynak | satır | CC | hüküm | imza |
|---|---|---|---|---|---|
| `_h1_beyan` | 3067–3086 | 23 | 12 | 3 | `(F, y)` → `snapL, bekle, duz` |
| `_h1_gercek` | 3088–3104 | 20 | 4 | 1 | `(F, O, kok, rc, y)` → `canliA, var` |
| `_h1_fark` | 3105–3133 | 30 | 13 | 2 | `(F, N, y, siki, bekle, var)` |
| `_h1_kova_bek` | 3145–3166 | 24 | 14 | **0** | `(kv, snapL, duz)` → `bek` — **SAF** |
| `_h1_kova` | 3134–3144 + 3167–3188 | 36 | 14 | 3 | `(F, y, snapL, duz, canliA)` |
| `_kapi_h1` (ince) | — | 8 | 2 | 0 | imza **değişmedi** |

**Hedef tuttu:** altısı da CC ≤ 20 ve ≤ 80 satır.

Gövdeler **elle yeniden yazılmadı**: `faz0/fazC_bolucu_h1.py` satırları birebir
taşır. Tek dönüşüm, girintinin **tekdüze azaltılmasıdır** (gövdenin tamamı tek bir
`if os.path.isfile(y.snap):` içinde yaşıyordu) — ve bu satır başına doğrulanır:
her boş olmayan satırın en az o kadar boşlukla başladığı iddia edilir, yoksa
üreteç **durur**. Sessiz bozma yolu yoktur.

### 1.1 Bölümler arası veri: dört kenar, imzada görünür

Yukarı-açık kullanım analiziyle ölçülen gerçek bağımlılık yalnız dört kenar:

| taşınan | üretici → tüketici |
|---|---|
| `bekle` | BEYAN → FARK |
| `snapL`, `duz` | BEYAN → KOVA |
| `var` | GERÇEK → FARK |
| `canliA` | GERÇEK → KOVA |

`snap0` ölçüldü ve **BEYAN'ın içinde kalıyor** — dışarı çıkmıyor, imzaya girmedi.

### 1.2 Koruma korundu: F/N/O hâlâ PARAMETRE

FAZC §1.2'de ölçülmüş koruma **sökülmedi**: parçalar `F/N/O`'yu parametre olarak
alır ve doğrudan yazar. Saf dönüş biçimi, bir parça yarıda `SystemExit` atarsa o
ana kadar toplanan hükmü kaybediyordu.

**Tek istisna `_h1_kova_bek`.** Orada `fail()` çağrısı **0 adettir** (ölçüldü),
dolayısıyla kaybedilecek bulgu da yoktur. Saflık orada bir tercih değil, **ölçümle
güvenli kılınmış** bir sadeleştirmedir. Bu ayrım kodun içine de yazıldı.

### 1.3 Sıra neden böyle — sabotaj.py kısıtı

`faz0/sabotaj.py` her hüküm çağrısını `(lineno, col)` sırasına göre numaralandırır
ve 61 maddelik kapsam envanteri o numaralara bağlıdır. Parçalar başka bir sırayla
yazılırsa numaralandırma kayar ve envanter **karşılaştırılamaz** hale gelir — yani
ölçüm kaybolur. Bu yüzden parçalar A→B→C→(saf)→D sırasıyla, kapının kendi yerinde
durur; ince `_kapi_h1` hiç hüküm içermediği için en sona konabildi.

### 1.4 Koruma satırı tersine çevrildi — mekanik ve güvenli

`if os.path.isfile(y.snap):` → ince `_kapi_h1` içinde `if not …: return`.
Bu dönüşüm güvenlidir çünkü **özgün fonksiyonda o `if` bloğundan sonra hiçbir
şey yoktu** (fonksiyon 3188'de, bloğun içinde bitiyordu). Ölçüldü, varsayılmadı.

---

## 2. KABUL ÖLÇÜTÜ — dokuzunun tamamı GEÇTİ

Non-root kullanıcıyla, bu sırayla koşuldu.

| # | ölçüt | sonuç |
|---|---|---|
| **a** | `altin_cikti.py --karsilastir` | **FARK YOK — 22 ölçüm, bit-bit** · exit 0 |
| **b** | `altin_cikti.py --kendini-sina` | **ISIRDI** (12 fark kaydı, H13 satırını 12'si yakaladı) · exit 0 |
| **c** | `fazC_bolme_mutanti.py` | **6 ısırdı / 0 kaçtı / 0 ölçülemedi** · exit 0 |
| **d** | `altin_kapi_mutanti.py` | **6 / 0 / 0** · exit 0 |
| **e** | `altin_olcut_mutanti.py` | **7 / 0 / 0** · exit 0 |
| **f** | `win_yol_probu.py` | KONTROL GEÇTİ · TEMİZ GEÇTİ · **SABOTAJ ISIRDI** (4 ölçüm) · exit 0 |
| **g** | `t_y3.py` | **20/20 senaryo TEMİZ HATA** · exit 0 |
| | `isir` (derle ÖNCESİ) | **34/34 ısırıyor** · 2 SINANMADI · exit 2 *(beklenen: ölçülemeyen mutant)* |
| | `isir` (derle SONRASI) | **36/36 ısırıyor** · 0 SINANMADI · exit 0 |
| | `t_y42.py` | **57 geçti · 0 kaldı · 1 yavaş · 0 ölçülemedi** (58) · exit 0 |
| **h** | `hukum_kapisi.py hukum.log` | beklenen **her hüküm BASILDI** · exit 0 |
| **i** | `sabotaj.py` kapsam envanteri | **61/61** · `faz0/sabotaj_rapor.json` ile **alan farkı 0** · 21 KAPSAMLI / 40 KAPSAMSIZ |

(a) maddesi bu bölmenin **tek gerçek eşdeğerlik kanıtıdır**: altın kümenin
referansı bölme öncesi motordan alınmıştır ve 22 ölçümün tamamı bit-bit tuttu.

### 2.1 Hüküm haritası — iki bağımsız ölçüm

Üreteç kendi kapısında `61 → 61, sıra→kapı eşlemesi AYNI` dedi. Bu **üreticinin
kendi beyanıdır**; ayrı bir sayaçla bağımsız olarak yeniden ölçüldü:

```
BAGIMSIZ AST KARSILASTIRMASI (ureteci degil, ayri sayac)
  eski: 61 · yeni: 61 · esleme AYNI mi: True
```

### 2.2 🔴 `faz0/kapsam_envanteri.json` BAYAT — ölçüldü

(i) maddesi iki referansa karşı koşuldu:

- `faz0/sabotaj_rapor.json` → **61 madde, alan farkı 0.** Geçerli taban budur.
- `faz0/kapsam_envanteri.json` → **60 madde.** Motor 61 hüküm içeriyor; bu dosya
  bir hüküm eksik. Karşılaştırma 30. maddeden sonra bir kayıyor ve **89 sahte
  fark** üretiyor. Bu bir gerileme değil, **bayat referans** kusurudur.

Bu dosyayı taban sanan bir sonraki koşum "89 alan değişti" diye kırmızı yanar ve
bölmeyi suçlar. Kapatılmadı, **bildiriliyor**: ya yeniden üretilmeli ya da
adı/kullanımı netleştirilmeli. Her iki referansın da motor yolu bugün geçersiz
(`/home/claude/dogrulama/…` ve emekli `C:\dev\hafiza-kur\…`).

---

## 3. KARMAŞIKLIK — bağlamıyla

`_kapi_h1`: **CC 54 → 2** · 126 satır → 8 satır.

Eşik ihlali tablosu (ölçüt: **kendi gövde CC'si** — `ADR_CC_OLCUTU.md`, kabul
12 Ağu 2026):

| | önce | sonra |
|---|---|---|
| CC > 20 | 12 fonksiyon | **11** |
| satır > 80 | 12 fonksiyon | **11** |
| toplam fonksiyon | 176 | 181 |

Kalan CC ihlalleri: `cmd_devral` 81 · `cmd_derle` 61 · `zincir_dogrula` 38 ·
`cmd_bloklastir` 37 · `_kapi_h14` 34 · `_kapi_h4` 28 · `_kapi_h10` 26 ·
`cmd_kur` 25 · `cmd_emekli` 24 · `_kapi_h12` 24 · `_kapi_h11` 22.

**Toplam karmaşıklık düşmedi, taşındı** — FAZ C'de olduğu gibi. Kazanç dağılımda.

### 3.1 Ne AÇTI — ruff, önce ve sonra

*"Bir düzeltmenin ne kapattığı değil, NE AÇTIĞI ölçülür."*

```
ESKI: 117 uyari   (E702 79 · E741 19 · E731 17 · F841 2)
YENI: 121 uyari   (E702 79 · E731 20 · E741 20 · F841 2)
```

**+4, ikisi de bölmenin doğrudan sonucu ve tamamı açıklanabilir:**

- **E731 +3** — dört yeni parça kendi `fail` lambda'sını tanımlıyor, eski
  `_kapi_h1`'inki kalktı. Net +3. Lambda adı **değiştirilemez**: `sabotaj.py`
  çağrıları AST'te `Name.id == "fail"` diye arar.
- **E741 +1** — `_h1_gercek`'in `O` parametresi. Mevcut 16 kapının hepsinde
  zaten var; bu 17.'si.

**Yeni bir uyarı SINIFI doğmadı** — dört kod önce de sonra da aynı.

---

## 4. NE ÖLÇÜLEMEDİ

Bu bölüm boş olamaz.

1. **Windows / macOS.** Hiçbir ölçüm o platformlarda koşulmadı. CI'ya kalır.
   `win_yol_probu` yalnız **desen** ölçer, platformu değil.
2. **`_h1_kova_bek`'in saflığı sınanmadı.** "Hüküm içermiyor, o yüzden saf
   olabilir" ölçüldü; ama o fonksiyonun **ileride** bir hüküm kazanması hâlinde
   koruma kaybı doğar — bunu yakalayan bir mutant **YOK**. Sınıf açık.
3. **Bu bölmeye özgü mutant YAZILMADI.** FAZ C'de `fazC_bolme_mutanti.py` vardı;
   bu tur için `_h1_*` kenarlarını (dört kenar) tek tek koparan bir mutant
   üretilmedi. Mevcut mutantlar bölmeyi **dolaylı** olarak ölçüyor: (a) bit-bit
   eşdeğerlik + (c/d/e) kapı/ölçüt mutantları. **Doğrudan kenar mutantı eksiktir**
   ve bu, FAZ C'nin kendi standardının altındadır.
4. **40 KAPSAMSIZ `fail()`.** Envanter değişmedi (21/40), ama "eşdeğerlik
   kanıtlandı" cümlesi o 40 hükmü **kapsamaz** — metinleri veya sıraları değişse
   hiçbir kapı görmez. Bölmeden önce de böyleydi.
5. **`t_y42` B-6 "1 yavaş".** Kalibrasyonsuz mutlak duvar saati; bilinen test
   kusuru (Faz F). Bölmeye atfedilemez, ama bu koşumda da tek yönde ölçüldü.
6. **`isir` H9 için mutant yok** (`M-H9 → SINANMADI`). "36/36" bunu gizler.
7. **Performans.** 300k satır ölçeğinde bölmenin maliyeti ölçülmedi; dört ek
   fonksiyon çağrısının B-6 sınırına etkisi bilinmiyor.
8. **`faz0/kapsam_envanteri.json`'ın neden 60 madde olduğu** araştırılmadı
   (§2.2). Bayat olduğu kesin, nedeni değil.

---

## 5. SIRADAKİ İŞ (öneri, karar Onur'da)

1. **Bu bölmeye özgü kenar mutantı** — §4.3'teki eksik. Dört kenarı tek tek
   koparan (`bekle`, `snapL/duz`, `var`, `canliA`) + koruma satırını sökme +
   `_h1_kova_bek`'in saflığını bozan bir mutant.
2. `_kapi_h14` (CC 34, 104 satır) alt-bölmesi — aynı üreteç kalıbıyla.
3. `faz0/kapsam_envanteri.json`'ın durumu (§2.2).
4. `faz0/karmasiklik.py` + CLAUDE.md §5 güncellemesi (`ADR_CC_OLCUTU.md` §7).
5. H16 YAPI kapısı — alt-bölme bittikten SONRA (`YAPI_KAPISI_TASARIM.md` §8).

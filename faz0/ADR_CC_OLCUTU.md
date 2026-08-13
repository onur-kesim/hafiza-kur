# ADR — "CC > 20 yok" kuralının ÖLÇÜM YOLU

**Durum:** 🟢 **KABUL EDİLDİ — Şık A (kendi gövde CC'si)** · Onur, 12 Ağustos 2026
**Tarih:** 12 Ağustos 2026
**Uygulama:** 🟢 **UYGULANDI** — 13 Ağustos 2026 · `faz0/karmasiklik.py` + `faz0/karmasiklik_mutanti.py` (9/9 ısırdı) + CLAUDE.md §5 güncellendi
**İlgili karar:** CLAUDE.md §5, *Mimari* satırı — *"Tek dosya KALIR. Bölünecek
olan fonksiyonlardır (hedef: hiçbir fonksiyon >80 satır, hiçbiri CC >20)."*

---

## 1. SORUN — kuralın ölçüm yolu YOK

CLAUDE.md §5 bir eşik koyuyor ama **hangi CC** olduğunu söylemiyor. Bu bir
üslup kusuru değil; kuralı **ölçülemez** kılıyor. İki savunulabilir metrik aynı
fonksiyona 8,6 kat farklı sayı veriyor:

```
cmd_isir  ·  700 satır  ·  43 adet İÇ İÇE fonksiyon tanımı içeriyor
    CC, iç fonksiyonlara İNEREK      = 146
    CC, iç fonksiyonlar SAYILMADAN   =  17
```

İkisi de doğru sayımlardır; farklı **soru** sorarlar:

- **İNEREK:** "bu `def` bloğunun tamamında kaç karar noktası var?"
- **İNMEDEN:** "bu fonksiyonun KENDİ gövdesinde kaç karar noktası var?"
  (iç fonksiyonlar ayrı fonksiyon sayılır — radon/McCabe'in yerleşik davranışı)

## 2. BUNUN YOL AÇTIĞI SOMUT ZARAR — ölçüldü

Aynı fonksiyon, projenin kendi belgelerinde **iki karşıt hükümle** geçiyor:

| kaynak | ifade |
|---|---|
| `faz0/FAZC_RAPOR.md` §5 | *"`cmd_isir` (700 satır, **CC 17** — uzun ama **düz**)"* |
| 12 Ağu 2026 DEVİR notu §2.3 | *"`cmd_isir` **CC=152**, 700 satır — dosyanın **EN karmaşığı**"* |

Aynı bayt dizisi. Bir belgede "düz", diğerinde "en karmaşık". Bir sonraki oturum
bu iki cümleden hangisini okuduğuna göre **farklı iş sırası** kurar — ve ikisi de
kendini ölçüme dayandırdığını sanır.

Bu, projenin kendi **H12 (BAYATLIK)** ve *"belge de bir arayüzdür ve yalan
söyleyebilir"* derslerinin bir örneğidir: yalan söyleyen belge değil, **ölçütü
tanımlanmamış kural**.

## 3. KURALIN BUGÜNKÜ KAPSAMI — iki metrikle

`hafiza.py` SHA `480cbd52…640` · 4878 satır · **176 fonksiyon** (12 Ağu 2026)

| ölçüt | ihlal eden | liste |
|---|---|---|
| **CC>20, İNEREK** | **14** | cmd_isir 146 · cmd_devral 81 · cmd_derle 61 · _kapi_h1 54 · zincir_dogrula 38 · cmd_bloklastir 37 · _kapi_h14 37 · _kapi_h4 28 · _kapi_h10 26 · cmd_kur 25 · cmd_emekli 24 · _kapi_h12 24 · yol_on_kontrol 22 · _kapi_h11 22 |
| **CC>20, İNMEDEN** | **12** | cmd_devral 81 · cmd_derle 61 · _kapi_h1 54 · zincir_dogrula 38 · cmd_bloklastir 37 · _kapi_h14 34 · _kapi_h4 28 · _kapi_h10 26 · cmd_kur 25 · cmd_emekli 24 · _kapi_h12 24 · _kapi_h11 22 |
| **satır>80** | **12** | cmd_isir 700 · cmd_devral 277 · cmd_derle 209 · zincir_dogrula 136 · _kapi_h1 126 · cmd_bloklastir 115 · _kapi_h14 104 · cmd_kur 91 · yol_on_kontrol 90 · cmd_emekli 87 · _guvenli_calistir 84 · _kapi_h10 81 |

İki metrik yalnız **iki fonksiyonda** ayrışıyor: `cmd_isir` (146/17) ve
`yol_on_kontrol` (22/13). Geri kalan 174 fonksiyonda fark yok. Yani ölçüt
tartışması **dar** — ama tam da en çok konuşulan fonksiyonu vuruyor.

### 3.1 Bölme listesinin de yazılı ölçütü yok

12 Ağu DEVİR'inin alt-bölme listesi — `cmd_devral · cmd_derle · zincir_dogrula ·
cmd_bloklastir · _kapi_h4` — **"CC>20 olanların hepsi" değil**, bir alt kümesi.
Hangi metrikle bakılırsa bakılsın dışarıda kalanlar var: `_kapi_h10` 26 ·
`cmd_kur` 25 · `cmd_emekli` 24 · `_kapi_h12` 24 · `_kapi_h11` 22
(+ İNEREK metriğinde `yol_on_kontrol` 22, `cmd_isir` 146).

Liste yanlış değil; **gerekçesi yazılı değil.** Bu ADR o gerekçeyi de zorunlu
kılmayı öneriyor.

---

## 4. ŞIKLAR

### Şık A — İNMEDEN (öneri) 🟢

CC, fonksiyonun kendi gövdesinden ölçülür; iç içe tanımlanan her `def` **ayrı
bir fonksiyon** sayılır ve kendi eşiğine tabi olur.

- **Lehine:** radon / standart McCabe'in yerleşik davranışı — dışarıdan
  denetlenebilir, üçüncü taraf araçla çapraz ölçülebilir. Mimari kararın kendi
  cümlesiyle tutarlı: *"bölünecek olan **fonksiyonlardır**"* — iç içe bir `def`
  **zaten** bölünmüş bir fonksiyondur.
- **Aleyhine:** 700 satırlık `cmd_isir` CC kuralını **geçer** (17 ≤ 20) ve yalnız
  satır kuralına takılır. "Geçti" hükmü, dosyanın en uzun fonksiyonu için
  sezgiye ters gelir.
- **Sonuç:** ihlal listesi 12'ye iner; `cmd_isir` ve `yol_on_kontrol` CC'den düşer.

### Şık B — İNEREK

CC, `def` bloğunun tamamından ölçülür.

- **Lehine:** "bu dosyayı açan insan kaç dala bakmak zorunda" sorusuna daha yakın.
  `cmd_isir`'ı listede tutar.
- **Aleyhine:** yerleşik araçlarla uyuşmaz (radon bu sayıyı vermez) → ölçüm
  **projeye özgü** bir sayaca bağlanır, yani ölçüt aracın kendi kusuruna açılır.
  Ayrıca iç fonksiyonlara bölerek karmaşıklığı azaltmayı **ödüllendirmez** —
  hedefin tersine çalışır.

### Şık C — İKİSİ BİRDEN, ayrı eşiklerle

`CC_kendi ≤ 20` **ve** `CC_toplam ≤ 60` gibi iki eşik.

- **Lehine:** her iki soruyu da ölçer; `cmd_isir` toplam eşiğine takılır.
- **Aleyhine:** ikinci eşiğin değeri (60?) **keyfî** olur ve gerekçesi yoktur.
  Gerekçesiz eşik, ölçütü bir dileğe çevirir. Ayrıca iki sayı iki ayrı tartışma
  demektir.

---

## 5. ÖNERİ

**Şık A (İNMEDEN)** + üç zorunluluk:

1. **Ölçüm aracı ADIYLA yazılır.** Kuralın yanına araç, sürüm ve komut konur —
   ör. `faz0/` altına küçük bir `karmasiklik.py` (stdlib `ast`, sıfır bağımlılık,
   projenin kendi doktrinine uygun) ya da geliştirme aracı olarak `radon cc -s`.
   *Ölçüm aracı kurulu olan kural prozayla tekrar edilmez; aracın adı yazılır.*
2. **Satır kuralı ayrı ve bağımsız kalır.** `cmd_isir` CC'den düşse de
   `700 > 80` ile listede **kalır**. İki ölçüt birbirinin yerine geçmez.
3. **Bölme listesinin ölçütü de yazılır.** Liste ya "ihlal edenlerin tamamı"dır
   ya da bir sıralama kuralıdır (ör. *"altın kümenin koruduğu `_kapi_*` önce,
   sonra CC azalan sırayla"*). Şu an ikisi de yazılı değil.

**Karşı-argüman, dürüstçe:** Şık A, 700 satırlık bir fonksiyona "CC temiz" dedirtir.
Bu rahatsız edicidir ve rahatsızlık haklıdır — ama çözümü CC metriğini bükmek
değil, **satır kuralının yerinde durması** ve `cmd_isir`'ın oradan
yakalanmasıdır. Ölçütü sezgiye uydurmak, ölçütü kaybetmektir.

---

## 6. KARAR (12 Ağustos 2026, Onur)

**Şık A kabul edildi:** CC, fonksiyonun **kendi gövdesinden** ölçülür; iç içe
tanımlanan her `def` ayrı bir fonksiyon sayılır ve kendi eşiğine tabidir.

Doğrudan sonuçları:

- `cmd_isir` CC kuralına **uyuyor** (17 ≤ 20). Bölme listesine CC'den girmez;
  **satır kuralından girer** (700 > 80) ve orada kalır.
- İhlal listesi: **CC>20 → 12 fonksiyon** · **satır>80 → 12 fonksiyon**.
- 🔴 **BU BÖLÜMDEKİ SAYILAR 13 Ağu 2026'da DÜZELTİLDİ** — bkz. §7.1. Karar
  doğruydu, sayılar yanlıştı. Aracın verdiği güncel sıra (13 Ağu 2026,
  `_kapi_h1` bölündüğü için listede yok):
  `cmd_devral` 88 → `cmd_derle` 63 → `zincir_dogrula` 40 → `cmd_bloklastir` 39 →
  `_kapi_h14` 35 → `_kapi_h4` 32 → `_kapi_h10` 27 → `cmd_kur` 27 →
  `_kapi_h12` 25 → `cmd_emekli` 24 → `_kapi_h11` 23.  (CC>20: **11**)
- Bundan sonra herhangi bir belgeye yazılan CC sayısı **bu ölçütle** ölçülmüş
  sayılır; başka bir ölçütle ölçülmüşse **metrik adı yanına yazılır**.

## 7. UYGULANDI (13 Ağustos 2026) — blokaj kalktı

Kararın CLAUDE.md'ye işlenmesi **bilerek ertelendi.** Gerekçe kuralın kendisidir:

> *Ölçüm aracı kurulu olan kural, talimatı prozayla tekrar etmez — aracın adını
> yazar.*

Blokajın gerekçesi buydu ve **sırasıyla açıldı** (13 Ağu 2026):

1. `faz0/karmasiklik.py` yazılır — stdlib `ast`, sıfır bağımlılık, tek komut,
   çıktısı deterministik: `ad · CC · satır · başlangıç`, CC azalan sıralı.
2. Araç kendi **mutantıyla** sınanır: bilerek iç fonksiyonlu bir örnek verilir;
   sayaç iç gövdeyi sayarsa **ISIRMALI** (yoksa ölçüt aracı yanlış ölçüttedir).
3. **Ancak o zaman** CLAUDE.md §5'in *Mimari* satırı şu hâle getirilir:

   > | Mimari | **Tek dosya KALIR.** Bölünecek olan **fonksiyonlardır**
   > (hedef: hiçbir fonksiyon >80 satır, hiçbiri CC >20). **Ölçüm:**
   > `python3 faz0/karmasiklik.py skill/scripts/hafiza.py` — CC, fonksiyonun
   > **kendi gövdesinden** sayılır; iç içe `def`'ler ayrı fonksiyondur
   > (ADR: `faz0/ADR_CC_OLCUTU.md`, 12 Ağu 2026). |

Bu ADR o değişikliğin **gerekçe kaydıdır**; değişiklik yapıldığında buraya
"UYGULANDI + tarih + commit" satırı eklenir.

## 8. NE ÖLÇÜLEMEDİ

1. Bu ADR'deki CC sayıları **bu belgeyi yazan sayaçla** ölçüldü; `radon` ile
   çapraz doğrulanmadı. İki metriğin **varlığı** kesindir, mutlak sayılar birkaç
   birim oynayabilir (sayaç `with` ve `assert`'ü karar sayıyor — radon `with`
   saymaz).
2. `sabotaj.py`'nin AST sayımı bir CC ölçmez (`fail()` sayar); yani projenin
   **hâlihazırda** bir CC aracı olup olmadığı bu turda araştırılmadı.
3. Eşiğin kendisi (20 / 80) hiç sorgulanmadı — bu ADR **ölçüm yolunu** tartışır,
   eşiği değil.
4. Ölçütün değişmesinin geçmiş belgeleri (FAZC_RAPOR, eski DEVİR'ler) nasıl
   etkileyeceği — hangi cümlelerin geriye dönük düzeltme gerektirdiği — listelenmedi.


## 7.1 🔴 UYGULARKEN ÇIKAN KUSUR — ADR BİR EKSENİ AÇIK BIRAKMIŞTI

Bu ADR iç içe geçme eksenini kilitledi ama **karar noktası kümesini yazmadı** —
ve sayılar ona da bağlıydı. Araç yazılırken `radon cc` ile 179 fonksiyon üzerinde
çapraz kontrol yapıldı; ölçüt iki noktada yanlıştı:

| kural | radon | ADR yazılırken kullanılan sayaç |
|---|---|---|
| comprehension içindeki `if`ler | **sayılır** | **sayılmıyordu** ❌ |
| `with` | sayılmaz | **sayılıyordu** ❌ |
| `try` gövdesi · `else` · `assert` | sayılmaz | sayılmıyor ✓ |

Düzeltilince **178/179 fonksiyon radon ile birebir** tutuyor. Kalan tek uyuşmazlık
`zincir_dogrula` (araç 40 · radon 41) ve **sebebi ÖLÇÜLMEDİ**.

**Kararın kendisi doğrulandı:** radon da `cmd_isir` için **17** der — yani
"kendi gövdeden say, iç `def`e inme" ekseni de-facto standartla örtüşüyor.

`radon` **bağımlılık değildir**; yalnız ölçüt seçilirken bir kez çapraz kontrol
olarak kullanıldı. `faz0/karmasiklik.py` stdlib `ast` ile çalışır.

**Ders:** bir metrik kararında ekseni değil **kural kümesini** yaz. "Kendi
gövdeden sayılır" yetmedi; hangi düğümün karar sayıldığı da yazılmalıydı. Ve bir
ölçüt kararı mümkünse **dış bir araçla çaprazlanır** — radon iki kusuru
20 dakikada buldu.

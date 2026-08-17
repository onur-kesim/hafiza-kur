# H10 EŞİTLİK KÖRLÜĞÜ — md.11 adayı (ölçüldü, kanıtlandı)

**Tarih:** 17 Ağustos 2026 · **Ortam:** bulut Linux, CPython 3.11, root
**Taban:** HEAD `526d6001` · `hafiza.py` SHA256 `81798E30…`
**Yöntem:** md.10'da bulunan kalıbın sistematik taranması + **motor mutantıyla
sınanması.** Doktrin: *ölçülmeyen kapının hükmü yoktur — ısırdığı mutantla
kanıtlanır.*

---

## 1. TARANAN KALIP

md.10 kapanışında şu ders defterlenmişti:

> **Senaryoda iki büyüklük EŞİTSE, hangisinin ölçüldüğü ÖLÇÜLEMEZ.**
> (md.10'da kapsam içi DOSYA sayısı = ROL sayısı olduğu için "rol say" mutantı
> yeşil geçiyordu.)

O tur **bir** kaçan mutant arandı ve bulundu. "Bir tane bulundu" ≠ "tek taneydi".
Bu tur kalıp **taranabilir hâle getirildi** ve altın kümenin tamamına uygulandı.

## 2. TARAMA — gözlem yüzeyi altın küme (11 hâl × 2 komut = 22 kayıt)

Her kayıttaki her kapı satırından sayılar çıkarıldı; **aynı kapı satırında
tekrar eden** sayı bir kör nokta ADAYIDIR.

**Tek aday çıktı ve istisnasızdı:**

```
[H10]  tekrar eden sayi: 4   -> 14 kayitta
       · H10: 4 blok / 4 ayrik konu
```

H10 satırı taşıyan kayıt sayısı **14/22**; bu 14'ün **14'ünde de** iki büyüklük
eşit. Kümede eşitliğin bozulduğu **tek bir hâl bile yok.**

Tarama kayıt düzeyine de genişletildi (farklı kapılar arası eşit sayı). Bulunan
diğer eşleşmeler §5'te; hiçbiri bu turda mutantla sınanmadı.

## 3. SINAMA — beş mutant, iki tanesi POZİTİF KONTROL

Çapa (motorda **tek yerde** olduğu `assert` ile doğrulandı):

```python
N.append("H10: %d blok / %d ayrik konu" % (len(bl), len(say)))
```

Her mutant için motor SHA'sı, mutant öncesi/sonrası **karşılaştırılarak**
gerçekten değiştiği doğrulandı ("uygulandı ≠ doğru yere uygulandı" dersi).

| mutant | ne bozar | motor SHA | `altin_cikti --karsilastir` | `h10_bolme_mutanti.py` |
|---|---|---|---|---|
| **M-K1 TAKAS** | `(len(say), len(bl))` — iki değer yer değiştirir | değişti | **exit 0 · FARK YOK → KAÇTI** | exit 0 → KAÇTI |
| **M-K2 BLOK YOK** | `(len(say), len(say))` — blok sayısı hiç ölçülmez | değişti | **exit 0 → KAÇTI** | exit 0 → KAÇTI |
| **M-K3 KONU YOK** | `(len(bl), len(bl))` — ayrık konu sayısı hiç ölçülmez | `dda03111` | **exit 0 → KAÇTI** | exit 0 → KAÇTI |
| **P1 METİN — KONTROL** | `"ayrik konu"` → `"ayrik KONU"` | `693f7559` | **exit 1 → ISIRDI ✓** | exit 0 |
| **P2 SAYI — KONTROL** | `len(bl) + 1` | `f7a1126a` | **exit 1 → ISIRDI ✓** | exit 0 |

### 3.1 Kontrol kolları neyi kanıtlıyor

- **P1 ısırdı** ⇒ altın küme bu satırı gerçekten okuyor; araç kör değil.
- **P2 ısırdı** ⇒ araç bu satırdaki **sayıyı** da ölçüyor; sayı değişirse görüyor.
- Buna rağmen M-K1/K2/K3 kaçtı ⇒ **körlük aracın zayıflığından değil,
  SENARYODAKİ EŞİTLİKTEN doğuyor.** Sayı doğru olduğu sürece **nereden geldiği
  ölçülmüyor.**

### 3.2 Görünmezlik doğrudan gösterildi

M-K3 yüklü motorla (`dda03111`) ve temiz motorla (`81798e30`) aynı projede
`kapi` koşuldu:

```
M-K3 yuklu : · H10: 4 blok / 4 ayrik konu
temiz      : · H10: 4 blok / 4 ayrik konu
diff       : (bos) — AYNI, mutant GORUNMEZ
```

Motor "ayrık konu" sayısını **hiç hesaplamasa bile** çıktı bit-bit aynı kalıyor.

## 4. 🔴 İKİNCİ, AYRI BULGU — `h10_bolme_mutanti.py` bu satırı HİÇ ölçmüyor

Tablodaki son sütun: **beş mutantın hiçbiri** `h10_bolme_mutanti.py`'yi kırmızı
yakmadı — P1 ve P2 dâhil. Yani H10'un kendi mutant aracı, H10'un **çıktı
satırının içeriğini** ölçmüyor; yalnız bölme sınıfını (fonksiyon dağılımı,
sıra, düşürme) ölçüyor.

`CLAUDE.md`/motor yorumunda yazılı olan *"`X.py` ile `X_mutanti.py` ÇİFTTİR"*
kuralı **kapsam eşitliği vaat etmiyor**: çift olmak, aynı yüzeyi ölçmek değildir.
Altın küme olmasaydı bu satırın hiçbir koruması olmayacaktı — ve altın küme de
yalnız **değeri** koruyor, **kaynağını** değil.

> **Örtüşen tespit körlüğü** defterde vardı: *"iki kapı aynı mutantı yakalıyorsa
> mutant ikisini de ölçüyor sanılır."* Buradaki hâl **tersi ve daha sinsi**:
> iki araç aynı satıra bakıyor sanılıyor, oysa **biri hiç bakmıyor** ve bu,
> diğerinin yeşili altında görünmez kalıyor.

## 5. NE ÖLÇÜLEMEDİ

1. **Kayıt-içi (kapılar arası) adaylar sınanmadı.** Tarama şunları buldu ama
   hiçbiri mutantla koşulmadı:
   - `60` → H2 ↔ H15, 12 kayıtta. **Kaynak okundu: ikisi de `rc["tavan_kb"]`**
     ⇒ tek büyüklüğün iki yerde basılması, aday DEĞİL.
   - `4` → H10 ↔ H15, 11 kayıtta. H10 defter içeriğinden, H15 `rc`den gelir —
     **bağımsız iki büyüklük, tesadüfen eşit. GERÇEK ADAY, sınanmadı.**
   - `2` → H2 ↔ H15 (4 kayıt) · `0` → H8 ↔ H11 (2 kayıt) · `1`/`3` → H1 ↔ H2 ↔
     `SONUC` (birer kayıt). Sınanmadı.
2. **Diğer kapıların kendi mutant araçları** aynı kapsam kusurunu taşıyor mu —
   yalnız `h10_bolme_mutanti.py` ölçüldü. 16 kapının 15'i bakılmadı.
3. **Sayı DIŞI eşitlikler.** Tarama yalnız sayı token'larına baktı; eşit
   **metin** alanları (iki farklı kaynaktan gelen aynı ad/yol) taranmadı.
4. **Kümedeki eşitliğin sebebi.** 14/14 hâlde `blok = ayrık konu = 4` olması
   `kur`un ürettiği şablondan mı geliyor, yoksa H10'un mantığından mı — **kök
   sebep araştırılmadı.** Eğer şablondan geliyorsa düzeltme senaryodadır
   (küme genişletilir); mantıktan geliyorsa düzeltme kapıdadır.
5. **Windows/macOS.** Yalnız Linux/CPython 3.11, **root**.
6. Ölçüm kum havuzunda (`/tmp/hk-m`, kopya depo) yapıldı; bağlı klasöre ve
   kanonik klona **dokunulmadı** — motor koşum sonunda `81798e30`'a geri yüklendi
   (doğrulandı).

## 6. AÇTIĞI İŞ (md.11 adayı — Onur kilidi ister)

Bu rapor bir **bulgu**dur, düzeltme değildir. Düzeltme yönü seçilmeden kod
yazılmaz. En az üç ayrı seçenek var ve **§5.4 ölçülmeden hangisinin doğru
olduğu bilinemez**:

- **(A) SENARYO düzeltmesi** — altın kümeye `blok ≠ ayrık konu` olan bir hâl
  eklenir (md.10'da `s_karma_2`nin 3 dosya/2 role çekilmesiyle aynı kalıp).
  Ucuz; ama yalnız bu satırı kapatır.
- **(B) ARAÇ düzeltmesi** — `h10_bolme_mutanti.py`'ye çıktı-değeri ekseni eklenir
  (M-K1/K2/K3 birer mutant olarak). Kapsamı gerçekten genişletir.
- **(C) SINIF düzeltmesi** — §2'deki tarama `faz0`'a bir araç olarak konur ve
  her koşumda "kümede eşit büyüklük var mı" diye sorar. En pahalısı; ama kalıbı
  **gelecekteki** kapılar için de kapatır (md.10 → md.11 zincirinin üçüncü
  ısırığını beklemez).

`CLAUDE.md` İŞLEYİŞ §3 (faz0 amaç kapısı) gereği: yeni araç ancak bir BİTTİ
maddesini doğrudan açan bir ölçüm içinse eklenir — (C) seçilirse hangi maddeyi
açtığı yazılmalıdır.

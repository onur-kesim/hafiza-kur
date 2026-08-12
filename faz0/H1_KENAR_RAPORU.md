# H1 KENAR MUTANTI — ÖLÇÜM RAPORU

**Tarih:** 12 Ağustos 2026 · **Motor:** `b954e0cb…ec5` (DEĞİŞMEDİ — bu tur koda
dokunmadı) · **Ortam:** bulut Linux, Python 3.11.15, root olmayan kullanıcı.
**Yeni dosya:** `faz0/h1_bolme_mutanti.py` (tek eklenen şey).

---

## 1. NEDEN — ve ne sorulduğu

`FAZC_H1_RAPOR.md` §4.3 bu turu açık borç olarak bırakmıştı: bölme yapıldı,
ona özgü mutant yazılmadı. Borç kapatıldı. Ama mutantın sorusu "yeni bir kapı
ekleyelim" değildi:

> Kabul ölçütü (a) — 22 ölçümde bit-bit eşdeğerlik — **bugünkü kodun aynı
> davrandığını** kanıtlar. **Bir kenar yarın sessizce koparsa herhangi bir
> ölçümün kırmızı olacağını KANITLAMAZ.**

Mutant bu yüzden **iki sütun** ölçer: kendi hâl kümesi ve altın kümenin aynı
sabotajı görüp görmediği.

---

## 2. SONUÇ

```
7 ısırdı · 0 kaçtı · 0 ölçülemedi        (kendi kümesi, 10 ölçüm)
ALTIN KÜME 3 mutanta KÖR
```

| mutant | ne koparır | kendi kümesi | **altın küme** |
|---|---|---|---|
| M-H1a KENAR `bekle` | BEYAN → FARK | ISIRDI (8) | ISIRDI |
| M-H1b KENAR `var` | GERÇEK → FARK | ISIRDI (8) | ISIRDI |
| **M-H1c KENAR `snapL`** | BEYAN → KOVA | ISIRDI (2) | **KÖR** |
| M-H1d KENAR `canliA` | GERÇEK → KOVA | ISIRDI (8) | ISIRDI |
| **M-H1e SAFLIK KENARI** | `_h1_kova_bek` dönüşü | ISIRDI (2) | **KÖR** |
| **M-H1f KORUMA SÖKME** | snapshot koruması | ISIRDI (2) | **KÖR** |
| M-H1g SIRA | FARK ↔ KOVA sırası | ISIRDI (2) | ISIRDI |

Hâl kümesi: `h_temiz` · `h_kayip` · `h_fazla` · `h_yeni_cakisma` · `h_snapsiz`
— beşi de temiz motorda **ayrık imza** üretiyor (5/5), yani küme körleştirici
değil. Determinizm kolu (aynı motor iki kez) FARK YOK.

---

## 3. 🔴 ASIL BULGU — kabul ölçütü (a) elle yazdığım satırı GÖRMÜYOR

`FAZC_H1_RAPOR.md` §1.4'te koruma satırının tersine çevrilmesini
*"mekanik ve güvenli"* diye niteledim ve gerekçesini yazdım. Gerekçe doğruydu;
**ama o satır, güvendiğim ölçütün kapsamı dışındaydı.**

Kendi aracımın hükmüne güvenmeyip elle kurdum ve altın karşılaştırmayı
doğrudan koşturdum:

```
koruma satiri TAMAMEN silindi -> python3 faz0/altin_cikti.py --karsilastir
  altin kume : faz0/altin_kapi.json (22 olcum)
  bu kosum   : 22 olcum
FARK YOK — kapi ciktisi ve cikis kodlari BIT-BIT ayni.        exit 0
```

**Sebep ölçüldü:** altın kümenin 11 hâlinin **hiçbirinde `_KAYNAK.md` eksik
değil.** Koruma o kümede hiç ateşlenmiyor; söküldüğünde de hiçbir çıktı
değişmiyor.

Bunun ağırlığı şurada: bölmenin **bütün gövdesi üreteçle birebir taşındı**;
elle yazılan tek mantık o koruma satırıydı. Yani (a) ölçütü, bölmedeki
**tek insan eliyle yazılmış karara** yapısal olarak kördü. Yanlış yazsaydım
"FARK YOK, 22 ölçüm bit-bit" yine yeşil yanacaktı.

Bu, FAZ C'de `bl`/`ks` kenarları için ölçülen sınıfın aynısıdır — kod doğru
ama **KANITSIZ**. O tur bunu bir kez öğretti; bu tur aynı sınıfın H1'de de
yaşadığını gösterdi.

### 3.1 Diğer iki körlük

- **M-H1c (`snapL` → KOVA):** altın kümede KOVA'nın "BEYANSIZ TAŞINMA" dalını
  uyandıran hâl yok. Kenar koparıldığında 22 ölçümün hiçbiri değişmiyor.
- **M-H1e (saflık kenarı):** `_h1_kova_bek`'in dönüşü `bek` — beş parçalı
  bölmenin **doğurduğu yeni kenar**. `FAZC_H1_RAPOR.md` §4.2'de "ileride bir
  hüküm kazanırsa koruma kaybı doğar, bunu yakalayan mutant YOK" diye açık
  bırakılmıştı. Artık var; ve altın kümenin o kenara kör olduğu ölçüldü.

---

## 4. ARAÇ KUSURU — bulundu ve düzeltildi

İlk koşumda iki mutant `OLCULEMEDI` döndü: sabotajlı motorla hâl kurulurken
`derle` çöküyordu (`derle`, kapı FAIL verirse derlemeyi reddediyor). Y-4 dersi
gereği bu bir **araç kusurudur**, "kenar sağlam" değildir.

Düzeltme: **hâller bir kez ve TEMİZ motorla kurulur**, kollara kopyalanır,
yalnız **ölçen** motor değişir. Sabotaj ölçende, ölçülen projede değil.
Yan faydası: bütün kollar bit-bit aynı proje ağacını ölçer — kurulum
değişkenliği tamamen kalkar. Düzeltmeden sonra 7/7.

---

## 5. KARAR: **B** (12 Ağustos 2026, Onur) — küme dokunulmadı, kapsam ayrı araçtan

Aşağıdaki iki şık sunuldu; **B kabul edildi ve uygulandı.**

Uygulama: `.github/workflows/capraz.yml`'ye `h1_kenar_mutanti` işi eklendi —
üç platform (ubuntu · windows · macos), Python 3.11, **`continue-on-error` YOK**,
çıktı artefakt olarak yükleniyor. `faz0/altin_kapi.json`'a **dokunulmadı**.

İkinci sütun (altın küme karşılaştırması) **bilerek CI'da koşuyor**: sabit bir
sayı değil, **sürüklenme ölçeri**. Altın kümeye ileride hâl eklenirse KÖR sayısı
düşmeli; kapsam daralırsa yükselmeli. Maliyeti ölçüldü — tam koşum 45 sn
(CI'da zaten olan `fazC_bolme_mutanti` 31 sn), kısaltmaya gerek yok.

🔴 **Bu iş Windows ve macOS'ta HİÇ KOŞMADI.** Düzenek hâl ağacını `copytree` ile
kollara kopyalıyor (git ile başlatılmış dizinler dâhil) ve o davranış orada
ölçülmedi. Kurulum çökerse araç `Kurulamadi → ÖLÇÜLEMEDİ → exit 2` verir,
sessiz PASS değil. **İlk CI koşumu bir ölçümdür**; kırmızı gelirse bilgidir.

### Sunulan şıklar (kayıt)

Mutant körlüğü **ölçtü**, ama kapatmadı. İki yol var, ikisi de Onur'un kararı:

**A) Altın kümeye iki hâl ekle** (`h12_snapsiz`, `h13_kova_kacan`) →
22 ölçüm 26'ya çıkar, kör noktalar kaynağında kapanır. Bedeli: küme yeniden
kaydedilir (`--kaydet`) ve o kayıt bu motordan alınır — yani küme artık
"bölme öncesi motordan alınmış referans" olmaktan çıkar, güvencesi zayıflar.

**B) Küme olduğu gibi kalsın, kapsamı `h1_bolme_mutanti.py` versin.**
Altın küme "bölme öncesine karşı" saflığını korur; kenar kapsamı ayrı araçtan
gelir. Bedeli: iki ayrı araç koşulmadan hüküm tam değildir — ve CI'da ikisi de
koşmalıdır.

**Önerim B**, çünkü altın kümenin tek değeri **bölme öncesi motora bağlı
olmasıdır**; bugünkü motordan yeniden kaydedilirse o bağ kopar ve bir daha
kurulamaz. Ama karar verilmeden CI'a bir şey eklemedim.

---

## 6. NE ÖLÇÜLEMEDİ

1. **CI'da koşmuyor.** `capraz.yml`'ye eklenmedi (§5 kararı beklendiği için).
   Bugün yalnız bulut Linux'ta koştu — Windows/macOS'ta **ölçülmedi**.
2. **Kenar listesi tam mı bilinmiyor.** Dört veri kenarı + saflık kenarı +
   koruma + sıra ölçüldü. `_h1_beyan`'ın `snap0`'ı gibi **parça içi** akışlar
   kapsam dışı; onları ancak parça içi mutasyon ölçer.
3. **`kapi`'nin yazma yapmadığı kanıtlanmadı.** Kollar arası kirlenmeyi
   kopyalayarak önledim; ama komutun gerçekten salt-okunur olduğu ayrıca
   ölçülmedi.
4. **Mutantların örtüşmesi ölçülmedi.** M-H1a ile M-H1d'nin ikisi de 8 ölçümde
   fark veriyor; aynı hâlleri mi kırıyorlar, farklı mı — bakılmadı. Örtüşen
   tespit körlük maskeleyebilir (CLAUDE.md §3).
5. **Altın kümenin diğer sınıflara körlüğü** yalnız bu 7 mutant için ölçüldü.
   Kümenin genel kapsamı bu raporun konusu değil.

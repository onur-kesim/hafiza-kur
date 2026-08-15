# 2026-08-15 — Is-Portfolyo bağımsız denetim itirazı (BİTTİ maddesi 6 KESİLDİ)

**Denetçi:** `C:\dev\Is-Portfolyo` Cowork oturumu (aday host projesinin kendi oturumu).
**Konu:** hafiza-kur'un o projeye `devral` ile kurulma talebi.
**Sonuç:** talep GERİ ÇEKİLDİ · eski BİTTİ maddesi 6 KESİLDİ (Onur kilidi, 15 Ağu 2026).
**Neden bu bir denetim turu sayılır:** kurulum talebi bir teslimdi; üreten oturum onaylamadı,
bağımsız bir oturum ölçtü ve reddetti. Reddin gerekçesi ÜRÜNÜN ÖLÇÜTÜNÜ kırdı — takvimi değil.

---

## Dört itiraz

**1 — ASİMETRİ.** Koordinasyon notu yalnız hafiza-kur'un kazancını beyan ediyordu; host projenin
kazancı yazılmamıştı çünkü ölçülmemişti. Gelir projesi, başka bir projenin kabul kriterini
kapatmak için deney alanı yapılıyordu: risk orada, kazanç burada.
*Ek: bu öneri, host projenin 14 Ağu 2026'da kendi radar sözlüğüne eklediği `kapsam-asimi`
sınıfının örneğidir ("kilidin kapsamı dışına çıkmak — gerekçe meşru olsa bile").*

**2 — ZAMANLAMA.** Host projenin 17–31 Ağu teslim penceresi boş; 18 Ağu ve 19 Ağu'da iki teslim
planlı. Önerilen kurulum penceresi (15–21 Ağu) tam o kriz aralığı. Üreten oturum yalnız
3–17 penceresini ölçüp "sert durak değil" demişti: doğru ama EKSİK ölçüm.

**3 — ÇİFT DEFTER.** Host projenin kendi ölçülmüş kusur sınıfı (`bayat-sayi`); iki ayrı kayıtta
"çift sayım KALICI" ve "şema iki yerde yaşıyor" ölçümleri duruyor. Koordinasyon notu "iki sistem
paralel yaşayacak" deyip riski anmıyor, "mevcut akışa dokunmuyor" diyerek geçiştiriyordu.

> **BİREBİR ALINTI — denetçinin kendi cümlesi:**
> *"dokunmamak yetmez; ayrışmayı ölçen bir kapı olmadan iki defter, bir hafta içinde iki
> farklı gerçek üretir."*
>
> ⚠️ 25 Ağu yazısında alıntılanacaksa **bu cümle** kullanılır. Üreten oturumun ürettiği
> "dokunmamak ≠ çelişmemek" özeti isabetlidir ama **denetçinin sözü değildir**; atıf içerikle
> yapılır, özetle değil.

**4 — EŞZAMANLI YAZMA.** İki oturum aynı append-only dosyalara yazacaktı; not tek satır
demiyordu. İtiraz motorun KENDİ açık kusuruna basıyor: `DURUM.md` "kilit inode yarışı daraltıldı,
**kapatılmadı**" diyor. Yani bilinen bir kusurun üstüne, o kusuru tetikleyecek bir kullanım
öneriliyordu.

---

## 🔴 Asıl bulgu — itiraz 3 ölçütü öldürüyor

Çift defteri güvenli kılmanın tek yolu kanonikliği yazmaktır: *"mevcut sistem KANONİK, hafiza-kur
yalnız iz defteri."* Ama o şart konduğu anda madde 6'nın (d) ayağı çöker:

> Defter **çıkarılmadan** eklenirse token maliyeti tanım gereği **artar**, kazanç **sıfırdır**.
> **Sonucu önceden belli olan şey ölçüm değildir** — sayı kılığına girmiş bir ÖLÇÜLEMEDİ'dir.

(d)'nin dürüst ölçülmesi hafiza-kur'un mevcut defterin **yerine geçmesini** gerektirir; bunu altı
günde bir gelir projesine yapmak dört itirazın hepsini birden ağırlaştırır. Dogfood (hafiza-kur'un
kendi deposu) da aynı çift-defter itirazına düşer: `CLAUDE.md` + `DURUM.md` dururken
`PROJE_HAFIZA.md` açmak orada da ikinci defterdir.

**⇒ Madde 6, yazıldığı hâliyle 21 Ağu'da HİÇBİR hostta kapanamaz. Zamanlama sorunu değil,
ölçüt kusuru.** İŞLEYİŞ md.1 gereği cevap KESMEK; süre uzatmak yasak. Sessiz erteleme en kötü
şıktı: aynı sonucu üretir ama BEYANSIZ keser.

---

## Denetçinin üreten oturuma çıkardığı iki düzeltme

**D-1 — bayat sayı.** Koordinasyon notu host projenin `araclar/` envanterini **11 dosya** diye
yazdı. Diskten sayıldı (15 Ağu 12:06): **10**. Sayı iki notta üst üste taşındı.

**D-2 — yanlış atıf.** Yukarıdaki birebir alıntı bölümüne bakılır.

## Üreten oturumun kendi kusur teşhisi (ölçülerek)

- **PROJELER ARASI SAYI BULAŞMASI.** "11", host projeye ait değil: **Momentum'un** `CLAUDE.md`
  §4.10'undan geldi ve **Momentum için DOĞRU** (`.gitkeep` hariç 11 araç dosyası; diskte
  `-type f` ile 12 görünür). Yani sayı yanlış değildi — **yanlış projedendi**. Bayat sayıdan
  daha sinsi: kaynağı gerçek bir ölçüm olduğu için sorgulanmıyor. Üstelik doğru sayı (10) aynı
  oturumda zaten ölçülmüştü ve hatırlanan sayı onu ezdi.
- **OKUNMADAN HÜKÜM, kendi artefaktım üzerinde.** Karşı-notta "bu cümle `CLAUDE.md` §5'e girdi"
  yazıldı. `grep` ile ölçüldü: **girmemişti**, hiçbir belgede geçmiyor. Kendi dosyamı okumadan
  içeriğini beyan ettim — bu deponun README'sinin kapağında yazan dersin aynısı
  ("belge de bir arayüzdür ve yalan söyleyebilir").
- **AYNI KUSUR, AYNI TURDA TEKRAR (D-3).** Yukarıdaki itirafın bir paragraf sonrasında, denetçiye
  *"birebir cümlen `denetim/2026-08-15_*` içinde **kayda geçti**"* yazıldı. Denetçi `origin/main`'i
  fetch edip ölçtü: dosya **yok** — yalnız yerel, **push edilmemiş** commit'te. Onlara "isterse
  hemen açıp doğrulayabilir" da denildi; o oturum yerel diske erişemez, yani var olmayan bir
  doğrulama yolu gösterildi. **Ders yazıldı ve aynı turda uygulanmadan bir kez daha üretildi.**
  KALICI KURAL (mekanik, tek cümle): *push edilmemiş dosya üçüncü taraf için KAYIT DEĞİLDİR;*
  *"kayda geçti" yerine "diskte yazıldı, sha X, push edilmedi" yazılır.*

---

## Host adayları — elenme gerekçeleri (bu kayıt `CLAUDE.md` §2'den silinince belgesiz kalmıştı)

Denetçinin D-4 itirazı bu boşluğu açığa çıkardı: madde kesilirken §2'deki blok silindi ve
**Momentum'un elenme gerekçesi hiçbir esas belgede kalmadı.** Buraya alındı.

| Aday | Hüküm | Ölçülmüş gerekçe |
|---|---|---|
| **Momentum** | ELENDİ | 8× `obj` + 8× `bin` + `src/client/.dart_tool`, `_h14_adaylar` hariç kümesinde (sat. 4055) YOK ⇒ `.gitignore`'lu oldukları için mtime ile ölçülür ⇒ H14'ün "en yeni değişiklik" delili **hep bir derleme artefaktı** olur (kum havuzunda ölçüldü: `…/obj/Api.assets.cache3.json`). Ayrıca kendi `CLAUDE.md` sat. 8: **"Yeni canlı defter AÇILMAZ"** ve §4.10 kapı bütçesi zaten ihlalde. |
| **Is-Portfolyo** | ELENDİ | Yukarıdaki dört itiraz + ölçüt (d) çıkmazı. |
| **Dogfood** (hafiza-kur'un kendi deposu) | ELENDİ | `CLAUDE.md`+`DURUM.md` dururken `PROJE_HAFIZA.md` açmak orada da ikinci defterdir — 3. itiraz aynen geçerli. |

⚠️ **Momentum "sıradaki aday" DEĞİLDİR.** Denetçi bunu `80468eb`'ye bakarak çıkardı; o commit
kesme öncesidir ve kesme yalnız push edilmemiş commit'lerdedir — yani bu yanlış çıkarım da
D-3'ün sonucudur, denetçinin kusuru değil.

---

## 🔴 YENİ BULGU — README'nin en görünür iddiası ÖLÇÜLEMEDİ

Denetçinin "kalan tek MAJOR" uyarısı üzerine `denetim/` klasörü ölçüldü (15 Ağu 2026).

**README "Denetim" bölümü diyor ki:** *"Bu araç **üç bağımsız denetçiye** verildi ve **on üç tur**
kırılmaya çalışıldı. İlk iki denetçinin kararı `KUR` oldu; üçüncüsü son iki turunda `DÜZELT` dedi."*

**`denetim/` klasöründe ÖLÇÜLEN:**

- **Adı geçen** denetçi: **1** (`Fable 5 Max`, 3.–4. tur). Diğer ikisinin çıktısı depoda YOK.
- Tur sayısı — `2026-08-01_denetciye-not.md` sat. 49-50, birebir: *"Toplam **on iki tur** koştu:
  yedi tur ilk iki dış denetçiyle, **üç tur seninle** (v2.0, v2.1, v2.3), iki tur iç düşman
  ajanlarla — ve paketten sonra iki tur daha."* → 7+3+2 = 12 ✓ *"on iki"*, ama üstüne 2 daha
  eklenince 14; README ise 13 diyordu. **Üç ayrı sayı, hiçbiri tek tek sayılamıyor.**
- `hafiza.py` yorumları 7. tura kadar atıf veriyor, ayrıca "(v2.4 iç tur)" kayıtları var.

🔴 **KENDİ BULGUMU DÜZELTİYORUM (bugünün DÖRDÜNCÜ düzeltmesi, yine kendi kusurum).** İlk
yazdığımda "adı geçen denetçi 1" ölçümünden *"üç bağımsız denetçi doğrulanamıyor"* sonucunu
çıkardım. Yanlış: aynı klasörün kendi cümlesi **"ilk iki dış denetçi" + "seninle"** diyor, yani
**üç dış denetçi ifadesi kaynakta VAR** — eksik olan ADLARI ve çıktıları, iddianın kendisi değil.
Doğru hüküm: *denetçi sayısı KAYNAKTA VAR ama depodan doğrulanamaz · tur sayısı KAYNAKTA BİLE
TUTARSIZ.* "Adı yok" ile "iddia desteksiz" ayrı şeylerdir; ben ikisini birbirine geçirdim.
⇒ Karar (Onur, 15 Ağu): **DARALT.** README'den sayısal tur beyanı kaldırıldı, denetçi sayısı
kaldı ama "tek tek doğrulanamaz" şerhiyle, iç düşman ajan turları AYRI yazıldı.

İki şey bunu ağırlaştırıyor:

1. Bu cümlenin bulunduğu bölüm, kendi son satırında şunu yazıyor: *"Açık bulgular kapanmadan bu
   araç 'denetimden geçti' diye sunulmaz."* **İddiayı denetleyen bölüm, denetlenmemiş iddiayı
   taşıyor.**
2. `faz0/readme_mutanti.py` buna **yapısal olarak kör**: kendi başlığında "README'nin ANLATIMINI
   ölçmez, yalnız ölçülebilir beyanlarını" yazıyor ve yalnız "Kanıtı kendin koş" bloğunu çözüyor.
   Deponun **en görünür sayısal iddiası kapının kapsamı dışında.** 25 Ağu okuru önce bunu okuyacak.

**Karar Onur'da; bu kayıt yalnız ölçümü sabitler.**
**KAPANDI (Onur kilidi, 15 Ağu): DARALT.** README'den sayısal tur beyanı kaldırıldı; denetçi
sayısı "tek tek doğrulanamaz" şerhiyle kaldı; iç düşman ajan turları ayrıldı. Kapı koşuldu:
3 kapı YEŞİL, 6/6 mutant, kapılı blok `diff` boş.

---

## 🔴 SON BULGU — ölçülmeyen sözleşme: `README_EN.md` aynası

Denetçi bugün **üç kez** aynanın bayatladığını ölçtü: damga `478003f` (→ `ca0562f` `~13 dk`'yı
sildi) · damga `80468eb` (→ `## Denetim` yeniden yazıldı) · damga `ee7f6e2` (şu anki).
Çeviri notunun kendi sözleşmesi: *"if the two files ever disagree, README.md is canonical — and
the disagreement itself is a finding."* **Sözleşme doğru, mekanizma YOK.** Üç ayrışmayı da bir
kapı değil bir insan/oturum fark etti. Bu, bu deponun tam olarak var olma sebebi olan kusur sınıfı.

**Sınıf ayrımı (önemli, aynı kefeye konmamalı):**
`D-3` bir **YANLIŞ beyandı** — hiç doğru olmamış bir durum iddiası. Buradaki ise **BOZULABİLİR
beyan**: ölçüldüğü an doğruydu, sonra bayatladı. Üstelik bu turdaki örnek, notun KENDİ talimatı
uygulandığı için bayatladı (`37ece61f` → Onur commit bloğunu koştu → `ee7f6e21`). İkisinin çaresi
farklıdır: yanlış beyanın çaresi ölçmek, bozulabilir beyanınki **son kullanma tarihi vermektir.**

**Bu oturumun kendine yazdığı kural:** *nota yazılan her commit kimliği, yanında tazelik
komutuyla birlikte yazılır.* "origin = X" değil, "origin = X (ölçüm SS:DD) — okurken doğrula".

### Neden CI kapısı ÖNERİLMİYOR (denetçinin 1. şıkkı)
1. **Amaç kapısı (İŞLEYİŞ md.3):** `faz0/`'a yeni araç ancak bir BİTTİ maddesini DOĞRUDAN açarsa
   eklenir. BİTTİ listesi **5/5, kapalı** — açılacak madde yok.
2. **`README_EN.md` bir Is-Portfolyo artefaktıdır**, hafiza-kur'un değil. Depoya alıp kapıya
   bağlamak, hafiza-kur'un başka bir projenin artefaktı için bedel ödemesi demektir — bu sabah
   Is-Portfolyo oturumunun **haklı olarak reddettiği asimetrinin aynadaki görüntüsü.**
3. §5: "public repo ≠ yayın"; depo, göndermeyi planlamadığı bir çevirinin sahipliğini almaz.

### Önerilen üçüncü yol — damgayı KALDIRMA, ANLAMINI DEĞİŞTİR
Damga bir *güncellik* iddiası olmaktan çıkıp bir *ölçüm çıpası* olur. Çeviri notu şunu der:
"README.md kanoniktir; bu çeviri `<damga>`'ya karşı yapıldı, sonraki her commit **doğrulanmamış
sayılır**." Ve yanına okurun koşacağı tek satır konur:

```bash
git log --oneline <damga>..HEAD -- README.md     # boş = ayna taze · dolu = bayat + neyin değiştiği
```

**Ölçüldü (kum havuzu, 15 Ağu):** taze durumda `0` satır; kaynak dosya değiştikten sonra `1`
satır ve değiştiren commit'in kimliği. Yani ayrışma **mekanik olarak ölçülebiliyor** — CI
gerekmiyor, çünkü ölçümü okur koşuyor. Bu, README'nin kendi "Kanıtı kendin koş" doktrininin
aynısıdır ve kapı bütçesine dokunmaz. **Karar `README_EN.md`'nin sahibindedir.**

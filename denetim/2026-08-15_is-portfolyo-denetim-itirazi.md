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

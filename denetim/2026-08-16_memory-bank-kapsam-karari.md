# 2026-08-16 — `memory-bank/` kapsam kararı (ölçüldü, kod yazılmadı)

**Soru:** Sektörün en yaygın ajan-hafıza konvansiyonu olan `memory-bank/`, adaptör
tablosunda `disarida` (kapsam dışı) sayılıyor. Bu bir KUSUR mu, yoksa bilinçli bir
KAPSAM SINIRI mı?

**Neden soruldu:** md.8 ölçümü gösterdi ki `memory-bank/` taşıyan **22/22** gerçek
depoda `canli` aday YOKTUR ve `devral` durur. Yani "hafızası olan projeyi devral"
diye tanımlanan komut, hafızası gerçekten olan projelerin tamamında reddediyordu.

**Karar önerisi: EŞLEME KALIR — bu bir kusur değil, kapsam sınırıdır.**
Karar Onur'undur; bu kayıt yalnız ölçümü ve gerekçeyi sabitler.

---

## Ölçüm 1 — konvansiyon gerçekten çok dosyalıdır (22 depo, salt okuma)
`progress.md` 22/22 · `activeContext.md` 20/22 · `systemPatterns.md` 20/22 ·
`productContext.md` 18/22 · `projectbrief.md` 18/22 · `techContext.md` 18/22.
Ortalama **6,4** dosya (min 5, maks 11).

Motor **TEK** canlı defter yazar. Altı dosyadan hangisinin "canlı" olduğu motorca
bilinemez: `progress.md` en yaygın olan, `activeContext.md` ise adıyla "güncel
bağlam" diyen. Motorun bunlardan birini KENDİ seçmesi, md.7'nin kapattığı **sessiz
sahiplenmenin** ta kendisidir.

## Ölçüm 2 — altısını `canli` adayı yapmak sonucu DEĞİŞTİRMEZ
O hâlde her memory-bank deposunda 5–11 aday olur ve md.7'nin **çoklu `canli`
KAPISI** ateşlenir: çıkış ≠ 0, diske sıfır bayt, `--esle` ister. Yani araç yine
durur; değişen tek şey mesajın metnidir. Kapsamı genişletmenin bedeli var, getirisi
yok.

## Ölçüm 3 — KAÇIŞ YOLU ZATEN ÇALIŞIYOR (asıl bulgu)
`devral --esle canli=memory-bank/progress.md` **22 deponun 22'sinde** koşuldu:

```
cikis != 0                    : 0 / 22
yalniz SECILEN dosya degisti  : 22 / 22
baska memory-bank dosyasi     : 0 / 22
```

Örnek (BookSwap): `progress.md` 6.919 → 7.265 B (**+346 bayt**); kullanıcının
**bütün satırları korundu**, v2 iskeleti (KARAR GÜNLÜĞÜ · ARŞİV DİZİNİ) sonuna
eklendi; diğer beş dosya bayt-birebir aynı kaldı.

⇒ Araç bir memory-bank'i **temiz biçimde devralabiliyor.** Sorun kapsamda değil.

---

## 🔴 O hâlde gerçek kusur nerede: GÖRÜNÜRLÜK
Durma mesajı doğru kaçış yolunu (`--esle canli=<dosya>`) veriyor ama:
1. Envanterde az önce listelediği altı dosyanın **birer aday olduğunu söylemiyor**;
   kullanıcı `<dosya>` yerine ne yazacağını mesajdan çıkaramıyor.
2. İkinci öneri **"Gerçekten YENİ defter aç: `--esle canli=PROJE_HAFIZA.md`"**.
   Çift defteri önlemek için durmuş bir araç, aynı ekranda ikinci defteri öneriyor —
   üstelik tanınmış altı hafıza dosyası ekranda dururken.

⇒ **md.9 adayı (kod işi, tek eksen):** tanınan hafıza dosyası varken durma mesajı
adayları adlarıyla göstersin ve "YENİ defter aç" ilk sırada olmasın. md.8'in
mesaj ayrımını tamamlar; ADDITIVE, kapı bütçesine dokunmaz.

## 🟡 Lafız riski (kusur beyanı DEĞİL — sınıfı ayrı tutuluyor)
`hafiza.py` sat. 3175 triyajda şunu basıyor: *"Mevcut sisteme (v1) DOKUNULMADI:
eski çıpa, zincir ve defterler olduğu gibi duruyor."* Cümle **v1 çıpa/zincir/defterleri**
hakkında doğrudur (memory-bank deposunda zaten yoktur). Ama `--esle` ile kullanıcının
kendi dosyası canlı seçildiğinde o dosyaya 346 B yazılır ve okur bunu "hiçbir şeyime
dokunulmadı" diye okuyabilir. Yanlış beyan değil, **yanlış okunmaya açık** beyan.
Kayda geçer; md.9 açılırsa aynı ekranda düzeltilebilir.

---

## NE ÖLÇÜLEMEDİ
1. **Devralma sonrası hüküm.** BookSwap'ta triyaj kırmızı verdi ([H4] ölü bağlantı ×11);
   araç "ilk koşumda KIRMIZI NORMALDİR" diyor ama bu **doğrulanmadı** — `kapi`/`isir`
   devralma sonrası hiç koşulmadı. 22 depoda yalnız `devral`ın kendisi ölçüldü.
2. **Platform.** Devralma yalnız Linux'ta koşuldu; Windows/macOS'ta hiç denenmedi.
3. **Kullanıcı niyeti.** `progress.md` hedef seçildi çünkü 22/22'de vardı; gerçek
   kullanıcının hangi dosyayı canlı sayacağı ÖLÇÜLEMEZ — zaten bu yüzden seçim
   kullanıcıya bırakılıyor.
4. `.cursor/rules/` çok dosyalı hâli (trpc'de 7 dosya) `kural_evi` tarafında aynı
   "hangisi" sorusunu doğuruyor; bu tur onu KAPSAMADI.

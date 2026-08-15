# hafiza-kur — PROJE ESASLARI (CLAUDE.md)
`MOD: NORMAL`

> **FESİH BEYANI (14 Ağu 2026, Onur onayı — hız-kaybı denetimi):** Bu dosya eski `CLAUDE.md`'nin
> yerine geçer (eskisi `CLAUDE-eski-2026-08-14.md`). Feshedilenler: 4 betikli oturum-açılış ritüeli ·
> iç denetim turu düzeni · her kapanışta zorunlu DEVİR. Ürün kararları ve ölçülmüş mayınlar KORUNDU.
> **EK (aynı gün):** BİTTİ listesi KİLİTLENDİ (§2) · %10 oran kuralı SİLİNDİ, yerine amaç kapısı ·
> `cmd_*` bölmeleri KESİLDİ (§5). Bu dosya ≤8 KB kalır; yanında tek `DURUM.md` yaşar.

## 1. NE (3 satır)
Taşınabilir proje-hafızası kapı sistemi: tek dosyalık saf-Python motor (`skill/scripts/hafiza.py`,
stdlib, sıfır bağımlılık) + Claude skill paketi. Ürünün tek vaadi ÖLÇÜLEBİLİRLİK; onu zayıflatan
değişiklik, getirdiği kolaylık ne olursa olsun yanlıştır. Doktrin: ölçülmeyen kapının hükmü yok ·
ölçülemeyene "temiz" denmez · engellenemeyeni GİZLENEMEZ KIL.

**Ürün kararları (özet; yeniden tartışılmaz, değiştirmek gerekçeli ADR ister):** tek dosya kalır
(bölünen fonksiyonlardır; CC ölçümü `faz0/karmasiklik.py` ile) · embedding/ANN yok, determinist
geri getirme · İngilizce kanonik komut + Türkçe alias · depo PUBLIC ama YAYIN YOK · çıkış-kodu
sözleşmesi kırılırsa minor artar.

## 2. BİTTİ LİSTESİ (KİLİT 14 Ağu · liste 6→5 KISALDI 15 Ağu 2026, İŞLEYİŞ md.1 — gerekçe §5)
- [x] Kullanıcı `kur/kapi/isir/not/derle/devral` komutlarını Linux'ta koşabilir (CI yeşil)
- [x] **Windows'ta** tam hüküm. ÖLÇÜT = (i) iki `win32` dalı mutantla koparılıp CI'da ISIRIYOR
      **ve** (ii) `.skill` taze projede GERÇEK Windows'ta kurulup `kur→kapi→isir` koşuyor.
      *(i) CI #43 `cde1998` `faz0/win_dal_mutanti.py` · (ii) CI #46 `5d81838` `win32`, 8,6 sn.)*
- [x] **macOS'ta** tam hüküm. ÖLÇÜT = ortak batarya macos-latest'te `continue-on-error`sız yeşil.
      *(CI #39, 14 Ağu: darwin dalı SIFIR — platforma özgü yüzey yok; NFC/NFD KAÇINMAYLA yönetiliyor (§4).)*
- [x] Kullanıcı `.skill` paketini kurup taze bir projede 5 dakikada çalıştırabilir (kurulum belgesiyle)
      *(CI #46 `5d81838`, üç platform: `faz0/paketten_kos.py` BELGENİN akışını izler ve komutları
      belgeye karşı ölçer; windows'ta 8,6 sn. ŞERH: ölçen CI'dır, insan eli değil.)*
- [x] 25 Ağu yazısının okuru, depoya gelip README ile sistemi kendi başına deneyebilir.
      ÖLÇÜT = README'nin "Kanıtı kendin koş" bloğu CI'da ÜÇ PLATFORMDA `continue-on-error`sız koşar
      ve bloktaki HER sayısal beyan gerçekle TUTAR; beklenen değerler BLOKTAN okunur.
      *(CI #49 `fba20c8`: `faz0/readme_mutanti.py` 3 kapı + 6/6 mutant; yedi beyanın yedisi ölçüldü.
      ŞERH: ölçen CI'dır, insan okuru değil.)*
*(Eski 6. madde — "gerçek bir projede 1 hafta fiilen kullanım" — 15 Ağu 2026'da KESİLDİ,
İŞLEYİŞ md.1. Gerekçe §5'te; zaman değil ÖLÇÜT kusuru. Liste 6→5, sayaç **5 ✅ / 5**.)*

## 3. SIRADAKİ İŞ (tek madde)
<`DURUM.md`'den takip edilir; tek dikey dilim.>

## 4. ORTAM MAYINLARI (ölçülmüş)
- Bağlı klasör mount'unda **hiçbir `git` komutu koşma** (`status` dâhil): mount `unlink` vermez,
  `.git/index.lock` kalıcı kalır. Depo durumunu `find`/`ls`/dosya okumayla anla; git işini komut
  olarak yaz, Onur koşsun. Push ve commit DAİMA Onur'da.
- Tek kanonik klon: `C:\Users\gulci\Desktop\fable dosyalama\depo\hafiza-kur`. İkinci klon açma.
- Disk adlarında Türkçe diyakritik ASLA (macOS NFD/NFC ayrışması zinciri kırar); ASCII bilinçli.
- `.hafizarc` anahtarları · `_CIPA.json`/`_ZINCIR.jsonl` alan adları · dosya adları ÇEVRİLMEZ.
- `.gitattributes`'taki `* -text` gevşetilmez (gerekçe dosyanın içinde).
- Çalışma zamanı import'u stdlib dışına çıkamaz (geliştirme araçları serbest); determinizm kırılmaz
  (indeks otorite değil: silinip yeniden üretilince bit-bit aynı).
- 🔴 25 Ağu 2026 sonrası depo adresi (`onur-kesim/hafiza-kur`) DEĞİŞMEZ — yazıda dışa verilecek.
- Süre tahmini belgeye yazılmaz (bir kez yazıldı, yanlıştı, sonraki oturumun teşhisini saptırdı).
- Çıktı kodlaması mayını (ÖLÇÜM DÜZELTİLDİ 14 Ağu): ayrım Türkçe/İngilizce DEĞİL, **UTF-8 / eski kod
  sayfası**. `✓` (U+2713) cp1254'te de cp1252'de de çöker; maskeleyen şey konsolun UTF-8 olmasıdır.
  "bende çalışıyor" hüküm değildir; `_cikti_kodlamasini_guvenceye_al()` ÖLÇÜM ARAÇLARINA DA konur (Y-2).
- Sürüm denetim turu SÜRERKEN koda dokunulmaz; kapı/koruma sökümü serbesttir ama daima gerekçeli ve
  beyanlıdır (sessiz söküm yok).

## 5. KAPSAM DIŞI (gizlenmez)
Tuzak Avcısı işleri · TSK/gelir hukuku · Reels-bülten operasyonu (ayrı projeler). PyPI/marketplace/
duyuru YOK ("public repo ≠ yayın"). Semantik arama/embedding bilinçli reddedildi.
**KESİLDİ 14 Ağu 2026:** `cmd_*` bölmeleri ve kalan CC borcu. `ihlal 8` ve `CC>20: 5` olduğu yerde
kalır. Gerekçe: hiçbir BİTTİ maddesi CC'ye bağlı değil, 25 Ağu'ya 11 gün var. Yeniden açmak ADR ister.
**KESİLDİ 15 Ağu 2026 (Onur kilidi, İŞLEYİŞ md.1):** eski madde 6 — "gerçek bir projede 1 hafta
fiilen kullanım" — ve `faz0/kullanim_kapisi.py`. Gerekçe **zaman değil ÖLÇÜT KUSURU:** (d) token
maliyeti/kazancı ancak hafiza-kur mevcut defterin YERİNE geçerse dürüst ölçülür; "mevcut sistem
kanonik kalır" şartıyla maliyet tanım gereği artar, kazanç sıfırdır ⇒ **sonucu önceden belli olan
şey ölçüm değil, sayı kılığında ÖLÇÜLEMEDİ'dir.** Aday host Is-Portfolyo'nun bağımsız denetçisi dört
itirazla reddetti: asimetri (kazanç ölçülmemiş) · 17–31 Ağu teslim penceresi boş, 18–19'da iki teslim ·
çift defter = o projenin K123/K127 `bayat-sayi` sınıfı · eşzamanlı yazma, ki motorun kendi
"kilit inode yarışı KAPATILMADI" kusuruna basıyor. Dogfood da çift deftere düşer. 25 Ağu yazısında
bu madde **"ölçülemedi, sebebi şu"** diye AÇIK yazılır — gizlenmez. Yeniden açmak ADR ister.

---

## İŞLEYİŞ (v2 — değişmez blok)

1. **Takvim kutusu:** madde güne bağlanır; kutu dolarsa madde kesilir, süre uzamaz; kesilen §5 + README'ye.
2. **Dikey dilim:** kullanıcıya görünen davranışla bitmeden "bitti" yok (bu projede kullanıcı = skill'i kuran kişi; "görünen davranış" = komutun gerçek projede koşması).
3. **faz0 AMAÇ KAPISI** *(oran kuralı 14 Ağu 2026'da SİLİNDİ)*: `faz0/`'a yeni araç ancak bir BİTTİ maddesini DOĞRUDAN açan bir ölçüm içinse eklenir; gözle denetlenir (§10). Gerekçe (ölçüldü 14 Ağu — satır: faz0 11.188 / skill 7.064 = %158): %10 oranı bu projede ölçülemez bir hedefti — `faz0/` §7'nin TEK VİTRİNİ'dir, onu bütçeye sokmak ürünü kendi vaadinden kısar; üstelik "her düzeltmeye ayrı mutant" kırmızı çizgisiyle çarpışıp her kapı düzeltmesini yasaklıyordu.
4. **Kâğıt denetim turu = 0; denetim SÜRÜM SINIRINDA tek bağımsız tur** (canlı koşum: `kur→kapi→isir` + iki koşucu, temiz makinede). İç düşman-ajan turları açılmaz. Ajan beyanına güven + sürüm başına 1 rastgele beyan doğrulaması.
5. **Açılış ≤3 komut:** (git'siz) dosya durumu · `DURUM.md` · son CI koşumu. Betik bataryası oturumda koşulmaz; CI (`capraz.yml`) koşar.
6. **Borç defteri yok:** ŞİMDİ YAP · KES (§5+README) · SİL.
7. **Tek vitrin:** "kör kapı protokolü + sabotaj sınaması" vitrindir; başka vitrin açılmaz.
8. **Kural yaşam döngüsü:** iki kez ısırmayan olay kural olamaz (yeri `DURUM.md` bilinen sınırlar); doğan kural ya CI'da koşar ya tek cümledir; §4'e girerken bir satır siler.
9. **Haftalık tek soru:** bitti listesinde kaç madde ✅'ye döndü?
10. **Taban:** bu dosya için kapı, mutant, altın küme, denetim turu yazılmaz; gözle denetlenir. Öncelik: MUTLAK SINIRLAR > global anayasa > bu dosya > diğer her şey.

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

## 2. BİTTİ LİSTESİ (KİLİT 14 Ağu · eski md.6 KESİLDİ §5 · md.6-9 15-17 Ağu, md.10 17 Ağu — **10 ✅ / 10**)
- [x] `kur/kapi/isir/not/derle/devral` Linux'ta koşuyor (CI yeşil)
- [x] **Windows'ta** tam hüküm — `win_dal_mutanti` CI #43, `kur→kapi→isir` CI #46
- [x] **macOS'ta** tam hüküm — ortak batarya `continue-on-error`sız yeşil CI #39, NFC/NFD
      KAÇINMAYLA (§4)
- [x] `.skill` taze projede 5 dk'da çalışır — `paketten_kos.py` BELGEYE karşı ölçer, CI #46
- [x] 25 Ağu okuru README ile deneyebilir — `readme_mutanti.py` 3 kapı/6 mutant, CI #49
      `fba20c8`. ŞERH (hepsinde): ölçen CI'dır, insan eli değil.
- [x] **Hafızası KENDİ ADIYLA duran projeyi devralabilir** — `--kesif`+`--esle`+DURMA KURALI;
      `devral_kesif_mutanti.py` 3/3, CI #57 `ccd9721`.
- [x] **İki defterin AYRIŞTIĞINI motordan öğrenir** — `sahip=` taşır, çoklu `canli` KAPI.
      `ayrisma_mutanti.py` 3/3, CI #59 `5f05b14`; kural evi KAPSAM DIŞI.
- [x] **Durma HÜKMÜ iki hali AYIRT EDER** — boş ağaç ile rol atanmış ağaç aynı hükmü basamaz
      (72 gerçek depo). `hukum_ayrimi_mutanti.py` 1/2. Çapa 97→99 (radon çaprazlı).
- [x] **Durma hükmü BİLDİĞİNİ komuta koyar** — kapsam içi dosya GERÇEK adıyla kilitlenir,
      kapsam dışı hiç önerilmez/kırpılmaz. `gorunurluk_mutanti.py` 4/5, CI #69 `7658b4a5`.
      Çapa `cmd_devral` 99→97 (govde ayrıştı, radon çaprazlı).
- [x] **Ayrım cümlesi kapsam dışını "gerçek defter OLABİLİR" iddiasına KATMIYOR** — hal-2
      dalının sayısı/rol listesi `envanter` yerine `ici`den gelir (SAYI+ROL bulaşması
      kapandı; md.9 kapısı buna kördü, ayrı eksen). `hukum_tutarliligi_mutanti.py` (yeni)
      1 kapı/3 mutant, her biri KENDİ ekseni (sayı/rol); kapı md.10 ÖNCESİ motorda KIRMIZI
      yandı. Hal-1/hal-3 BİREBİR korundu (byte-diff). CC/`ihlal` DEĞİŞMEDİ (ADDITIVE).

## 3. SIRADAKİ İŞ (tek madde)
<`DURUM.md`'den takip edilir; tek dikey dilim.>

## 4. ORTAM MAYINLARI (ölçülmüş)
- Bağlı klasörde **hiçbir `git` komutu koşma** (`status` dâhil): kalıcı `.git/index.lock` bırakır.
  Durumu **loose ref** okuyarak anla (`packed-refs` BAYAT olabilir); git işini komut olarak yaz.
  **PUSH Onur'da; KOD ve COMMIT Claude Code'da** — Cowork ölçer, denetler, kararı hazırlar
  (Onur kilidi 16 Ağu: üreten ≠ denetleyen · commit ayrımı 19 Ağu).
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
**KESİLDİ 14 Ağu 2026:** `cmd_*` bölmeleri ve kalan CC borcu. `CC>20: 5` sabit; `ihlal` 9'da
(md.6-9 ölçüm, kapı değil). Gerekçe: hiçbir BİTTİ maddesi CC'ye bağlı değil. Açmak ADR ister.
**md.7 İKİ KEZ DARALTILDI 15 Ağu (kod yazılmadan):** lafzi D + (b) ayağı ELENDİ (gerekçe git
geçmişinde).
**KESİLDİ 15 Ağu 2026 (Onur kilidi, İŞLEYİŞ md.1):** eski madde 6 — "gerçek bir projede 1 hafta
fiilen kullanım" — ve `faz0/kullanim_kapisi.py`. Gerekçe **zaman değil ÖLÇÜT KUSURU:** (d) token
kazancı ancak hafiza-kur mevcut defterin YERİNE geçerse dürüst ölçülür; "mevcut defter kanonik
kalır" şartıyla sonuç önceden EKSİ'dir ⇒ **sonucu belli olan şey ölçüm değil, sayı kılığında
ÖLÇÜLEMEDİ'dir.** Üç adayın (Is-Portfolyo · Momentum · dogfood) elenme gerekçeleri ve dış
denetçinin dört itirazı ÖLÇÜLDÜ: `denetim/2026-08-15_*`. 25 Ağu yazısında "ölçülemedi + sebebi"
diye AÇIK yazılır. Yeniden açmak ADR ister.

---

## İŞLEYİŞ (v2 — değişmez blok)

1. **Takvim kutusu:** madde güne bağlanır; kutu dolarsa madde kesilir, süre uzamaz; kesilen §5 + README'ye.
2. **Dikey dilim:** kullanıcıya görünen davranışla bitmeden "bitti" yok (bu projede kullanıcı = skill'i kuran kişi; "görünen davranış" = komutun gerçek projede koşması).
3. **faz0 AMAÇ KAPISI** *(oran kuralı 14 Ağu 2026'da SİLİNDİ)*: `faz0/`'a yeni araç ancak bir BİTTİ maddesini DOĞRUDAN açan bir ölçüm içinse eklenir; gözle denetlenir (§10). Gerekçe (ölçüldü 14 Ağu, faz0 11.188 / skill 7.064 = %158): %10 ölçülemez bir hedefti — `faz0/` §7'nin TEK VİTRİNİ'dir ve "her düzeltmeye ayrı mutant" çizgisiyle çarpışıp her kapı düzeltmesini yasaklıyordu.
4. **Kâğıt denetim turu = 0; denetim SÜRÜM SINIRINDA tek bağımsız tur** (canlı koşum: `kur→kapi→isir` + iki koşucu, temiz makinede). İç düşman-ajan turları açılmaz. Ajan beyanına güven + sürüm başına 1 rastgele beyan doğrulaması.
5. **Açılış ≤3 komut:** (git'siz) dosya durumu · `DURUM.md` · son CI koşumu. Betik bataryası oturumda koşulmaz; CI (`capraz.yml`) koşar.
6. **Borç defteri yok:** ŞİMDİ YAP · KES (§5+README) · SİL.
7. **Tek vitrin:** "kör kapı protokolü + sabotaj sınaması" vitrindir; başka vitrin açılmaz.
8. **Kural yaşam döngüsü:** iki kez ısırmayan olay kural olamaz (yeri `DURUM.md` bilinen sınırlar); doğan kural ya CI'da koşar ya tek cümledir; §4'e girerken bir satır siler.
9. **Haftalık tek soru:** bitti listesinde kaç madde ✅'ye döndü?
10. **Taban:** bu dosya için kapı, mutant, altın küme, denetim turu yazılmaz; gözle denetlenir. Öncelik: MUTLAK SINIRLAR > global anayasa > bu dosya > diğer her şey.

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

## 2. BİTTİ LİSTESİ (KİLİT 14 Ağu · 15 Ağu: eski md.6 KESİLDİ §5; md.6 açıldı+kapandı, md.7 AÇILDI — **6 ✅ / 7**)
- [x] `kur/kapi/isir/not/derle/devral` Linux'ta koşuyor (CI yeşil)
- [x] **Windows'ta** tam hüküm — `win_dal_mutanti` CI #43 `cde1998` + gerçek Windows'ta
      `kur→kapi→isir` CI #46 `5d81838`
- [x] **macOS'ta** tam hüküm — ortak batarya `continue-on-error`sız yeşil CI #39; darwin dalı
      SIFIR, NFC/NFD KAÇINMAYLA (§4)
- [x] `.skill` taze projede 5 dk'da çalışır — `paketten_kos.py` BELGEYE karşı ölçer, CI #46 `5d81838`
- [x] 25 Ağu okuru README ile deneyebilir — `readme_mutanti.py` 3 kapı/6 mutant, beklenen değerler
      BLOKTAN okunur, CI #49 `fba20c8`. ŞERH (hepsinde): ölçen CI'dır, insan eli değil.
- [x] **Hafızası KENDİ ADIYLA duran projeyi devralabilir** — `devral --kesif` + `--esle` + DURMA
      KURALI; `devral_kesif_mutanti.py` 3 kapı/3 mutant, CI #57 `ccd9721` (94 iş/0 başarısız).
      Ölçüt (c)'nin VE'li ilk yazımı DELİKTİ, tek koşula indi; M-3 tam onu kurar.
- [ ] **Kullanıcı, iki defterin AYRIŞTIĞINI motordan öğrenir.** *(AÇILDI 15 Ağu, Onur kilidi;
      aynı gün iki kez DARALTILDI — gerekçeler §5.)* ÖLÇÜT — (a) motorun yazdığı her blok
      `sahip=` taşır (`hafiza-kur` = iskelet · `proje` = içerik); alan YOKSA **ÖLÇÜLEMEDİ**
      basılır, sessizce sahiplenilmez · (c) tanınan `canli` birden çoksa **DURUR** (çıkış ≠ 0,
      `--esle` ister; bugüne kadar uyarıp ilkini seçiyordu) · (d) ikisi de AYRI mutantla ısırır.
      Araç: `faz0/ayrisma_mutanti.py` · Kutu **22 Ağu**. Kural evi KAPSAM DIŞI (`SKILL.md` §2).

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
**KESİLDİ 14 Ağu 2026:** `cmd_*` bölmeleri ve kalan CC borcu. `CC>20: 5` olduğu yerde kalır;
`ihlal` 15 Ağu'da 8→**9** (md.6 iki bayrak ekledi, `main` 80→82 satır; ölçüm, kapı değil).
Gerekçe: hiçbir BİTTİ maddesi CC'ye bağlı değil, 25 Ağu'ya 11 gün var. Yeniden açmak ADR ister.
**md.7 İKİ KEZ DARALTILDI 15 Ağu (kod yazılmadan):** (i) lafzi D ("aynı rol iki kez = KIRMIZI")
ELENDİ — altı gerçek ağaç şeklinin dördünde kırmızı, üçü MEŞRU ⇒ kırmızıyı değersizleştirirdi.
(ii) (b) ayağı ("aynı `konu` iki dosyada FARKLI gövde") KESİLDİ — `derle` eski bloğu arşive TAŞIR,
gövdeler ZORUNLU farklıdır ⇒ SAĞLIKLI akışta yanardı; "arşivdeki satır değişti" H1'de ZATEN kapılı.
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

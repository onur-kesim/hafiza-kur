# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (origin `0e3e535`; P4.1 `1f03d12`..`5a15f3c` yerelde; tam tur 74 OK/9 bilinen KIRMIZI)
Son güncelleme: 13 Eki 2026 · ≤8 KB · **kapanan bölüm tek satıra iner**

## DEVİR O21 → O22 (13 Eki) — P4.1 BİTTİ (yerelde) · PUSH YOK · Cowork kabulü + kör okuma tekrarı bekler
Taban `0e3e535` = origin. Zincir: K1 `1f03d12` · K2 `246c825` · K3 `10e21df` · belge `3d22807` · inceleme düzeltmeleri `0d79516` · çapa `5a15f3c`. `karar-kaynagi` (İKİNCİ blok YOK): satır içi `gerekce` önceliği (etiketli > satır başı sözcük > `🔴`/`**`+sözcük; tablo/başlık hariç) · yalnız-başlık beyanı `(yalniz baslik: icerik icin dosyayi ac)` · sıra alıntılı→yalnız başlık→GEREKCESIZ, GECERLI→BEYANSIZ→TASLAK · kayıt ≤ 280 B (GECERLI'de her alanın ilk alıntısı korunur) · `listelenmedi: <durum dağılımı>` · kapı 4/4 + R3 için L66 (COEP).
**Ölçüm:** harness 95 sabotaj/0 çapa bozuk, hepsi ISIRDI (M-Z17..32) · tam tur `_olcum\p41_tur\ci_son.log`: 74 OK / 9 bilinen KIRMIZI / 2 SKIP · `sabotaj.py` 67/0 · `karmasiklik` 7/9/99/30 AYNI · `altin_cikti` FARK YOK · motor +93 satır/+4.963 B · **Momentum `d4b5417` (ham `_olcum\p41_momentum.txt`): altın 4/4**, R3 `:66` COEP alıntısı, blok 8095 B (marj ~100 B), 20/29 listelenir.
**Bağımsız inceleme 7 bulgu** (durum ayrıştırma · bedel tavanda düşüyordu · sayım · etiket kayması · P1 bütçe guard'i · fixture TASLAK değildi · `🔴`) **hepsi kapandı**. **Sınırlar:** sınıf 3 gürültülü · alıntı ilk 160 kr · marj ~100 B: ilk düşen TASLAK ADR · TASLAK'ta yalnız ilk satır garanti.
**Sıradaki:** Cowork: mekanik kabul + 1 rastgele beyan + kör okuma tekrarı (aynı protokol; hedef KARAR > 1,83, R3'te YANLIŞ 0) → Onur push → CI. **Uyarı:** `\n` tuzağı (yama Write ile) · `rm -rf` yasak · sabotaj çapaları kod değişince kayar.

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
**25 Ağu yazısı** KAPSAM DIŞI · **Deneme**: BEŞLİ PAKET kapandı, Onur kilidi bekler.
🔒 **Tuzak Avcısı ölçüm fixture'ı DEĞİL (6 Eyl kilidi) — gerçek-proje regresyonu YALNIZ Momentum.**

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**P4** (O20, push edildi): karar adres defteri · **P4.1** (O21): Momentum 4/4 · **P5.4** (O19, push edildi): `not` bayat defterde H20 taze kümesi (`43a260d`/`aed4169`/`e7b2ae2`) · **P2.1** (O16): `adres` tembel kurulum·maske·atlama · **P2** (O15): 4 dil · **H14** (O14) · **P1** (O13) · **O10-O12:** K-DURUM·K-GECIS·K-ISARET·K-SATIR·K-YOL·K-BAYAT (H18/H19) · B1+B2 (H16).
**ÜRÜN HAZIRLIĞI** (30 Eyl, CI #117; K7 yok). **AÇIK:** büyük/küçük harf çakışan adlar · `name:` YAML ölçülmez · `--guncelle`+izin hatası boş yedek · DETERMİNİZM yalnız aynı makinede.

## Bilinen sınırlar (ölçülmüş)
- 🔴 `isir` exit 0 böl-kur'lu/devral'li projede ULAŞILAMAZ (5 Eki): `kapi --siki` bolum-kur başlıklarını BEYANSIZ sayar → M-H1s KURULAMADI → exit 2 (taban Momentum'da da). M-DEVIR ölçütü canlıda ÖNCEDEN `CAPA DEVRI` varken sabotajı GÖRMEZ · `.kilit` varken M-KILIT `isir`i öldürür.
- 🔴 `.gitkeep` sınırı (5 Eki): Win varsayılan klon (`autocrlf=true`, `.gitattributes` yok) `.gitkeep`'ten BAĞIMSIZ H0 KIRMIZI (`kur` yazmıyor) · `.gitignore` dizini yutarsa izlenmez · B2 mevcut projeyi onarmaz · `not/derle/karar` dizin yaratır, `.gitkeep` yazmaz (bilerek).
- 🔴 "GERÇEK ORTAMDA OLMAZ" DEMEDEN ÖNCE ORTAMI ÖLÇ (6 Eyl; M-Y2 macOS'ta tam oradaydı). POZİTİF KONTROLSÜZ DÜZELTME KAPANMIŞ SAYILMAZ. Push'u `git ls-remote` ölçer.
- 🔴 ÖLÇÜM ORTAMI HÜKMÜ ÇARPITIR (6 Eyl): root'ta `fazB_*`/`y4_mutant` SAHTE KIRMIZI ⇒ `olcum` kullanıcısıyla koş (WSL; Windows'ta `t_y42`/`readme_mutanti` KAPI-2 symlink 1314'ten çöker). Ağır doğrulama SOLO (paralel yük `isir`'i 300 sn aştırır).
- 🔴 `continue-on-error` TAŞIYAN YEŞİL KAPI DEĞİLDİR (4 Eyl). Talimat yalnız YAML yorumunda durursa iş emrine girmez. Bilinçli ÖLÇÜM işleri: `win_kill_probu` · `boru_probu` · `ortam` · `kalite` · `kanit`.
- 🔴 PAYLAŞILAN KURAL = PAYLAŞILAN KÖRLÜK (1 Eki): paket↔KAPI-2 AYNI süzgeçten türediği için `deneme_x` sızıntısını İKİSİ DE göremedi; KAPI-4 beklentisi README'den.
- 🔴 Aynı politika iki yerde = bayatlama (3 Eki): `oturum_sagligi` yalnız N basar, renk/eşik YALNIZ anayasada (ADR 2026-10-03).
- 🔴 KAPI NEYİ ÖLÇTÜĞÜNÜ ÖLÇEMEZ: VARLIK kapısı SAYIYI ölçmez · iki büyüklük EŞİTSE hangisi ölçüldü ÖLÇÜLEMEZ · YOL UZUNLUĞU BİR ÖLÇÜM EKSENİDİR.
- 🔴 ÖLÇÜM ALETİ DE YALAN SÖYLER: boru sonrası `$?` · uydurma `d[rol]` · argümansız araç · `stderr=STDOUT` · PAYLAŞILAN KUM HAVUZU · regex HAM BLOĞU okumaz · artefakt BOYUTU oracle DEĞİL ⇒ akış BİRLEŞTİRİLMEZ, HAM ÇIKTI okunur.
- 🔴 YENİ ÖLÇÜMÜN HATASI "FAZLA GEÇİRME" YÖNÜNDEYSE (30 Eyl): `paket` mini-YAML sayımı kırpılacak açıklamayı GEÇİRİYORDU; 12.000'lik rastgele PyYAML karşılaştırması olmadan kapanmış sayılmaz.
- 🔴 CI HÜKMÜ: API URL'ine navigasyon + `JSON.parse(innerText)`; sayfa başına 100 ⇒ `total_count` ile SAYFALA; hepsi `completed` olmadan SAYMA; 403/504 ⇒ bir kez YENİLE.
- 🔴 CI kırmızısı KAPI kırmızısı olmayabilir (#66). KAPININ SENARYOSU KAPIYI KIRMIZI YAKABİLİR ⇒ gerçek vakaya çevir.
- 🔴 ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR. ÇAPALARA BAKILMADAN KAPI GÖVDESİNE SATIR EKLENMEZ. `capraz.yml`'deki HER `run:` adımı push ÖNCESİ koşulur (liste YML'DEN TÜRETİLİR); tabanda da koş, yalnız FARK regresyondur. BELGE/YORUM da kapı kırar; ÇAPA ARACIN KENDİ ÇIKTISINDAN GÜNCELLENMEZ.
- 🔴 İŞ EMRİ KISITI EN BAŞA YAZILIR. Tarihi ÖLÇEN taraf yazar. YEŞİL CI ÖLÇÜLMEMİŞ ŞART olabilir (#45).
- 🔴 Defter COMMIT'lenmeden `kapi` KIRMIZI ([H9]); derleme artefaktı H14'ün DELİLİNİ bozar.
- 🔴 BAĞLI KLASÖRDE KOŞMAYANLAR: `hafiza.py` (H9 → kalıcı `.git/index.lock`) · `t_y42.py` (150 sn'de bitmiyor) ⇒ WSL `olcum`da koşulur.
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK · `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar · `readme_mutanti`/`paketten_kos` ANLAMI değil GEÇTİĞİNİ ölçer · kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- 🔴 `rmtree(ignore_errors=True)`: motorda 5 yer `_gecici_sil`e döndü (4 Eki); faz0'daki ~90 çağrı KAPSAM DIŞI — Win'de salt-okunur `.git` artığı bırakır.
- 🟡 H18 (5 Eki): yalnız `canli` · madde + `yol:N` · UYARI (exit değişmez) · içerik bayatlığını ÖLÇMEZ (`:85` TUTUYOR der) · kod çiti içi madde ayırt edilmez · `isir` kataloğunda DEĞİL.
- 🟡 P5-P5.3 (10-11 Eki): iddianın ANLAMI ölçülmez · DAMGASIZ geriye dönük damgalanmaz · ad 6+ tanımda damga YOK · iz YOL taşımaz · K1/K3 ad→dosya defterden (bayatta yeni tanım `not`'ta görünmez; H20 tazeler, tavan 100 dosya/8 MiB) · izlenmeyen dosya `adres` evreninde yok · kapi soğuk geçişi maliyetli (önbelleği ısıtmaz) · K3 ≤20 dosya/15 sn · N=5 · kanca YOK.
- 🔴 KESME (6 Eki, Onur kilidi): `karar-kaynagi` karar DİZİNİNE yol verir + her ADR'nin durumunu taşır; dizin DIŞI gerekçe dosyaları ve taslak/kilitli yorumu okuyucuya kalır · H19 yalnız ADI ölçer: "X'i ASLA okuma" kapıyı susturur.
- 🟡 P1 (6 Eki): sözlük dışı beyan SINIFLANAMADI'ya düşer; motor beyanın ANLAMINI ölçmez — `kabul` yazan taslak GECERLI görünür (`kabul edilmedi`/`not approved` dahil) · sınıf 60 kr GÖRÜNEN metinden.
- 🟡 K-YOL/K-GECIS (5-6 Eki): karar dizini `devral`da VEYA ilk fragman işleyen `derle`de (`""` bilinçli boş) · çok adayda İLK · `NNNN-*.md`/`ADR-*.md` · ≤40 ad · DIŞA bağlı dizin OKUNMAZ.
- 🟡 Y2 sınırı: başka başlığın ALTINA düşen yetim detay ayırt EDİLEMEZ. Y3: hook'lu `isir` iskeleti COMMIT'Lİ proje ister. Win'de yükte `sabotaj.py`nin `isir`i 300 sn aşar ⇒ solo koş; izole TEMP kısa yolda olmalı (260).

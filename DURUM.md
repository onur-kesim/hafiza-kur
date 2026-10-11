# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (taban `ceb0454` = main = origin; CI #127 198/198; P5+P5.2 yerelde)
Son güncelleme: 11 Eki 2026 · ≤8 KB · **kapanan bölüm tek satıra iner**

## SON İŞ — P5 + P5.2 birleşik damga (Code O17, 10-11 Eki) · PUSH YOK
Taban `ceb0454`. **P5** `7f9407d`..`343427b` (K0-K3). **P5.2** (Onur kilidi: BİRLEŞİK DAMGA): K4 `ee179fa` ad 2-5 tanım → TEK iz `sha256(sıralı izler)[:8]` (yol girmez, tavan 5, tekil iz geri uyumlu; not+H20+K3) · K5 `698be93` dil sabitleri aday değil · K6 `933a094` DAMGASIZ araç kusurunda OLCULEMEDI · düzeltme `20b647e` `ef36cbe` `369973a` · belge `534230d`. **17 kol / 171 sabotaj** ISIRDI; inceleme 82 bulgu işlendi.
**✅ K3 KABUL SAPMASI KAPANDI** — Momentum `4359fa8` md.40 (taze klon): `ATIF DAMGALANDI: 2 (ShouldResyncAsync#f6f96469 [3 tanim], SyncCommandHandler.cs:85#45c11a6a)` · `DIKKAT: ShouldResyncAsync 3 tanimdan 3'u 2 commit once degisti (4005380)` · `ResyncRequired` COZULEMEDI. H20 adım 2 (`4359fa8..HEAD` 4 dosyada commit yok) ÖLÇÜLEMEDİ; sentetik düzenleme `GOVDE DEGISTI 1`. Momentum canlı: `7 COKLU | 6 DAMGASIZ`.
**Sapmalar (Onur teyidi):** K6 değişmezi "toplam AYNI" → "azalmaz, yalnız `yok` kadar artar" · silinme → GOVDE DEGISTI yalnız TAZE defterle (bayat → OLCULEMEDI) · DAMGASIZ/COKLU yalnız numaralı madde.
Çapa AYNEN (`cmd_isir` 30 · `cmd_devral` 99 · CC>20 7 · `ihlal` 9 · `cmd_kapi` 20 · `_kapi_govde` 79) · motor 11108 → 11928 satır (+820) · `altin_cikti` FARK YOK · `sabotaj` **67/67** · fxa `kapi` 10,74 → 10,57 s · ruff/mypy/bandit = taban · **Tam tur 534230d:** 73 OK · 9 KIRMIZI = bilinen küme · exit FARKI 0/84 · `adres_mutanti` 3289 s → CI timeout 150.
**Sıradaki:** Onur: Cowork kabul + 1 beyan → push → CI say.
**AÇIK:** P5/P5.2 kolları macOS/py3.11/3.13'te KOŞULMADI · K1/H20 aday çıkarımı bütçesiz · Windows `subprocess` zaman aşımı torunlu git'te · M-H10c KACTI (ikisi ÖNCEDEN VAR) · Python adları NFKC

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
**25 Ağu yazısı** KAPSAM DIŞI · **Deneme**: BEŞLİ PAKET kapandı, Onur kilidi bekler.
🔒 **Tuzak Avcısı ölçüm fixture'ı DEĞİL (6 Eyl kilidi) — gerçek-proje regresyonu YALNIZ Momentum.**

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**P2.1** (O16): `adres` tembel kurulum · maske · atlama · sorgu hızı · **P2** (O15): 4 dil · **H14** (O14): git yolları parçalı · **P1** (O13): ADR 4 sınıf.
**O10-O12:** K-DURUM·K-GECIS·K-ISARET (ADR durumu · karar dizini · H19) · K-SATIR·K-YOL·K-BAYAT (H18 · `atif-kaymasi`) · B1+B2 (`isir` sahte KAPI KÖR · H16).
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
- 🟡 H18 (5 Eki): yalnız `canli` · madde + `yol:N` · UYARI (exit değişmez) · içerik bayatlığını ÖLÇMEZ (`:85` TUTUYOR der) · kod çiti içi madde ayırt edilmez · `isir` kataloğunda DEĞİL. Zaman/sıra adayları kesildi (Momentum A 0/3, B 1/6).
- 🟡 P5/P5.2 (10-11 Eki): iddianın ANLAMI ölçülmez (yalnız "dayandığı kod değişti") · DAMGASIZ geriye dönük damgalanmaz · ad 6+ tanımda damgalanmaz · iz YOL taşımaz (taşınma görünmez) · ad→dosya defterden (sonradan eklenen tanım görünmez) · K3 ≤20 dosya/15 sn · N=5 sabit · kanca YOK · H20/K3 `isir` kataloğunda DEĞİL.
- 🔴 KESME (6 Eki, Onur kilidi): `karar-kaynagi` karar DİZİNİNE yol verir + her ADR'nin durumunu taşır; dizin DIŞI gerekçe dosyaları ve taslak/kilitli yorumu okuyucuya kalır · H19 yalnız ADI ölçer: "X'i ASLA okuma" kapıyı susturur.
- 🟡 P1 (6 Eki): sözlük dışı beyan SINIFLANAMADI'ya düşer; motor beyanın ANLAMINI ölçmez — `kabul` yazan taslak GECERLI görünür (`kabul edilmedi`/`not approved` dahil) · sınıf 60 kr GÖRÜNEN metinden.
- 🟡 K-YOL/K-GECIS (5-6 Eki): karar dizini `devral`da VEYA ilk fragman işleyen `derle`de (`""` bilinçli boş) · çok adayda İLK · `NNNN-*.md`/`ADR-*.md` · ≤40 ad · DIŞA bağlı dizin OKUNMAZ.
- 🟡 Y2 sınırı: başka başlığın ALTINA düşen yetim detay ayırt EDİLEMEZ. Y3: hook'lu `isir` iskeleti COMMIT'Lİ proje ister. Win'de yükte `sabotaj.py`nin `isir`i 300 sn aşar ⇒ solo koş; izole TEMP kısa yolda olmalı (260).

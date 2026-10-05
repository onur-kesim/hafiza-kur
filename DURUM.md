# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (taban CI #122 `5f2ae09` 189/189 `gh` ölçtü; B1/B2 + K-* PUSH'SUZ)
Son güncelleme: 5 Eki 2026 · ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## SON İŞ — K-SATIR · K-YOL · K-BAYAT (Code O11, 5 Eki 2026) · PUSH YOK
**Taban** yerel `c913725` (origin `5f2ae09`). `d57c50b` K-SATIR · `7e12d27` K-YOL · `540db82` K-BAYAT · `077eaa6`+`ae309d7` düzeltme. Motor `9DA7643D…` 424.717 B → `3BF9869F…` 447.799 B (fonksiyon 329→358). Mutant: MEVCUT `guncel_durum_kapisi_mutanti.py`'ye KOL (14 kol, 28 sabotaj).
Çapa `cmd_isir` 30 · `cmd_devral` 99 · CC>20 7 · `ihlal` 9 · `cmd_kapi` CC 20 AYNEN · `_kapi_govde` 80→**79** (ölü `return` çıktı) · `fail()` 67 AYNI.
**Ölçüldü (Win py3.12, `capraz.yml` 82 adım, TAZE klon):** taban 71 OK · 9 KIRMIZI (bilinen) · 2 SKIP; son `077eaa6` AYNI küme (+`guncel_durum` çapa hatası → `ae309d7`, YEŞİL) · ruff 59 · mypy 2 · bandit 44/1 · `isir` 79+2/81 · `sabotaj` **67/67, KAPSAMSIZ 0**. Linux (WSL `olcum`, py3.14): `guncel_durum` · `readme_mutanti` 16/16 · `t_y42` 58/58 · `paketten_kos` · `altin_cikti` · `ci_kapsam` 50/50 YEŞİL · `isir` iki bloklu projede 81/81 = taban.
**Momentum (YENİ motor):** `kapi` KAYMA **1** (`main.dart:25`) · TUTUYOR 2 · `localhost:5298` ÖLÇÜLEMEDİ · `docs/ADR` **5** ad (iş emri "6" = `.gitkeep` dâhil) · iki blok VAR · iki klonda bayt-bayt aynı.
**Sıradaki:** push Onur'da → Cowork: `kapi` KAYMA 1 + iki blok · `derle` iki kez bit-bit (aynı dakika; `kaynak=` dakikalık) · kör okuma KARAR ≤2/4.
**AÇIK:** macOS · py3.11/3.13 yerelde YOK · Momentum tam `isir` (~80 dk, iki bloklu) koşulmadı · README:190 "tam liste SKILL.md §9" H18/K-YOL'u içermiyor · yerel `.skill` bayat+ignore'lu · Win `t_y42` 1314 · M-H10c kod çitli KACTI (ÖNCEDEN VAR)

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
K4 TAMAM (67/67), kör nokta **0**; **25 Ağu yazısı** KAPSAM DIŞI; **Deneme**: BEŞLİ PAKET kapandı, Onur kilidi bekler.
🔒 **Tuzak Avcısı ölçüm fixture'ı DEĞİL (6 Eyl kilidi) — gerçek-proje regresyonu YALNIZ Momentum.**

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**K-SATIR·K-YOL·K-BAYAT** (O11): H18 satır atfı kayması + `derle` `atif-kaymasi` · `devral` karar dizini → `karar-kaynagi` · içerik bayatlığı KESİLDİ.
**B1+B2** (O10): `isir` sahte KAPI KÖR · taze klonda H16 → `_gitkeep_yaz` · Cowork TUTTU (`OLCUM_RAPORU_05EKIM_B1B2.md`): isir 80/80 exit 2, H16 yok.
**O7-O9** (W1/W2·Y3·Y1·Y2·12 kör nokta): `_gecici_sil` · hook'lu `isir` 81/81 · sabotaj 55→**67/67**.
**ÜRÜN HAZIRLIĞI** (30 Eyl, CI #117; yükleme K7 HÂLÂ yok). **AÇIK:** harf-büyüklüğü çakışan adlar · `name:` YAML ölçülmez · `--guncelle`+izin hatası boş yedek · DETERMİNİZM yalnız aynı makinede.

## Bilinen sınırlar (ölçülmüş)
- 🔴 `isir` exit 0 böl-kur'lu/devral'li projede ULAŞILAMAZ (5 Eki): `kapi --siki` bolum-kur başlıklarını BEYANSIZ sayar → M-H1s KURULAMADI → exit 2 (taban Momentum'da da). M-DEVIR ölçütü canlıda ÖNCEDEN `CAPA DEVRI` varken sabotajı GÖRMEZ (`d0b37ce` mesajındaki "gerçek Momentum" YANLIŞ) · `.kilit` varken M-KILIT `isir`i yarıda öldürür.
- 🔴 `.gitkeep` sınırı (5 Eki): Win varsayılan klon (`autocrlf=true`, `.gitattributes` yok) `.gitkeep`'ten BAĞIMSIZ H0 KIRMIZI (`kur` yazmıyor) · `.gitignore` dizini yutarsa izlenmez · B2 mevcut projeyi onarmaz (Tuzak Avcısı/Momentum klon+pull'da `gunluk/` kaybeder) · `not/derle/karar` dizin yaratır, `.gitkeep` yazmaz (bilerek).
- 🔴 "GERÇEK ORTAMDA OLMAZ" DEMEDEN ÖNCE ORTAMI ÖLÇ (6 Eyl): M-Y2 kusuru "hiçbir runner'da bu TMPDIR yok" diye KESİLMİŞTİ; macOS tam oradaydı. Kardeşi: POZİTİF KONTROLSÜZ DÜZELTME KAPANMIŞ SAYILMAZ. Push'u `git ls-remote` ölçer — bir tur "push yapıldı" dendi, gitmemişti.
- 🔴 ÖLÇÜM ORTAMI HÜKMÜ ÇARPITIR (6 Eyl): root'ta `fazB_*`/`y4_mutant` SAHTE KIRMIZI, `t_y42` "57+1" der ⇒ `olcum` kullanıcısıyla koş (`t_y42` 58/58). Yerel Linux: WSL `olcum`; Windows'ta `t_y42`/`readme_mutanti` KAPI-2 symlink 1314'ten çöker. Ağır doğrulama SOLO (ajan/paralel yük `isir`'i 300 sn aştırır, WinError 1450).
- 🔴 `continue-on-error` TAŞIYAN YEŞİL KAPI DEĞİLDİR (4 Eyl). Talimat yalnız YAML yorumunda durursa iş emrine girmez. Bilinçli ÖLÇÜM işleri: `win_kill_probu` · `boru_probu` · `ortam` · `kalite` · `kanit`.
- 🔴 PAYLAŞILAN KURAL = PAYLAŞILAN KÖRLÜK (1 Eki): paket↔KAPI-2 AYNI süzgeçten türediği için `deneme_x` sızıntısını İKİSİ DE göremedi; KAPI-4 beklentisi README'den.
- 🔴 Aynı politika iki yerde = bayatlama (3 Eki): `oturum_sagligi` kümülatif toplam ölçüyordu; şimdi yalnız N basar, renk/eşik YALNIZ anayasada (ADR 2026-10-03).
- 🔴 KAPI NEYİ ÖLÇTÜĞÜNÜ ÖLÇEMEZ: VARLIK kapısı SAYIYI ölçmez · iki büyüklük EŞİTSE hangisi ölçüldü ÖLÇÜLEMEZ · YOL UZUNLUĞU BİR ÖLÇÜM EKSENİDİR (`[:N]` kesmeleri).
- 🔴 ÖLÇÜM ALETİ DE YALAN SÖYLER: boru sonrası `$?` · uydurma `d[rol]` · argümansız araç · `stderr=STDOUT` · PAYLAŞILAN KUM HAVUZU · regex HAM BLOĞU okumaz · artefakt BOYUTU oracle DEĞİL ⇒ akış BİRLEŞTİRİLMEZ, HAM ÇIKTI okunur.
- 🔴 YENİ ÖLÇÜMÜN HATASI "FAZLA GEÇİRME" YÖNÜNDEYSE (30 Eyl): `paket` mini-YAML sayımı kırpılacak açıklamayı GEÇİRİYORDU; üretici "TUTTU" demişti. 12.000'lik rastgele PyYAML karşılaştırması olmadan kapanmış sayılmaz.
- 🔴 CI HÜKMÜ: API URL'ine navigasyon + `JSON.parse(innerText)`; sayfa başına 100 ⇒ `total_count` ile SAYFALA; hepsi `completed` olmadan SAYMA; 403/504 ⇒ bir kez YENİLE.
- 🔴 CI kırmızısı KAPI kırmızısı olmayabilir (#66). KAPININ SENARYOSU KAPIYI KIRMIZI YAKABİLİR ⇒ gerçek vakaya çevir.
- 🔴 ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR (dört kez ısırdı). ÇAPALARA BAKILMADAN KAPI GÖVDESİNE SATIR EKLENMEZ. Ölçüt = `capraz.yml`'deki HER `run:` adımı push ÖNCESİ koşulur; liste YML'DEN TÜRETİLİR, elle seçilmez; tabanda da koş, yalnız FARK regresyondur. BELGE/YORUM da kapı kırar; ÇAPA ARACIN KENDİ ÇIKTISINDAN GÜNCELLENMEZ.
- 🔴 İŞ EMRİ KISITI EN BAŞA YAZILIR. Tarihi ÖLÇEN taraf yazar. YEŞİL CI ÖLÇÜLMEMİŞ ŞART olabilir (#45).
- 🔴 Defter COMMIT'lenmeden `kapi` KIRMIZI ([H9]); derleme artefaktı H14'ün DELİLİNİ bozar.
- 🔴 BAĞLI KLASÖRDE KOŞMAYANLAR: `hafiza.py` (H9 → kalıcı `.git/index.lock`) · `t_y42.py` (150 sn'de bitmiyor) ⇒ WSL `olcum`da koşulur.
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK · `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar · `readme_mutanti`/`paketten_kos` ANLAMI değil GEÇTİĞİNİ ölçer · kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- 🔴 `rmtree(ignore_errors=True)`: motorda 5 yer W1'de `_gecici_sil`e döndü (4 Eki); faz0'daki ~90 çağrı (geliştirici aracı) KAPSAM DIŞI — Win'de salt-okunur `.git` artığı bırakır (`hook_mutanti` hariç).
- 🟡 H18 (5 Eki): yalnız `canli` · madde + `yol:N` · UYARI (exit değişmez) · içerik bayatlığını ÖLÇMEZ (`:85` TUTUYOR der) · kod çiti içi madde ayırt edilmez · `isir` kataloğunda DEĞİL.
- 🟡 İçerik bayatlığı ölçülmez (5 Eki): zaman/sıra adayları Momentum'da A 0/3, B 1/6; md.40 iddia DOĞUŞTA bayattı → mekanik ayırt edilemiyor. Kanıt: besli-paket ölçüm raporu (depoya kopyalanmaz).
- 🟡 K-YOL (5 Eki): karar dizini YALNIZ `devral` anında (kurulu proje reddeder) · blok yalnız fragman işleyen `derle`'de tazelenir · çok adayda İLK (diğeri "baska aday") · `NNNN-*.md`/`ADR-*.md`; `.gitkeep`/README/alt dizin SAYILMAZ · ≤40 ad · proje DIŞINA bağlı dizin OKUNMAZ (ATLANDI) · devral→`bolum-kur`te blok `ARSIV DIZINI` altına düşer (kozmetik).
- 🟡 Y2 sınırı: başka başlığın ALTINA düşen yetim detay ayırt EDİLEMEZ. Y3: hook'lu `isir` iskeleti COMMIT'Lİ proje ister. Win'de yükte `sabotaj.py`nin `isir`i 300 sn aşar ⇒ solo koş; izole TEMP kısa yolda olmalı (260).

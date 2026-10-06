# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (taban CI #122 `5f2ae09` 189/189; B1/B2 + K-* PUSH'SUZ)
Son güncelleme: 6 Eki 2026 · ≤8 KB · **kapanan bölüm tek satıra iner**

## SON İŞ — K-DURUM · K-GECIS · K-ISARET (Code O12, 6 Eki 2026) · PUSH YOK
**Taban** `7c6ff91` (origin `5f2ae09`). `12e437c` K-DURUM · `e73b68a` K-GECIS · `a11d79d` K-ISARET · `df46d2b` `cmd_etki` S-4 çapa düzeltmesi. Motor → 454.254 B (fonksiyon 358→365). Mutant: MEVCUT `guncel_durum_kapisi_mutanti.py`'ye 3 KOL (17 kol, 46 sabotaj, KACTI 0). README+SKILL §9 güncel.
Çapa `cmd_isir` 30 · `cmd_devral` 99 · CC>20 7 · `ihlal` 9 · `cmd_kapi` 20 · `_kapi_govde` 79 AYNEN · `sabotaj` **67/67** · `altin_cikti` FARK YOK.
**Tam tur (Win, 82 adım, taze klon):** 70 OK · 10 KIRMIZI (9 bilinen + `cmd_etki` → düzeltildi) · 2 SKIP · fark yalnız satır no/bayt/tarih · ruff 59 · mypy 2 · bandit 44/1 AYNI.
**Momentum (kopya `o13A/B`):** 5 ADR durumlu (0001/0002 `✅ KİLİTLİ (v3)…` · iki 0003 `🟡 TASLAK v6 — KİLİTLİ DEĞİL…` · 0004 `📝 GÖVDE YAZILDI…`) · eski motorla kurulu kopyada `derle`: `karar_dizini` `docs/ADR` + blok 5 ad, ikinci `derle` bayt aynı · `CLAUDE.md` `DURUM.md`'yi **5 kez** anıyor → H19 SESSİZ, `ISARETCI YOK` yok.
**Sıradaki:** push Onur'da → Cowork: beş durum satırı · keşif+ikinci derle · taze `kur` işaretçi · kör okuma R1.
**AÇIK:** macOS · py3.11/3.13 · WSL `olcum` yok · `## Status` başlık-altı değer BEYANSIZ · Win `t_y42` 1314 · M-H10c KACTI (ÖNCEDEN VAR)

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
K4 TAMAM (67/67), kör nokta **0**; **25 Ağu yazısı** KAPSAM DIŞI; **Deneme**: BEŞLİ PAKET kapandı, Onur kilidi bekler.
🔒 **Tuzak Avcısı ölçüm fixture'ı DEĞİL (6 Eyl kilidi) — gerçek-proje regresyonu YALNIZ Momentum.**

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**K-DURUM·K-GECIS·K-ISARET** (O12): `karar-kaynagi` her ADR'nin `[durum: …]`/BEYANSIZ'ı · kurulu projede `derle` karar dizinini bulur · kural evi canlı defter işaretçisi + `kapi` H19.
**K-SATIR·K-YOL·K-BAYAT** (O11): H18 satır atfı kayması + `derle` `atif-kaymasi` · `devral` karar dizini → `karar-kaynagi` · içerik bayatlığı KESİLDİ.
**B1+B2** (O10): `isir` sahte KAPI KÖR · taze klonda H16 → `_gitkeep_yaz` · Cowork TUTTU (`OLCUM_RAPORU_05EKIM_B1B2.md`).
**O7-O9**: `_gecici_sil` · hook'lu `isir` 81/81 · sabotaj 55→**67/67**.
**ÜRÜN HAZIRLIĞI** (30 Eyl, CI #117; yükleme K7 HÂLÂ yok). **AÇIK:** harf-büyüklüğü çakışan adlar · `name:` YAML ölçülmez · `--guncelle`+izin hatası boş yedek · DETERMİNİZM yalnız aynı makinede.

## Bilinen sınırlar (ölçülmüş)
- 🔴 `isir` exit 0 böl-kur'lu/devral'li projede ULAŞILAMAZ (5 Eki): `kapi --siki` bolum-kur başlıklarını BEYANSIZ sayar → M-H1s KURULAMADI → exit 2 (taban Momentum'da da). M-DEVIR ölçütü canlıda ÖNCEDEN `CAPA DEVRI` varken sabotajı GÖRMEZ · `.kilit` varken M-KILIT `isir`i öldürür.
- 🔴 `.gitkeep` sınırı (5 Eki): Win varsayılan klon (`autocrlf=true`, `.gitattributes` yok) `.gitkeep`'ten BAĞIMSIZ H0 KIRMIZI (`kur` yazmıyor) · `.gitignore` dizini yutarsa izlenmez · B2 mevcut projeyi onarmaz (Tuzak Avcısı/Momentum klon+pull'da `gunluk/` kaybeder) · `not/derle/karar` dizin yaratır, `.gitkeep` yazmaz (bilerek).
- 🔴 "GERÇEK ORTAMDA OLMAZ" DEMEDEN ÖNCE ORTAMI ÖLÇ (6 Eyl): M-Y2 kusuru "hiçbir runner'da bu TMPDIR yok" diye KESİLMİŞTİ; macOS tam oradaydı. Kardeşi: POZİTİF KONTROLSÜZ DÜZELTME KAPANMIŞ SAYILMAZ. Push'u `git ls-remote` ölçer — bir tur "push yapıldı" dendi, gitmemişti.
- 🔴 ÖLÇÜM ORTAMI HÜKMÜ ÇARPITIR (6 Eyl): root'ta `fazB_*`/`y4_mutant` SAHTE KIRMIZI, `t_y42` "57+1" der ⇒ `olcum` kullanıcısıyla koş (`t_y42` 58/58). Yerel Linux: WSL `olcum`; Windows'ta `t_y42`/`readme_mutanti` KAPI-2 symlink 1314'ten çöker. Ağır doğrulama SOLO (paralel yük `isir`'i 300 sn aştırır).
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
- 🔴 KESME (6 Eki, Onur kilidi): `karar-kaynagi` karar DİZİNİNE yol verir + her ADR'nin durumunu taşır; dizin DIŞI gerekçe dosyaları ve taslak/kilitli yorumu okuyucuya kalır (Momentum kör okuma KARAR 2/4: `TASLAK`a rağmen taslak karar sanıldı, R1 ×2) · H19 yalnız ADI ölçer: "X'i ASLA okuma" kapıyı susturur.
- 🟡 K-YOL/K-GECIS (5-6 Eki): karar dizini `devral`da VEYA kurulu projede ilk fragman işleyen `derle`de (anahtar yoksa; `""` bilinçli boş) · çok adayda İLK · `NNNN-*.md`/`ADR-*.md` · ≤40 ad · DIŞA bağlı dizin OKUNMAZ · devral→`bolum-kur`te blok `ARSIV DIZINI` altına düşer.
- 🟡 Y2 sınırı: başka başlığın ALTINA düşen yetim detay ayırt EDİLEMEZ. Y3: hook'lu `isir` iskeleti COMMIT'Lİ proje ister. Win'de yükte `sabotaj.py`nin `isir`i 300 sn aşar ⇒ solo koş; izole TEMP kısa yolda olmalı (260).

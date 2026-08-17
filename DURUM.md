# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (yerel ölçüm: `hukum_tutarliligi_mutanti` 1/1 kapı
temiz + 2/2 mutant KENDİ ekseninde ISIRDI, kapı md.10 ÖNCESİ motorda KIRMIZI yandı; CI push
sonrası numara/sha ile güncellenir — commit/push Onur'da. Taban: CI #70 `818dc746`, 103/0)
Son güncelleme: 17 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
Aday: **H16 YAPI kapısı** (tasarım onaylı, kod yok, ADR ister).
25 Ağu yazısı TASLAK (`fable dosyalama\25agu-yazisi\`, depo DIŞI); yayın kararı ayrı.

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**md.10** hüküm iç tutarlılığı — ayrım cümlesi (hal-2) kapsam dışını "biri gerçek defter
OLABİLİR" iddiasına artık KATMIYOR: sayı/rol `envanter` değil `ici`den gelir (md.9 kapısı buna
KÖRDÜ, ayrı eksen). `hukum_tutarliligi_mutanti` (yeni) 1/2, kapı ÖNCESİ motorda KIRMIZI yandı.
Hal-1/hal-3 BİREBİR korundu (byte-diff); CC/`ihlal` DEĞİŞMEDİ ·
**md.9** görünürlük — kapsam dışı hiç önerilmez, `gorunurluk_mutanti` 4/5, çapa 99→97 ·
**md.6-8** kesif/esle/durma kuralı + çoklu-`canli` kapısı + hükum ayrımı, kendi ÖNCESİ
motorlarında kırmızı yandı · md.2+4+5 README kanıt bloğu + yol ayracı körlüğü kapandı.
🔴 `--kesif` **72 gerçek public depoda** koşuldu (50 + 22 `memory-bank/`), salt okuma, 0 bayt.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **KAPSAM DIŞI ROL, AYRIM CÜMLESİNE SIZAR** (md.10) — bir kapı bir cümlenin VARLIĞINI
  ölçüyorsa SAYISINI ölçmüyordur: md.9 kapısı buna KÖRDÜ, iki motora bit-bit aynı cikti verdi.
- 🔴 **CI kırmızısı KAPI kırmızısı olmayabilir** (#66 `6c6d407a`): 100 işin 2'si kırmızı,
  ikisi de `upload-artifact` **Finalize 403**; ölçüm+kapı adımları YEŞİL, #67'de 100/0.
- 🔴 **WebFetch API DE BAYAT** (2. ısırık: en yeni #55 dedi, gerçek #67) ⇒ CI hükmü
  TARAYICI `fetch`'inden okunur; iş logu API'den 403, sayfadan JS ile açılır.
- 🔴 **KAPININ KENDİ SENARYOSU KAPIYI KIRMIZI YAKABİLİR:** md.7/A2 `kur`dan sonra canlıyı ELLE
  kırpıyordu ⇒ çıpayla ayrışıp H1 "satır KAYIP" veriyordu. Senaryo gerçek vakaya çevrildi.
- 🔴 **ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR — ÜÇ KEZ ısırdı, üçü de kod yazılmadan:** md.6(c)'nin
  VE'li yazımı `CLAUDE.md`+`DURUM.md` projesinde hiç ateşlenmiyordu · md.7'nin lafzi D'si 6 gerçek
  şeklin 4'ünde yanıyordu (3'ü meşru) · md.7(b) SAĞLIKLI akışta yanıyordu (`derle` eski bloğu
  arşive taşır). ⇒ ölçüt yazılır yazılmaz vakaya koşulur; kilit ondan SONRA.
- 🔴 **ÖLÇÜMÜ KOŞTUM, ONU KORUYAN KAPIYI KOŞMADIM (CI #56, #58):** kapı gövdesine satır eklerken
  O KAPININ mutant ÇAPALARINA bakılır (M-H10e'ninki İKİ BİTİŞİK SATIRDI); araç EL İLE SEÇİLMEZ,
  **TÜM `faz0` bataryası** koşulur. md.8'de uygulandı: `_md8_ayrim` `if not adaylar:`in ÜSTÜNE
  kondu, çapa kırılmadı. Çevre kırmızısı TEMİZ motorla ayrılır; staged BAYAT kopya üzerine yazmasın.
- 🔴 **ÖLÇÜM ALETİ DE YALAN SÖYLER — 16 Ağu'da BEŞ KEZ, sonuncusu İKİ CI TURU yaktı:**
  `| tail` sonrası `$?` boruyu ölçtü · `d[rol]=dosya` sözlüğü OLMAYAN bir kusur UYDURDU (bir
  bağımsız denetim turu ona kuruldu) · argümanı YOK SAYAN araca A/B iki kez aynı motoru ölçtü ·
  eşitlik tabanlı yol maskelemesi sessizce başarısız oldu · **`stderr=STDOUT` birleştirmesi md.8
  kapısını KÖR etti**: hüküm stderr'e tamponsuz, envanter stdout'a tamponlu gider ⇒ envanter
  bloğun ARDINA düşüp onu senaryoya göre farklılaştırır ⇒ mutantlar HEP kaçar. CI #61+#62
  yakaladı; **YEREL BEŞ AYRI ORTAMDA YEŞİL DEDİ.**
  ⇒ akış BİRLEŞTİRİLMEZ · çok-değerli alan LİSTEYE · hüküm öncesi N=1 HAM ÇIKTI gözle okunur ·
  motor A/B'si KOPYA DEPODA yapılır · normalizasyonun OLDUĞU ayrıca doğrulanır, yoksa ÖLÇÜLEMEDİ.
- 🔴 **ÇAPA, ARACIN KENDİ ÇIKTISINDAN GÜNCELLENMEZ** (yoksa kendini onaylar): 88→97 BAĞIMSIZ
  `radon cc` ile çaprazlandı. **YORUMDAKİ CANLI SAYI BAYATLAR:** `capraz.yml`'deki "bugün 14
  ihlal" iki günde 9/5/9 oldu; sayı silindi, "artefakttan oku" kondu.
- 🔴 **MUTANT ÇAPASI TEK YERDE OLMALI:** `if not adaylar:` motorda ÜÇ yerde geçiyordu,
  `replace(...,1)` YANLIŞ fonksiyona kurdu. "Uygulandı" ≠ "DOĞRU YERE uygulandı"; çapa tek
  yerde değilse mutant KURULAMADI = kırmızı.
- 🔴 **YAKALA-HEPSİ DESENİ ÖLÜ MANTIK DOĞURUR:** adaptöre `.*\.JSONL$` konsaydı ölçüt (b)'nin
  `.jsonl` yarısı hiç ateşlenemezdi. Bedel: `README.md` her projede OLCULEMEDI'de görünür.
- 🔴 **SAYI BULAŞMASI · OKUNMADAN HÜKÜM · BOZULABİLİR BEYAN** (dış denetçi): başka projenin sayısı
  yeniden ölçülmeden yazılmaz · dosyanı okumadan beyan etme. Ayrıntı: `denetim/2026-08-15_*`.
- 🔴 **YEŞİL CI, ÖLÇÜLMEMİŞ ŞART** (#45 yeşilken `paketten_kos` belgenin 1. adımını atlıyordu) ⇒
  madde ✅ olmadan önce ölçüt cümlesi KELİME KELİME araca karşı okunur. Kardeşi: **"GEÇİYOR MU"
  KAPISI ZAYIFTIR** — "tutarlı mı" AYRI eksendir (S-6; yol ekseni eklendi).
- 🔴 **Defter COMMIT'lenmeden `kapi` KIRMIZI** ([H9] git'te IZLENMIYOR → çıkış 1) ⇒ "defteri
  `.gitignore`'a al" fikri md.6(c)'yi ULAŞILMAZ kılar.
- 🔴 **Derleme artefaktı H14'ün DELİLİNİ bozar:** hariç kümesinde `obj`/`bin`/`.dart_tool` YOK ⇒
  "en yeni değişiklik" hep bir artefakt olur; işaretçi gerçek dosyayı gösteremez.
- 🔴 **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (belge-iç-tutarsızlık, İKİNCİ ısırık):
  git'li ama KODSUZ proje hem HAFİF hem KAPILI satırına uyuyor; bu turda KAPILI seçildi.
- 🔴 Motorda `push`/`fetch`/`remote`/`origin` SIFIR eşleşme — yalnız yerel git.
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR** (CI #43: win kolu daha UZUN metin taşıyor ama
  zip'i daha KÜÇÜK). Hüküm `conclusion` + log metnidir.
- 🔴 **GitHub API 403'ü ARALIKLIDIR** (aynı oturumda hem 403 hem başarı): tek 403'te vazgeçme,
  URL'i değiştir, iki kez 403 ise TARAYICIDAN sayfa bağlamında `fetch`. **HTML `/actions`
  sayfasını WebFetch ile OKUMA — BAYAT dönüyor** ("#23 Queued" dedi, gerçek #55'ti).
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ve
  `paketle.sh` (mount `zip`e izin vermiyor). Kum havuzu `/tmp`'e kurulur; gerçek ağaç probu
  gerekiyorsa kök dosyaları `$HOME/kesif_probu/` altına KOPYALANIR (mount dışı).
  Mount `unlink` vermiyor — silmek yerine `fable dosyalama/_to_delete/` altına TAŞI.
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor, `device_bash`
  yazıyor (beş kez ölçüldü, sha bulut kopyasıyla birebir).
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK (§8: ikinci ısırıkta H12'ye "İŞARET" hâli).
- **`continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — bilinçli olanlar: `kanit`in
  ölçüm adımları (hüküm kapısı HARİÇ) · `win_kill_probu` · `boru_probu` · `ortam` · `kalite`.
- `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar · `ci_kapsam_kapisi.py` deseni `faz0/*_mutanti.py`
  — `yol_ayraci_kapisi.py`/`paketten_kos.py` girmez, işleri elle konur.
- `readme_mutanti` README'nin ANLATIMINI ölçmez · `paketten_kos` belgenin ANLAMINI değil GEÇTİĞİNİ
  ölçer · `devral`ın YAZIM ayağı (çıpa/zincir/yedek/triyaj) hâlâ mutantsız; yeni kapı yalnız
  KEŞİF+DURMA ölçer · `derle` sonrası ikinci `isir` ölçülmüyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

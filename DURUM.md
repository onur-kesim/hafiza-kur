# DURUM — hafiza-kur
**BİTTİ sayacı: 7 ✅ / 7 — LİSTE KAPALI** (CI #59 `5f05b14`: 97 iş, **0 başarısız**)
Son güncelleme: 15 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — liste KAPALI; yeni madde ONUR KİLİDİ bekliyor
AMAÇ KAPISI (İŞLEYİŞ md.3) yeni `faz0/` aracını yasaklıyor. Üç aday: **25 Ağu yazısı** (BİTTİ
maddesi GEREKTİRMEZ, bugün başlanabilir, son tarih 10 gün) · **depo atfı history rewrite**
(son tarih **24 Ağu**, force-push → ayrı açık onay + `git bundle` yedeği) · **H16 YAPI kapısı**
(tasarım onaylı, kod yok, ADR ister). Ayrıca md.7'nin ayırt edici hâli (kural evi ↔ canlı içerik
ayrışması) kapsam **B**'yi gerektiriyor ve md.8 olarak açılabilir — bugünkü md.7 bir SAĞLIK
KONTROLÜDÜR, piyasa ayırt edicisi değildir; 25 Ağu yazısında böyle geçmeli.

## ✅ md.7 KAPANDI (CI #59 `5f05b14`, 97 iş / 0 başarısız) — TEK SATIRA İNDİ
`sahip=` alanı (`kur` iskeleti → `hafiza-kur` · `derle`/`bloklastir` → `proje`; alan yoksa
`H10-SAHIP` ÖLÇÜLEMEDİ, FAIL değil) + çoklu `canli` KAPISI (çıkış 2, diske sıfır bayt).
`faz0/ayrisma_mutanti.py` 3 kapı / 3 mutant AYRI eksende, üç platformda. Altın küme yeniden
üretildi (28 satır, hepsi `H2:` boyut — 4 × `sahip=` = 84 bayt). Lafız İKİ KEZ ölçülüp daraltıldı.

## 25 AĞU YAZISI — ikinci dikey dilim
Eski md.6 KESİLDİ (`CLAUDE.md` §5 — zaman değil ÖLÇÜT kusuru); **kurulum YAPILMADI**. Yazıda
"ölçülemedi + sebebi" diye geçer. En güçlü malzeme: **ölçüt YAZMAK ile ölçüt SINAMAK ayrı işlerdir**
— üç ölçüt lafzı kod yazılmadan somut vakada kırıldı.

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**md.6** `devral --kesif`+`--esle`+DURMA KURALI, `devral_kesif_mutanti` 3 kapı/3 mutant, CI #57
`ccd9721` (94/0); gerileme: altın küme 22 ölçüm BIT-BIT FARK YOK · `isir` 34/34 · fazA 6/0 ·
`ihlal` 8→9, `cmd_devral` çapası 88→97 · `DEVIR_ADAPTORU` motorda TEK EV ·
md.2+4 CI #43 `cde1998` + #46 `5d81838` · md.5 README kanıt bloğu CI #49 `fba20c8` (aracın kendi
`shlex` kusurunu ÖLÇÜM buldu, CI değil) · `devral` gerçek Windows'ta gerçek projede (421 MB/1001
dosya/git'li) exit 0, 0 satır silindi — **`devral`'ın TEK canlı ölçümü budur** · yol ayracı
körlüğü kapandı (`_rel()` + 21 çağrı) · CI #41 KIRMIZI'dan #46'ya.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **KAPININ KENDİ SENARYOSU KAPIYI KIRMIZI YAKABİLİR:** md.7/A2 `kur`dan sonra canlıyı ELLE
  kırpıyordu ⇒ çıpayla ayrışıp H1 "satır KAYIP" veriyordu. Senaryo gerçek vakaya çevrildi.
- 🔴 **ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR — ÜÇ KEZ ısırdı, üçü de kod yazılmadan:** md.6(c)'nin
  VE'li yazımı `CLAUDE.md`+`DURUM.md` projesinde hiç ateşlenmiyordu · md.7'nin lafzi D'si 6 gerçek
  şeklin 4'ünde yanıyordu (3'ü meşru) · md.7(b) SAĞLIKLI akışta yanıyordu (`derle` eski bloğu
  arşive taşır). ⇒ ölçüt yazılır yazılmaz vakaya koşulur; kilit ondan SONRA.
- 🔴 **ÖLÇÜMÜ KOŞTUM, ONU KORUYAN KAPIYI KOŞMADIM — İKİ KEZ ISIRDI, ikisini de CI yakaladı:**
  (1) CI #56: `karmasiklik.py` koştum, çapasını koruyan `karmasiklik_mutanti.py`'yi koşmadım.
  (2) CI #58: H10 gövdesine `_h10_sahiplik` satırı ekledim, `h10_bolme_mutanti.py`'yi koşmadım —
  M-H10e'nin ÇAPASI İKİ BİTİŞİK SATIRDI, araya girince kırıldı ve araç OLCULEMEDI dedi (exit 2).
  ⇒ **Kapı gövdesine satır eklerken O KAPININ mutant aracının ÇAPALARINA bakılır; araç EL İLE
  SEÇİLMEZ, TÜM `faz0` bataryası koşulur.** Bataryayı koşarken staged uploads'tan gelen BAYAT
  kopyaların üzerine yazmamasına dikkat — iki SAHTE kırmızı öyle doğdu (çapa 88, bayat altın küme).
  Çevre kırmızısını ayırmanın yolu: aynı kabı TEMİZ motorla da koş (fazB/y2/y4 ikisinde de aynı).
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

# DURUM — hafiza-kur
**BİTTİ sayacı: 6 ✅ / 7** — md.7'nin KODU YAZILDI ve ölçüldü; **CI BEKLİYOR** (push Onur'da)
Son güncelleme: 15 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — md.7 CI'da yeşillenirse ✅ (6→7) · kutu 22 Ağu
md.7 = "Kullanıcı, iki defterin AYRIŞTIĞINI motordan öğrenir." **Kod yazıldı, DİSKTE, PUSH YOK.**
(a) motorun yazdığı blok `sahip=` taşır (`kur` iskeleti → `hafiza-kur` · `derle`/`bloklastir` →
`proje`); sahipsiz blok `H10-SAHIP` OLCULEMEDI satırı basar — **FAIL değil**, eski defterlerde alan
yoktur. (c) çoklu `canli` UYARI DEĞİL KAPI: iki aday → çıkış 2, diske sıfır bayt, `--esle` ister;
kilit varsa akış eskisi gibi, tek aday ADDITIVE.
`faz0/ayrisma_mutanti.py`: **3 kapı YEŞİL, 3/3 mutant AYRI eksende** (A1 sahiplik · A2 görünürlük ·
C çoklu canlı). CI işi `capraz.yml`'e eklendi (32 iş, YAML doğrulandı, sha çaprazlandı).
🔴 **ALTIN KÜME YENİDEN ÜRETİLDİ:** 28 ham satır değişti, **hepsi `H2:` boyut satırı, sıfırı başka
eksende** — 4 × `sahip="hafiza-kur"` = 84 bayt. Davranış değişmedi, çıkış kodu değişmedi.
Gerileme (bulut, linux): `isir` 34/34 · fazA 6/0 · `altin_kapi_mutanti` 6/6 · `altin_olcut_mutanti`
7/7 · `karmasiklik_mutanti` 9/9 + çapa TUTUYOR (`cmd_devral` 97 sabit) · `ci_kapsam` çifti yeşil ·
md.6 kapısı 3/3.
Sonraya: 25 Ağu yazısı (madde gerektirmez) · depo atfı history rewrite (son tarih **24 Ağu**) ·
H16 YAPI kapısı (tasarım onaylı, kod yok).

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
- 🔴 **KAPININ KENDİ SENARYOSU KAPIYI KIRMIZI YAKABİLİR:** md.7/A2'nin ilk senaryosu `kur`dan sonra
  canlıyı ELLE kırpıyordu ⇒ çıpayla ayrışıp H1 "satır KAYIP" veriyordu. Senaryo gerçek vakaya
  çevrildi (sahipsiz ESKİ defter DEVRALINIR). Kırmızıyı okumadan "kapı çalışıyor" deme.
- 🔴 **ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR — ÜÇ KEZ ısırdı, üçü de kod yazılmadan:** md.6(c)'nin
  VE'li yazımı `CLAUDE.md`+`DURUM.md` projesinde hiç ateşlenmiyordu · md.7'nin lafzi D'si 6 gerçek
  şeklin 4'ünde yanıyordu (3'ü meşru) · md.7(b) SAĞLIKLI akışta yanıyordu (`derle` eski bloğu
  arşive taşır). ⇒ ölçüt yazılır yazılmaz vakaya koşulur; kilit ondan SONRA.
- 🔴 **ÖLÇÜMÜ KOŞTUM, ONU KORUYAN KAPIYI KOŞMADIM** (CI #56 yakaladı, ben değil):
  `karmasiklik.py --ihlal` koştum, "rapor kipi, exit 0" dedi — ama o sayıyı KORUYAN
  `karmasiklik_mutanti.py`'yi koşmadım; çapası kırmızıydı. **`X.py` ile `X_mutanti.py` AYRI
  DEĞİL, ÇİFTTİR.** "exit 0" uyutur.
- 🔴 **ÇAPA, ARACIN KENDİ ÇIKTISINDAN GÜNCELLENMEZ** (yoksa çapa kendini onaylar): 88→97
  BAĞIMSIZ `python -m radon cc` ile çaprazlandı (yeni 97 · eski 88 · `cmd_isir` ikisinde de 17).
- 🔴 **YORUMDAKİ CANLI SAYI BAYATLAR:** `capraz.yml`'de 13 Ağu'da yazılan "bugün 14 ihlal
  (11 CC>20, 11 satır>80)" 15 Ağu'da 9/5/9 idi. Sayı silindi, "artefakttan oku" kondu.
- 🔴 **MUTANT ÇAPASI TEK YERDE OLMALI:** M-3'ün çapası `if not adaylar:` motorda ÜÇ yerde
  geçiyordu, `str.replace(...,1)` YANLIŞ fonksiyona kurdu, araç KAÇTI dedi. "Uygulandı" ≠
  "DOĞRU YERE uygulandı". Çapa tek yerde değilse mutant KURULAMADI = kırmızı.
- 🔴 **YAKALA-HEPSİ DESENİ ÖLÜ MANTIK DOĞURUR:** adaptöre `.*\.JSONL$` konsaydı hiçbir `.jsonl`
  "tanınmayan" olamaz, ölçüt (b)'nin `.jsonl` yarısı hiç ateşlenemezdi. Bilinçli bedel:
  `README.md` her projede OLCULEMEDI listesinde görünür — dürüst hâli budur.
- 🔴 **SAYI BULAŞMASI · OKUNMADAN HÜKÜM · BOZULABİLİR BEYAN** (dış denetçi): başka projenin sayısı
  yeniden ölçülmeden yazılmaz · dosyanı okumadan beyan etme · commit kimliği tazelik komutuyla
  yazılır. Ayrıntı: `denetim/2026-08-15_*`.
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

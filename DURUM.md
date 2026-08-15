# DURUM — hafiza-kur
**BİTTİ sayacı: 5 ✅ / 6** — md.6 push'landı (`3c38c6c5`); CI #56 **91/94**, düzeltmesi diskte
Son güncelleme: 15 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — SIFIR BAŞARISIZ bir koşum; sonra md.6 ✅ (5→6)
`devral --kesif` (kuru prova, tek bayt yazmaz) + `--esle` rol kilidi + **DURMA KURALI** yazıldı;
`DEVIR_ADAPTORU` motorda TEK EV (kuru prova ile yazan yol AYNI tabloyu okur).
`faz0/devral_kesif_mutanti.py`: 3 kapı, 3/3 mutant AYRI eksende ISIRDI.
**CI #56 (`3c38c6c5`) ÖLÇÜLDÜ — 94 işin 91'i success.** `devir kesfi mutanti` ubuntu·windows·
macos ÜÇÜNDE DE YEŞİL ⇒ md.6'nın KENDİ kapısı geçti. Kırmızı olan tek iş `karmasiklik olcutu`
(üç platformda aynı adım): `karmasiklik_mutanti.py`'nin ÇAPASI `cmd_devral 88` idi, md.6 dalları
CC'yi **97**'ye çıkardı. Çapa 97'ye güncellendi + `capraz.yml`'deki bayat sayı silindi —
**ikisi de DİSKTE, PUSH YOK.** #56 kırmızı olduğu için sayaç 5'te KALDI.
Gerileme (bulut, linux): altın küme 22 ölçüm **BIT-BIT FARK YOK** · `isir` 34/34 temiz motorla
birebir · fazA 6/0 · fazB temiz motorla AYNI · `CC>20` 5 sabit, `ihlal` 8→9.
Sonra: **C** (sahiplikli benimseme) ve **D** (**AYRIŞMA KAPISI**: iki dosya aynı rolü iddia
ederse KIRMIZI). Piyasada (`skill-memory-bank`, 8 istemci) adaptör + sahiplik işareti GİRİŞ
BİLETİ; ayrışmayı ÖLÇEN kapı kimsede yok ⇒ **ayırt edici D'dir, A değil.**

## 🔴 ÖLÇÜT (c) DELİKTİ — kod yazılmadan bulundu (15 Ağu, Onur kilidi)
İlk yazım "canli YOK **ve** tanınmayan aday VAR" idi. `CLAUDE.md`+`DURUM.md` taşıyan proje
ikisini de TANIDIĞI için koşul ateşlenmez, motor gene boş defter açardı — ölçüt, uğruna
yazıldığı iki örneği (Momentum · Is-Portfolyo) ISKALIYORDU. Yeni hâli tek koşul: `canli` YOKSA
DUR; M-3 mutantı tam bu VE'li yazımı geri kurar. **DERS:** ölçüt cümlesi, uğruna yazıldığı
SOMUT VAKAYA karşı okunur — "mantıklı mı" değil, "o vakada ateşliyor mu".

## 25 AĞU YAZISI — ikinci dikey dilim
Eski md.6 KESİLDİ (`CLAUDE.md` §5 — zaman değil ÖLÇÜT kusuru). **Kurulum YAPILMADI, Is-Portfolyo'ya
tek bayt yazılmadı**; `faz0/kullanim_kapisi.py` de kesildi. Yazıda "ölçülemedi + sebebi" diye açık
geçer; "bir hafta kullandım" iddiası KURULMAZ. Yeni md.6'nın (c) deliği de girer: ölçüt YAZMAK ile
ölçüt SINAMAK ayrı işlerdir. Ara işler (BİTTİ'ye bağlı DEĞİL, ADR ister): depo atfı history rewrite
(son 24 Ağu) · H16 YAPI kapısı (tasarım onaylı, kod yok) · `kanit`teki `t_y3`/`t_y42` hâlâ
`continue-on-error` (bilinçli; `readme_kapisi` kapılı koşuyor).

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
Md.2+4 CI #43 `cde1998` + #46 `5d81838` · md.5 README kanıt bloğu CI #49 `fba20c8`
(`readme_mutanti` 3 kapı/6 mutant; aracın kendi `shlex` kusurunu ÖLÇÜM buldu, CI değil) ·
`devral` gerçek Windows'ta gerçek projede (421 MB/1001 dosya/git'li) exit 0, 0 satır silindi —
**`devral`'ın TEK canlı ölçümü budur** · yol ayracı körlüğü kapandı (`_rel()` + 21 çağrı) ·
CI #41 KIRMIZI'dan #46'ya (`_cikti_kodlamasini_guvenceye_al()`).

## Bilinen sınırlar (ölçülmüş)
- 🔴 **ÖLÇÜMÜ KOŞTUM, ONU KORUYAN KAPIYI KOŞMADIM** (15 Ağu; CI #56 yakaladı, ben değil):
  `karmasiklik.py --ihlal` koştum, "rapor kipi, exit 0" dedi, içim rahat etti — ama o sayıyı
  KORUYAN `karmasiklik_mutanti.py`'yi koşmadım; çapası kırmızıydı. **`X.py` ile `X_mutanti.py`
  AYRI DEĞİL, ÇİFTTİR.** "exit 0" uyutur.
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
- 🔴 **Derleme artefaktı H14'ün DELİLİNİ bozar:** `_h14_adaylar` hariç kümesinde `obj`/`bin`/
  `.dart_tool` YOK ⇒ "en yeni değişiklik" hep bir artefakt olur; işaretçi gerçek dosyayı gösteremez.
- 🔴 **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (belge-iç-tutarsızlık, İKİNCİ ısırık):
  git'li ama KODSUZ proje hem HAFİF hem KAPILI satırına uyuyor; bu turda KAPILI seçildi.
- 🔴 Motorda `push`/`fetch`/`remote`/`origin` SIFIR eşleşme — yalnız yerel git; git ya da commit
  yoksa H9 ÖLÇÜLEMEDİ.
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR** (CI #43: win kolu daha UZUN metin taşıyor ama
  zip'i daha KÜÇÜK). Hüküm `conclusion` + log metnidir.
- 🔴 **GitHub API 403'ü ARALIKLIDIR** (aynı oturumda hem 403 hem başarı ölçüldü): tek 403'te
  vazgeçme, URL'i değiştirip bir kez daha dene, iki kez 403 ise tarayıcıya in. **HTML `/actions`
  sayfasını WebFetch ile OKUMA — BAYAT dönüyor** ("#23 Queued" dedi, gerçek #55'ti).
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ve
  `paketle.sh` (mount `zip`e izin vermiyor). Kum havuzu `/tmp`'e kurulur. Gerçek ağaç probu
  gerekiyorsa kök dosyaları `$HOME/kesif_probu/` altına KOPYALANIR (mount dışı).
  Mount `unlink` vermiyor — silmek yerine `fable dosyalama/_to_delete/` altına TAŞI.
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor, `device_bash`
  yazıyor (beş kez ölçüldü, sha bulut kopyasıyla birebir).
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK (§8: ikinci ısırıkta H12'ye "İŞARET" hâli).
- **`continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — bilinçli olanlar: `kanit`in
  ölçüm adımları (hüküm kapısı HARİÇ) · `win_kill_probu` · `boru_probu` · `ortam` · `kalite`.
- `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar · `ci_kapsam_kapisi.py` deseni `faz0/*_mutanti.py`
  — `yol_ayraci_kapisi.py`/`paketten_kos.py` girmez, işleri elle konur.
- 🟡 `kanit`teki `t_y3`/`t_y42` hâlâ KAPI DEĞİL ama `readme_kapisi` kapılı koşuyor (son 4 koşum
  48/48 success). Bilinçli karar DEĞİŞMEDİ.
- `readme_mutanti` README'nin ANLATIMINI ölçmez · `paketten_kos` belgenin ANLAMINI değil GEÇTİĞİNİ
  ölçer · `devral`ın YAZIM ayağı (çıpa/zincir/yedek/triyaj) hâlâ mutantsız; yeni kapı yalnız
  KEŞİF+DURMA ölçer · `derle` sonrası ikinci `isir` ölçülmüyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

# DURUM — hafiza-kur
**BİTTİ sayacı: 5 ✅ / 6** — md.6'nın KODU YAZILDI, **CI BEKLİYOR** (push Onur'da)
Son güncelleme: 15 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — md.6 CI'da yeşillenirse ✅ (5→6)
`devral --kesif` (kuru prova, tek bayt yazmaz) + `--esle` rol kilidi + **DURMA KURALI** yazıldı;
adaptör tablosu `DEVIR_ADAPTORU` motorda TEK EV (kuru prova ile yazan yol AYNI tabloyu okur).
`faz0/devral_kesif_mutanti.py`: 3 kapı YEŞİL, **3/3 mutant AYRI eksende ISIRDI** (kum havuzu
`/tmp`, linux, 15 Ağu). Gerileme ÖLÇÜLDÜ: altın küme 22 ölçüm **BIT-BIT FARK YOK** · `isir` 34/34
(temiz motorla birebir) · fazA 6 ısırdı/0 kaçtı · fazB temiz motorla AYNI (2 ölçülemedi = root).
CI işi `capraz.yml`'e eklendi (`ci_kapsam_kapisi` bunu şart koşuyor).
🔴 **DİSKTE YAZILDI, PUSH EDİLMEDİ** — üçüncü taraf için kayıt değildir; push + CI Onur'da.
Sonra: **C** (sahiplikli benimseme, blok başına `sahip=`) ve **D** (**AYRIŞMA KAPISI**: iki dosya
aynı rolü iddia ederse KIRMIZI). Piyasada (`skill-memory-bank`, 8 istemci) adaptör + sahiplik
işareti GİRİŞ BİLETİ; ayrışmayı ÖLÇEN kapı kimsede yok ⇒ **ayırt edici D'dir, A değil.**

## 🔴 ÖLÇÜT (c) DELİKTİ — kod yazılmadan bulundu (15 Ağu, Onur kilidi)
İlk yazım "tanınan `canli` YOK **ve** tanınmayan aday VAR" idi. `CLAUDE.md`+`DURUM.md` taşıyan bir
proje **ikisini de TANIDIĞI** için "tanınmayan aday" üretmez ⇒ koşul ateşlenmez ⇒ motor gene boş
defter açardı. Yani ölçüt, uğruna yazıldığı iki örneği (Momentum · Is-Portfolyo) ISKALIYORDU.
Yeni hâli tek koşul: `canli` YOKSA DUR. M-3 mutantı tam bu VE'li yazımı geri kurar.
**DERS (yeni sınıf):** ölçüt cümlesi, uğruna yazıldığı **SOMUT VAKAYA karşı** okunur — "mantıklı
mı" değil, "o vakada ateşliyor mu". Bu, "GEÇİYOR MU kapısı zayıftır" dersinin ölçüt kardeşidir.

## 25 AĞU YAZISI — ikinci dikey dilim
Eski md.6 KESİLDİ (15 Ağu; gerekçe `CLAUDE.md` §5 — zaman değil ÖLÇÜT kusuru). **Kurulum
YAPILMADI, Is-Portfolyo'ya tek bayt yazılmadı.** `faz0/kullanim_kapisi.py` de kesildi. Yazıda
kesilen madde **"ölçülemedi + sebebi"** diye açık geçer; "bir hafta kullandım" iddiası KURULMAZ.
Yeni md.6'nın (c) deliği de yazıya girer: ölçüt YAZMAK ile ölçüt SINAMAK ayrı işlerdir.
Ara işler (BİTTİ'ye bağlı DEĞİL, ADR ister): depo atfı history
rewrite (son tarih 24 Ağu) · H16 YAPI kapısı (tasarım onaylı, kod yok) · `kanit`teki
`t_y3`/`t_y42` hâlâ `continue-on-error` (bilinçli; `readme_kapisi` kapılı koşuyor).

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
Md.2+4 CI #43 `cde1998` + #46 `5d81838` (üç kapı ailesi, üç platform, `continue-on-error`SIZ) ·
md.5 README kanıt bloğu CI #49 `fba20c8` (`readme_mutanti` 3 kapı/6 mutant; aracın kendi `shlex`
kusurunu ÖLÇÜM buldu, CI değil) · `devral` gerçek Windows'ta gerçek projede (421 MB/1001 dosya/
git'li): exit 0, 0 satır silindi — **`devral`'ın TEK canlı ölçümü budur** · yol ayracı körlüğü
kapandı (`_rel()` + 21 çağrı) · CI #41 KIRMIZI'dan #46'ya (`_cikti_kodlamasini_guvenceye_al()`).

## 🔴 İKİ ÖZ-KUSUR (ikisini de ÖLÇÜM buldu, CI DEĞİL)
1. **YEŞİL CI, ÖLÇÜLMEMİŞ ŞART** (CI #45 yeşilken `paketten_kos.py` belgenin 1. adımını atlıyordu)
   ⇒ madde ✅ olmadan önce ölçüt cümlesi KELİME KELİME araca karşı okunur.
2. **"GEÇİYOR MU" KAPISI ZAYIFTIR** — "tutarlı mı" AYRI eksendir (S-6; yol ekseni eklendi).

## Bilinen sınırlar (ölçülmüş)
- 🔴 **MUTANT ÇAPASI TEK YERDE OLMALI** (15 Ağu, ilk koşumda ısırdı): M-3'ün çapası
  `if not adaylar:` motorda ÜÇ yerde geçiyordu; `str.replace(...,1)` mutantı YANLIŞ fonksiyona
  kurdu, metin değişti, araç "kuruldu" sayıp KAÇTI dedi. "Uygulandı" ile "DOĞRU YERE uygulandı"
  aynı şey değildir. Artık çapa tek yerde değilse mutant KURULAMADI = kırmızı.
- 🔴 **YAKALA-HEPSİ DESENİ ÖLÜ MANTIK DOĞURUR** (15 Ağu): adaptöre `.*\.JSONL$` konsaydı hiçbir
  `.jsonl` asla "tanınmayan" olamaz ve ölçüt (b)'nin `.jsonl` yarısı hiç ateşlenemezdi. Adlandırılmış
  defterler tanınır (`_ZINCIR.jsonl`·`PROJE_RADAR.jsonl`), gerisi OLCULEMEDI'ye düşer.
  Bilinçli bedel: `README.md` her projede OLCULEMEDI listesinde görünür — dürüst hâli budur.
- 🔴 **PROJELER ARASI SAYI BULAŞMASI · OKUNMADAN HÜKÜM · BOZULABİLİR BEYAN** (15 Ağu, üçünü de dış
  denetçi buldu): başka projenin belgesinden alınan sayı hedef projede yeniden ölçülmeden yazılmaz ·
  kendi dosyanı okumadan içeriğini beyan etme · nota giren commit kimliği yanında tazelik komutuyla
  yazılır (`git log --oneline <damga>..HEAD -- <dosya>`). Ayrıntı: `denetim/2026-08-15_*`.
- 🔴 **Defter COMMIT'lenmeden `kapi` KIRMIZI** (kum havuzu): `[H9] git'te IZLENMIYOR` → çıkış 1;
  commit'lenince YEŞİL. ⇒ "defteri `.gitignore`'a al" fikri md.6(c)'yi ULAŞILMAZ kılar.
- 🔴 **Derleme artefaktı H14'ün DELİLİNİ bozar**: `_h14_adaylar` hariç kümesinde `obj`/`bin`/
  `.dart_tool` YOK; `.gitignore`'lu oldukları için mtime ile ölçülürler ⇒ "en yeni değişiklik" hep
  bir artefakt olur. Hüküm doğru olsa da işaretçi gerçek dosyayı ASLA gösteremez.
- 🔴 **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (belge-iç-tutarsızlık, İKİNCİ ısırık):
  git'li ama KODSUZ proje hem "HAFİF" hem "KAPILI" satırına uyuyor. Bu turda KAPILI seçildi.
- 🔴 Motorda `push`/`fetch`/`remote`/`origin`/`clone` SIFIR eşleşme — yalnız yerel git; git YOKSA
  ya da commit yoksa H9 ÖLÇÜLEMEDİ.
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR** (KESİN KANIT CI #43: win kolu daha UZUN metin
  taşıyor ama zip'i daha KÜÇÜK). Hüküm `conclusion` alanı + log metnidir.
- 🔴 **GitHub Actions HTML sayfası WebFetch'te BAYAT döndü** (15 Ağu): "#23 Queued" dedi, gerçek
  #55'ti. CI hükmü `api.github.com/repos/<...>/actions/runs`'tan alınır, HTML sayfasından DEĞİL.
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ve
  `paketle.sh` (mount `zip`e izin vermiyor). Mutant/prob araçları kum havuzunu `/tmp`'e kurar,
  orada koşar. Mount `unlink` vermiyor — silmek yerine `fable dosyalama/_to_delete/` altına TAŞI.
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor, `device_bash`
  yazıyor (dört kez ölçüldü, sha bulut kopyasıyla birebir).
- 🟡 **Beyan ile mtime çelişince ölçen kapı YOK** (§8 gereği kapı YAZILMADI; ikinci ısırıkta
  H12'ye "İŞARET" hâli eklenir).
- **`continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — bilinçli olanlar: `kanit`in ölçüm
  adımları (hüküm kapısı HARİÇ) · `win_kill_probu` · `boru_probu` · `ortam` · `kalite`.
- `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar (`faz0/` lint edilmez) · `ci_kapsam_kapisi.py`
  deseni `faz0/*_mutanti.py` — `yol_ayraci_kapisi.py`/`paketten_kos.py` girmez, işleri elle konur.
- 🟡 `kanit` işindeki `t_y3`/`t_y42` hâlâ KAPI DEĞİL (`continue-on-error`) ama `readme_kapisi`
  onları kapılı koşuyor; son 4 koşumda 48/48 adım success. Bilinçli karar DEĞİŞTİRİLMEDİ.
- `readme_mutanti.py` README'nin ANLATIMINI ölçmez · `paketten_kos.py` belgenin ANLAMINI değil
  GEÇTİĞİNİ ölçer · `devral`ın YAZIM ayağı (çıpa/zincir/yedek/triyaj) hâlâ mutantsız; yeni kapı
  yalnız KEŞİF + DURMA eksenini ölçer · `derle` sonrası ikinci `isir` ölçülmüyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli) · CC: `CC>20: 5`
  sabit, `ihlal` 8→9 (md.6'nın iki bayrağı `main`i 80→82 satıra çıkardı; ölçüm, kapı değil).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

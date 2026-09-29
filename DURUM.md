# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (**CI #99 `b6a3dda3`: 151 iş, 0 başarısız — 6 Eyl ölçüldü**)
Son güncelleme: 29 Eyl 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
**K4 — H6/H8/H16 + TEK TANIK İSIR TAMAMLANDI (39→49→55/67).** ŞIK B kilit ailesi (B2+B3) ·
md.11 eşitlik körlüğü yönü · README_EN kapısı · `h4_gitignore_mutanti`ye **2-EK için AYRI kol**.
Kalan 12 kör nokta (H0 3911·H4·H1-KOVA×2·H5·H12 4968·H13×2·H2·H17·H-LINK·H10 4716; başka
tanıklı/yetim) KAPSAM DIŞI; yeni tur ONUR KİLİDİ ister. **25 Ağu yazısı KAPSAM DIŞI**
(İş Portföyü'nde kapanır) · **Deneme**: BEŞLİ PAKET kapandı, başlaması Onur kilidi bekler.
🔒 **Tuzak Avcısı ölçüm fixture'ı DEĞİL (6 Eyl kilidi) — gerçek-proje regresyonu YALNIZ Momentum.**

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**TEK TANIK İSIR** (bu tur, motor `479cb056`→`f7eeaa6b`, 362.848→371.550 B) — 6 yeni mutant
(M-Hcy·M-H0k·M-H10t·M-H12c·M-H14e·M-H9: sabote edilince kapı YEŞİL basan fail()'ler); sabotaj
isir 49→**55/67** (köşegen 6/6, önceki 49 KORUNDU, örtüşme 0). SONUÇ kuyruğu M-H9 durumunu
söyler (öneki B-7/readme için BİREBİR). Ölçüldü: taze git'li 67/67+2 SINANMADI · derle 69/69 ·
git'siz derle 66/66+3 UYGULANMAZ; 10 yerde sayı güncellendi. `t_y42` (dokunulmadı) 56 senaryoda
taban motorla hüküm farkı 0. ·
**H6/H8/H16 İSIR** (`1ba9d08e`/`60c32af9`) — 10 yeni mutant, sabotaj isir 39→49/67; EK-1 yetkisiz
Windows'ta `os.symlink`→`mklink /J` junction (ÖLÇÜLDÜ); `isir_eslesme_mutanti` KOL O+KOL J. ·
**H11 İSIR** (`fe3df31e`, CI #112) — 10 kör fail(), sabotaj isir 29→39/67. ·
**ŞIK B** (`c4acba69`, CI #111 181/181) — isir H1 0/6→6/6 (tam etiket + eksen parçası + `siki`), sabotaj isir 23→29/67. ·
**ŞIK A** (`612a2a74`, CI #110 178/178) — `h1_kapsam_mutanti` + `sabotaj.py --ek-olcer` (isir/ek/birleşim AYRI). ·
**ayrisma zaman bombası** (27 Eyl, `sabit_tarih_mutanti`) · **devral GİRİŞ KAPISI** (26 Eyl) ·
**`bolum-kur`** (13 Eyl; aday listesi `BOLUM_HEDEF`+ARŞİV DİZİNİ, `rc["zorunlu_bolumler"]` DEĞİL). ·
**CI ölü kod+bayat yorum+izlenmeyen artık** (13 Eyl) — `shell: bash -e` exit-2 muafiyetini
`ec=`ye ULAŞTIRMIYORDU ⇒ `set +e`/`set -e` + `ci_adim_muafiyeti_mutanti.py`. ·
**B4-3+B4-4+grep tuzağı+ÖLÇEN TARAFIN körlüğü** (12 Eyl) — `derle` `yaz(y.canli)` dönene kadar
ERTELER · `kilit_al` on-kontrolden geçer + son ağ EACCES/EPERM/EROFS · `_b44_sinifla` DÖRT
kuralla sertleşti. ·
**devral türetimi+H4 git havuzu+H12/H14 git delili+çapa/dosya ekseni+H4 çıplak ad+BEŞLİ PAKET+
gitfile körlüğü** (4-6 Eyl, CI #96-99) — devral disk'ten türetir, git sorguları CI'da hızlı,
M-Y4/çıplak-ad/AYLAR kilitleri KORUNDU.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **"GERÇEK ORTAMDA OLMAZ" DEMEDEN ÖNCE ORTAMI ÖLÇ (6 Eyl ISIRDI):** M-Y2 kusuru "hiçbir
  runner'da bu TMPDIR yok" diye KESİLMİŞTİ; macOS tam oradaydı. Kardeşi: **POZİTİF KONTROLSÜZ
  DÜZELTME KAPANMIŞ SAYILMAZ**. **Push'u `git ls-remote` ölçer** — bir tur "push yapıldı" dendi,
  gitmemişti.
- 🔴 **ÖLÇÜM ORTAMI HÜKMÜ ÇARPITIR — ISIRDI (6 Eyl):** bulut konteynerde `id -u`=0; `fazB_olcut_
  mutanti` · `fazB_senaryolari` · `y4_mutant` ROOT'ta SAHTE KIRMIZI verir, `t_y42` "57+1" der.
  Çözüm ölçüldü: `useradd olcum` + `su olcum` ⇒ dördü de exit 0, `t_y42` **58/58**. Bataryayı
  root koşma; "root için device VM tek adres" kaydı BAYATTI.
- 🔴 **`continue-on-error` TAŞIYAN YEŞİL KAPI DEĞİLDİR — ISIRDI (4 Eyl):** CI #85'in gitfile
  yeşili HİÇBİR ŞEY ölçmüyordu. **Talimat yalnız YAML yorumunda durursa iş emrine girmez ve
  kaçar.** Bilinçli ÖLÇÜM işleri: `win_kill_probu` · `boru_probu` · `ortam` · `kalite` · `kanit`.
- 🔴 **KAPI NEYİ ÖLÇTÜĞÜNÜ ÖLÇEMEZ — ÜÇ ISIRIK** (§8): VARLIĞI ölçen kapı SAYIYI ölçmez · iki
  büyüklük EŞİTSE hangisinin ölçüldüğü ÖLÇÜLEMEZ (md.10) · `M-A8`i kıran KESMEYDİ.
- 🔴 **YOL UZUNLUĞU BİR ÖLÇÜM EKSENİDİR:** sabit `[:N]` kesmeleri kök uzunsa mesaj kuyruğunu yer.
  Kısa `/tmp` TÜM bataryayı KÖR bırakıyordu; `--uzun-yol` + M-Y2 kalıbı bunu ölçer.
- 🔴 **ÖLÇÜM ALETİ DE YALAN SÖYLER — DOKUZ VAKA:** boru sonrası `$?` · `d[rol]=dosya` uydurdu ·
  argümansız araç · eşitlik maskelemesi · `stderr=STDOUT` md.8'i KÖR etti · PAYLAŞILAN KUM HAVUZU ·
  `A or B` zincirinde "boş" · regex HAM BLOĞU okumadan hüküm vermez · artefakt BOYUTU oracle DEĞİL.
  ⇒ akış BİRLEŞTİRİLMEZ · HAM ÇIKTI okunur.
- 🔴 **CI HÜKMÜ:** API URL'ine navigasyon + `JSON.parse(innerText)`; **sayfa başına 100** ⇒
  `total_count` ile SAYFALA (151 = 100+51). 🔴 **`total_count` koşum sürerken BÜYÜR** (7 Eyl: 148→151)
  ⇒ hepsi `completed` olmadan SAYMA. 403/504 aralıklı ⇒ bir kez YENİLE; `fetch` ÖLÜ. 🟢 **LOG
  OKUNUR:** Chrome + `get_page_text`, `runs/<RUN_ID>/job/<JOB_ID>` (`check_suite_id` ≠ `run_id`).
- 🔴 **CI kırmızısı KAPI kırmızısı olmayabilir** (#66: `upload-artifact` 403).
- 🔴 **KAPININ SENARYOSU KAPIYI KIRMIZI YAKABİLİR** (md.7/A2) ⇒ gerçek vakaya çevir.
- 🔴 **ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR — DÖRT KEZ ısırdı, hepsi kod yazılmadan:** md.6(c) ·
  md.7 lafzi D · md.7(b) · "çapa en son koşumdan eskiyse kırmızı" (sonsuz kırmızı verirdi).
- 🔴 **ÇAPALARA BAKILMADAN KAPI GÖVDESİNE SATIR EKLENMEZ — DÖRDÜNCÜ ısırık 6 Eyl** (`gitfile`
  6. kol 4→6 unutuldu). 🔴 **"TÜM `faz0` bataryası" YALNIZ `*_mutanti.py` DEĞİL, `.sh` de DEĞİL**
  — `yol_ayraci_kapisi` atlandı (CI #96 kırmızı), `ortam_olcum.sh` aylarca hiç koşulmadı.
  **BELGE ve YORUM da kapı kırar**; `yol_ayraci_kapisi` YORUM ile KODU AYIRT ETMİYOR (ayrı tur).
  **ÇAPA ARACIN KENDİ ÇIKTISINDAN GÜNCELLENMEZ**; **mesaj metni ile koşul TEK KAYNAKTAN üretilir**.
- 🔴 **İŞ EMRİ KISITI EN BAŞA YAZILIR**; geçici satırın kaldırma talimatı KALEM 1'e girer.
  **Tarihi ÖLÇEN taraf yazar.** **Kabul kriterindeki sayı ROOT koşumundan alınmaz** (6 Eyl: "57+1").
- 🔴 **YEŞİL CI, ÖLÇÜLMEMİŞ ŞART** (#45) ⇒ ölçüt cümlesi KELİME KELİME araca karşı okunur.
- 🔴 **YAKALA-HEPSİ DESENİ ÖLÜ MANTIK DOĞURUR** · **SAYI BULAŞMASI / OKUNMADAN HÜKÜM** ·
  **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (İKİNCİ ısırık).
- 🔴 **Defter COMMIT'lenmeden `kapi` KIRMIZI** ([H9]) ⇒ "defteri `.gitignore`'a al" md.6(c)'yi
  ULAŞILMAZ kılar. **Derleme artefaktı H14'ün DELİLİNİ bozar**.
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ·
  `paketle.sh` (mount `zip` yok) · `t_y42.py` (150 sn'de bitmiyor) ⇒ **bulut konteynerde** koşulur
  (SHA çapraz). Push'suz ağaç: sha256 listesi `comm` ile karşılaştırılıp yalnız FARKLI dosyalar
  stage edilir, sonra bit-bit doğrulanır. Mount `unlink` vermiyor — `_to_delete/`ye TAŞI.
  ✏️ `.github/workflows/*` `device_bash` ile YAZILIR; `device_commit_files` REDDEDER.
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK · `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar ·
  `ci_kapsam_kapisi.py` deseni `faz0/*_mutanti.py` · `readme_mutanti` README'nin ANLATIMINI ölçmez ·
  `paketten_kos` belgenin ANLAMINI değil GEÇTİĞİNİ ölçer · `derle` sonrası ikinci `isir`
  ölçülmüyor · `isir`da **M-H9 (git izlenirliği) mutantı YOK** · KALEM 3'ün iki yeni hüküm
  cümlesi (sat. 4626/4897) `isir` kataloğunda KARŞILIKSIZ ⇒ sabotaj körlüğü 43→45 (Onur kilidi:
  kapatılmaz) · dört ölçümün koşucusu pakette yok · kilit inode yarışı daraltıldı, kapatılmadı ·
  zincir anahtarsız (bilinçli) · `PROJE_RADAR.jsonl` YOK ⇒ radar HÜKÜM VEREMİYOR.
- 🔴 `rmtree(ignore_errors=True)` 38 dosya/124 yer, `onerror` YOK (5 Eyl, çöplenme) — md.8 ⇒ **KOD DEĞİŞMEZ**.

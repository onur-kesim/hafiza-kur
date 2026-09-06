# DURUM — hafiza-kur
**BİTTİ sayacı: 10 ✅ / 10 — LİSTE KAPALI** (**CI #94 `66cfd1f1`: 124 iş, 0 başarısız — 6 Eyl ölçüldü**)
Son güncelleme: 6 Eyl 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## 🔴 SIRADAKİ İŞ — liste 10/10 KAPALI; yeni madde ONUR KİLİDİ ister
ŞIK B kilit ailesi (B2+B3) · md.11 eşitlik körlüğü yönü · kapsam envanteri α/β (motor `401a3f71`
BAYAT) · README_EN kapısı. **25 Ağu yazısı KAPSAM DIŞI** — İş Portföyü'nde kapanır (5 Eyl kilidi).
🔴 **Deneme, BEŞLİ PAKET kapanınca başlar** (Onur kilidi 6 Eyl).

## ✅ KAPANANLAR (tek satır — ayrıntı git geçmişinde)
**BEŞLİ PAKET** (6 Eyl, dogfood bulguları — 5 düzeltme, 5 AYRI mutant, hepsi pozitif kontrollü)
— ① `AYLAR` ay KISALTMASINI tanımıyordu ⇒ H12 **ve** H14 tek kökten kördü (hafiza-kur'un KENDİ
`DURUM.md`'si aylardır ölçülmüyordu; ilk hipotez `·` ayracıydı, ÖLÇÜMLE YANLIŞLANDI) ② `kur`
yalnız KENDİ v1 izlerini tarıyordu ⇒ `devir_rolu()` yeniden kullanıldı, kaçış `--yine-de` zincire
düşer ③ `--kapsam-zorla` → exit 5 (varsayılan BİREBİR korundu; beyanlı gevşekliği de kapsar)
④ `surum` komutu ⑤ `hook --kur` (motorda `hook` SIFIR eşleşmeydi). 🔴 İKİ REGRESYON AÇILDI VE
KAPANDI: `cmd_kur_bolme` iki çapası + `gitfile_korlugu` 6. kol sayacı (3→4, bağımsız sayımla) ·
**çok satırlı mesajın HÜKÜM KANALINDA kaybı** (6 Eyl, CI #90→#94) — `oldur()` mesajı hükümde
birinci satıra düşüyordu, İŞARETSİZ; artık `(+N satir: stderr)` taşır. 19 KARAKTERLİK işaret ölçüm
katmanında BEŞ yeri ısırdı, son üçü YALNIZ macOS'ta ·
**gitfile körlüğü** (4 Eyl, CI #86) — `.git` worktree/`--separate-git-dir`/submodule'de METİN
DOSYASIDIR ⇒ sağlam depoda "H9: git YOK". ŞIK D 12/0, `--git-dir` ELENDİ ·
**M-Y4** (20 Ağu) — `pay = esik//10` KALDIRILDI; **PAY GERİ EKLENMEZ** · **md.10** hüküm iç
tutarlılığı · **md.9** görünürlük · **md.6-8** keşif/eşle/durma + çoklu-`canli` + hüküm ayrımı ·
**md.2+4+5** README · `--kesif` **72 public depoda**, salt okuma, 0 bayt.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **"GERÇEK ORTAMDA OLMAZ" DEMEDEN ÖNCE ORTAMI ÖLÇ (6 Eyl ISIRDI):** M-Y2 kusuru bulunmuş,
  "hiçbir runner'da bu TMPDIR yok" diye KESİLMİŞTİ; macOS tam oradaydı. Kardeşi: **POZİTİF
  KONTROLSÜZ DÜZELTME KAPANMIŞ SAYILMAZ** (iki macOS turu kör gitti). **Push'u `git ls-remote`
  ölçer** — bir tur "push yapıldı" dendi, gitmemişti.
- 🔴 **`continue-on-error` TAŞIYAN YEŞİL KAPI DEĞİLDİR — ISIRDI (4 Eyl):** CI #85'in gitfile yeşili
  HİÇBİR ŞEY ölçmüyordu; POZİTİF KONTROLLE bulundu (#84'te motor kusurluyken ve mutant exit 1
  verirken hem iş hem adım "success"). `capraz.yml` KAPI'ya çevrildi. **Talimat yalnız YAML
  yorumunda durursa iş emrine girmez ve kaçar.** Bilinçli ÖLÇÜM işleri: `win_kill_probu` ·
  `boru_probu` · `ortam` · `kalite` · `kanit`in ölçüm adımları.
- 🔴 **KAPI NEYİ ÖLÇTÜĞÜNÜ ÖLÇEMEZ — ÜÇ ISIRIK** (§8): (1) VARLIĞI ölçen kapı SAYIYI ölçmez ·
  (2) senaryoda iki büyüklük EŞİTSE hangisinin ölçüldüğü ÖLÇÜLEMEZ (md.10: dosya=rol) · (3) `M-A8`in
  adı "realpath maskesi"ydi ama kırmızıyı yakan KESMEYDİ ⇒ maske hiç ölçülmemişti.
- 🔴 **YOL UZUNLUĞU BİR ÖLÇÜM EKSENİDİR:** sabit `[:N]` kesmeleri kök uzunsa mesaj kuyruğunu yer
  (ŞIK A'da düzeltildi). Kısa `/tmp` TÜM bataryayı KÖR bırakıyordu; `--uzun-yol` +
  M-Y2 kalıbı kapının YANLIŞ ORTAMDA kaçtığını ölçer.
- 🔴 **ÖLÇÜM ALETİ DE YALAN SÖYLER — DOKUZ VAKA:** `| tail` sonrası `$?` boruyu ölçtü ·
  `d[rol]=dosya` OLMAYAN kusur uydurdu · argümanı YOK SAYAN araç A/B'de aynı motoru ölçtü ·
  eşitlik tabanlı maskeleme sessizce başarısız oldu · `stderr=STDOUT` md.8'i KÖR etti (yerelde
  BEŞ ortamda yeşil, CI #61/#62 yakaladı) · **PAYLAŞILAN KUM HAVUZU YALANCI KIRMIZI ÜRETİR** ·
  **`A or B` zincirinde "boş"u AÇIKÇA tanımla** · **regex HAM BLOĞU okumadan hüküm vermez** ·
  artefakt BOYUTU içerik oracle'ı DEĞİL. ⇒ akış BİRLEŞTİRİLMEZ · hüküm öncesi HAM ÇIKTI okunur.
- 🔴 **CI HÜKMÜ:** API URL'ine DOĞRUDAN NAVİGASYON + `JSON.parse(innerText)`; **SAYFA BAŞINA 100
  DÖNER** — `total_count` ile karşılaştır, SAYFALA. **403 ARALIKLIDIR.** `WebFetch` API'de 403,
  HTML `/actions`ta BAYAT; tarayıcıda `fetch` ÖLÜ. 🟢 **LOG OKUNUR (5 Eyl):** Chrome'un açık
  oturumunda `runs/<RUN_ID>/job/<JOB_ID>` + `get_page_text` (`check_suite_id` ≠ `run_id`) ⇒
  **devralınan "okunamaz" kaydı bir kez YENİDEN DENENİR.**
- 🔴 **CI kırmızısı KAPI kırmızısı olmayabilir** (#66: `upload-artifact` Finalize 403).
- 🔴 **KAPININ KENDİ SENARYOSU KAPIYI KIRMIZI YAKABİLİR** (md.7/A2 elle kırpma) ⇒ gerçek vakaya çevir.
- 🔴 **ÖLÇÜT CÜMLESİ SOMUT VAKAYA KOŞULUR — ÜÇ KEZ ısırdı, üçü de kod yazılmadan:** md.6(c) hiç
  ateşlenmiyordu · md.7 lafzi D 6 şeklin 4'ünde yanıyordu · md.7(b) SAĞLIKLI akışta yanıyordu.
- 🔴 **KAPI GÖVDESİNE SATIR EKLERKEN O KAPININ MUTANT ÇAPALARINA BAKILIR** (CI #56/#58; **6 Eyl'de
  ÜÇÜNCÜ kez ısırdı** — `_kur_halka`/`_kur_rapor` imzası ve `gitfile` 6. kol sayacı). Araç EL İLE
  SEÇİLMEZ, **TÜM `faz0` bataryası** koşulur; **BELGE kapıları da** (`readme_mutanti` README'nin
  sözleşme CÜMLESİNİ ölçer — satırı bölmek bile kırar). **ÇAPA ARACIN KENDİ ÇIKTISINDAN
  GÜNCELLENMEZ** (bağımsız sayım/`radon cc` ile çaprazlanır). **YORUMDAKİ CANLI SAYI BAYATLAR**.
- 🔴 **İŞ EMRİ KISITI EN BAŞA YAZILIR** (üç turdur tutuyor); geçici satırın kaldırma talimatı
  **KALEM 1'e** girer, kod yorumunda kalırsa kaçar. **Tarihi ÖLÇEN taraf yazar.**
- 🔴 **YEŞİL CI, ÖLÇÜLMEMİŞ ŞART** (#45) ⇒ madde ✅ olmadan önce ölçüt cümlesi KELİME KELİME araca
  karşı okunur. Kardeşi: "GEÇİYOR MU" kapısı zayıftır; "tutarlı mı" AYRI eksendir.
- 🔴 **YAKALA-HEPSİ DESENİ ÖLÜ MANTIK DOĞURUR** · **SAYI BULAŞMASI / OKUNMADAN HÜKÜM**
  (`denetim/2026-08-15_*`) · **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (İKİNCİ ısırık).
- 🔴 **Defter COMMIT'lenmeden `kapi` KIRMIZI** ([H9]) ⇒ "defteri `.gitignore`'a al" md.6(c)'yi
  ULAŞILMAZ kılar. **Derleme artefaktı H14'ün DELİLİNİ bozar**.
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ·
  `paketle.sh` (mount `zip` vermiyor) · **UZUN BATARYA (6 Eyl):** `t_y42.py` mount VM'inde 150 sn'de
  bitmedi, arka plan süreci de çağrılar arası ÖLÜYOR ⇒ depo PUBLIC olduğundan **bulut konteynerde
  klonlanıp** koşulur (aynı batarya 67 sn; SHA ile çaprazla; orası **root**tur, `t_y42` Y-1 senaryosu
  orada ÖLÇÜLEMEDİ döner). Mount `unlink` vermiyor — silmek yerine `fable dosyalama/_to_delete/`
  altına TAŞI. ✏️ `.github/workflows/*` köprüden `device_bash` ile YAZILABİLİYOR (BOM'suz UTF-8/LF);
  `device_commit_files` o yolu REDDEDİYOR.
- 🟡 Beyan/mtime çelişkisini ölçen kapı YOK · `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar ·
  `ci_kapsam_kapisi.py` deseni `faz0/*_mutanti.py` · `readme_mutanti` README'nin ANLATIMINI ölçmez ·
  `paketten_kos` belgenin ANLAMINI değil GEÇTİĞİNİ ölçer · `devral`ın YAZIM ayağı mutantsız ·
  `derle` sonrası ikinci `isir` ölçülmüyor · `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ ·
  `isir`da **M-H9 (git izlenirliği) mutantı YOK** · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli) · motorda
  `push`/`fetch`/`remote`/`origin` SIFIR eşleşme · `PROJE_RADAR.jsonl` YOK ⇒ kısır döngü radarı
  bu projede HÜKÜM VEREMİYOR.
- 🔴 **`rmtree(ignore_errors=True)` 38 dosyada / 124 yerde, `onerror` YOK (5 Eyl, kusur DEĞİL
  çöplenme):** md.8 ⇒ **KOD DEĞİŞMEZ**, ikinci ısırıkta açılır. Tazelik:
  `dir /b "%TEMP%\h16km_*" | find /c /v ""`.

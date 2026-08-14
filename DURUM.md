# DURUM — hafiza-kur
**BİTTİ sayacı: 4 ✅ / 6** (madde 1·2·3·4 kapandı — ölçütler ve kanıtları `CLAUDE.md` §2'de)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra yazılır**

## Sıradaki iş (tek madde) — MADDE 5
**Bir sonraki CI koşumunu oku** (`readme_kapisi`, üç platform). YEŞİL TİK YETMEZ; her kolda
`KAPI-1 BEYAN : YESIL` · `KAPI-2 GERCEK : YESIL` · `KAPI-3 SOZLESME : YESIL` ·
`KOSUCU : t_y3 ... 20 senaryo` · `KOSUCU : t_y42 ... 58 senaryo` · `6/6 mutant AYRI eksende
ISIRDI` aranır. Yeşilse **madde 5 ✅** → BİTTİ 5/6; geriye yalnız madde 6 kalır (saati 21 Ağu).

## ✅ MADDE 2 + MADDE 4 KAPANDI (CI #43 `cde1998` + CI #46 `5d81838`) — tek satıra indi
Üç kapı ailesi, hepsi üç platformda ve `continue-on-error`SIZ:
- **`faz0/win_dal_mutanti.py`** (2(i)) — 3 kapı / 4 mutant. KAPI-1 yalnız FAZLA dalı, KAPI-2 EKSİK
  dalı kovalar → **örtüşme YAPISAL kesildi**. KAPI-3 CANLI yalnız win32'de hüküm verir.
  CI #43 windows: `KAPI-3 CANLI : YESIL` · `M-3 → KAPI-3 de KIRMIZI ✓` · `4/4 mutant`.
- **`paketle.sh` + `faz0/paket_mutanti.py`** — SHA kapısı ÖLÜYDÜ, **başlık yalandı**; beyan bırakıldı,
  **ÜRETİLEN PAKET ölçülüyor** (MOTOR BİT-BİT + ENVANTER, M-1 `zip -l` / M-2 `-x references/*`).
- **`faz0/paketten_kos.py`** (4 + 2(ii)) — KAPI-1 BELGE (komut **ve** yol ekseni, PAKETTEKİ
  `SKILL.md`'ye karşı) · KAPI-2 CANLI (belgenin akışıyla). Çıkış kodu sözleşmesi `hafiza.py`
  sat. 4845'ten OKUNDU: `isir` taze projede **2** = SAĞLIKLI, **1 ve 4 KIRMIZI**.
  CI #46 windows: `KAPI-1 BELGE : YESIL` · `C1 komut ISIRDI ✓ · C2 yol ISIRDI ✓` · `8.6 sn, win32`.

## ✅ README KANIT BLOĞU KAPISI (14 Ağu — madde 5'in ölçütü; CI hükmü bekleniyor)
README'nin "Kanıtı kendin koş" bloğu okurun yapacağı şeydir ve **sayısal beyan taşıyor**
(`34/34 + 2 SINANMADI, exit 2` · `36/36, exit 0`). Hiçbir kapı ölçmüyordu; ikincisi
(`derle` sonrası `isir`=0) bu dosyanın "ölçülmüyor" dediği boşluğun ta kendisiydi.
`faz0/readme_mutanti.py`: **ÜÇ kapı, DÖRT mutant, örtüşme yok.**
- KAPI-1 BEYAN (blok ayıklanabilir beyan taşıyor mu) · KAPI-2 GERÇEK (blok KOŞULUR; beklenen
  değerler **BLOKTAN okunur, araca YAZILMAZ** — "sayı yazılmaz, ÜRETİLİR") · KAPI-3 SÖZLEŞME
  (README'nin ilan ettiği `isir` kod kümesi motorun bastığıyla aynı mı).
- M-1→KAPI-1 (beyan silinir) · M-2→KAPI-2 (yanlış oran) · M-3→KAPI-2 (yanlış çıkış kodu) ·
  M-4→KAPI-3 (sözleşmeden kod düşer). Blokta TANIMADIĞI satır görürse ÖLÇÜLEMEDİ der (exit 2):
  README'ye yeni adım eklenip kapının sessizce yok sayması engellenir.
- **`t_y3`/`t_y42` DE BU KAPIDA** (Onur kararı 14 Ağu): `kanit` işindeki kopyaları
  `continue-on-error: true` taşıyor (yani KAPI değil ÖLÇÜM); burada taşımıyor. Senaryo sayıları
  çıktıdan okunup README'nin `# 20 senaryo` / `# 58 senaryo` beyanlarıyla karşılaştırılır.
  Ağır koşucular YALNIZ temiz turda koşar; mutant turları yakalanan çıktıyı yeniden kullanır —
  SINIR: mutant koşucunun davranışını değil KARŞILAŞTIRMAYI ölçer (araç başlığında yazılı).
- Ölçüldü (Linux): üç kapı yeşil, **6/6 mutant** ayrı eksende ISIRDI, 2 dk 57 sn
  (`t_y42` tek sefer, ~60 sn). Y-2: ascii dâhil exit 0. **Araç kendi kusurunu da yazdı:** ilk
  sürümü `shlex` kullanmıyordu, `--metin="ilk not"` bozulup her komut exit 2 dönüyordu — araç
  README'yi suçlayacaktı.
- ✏️ README'deki `~13 dk` SİLİNDİ (`CLAUDE.md` §4: süre tahmini belgeye yazılmaz). `capraz.yml`
  sat. 95 bu beyanın run #2'de ÖLÇÜLÜP YANLIŞ çıktığını zaten yazıyordu — kimse README'yi
  düzeltmemişti. Adım adındaki `~1-2 dk` de kaldırıldı.

## 🔴 BU TURUN İKİ ÖZ-KUSURU (ikisini de ÖLÇÜM buldu, CI DEĞİL)
1. **YEŞİL CI, ÖLÇÜLMEMİŞ ŞART.** CI #45 tamamen yeşilken `paketten_kos.py` motoru PAKET
   DİZİNİNDEN koşturuyordu; belgenin 1. adımı atlanmıştı, yani madde 4'ün "(kurulum belgesiyle)"
   şartı ölçülmüyordu. Yeşil tik bunu göstermez — **ölçüt cümlesini KELİME KELİME araca karşı
   okumak** gösterir. Kalıp: bir madde ✅ olmadan önce ölçüt metni araçla karşılaştırılır.
2. **"GEÇİYOR MU" KAPISI ZAYIFTIR.** KAPI-1 BELGE önce yalnız "komut blokta geçiyor mu" soruyordu;
   belge kendi içinde tutarsız olabiliyordu (1. adım `bin/`, komutlar `araclar/hafiza/`) ve kapı
   KAÇIRIYORDU (sabotaj probu S-6 buldu). **"Tutarlı mı" AYRI bir eksendir**; yol ekseni eklendi.

## 🟢 MADDE 6 SAATİ — 14 Ağu başladı, 21 Ağu biter
`devral` gerçek Windows'ta gerçek projede (421 MB / 1001 dosya / git'li): exit 0, 0 satır silindi.

## ✅ BUGÜN KAPANANLAR (tek satır — ayrıntı git geçmişinde)
- **Yol ayracı körlüğü**: `os.path.relpath` 22 kez elle çevriliyordu (18'i koşulsuz = D-1 ihlali).
  `_rel()` + 21 çağrı; motor `dffe3ce6…`→**`82c6e91b…`**; altın küme FARK YOK (22 ölçüm bit-bit).
- **CI #41→#46**: #41 KIRMIZI (araç KENDİ çıktısındaki U+2713'te çöktü) →
  `_cikti_kodlamasini_guvenceye_al()` HER faz0 aracına konur; #42/#43/#45/#46 hepsi 0 başarısız.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR.** `size_in_bytes` ZIP boyutudur; içerik aynıyken
  windows−ubuntu farkı −2…+2 salınır. KESİN KANIT CI #43: `win-dal`ın windows kolu gerçekten
  FARKLI ve DAHA UZUN metin taşıyor, buna rağmen zip'i daha KÜÇÜK (608/613/614). Hüküm
  `conclusion` alanı + log metnidir.
- 🔴 **BAĞLI KLASÖRDE KOŞMAYANLAR:** `hafiza.py` (H9 `git status` → kalıcı `.git/index.lock`) ve
  `paketle.sh` (mount `zip` çıktısına izin vermiyor → exit 15, 0 baytlık artık bırakır).
  `faz0/paket_mutanti.py` KOŞAR (kum havuzunu `/tmp`'e kurar). Mount `unlink` vermiyor — silmek
  yerine `fable dosyalama/_to_delete/` altına TAŞI.
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor, `device_bash`
  yazıyor (üç kez ölçüldü, sha bulut kopyasıyla birebir).
- 🟡 **Beyan ile mtime çelişince ölçen kapı YOK** (Tuzak Avcisi `PROJE_HAFIZA.md`: mtime 5 Ağu,
  beyan 25 Tem). §8 gereği kapı YAZILMADI; ikinci ısırıkta H12'ye "İŞARET" hali eklenir.
- **`continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — bilinçli olanlar: `kanit`in ölçüm
  adımları (hüküm kapısı HARİÇ) · `win_kill_probu` · `boru_probu` · `ortam` · `kalite`.
- `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar (`faz0/` lint edilmez) · `ci_kapsam_kapisi.py`
  deseni `faz0/*_mutanti.py` — `yol_ayraci_kapisi.py`/`paketten_kos.py` girmez, işleri elle konur.
- 🟡 **`kanit` işindeki `t_y3`/`t_y42` hâlâ KAPI DEĞİL** (`continue-on-error: true`) — ama
  `readme_kapisi` onları kapılı koşuyor. Ölçüldü (son 4 koşum, 3 platform × 2 python):
  48/48 adım success. `kanit`teki bilinçli karar DEĞİŞTİRİLMEDİ.
- `readme_mutanti.py` README'nin ANLATIMINI (sıra, dil) ölçmez, yalnız ölçülebilir beyanlarını.
- `paketten_kos.py` belgenin ANLAMINI değil GEÇTİĞİNİ ölçer (yanlış SIRA görünmez) · `devral` yolu
  hiç ölçülmüyor · `derle` sonrası ikinci `isir` (yani `isir`=0 hâli) ölçülmüyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

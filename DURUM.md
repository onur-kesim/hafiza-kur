# DURUM — hafiza-kur
**BİTTİ sayacı: 2 ✅ / 6** · madde 2: **(i) KAPANDI** (CI #43) · **(ii)** madde 4 ile BİRLİKTE kapanır (Onur kilidi, `CLAUDE.md` §2)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB, yerinde güncellenir · **kapanan bölüm tek satıra iner**

## Sıradaki iş (tek madde)
**CI #46'yı oku** — `paketten kosum` üç platformda, BELGE kapılı sürümle. YEŞİL TİK YETMEZ;
windows kolunda üç satır aranır: `KAPI-1 BELGE : YESIL (4 adimin 4'u belgede)` ·
`BELGE ADIM 1 : motor projeye kopyalandi -> araclar/hafiza/hafiza.py` · `C) belge mutantlari:
C1 komut ISIRDI ✓ · C2 yol ISIRDI ✓`. Yeşilse **madde 4 ✅ VE madde 2 ✅** → BİTTİ 4/6.
(CI #45 zaten yeşildi: 88 iş / 0 başarısız, windows `9.3 sn, win32` — ama belge şartı ölçülmüyordu.)

## ✅ PAKET KAPISI (14 Ağu — kod yazıldı, CI hükmü bekleniyor)
İki ölçüm: **(a)** `paketle.sh`'in SHA kapısı ÖLÜYDÜ — `[ -n "$BEYAN" ]` koruyor ve `SKILL.md`'de
64'lük hex **sıfır**; ölü olan mantık değil, **başlık yalandı**. Üstelik `SKILL.md` sat. 245-249
SHA yazmamayı ÖLÇÜLMÜŞ dersle savunuyor ("bayatlar; iki sürüm görülmedi") → çözüm beyanı geri
getirmek değil **ÜRETİLEN PAKETİ ölçmek**. **(b)** `capraz.yml`'de `paketle`/`.skill` için **sıfır**
eşleme: madde 4'ün dayandığı tek yüzeyin kapısı yoktu. Sınıf ikinci ısırık (1: LİSANS, 10 Ağu) →
§8 gereği artık CI'da mekanik koşuyor.
- `paketle.sh` içinde **KAPI-1 MOTOR BİT-BİT** (zip'ten geri çıkarılan `hafiza.py` == kaynak) +
  **KAPI-2 ENVANTER** (filtre-dışı her dosya var, fazlası yok). Kapı insanın koştuğu yerde yaşar.
- `faz0/paket_mutanti.py` ısırmayı kanıtlar: **M-1 `zip -l`→KAPI-1** (ölçüldü: motor 259.228 →
  264.431 B; 5.203 satırın LF'i CRLF oldu) · **M-2 `-x references/*`→KAPI-2** (6 dosya düştü).
  Örtüşme yok; ikisi de gerçek arıza sınıfı (`* -text` dersi ve LİSANS sınıfı).
- `faz0/paketten_kos.py` madde 4'ü CANLI ölçer, **İKİ KAPI**: **KAPI-1 BELGE** (koştuğu adımlar
  PAKETTEKİ `SKILL.md` §2 "Sıfırdan kurulum" blokunda geçiyor mu + bloktaki her `hafiza.py`
  referansı `araclar/hafiza/` altında mı) · **KAPI-2 CANLI** (belgenin akışıyla — önce motoru
  `<proje>/araclar/hafiza/`ya kopyala — sonra `kur→kapi→isir`). Paket `zipfile` ile açılır
  (hedefte `unzip` GEREKMEZ → windows kolu çalışır).
  **Çıkış kodu sözleşmesi `hafiza.py` sat. 4845'ten OKUNDU:** `isir` taze projede **2** döner ve
  bu SAĞLIKLIDIR (M-H1b kurulamaz, `derle` koşmadı); **1 ve 4 KIRMIZI**. `|| true` sahte yeşil
  üretirdi. Süre ölçütü <300 sn (madde 4 "5 dakika").
- 🔴 **ARACIN KENDİ KUSURU — CI #45 YEŞİLKEN bulundu:** ilk sürüm motoru PAKET DİZİNİNDEN
  koşturuyordu; belgenin 1. adımı (motoru projeye kopyala) atlanmıştı. Yani araç belgenin akışını
  değil KENDİ akışını ölçüyordu ve madde 4'ün "(kurulum belgesiyle)" şartı ölçülmemiş kalıyordu —
  CI bunu hiç göstermiyordu. Düzeltildi: belge izlenir VE belgenin kendisi kapıya bağlandı.
- 🔴 **İKİNCİ KUSUR (sabotaj probu S-6 buldu):** KAPI-1 yalnız "komut geçiyor mu" soruyordu; belge
  KENDİ İÇİNDE tutarsız olabiliyordu (1. adım `bin/`, komutlar `araclar/hafiza/`) ve KAÇIRIYORDU.
  Yol ekseni eklendi; S-6 artık ısırıyor.
- Ölçüldü (Linux, belgenin akışıyla): `kur` 0 · `kapi` 0 · `isir` 2 · **toplam 4,8 sn**.
  Dört sabotaj probu ısırdı (belgede komut değişti · başlık değişti → ÖLÇÜLEMEDİ · motor yolu
  değişti · komut yolu değişti) + motorsuz paket · bozuk motor · `isir` 2 yerine 1.
  Kör-değil ölçümü araca gömülü (A sözleşme · B bozuk motor · **C1 komut / C2 yol belge mutantı**).
  Y-2 dört kod sayfasında exit 0.

## ✅ WIN32 DALI KAPISI — MADDE 2(i) KAPANDI (14 Ağu, CI #43 `cde1998`)
Motorun iki `win32` dalı (sat. 899 `_surec_yasiyor`→`_surec_yasiyor_win` = Y-1 · sat. 4877
`_boru_koptu_mu` = Y-3) hiçbir mutantla ölçülmüyordu. `faz0/win_dal_mutanti.py`: **ÜÇ kapı,
DÖRT mutant, örtüşme yok** — KAPI-1 ENVANTER (yalnız FAZLA dalı kovalar; EKSİK dal KAPI-2'nin işi,
örtüşme YAPISAL kesildi) · KAPI-2 DAVRANIŞ (simülasyon) · **KAPI-3 CANLI** (gerçek ctypes+pid,
yalnız win32'de hüküm). M-1→K1 · M-2→H-a · M-3→H-b · M-4→H-c; windows'ta M-3 KAPI-3'ü de yakar
(örtüşme değil, canlı kapının kör olmadığının ölçümü). CI #43 windows logu birebir:
`KAPI-3 CANLI : YESIL` · `M-3 (KAPI-3 kendi sinamasi) -> KAPI-3 de KIRMIZI ✓` · `SONUC: YESIL —
uc kapi da temiz, 4/4 mutant AYRI eksende ISIRDI.` ("YESIL SINIRLI" değil "YESIL" = dal alındı.)
ÖLÇÜLMEYEN: Dal B'nin tümden silinmesinin ayrı mutantı yok; H-b'nin beş halinden yalnız 259'unki var.

## 🟢 MADDE 6 SAATİ — 14 Ağu başladı, 21 Ağu biter
`devral` gerçek Windows'ta gerçek projede (421 MB / 1001 dosya / git'li): exit 0, 0 satır silindi.

## ✅ BUGÜN KAPANANLAR (tek satır — ayrıntı git geçmişinde)
- **Taze Windows koşumu** (gerçek Windows): `kur`=0 · `kapi`=0 · `isir`=2 → **34/34 mutant
  ISIRDI**, Linux'la ÖZDEŞ.
- **Yol ayracı körlüğü**: `os.path.relpath` 22 kez elle çevriliyordu (18'i koşulsuz = D-1 ihlali).
  `_rel()` + 21 çağrı; motor `dffe3ce6…`→**`82c6e91b…`**; altın küme FARK YOK (22 ölçüm bit-bit).
  `faz0/yol_ayraci_kapisi.py` iki kapı/üç mutant; eski motora karşı KIRMIZI, 21 kaçak.
- **CI #41→#45**: #41 KIRMIZI (araç KENDİ çıktısındaki U+2713'te çöktü) →
  `_cikti_kodlamasini_guvenceye_al()`; #42/#43/#45 üçü de 0 başarısız.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR.** `size_in_bytes` ZIP boyutudur; içerik aynıyken
  windows−ubuntu farkı −2…+2 salınır (`h11-kenar` 1005/1004/1006). KESİN KANIT CI #43: `win-dal`
  artefaktının windows kolu gerçekten FARKLI ve DAHA UZUN metin taşıyor, buna rağmen zip'i daha
  KÜÇÜK (608/613/614). "Üçü de N bayt" bir KAPI DEĞİLDİR; hüküm `conclusion` + log metnidir.
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor ama
  `device_bash` yazıyor (iki kez ölçüldü, sha bulut kopyasıyla birebir). Mount `unlink` vermiyor —
  silmek yerine `fable dosyalama/_to_delete/` altına TAŞI.
- 🔴 **`paketle.sh` BAĞLI KLASÖRDE KOŞTURULMAZ** (ölçüldü 14 Ağu): mount `zip`in çıktı dosyasını
  yazmasına izin vermiyor → `zip I/O error: Operation not permitted`, exit 15 (sessiz değil,
  gürültülü). **0 baytlık `hafiza-kur.skill` artığı bırakır** (gitignore'da, ama `_to_delete/`'e
  taşınır). `faz0/paket_mutanti.py` ise orada KOŞAR: kum havuzunu `/tmp`'e kurar (ölçüldü, 2/2).
- 🔴 **`hafiza.py` BAĞLI KLASÖRDE KOŞTURULMAZ.** H9 kapısı `git -C <kok> status --porcelain`
  koşuyor; mount `unlink` vermediği için `.git/index.lock` KALICI kalır (B4-1'in aynısı, tetikleyen
  ARACIN KENDİSİ). Hedefte git varsa YERLİ kabukta (PowerShell) koşulur.
- 🟡 **Beyan ile mtime çelişince ölçen kapı YOK** (Tuzak Avcisi `PROJE_HAFIZA.md`: mtime 5 Ağu,
  beyan 25 Tem → 11 gün). §8 gereği kapı YAZILMADI; ikinci ısırıkta H12'ye "İŞARET" hali eklenir.
- **`continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — kırmızısı yutulur. Bilinçli
  olanlar: `kanit`in ölçüm adımları (hüküm kapısı HARİÇ) · `win_kill_probu` · `boru_probu` ·
  `ortam` · `kalite`. Kenar/hüküm kapılarında YOKTUR.
- `ruff/mypy/bandit` YALNIZ `hafiza.py`'yi tarar (`faz0/` lint edilmez) · `ci_kapsam_kapisi.py`
  deseni `faz0/*_mutanti.py` — `yol_ayraci_kapisi.py`/`paketten_kos.py` girmez, işleri elle konur.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

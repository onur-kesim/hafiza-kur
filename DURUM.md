# DURUM — hafiza-kur
**BİTTİ sayacı: 2 ✅ / 6** · madde 2: **(i) KAPANDI** (CI #43) · **(ii)** madde 4 ile BİRLİKTE kapanır (Onur kilidi, `CLAUDE.md` §2)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB, yerinde güncellenir · **kapanan bölüm tek satıra iner**

## Sıradaki iş (tek madde)
**CI #45'i oku** — `paket kapisi` (ubuntu) + `paketten kosum` (üç platform). YEŞİL TİK YETMEZ:
windows kolunda `isir : exit 2 ✓ (kabul 0/2)` ve `SONUC: YESIL — paketten acilmis motor TAZE
projede kur→kapi→isir kosdu` satırları aranır. Yeşilse **madde 4 ✅ VE madde 2 ✅** → BİTTİ 4/6.

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
- `faz0/paketten_kos.py` madde 4'ü CANLI ölçer: paket `zipfile` ile açılır (hedefte `unzip`
  GEREKMEZ → windows kolu çalışır), TAZE projede `kur→kapi→isir`. **Çıkış kodu sözleşmesi
  `hafiza.py` sat. 4845'ten OKUNDU:** `isir` taze projede **2** döner ve bu SAĞLIKLIDIR (M-H1b
  kurulamaz, `derle` koşmadı); **1 ve 4 KIRMIZI**. `|| true` sahte yeşil üretirdi.
  Süre ölçütü <300 sn (madde 4 "5 dakika").
- Ölçüldü (Linux, paketten açılmış motorla): `kur` 0 · `kapi` 0 · `isir` 2 · **toplam 4,8 sn**.
  Üç sabotaj probu ısırdı: motorsuz paket · bozuk motor · `isir` 2 yerine 1 (sözleşme ayrımının
  gerçekten ölçtüğünün kanıtı). Kör-değil ölçümü araca gömülü. Y-2 dört kod sayfasında exit 0.

## ✅ WIN32 DALI KAPISI — MADDE 2(i) KAPANDI (14 Ağu, CI #43 `cde1998`)
Motorda `sys.platform == "win32"` YALNIZ iki yerde (sat. 899 `_surec_yasiyor`→`_surec_yasiyor_win`
= Y-1 · sat. 4877 `_boru_koptu_mu` = Y-3) ve ikisi de hiçbir mutantla ölçülmüyordu; ortak
bataryanın üç platformda koşması bunu KAPATMIYOR (batarya platformdan BAĞIMSIZ davranışı görür).
`faz0/win_dal_mutanti.py`: **ÜÇ kapı, DÖRT mutant, örtüşme yok.**
- KAPI-1 ENVANTER (listelenmemiş platform dalı; `os.name=="nt"`/`platform.system()` de görür —
  eksik dalı KOVALAMAZ, o KAPI-2'nin işi: örtüşme YAPISAL olarak kesildi) · KAPI-2 DAVRANIŞ
  (H-a yönlendirme · H-b ayrım · H-c boru; simülasyon) · **KAPI-3 CANLI** (gerçek ctypes + gerçek
  pid, yalnız win32'de hüküm; başka yerde ÖLÇÜLEMEDİ).
- M-1→KAPI-1 · M-2→H-a · M-3→H-b · M-4→H-c. Windows'ta M-3 KAPI-3'ü de kırmızı yakar; bu ÖRTÜŞME
  DEĞİL, canlı kapının kör olmadığının ölçümüdür (sayıma girmez, ayrı raporlanır).
- **CI #43 (84 iş, 0 başarısız)** windows logunda birebir: `KAPI-3 CANLI : YESIL (gercek ctypes:
  kendi pid VAR, bitmis cocuk YOK)` · `M-3 (KAPI-3 kendi sinamasi) -> KAPI-3 de KIRMIZI ✓` ·
  `SONUC: YESIL — uc kapi da temiz, 4/4 mutant AYRI eksende ISIRDI.` ("YESIL SINIRLI" DEĞİL
  "YESIL" demesi, dalın gerçekten alındığının kanıtıdır.)
- BEYAN — ölçülmeyen: Dal B'nin TÜMDEN silinmesinin AYRI mutantı yok (H-c yakalar, tek kapı);
  H-b'nin beş halinden yalnız 259'un mutantı var. Aracın başlığında yazılı, gizlenmedi.

## 🟢 MADDE 6 SAATİ — 14 Ağu başladı, 21 Ağu biter
`devral` gerçek Windows'ta `Desktop\Uygulama - Tuzak Avcisi` (421 MB / 1001 dosya / git'li):
exit 0. `PROJE_HAFIZA.md`: 0 satır silindi, 10 eklendi, yedek bit-bit alındı.

## ✅ BUGÜN KAPANANLAR (tek satır — ayrıntı git geçmişinde)
- **Taze Windows koşumu** (`%TEMP%\hk-taze`, gerçek Windows): `kur`=0 · `kapi`=0 · `isir`=2 →
  **34/34 koşulan mutant ISIRDI**, Linux'la ÖZDEŞ. Madde 2(ii)'nin ölçüm tabanı budur.
- **Yol ayracı körlüğü**: `os.path.relpath` 22 kez elle çevriliyordu (18'i koşulsuz = D-1 ihlali).
  `_rel()` + 21 çağrı; motor `dffe3ce6…`→**`82c6e91b…`**; altın küme FARK YOK (22 ölçüm bit-bit).
  `faz0/yol_ayraci_kapisi.py` iki kapı/üç mutant; eski motora karşı KIRMIZI, 21 kaçak.
- **CI #41→#42→#43**: #41 KIRMIZI (araç KENDİ çıktısındaki U+2713'te çöktü) →
  `_cikti_kodlamasini_guvenceye_al()`; #42 81 iş / #43 84 iş, ikisi de 0 başarısız.

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
- `ruff/mypy/bandit` işi YALNIZ `skill/scripts/hafiza.py`'yi tarar; `faz0/` lint edilmez.
- `ci_kapsam_kapisi.py` deseni `faz0/*_mutanti.py`'dir; `yol_ayraci_kapisi.py` ve `paketten_kos.py`
  bu desene GİRMEZ (CI işleri elle konur).
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

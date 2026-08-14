# DURUM — hafiza-kur
**BİTTİ sayacı: 2 ✅ / 6** (madde 2 yarım: (ii) ✔ · (i) kod yazıldı, CI hükmü bekleniyor) (liste 14 Ağu 2026'da KİLİTLENDİ — ölçütler `CLAUDE.md` §2'de)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB, yerinde güncellenir

## Son yapılan (14 Ağu, tek oturum)
Esaslar v2 kilitlendi (`8c0d040`) · `cmd_*` KESİLDİ · %10 oran kuralı silinip amaç kapısı geldi ·
`.skill` üretilip taze projede koştu (5 sn, Linux) · **`devral` GERÇEK Windows'ta gerçek projede
koştu (exit 0)** · yol ayracı körlüğü kapatıldı · **iki `win32` dalı mutantlandı.**

## ✅ TAZE WINDOWS KOŞUMU (14 Ağu 15:33, commit `b7d753a` sonrası — yamalı motor)
`%TEMP%\hk-taze` (taze git deposu), GERÇEK Windows: `kur`=0 · `kapi`=0 ("YEŞİL SINIRLI", H9
ÖLÇÜLEMEDİ çünkü henüz commit yok) · `isir`=2 → **34/34 koşulan mutant ISIRDI**, 2 SINANMADI
(M-H1b, M-DEVIR — testin kendi eksiği, kapı körlüğü değil), H9 için mutant yok.
Linux koşumuyla ÖZDEŞ. Bu, `_rel` yamasının (82c6e91b) gerçek Windows'ta da doğrulanmasıdır.
**Madde 2'nin (ii) yarısı KARŞILANDI** — şerh: koşan şey depodaki `skill/scripts/hafiza.py`,
paketten AÇILMIŞ `.skill` değil. Motor baytı aynı ama "paketi kurup koşturma" adımı hâlâ
ÖLÇÜLMEDİ; madde 4 bu yüzden açık. Elimdeki `.skill` de artık BAYAT (dffe3ce6 ile üretildi).

## Sıradaki iş (tek madde)
**CI #43'ü oku** — `win dal mutanti` işi üç platformda. YEŞİL TİK YETMEZ: windows kolunun
çıktısında `KAPI-3 CANLI : YESIL` satırı ARANIR (ubuntu/macOS'ta o satır "ÖLÇÜLEMEDİ" der ve
YEŞİL SAYILMAZ) ve `M-3 (KAPI-3 kendi sinamasi) -> KAPI-3 de KIRMIZI ✓` satırı bulunmalıdır.
Yeşilse madde 2 ✅ olur (BİTTİ 3/6); sıra madde 4'e (`.skill` paketten kurulup taze projede) geçer.

## ✅ WIN32 DALI KAPISI (14 Ağu — kod yazıldı, CI hükmü bekleniyor)
Motorda `sys.platform == "win32"` YALNIZ iki yerde: sat. 899 `_surec_yasiyor`→`_surec_yasiyor_win`
(Y-1) ve sat. 4877 `_boru_koptu_mu` (Y-3). İkisi de `faz0/` ve `capraz.yml`'de hiç geçmiyordu;
ortak bataryanın üç platformda koşuyor olması bunu KAPATMIYOR (batarya platformdan BAĞIMSIZ
davranışı görür). `faz0/win_dal_mutanti.py`: **ÜÇ kapı, DÖRT mutant, örtüşme yok.**
- KAPI-1 ENVANTER (listelenmemiş platform dalı; `os.name=="nt"` ve `platform.system()` idiomlarını
  da görür — eksik dalı KOVALAMAZ, o KAPI-2'nin işi; ayrım örtüşmeyi yapısal olarak keser) ·
  KAPI-2 DAVRANIŞ (H-a yönlendirme · H-b ayrım · H-c boru; simülasyon) ·
  KAPI-3 CANLI (gerçek ctypes + gerçek pid, YALNIZ win32'de hüküm verir; başka yerde ÖLÇÜLEMEDİ).
- M-1→KAPI-1 · M-2→H-a · M-3→H-b · M-4→H-c. Windows'ta M-3 KAPI-3'ü de kırmızı yakmalı; bu
  ÖRTÜŞME DEĞİL, canlı kapının kör olmadığının ölçümüdür ve ayrı raporlanır.
- Ölçüldü (Linux): 4/4 ISIRDI, örtüşme yok, temiz motor yeşil; cp1252/cp1254/ascii/utf-8
  dördünde de exit 0 (Y-2 koruması baştan kondu). Beş sabotaj probu (Dal B tümden silme ·
  yardımcı hep True · hata 87 · ENOSPC yutma · `os.name` ile gizlenen dal) beşi de ısırdı.
- `ci_kapsam_kapisi.py` yeni betiği ölçtü: CI işi eklenmeden KIRMIZI, eklendikten sonra YEŞİL.
- BEYAN — ölçülmeyen: Dal B'nin TÜMDEN silinmesinin AYRI mutantı yok (H-c yakalar, tek kapı);
  H-b'nin beş halinden yalnız 259 halinin mutantı var. Gizlenmiyor, aracın başlığında yazılı.

## ✅ YOL AYRACI KAPISI (14 Ağu — bulgu KAPANDI)
`os.path.relpath` motorda 22 kez elle çevriliyordu (18'i koşulsuz = D-1 ihlali, 4'ü hiç) →
kaçak üreticisi. `_rel(p, kok)` eklendi, **21 çağrı** ona çevrildi; motor `dffe3ce6…` →
**`82c6e91b…`** · 5.185 → 5.203 satır. Eşdeğerlik: altın küme `--karsilastir` → **FARK YOK,
22 ölçüm bit-bit aynı.** `faz0/yol_ayraci_kapisi.py`: İKİ kapı, ÜÇ mutant, örtüşme yok
(M-1→KAPI-1 · M-2→H-a · M-3→H-b). Eski motora karşı KIRMIZI, 21 kaçak.

## 🟢 MADDE 6 SAATİ — 14 Ağu başladı, 21 Ağu biter
`devral` gerçek Windows'ta, `Desktop\Uygulama - Tuzak Avcisi` (421 MB / 1001 dosya / git'li):
exit 0. `PROJE_HAFIZA.md`: 0 satır silindi, 10 eklendi, yedek bit-bit alındı.

## ✅ CI #41 → #42 (kapandı)
#41 KIRMIZI: `yol_ayraci_kapisi` KENDİ çıktısındaki U+2713'te çöküyordu
(`UnicodeEncodeError: 'charmap'`). `_cikti_kodlamasini_guvenceye_al()` eklendi.
**#42 (`478003f`) ÖLÇÜLDÜ: 81 iş, 0 başarısız; `yol ayraci kapisi` üç platformda da success;
windows log satırları Linux'unkiyle birebir aynı, U+2713 sağlam.** Ders `CLAUDE.md` §4'te.

## Bilinen sınırlar (ölçülmüş)
- 🔴 **Artefakt BOYUTU içerik oracle'ı DEĞİLDİR.** Ölçüldü 14 Ağu (CI #42, 16 artefakt ailesi):
  `size_in_bytes` ZIP boyutudur; içerik aynıyken windows−ubuntu farkı −2…+2 salınıyor
  (`h11-kenar` 1005/1004/1006). `yol-ayraci`ndaki 465 vs 458 farkı satır-sonu çevirimidir
  (çıktı 485 B / 10 satır). "Üçü de N bayt olmalı" bir KAPI DEĞİLDİR; hüküm iş sonucundan ve
  log metninden okunur. *(Sınıf ilk kez ısırdı — §8 gereği kapı yazılmadı.)*
- ✏️ `.github/workflows/*` köprüden YAZILABİLİYOR: `device_commit_files` reddediyor ama
  `device_bash` yazıyor (ölçüldü 14 Ağu). *(Mount hâlâ `unlink` vermiyor — silmek yerine
  `fable dosyalama/_to_delete/` altına TAŞI.)*
- 🔴 **`hafiza.py` BAĞLI KLASÖRDE KOŞTURULMAZ.** H9 kapısı `git -C <kok> status --porcelain`
  koşuyor; mount `unlink` vermediği için `.git/index.lock` KALICI kalır (B4-1'in aynısı,
  tetikleyen ARACIN KENDİSİ). Hedefte git varsa YERLİ kabukta (PowerShell) koşulur.
- 🔴 **`paketle.sh`'in SHA256 kapısı ÖLÜ.** Başlığı "beyanla tutmazsa DURUR" diyor ama `SKILL.md`'de
  SHA bilinçli olarak YOK (SKILL.md sat. 246); kontrol `[ -n "$BEYAN" ]` ile korunduğu için
  atlanıyor ve paket sessizce üretiliyor. Sınıf İKİNCİ kez ısırdı (1: LİSANS, 10 Ağu). Düzeltme tek
  dokunuş: başlık + ölü `if` gerçeğe çekilir. Yeni faz0 aracı DEĞİL.
- 🟡 **Beyan ile mtime çelişince ölçen kapı YOK.** Ölçüldü: Tuzak Avcisi `PROJE_HAFIZA.md` mtime
  5 Ağu 22:34, içindeki "Son güncelleme" 25 Tem → 11 gün. §8 gereği kapı YAZILMADI (sınıf ilk kez
  ısırdı); ikinci ısırıkta H12'ye "İŞARET" hali eklenir — hüküm değil.
- **CI'da `continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — kırmızısı yutulur.
  Bilinçli olanlar: `kanit`in ölçüm adımları (hüküm kapısı HARİÇ) · `win_kill_probu` (Y-1) ·
  `boru_probu` (Y-3) · `ortam` · `kalite`. Y-1'in exit 1'i arıza değil, sözleşmesi.
- `ruff/mypy/bandit` işi YALNIZ `skill/scripts/hafiza.py`'yi tarıyor; `faz0/` lint edilmiyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ (salt-okunur dizin, chmod 500 root'ta ısırmaz).
- Dört ölçümün koşucusu pakette yok (2.330 traceback avı · kayıpsızlık 50× · normal hafta ·
  2.000 dosyalı depo) — beyandır, doğrulanamaz.
- Kilit inode yarışı DARALTILDI, kapatılmadı. Zincir anahtarsız (bilinçli).
- `faz0/win_yol_probu.py` CI'da koşmaz ve gerekmiyor: tek seferlik erken-uyarı aracıydı; ayakta
  duran kapı `altin_cikti`.
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

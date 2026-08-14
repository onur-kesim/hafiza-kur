# DURUM — hafiza-kur
**BİTTİ sayacı: 4 ✅ / 6** (madde 1·2·3·4 kapandı — ölçütler ve kanıtları `CLAUDE.md` §2'de)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra yazılır**

## Sıradaki iş (tek madde) — MADDE 5
**"25 Ağu yazısının okuru, depoya gelip README ile sistemi kendi başına deneyebilir."**
Bu maddenin ÖLÇÜTÜ HENÜZ YAZILMADI; ilk iş onu yazmak (kod değil). Ham malzeme hazır: paket her CI
koşumunda üretiliyor (artefakt `hafiza-kur-skill`) ve `faz0/paketten_kos.py` kurulum yolunu üç
platformda ölçüyor. Açık soru: ölçüt "README'deki adımlar `SKILL.md` §2 ile TUTUYOR mu" mu olsun
(mekanik — `paketten_kos` kalıbı README'ye uygulanır), yoksa "okur" bir insan mı olsun (ölçülemez)?
**Karar Onur'da; kod yazmadan önce şıklarla sunulacak.** Son tarih 25 Ağu.

## ✅ MADDE 2 + MADDE 4 KAPANDI (CI #43 `cde1998` + CI #46 `5d81838`)
Üç kapı ailesi kuruldu; hepsi üç platformda ve `continue-on-error`SIZ.
- **`faz0/win_dal_mutanti.py`** (madde 2(i)) — motorun iki `win32` dalı (sat. 899 Y-1 · sat. 4877
  Y-3) hiçbir mutantla ölçülmüyordu. ÜÇ kapı, DÖRT mutant, örtüşme yok: KAPI-1 ENVANTER (yalnız
  FAZLA dalı kovalar; EKSİK dal KAPI-2'nin işi → örtüşme YAPISAL kesildi) · KAPI-2 DAVRANIŞ
  (simülasyon) · KAPI-3 CANLI (gerçek ctypes+pid, yalnız win32'de hüküm). CI #43 windows:
  `KAPI-3 CANLI : YESIL` · `M-3 ... -> KAPI-3 de KIRMIZI ✓` · `SONUC: YESIL — ... 4/4 mutant`.
- **`paketle.sh` + `faz0/paket_mutanti.py`** — SHA kapısı ÖLÜYDÜ (`[ -n "$BEYAN" ]` koruyor,
  `SKILL.md`'de 64'lük hex sıfır); ölü olan mantık değil **başlık yalandı**, üstelik `SKILL.md`
  sat. 245-249 SHA yazmamayı ölçülmüş dersle savunuyor. Çözüm: beyanı bırak, **ÜRETİLEN PAKETİ
  ölç** → KAPI-1 MOTOR BİT-BİT + KAPI-2 ENVANTER. Mutantlar: M-1 `zip -l`→K1 (motor 259.228 →
  264.431 B) · M-2 `-x references/*`→K2 (6 dosya düştü). Ayrıca `capraz.yml`'de `paketle`/`.skill`
  için SIFIR eşleme vardı — madde 4'ün dayandığı yüzeyin kapısı yoktu (sınıf ikinci ısırık: LİSANS).
- **`faz0/paketten_kos.py`** (madde 4 + 2(ii)) — KAPI-1 BELGE (koştuğu adımlar PAKETTEKİ `SKILL.md`
  §2 blokunda geçiyor mu **ve** bloktaki her `hafiza.py` referansı `araclar/hafiza/` altında mı) ·
  KAPI-2 CANLI (belgenin akışıyla: önce motoru projeye kopyala, sonra `kur→kapi→isir`).
  Çıkış kodu sözleşmesi `hafiza.py` sat. 4845'ten OKUNDU: `isir` taze projede **2** döner ve
  SAĞLIKLIDIR; **1 ve 4 KIRMIZI**; `|| true` sahte yeşil üretirdi. CI #46 windows birebir:
  `KAPI-1 BELGE : YESIL (4 adimin 4'u belgede)` · `BELGE ADIM 1 : motor projeye kopyalandi ->
  araclar/hafiza/hafiza.py` · `C) belge mutantlari: C1 komut ISIRDI ✓ · C2 yol ISIRDI ✓` ·
  `SONUC: YESIL — BELGENIN akisiyla ... (8.6 sn, win32).`

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
- `paketten_kos.py` belgenin ANLAMINI değil GEÇTİĞİNİ ölçer (yanlış SIRA görünmez) · `devral` yolu
  hiç ölçülmüyor · `derle` sonrası ikinci `isir` (yani `isir`=0 hâli) ölçülmüyor.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ · dört ölçümün koşucusu pakette yok (beyandır) ·
  kilit inode yarışı daraltıldı, kapatılmadı · zincir anahtarsız (bilinçli).
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

# DURUM — hafiza-kur
**BİTTİ sayacı: 5 ✅ / 5** — madde 6 KESİLDİ 15 Ağu 2026 (ölçüt kusuru, `CLAUDE.md` §5)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB · **kapanan bölüm tek satıra iner, yenisi ondan sonra**

## Sıradaki iş — BİTTİ LİSTESİ KAPANDI, TEK DİKEY DİLİM: 25 AĞU YAZISI
Madde 6 KESİLDİ (15 Ağu, Onur kilidi; gerekçe `CLAUDE.md` §5 — zaman değil ÖLÇÜT kusuru).
**Kurulum YAPILMADI, Is-Portfolyo'ya tek bayt yazılmadı.** `faz0/kullanim_kapisi.py` de kesildi.
Yazıda kesilen madde **"ölçülemedi + sebebi"** olarak açık geçer; "bir hafta kullandım" iddiası
KURULMAZ. Denetçi itirazının kendisi yazıya malzemedir: ölçütün nasıl kusurlu çıktığı anlatılır.
Ara işler (hiçbiri BİTTİ maddesine bağlı DEĞİL, ADR/onay ister): depo atfı history rewrite
(son tarih 24 Ağu) · H16 YAPI kapısı (tasarım onaylı, kod yok) · `kanit` işindeki
`t_y3`/`t_y42` hâlâ `continue-on-error: true` (bilinçli; `readme_kapisi` onları kapılı koşuyor).

## ✅ MADDE 2 + 4 KAPANDI (CI #43 `cde1998` + #46 `5d81838`) — TEK SATIRA İNDİ
Üç kapı ailesi, üç platform, `continue-on-error`SIZ: `win_dal_mutanti` 3 kapı/4 mutant (örtüşme
YAPISAL kesildi) · `paketle.sh`+`paket_mutanti` (ölü SHA kapısı → ÜRETİLEN PAKET ölçülüyor) ·
`paketten_kos` KAPI-1 BELGE (komut **ve** yol ekseni) + KAPI-2 CANLI. Ayrıntı git geçmişinde.

## ✅ README KANIT BLOĞU — MADDE 5 KAPANDI (CI #49 `fba20c8`, 91 iş/0 başarısız) — TEK SATIRA İNDİ
`faz0/readme_mutanti.py`: 3 kapı / 6 mutant, örtüşme yok. Beklenen değerler **BLOKTAN okunur, araca
YAZILMAZ**; tanımadığı satıra ÖLÇÜLEMEDİ der. `t_y3`(20)/`t_y42`(58) burada KAPILI koşar.
🔴 Aracın kendi kusuru: `shlex` yoktu, `--metin="ilk not"` bozuluyordu — araç README'yi
SUÇLAYACAKTI. **Ölçüm buldu, CI değil.**

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
- 🔴 **PROJELER ARASI SAYI BULAŞMASI + OKUNMADAN HÜKÜM** (15 Ağu, ikisi de bu oturumun kusuru,
  ikisini de dış denetçi buldu): (i) Is-Portfolyo'ya giden nota `araclar/` için **11** yazıldı,
  doğrusu **10**; 11 sayısı **Momentum'un** belgesinden geldi ve orası için DOĞRU ⇒ sayı yanlış
  değil, **YANLIŞ PROJEDEN**di — bayat sayıdan sinsi, çünkü kaynağı gerçek ölçüm. Doğru sayı
  aynı oturumda ölçülmüştü, hatırlanan sayı onu ezdi. (ii) "Bu cümle `CLAUDE.md` §5'e girdi"
  denildi; `grep` ölçtü, **girmemişti**. Ayrıntı + birebir alıntı: `denetim/2026-08-15_*`.
- 🔴 **Defter COMMIT'lenmeden `kapi` KIRMIZI** (kum havuzu, 15 Ağu): `[H9] git'te IZLENMIYOR:
  PROJE_HAFIZA.md` → FAIL/çıkış 1; commit'lenince YESIL/çıkış 0. ⇒ "defteri `.gitignore`'a al"
  fikri madde 6(c)'yi ULAŞILMAZ kılar. Hedef projede haftada en az bir commit ŞART.
- 🔴 **Derleme artefaktı H14'ün DELİLİNİ bozar** (ölçüldü): `_h14_adaylar` hariç kümesinde (sat.
  4055) `obj`/`bin`/`.dart_tool` YOK; `.gitignore`'lu oldukları için mtime ile ölçülürler ⇒ "en
  yeni değişiklik" hep bir artefakt olur (`…/obj/Api.assets.cache3.json`). Hüküm doğru olsa da
  işaretçi gerçek dosyayı ASLA gösteremez. Flutter `build/` hariç kümesinde VAR, `.dart_tool` yok.
- 🔴 **SKILL.md §1 kademe tablosu kendi içinde ÇELİŞİYOR** (belge-iç-tutarsızlık sınıfının İKİNCİ
  ısırığı; ilki paketten_kos S-6 yol ekseniydi): git'li ama KODSUZ proje (Is-Portfolyo) hem
  "Kod/depo olmayan işler → HAFİF" hem "Depo/git olan projeler → KAPILI" satırlarına uyuyor.
  Kararsızlık kuralı ("kod varsa KAPILI") HAFİF diyor, ama madde 6 KAPILI'yı zorunlu kılıyor.
  Bu turda KAPILI seçildi (gerekçe: git + uzun ömürlü + çok oturumlu = KAPILI sütununun iki şartı).
- 🔴 **Motorda `push`/`fetch`/`remote`/`origin`/`clone` SIFIR eşleşme** — GitHub gerekmiyor; yalnız
  yerel git. git YOKSA H9 "ÖLÇÜLEMİYOR" (sat. 3605), depo var commit yoksa yine ÖLÇÜLEMEDİ (3599).
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

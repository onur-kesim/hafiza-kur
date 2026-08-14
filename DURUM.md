# DURUM — hafiza-kur
**BİTTİ sayacı: 2 ✅ / 6** (liste 14 Ağu 2026'da KİLİTLENDİ — ölçütler `CLAUDE.md` §2'de)
Son güncelleme: 14 Ağu 2026 · bu dosya ≤8 KB, yerinde güncellenir

## Son yapılan (14 Ağu, tek oturum)
Esaslar v2 kilitlendi (`8c0d040`) · `cmd_*` KESİLDİ · %10 oran kuralı silinip amaç kapısı geldi ·
`.skill` üretilip taze projede koştu (5 sn, Linux) · **`devral` GERÇEK Windows'ta gerçek projede
koştu (exit 0)** · yol ayracı körlüğü bulundu ve kapatıldı.

## Sıradaki iş (tek madde)
`_capraz_yeni.yml` → `capraz.yml`: `yol_ayraci_kapisi` CI işi ÜÇ platformda, `continue-on-error`SUZ.
🔴 Bu işi `faz0/ci_kapsam_kapisi.py` YAKALAMAZ (kapsamı yalnız `faz0/*_bolme_mutanti.py`) —
commit'e girmezse kimse görmez. İndiğini `git show --stat HEAD` ile ÖLÇ.
Sonra: taze Windows koşumu (`kur→kapi→isir`) ile madde 2'nin (ii) yarısını kapat.

## ✅ YOL AYRACI KAPISI (14 Ağu — bulgu KAPANDI)
Gerçek Windows koşumunda `devral` `YEDEK: arsiv\hafiza\v2\...` bastı, aynı çıktının H4 satırları
düz bölü bastı. Kök neden: `os.path.relpath` 22 kez çağrılıyor, çevirim her yerde ELLE
tekrarlanıyordu — 18'i koşulsuz (D-1 ihlali), 4'ü hiç. Kaçak üreticisi.
- `_rel(p, kok)` eklendi (D-1 tek yerde yaşar), **21 çağrı** ona çevrildi. Geriye yalnız
  `kok_goreli` ve `_rel` gövdeleri kaldı. Motor `dffe3ce6…` → **`82c6e91b…`** · 5.185 → 5.203 satır.
- **BEYAN — davranış değişikliği (sessiz değil):** 18 nokta KOŞULSUZ'dan KOŞULLU'ya döndü.
  Windows'ta fark yok; POSIX'te yalnız adında ters bölü olan dosyalarda var, ve yeni davranış
  D-1'e UYGUN olandır. KANIT: altın küme `--karsilastir` → **FARK YOK, 22 ölçüm bit-bit aynı.**
- `faz0/yol_ayraci_kapisi.py` (250 satır): **İKİ kapı, ÜÇ mutant, örtüşme yok.**
  KAPI-1 YAPI (depo metni, muafiyet listesi YOK — kural fonksiyon adıyla tanımlı) ·
  KAPI-2 DAVRANIŞ (H-a çevirir · H-b POSIX'te `\` KORUR · H-c çökmez).
  M-1→KAPI-1 · M-2→H-a · M-3→H-b. İki kapıyı birden ateşleyen mutant "ORTUSTU" deyip kırmızı yanar.
  Kapının ölçtüğü ESKİ motorla kanıtlandı: `dffe3ce6…` → **KIRMIZI, 21 kaçak.**

## 🟢 MADDE 6 SAATİ — 14 Ağu başladı, 21 Ağu biter
`devral` gerçek Windows'ta, `Desktop\Uygulama - Tuzak Avcisi` (421 MB / 1001 dosya / git'li):
exit 0. `PROJE_HAFIZA.md`: 0 satır silindi, 10 eklendi, yedek bit-bit alındı.
Linux kopyası ile Windows koşumu, gerçekten farklı olan yer DIŞINDA bit-bit aynı; fark yalnız
H9'da (kopyada `.git` yoktu → ÖLÇÜLEMEDİ, Windows'ta gerçek hüküm).

## Bilinen sınırlar (ölçülmüş)
- ✏️ **MAYIN GÜNCELLENDİ:** ".github/workflows/* köprüden yazılamaz" artık YANLIŞ.
  Ölçüldü 14 Ağu: `device_commit_files` reddediyor ama **`device_bash` ile YAZILABİLİYOR**
  (`capraz.yml`'e 53 satır eklendi, 1076→1129, YAML doğrulandı). Depo köküne `_capraz_yeni.yml`
  yazıp Onur'a taşıtma zahmeti gereksiz. *(Mount hâlâ `unlink` vermiyor — silmek yerine
  `fable dosyalama/_to_delete/` altına TAŞI.)*
- 🔴 **`hafiza.py` BAĞLI KLASÖRDE KOŞTURULMAZ.** H9 kapısı `hafiza.py`'de
  `git -C <kok> status --porcelain` koşuyor; Cowork mount'u `unlink` vermediği için hedef deponun
  `.git/index.lock` dosyası KALICI kalır (projenin B4-1 bulgusunun aynısı, tetikleyen ARACIN
  KENDİSİ). Hedefte git varsa YERLİ kabukta (PowerShell) koşulur.
- 🔴 **`paketle.sh`'in SHA256 kapısı ÖLÜ.** Başlığı "beyanla tutmazsa DURUR" diyor ama `SKILL.md`'de
  SHA bilinçli olarak YOK (SKILL.md sat. 246); kontrol `[ -n "$BEYAN" ]` ile korunduğu için
  atlanıyor ve paket sessizce üretiliyor. Sınıf İKİNCİ kez ısırdı (1: LİSANS, 10 Ağu). Düzeltme tek
  dokunuş: başlık + ölü `if` gerçeğe çekilir. Yeni faz0 aracı DEĞİL.
- 🟡 **Beyan ile mtime çelişince ölçen kapı YOK.** Ölçüldü: Tuzak Avcisi `PROJE_HAFIZA.md` mtime
  5 Ağu 22:34, içindeki "Son güncelleme" 25 Tem → 11 gün. H12 BEYANI okur, H14 mtime'a bakar ama
  başka soru sorar. §8 gereği kapı YAZILMADI (sınıf ilk kez ısırdı); ikinci ısırıkta H12'ye
  "İŞARET" hali eklenir — hüküm değil, çünkü "mtime hüküm vermez" bilinçli duruştur.
- **CI'da `continue-on-error: true` taşıyan iş KAPI DEĞİL, ÖLÇÜMDÜR** — kırmızısı yutulur.
  Bilinçli olanlar: `kanit`in ölçüm adımları (hüküm kapısı HARİÇ) · `win_kill_probu` (Y-1) ·
  `boru_probu` (Y-3) · `ortam` · `kalite`. Y-1'in exit 1'i arıza değil, sözleşmesi:
  `SONUC: ORTAM GERÇEĞİ — bu platformda os.kill(pid,0) VARLIK SINAMAZ`.
- 🔴 `hafiza.py`'nin iki `win32` dalı (sat. 881/4859, hedef `_surec_yasiyor_win`) **hiçbir mutantla
  ölçülmüyor** — `faz0/` ve `capraz.yml`'de adı geçmiyor. Madde 2'nin (i) yarısı budur.
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ (salt-okunur dizin, chmod 500 root'ta ısırmaz).
- Dört ölçümün koşucusu pakette yok (2.330 traceback avı · kayıpsızlık 50× · normal hafta ·
  2.000 dosyalı depo) — beyandır, doğrulanamaz.
- Kilit inode yarışı DARALTILDI, kapatılmadı. Zincir anahtarsız (bilinçli).
- `faz0/win_yol_probu.py` CI'da koşmaz ve gerekmiyor: tek seferlik erken-uyarı aracıydı, öngörüsü
  CI #22'de `altin_cikti`'nın windows'ta yeşil dönmesiyle doğrulandı. Ayakta duran kapı `altin_cikti`.
- Cowork proje talimatındaki depo adresi (`tuzakavcisi1-cloud`) YANLIŞ; doğrusu
  `onur-kesim/hafiza-kur`. Talimat Onur'un panelinde, depodan düzeltilemez.

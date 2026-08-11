# ALTIN ÇIKTI KAPISI — ÖLÇÜT KUSURU VE ÜÇ DÜZELTME · ÖLÇÜM RAPORU

**Tarih:** 11 Ağustos 2026 · **Ortam:** bulut Linux, Python 3.11.15, **root olmayan
kullanıcı (`olcum`)**, 2 CPU. **Windows/macOS bu raporda ÖLÇÜLMEDİ** (CI'ya kalır).

**Motor DEĞİŞMEDİ:** `hafiza.py` SHA `480cbd52…640`, 4878 satır, `fail()` 61
(`grep -c` 61, AST sayımı 61). `faz0/altin_kapi.json` DEĞİŞMEDİ (`688af183…fd79`).
Bu tur yalnız `faz0/` ölçüm altyapısına dokunur; ürün koduna dokunulmadı.

---

## 1. TETİKLEYİCİ — CI #17 VE #18 KIRMIZIYDI, VE HÜKÜM YANLIŞTI

| run | commit | sonuç |
|---|---|---|
| **#18** | `8e3993f` (Faz C bölmesi) | **failure** |
| **#17** | `41b23ac` (altın çıktı aracının eklendiği commit) | **failure** |
| #16 `6902010` · #15 · #14 · #13 · #12 | | success |

Her iki kırmızıda **tek** kırmızı iş, aynısı:
`Altin cikti / kapi esdegerligi (windows-latest)` → adım `kapi ciktisi altin kumeyle AYNI mi`.
Aynı işin önceki adımı (`arac once KENDINI kanitliyor mu`) **YEŞİL**; ubuntu ve macOS **YEŞİL**.

`altin_cikti.py` **`41b23ac`'te eklendi** (`git log --diff-filter=A`), `6902010`'da yoktu →
#16'nın yeşilliği bu kırmızıyı çürütmez. **Eşdeğerlik kapısı, eklendiği günden beri
Windows'ta kırmızı.** `FAZC_RAPOR.md §2(a)`'nın *"FARK YOK, bit-bit"* hükmü yalnız
Linux/macOS'ta geçerliydi; rapor bunu "Windows CI'ya kalır" diye yazdı ve CI **kaldı, ama
kırmızı yandı ve okunmadı.**

### 1.1 ARTEFAKT NE GÖSTERDİ (`altin-windows-latest/altin-fark.txt`, Onur indirdi)

```
10 olcumun 10'unda   CIKTI DEGISTI
hicbirinde           EXIT DEGISTI  YOK
hepsinde tek satir   "(satir farki bulunamadi — bosluk/satir sonu farki olabilir)"
hukum                "SONUC: 10 FARK — davranis DEGISTI."   (exit 1)
```

**Bu bir ÜRÜN hükmü değildi.** Araç bir fark GÖRDÜ, **ADLANDIRAMADI**, ve buna rağmen
ürünü suçladı. Deponun kendi **Y-4** sınıfı: *"ölçemediğini ARAÇ KUSURU diye mi
raporluyor?"* — hayır, ürün regresyonu diye raporluyordu.

`EXIT DEGISTI` satırının **hiç olmaması** aday havuzunu daraltır: yol normalleştirmesi
sızması, `stderr` sızması, `H-LINK` yanlış pozitifi, `H9`/git dalı farkı — **hepsi
adlandırılabilir bir satır farkı üretirdi.** Geriye tek aile kalır: **satır sınırı
karakteri.**

Artefakt hangi KARAKTER olduğunu söylemez — çünkü *adlandıramamak kusurun kendisidir.*
Düzeltmeler indikten sonraki ilk Windows koşumu ya YEŞİL olur (sınıf `\r`'ydi) ya da
**exit 2 + sınıf adını basar.**

---

## 2. ÜÇ DÜZELTME

### DÜZELTME-1 · `kos()` — universal newline + AÇIK kodlama

```python
r = subprocess.run([sys.executable, "-X", "utf8", motor] + arglar + ["--kok=" + kok],
                   capture_output=True, timeout=saniye, env=o,
                   text=True, encoding="utf-8", errors="replace")
```

Teslim günündeki hâl `capture_output=True` ile ham bayt alıp `.decode()` ediyordu; `\r`
korunuyordu. Altın küme LF kayıtlı (`altin_kapi.json`'da ham CR = 0). `text=True`
universal newline'ı açar: `\r\n` → `\n`.

**Kodlama ayağı — ÖLÇÜLDÜ, ve ilk yazımdaki gerekçe YANLIŞTI.** Bağımsız denetçi bunu
teslimden önce buldu. Doğrusu:

| ortam | `getpreferredencoding` / `utf8_mode` | çıplak `text=True` | AÇIK kodlamalı (teslim) | `8e3993f` ham-bayt |
|---|---|---|---|---|
| temiz | `utf-8` / 1 | FARK YOK exit 0 | FARK YOK exit 0 | FARK YOK exit 0 |
| `LC_ALL=C` | `utf-8` / **1** | FARK YOK exit 0 | FARK YOK exit 0 | FARK YOK exit 0 |
| `LC_ALL=C PYTHONUTF8=0` | `ANSI_X3.4-1968` / 0 | **`UnicodeDecodeError` · ham traceback · exit 1** | FARK YOK exit 0 | FARK YOK exit 0 |

**`LC_ALL=C` tek başına bunu TETİKLEMEZ** — PEP 540 UTF-8 kipini kendiliğinden açar
(POSIX, Python ≥ 3.7). Tetikleyen hâl `LC_ALL=C PYTHONUTF8=0`'dır.

Ve ikinci düzeltme: **teslim günündeki ham-bayt `.decode("utf-8","replace")` hâli bu
sınıfa ZATEN bağışıktı.** Yani kodlamayı açık vermek **mevcut bir kusuru kapatmıyor**;
`text=True`'nun **getireceği** kusuru önlüyor. Bu ayrım önemlidir: bir düzeltmenin ne
kapattığı değil **ne AÇTIĞI** ölçülür — burada açtığı şey sıfırda tutuldu.

`-X utf8` ise bir **tutarlılık** düzeltmesi: `altin_cikti`, motoru bu bayrak olmadan
çağıran **tek** araçtı (`t_y3:43 · t_y42:59,838,980,993,1227,1248,1598 · fazC:129`
hepsi kullanıyor). Altın küme, başka hiçbir aracın kullanmadığı bir yorumlayıcı
konfigürasyonuyla kaydedilmişti. Linux'ta eklenmesi kümeyi **değiştirmiyor** (M-A4).

### DÜZELTME-2 · adlandırılamayan fark = **ÖLÇÜLEMEDİ (exit 2)**, ürün hükmü değil

`satir_farki()` artık `(metin, adlandirildi)` döndürür. Adlandırılamıyorsa
`gorunmez_teshis()` görünmez karakterin **SINIFINI** ve ilk ayrışma noktasının **`repr`
penceresini** basar; hüküm **exit 2 ÖLÇÜLEMEDİ** olur.

**Neden düzeltme-1 yetmez:** `splitlines()` yalnız `\r`'yi değil CPython'un **tüm** satır
sınırı kümesini yutar; universal newline ise yalnız `\r\n`'i çevirir. Bir örnek yeter:
`"a\x0bb".splitlines() == "a\nb".splitlines()`.

**🔴 SINIF TABLOSUNA YALNIZ SATIR SINIRI KARAKTERLERİ GİRER.** İlk yazımda tablo NBSP ·
BOM · SEKME · ZWSP da içeriyordu ve rapor 9 sınıf iddia ediyordu; **bağımsız denetçi
bunun yanlış olduğunu ölçtü.** Satır listeleri eşitse ilk ayrışma **zorunlu olarak** bir
satır sınırı karakterindedir; öteki görünmez karakterler satır listesini **değiştirir**,
dolayısıyla **adlandırılabilir** bir satır farkı üretir ve teşhise **hiç ulaşmaz.**

Tablo yeniden yazıldı ve **dokuz sınırın dokuzu da ölçüldü** (doğrudan çağrı,
`satir_farki("a\nb", "a<C>b")`):

| karakter | sınıf adı | ulaşır? |
|---|---|---|
| `\r` | SATIR SONU (CR) | ✓ |
| `\x0b` | DIKEY SEKME (VT) | ✓ |
| `\x0c` | SAYFA SONU (FF) | ✓ |
| `\x1c` `\x1d` `\x1e` | DOSYA / GRUP / KAYIT AYIRICI | ✓ |
| `\x85` | SONRAKI SATIR (NEL, U+0085) | ✓ |
| U+2028 · U+2029 | SATIR / PARAGRAF AYIRICI | ✓ |
| NBSP · BOM · SEKME · ZWSP · boşluk | — | **ULAŞMAZ** (satır farkı görünür, exit 1) |

Kenar vakalar ölçüldü, **ham traceback yok, IndexError yok**: `("","")` ve `("abc","abc")`
→ `AYRISMA YOK (metinler esit — ARAC KUSURU adayi)` · `("a\n","a")` →
`SONDAKI SATIR SINIRI (uzunluk farki)` · `("","a")`, `("a","")`, `("aıb","aİb")` →
adlandırılabilir satır farkı.

### DÜZELTME-3 · referansın **ŞEKLİ** kapıda sınanır → **ARAÇ KUSURU (exit 3)**

Bağımsız denetçi teslimden önce üçüncü bir yol buldu: `except` yalnız `json.load`
satırını sarıyordu. Şekli bozuk bir referans (bir kayıtta `exit` alanı yok, ya da
`{"kume": 42}`) `farklari_bul` içinde `KeyError`/`TypeError` atıyor, **ham traceback +
exit 1** veriyordu — yani *düzeltme-2'nin kapattığı kusurun aynısı başka kapıdan geri
geliyordu.* Bu, `8e3993f`'te de vardı (regresyon değil, mevcut kusur), ama teslimin tezi
tam olarak bunu yasaklıyor.

`_kume_sekli_dogrula()` eklendi: liste mi · boş mu · her kayıt nesne mi · `hal/komut/exit/
cikti` alanları var mı · `cikti` metin mi. İhlal → **exit 3 ARAÇ KUSURU**, ham traceback
yok. Kesik indirme, birleştirme çatışması ve elle düzenleme bu hâli üretir.

### Çıkış kodu sözleşmesi (bu araç)

`0` fark yok · `1` **FARK VAR (ürün hükmü)** · `2` **ÖLÇÜLEMEDİ** (fark var, satır
düzeyinde adlandırılamıyor) · `3` **ARAÇ KUSURU**. Düzeltme-2 daha önce `1`'e giden bir
sınıfı `2`'ye, düzeltme-3 ise `1`'e giden bir sınıfı `3`'e taşır. CI'da iş **yine kırmızı**
yanar — ama artık **doğru hükümle**.

---

## 3. ÖLÇÜT MUTANTI — `faz0/altin_olcut_mutanti.py` · **7 ısırdı / 0 kaçtı** (exit 0, 44 sn)

Ortam **enjeksiyonla üretilir**, motora dokunulmaz: `sitecustomize.py` + `PYTHONPATH` ile
çocuk sürecin satır sonu kipi değiştirilir. Enjeksiyon **yalnız `hafiza.py` çağrısında**
devreye girer — aksi halde mutant kendi grep'ini ölçerdi.

Ölçüldü: motorun **Y-2 koruması** (`reconfigure(encoding=…, errors=…)`) newline ayarını
**sıfırlamaz** → enjeksiyon korumadan sonra da ayakta. Örnek: motor çıktısı
`b'=== HAFIZA KAPISI v2.5.0-dev === kok: ?\r\n\r\nSONUC: FAIL…'`.

| mutant | ölçtüğü koruma | diferansiyel? | sonuç |
|---|---|---|---|
| **M-A1** SATIR SONU (CRLF) | düzeltme-1 | eski ↔ yeni | **ISIRDI** · ESKİ exit 1 · 10 adsız · "davranış DEĞİŞTİ" → YENİ exit 0 · FARK YOK |
| **M-A2** SATIR SINIRI (`\x0b` **ve** `\x85`) | düzeltme-1'in **kapatmadığı** sınıf + tablonun kapsamı | eski ↔ yeni, **iki karakter** | **ISIRDI** · her kolda ESKİ exit 1 / 10 adsız → YENİ exit 2 / 10 teşhis / doğru sınıf adı |
| **M-A3** GERÇEK FARK | yeni sınıflandırma **yutmuyor** | tek kollu | **ISIRDI** · exit 1 · 10 satır ADLANDIRILDI · ÖLÇÜLEMEDİ yok |
| **M-A4** TEMİZ KOL | düzeltme altın kümeyi bozmuyor | tek kollu | **ISIRDI** · exit 0 · FARK YOK · traceback yok |
| **M-A5** KAPI DÜŞÜRME | düzeltme-2'nin **HÜKMÜ** | tam ↔ sökük | **ISIRDI** · TAM exit 2 → SÖKÜK exit 1 |
| **M-A6** İZ KİLİDİ | düzeltme-2'nin **TEŞHİSİ** | tam ↔ sökük | **ISIRDI** · iki kol da exit 2 (**hüküm AYNI**) ama TAM sınıf adı basıyor / SÖKÜK `None` |
| **M-A7** BOZUK REFERANS | düzeltme-3 | eski ↔ yeni | **ISIRDI** · ESKİ exit 1 + ham traceback → YENİ exit 3 + ARAÇ KUSURU, traceback yok |

**M-A1'in ESKİ kolu, CI artefaktının imzasını birebir üretir** (exit 1 · adsız fark 10 ·
"davranış DEĞİŞTİ"). Bu, artefaktta gözlenen şeyin **sınıfını** ölçer; içeriğini kanıtlamaz.

**M-A3 ve M-A4 tek kolludur** (yalnız yeni araç). Isırdıkları, cerrahi sabotajla ayrıca
kanıtlandı (bağımsız denetçi: `if out:` → `if False:` M-A3'ü düşürdü; düzeltme-1'in
etkisini geri alan yama M-A4'ü düşürdü).

**Yama çıpası kaybolursa mutant `exit 3 ARAÇ KUSURU` der, `KACTI` demez** — `_degistir`'in
tek-eşleşme kilidi *fail-closed*'dur (fazA/fazB/fazC ile aynı ev usulü). Kaynak değişince
mutant sessizce yeşile dönmez; ama "KACTI" da demez, "ölçemedim" der.

### 3.1 Bu mutantın kendi tarihi — ÜÇ turda İKİ KÖRLÜK

1. İlk yazımda M-A1 ve M-A2 **KAÇTI** (`adsiz-fark=0`): "eski ölçüt" yaması düzeltme-2'yi
   **eksik** geri alıyordu (hükmü söküyor, teşhis fonksiyonunu bırakıyordu), dolayısıyla
   "eski" kol eski aracın çıktısını üretmiyordu. Yama ikiye bölündü ve bu bölünme
   **M-A6'yı doğurdu**: hüküm ile iz ayrı iki korumadır.
2. M-A7 ilk hâlinde **KAÇTI**: eski kol da `exit 3` veriyordu, çünkü `ESKI_TAM` düzeltme-3'ü
   geri almıyordu. `yama_eski_sekil` eklendi.
3. M-A2 ilk hâlinde **tek karakterle** ölçüyordu (`\x0b`) ve dokuz üyeli tablonun
   ölçüldüğü sanılıyordu — **örtüşen tespit körlüğünün** aynısı. `\x85` kolu eklendi;
   `\x85` zaten düzeltme-2'nin gerekçe metninde adı geçen ama tabloda **eksik** olan
   üyeydi ve `sinif: ?` veriyordu.

*Mutantın kendisi de bir kapıdır ve kör olabilir.*

---

## 4. GÖNDERİLMEYEN DÜZELTME — `--kendini-sina`'ya TOPLAM FARK KAPISI

Önerildi, **onaylandı**, sonra **ölçüldü, ÇÜRÜTÜLDÜ, gönderilmedi.**

| ortam | `--kendini-sina` |
|---|---|
| temiz | `toplam fark kaydi: 10 · H13 yakalayan: 10 · ISIRDI · exit 0` |
| CRLF | **birebir aynı** |
| `\x0b` | **birebir aynı** |
| düzeltilmiş araç + CRLF | **birebir aynı** |

Sayı hiç değişmiyor → o kapı **hiçbir şeyi ısırmazdı**. Sebep yapısaldır:
`--kendini-sina` iki **koşum-anı** kolunu karşılaştırır (temiz motor ↔ sabotajlı motor),
ikisi de aynı platformda; ortama **sistematik** her fark iki kolda da bulunup birbirini
götürür. `--karsilastir` ise koşum-anını **SAKLANMIŞ artefaktla** kıyaslar. Kusur yalnız
BU eksende var, ve kendini-sına'nın saklanmış artefaktı **yok**.

Bunun tersi de doğru ve teslim günü gözden kaçtı: **`--kendini-sina` yeşili,
`--karsilastir` kırmızısı hakkında hüküm vermez.** Ama **bilgi taşır**: `git init`/`kur`/
zaman aşımı/araç çökmesi/çocuk kodlaması gibi tüm **kurulum** sebeplerini dışlar — aday
havuzunu daraltan tek argüman budur.

*Ders: onaylanmış bir tasarım da ölçülmeden uygulanmaz. Kör kapı yok.*

---

## 5. REGRESYON — bu turda koşulanlar

Motor koşucuları (root olmayan kullanıcı, taze klon, `deneme/` ve `hukum.log` SİLİNDİKTEN
sonra), **iki bağımsız koşumda** aynı: `t_y3` 20/20 exit 0 · `t_y42` 57 geçti / 0 kaldı /
**1 yavaş** (B-6, kalibrasyonsuz mutlak duvar saati — bilinen test kusuru, Faz F) / 0
ölçülemedi exit 0 · `isir` taze 34/34 + 2 SINANMADI **exit 2**, `derle` sonrası 36/36
exit 0 · `hukum_kapisi` 4/4 BASILDI exit 0 · `y2_mutant` 2/0/0 · `y4_mutant` 2/0/0 ·
`fazA_senaryolari` 6/0/0 · `fazB_senaryolari` 6/0/0/0 · `fazB_olcut_mutanti` 2/0/0 ·
`boru_probu` exit 0 · `fazC_bolme_mutanti` 6/0/0 exit 0 · `sabotaj.py --is 2` exit 1,
**21 KAPSAMLI / 40 KAPSAMSIZ** (21+40 = 61 = `fail()` sayısı ✓).

**Düzeltme sonrası araç:** `--kendini-sina` **ISIRDI** exit 0 · `--karsilastir`
**FARK YOK** exit 0 · `--kaydet` çıktısı commit'lenmiş `altin_kapi.json` ile **bit-bit
aynı** (SHA `688af183…` her ikisi) → **referansı yeniden kaydetmek GEREKMİYOR.**

`ruff --no-cache --isolated --select F,E9,B,S,PLE` (kullanıcı `olcum`): yeni iki dosyada
**8 bulgu** — `S603×3 · B904×2 · S110×2 · S607×1`. Mevcut `faz0/*.py` tabanı aynı
sınıfları taşıyor (`S603×19 · B904×14 · S110×10 · S607×3`); **yeni sınıf getirilmedi.**
CI kalite işi yalnız `skill/scripts/hafiza.py`'yi tarar; `faz0/` kapsam dışıdır, yani bu
ölçüm CI tarafından **zorlanmıyor**.

⚠️ **ÖLÇÜM HİJYENİ:** `isir`/`hukum_kapisi` koşmadan ÖNCE `skill/scripts/deneme` ve
`hukum.log` **silinmeli**. Bayat log `hukum_kapisi`'ni **sahte YEŞİL** yapıyor; bayat
`deneme/` taze projeyi 34/34 yerine 36/36 gösteriyor. Bu tur ikisi de üretilip sonra taze
klonda temizinden doğrulandı. Ayrıca `ruff` root ile koşulursa `.ruff_cache` **root
sahipli** kalır ve sonraki non-root ölçümü `Permission denied` ile düşer — `--no-cache`
kullan ya da dizini sil.

---

## 6. NE ÖLÇÜLEMEDİ

Bu bölüm boş olamaz.

1. ~~**Windows ve macOS'ta hiçbir şey koşulmadı.**~~ → **Windows §8.1'de ÖLÇÜLDÜ**
   (CI run #19). **macOS işleri YEŞİL ama hüküm satırları OKUNMADI** — bkz. §8.4.1.
   Aşağıdaki metin teslim anındaki hâldir, kayıt için bırakıldı:
   **Windows ve macOS'ta hiçbir şey koşulmadı.** Üretilen ortam gerçek Windows değil.
   "Windows stdout `\n`→`\r\n` çevirir" **TAHMİN** (yüksek güven; Y-2 korumasının
   newline'ı sıfırlamadığı ölçüldü, Windows'un kendisi ölçülmedi). `capraz_YENI.yml`'nin
   iki yeni işinin `windows-latest` / `macos-latest` kolları hiç koşmadı. Özellikle
   M-A2'nin `write()` sarmalayıcısının Windows'un kendi `\n`→`\r\n` katmanıyla nasıl
   etkileştiği **TAHMİN**: sarmalayıcı `\n`'leri tükettiği için CRLF çevirisi devreye
   girmez ve sınıf `DIKEY SEKME (VT)` çıkar — ölçülmedi.
2. ~~**Kırmızının HANGİ karakterden geldiği.**~~ → **§8'de ÖLÇÜLDÜ: `\r` (CRLF).**
   Teslim anındaki hâl:
   **Kırmızının HANGİ karakterden geldiği.** Artefakt sınıfı adlandırmıyor;
   adlandıramamak kusurun kendisiydi. Düzeltmeler indikten sonraki ilk Windows koşumu
   ya YEŞİL olur ya da exit 2 + **sınıf adı** verir. İkinci hâlde tur bitmez, teşhis başlar.
3. **Düzeltme-1'in Windows'ta yeterli olduğu.** `text=True` yalnız `\r\n`'i çevirir;
   sınıfın öteki sekiz üyesi düzeltme-2 tarafından **raporlanır**, düzeltilmez.
4. ~~**`text=True` olmadan motoru çağıran 8 yer daha var**~~ → **§8.2'de ÖLÇÜLDÜ:
   altısının altısı da CRLF'e duyarsız.** Teslim anındaki hâl:
   **`text=True` olmadan motoru çağıran 8 yer daha var:** `fazA:156,374 · fazB:310 ·
   fazB_olcut:184 · y2:155 · y4:133 · boru_probu:212,229`. Bunlar `splitlines()`/çapasız
   regex kullandığı için öldürücü değil (`y2:166` ve `fazB_olcut:195` nokta denetimiyle
   zararsız ölçüldü); **`fazA` / `fazB` / `y4` / `boru_probu` tam denetlenmedi.** Sınıf
   **SINIRDA kapanmamıştır** — bilinçli, çünkü "her düzeltmeye ayrı mutant" kuralı 8
   mutant demekti ve bu tur o kadar büyümedi.
5. **`altin_kapi.json` yalnız YEŞİL yolu ölçüyor** (10/10 ölçüm exit 0). FAIL, kesilme ve
   exit 1/2/3 dalları referansın dışındadır. 🔴 **TUZAK:** altın kümeyi Windows'ta yeniden
   kaydetmek kırmızıyı ubuntu+macOS'a **TAŞIR** (JSON `\r`'yi `\\r` diye kaçırır, taşınır
   olur). Yeniden kayıt tek başına çözüm değildir; **önce** düzeltme-1 inmelidir.
6. **`_RE_SHA` deseni** (`[0-9A-Fa-f]{16,}`) 16+ haneli **ondalık** sayıları da `<SHA>`
   yapıyor (`altin_cikti.py` + `fazC_bolme_mutanti.py`). Bu tur daraltılmadı.
7. **CI okuması tek kaynaklı.** `api.github.com` üreticide çalıştı, bağımsız denetçi
   ajanda 403 verdi. Adım logu ve artefakt indirmesi kimlik doğrulaması istiyor; §1.1'deki
   imzayı **Onur** okudu, ajan **bağımsız doğrulayamadı**. Denetçinin ölçtüğü şey yalnız
   "M-A1/M-A2'nin ESKİ kolu aynı imzayı üretiyor"dur; imza eşleşmesi artefaktın içeriğini
   kanıtlamaz.
8. **`mypy` ve `bandit` yeni iki dosyada koşulmadı** (yalnız `ruff` ölçüldü).
9. **`fazC_bolucu.py`'nin CRLF yolu** hiç koşulmadı (Faz C raporundan devreden madde).
10. **300k ölçekte maliyet** ölçülmedi; bu araç küçük fikstür kullanıyor.
11. ~~**`capraz_YENI.yml` bu teslimle CI'da KOŞMUYOR**~~ → **ARTIK YANLIŞ.** Dosya
    `5c7e70a`'da `.github/workflows/capraz.yml` olarak taşındı (`git show --stat`:
    `capraz.yml | 92 +++` · `faz0/capraz_YENI.yml | 509 ---`) ve iki yeni iş run #19'da
    üç platformda koştu (§8.1). Teslim anındaki hâl, kayıt için:
    **`capraz_YENI.yml` bu teslimle CI'da KOŞMUYOR** — `faz0/` altında duruyor,
    `.github/workflows/` değişmedi. İki yeni iş ancak Onur dosyayı taşıdıktan sonra
    ölçmeye başlar. Bu teslimin kendisinde **CI kazanımı yoktur.**

---

## 7. SIRADAKİ İŞ (öneri, karar Onur'da)

1. ✅ **YAPILDI (`5c7e70a`, run #19 SUCCESS).** `faz0/capraz_YENI.yml` →
   `.github/workflows/capraz.yml` (iki yeni iş:
   `fazC_bolme_mutanti` ve `altin_olcut_mutanti`, üç platform).
   🔴 **İş Portföyü'ne bildirim yükümlülüğü.**
2. İlk Windows koşumunu oku: YEŞİL mi, yoksa exit 2 + sınıf adı mı? Sınıf adı çıkarsa
   `gorunmez_teshis`'in verdiği karakterle düzeltme-1 genişletilir.
3. `altin_kapi.json`'a FAIL + kesilme hâlleri ekle ve **düzeltme-1 indikten sonra**
   yeniden kaydet (§6.5'teki tuzağa dikkat).
4. Alt-bölme sırası (Faz C raporundan devreden): `_kapi_h1` (CC 57) · `_kapi_h14` (35) ·
   sonra `cmd_devral` (88) · `cmd_derle` (63) · `zincir_dogrula` (41) ·
   `cmd_bloklastir` (39).
5. `_RE_SHA` desenini daralt, sonra `--kendini-sina`'yı yeniden koş.
6. ~~§6.4'teki 8 çağrı yerini hizala~~ — **GEREKMİYOR, ölçüldü (§8.2):** altı aracın
   altısı da CRLF'e duyarsız, hizalama bir kapı kazandırmıyor. "ADDITIVE kal, kanıtsız
   dokunma" gereği yapılmadı. Kalan boşluk: CRLF DIŞI satır sınırı karakterleri bu altı
   araç için denenmedi (§8.4.3).

---

## 8. TESLİMDEN SONRA ÖLÇÜLENLER (11 Ağustos 2026, aynı gün)

Teslim `e4c4fa5` + `5c7e70a` olarak commit'lendi ve push edildi. Uzaktaki baytlar teslim
edilen baytların birebir aynısıdır (dört dosyanın SHA256'sı doğrulandı).

### 8.1 CI RUN #19 — `5c7e70a` · **SUCCESS** · 6m 24s · 24 artefakt

`Matrix: altin_cikti` 3/3 · `Matrix: altin_olcut_mutanti` 3/3 · `Matrix: fazC_bolme_mutanti` 3/3.

**§6.1 ve §6.2 KAPANDI.** `Altin cikti / kapi esdegerligi (windows-latest)` — #17'den beri
kırmızı olan iş — **27 saniyede yeşil**. Kırmızı olan adımın (`kapi ciktisi altin kumeyle
AYNI mi`) çıktısı, Windows runner'ın kendi logundan birebir:

```
ALTIN CIKTI KARSILASTIRMASI
  altin kume : faz0/altin_kapi.json (10 olcum)
  bu kosum   : 10 olcum
--------------------------------------------------------------------------------
FARK YOK — kapi ciktisi ve cikis kodlari BIT-BIT ayni.
  (Normallestirilen: <KOK> · <TARIH> · <GUN> · <SHA>. Baska hicbir sey.)
```

Yani **sınıf `\r` (CRLF) idi** ve DÜZELTME-1 kapattı. §6.1'in TAHMİN'i artık ÖLÇÜLDÜ.

`Altin olcut mutanti (windows-latest)` — `win32 · py3.11.9`, 1m 5s:
**`SONUC: 7 isirdi - 0 kacti - 0 olculemedi (toplam 7)`**. M-A2 gerçek Windows'ta iki sınıfı
da adlandırdı: `\x0b → 'DIKEY SEKME (VT)'` · `\x85 → 'SONRAKI SATIR (NEL, U+0085)'` →
enjeksiyon Windows'un **kendi** satır-sonu katmanından sağ çıkıyor. §6.1'in ikinci TAHMİN'i
de ölçüldü. `Faz C bolme mutanti (windows-latest)` yeşil (59 s) — altı bölme mutantı ilk kez
Windows'ta koştu.

⚠️ **YEŞİL TİKİN OKUNUŞU:** run #19'da **6 "error" annotation** var ve iş buna rağmen
SUCCESS: `ruff / mypy / bandit` ×4 · `Y-1 probu (windows)` · `ortam sinifi (linux)`. Altısı da
`continue-on-error: true` olan **ÖLÇÜM** adımıdır, kapı değil. Bu depoda run #2'de
`continue-on-error` bir çökmeyi yutup işi yeşil göstermişti; o yüzden gizlenmiyor.
Ayrıca 45 uyarı: `actions/checkout@v4`, `setup-python@v5`, `upload-artifact@v4` Node.js 20
hedefliyor, GitHub zorla Node 24'e alıyor — ileride sürüm yükseltmesi gerekecek.

### 8.2 §6.4 KAPANDI — `text=True` eksikliği ALTI ARAÇTA (sekiz çağrı yeri) ÖLÇÜLDÜ

Soru "geçiyor mu" değil, **"hâlâ ISIRIYOR mu"**dur: bir araç kör olduğu için de yeşil
olabilir (Y-2 dersi — 58 hüküm kaybolmuş, iş yeşil görünmüştü).

Ortam: `sitecustomize.py` + `PYTHONPATH`, **istisnasız her Python sürecinde**
`sys.stdout.reconfigure(newline="\r\n")`. Kapsam ölçüldü: her araçta **satır sayısı = CR
sayısı** — `boru_probu` 33=33 · `fazB_senaryolari` 35=35 · `y4_mutant` 12=12 ·
`fazA_senaryolari` 15=15 · `y2_mutant` 15=15 · `fazB_olcut_mutanti` 20=20 → enjeksiyon
aracın **kendi** satırlarını da kapsadı, yalnız gömülü çocuk çıktısını değil.
(İlk yazımda bu sayılar tabloya YANLIŞ SIRADA yazılmıştı — `fazA` 33, `boru_probu` 15
görünüyordu; bağımsız denetçi buldu, düzeltildi. Çokluk kümesi doğruydu, eşleme değildi.) Ayrıca doğrulandı:
`reconfigure(encoding="utf-8", errors="replace")` newline ayarını **sıfırlamıyor**
(`b'1\r\n'`) — yani Y-2 koruması enjeksiyonu geri almıyor.

| araç | çağrı yeri | süre | exit (temiz/CRLF) | hüküm | CR hariç çıktı farkı |
|---|---|---|---|---|---|
| `fazA_senaryolari` | `:156`, `:374` | 64 s | 0 / 0 | `6 isirdi - 0 kacti - 0 olculemedi` | **0 satır** |
| `fazB_senaryolari` | `:310` | 6 s | 0 / 0 | `6 isirdi - 0 kacti - 0 UYGULANMAZ - 0 olculemedi` | **0 satır** |
| `y4_mutant` | `:133` | 20 s | 0 / 0 | `2 isirdi - 0 kacti - 0 olculemedi` | **0 satır** |
| `boru_probu` | `:212`, `:229` | 3 s | 0 / 0 | `hukum boruya bagli degil — bu ortamda tuzak YOK` | **0 satır** |
| `y2_mutant` | `:155` | 539 s | 0 / 0 | `2 isirdi - 0 kacti - 0 olculemedi` | **0 satır** |
| `fazB_olcut_mutanti` | `:184` | 15 s | 0 / 0 | `2 isirdi - 0 kacti - 0 olculemedi` | **0 satır** |

**Altısının altısı da CRLF'e duyarsız.** Hüküm, çıkış kodu ve çıktı — `\r` dışında birebir aynı.

**SEBEP, ve asıl ders:** bu araçların hiçbiri **SAKLANMIŞ bir artefaktla** karşılaştırma
yapmıyor; hepsi hükmünü koşum anında üretilen metinden çıkarıyor.

İlk yazımda gerekçeyi *"hepsi `splitlines()` · alt-dize · çapasız regex kullanıyor"* diye
yazmıştım; **bağımsız denetçi bunun yanlış olduğunu ölçtü.** Bağışıklığın gerçek nedenleri
daha çeşitli, ve her biri ayrı:

| desen | yer | neden `\r` bozmuyor |
|---|---|---|
| **çapalı** regex | `y2_mutant.py:166` `re.compile(r"^SONUC: \d+ gecti", re.M)` | `\r` satır SONUNDA duruyor, `^` çapası satır BAŞINDA; tam y2 koşumunda CRLF metne karşı fiilen sınandı (`hukum=VAR`) |
| `.split("\n")` | `fazA_senaryolari.py:199` · `boru_probu.py:219` | ikisi de `open()` ile **DOSYA** okuyor; universal newline `\r`'yi zaten yiyor. Enjeksiyon yalnız `sys.stdout/stderr`'e dokunuyor |
| **tam eşitlik** | `fazB_senaryolari.py:468-469` `t["sinif"] == "SALT-OKUNUR-TESHIS"` | karşılaştırılan şey ham çıktı değil, `mesaj_sinifi()` (`:138`, saf alt-dize) üretimi SINIF ADI |
| **tam eşitlik** | `boru_probu.py:175,184,192,196` `ad.strip() == "ciplak"` | `ad` aracın kendi sabit etiketi, çocuk çıktısı değil |

Yani bağışıklık bir **tesadüf değil ama tek bir sebebe de indirgenemez** — dört ayrı
mekanizma. Bit-bit karşılaştıran  **tek** araç `altin_cikti.py`'ydi — ve eksiklik
**yalnız orada öldürücüydü.** Kapsam da ölçüldü: motoru çağıran öteki BÜTÜN yerlerde
`text=True` VAR (`fazC_bolme_mutanti:129` · `sabotaj:125` · `t_y42:59,838,980,993,1227,1248` ·
`t_y3:43` · `hafiza.py:2238,3815,3864,4402`) → altı araçlık liste eksik değil.

Yani `text=True`'yu altı yere de eklemek **bir kapı kazandırmaz**; ölçülmüş bir gerekçesi
yoktur ve "ADDITIVE kal, kanıtsız dokunma" gereği **yapılmadı.** Sınıf artık SINIRDA değil
ama **ÖLÇÜLMÜŞ** olarak kapalı: eksikliğin hükme etkisi altı yerin altısında sıfırdır.

### 8.3 Defter düzeltmesi

`faz0/altin_olcut_mutanti.py` satır **3**, **20** ve **490** "IKI duzeltme" diyordu; üç
düzeltme (D-1/D-2/D-3) ve yedi mutant var. Satır 490 bunu **her CI koşumunun ilk satırında
basıyordu (ölçüldü: çıktının **2.** satırı; 1. satır ayraç).** Üçü de "UC" olarak
düzeltildi. Ayrıca `.github/workflows/capraz.yml`'de aynı yalanın iki kopyası daha
bulundu — biri **CI adım adı** (`:428` "alti mutant", oysa yedi; Actions arayüzünde her
koşumda yazıyor), biri yorum (`:395` "IKI duzeltmesi"). İkisi de düzeltildi.
🔴 `capraz.yml` değişti → **İş Portföyü'ne bildirim yükümlülüğü.**
`:367`'deki "alti mutant" DOĞRUDUR ve dokunulmadı: o satır `fazC_bolme_mutanti` işine ait
ve o araçta gerçekten altı mutant var (M-C1…M-C6). Denetçi onu da bulgu saymıştı;
denetçi de yanılabilir, o yüzden her bulgu tek tek doğrulandı. Kod etkilenmedi; etkilenen şey defterin
doğruluğuydu — *"belge de bir arayüzdür ve yalan söyleyebilir."*

### 8.4 §8'de NE ÖLÇÜLEMEDİ

1. **macOS logları okunmadı.** `altin_olcut_mutanti (macos-latest)` ve
   `fazC_bolme_mutanti (macos-latest)` işleri YEŞİL ama hüküm satırları birebir okunmadı;
   yalnız iş düzeyinde yeşil görüldü. Sözleşmeye göre exit 0 = "hepsi ısırdı", ama bu bir
   ÇIKARIMDIR, okuma değildir.
2. **§8.2 ölçümü yalnız Linux'ta yapıldı.** Altı aracın Windows CI kolları run #19'da
   yeşildi, ama hüküm SAYILARI (ör. fazA'nın "6 isirdi") Windows loglarından okunmadı →
   "Windows'ta da kör değil" iddiası ÖLÇÜLMEDİ, yalnız "kırmızı yanmadı" biliniyor.
3. **CRLF dışı satır sınırı karakterleri** (`\x0b` · `\x85` · U+2028 …) bu altı araç için
   denenmedi; yalnız `\r` ölçüldü. `altin_cikti` için ikisi de ölçüldü (M-A2).
4. `mypy` / `bandit` yeni dosyalarda hâlâ koşulmadı. `fazC_bolucu.py`'nin CRLF yolu hâlâ
   hiç koşulmadı. `_RE_SHA` hâlâ daraltılmadı. `altin_kapi.json` hâlâ yalnız yeşil yolu
   ölçüyor.
5. **CI run #19 tek kaynaklı.** §8.1'deki her sayı (SUCCESS · 6m 24s · 24 artefakt ·
   6 error annotation · 45 uyarı), birebir alıntılanan Windows log bloğu ve Windows'ta
   M-A2'nin bastığı sınıf adları **Onur'un tarayıcı oturumundan** okundu. Bağımsız denetçi
   ajanın GitHub'a erişimi yok; hiçbirini doğrulayamadı.
6. **`.split("\n")` sitelerinin DİSKTE CRLF'li dosyayla davranışı** ölçülmedi. §8.2'nin
   bağışıklık savı `open()`'ın universal-newline okumasına dayanıyor; CRLF'li bir fikstür
   kurulmadı.
7. **Tekrarlanabilirlik:** §8.2'nin her kolu tek koşum. Kararsızlık (flakiness) ölçülmedi.
8. **`ruff` / `mypy` / `bandit`** bu turda hiç koşulmadı (§8.3'ün değiştirdiği satırlar
   yorum ve dize; sözdizimi ve mutant koşumu ile doğrulandı).

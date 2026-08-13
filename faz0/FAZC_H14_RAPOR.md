# FAZ C ALT-BÖLME — `_kapi_h14` · ÖLÇÜM RAPORU

**Tarih:** 13 Ağustos 2026 · **Motor:** `skill/scripts/hafiza.py`
**Girdi SHA256:** `b954e0cb…` (4930 satır) → **çıktı SHA256:** `b0750786…` (4977 satır)
**Üreteç:** `faz0/fazC_bolucu_h14.py` · **Kenar mutantı:** `faz0/h14_bolme_mutanti.py`

> Bu belgedeki her sayı bu oturumda koşuldu. Beyandan alınan tek sayı yoktur;
> bölme öncesi değerler için motorun `HEAD` sürümü (`b954e0cb…`) ayrı bir dosyaya
> çıkarılıp aynı araçlarla ölçüldü.

---

## 1. NE YAPILDI

`_kapi_h14` — **CC 35 · 104 satır** — dört parçaya bölündü; ince `_kapi_h14`
en sona kondu.

| fonksiyon | CC | satır | ne yapar |
|---|---|---|---|
| `_h14_git_durumu(kok)` | 9 | 43 | `git status -z` + `ls-files -z` → `git_var, kirli, izlenen` |
| `_h14_adaylar(kok, y)` | 9 | 18 | `os.walk` + hariç kümesi → `adaylar` |
| `_h14_en_yeni(kok, adaylar, git_var, kirli, izlenen)` | 14 | 25 | sınıflandırma + toplu `git log` → `en_yeni_t, en_yeni_f` |
| `_h14_hukum(F, N, gecikme, t_son, en_yeni_t, en_yeni_f)` | 4 | 17 | **tek hüküm bölgesi** |
| `_kapi_h14(F, N, O, kok, rc, y, t_son)` | **3** | **12** | dallar + dört çağrı |

Motor geneli: **CC>20 11 → 10 · satır>80 11 → 10 · birleşik ihlal 14 → 13 ·
fonksiyon 181 → 185.** Ölçüm: `python3 faz0/karmasiklik.py skill/scripts/hafiza.py`
(CLAUDE.md §5; başka bir CC sayısı beyan edilmez).

Gövdeler **elle yeniden yazılmadı**: `faz0/fazC_bolucu_h14.py` satırları birebir
taşır, girintiyi tekdüze 4 boşluk azaltır ve her satırda bunu doğrular.

### 1.1 Parçalar arası veri: BEŞ kenar, hepsi imzada

```
git_var, kirli, izlenen   GIT DURUMU  -> EN YENI
adaylar                   ADAY TARAMA -> EN YENI
en_yeni_t, en_yeni_f      EN YENI     -> HUKUM
```

### 1.2 🔴 Üç parça F/N/O ALMIYOR — ve bu bir tercih değil, ölçüm

11 Ağustos 2026'da `_kapi_govde` bölmesinde ölçülmüştü: hüküm listelerini
*döndüren* bir parça yarıda `SystemExit` atarsa o ana kadar toplanan bulgu
KAYBOLUR (`FAIL (2 bulgu)/exit 1` → `FAIL (1 bulgu)/exit 3`). Bu yüzden H1
bölmesinde bütün parçalar `F` almaya devam etti.

H14'te üç parça almıyor, çünkü **taşınan bölgelerde hüküm çağrısı SIFIR**:

```
3765-3805 (git durumu)   fail/F.append/N.append/O.append = 0
3764,3806-3820 (tarama)  = 0
3821-3843 (en yeni)      = 0
3844-3858 (hüküm)        = fail x2, N.append x2, F.append x1
```

Bu sayıyı üreteç **her koşumda yeniden ölçer** (`bos bolge kapisi` adımı, AST ile).
Sıfır değilse dosya YAZILMAZ. Yani koruma "gerek yok" diye sökülmedi; sökülmesinin
bir şey kaybettirmediği ölçüldü ve o ölçüm kalıcı bir kapıya bağlandı.
`_h1_kova_bek` istisnasıyla aynı gerekçe.

### 1.3 Sıra neden böyle

`faz0/sabotaj.py` her `fail()` çağrısını `(lineno, col)` sırasına göre
numaralandırır. Parçalar kapının kendi yerinde ve koşum sırasında durur; hüküm
haritası (sıra → kapı etiketi) üretim öncesi ve sonrası karşılaştırıldı:
**61 → 61, eşleme AYNI.**

### 1.4 Dal yapısı BİREBİR korundu

H1'de koruma satırı ters çevrilmişti (`if not ...: return`) ve **elle yazılan o
tek satır**, altın kümenin kör olduğu üç sınıftan biri çıktı. H14'te bu risk
küçültüldü: `if gecikme <= 0: / elif not t_son: / else:` üçlüsü **hiç
dokunulmadan** taşındı. Elle yazılan tek şey `else` bloğundaki dört çağrı
satırıdır — ve beş kenar mutantının hedefi tam olarak o dört satırdır.

---

## 2. KABUL ÖLÇÜTÜ — DEVİR'in listesi, aynı sırayla

Hepsi bulut Linux'ta, **root olmayan** kullanıcıyla (`olcum`) koşuldu.

| # | ölçüm | sonuç |
|---|---|---|
| 1 | `altin_cikti.py --karsilastir faz0/altin_kapi.json` | **FARK YOK — 22 ölçüm bit-bit** ✅ |
| 2 | `altin_cikti.py --kendini-sina` | ISIRDI · exit 0 ✅ |
| 3 | `fazC_bolme_mutanti.py` | 6 ısırdı / 0 kaçtı ✅ |
| 4 | `altin_kapi_mutanti.py` | 6 ısırdı / 0 kaçtı ✅ |
| 5 | `altin_olcut_mutanti.py` | 7 ısırdı / 0 kaçtı ✅ |
| 6 | `h1_bolme_mutanti.py` | 7 ısırdı / 0 kaçtı (altın küme 3'üne kör — değişmedi) ✅ |
| 7 | `win_yol_probu.py` | exit 0 ✅ |
| 8 | `t_y3.py` | 20/20 temiz hata ✅ |
| 9 | `isir` (derle ÖNCESİ) | 34/34 ısırıyor · 2 SINANMADI · **exit 2** ⚠️ |
| 10 | `isir` (derle SONRASI) | 36/36 ısırıyor · 0 SINANMADI · exit 0 ✅ |
| 11 | `t_y42.py` | 57 geçti · 0 kaldı · 1 yavaş · 0 ölçülemedi ✅ |
| 12 | `hukum_kapisi.py hukum.log` | beklenen her hüküm BASILDI · exit 0 ✅ |
| 13 | `sabotaj.py` — bölme SONRASI vs bölme ÖNCESİ | **61/61 madde · sıra→kapı→hüküm dizisi AYNI** ✅ |

**13. satır — sabotaj diferansiyeli.** `faz0/sabotaj.py` iki motorda ayrı ayrı
koşuldu (`--is 4`, root olmayan kullanıcı): bölme öncesi `b954e0cb…` ve bölme
sonrası `b0750786…`. Her ikisi de **61 madde · 21 KAPSAMLI · 40 KAPSAMSIZ**;
`(sıra, kapı, hüküm)` dizisi **birebir aynı**. Aynı dizi `faz0/sabotaj_rapor.json`
tabanının (commit `f149407`) kapı+hüküm dizisiyle de örtüşüyor — yani bölme
kapsam envanterinde tek bir maddeyi bile oynatmadı.

**9. satırdaki exit 2 bölmenin ürünü DEĞİLDİR.** Aynı ölçüm bölme öncesi motorla
(`b954e0cb…`) tekrarlandı: **exit 2**. `derle` öncesi iki mutant sınanamıyor ve
araç bunu "ölçülemeyen mutant" (2) diye raporluyor — sözleşme gereği. Sayı
değişmedi, dolayısıyla bu turun hükmü değil.

---

## 3. KENAR MUTANTI — `faz0/h14_bolme_mutanti.py`

Yedi hâl (7 ölçüm) × yedi mutant. Hâller **temiz motorla bir kez** kurulur,
kollara `copytree` ile kopyalanır (mtime KORUNUR — H14'ün ölçtüğü şey tam olarak
mtime olduğu için bu bir ayrıntı değil, ön koşuldur); yalnız **ölçen** motor değişir.

| hâl | ne uyandırır | temiz koldaki H14 satırı |
|---|---|---|
| `h_es` | hafıza ile proje aynı tarihte | `H14: hafiza projeyle es` |
| `h_geride` | proje ilerledi, hafıza ilerlemedi | `[H14] PROJE ILERLEDI…` |
| `h_ileri` | hafıza dosyalardan ileride | `[H14] … ILERIDE — tutarsiz` |
| `h_kirli` | **izlenen ama DEĞİŞMİŞ** dosya → mtime geçerli | `[H14] PROJE ILERLEDI…` |
| `h_temiz` | **izlenen, değişmemiş, mtime taze** → commit tarihi geçerli | `H14: hafiza projeyle es` |
| `h_ignore` | `.gitignore`'lu taze dosya → izlenmeyen | `[H14] PROJE ILERLEDI…` |
| `h_kapali` | `hafiza_gecikme_gun = 0` → kapı KAPALI | `? H14: … disiplin kapisi KAPALI` |

**Hâl kapısı (bu betiğe özgü):** temiz kolda her hâlin çıktısında bir H14 satırı
bulunmak ZORUNDA. Bulunmazsa hâl kapıyı hiç ateşlememiştir ve bütün mutantlar
sahte "temiz" görünürdü → betik `OLCULEMEDI` der, exit 2. Ölçüldü: 7/7 ateşledi,
7 hâlin 7'si de ayrık imza üretti.

### 3.1 🔴 ASIL BULGU — altın küme yedi mutantın BEŞİNE kör

| mutant | kendi kümesi | altın küme |
|---|---|---|
| M-H14a KENAR `git_var` | ISIRDI (h_temiz) | **KÖR — FARK YOK** |
| M-H14b KENAR `kirli` | ISIRDI (h_kirli) | **KÖR — FARK YOK** |
| M-H14c KENAR `izlenen` | ISIRDI (h_temiz) | **KÖR — FARK YOK** |
| M-H14d KENAR `adaylar` | ISIRDI (6 ölçüm) | ISIRDI |
| M-H14e KENAR `en_yeni` | ISIRDI (6 ölçüm) | ISIRDI |
| M-H14f TOLERANS (eşik → 10⁶) | ISIRDI (4 ölçüm) | **KÖR — FARK YOK** |
| M-H14g KORUMA SÖKME (kapalı dalı) | ISIRDI (h_kapali) | **KÖR — FARK YOK** |

H1 turunda oran 3/7'ydi; H14'te **5/7**. Körlük tesadüf değil, **yapısal**:
altın kümenin hâlleri taze kurulmuş, hafızası bugün yazılmış projelerdir — orada
H14 hep aynı tek cümleyi üretir ve git'in dört sınıfı (izlenen-temiz ·
izlenen-kirli · izlenmeyen · `.gitignore`'lu) HİÇ ayrışmaz. Oysa H14'ün git
mantığının var oluş nedeni tam olarak o dört sınıfı ayırmaktır (Fable Bulgu 9,
§3.1). En ağırı **M-H14f**: tolerans eşiği sessizce sonsuza çekildiğinde kapı
fiilen kapanır, tek bir kırmızı bile yanmaz — altın küme bunu görmez.

**KARAR B korundu** (12 Ağu 2026): altın kümeye dokunulmadı. Kümenin tek değeri
bölme öncesi motora bağlı olmasıdır; bugünkü motordan yeniden kaydedilirse o bağ
bir daha kurulamaz. Kenar kapsamı ayrı araçtan gelir — bu araçtan.

---

## 4. NE AÇTI (ne kapattığı değil)

| ölçüm | bölme ÖNCESİ | bölme SONRASI |
|---|---|---|
| `ruff --select F,E9,B,S,PLE` | 31 | **31** |
| `ruff --statistics` (stil toplamı) | 119 | **119** |
| hüküm sayısı / sıra→kapı eşlemesi | 61 | **61 · AYNI** |
| `karmasiklik.py` birleşik ihlal | 14 | **13** |

Yeni bir hata sınıfı açılmadı; ihlal listesi bir madde kısaldı.

---

## 5. CI

`.github/workflows/capraz.yml`'ye iki iş eklendi (`continue-on-error` YOK):

* **`h14_kenar_mutanti`** — üç platform (ubuntu/windows/macos), `h14_bolme_mutanti.py`
  + altın sütunu, çıktı artefakt olarak saklanır.
* **`karmasiklik`** — `karmasiklik_mutanti.py` (9 mutant, **9/9 ısırdı** — bu
  oturumda koşuldu) + `karmasiklik.py … --ihlal` **RAPOR kipinde**.
  🔴 Araç `--kapi` ile koşulmuyor: bugün 14 ihlal var, `--kapi` her koşumu kırmızı
  yakar ve kırmızı değersizleşirdi.

YAML `yaml.safe_load` ile doğrulandı: **17 iş**, sözdizimi geçerli.

⚠️ `.github/workflows/*` köprüden YAZILAMAZ. Dosya teslim edildi; diske kaydeden
Onur'dur ve kaydettiğini `(Get-Content ...).Count` ile doğrulaması gerekir
(`c0478f0` dersi: commit mesajı beyandır, içerik ölçümdür).

---

## 6. 🔴 YAN BULGU — H14 ters yönde İKİ hüküm birden basıyor

`h_ileri` hâlini kurarken ölçüldü: `fark < -gecikme` olduğunda motor **hem**
`[H14] hafiza tarihi proje dosyalarindan 40 gun ILERIDE — tutarsiz` FAIL'ini
**hem de** `H14: hafiza projeyle es` notunu basıyor. Sebep, hüküm bloğunun
`if fark < -gecikme:` / `if fark > gecikme: … else:` yapısı: ters yön ikinci
koşulun `else` dalına düşüyor.

**Bu bölmenin ürünü DEĞİLDİR** — bölme öncesi motor da aynı ikisini basar (altın
küme 22 ölçümde bit-bit aynı olduğu için bu kesindir). Refactoring turunda
davranış değiştirilmez; **düzeltilmedi**, ayrı bir tura yazıldı. Kenar mutantı
bu hâli okurken FAIL satırını önceler, yoksa hâl "eş" sanılır.

---

## 7. NE ÖLÇÜLEMEDİ

1. **Windows ve macOS.** Bölme ve kenar mutantı yalnız bulut Linux'ta koştu.
   `h14_bolme_mutanti.py` hâlleri `git commit` + `os.utime` ile kurar; Windows'ta
   dosya kilidi ve mtime çözünürlüğü ölçülmedi. CI işi tam bunun için eklendi —
   ama **bu rapor yazılırken o iş henüz koşmadı**.
2. **`t_son` çözülemeyen dal.** `elif not t_son:` kolunu ateşleyen bir hâl
   kurulamadı (H12 tarihi çözemediğinde ne olduğunu ölçen ayrı bir düzenek gerekir).
   O dalın koruması bu turda KANITSIZ kaldı.
3. **`gecikme` sınır değerleri.** Hâller 40 gün mesafeyle kuruldu; `fark == gecikme`
   ve `fark == -gecikme` tam sınır noktaları ölçülmedi.
4. **CI'nın kendisi.** Bu rapor yazılırken yeni `capraz.yml` push edilmemişti
   (push/commit Onur'da). CI #28'in hükmü bu belgede YOKTUR.
5. **`faz0/kapsam_envanteri.json` hâlâ BAYAT** (60 madde, motorda 61 hüküm).
   Bu turda dokunulmadı; geçerli taban `faz0/sabotaj_rapor.json`.
6. **Oturum sağlığı.** `oturum_sagligi.py` bu depoda yok (aracın evi Momentum) ve
   Desktop Commander bu oturumda yüklü değildi → kullanılan token'ın **politika
   formülüne göre** değeri ÖLÇÜLEMEDİ. Ham bileşenler ölçüldü ve DEVİR'e yazıldı.
7. **`hafiza_gecikme_gun` yokluğu.** `.hafizarc`'ta anahtarın hiç bulunmaması
   (varsayılan 2 koddan gelir) bu turda ölçüldü ve kenar mutantının ilk koşumunu
   `Kurulamadi` ile düşürdü. Aynı sınıfın başka anahtarlarda da geçerli olup
   olmadığı ölçülmedi.

---

## 8. SIRADAKİ İŞ (öneri, karar Onur'da)

1. `capraz.yml` diske kaydedilsin, push edilsin, **CI #28 okunsun** — özellikle
   `h14_kenar_mutanti` Windows kolu.
2. Alt-bölmede sıradaki hedef: `_kapi_h4` (CC 32 · 61 satır) ya da `_kapi_h10`
   (CC 27 · 81 satır). Aynı turda kendi kenar mutantı.
3. §6'daki çift hüküm — ayrı bir düzeltme turu, kendi mutantıyla.
4. H16 YAPI kapısı: alt-bölme bittikten sonra (`faz0/YAPI_KAPISI_TASARIM.md`).

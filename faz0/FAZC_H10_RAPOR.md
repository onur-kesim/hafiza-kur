# FAZ C ALT-BÖLME — `_kapi_h10` · ÖLÇÜM RAPORU

**Tarih:** 13 Ağustos 2026 · **Motor:** `skill/scripts/hafiza.py`
**Girdi SHA256:** `fb64f25a…` (5017 satır) → **çıktı SHA256:** `09f24896…` (5060 satır)
**Üreteç:** `faz0/fazC_bolucu_h10.py` · **Kenar mutantı:** `faz0/h10_bolme_mutanti.py`
**Duran onayla koşuldu** (kalıp dışına çıkılmadı; bir kapı GENİŞLETİLDİ — §1.2).

---

## 1. NE YAPILDI

`_kapi_h10` — **CC 27 · 81 satır** — dört parçaya bölündü.

| fonksiyon | CC | satır | ne yapar |
|---|---|---|---|
| `_h10_tekillik(F, y)` | 4 | 12 | canlı bloklar + konu sayımı → `bl, say` |
| `_h10_cit(F, O, y)` | 8 | 39 | kod çiti · girintili işaret · gizli blok → `_ham` |
| `_h10_yapi(F, _ham)` | 12 | 26 | blok açılış/kapanış taraması |
| `_h10_sozluk(F, y, say)` | 6 | 9 | `KONULAR.md` tanımlılığı |
| `_kapi_h10(F, N, O, y)` | **1** | **8** | akış + dört çağrı |

Motor geneli: **CC>20 9 → 8 · birleşik ihlal 12 → 11 · fonksiyon 189 → 193.**
Hüküm haritası **61 → 61**, (sıra → kapı) eşlemesi aynı.

### 1.1 Üç kenar, hepsi imzada

```
bl    TEKILLIK -> ebeveyn (dönüş değeri, H12 bunu kullanır)
say   TEKILLIK -> SOZLUK
_ham  CIT      -> YAPI
```

`N.append("H10: %d blok / %d ayrik konu")` **ebeveynde kaldı** — YAPI taramasından
sonra, SÖZLÜK denetiminden önce basılır ve sıra sözleşmedir.

### 1.2 🔴 BOŞ BÖLGE KAPISI → **KANAL KAPISI** (kalıp genişletildi)

H14 ve H4'te taşınan bölgelerde hüküm çağrısı **sıfırdı**; üreteç "sıfır mı" diye
soruyordu ve parçalar saf dönebiliyordu. **H10'da durum tersi**: dört bölgenin
dördü de hüküm basar (`fail` · `F.append` · `O.append`). Orada "sıfır mı" sorusu
anlamsız olurdu. Sorulması gereken şu:

> Bir bölge hangi **hüküm kanallarını** kullanıyorsa, o parçanın **imzası** o
> kanalları taşımak zorundadır.

Üreteç bunu AST ile ölçer ve eksikse **dosyayı yazmaz**. Koşum çıktısı:

```
kanal kapisi: _h10_tekillik  kullanilan F      imza TASIYOR
kanal kapisi: _h10_cit       kullanilan F,O    imza TASIYOR
kanal kapisi: _h10_yapi      kullanilan F      imza TASIYOR
kanal kapisi: _h10_sozluk    kullanilan F      imza TASIYOR
```

Böylece 11 Ağu 2026'da ölçülen kısmi-çıktı kaybı (saf dönüşe çevrilen bir parçanın
bulgusunun `SystemExit`'te kaybolması) hem boş hem dolu bölgede **mekanik olarak**
imkânsızlaşır. Eski boş-bölge kapısı bu kapının özel hâlidir.

---

## 2. KENAR MUTANTI — 9 hâl × 6 mutant

Hâller: `h_temiz` · `h_cift` (konu tekilliği) · `h_cit` (kapanmamış çit) ·
`h_girintili` · `h_gizli` (O kanalı) · `h_cakisan` · `h_bozuk` · `h_tanimsiz` ·
`h_cift_cit`. **Hâl kapısı 9/9** — hepsi temiz kolda H10 satırı üretti, 9 ayrık imza.

Sonuç: **6/6 ısırdı, 0 kaçtı.** Altın sütunu: **altısının altısına da KÖR**. Zincir artık dört turluk ve tek yönlü: H1 **3/7** → H14 **5/7** → H4 **6/6** → H10 **6/6**. Altın küme, bölmelerin kenarları hakkında ARTIK HİÇBİR ŞEY söylemiyor; kenar kapsamının tamamı bu mutantlardan geliyor.

🔴 **EŞDEĞER MUTANT KAYDI (bu turun asıl dersi).** İlk `SIRA` mutantı —
`_h10_yapi` (F kanalı) ile `N.append` (N kanalı) yer değiştirir — **KAÇTI**.
İnceleme sonucu: bu bir körlük değil, **eşdeğerlik**. Bulgular ve notlar çıktının
ayrı bölümlerinde basılır, dolayısıyla sıra yalnız **aynı kanal içinde**
gözlenebilir; iki farklı kanal arasında yer değiştirmek hiçbir şeyi değiştirmez.
Eşdeğer bir mutantı "kaçtı" diye raporlamak **sahte kırmızıdır** (Y-4 dersi).
Mutant aynı kanala yazan iki parçaya taşındı (`_h10_tekillik` ↔ `_h10_cit`) ve
kümeye `h_cift_cit` hâli eklendi — ikisi de F'e yazdığı için sıra artık ölçülebilir.
Yeni mutant ısırdı.

---

## 3. NE AÇTI

| ölçüm | H4 motoru (`fb64f25a`) | H10 motoru (`09f24896`) |
|---|---|---|
| `ruff --select F,E9,B,S,PLE` | 31 | **31** |
| `ruff --statistics` toplam | 121 | **125** (+4) |
| birleşik ihlal | 12 | **11** |
| hüküm sayısı / eşleme | 61 | **61 · AYNI** |

**+4 nereden geldi — ölçüldü, açıklanabilir ve kaçınılmaz:**

* **E731 lambda-assignment 20 → 23 (+3):** her yeni parça kendi
  `fail = lambda k, m: F.append(...)` satırını taşır. `fail` **adı
  değiştirilemez** — `faz0/sabotaj.py` çağrıları AST'te `Name.id == "fail"` diye
  arar; ad değişirse kapsam envanteri sessizce 0'a düşer.
* **E741 ambiguous-variable-name 20 → 21 (+1):** `_h10_cit(F, **O**, y)` —
  `O` kanal adıdır ve motorun her yerinde aynıdır.

Yani yeni bir hata sınıfı açılmadı; artan iki sayı da **sözleşmenin bedelidir**.
Bu ayrım kayda geçiyor çünkü "ne açtığı ölçülür" kuralı sayının artmamasını değil,
**artışın açıklanmasını** ister.

---

## 4. KABUL ÖLÇÜTÜ

| # | ölçüm | sonuç |
|---|---|---|
| 1 | `altin_cikti.py --karsilastir` | **FARK YOK — 22 ölçüm bit-bit** ✅ |
| 2 | `--kendini-sina` | ISIRDI ✅ |
| 3 | `fazC_bolme_mutanti.py` | 6 / 0 ✅ |
| 4 | `altin_kapi_mutanti.py` | 6 / 0 ✅ |
| 5 | `altin_olcut_mutanti.py` | 7 / 0 ✅ |
| 6 | `h1_bolme_mutanti.py` | 7 / 0 (altın 3'üne kör) ✅ |
| 7 | `h14_bolme_mutanti.py` | 7 / 0 (altın 5'ine kör) ✅ |
| 8 | `h4_bolme_mutanti.py` | 6 / 0 (altın 6'sına kör) ✅ |
| 9 | `h10_bolme_mutanti.py` (**yeni**) | **6 / 0 — altın küme ALTISINA DA KÖR** ✅ |
| 10 | `win_yol_probu.py` | exit 0 ✅ |
| 11 | `karmasiklik_mutanti.py` | 9 / 0 ✅ |
| 12 | `oturum_sagligi_mutanti.py` | 6 / 0 ✅ |
| 13 | `t_y3.py` | 20/20 ✅ |
| 14 | `isir` (derle öncesi / sonrası) | 34/34 (exit 2 — önceki turlarla aynı) · 36/36 ✅ |
| 15 | `t_y42.py` | 57 · 0 · 1 yavaş ✅ |
| 16 | `hukum_kapisi.py` | beklenen her hüküm BASILDI ✅ |
| 17 | `sabotaj.py` (H4 motoruna karşı diferansiyel) | **61/61 · (sıra,kapı,hüküm) dizisi AYNI** ✅ |

---

## 5. CI

`capraz.yml` **20 işe** çıktı (831 satır · 39.299 bayt · `yaml.safe_load` geçti).
Yeni iş: **`h10_kenar_mutanti`** — üç platform, `continue-on-error` YOK.

⚠️ Köprüden yazılamaz; Onur kaydeder ve `(Get-Content …).Count` = **831** ile doğrular.

---

## 6. NE ÖLÇÜLEMEDİ

1. **Windows/macOS'ta H10 kenar mutantı** — yalnız bulut Linux'ta koştu; CI işi
   eklendi ama bu rapor yazılırken koşmadı.
2. **Eşdeğer mutant taraması yapılmadı.** `SIRA` mutantının eşdeğer olduğu ELLE
   bulundu. Diğer beş mutantın eşdeğer OLMADIĞI ısırmalarıyla kanıtlı, ama
   *başka* eşdeğer mutantların var olup olmadığı ölçülmedi — sistematik bir
   eşdeğerlik taraması bu projede henüz yok.
3. **`_h10_yapi`'nin CC 12'si** hâlâ bu turun en yükseği; 20 tavanının altında ama
   ikinci bir bölmeye aday olup olmadığı ölçülmedi.
4. **`kod_disi` / `girintili_isaretler` gibi yardımcılar** bölmeye girmedi;
   kenar mutantı onları dolaylı ölçer, doğrudan değil.
5. **`faz0/kapsam_envanteri.json` hâlâ BAYAT** (60 madde / 61 hüküm).
6. **CI #31** — bu rapor yazılırken push edilmemişti.

---

## 7. SIRADAKİ İŞ

Kalan ihlal **11**: `cmd_devral` 88 · `cmd_derle` 63 · `zincir_dogrula` 40 ·
`cmd_bloklastir` 39 · `cmd_kur` 27 · `_kapi_h12` 25 · `cmd_emekli` 24 ·
`_kapi_h11` 23 · `_guvenli_calistir` (84 satır) · `cmd_isir` (700 satır) ·
`yol_on_kontrol` (90 satır).

Kapılarda sıradaki: **`_kapi_h12`** (CC 25 · 46 satır) ve **`_kapi_h11`** (23 · 48).
İkisi bittiğinde **kapı fonksiyonlarında ihlal kalmaz**; geriye yalnız `cmd_*`
komutları ve üç uzun fonksiyon kalır — onlar ayrı bir sınıftır ve kenar mutantı
kalıbı henüz yoktur (altın küme onları exit/çıktı düzeyinde ölçer).

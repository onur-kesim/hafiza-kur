# FAZ C ALT-BÖLME — `_kapi_h12` · ÖLÇÜM RAPORU

**Tarih:** 14 Ağustos 2026 · **Motor:** `skill/scripts/hafiza.py`
**Girdi SHA256:** `09f24896…` (5060 satır) → **çıktı SHA256:** `61283ff7…` (5091 satır)
**Üreteç:** `faz0/fazC_bolucu_h12.py` · **Kenar mutantı:** `faz0/h12_bolme_mutanti.py`
**Duran onayla koşuldu.**

---

## 1. NE YAPILDI

`_kapi_h12` — **CC 25 · 46 satır** — üç parçaya bölündü.

| fonksiyon | CC | satır | kanal | ne yapar |
|---|---|---|---|---|
| `_h12_tazelik(F, N, O, rc, y)` | 7 | 21 | **F · N · O** | "Son güncelleme" çözümü + bayatlık → `t_son` |
| `_h12_sapma_haritasi(y, ks)` | 11 | 17 | **(SAF)** | fragman/karar tarihleri → `en_yeni` |
| `_h12_sapma_hukmu(F, N, y, bl, en_yeni)` | 9 | 11 | F · N | CANLI BAYAT + bekleyen fragman |
| `_kapi_h12(F, N, O, rc, y, bl, ks)` | **1** | **6** | — | akış + üç çağrı |

Motor geneli: **CC>20 8 → 7 · birleşik ihlal 11 → 10 · fonksiyon 193 → 196.**
Hüküm haritası **61 → 61**, eşleme aynı.

### 1.1 🔴 KALIBIN İKİ UCU AYNI BÖLMEDE

H14/H4'te taşınan bölgeler hüküm basmıyordu (hepsi saf), H10'da hepsi basıyordu.
H12 ikisini birden içeriyor: `_h12_tazelik` **üç kanalı birden** kullanıyor,
`_h12_sapma_haritasi` **hiç** kullanmıyor. Kanal kapısı ikisini de tek ölçütle
ele alıyor ve koşumda bunu yazıyor:

```
kanal kapisi: _h12_tazelik         kullanilan F,N,O   imza TASIYOR
kanal kapisi: _h12_sapma_haritasi  kullanilan (SAF)   imza TASIYOR
kanal kapisi: _h12_sapma_hukmu     kullanilan F,N     imza TASIYOR
```

Ölçüt tek: **kullandığını taşı.** Kullanılmayanı taşıtmak da bir maliyettir —
"koruma" adı altında ölçülmemiş parametre birikir ve bir sonraki bölmede
"bu neden burada?" sorusuna ölçülmüş bir cevap kalmaz.

### 1.2 İki kenar, ikisi de imzada

```
t_son    TAZELİK -> ebeveyn (dönüş değeri; H14 bunu kullanır)
en_yeni  SAPMA HARİTASI -> SAPMA HÜKMÜ
```

---

## 2. KENAR MUTANTI — 7 hâl × 6 mutant

Hâller: `h_temiz` · `h_bayat` · `h_gelecek` · `h_cozulemez` (O kanalı) ·
`h_satirsiz` · `h_canli_bayat` · `h_bekleyen`. **Hâl kapısı 7/7**, 7 ayrık imza.

Mutantların üçü doğrudan **kanalları** koparıyor (F/N/O yerine boş liste), ikisi
veri kenarlarını, biri kapının **dönüş değerini** (`t_son` → `None`; H14 o tarihi
kullandığı için bu bir *kapılar arası* kenardır).

Sonuç: **6/6 ısırdı, 0 kaçtı.** Altın sütunu: **altın küme 4'üne KÖR** (M-H12a KANAL F · M-H12c KANAL O · M-H12d KENAR en_yeni · M-H12e KENAR bl); ikisini GÖRDÜ (KANAL N ve DÖNÜŞ t_son).

🔴 **Bu, önceki turların "tek yönlü artış" okumasını DÜZELTİR.** Zincir H1 3/7 → H14 5/7 → H4 6/6 → H10 6/6 → **H12 4/6**; yani körlük monoton DEĞİL. Belirleyen şey, kapının altın kümenin hâllerinde **ne kadar konuştuğudur**: H12 her projede konuşur (her projede bir 'Son güncelleme' satırı vardır ve H12 not basar), bu yüzden N kanalının ve `t_son` dönüşünün kopması altın çıktıyı değiştirir. H4 ise o hâllerde hiç konuşmaz. Ölçüt "tur numarası" değil, **kapının o kümedeki ses düzeyidir**.

---

## 3. NE AÇTI

| ölçüm | H10 motoru (`09f24896`) | H12 motoru (`61283ff7`) |
|---|---|---|
| `ruff --select F,E9,B,S,PLE` | 31 | **31** |
| `ruff --statistics` toplam | 123 | **125** (+2) |
| birleşik ihlal | 11 | **10** |
| hüküm sayısı / eşleme | 61 | **61 · AYNI** |

+2'nin kaynağı ölçüldü: **E731 23 → 24** (yeni bir `fail` lambda'sı) ve
**E741 21 → 22** (`_h12_tazelik(F, N, **O**, rc, y)` — kanal adı). H10 turundaki
ile aynı sınıf; yeni hata sınıfı açılmadı.

---

## 4. KABUL ÖLÇÜTÜ (19 madde)

| # | ölçüm | sonuç |
|---|---|---|
| 1 | `altin_cikti.py --karsilastir` | **FARK YOK — 22 ölçüm** ✅ |
| 2 | `--kendini-sina` | ISIRDI ✅ |
| 3 | `fazC_bolme_mutanti.py` | 6 / 0 ✅ |
| 4 | `altin_kapi_mutanti.py` | 6 / 0 ✅ |
| 5 | `altin_olcut_mutanti.py` | 7 / 0 ✅ |
| 6 | `h1_bolme_mutanti.py` | 7 / 0 ✅ |
| 7 | `h14_bolme_mutanti.py` | 7 / 0 ✅ |
| 8 | `h4_bolme_mutanti.py` | 6 / 0 (altın 6'sına kör) ✅ |
| 9 | `h10_bolme_mutanti.py` | 6 / 0 (altın 6'sına kör) ✅ |
| 10 | `h12_bolme_mutanti.py` (**yeni**) | **6 / 0 — altın küme 4'üne kör** ✅ |
| 11 | `win_yol_probu.py` | exit 0 ✅ |
| 12 | `karmasiklik_mutanti.py` | 9 / 0 ✅ |
| 13 | `oturum_sagligi_mutanti.py` | 6 / 0 ✅ |
| 14 | `t_y3.py` | 20/20 ✅ |
| 15-16 | `isir` (derle öncesi / sonrası) | 34/34 (exit 2, değişmedi) · 36/36 ✅ |
| 17 | `t_y42.py` | 57 · 0 · 1 yavaş ✅ |
| 18 | `hukum_kapisi.py` | beklenen her hüküm BASILDI ✅ |
| 19 | `sabotaj.py` (H10 motoruna karşı diferansiyel) | **61/61 · dizi AYNI** ✅ |

---

## 5. CI

`capraz.yml` **21 işe** çıktı (869 satır · 41.065 bayt · `yaml.safe_load` geçti).
Yeni: **`h12_kenar_mutanti`** — üç platform, `continue-on-error` YOK.

🔴 **Teslim yolu değişti (bu turdan itibaren):** workflow dosyası köprüyle depo
**köküne** yazılır (`_capraz_yeni.yml`), Onur tek `Move-Item` komutuyla yerine
koyar. Gerekçe ölçüldü: "karttan indir + doğru klasöre kaydet" adımı **iki kez**
başarısız oldu (`c0478f0` ve `2550eba` — ikisinde de commit mesajı CI işini beyan
etti, içerik gelmedi). İki kez aynı sınıf = yöntem kusuru.

---

## 6. NE ÖLÇÜLEMEDİ

1. **Windows/macOS'ta H12 kenar mutantı** — yalnız bulut Linux'ta koştu.
2. **`ks` (kararlar) kenarı ölçülmedi.** `_h12_sapma_haritasi(y, ks)` çağrısında
   `ks` koparılmadı: kararlardan gelen tarihin CANLI BAYAT hükmünü tetiklediği bir
   hâl kurulmadı. Bu kenar **kanıtsızdır**; fragman ayağı ölçüldü, karar ayağı hayır.
3. **`_h12_sapma_haritasi`'nın CC 11'i** turun en yükseği; ikinci bölmeye aday olup
   olmadığı ölçülmedi.
4. **Eşdeğerlik taraması** yine yapılmadı (H10 dersinden sonra sistematik hâle
   getirilmedi).
5. **`faz0/kapsam_envanteri.json` BAYAT** (60 madde / 61 hüküm).
6. **CI #32** — bu rapor yazılırken push edilmemişti.

---

## 7. SIRADAKİ İŞ

Kalan ihlal **10**: `cmd_devral` 88 · `cmd_derle` 63 · `zincir_dogrula` 40 ·
`cmd_bloklastir` 39 · `cmd_kur` 27 · `cmd_emekli` 24 · **`_kapi_h11` 23** ·
`_guvenli_calistir` (84 satır) · `cmd_isir` (700 satır) · `yol_on_kontrol` (90 satır).

**`_kapi_h11` (CC 23 · 48 satır) son kapı fonksiyonudur** — o da bölündüğünde
`_kapi_*` ailesinde tek bir ihlal kalmaz. Sonrası `cmd_*` komutları: ayrı sınıf,
kenar mutantı kalıbı henüz yok (altın küme onları yalnız exit/çıktı düzeyinde ölçer).

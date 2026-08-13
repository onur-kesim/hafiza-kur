# FAZ C ALT-BÖLME — `_kapi_h4` · ÖLÇÜM RAPORU

**Tarih:** 13 Ağustos 2026 · **Motor:** `skill/scripts/hafiza.py`
**Girdi SHA256:** `b0750786…` (4977 satır) → **çıktı SHA256:** `fb64f25a…` (5017 satır)
**Üreteç:** `faz0/fazC_bolucu_h4.py` · **Kenar mutantı:** `faz0/h4_bolme_mutanti.py`

> Bu tur **duran onayla** koşuldu (13 Ağu 2026, Onur): H14 turunda kurulan kalıp
> — SHA kapılı üreteç · boş bölge kapısı · kabul ölçütü · kenar mutantı · CI işi ·
> rapor — tur başına onay beklemeden uygulanır. Onay yalnız **kalıp dışına**
> çıkıldığında istenir. Bu turda kalıp dışına çıkılmadı.

---

## 1. NE YAPILDI

`_kapi_h4` — **CC 32 · 61 satır** — dört parçaya bölündü.

| fonksiyon | CC | satır | ne yapar |
|---|---|---|---|
| `_h4_adaylar(metin)` | 8 | 21 | backtick + markdown taraması → `aday` |
| `_h4_havuz(kok)` | 5 | 7 | `os.walk` → dosya adı havuzu |
| `_h4_siniflandir(eksik, havuz)` | 13 | 23 | ölü / taşınmış ayrımı |
| `_h4_hukum(F, N, olu, tasinmis)` | 6 | 11 | **tek hüküm bölgesi** |
| `_kapi_h4(F, N, O, kok, y)` | **4** | **10** | akış + dört çağrı |

Motor geneli: **CC>20 10 → 9 · birleşik ihlal 13 → 12 · fonksiyon 185 → 189.**

**Boş bölge kapısı ölçtü:** taşınan üç bölgede (adaylar · havuz · sınıflandırma)
hüküm çağrısı **0**; hepsi `_h4_hukum`'da (2 `fail`, 2 `N.append`).
**Hüküm haritası 61 → 61, (sıra → kapı) eşlemesi aynı.**

---

## 2. KABUL ÖLÇÜTÜ

Root olmayan kullanıcıyla, bu sırayla — sonuçlar §2.1'de.

| # | ölçüm | sonuç |
|---|---|---|
| 1 | `altin_cikti.py --karsilastir` | **FARK YOK — 22 ölçüm** ✅ |
| 2 | `altin_cikti.py --kendini-sina` | ISIRDI ✅ |
| 3 | `fazC_bolme_mutanti.py` | 6 ısırdı / 0 kaçtı ✅ |
| 4 | `altin_kapi_mutanti.py` | 6 / 0 ✅ |
| 5 | `altin_olcut_mutanti.py` | 7 / 0 ✅ |
| 6 | `h1_bolme_mutanti.py` | 7 / 0 (altın küme 3'üne kör — değişmedi) ✅ |
| 7 | `h14_bolme_mutanti.py` (regresyon) | 7 / 0 (altın küme 5'ine kör — değişmedi) ✅ |
| 8 | `h4_bolme_mutanti.py` (**yeni**) | **6 / 0 — altın küme 6'sının 6'sına da KÖR** ✅ |
| 9 | `win_yol_probu.py` | exit 0 ✅ |
| 10 | `karmasiklik_mutanti.py` | 9 / 0 ✅ |
| 11 | `oturum_sagligi_mutanti.py` (**yeni**) | 6 / 0 ✅ |
| 12 | `t_y3.py` | 20/20 temiz hata ✅ |
| 13 | `isir` (derle öncesi / sonrası) | 34/34 (exit 2 — bölme öncesi de aynı) · 36/36 exit 0 ✅ |
| 14 | `t_y42.py` | 57 geçti · 0 kaldı · 1 yavaş ✅ |
| 15 | `hukum_kapisi.py` | beklenen her hüküm BASILDI ✅ |
| 16 | `sabotaj.py` (H14 motoruna karşı diferansiyel) | **61/61 · (sıra,kapı,hüküm) dizisi AYNI** ✅ |

---

## 3. KENAR MUTANTI — 7 hâl × 6 mutant

H4'ün altın kümedeki görünürlüğü H14'ünkinden de düşük: altın kümenin
hâllerinde canlı hafızada **backtick'li yol beyanı yoktur**, dolayısıyla H4
orada çoğunlukla hiç konuşmaz. Konuşmayan bir kapının kenarı "FARK YOK" ile
kanıtlanamaz.

Hâller (hepsi temiz kolda H4 satırı üretti — **hâl kapısı 7/7**):

| hâl | uyandırdığı dal |
|---|---|
| `h_olu` | `[H4] OLU BAGLANTI … (hicbir yerde yok)` |
| `h_tasinmis` | `H4: TASINMIS (olu degil)` notu — FAIL değil |
| `h_ayni_ad` | `OLU … ayni adli baska dosya var ama yol tutmuyor` |
| `h_kirpma` | 12 ölü → `… +2 OLU BAGLANTI daha (ekranda kirpildi, HEPSI sayildi)` |
| `h_tas_kirp` | 7 taşınmış → `… +2 tasinmis dosya daha` |
| `h_markdown` | `[]()` biçimli bağlantı (ikinci tarama döngüsü) |
| `h_turkce` | **Türkçe adlı** ölü bağlantı — Fable Bulgu 4'ün UNICODE dalı |

Mutant sonucu: **6/6 ısırdı, 0 kaçtı.** Altın sütunu: **altın küme ALTISINA DA KÖR**. Eğilim ölçüldü ve tek yönlü: H1 3/7 → H14 5/7 → **H4 6/6**. Bir kapı altın kümenin hâllerinde ne kadar az konuşuyorsa, o kapının kenarları o kadar kanıtsızdır — ve bu "22 ölçüm bit-bit" hükmünün altında GÖRÜNMEZ.

🔴 **Araç kusuru bulundu ve düzeltildi:** ilk koşumda `M-H4f KORUMA SOKME`
`OLCULEMEDI` verdi — hedef dizge `    if eksik:` motorda **üç kez** geçiyor.
Tek satırlık çapa yetmedi; mutant artık satırı **izleyen yorumla birlikte**
çapalıyor. Bu, Y-4 dersinin tekrarı: ölçülemeyen hâl, yeşil sayılmadı.

---

## 4. NE AÇTI

| ölçüm | H14 motoru (`b0750786`) | H4 motoru (`fb64f25a`) |
|---|---|---|
| `ruff --select F,E9,B,S,PLE` | 31 | **31** |
| `ruff --statistics` (stil toplamı) | 119 | **119** |
| hüküm sayısı / eşleme | 61 | **61 · AYNI** |
| birleşik ihlal | 13 | **12** |

---

## 5. YENİ ARAÇ — `araclar/oturum_sagligi.py`

Oturum sağlığı bu oturumun başında **ÖLÇÜLEMEDİ** hükmü vermişti (araç başka bir
projedeydi). Artık bu depoda:

* Dört bileşeni (girdi · çıktı · cache yazımı · cache okuması) **ayrı ayrı** basar.
* **Formül bir politika kararıdır** ve çıktıda adıyla yazılır; varsayılan
  `girdi+cikti`. Gerekçe ölçülebilir: cache alanları dahil edilince aynı sınıftaki
  bir oturum milyonları aşıyor (bu oturumda cache okuması 41.251.953), oysa
  13 Ağu'da bir oturum **469.417** ile SARI raporlanmıştı — o sayıyı SARI
  aralığında tutan tek okuma cache hariç olanıdır. Bu bir **çıkarımdır**, öyle
  işaretlenmiştir; `--formul` ile değiştirilebilir.
* **Yüzde BASMAZ** — tavanı ölçen bir kaynak yok, payda uydurma olurdu.
* Transcript bulunamazsa **ÖLÇÜLEMEDİ / exit 2** (YEŞİL değil).
* `araclar/oturum_sagligi_mutanti.py`: 6 mutant (SARI eşiği · KIRMIZI eşiği ·
  formül · ÖLÇÜLEMEDİ koruması · çıkış kodu sözleşmesi · sessiz satır atlama),
  sentetik transcript'lerle, gerçek oturuma bağımsız. **6/6 ısırdı.**

Bu oturumun ölçümü (22:5x): girdi 368 · çıktı 333.810 · cache yazımı 977.286 ·
cache okuması 41.251.953 → **kullanılan 334.178 · YEŞİL**.

---

## 6. CI

`capraz.yml` **19 işe** çıktı (`yaml.safe_load` ile doğrulandı). Yeni:
* `h4_kenar_mutanti` — üç platform, `continue-on-error` YOK.
* `oturum_sagligi` — ubuntu + windows; **yalnız mutant** koşar.
  🔴 Aracın kendisi CI'da koşulmaz: runner'da Claude transcript'i yoktur, araç
  doğru davranıp ÖLÇÜLEMEDİ/exit 2 döndürür ve iş **sahte kırmızı** yanardı.
  Ölçülen şey aracın **sözleşmesidir**, ortam değil.

⚠️ `.github/workflows/*` köprüden yazılamaz — dosya teslim edilir, Onur kaydeder
ve `(Get-Content …).Count` = **789** ile doğrular.

---

## 7. NE ÖLÇÜLEMEDİ

1. **Windows/macOS'ta H4 kenar mutantı.** Yalnız bulut Linux'ta koştu; hâller
   `git init` + dosya yazımıyla kuruluyor. CI işi bunun için eklendi ama bu rapor
   yazılırken **koşmadı**.
2. **`oturum_sagligi.py`'nin GERÇEK transcript'te platformlar arası davranışı.**
   Mutant sentetik dosya kullanır; Windows'ta `~/.claude/projects` arama deseninin
   tutup tutmadığı ÖLÇÜLMEDİ (yalnız `--transcript` yolu ölçüldü).
3. **Formülün doğruluğu.** `girdi+cikti` seçimi bir çıkarımdır; Momentum'daki
   `oturum-sagligi.py` ile **çapraz karşılaştırma yapılmadı** (Desktop Commander
   bu oturumda yüklü değil). İki araç aynı transcript'te aynı sayıyı veriyor mu —
   bilinmiyor.
4. **H4'ün `DOSYA_UZANTILARI` beyaz listesi.** Kenar mutantı uzantı listesinin
   kendisini sınamaz; `.keystore/.properties` gibi sınır uzantılar ölçülmedi.
5. **`faz0/kapsam_envanteri.json` hâlâ BAYAT** (60 madde / 61 hüküm).
6. **CI #30.** Bu rapor yazılırken push edilmemişti; hüküm bu belgede YOKTUR.

---

## 8. SIRADAKİ İŞ

Kalan ihlal **12**: `cmd_devral` 88 · `cmd_derle` 63 · `zincir_dogrula` 40 ·
`cmd_bloklastir` 39 · `_kapi_h10` 27 · `cmd_kur` 27 · `_kapi_h12` 25 ·
`cmd_emekli` 24 · `_kapi_h11` 23 · `_guvenli_calistir` (84 satır) ·
`cmd_isir` (700 satır) · `yol_on_kontrol` (90 satır).

Kapı fonksiyonlarında sıradaki: **`_kapi_h10`** (CC 27 · 81 satır). Ondan sonra
`_kapi_h12` ve `_kapi_h11`; komutlar (`cmd_*`) ayrı bir sınıftır — altın küme
onları exit/çıktı düzeyinde ölçer ve kenar mutantı kalıbı henüz yoktur.

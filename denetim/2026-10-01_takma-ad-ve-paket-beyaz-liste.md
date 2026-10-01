# 2026-10-01 — İngilizce takma ad (yalnız komutlar) + `paket`/`skill-kur` BEYAZ LİSTE

**Soru (b):** `CLAUDE.md` §1 "İngilizce kanonik komut + Türkçe alias" diyordu; motorda `add_parser(aliases=…)`
kullanımı **0** idi (16 alt komutun hepsi Türkçe). Belge ≠ gerçek.

**Soru (d):** `paket`/`skill-kur` dosya süzgeci `deneme`yi TAM ad eşlemesiyle eliyordu; `.gitignore` ise
`skill/scripts/deneme*/` önekiyle yok sayıyor. Aradaki fark gizli bir sızıntıydı ve ölçülmüştü (aşağıda).

## ✅ KARAR (Onur kilidi, 1 Eki 2026 19:5x — Cowork O5, interaktif seçim)
- **(b)** alias EKLE · **Türkçe KANONİK KALIR** · Set A eşlemesi (aşağıda) · **YALNIZ KOMUTLAR** (bayraklar Türkçe).
- **(d)** BEYAZ LİSTE + BAĞIMSIZ KAPI-2. İkisi AYNI iş emri, İKİ KALEM, ayrı commit.
- Değiştirmek (başka ad, bayrak takma adı, listeye yeni girdi) **ADR ister.**

## Set A (Onur kilidi)
| Türkçe (kanonik) | İngilizce takma ad |
|---|---|
| `kur` | `init` |
| `devral` | `adopt` |
| `bloklastir` | `mark-blocks` |
| `bolum-kur` | `add-sections` |
| `not` | `note` |
| `derle` | `compile` |
| `emekli` | `retire` |
| `karar` | `decide` |
| `muhur` | `seal` |
| `korunan` | `protect` |
| `kapi` | `gate` |
| `isir` | `bite` |
| `surum` | `version` |
| `skill-kur` | `install-skill` |
| `paket` | `package` |
| `hook` | — (takma ad yok) |

---

## KALEM 1 — İngilizce takma ad

### Ne yapıldı
- Tablo motorda TEK yerde (`_KOMUT_TAKMA_AD`, modül sabiti); `main()` her `add_parser`a `aliases=_takma_ad(…)` verir.
  Dağıtım `set_defaults(fn=…)` + `a.fn(a)` ile yapılır, `a.komut` hiçbir yerde okunmaz (grep ile ölçüldü) ⇒
  argparse'ın "dest yazılan adı taşır" davranışı dağıtımı KIRMAZ. Kilit dosyası `sys.argv[1:]`'i yazar: İngilizce adla
  da aynı kalıp, hüküm etkisi yok. **Kapı bölgesi (sat. 1-5332) bayt-AYNI** (`cmp`). Çıkış kodu sözleşmesi değişmedi.
- README "Kullanım" altına tablo; SKILL.md gövdesine tek satır (`description` frontmatter'ı DOKUNULMADI, ≤500 kapısı).
  `CLAUDE.md` §1 cümlesi "Türkçe kanonik komut + İngilizce takma ad (yalnız komut; bayraklar Türkçe) — ADR 2026-10-01"
  oldu (8162 B ≤ 8192; satır eklenmedi).
- **ÖLÇÜM = `faz0/readme_mutanti.py` KAPI-4** (yeni `faz0/` dosyası YOK; md.5'in "okur README ile deneyebilir" kapısı).
  Beklenti **README tablosundan** ayıklanır, motorun sözlüğünden OKUNMAZ (paylaşılan kural = paylaşılan körlük).
  Beş alt eksen, her biri etiketli: `[TABLO]` · `[YARDIM]` (her satırda `<ing> --help` ≡ `<tr> --help`, kanonik `usage:`) ·
  `[KÜME]` (motorun `--help` komut kümesi == README'nin adları: belgelenmemiş/vaat edilip verilmeyen ad yok) ·
  `[DAVRANIŞ]` (iki AYRI kum havuzunda 16 adım, `isir` dahil, aynı girdi → aynı exit + aynı stdout; kanonik taraf her
  adımda 0 vermeli, zaman aşımı "eşit" sayılmaz) · `[BELGE]` (SKILL.md'deki satır README tablosunun kopyası: aynı küme).
- Mutantlar — **her KAPI-4 mutantı atesleyen alt eksenin BEKLENENLE BİREBİR aynı olmasını ister** (bağımsız inceleme
  bulgusu: aksi halde `[DAVRANIŞ]` ölü olsa da mutantlar "KAPI-4 kırmızı" diye ISIRDI derdi): M-AD-1 motorda `gate` silinir
  (YARDIM+KÜME+DAVRANIŞ) · M-AD-2 `gate`↔`bite` yer değiştirir (YARDIM+DAVRANIŞ) · M-AD-3 README motorda olmayan takma ad
  vaat eder (YARDIM+KÜME+BELGE) · M-AD-4 motorda `note` dağıtımda sessizce düşer (yalnız DAVRANIŞ) · M-AD-5 README çekirdek
  `kapi` takma adını düşürür (TABLO+KÜME+DAVRANIŞ+BELGE) · M-AD-6 motor README'de olmayan ad kabul eder (yalnız KÜME) ·
  M-AD-7 SKILL.md kopyası ayrışır (yalnız BELGE). İş emri 3 mutant istemişti; dördü fazladan, her biri bir alt ekseni kanıtlar.

### Ölçülen kusur (üretici fark etti, kapıya yazıldı)
`muhur`≡`seal` karşılaştırması ilk sürümde iki kum havuzunda FARKLI halka karması gördü: `zincir_halka` saniye damgasını
(`t`) hash'e katar, iki havuzun aynı saniyeye düşmesi tesadüftür. Halka karması normalize edilir; başka bir şey değil.

### Ölçüm (1 Eki 2026; Linux = WSL Ubuntu `olcum` kullanıcısı py3.14, Windows = py3.12)
- **K1:** 15 takma ad × `--help` exit 0 ve çıktısı Türkçe komutla BİREBİR aynı (Windows, tek tek). `hooks` (takma ad
  uydurması) exit 2. Beş çekirdek + 11 ek adım, iki ayrı kum havuzunda Tr≡İng (exit + stdout): Linux ve Windows'ta 0 bulgu.
- **K2:** Linux'ta tam `readme_mutanti.py`: KAPI-1/2/3/4 YEŞİL, **16/16 mutant** ISIRDI; M-AD-1..7'nin atesleyen
  alt eksenleri beklenenle birebir; KAPI-1/2/3 her M-AD mutantında yeşil kaldı.
- **K4 (kısmen):** kapı bölgesi (sat. 1-5332) `cmp` ile bayt-AYNI. Motor `7f37417b…` 398.865 B → `98ebe9b6…` 400.435 B.
- **ÖLÇÜLEMEDİ:** macOS ve py3.11/3.13 (bu makinede yok; CI'da koşar). `capraz.yml` bataryası (K5) ve sabotaj/isir sayıları
  KALEM 2 sonunda, son ağaçta ölçülür (aşağıda).

## KALEM 2 — Beyaz liste

*(commit 2'de doldurulur)*

## Bedeller ve sınırlar (gizlenmez)
- Beklenti README'den geldiği için **README ve motor AYNI yönde birlikte değişirse KAPI-4 yeşil kalır** (örn. ikisinde
  `gate` → `check`). Bunu kapı değil bu ADR + Onur kilidi korur.
- `korunan`/`protect` yalnız `[YARDIM]` ile ölçülür (davranış adımı yok: bir blok işareti kurmayı gerektirir).
- `capraz.yml` adım adı ("uc kapi + dokuz mutant") ve üstündeki yorum bloğu BAYAT kaldı: `capraz.yml` bu işin kısıtı
  gereği DEĞİŞMEDİ (Cowork'a bırakılan tek satırlık düzeltme).

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
  son ağaçta ölçüldü: aşağıda "Sonuç ölçümü".

## KALEM 2 — Beyaz liste

### Ölçülmüş zemin (Cowork, 1 Eki 2026, taban `8aab8197`) — `deneme_*` sızıntısı
Süzgeç `_SKILL_KUR_HARIC_DIZIN = ("deneme","__pycache__")` TAM ad eşlemesi; `.gitignore` `skill/scripts/deneme*/` önekiyle yok sayar.

| vaka (skill/scripts/ altında) | pakette (taban) | `paketle.sh` KAPI-2 (taban) |
|---|---|---|
| TABAN | 10 | YEŞİL |
| `deneme/arsiv/PROJE_HAFIZA.md` | 10 (elendi) | YEŞİL |
| `deneme_b4e/arsiv/PROJE_HAFIZA.md` | **11 — SIZDI** | **YEŞİL** (kör) |
| `deneme2/arsiv/PROJE_HAFIZA.md` | **11 — SIZDI** | **YEŞİL** (kör) |

`skill-kur` (HOME geçici) aynı vakada "11 dosya" kurdu ⇒ sızıntı kullanıcının `~/.claude/skills/` dizinine de gidiyordu.
Motorun kendi ölçümü ile `paketle.sh` KAPI-2 AYNI kuraldan türediği için İKİSİ DE KÖRDÜ.

### Ne yapıldı
- `_skill_kur_dosyalar` artık **BEYAZ LİSTE**: kökte `SKILL.md` · `references/*.md` · `scripts/*.py` (tek seviye); BAŞKA her dosya
  ALINMAZ. Kural TEK yerde (`_skill_kur_beyaz_mi`, sabitler `_SKILL_KUR_BEYAZ_KOK`/`_SKILL_KUR_BEYAZ_DIZIN`); `paket` ve `skill-kur`
  aynı fonksiyonu kullanır.
- **GİZLENEMEZ KILINDI:** beyaz liste dışı HER dosya için iki komut stdout'a `DISARIDA BIRAKILDI: <rel> (beyaz liste disi)`
  basar, çıkış kodu DEĞİŞMEZ. `__pycache__` ve nokta ile başlayan ad/dizinler gürültüdür: satır üretmez. **`scripts/deneme/`
  (tam ad) artık SESSİZ DEĞİL** — beyaz listede `deneme` istisnası yok; README'nin kanıt akışı o dizini yaratır ve paket/skill-kur
  onun her dosyasını bildirir (gürültü, ama bilinçli: sessiz eleme yok).
- **Kurulu hedefin ve kopyanın envanteri beyaz listeyle SÜZÜLMEZ** (`_skill_kur_tum`): süzülseydi eski kara liste döneminden
  kalan kurulumdaki sızıntı (`~/.claude/skills/hafiza-kur/scripts/deneme_b4e/…`) "ZATEN KURULU" diye gizlenirdi. Şimdi `skill-kur`
  CATISMA (exit 2) der, `--guncelle` eskisini yedeğe TAŞIR (silmez) ve temizini kurar.
- `paketle.sh` KAPI-2 **DEĞİŞMEDİ** (bilinçli: kendi `os.walk`'u, yalnız tam `deneme`/`__pycache__`/nokta; motordan BAĞIMSIZ). Sonuç:
  `deneme_x/` varken motor 10 dosya paketler, KAPI-2 "EKSİK: scripts/deneme_x/…" der ve KIRMIZI yanar, paket SİLİNİR — çöp ağaçta
  durduğu için GÖRÜNÜR. Yanıltıcı "EKSİK" kelimesi için KAPI-2'ye tek satır not eklendi (gövde mantığı değişmedi).
- **Bağımsız inceleme bulgusu (kapatıldı):** kaynakta DİZİN BAĞLANTISI varken `paket` reddediyordu (exit 2) ama `skill-kur` içeriği
  sessizce düşürüp exit 0 "KURULDU" diyordu (`os.walk` bağlı dizine inmez ⇒ ne beyaz listeye ne DISARIDA'ya girer; Windows
  junction'da ise tersine içeri iner). `skill-kur` artık `paket` ile aynı reddi yapar (`_paket_baglantilar`, exit 2). Çıkış kodu
  KÜMESİ değişmedi (2 zaten "kullanım hatası/çakışma"); `_SKILL_KUR_KODLAR`, README ve SKILL.md'deki 2 cümlesi buna göre genişledi.
- `_SKILL_KUR_HARIC_DIZIN`'in "TAM ad eşlemesi … KAPSAMAZ" notu kalktı; sabit artık yalnız `("__pycache__",)`.

### Ölçüm araçları (VAR OLAN dosyalar; yeni `faz0/` dosyası YOK)
- `paket_mutanti.py`: yeni **BEYAZ ekseni** (beklenen küme harness'in KENDİ okuyuşuyla; `deneme_x/`+`deneme2/` varken temiz motor
  10 dosya + STDOUT'ta her çöp için satır (liste olarak, ne eksik ne fazla) + `paketle.sh` KAPI-2 KIRMIZI + paket silindi);
  M-2 yeniden hedeflendi (beyaz liste `references`'i düşürür); **M-8** beyaz liste sökülür (iş emrinde "M-4" geçiyordu; M-4 zaten
  vardı, sıradaki numara M-8). 8/8 mutant.
- `skill_kur_mutanti.py`: yeni **K-COP** kolu (çöp varken 10 dosya + DISARIDA satırları + kurulu hedefteki çöp CATISMA/`--guncelle`
  yedekler + kaynakta dizin bağlantısı REDDEDİLİR); `suzulmus()` beyaz liste okuyuşuna geçti (kaynakta `deneme_x/` varken K-TAZE/
  K-GUNCELLE/K-PROJE'nin yanlış kırmızı vermesi giderildi); M-SK-SUZGEC → **M-SK-BEYAZ** (beyaz liste sökülür), + **M-SK-HEDEF**
  (kurulu hedef de süzülür) + **M-SK-BAGLANTI** (reddi sök). 9 kol / 10 mutant.

### Ölçüm (Windows py3.12, 1 Eki 2026; Linux ve tam batarya KALEM 3 notunda)
`paket_mutanti` 8/8 · `skill_kur_mutanti` 9 kol yeşil, 10/10 mutant ISIRDI (K-SALTOKUNUR gerçek-izin kolları B/C/D ÖLÇÜLEMEDİ:
POSIX değil) · K3: TABAN paketi 10 dosya, KALEM 2 öncesiyle AYNI ad listesi (yalnız `SKILL.md` ve `scripts/hafiza.py` baytları değişti,
ikisi de KALEM 2'nin kendi düzenlemesi) · `deneme_b4e`/`deneme2`/`Deneme` vakalarında `paketle.sh` KAPI-2 KIRMIZI + paket silindi;
motor aynı vakada 10 dosya + DISARIDA satırı. `_olcum/o5/kos.sh` birebir koşuldu; `sk.sh` birebir KOŞULAMADI (izin: `rm -rf "$HOME"`),
yerine aynı vaka elle ve K-COP ile ölçüldü.

## Sonuç ölçümü (K4/K5 — son ağaç `006e84c`, taban `8aab8197`; 2 Eki 2026)
- **K5:** `capraz.yml`'deki 88 `run:` adımı (matris değişkenleri çözülerek; liste YML'den türetildi; `ci_yerel.py` kuralları) HER İŞ TAZE
  KOPYADA, paralel (3 işçi), **TABANDA da** koşuldu; yalnız FARK regresyondur. Linux (WSL `olcum`, py3.14): 82 koştu · 81 exit 0 · 1 exit≠0
  (`win_kill_probu` exit 2, Linux'ta beklenen) · 6 atlandı (`ruff/mypy/bandit/pip/sudo` yok). Windows (py3.12; matris py3.13 kolları `py -3.14`):
  86 koştu · 75 exit 0 · 11 exit≠0 (symlink 1314 sınıfı: `t_y42`, `readme_kapisi`, `y2_mutant`, `kalite`…) · 2 atlandı.
  **Taban↔yeni adım adım exit FARKI SIFIR** (Linux 88/88, Windows 88/88 eşleşti). `readme_kapisi` Linux'ta 1633 s (taban) / 1594 s (yeni).
- **K4:** sabotaj (`faz0/sabotaj.py`, taban ve yeni motorda AYRI koşum): **55/67 KAPSAMLI**, 12 KAPSAMSIZ, 67 kaydın HEPSİ (satır no, kapı,
  hüküm, kaçan mutant) tabanla BİREBİR aynı (fark 0) · isir 67/67+2 · derle sonrası 69/69 · git'siz (derle sonrası) 66/66+3 UYGULANMAZ (tabanla
  aynı) · `t_y42` 57 geçti + 1 YAVAŞ (B-6 "300k satır < 8 sn" zaman duvarı: yeni 8,24 sn, TABAN 8,99 sn — sakin makinede bile; hız notu,
  doğruluk hükmü DEĞİL; **58/58 bu makinede ÖLÇÜLEMEDİ**, Cowork bulut konteynerinde ölçülmüştü) · CC>20 7→7 · ihlal 9→9 (fonksiyon 306→310)
  · kapı bölgesi (sat. 1-5332) `cmp` ile bayt-AYNI.
- **Linux (batarya içinde):** `paket_mutanti` 8/8 (BEYAZ ekseni + M-8 dahil) · `skill_kur_mutanti` 9 kol YEŞİL (K-COP: dizin bağlantısı
  symlink ile REDDEDİLDİ; K-SALTOKUNUR B/C/D gerçek salt-okunur dizinle YEŞİL) + 10/10 mutant · `paketten_kos` YEŞİL · `readme_mutanti` 4 kapı + 16/16.
- **ÖLÇÜLEMEDİ:** macOS · py3.11/3.13 (yerelde yok) · Windows'ta `t_y42`/`readme_kapisi` KAPI-2 (symlink 1314 ⇒ Linux'ta ölçüldü) ·
  Windows'ta K-SALTOKUNUR B/C/D (POSIX değil) ve `skill-kur` dizin bağlantısı reddi yalnız junction ile (symlink Windows'ta kurulamadı).

## Bedeller ve sınırlar (gizlenmez)
- Beklenti README'den geldiği için **README ve motor AYNI yönde birlikte değişirse KAPI-4 yeşil kalır** (örn. ikisinde
  `gate` → `check`). Bunu kapı değil bu ADR + Onur kilidi korur.
- `korunan`/`protect` yalnız `[YARDIM]` ile ölçülür (davranış adımı yok: bir blok işareti kurmayı gerektirir).
- `capraz.yml` adım adı ("uc kapi + dokuz mutant") ve üstündeki yorum bloğu BAYAT kaldı: `capraz.yml` bu işin kısıtı
  gereği DEĞİŞMEDİ (Cowork'a bırakılan tek satırlık düzeltme).

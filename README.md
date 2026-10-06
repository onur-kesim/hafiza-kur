# hafiza-kur

Taşınabilir bir **proje hafızası kapı sistemi**. Tek dosyalık saf Python motoru
(stdlib, sıfır bağımlılık) bir projenin hafıza dosyalarını yönetir ve **ölçer**.

> **Durum:** geliştirme aşamasında, **henüz yayımlanmadı.** Aşağıdaki Kurulum komutları
> vardır ve ölçülmüştür — Claude Code yolu (`skill-kur`) gerçek ev dizininde ve CI'da;
> `paket` paketi üretip kendi kendini ölçer. **Ölçülmeyen tek halka:** `paket`in ürettiği
> dosyanın claude.ai'ye yüklenip kabul edilmesi (30 Eyl 2026 yüklemesi `zip` ile üretilmiş
> paketleydi). Bu depo CI ölçümü ücretsiz koşabilsin diye publictir — bir yayın değildir.
> PyPI paketi, marketplace girişi ya da duyuru **yoktur**.

---

## Kurulum

Python 3 ve `git` yeter (motor stdlib, sıfır bağımlılık; `bash` ve `zip` gerekmez). Komutlar
`python3` ile yazıldı; **Windows'ta `python` ya da `py` kullan.**

1. Depoyu al:

   ```bash
   git clone https://github.com/onur-kesim/hafiza-kur.git
   cd hafiza-kur
   ```

2. **Claude Code** — skill'i `~/.claude/skills/hafiza-kur/` altına kopyalar ve kopya üzerinde ölçer:

   ```bash
   python3 skill/scripts/hafiza.py skill-kur
   ```

   Sonra Claude Code'da `/hafiza-kur` (`skills/` dizini yeni açıldıysa açık oturumda `/reload-skills`).

3. **Cowork / claude.ai** — bu klasörü okumazlar; `.skill` paketini üretip yüklersin:

   ```bash
   python3 skill/scripts/hafiza.py paket
   ```

   Paket depo kökünde `hafiza-kur.skill` olarak oluşur (komut yolunu basar). Sonra claude.ai →
   **Customize → Skills → Upload skill** → `hafiza-kur.skill`.

---

## Fikir

Üç cümle:

1. **LOG ile DURUM ayrıdır.** Log tam ve ekle-only'dir, nadiren okunur. Durum
   kompakt ve türetilmiştir, sürekli okunur.
2. **Hiçbir satır silinmez, TAŞINIR** — bayt-birebir, beyanla, ve taşıyan araç
   kendi kapısını koşar; kapı kırmızıysa taşımayı geri alır.
3. **"Kaybolmadı" bir iddia değil TEST SONUCUDUR.** Kapı ölçer; ölçemediğine
   "ölçemiyorum" der — **sessiz PASS yoktur.**

## Ayırt edici olan ne

Bu alanda talimat dosyası (CLAUDE.md, AGENTS.md), hafıza katmanı (mem0, Letta,
Zep) ve memory-bank kalıbı çok. Onlarda **olmayan** üç şey:

- **Kör kapı protokolü.** Bir kapının var olması ısırdığı anlamına gelmez.
  `hafiza.py isir` her kapı için bilerek bir açık üretir ve yakaladığını
  **kanıtlar**. Isırmayan kapının "temiz" hükmü geçersizdir.
- **Sabotaj sınaması.** Testin kendisi de sınanır: koruduğunu iddia ettiği şeyi
  kapat, test `KAÇTI` demeli. Demiyorsa komşu bir sınıfı ölçüyordur.
- **Ölçülemezliğin itiraf edilmesi.** `ÖLÇÜLEMEDİ` PASS'tan ayrı üçüncü bir
  hükümdür ve çıkış kodu bile bunu ayırır. (Bu üçüncüsü özgün değil — GNU
  Automake'in `77 = SKIP`'i ve pytest'in `skip`/`xfail`'i aynı geleneğe ait;
  yeni olan, bunu bir *hafıza/doküman* kapısına taşımak.)

## Kullanım

```bash
python3 skill/scripts/hafiza.py kur   --kok=<proje> --ad "<Proje Adı>"
python3 skill/scripts/hafiza.py kapi  --kok=<proje>   # kapıları koş, hüküm ver
python3 skill/scripts/hafiza.py isir  --kok=<proje>   # kapıların ısırdığını kanıtla
```

İlerlemiş bir projede `kur` **değil** `devral` kullan. Ayrıntı: `skill/SKILL.md`.

`devral`, projenin **kendi karar dizinini** (`docs/ADR` · `docs/adr` · `docs/decisions` · `adr` ·
`doc/adr`; içinde `NNNN-*.md` ya da `ADR-*.md` varsa) bulursa canlıya **yol taşıyan** bir blok yazar
(`konu="karar-kaynagi"`, `sahip="hafiza-kur"`: dizin, dosya sayısı, adlar, ilk başlık) ve yolu
`.hafizarc`a (`karar_dizini`) kaydeder; `derle` bloğu diskten yeniden üretir (dizin silinirse
"YOK (kayıtlı: …)" der, sessizce düşmez). Dosyalara **dokunulmaz**, taşınmaz, kopyalanmaz. Motorun kendi
`kararlar/` dizini de doluysa ikisi birlikte listelenir; hangisinin otorite olduğuna motor karar
vermez. Kurulu bir projede (`.hafizarc` var) `devral` zaten durur: yol yalnız devir anında kaydedilir.

**Çıkış kodları** — `kapi`: `0` yeşil · `1` kırmızı · `2` kullanım hatası ·
`3` ölçüm yapılamadı, hüküm yok · `5` **yalnız `--kapsam-zorla` ile**: hüküm
yeşil ama kapsam eksik (`?` ile işaretli en az bir şey ölçülmedi).
`isir`: `0` hepsi ısırdı · `1` **kapı kör** ·
`2` ölçülemeyen mutant · `4` temiz sürüm zaten FAIL.

`skill-kur`: `0` kuruldu ya da zaten kurulu · `1` kurulum ölçümü tutmadı (kurulmadı) ·
`2` kullanım hatası, kaynakta dizin bağlantısı ya da hedefte FARKLI bir kurulum var (hiçbir şey değişmez) ·
`3` dosya sistemi yazmaya izin vermedi (kurulum tamamlanmadı) ya da beklenmeyen hata (hüküm yok).

`paket`: `0` üretildi ve ölçüldü · `1` üretim sonrası ölçüm tutmadı (paket bırakılmaz) ·
`2` kullanım hatası ya da kaynakta dizin bağlantısı var ·
`3` dosya sistemi yazmaya izin vermedi (paket üretilmedi) ya da beklenmeyen hata (hüküm yok).

**İngilizce takma adlar (yalnız komut adı; bayraklar Türkçe)** — Türkçe ad kanoniktir; takma ad AYNI alt
komuttur ve aynı çıkış kodunu verir (ör. `gate --kok=<proje> --siki` ≡ `kapi --kok=<proje> --siki`):

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

**Yardımcı komutlar**

```bash
python3 skill/scripts/hafiza.py skill-kur          # skill'i ~/.claude/skills/hafiza-kur/ altına kopyalar + ölçer
python3 skill/scripts/hafiza.py paket              # claude.ai / Cowork için hafiza-kur.skill üretir + ölçer
python3 skill/scripts/hafiza.py surum              # sürüm + motorun KENDİ sha256'sı
python3 skill/scripts/hafiza.py hook --kur --kok=<proje>   # pre-commit kapısı kurar
python3 skill/scripts/hafiza.py kapi --kok=<proje> --kapsam-zorla   # CI için
```

`skill-kur`, `skill/` dizinini Claude Code'un skill klasörüne **kopyalar** ve kopya üzerinde
ölçer (motor bit-bit · envanter · kopyadaki motorun `surum` SHA'sı); `--proje <kök>` ile
`<kök>/.claude/skills/` altına kurar. Beyaz liste dışında kalan her dosya paketlenmez/kopyalanmaz ve `DISARIDA BIRAKILDI: <yol> (beyaz liste disi)` satırıyla
**görünür kılınır** (`__pycache__` ve nokta ile başlayan ad/dizinler hariç; çıkış kodu değişmez; kaynakta dizin bağlantısı varsa iki komut da
reddeder: bağlantının içine inilmez, sessizce düşürülmez). Hedefte FARKLI bir kurulum varsa **durur**; `--guncelle`
eskisini `~/.claude/hafiza-kur-yedek/` altına TAŞIR (silmez). Cowork ve claude.ai bu klasörü
okumaz — orada `paket` ile `hafiza-kur.skill`'i üret ve claude.ai'ye yükle.

`paket`, aynı `skill/` kaynağından (aynı **beyaz listeyle**: `SKILL.md` · `references/*.md` · `scripts/*.py`, tek seviye)
`hafiza-kur.skill`'i üretir; `--cikti <yol>` ile
yerini seçersin. Çıktı **deterministiktir** (sıralı ad, sabit tarih/izin, sıkıştırma yok: aynı kaynaktan
iki üretim bayt-birebir eşittir) ve komut üretimden sonra **kendi paketini ölçer** — zip'ten geri
okunan motor kaynakla bit-bit, envanter süzülmüş kaynakla aynı, açıklama en çok 500 karakter
(claude.ai daha fazlasını kayıtta sessizce kırpıyor). Ölçüm tutmazsa paket **bırakılmaz**.
Kaynakta dizin bağlantısı (symlink/junction) varsa `paket` **reddeder** — bağlantıyı izlemez,
sessizce de düşürmez.

`kur`, ağaçta başka bir aracın defterini tanırsa (`CLAUDE.md`, `AGENTS.md`,
`DURUM.md`, `memory-bank/` …) **durur** ve `devral` önerir — belge bunu zaten
söylüyordu, artık kod da zorluyor. Bilerek geçmek için `--yine-de`; geçiş
zincire düşer.

## Depo düzeni

| Dizin | Ne |
|---|---|
| `skill/` | `.skill` paketinin **tek gerçek kaynağı** — `SKILL.md` + `references/` + `scripts/` |
| `skill/scripts/` | Motor (`hafiza.py`) ve kanıt koşucuları (`t_y3.py`, `t_y42.py`). Motorun **ikinci bir kopyası yoktur.** |
| `faz0/` | Ölçüm altyapısı. Koda dokunmaz: ortam sınıfı, Windows probu, otomatik sabotaj |
| `denetim/` | Bağımsız denetim turlarının defteri |
| `.github/workflows/` | 3 platform × 2 Python + ortam sınıfı + kod kalitesi |
| `CLAUDE.md` | **Kalıcı protokol.** Çalışmaya başlamadan önce oku. |

## Kanıtı kendin koş

Beyana güvenme; bu deponun kuralı bu.

```bash
cd skill/scripts
mkdir -p deneme && git init -q deneme
python3 hafiza.py kur --kok=deneme --ad "Deneme"
python3 hafiza.py isir --kok=deneme    # taze projede: 79/79 + 2 SINANMADI, exit 2
python3 hafiza.py not --kok=deneme --konu=genel-durum --metin="ilk not"
python3 hafiza.py derle --kok=deneme
python3 hafiza.py isir --kok=deneme    # derle sonrası: 81/81, exit 0
python3 t_y3.py                        # 20 senaryo, temiz hata
python3 t_y42.py                       # 58 senaryo
```

Mutant sayısını **bağlamsız okuma**: `81/81` yalnız `derle` koşulmuş projede
doğrudur. Taze bir projede `M-H1b` ve `M-DEVIR` ön-koşulsuz kalır — bu sağlıklı
bir projedir ve çıkış kodu `2`'dir.

Ortam sınıfını ölçmek için (root gerekir):

```bash
sudo bash faz0/ortam_olcum.sh          # root olmayan kullanıcı · dolu disk · salt-okunur
python3 faz0/sabotaj.py                # her fail() tek tek kapatılır -> kapsam envanteri
```

## Bilinen sınırlar

Bunlar gizlenmiyor; `skill/SKILL.md` §9'da tam listesi var (H18 satır atfı, K-YOL/K-DURUM karar
dizini ve ADR durumu, K-GECIS kurulu projede karar dizini keşfi, K-ISARET kural evi → canlı defter
işaretçisi dahil). En önemlileri:

- **Yeniden çıpalama engellenemez, yalnız görünür kılınır.** Dosya tabanlı bir
  şemada yazma erişimi olan bir aktöre karşı bütünlük garantisi matematiksel
  olarak imkânsızdır. Doktrin: *tamper-evidence*, *tamper-proof* değil.
- **Zincir anahtarsızdır.** Depo-içi bir zincir, tutarlı biçimde N dosyayı
  düzenleyen bir aktörü durduramaz; yaptığı, maliyeti 1 hamleden N tutarlı
  hamleye çıkarmaktır.
- **Beyanlı gevşeklik gerçek bir kaçış deliğidir.** `politika_gerekce` ile bir
  kapı kapatılabilir; gizlenemez ama **kullanılabilir**. Kaçış yolu olmayan kapı,
  kırılan kapıdır.
- **Disiplin nihayetinde insana/ajana bağlıdır.** Fragman yazılmazsa sistem boş
  döner. Git hook bunu kısmen zorlar, tamamen değil.
- **Uzun hafıza her zaman iyi değildir.** Girdi uzadıkça model başarımı düşer;
  bu yüzden tavan vardır ve canlı dosya **yol taşır, metin taşımaz**.

- **Karar yolu ≠ karar doğrulaması (K-BAYAT/K-DURUM kesme beyanı, 6 Eki 2026).** `karar-kaynagi`
  bloğu karar DİZİNİNE yol verir ve her ADR'nin kendi durum satırını taşır; dizin DIŞINDAKİ
  gerekçe dosyaları (iş emirleri vb.) ve taslak/kilitli ayrımının yorumu okuyucuya kalır. Ölçüldü
  (Momentum, kör okuma): KARAR 2/4; okuyucu `TASLAK` etiketini görüp yine taslağı karar sandı
  (R1 yanlış ×2). Ayrıca H19 yalnız ADI ölçer: "X'i ASLA okuma" satırı kapıyı susturur.

- **Platform hükmü eşit değildir.** `capraz.yml`deki adımlar iki sınıftır: KAPI
  (`continue-on-error` YOK — üç platformlu MUTANT bataryası: h1/h4/h10/h12/h14
  kenar mutantları, altın çıktı/ölçüt/küme ailesi, yapı kapısı, karmaşıklık
  ölçütü ve benzerleri) ve ÖLÇÜM (`continue-on-error: true` — kanıt koşucuları,
  Y-1/Y-3 probları, ortam sınıfı, kalite taraması). Hangi adımın hangi sınıfta
  olduğu ve kaçının bu bayrağı taşıdığı `capraz.yml`den okunur; sayı burada
  yazılmaz (bir kez yazıldı, iki gün içinde bayatladı). Tek belgelenmiş istisna
  `h9_kesme_mutanti`dir: `chown` POSIX'e özgü olduğu için ubuntu kolu KAPI,
  macOS/Windows kolları platform sınırı nedeniyle ÖLÇÜM (`capraz.yml`de
  gerekçesiyle yazılı). Motorda platforma özgü tek
  dal `sys.platform == "win32"` altındadır ve `faz0/win_dal_mutanti.py` onu ölçer:
  envanter ve davranış kapıları temiz, **4/4 mutant ayrı eksende ısırıyor**. Ama o
  aracın kendi hükmü **"YEŞİL SINIRLI"**: üçüncü kapısı (gerçek `win32` üzerinde
  canlı koşum) yalnız Windows kolunda çalışır, diğer iki platformda `ÖLÇÜLEMEDİ`
  basar. Yani hüküm vardır ama her platformda aynı ağırlıkta değildir.
  > *Bu madde bir süre "o dal henüz bir mutantla ölçülmemiştir" diyordu. 16 Ağu
  > 2026'da ölçüldü: cümle bayatlamıştı — mutant zaten vardı ve ısırıyordu.
  > Tazeliği kendin sına: `python3 faz0/win_dal_mutanti.py`*

  macOS'a özgü kod yolu ise hiç yoktur; macOS'un bilinen mayını (dosya adlarında
  NFC/NFD ayrışması) bir kapıyla değil bir **kaçınma kuralıyla** yönetiliyor: disk
  adlarına Türkçe diyakritik konmuyor. Kural, kapı değil — ve kuralı zorlayan bir
  şey yok.
- **"Gerçek bir projede bir hafta fiilen kullanım" maddesi KESİLDİ** (15 Ağu 2026).
  Sebep zaman değil, ölçütün kendisi: token kazancı ancak bu sistem mevcut defterin
  **yerine geçerse** dürüst ölçülebilir. Aday projede mevcut defter kanonik kalacaktı;
  o şartla maliyet tanım gereği artar, kazanç sıfırdır — **sonucu önceden belli olan
  şey ölçüm değildir**, sayı kılığına girmiş bir ÖLÇÜLEMEDİ'dir. Aday projenin bağımsız
  denetçisi ayrıca iki defterin bir arada yaşamasının orada bilinen bir kusur sınıfını
  doğuracağını gösterdi. Yani bu araç, hâlâ **gerçek bir projede bir hafta boyunca
  kullanılmış değildir** ve bu satır o boşluğun kendisidir.
- **Karmaşıklık borcu bilinçli olarak açık bırakıldı.** Motorun sekiz fonksiyonu
  projenin kendi eşiğini aşıyor, beşi CC 20'nin üstünde. 14 Ağu 2026'da bu bölme
  işi KESİLDİ: ölçülebilirliği zayıflatmıyor, yalnız okunabilirliği. Kesim
  gizlenmiyor, burada duruyor.
- **Satır atfı kayması ölçülür (H18); içerik bayatlığı ölçülmez.** `kapi`, canlı defterin
  numaralı maddelerindeki backtick'li `yol:N` atfını ölçer: atıftaki satırda (±2) maddenin
  tanımlayıcısı yoksa ve dosyada başka yerde varsa **KAYMA** der — yalnız uyarıdır, çıkış kodu
  değişmez; `derle` (fragman işlediği koşuda) aynı listeyi canlıya `sahip="hafiza-kur"` bloğu
  olarak yazar, KAYMA yoksa blok yazılmaz. **Kapsam yalnız `canlı`dır** (kural evi, arşiv,
  `HAFIZA_*.md` dışarıda; kod çiti içindeki numaralı maddeler ayırt edilmez). Çözülemeyen ya da
  ölçülemeyen atıf ÖLÇÜLEMEDİ sayısıyla basılır. Satır doğru ama iddia bayatsa (`:85` hâlâ
  "tutuyor" der) bunu **görmez**. H18 `isir` kataloğunda değildir: uyarıdır, `fail` üretmez;
  `faz0/guncel_durum_kapisi_mutanti.py` onu ısırtır.
- **Defter↔kod İÇERİK bayatlığı ölçülmez.** Zaman/sıra tabanlı iki aday Momentum'da ölçüldü
  (5 Eki 2026): isabet A 0/3, B 1/6; motive eden vaka (md.40) iddia doğuşta bayattı (kod 2
  commit önce değişmişti) — mekanik olarak ayırt edilemiyor. Kanıt: `besli-paket` ölçüm raporu
  (depoya kopyalanmaz; bu yüzden bu satırın sayıları depodan doğrulanamaz).

## Denetim

Bu araç üç dış denetçiye verildi. İlk ikisinin kararı `KUR` oldu; üçüncüsü son iki
turunda `DÜZELT` dedi. Bulgular ve kapatılışları `denetim/` ile
`skill/references/denetim-yaniti.md` içindedir.

İki şeyi ayrı yazmak gerekiyor:

- **Denetçilerden yalnız biri depoda adıyla geçiyor** (`Fable 5 Max`); diğer ikisinin
  çıktısı bu depoda yok. Yani "üç dış denetçi" ifadesi depodan **tek tek doğrulanamaz.**
- **Turların bir kısmı üreticinin kendi düşman ajanlarıyla koşuldu.** Onlar bağımsız
  denetim değildir ve öyle sayılmaz.

🔴 **Tur sayısı ölçülemedi, o yüzden burada sayı yazmıyoruz.**
`denetim/2026-08-01_denetciye-not.md` "toplam on iki tur" diyor, dökümünü yedi + üç +
iki olarak veriyor ve üstüne "paketten sonra iki tur daha" ekliyor; bu README bir süre
"on üç" yazdı. Üç ayrı sayı, hiçbiri depodan tek tek sayılamıyor. Aynı belge bunu kendi
üstünde zaten uygulamıştı: *"doğrulanamaz bir sayı, güven parası olarak kullanılamaz."*
Bu satırın kendisi, aracın vaadinin kendi kapağında sınanmasıdır — bir kapı bunu
yakalamadı, dışarıdan bir denetçi yakaladı (bkz. `denetim/2026-08-15_*`).

Açık bulgular kapanmadan bu araç "denetimden geçti" diye sunulmaz.

## Lisans

**MIT.** Tam metin: [`LICENSE`](LICENSE).

> Bu bölüm bir süre "henüz seçilmedi, tüm hakları saklıdır" diyordu. `LICENSE`
> eklendikten sonra aynı depo iki farklı lisans durumu söyledi ve bunu **hiçbir
> kapı ölçmüyordu** (ölçüldü: 10 Ağu 2026). Belge de bir arayüzdür ve yalan
> söyleyebilir — bu depo bunu kendi kapağında bir kez yaşadı.

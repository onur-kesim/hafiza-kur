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
| `adres` | — (takma ad yok) |
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

**Kod adres defteri (`adres`)** — izlenen kod dosyalarındaki **tanımların adresi** (sınıf/arayüz/kayıt/yapı/enum,
metot/fonksiyon/kurucu/özellik, ok-fonksiyon ataması, alan/sabit): `arsiv/hafiza/ADRES.tsv`. İlk dilim dört dil:
Python (`ast`, kesin) · C# · Dart · TypeScript/JavaScript (stdlib desenleri + parantez dengeleme). Amaç: bir asistan
"bu sembol nerede, kim çağırıyor?" sorusunu **bütün depoyu okumadan** cevaplasın; cevabın büyüklüğü sorunun büyüklüğü
kadardır, projenin değil. Çıktı düz metindir (Claude'a bağlı değil).

```bash
python3 skill/scripts/hafiza.py adres --kok=<proje> --kur                  # defteri (yeniden) üretir
python3 skill/scripts/hafiza.py adres --kok=<proje> ShouldResyncAsync      # tanım adresi + çağıranlar
python3 skill/scripts/hafiza.py adres --kok=<proje> --mahalle src/Sync     # o önekteki tanımların listesi
```

- **`--kur`** git'in **izlediği** kod dosyalarını okur (git deposunun alt dizininde de; git yoksa dosya sistemi — `.gitignore`
  saygısı YOK, budanan dizin adları ve atlanan bağlantı/okunamayan dizinler çıktıda **söylenir**). Satır: `yol` ⇥ `tür` ⇥
  `nitelikli ad` ⇥ `başlangıç` ⇥ `bitiş` ⇥ `parmak izi (8 hex)`. Başlangıç = adın geçtiği satır, bitiş = gövde `}` ya da
  bildirimi bitiren satır; nitelikli ad `Sınıf.üye` (iç içe `A.B.üye`; C# ad alanı ada GİRMEZ). **Parmak izi**, o
  satırların (satır sonu boşlukları atılmış, LF) SHA-256'sının ilk 8 hex'idir: gövde değişince değişir, yalnız
  boşluk/CRLF değişince **değişmez**; **adın ÖNCEKİ satırları** (attribute/decorator/ek açıklama/dönüş tipi bir üst
  satırdaysa o) izin DIŞINDADIR. Her dosya için ayrıca bir `dosya` satırı vardır (ad sütunu = dosyanın tam SHA-256'sı:
  bayatlık kararı buna bakar; tanım listelerinden süzülür). Aynı ağaç + aynı motor → `ADRES.tsv` bit-bit aynı (sıralı,
  LF, UTF-8; Windows/Linux, Python 3.12/3.14'te ölçüldü); istisna: Python dosyası yorumlayıcı sürümüne özgü sözdizimi
  taşıyorsa eski sürüm onu `ATLANDI sozdizimi` sayar. Başlık satırı: motor sürümü + kod ağacı özeti + dil başına
  dosya/tanım sayısı + `atlanan=` alanı (gömülü/üretilmiş dosyalar; aşağıda). Dört dil dışındaki kaynak diller
  `KAPSAM DISI DIL: n dosya (.kt 12, .java 3)` olarak **sayılır**, gizlenmez. UTF-16/UTF-32 (BOM'lu) çözülür; UTF-8 olmayan dosya latin-1 varsayılır ve `UYARI` basılır; NUL baytlı (ikili)
  dosya `ATLANDI ikili`dir. Bir dosyada çıkarıcı **beklenmedik** istisna atarsa defter yine yazılır, çıktı `ARAC KUSURU`
  der ve `exit 3` döner (dosyanın kendi sözdizimi hatası araç kusuru DEĞİLDİR: `ATLANDI sozdizimi`). Yol sütununda sekme/satır
  sonu `%09`/`%0A`/`%0D` olur; adda gerçekten `%09`/`%0A`/`%0D`/`%25` dizisi varsa onun `%`si `%25` yazılır (kaçış tersinirdir:
  iki ayrı dosya tek anahtara düşmez). Python'da `if/try/with/for/while/match` ve `except*` gövdeleri ile `type X = ...` (3.12)
  de taranır; Python adlarını `ast` NFKC'ye çevirir (kaynakta `µ` yazılı bir ad defterde `μ`dür — bilinen sınır).
- **Gömülü/üretilmiş paket dosyaları ATLANIR (P2.1).** İzlenen olsalar bile taranmaz: ne deftere ne çağıran listesine
  girerler (fxa'da `.yarn/releases/yarn-4.9.2.cjs`, `parse`/`load`/`init` gibi adların çağıranlarına karışıyordu).
  **Liste TEK tablodur ve budur:** yolun herhangi bir seviyesinde şu adlı bir dizin bileşeni — `.yarn`, `node_modules`,
  `vendor`, `dist`, `build` — ya da dosya adının sonu `.min.js` / `.cjs`. Eşleşme tam bileşendir ve büyük/küçük harfe
  DUYARLIDIR (`src/build_tools/` ve `src/Dist/` atlanmaz); dizin sonekten önce sayılır (`.yarn/x.cjs` → `.yarn`).
  Liste `.hafizarc` ile genişletilemez. Atlama **sessiz değildir**: `--kur` konsolu `ATLANAN: 5 dosya (.yarn 2, *.cjs 1,
  *.min.js 1, vendor 1)` basar (sayı azalan, sonra ad; yalnız kod ya da kapsam dışı uzantılı dosyalar sayılır —
  `README.md`, `package.json` sayılmaz; atlama `KAPSAM DISI DIL` sayımından ÖNCE uygulanır, atlanan dosya orada da yoktur);
  `ADRES.tsv` başlığına `atlanan=.yarn:2,*.cjs:1,…` (yoksa `atlanan=-`) yazılır; atlanan bir dosyadaki ad sorulup
  bulunamazsa `BULUNAMADI` cevabının altında `(defter TARAMADI - gomulu/uretilmis dosyalar atlandi: .yarn:2,…)` basılır.
  Sorgu, `--mahalle` ve bayatlık kararı AYNI süzgeci kullanır (atlanan bir dosyanın değişmesi defteri bayatlatmaz). Git
  yokken dosya sistemi yürüyüşü `node_modules`/`dist`/`build`'i zaten budar (`not    : budanan dizin adlari`) ve onlar
  ATLANAN'da sayılmaz; yalnız `.yarn`, `vendor`, `*.min.js`, `*.cjs` sayılır. Defter biçimi `1` kaldı: eski okuyucu yeni
  alanı yok sayar, yeni okuyucu eski defteri okur — atlanan dosyaları kapsayan eski bir defter `ADRES DEFTERI BAYAT`
  görünür (`--kur` yeniler).
- **Yükleme anında etkisiz — tembel kurulum (P2.1).** `hafiza.py` yüklenirken adres koduna ait HİÇBİR desen derlenmez ve
  HİÇBİR desen tablosu kurulmaz: desenler ilk kullanımda derlenen tembel vekillerdir, dil kural tabloları ilk `adres`
  çağrısında bir kez kurulur, `ast`/`bisect`/`difflib`/`warnings` yalnız adres fonksiyonlarının içinde alınır (yükleme
  sırasındaki `re.compile` çağrısı motor toplamında 120 → 29, adres bloğundan 0; 8 Eki 2026, `0d7ce4a` ölçümü). Sonuç:
  bir adres deseni ya da tablosu bozulsa yalnız `adres` düşer (`--kur` → `exit 3`); `kapi`/`derle`/`devral`/`not`/`isir`
  çıktısı ve çıkış kodu bayt bayt aynı kalır — `faz0/adres_mutanti.py` bunu yükleme anında bozulmuş desen ve tablo
  enjekte ederek ölçer (A-ETKI kolu, `ETKI-YUKLEME` ekseni).
- **`adres <ad>`** tanım(lar)ı ve **çağıranları** basar (çağıranın kendi adresine gruplanmış: `yol > Sınıf > üye:satır`;
  tanım satırları hariç, aynı satırdaki geçişler tek; en çok 30 satır + `+N daha`). Ad kısmi verilebilir (`ShouldResync`
  → tam eşleşme + `BENZER AD` olarak `ShouldResyncAsync`); eşleşme yoksa `exit 1` + en yakın 5 ad. Çıktı ayracı ASCII `>`
  ve `-`'dir (iş emrindeki `›`/`—` yerine: KISIT "ASCII konsol çıktısı"); yol ve ad olduğu gibi basılır.
- **Yorum ve metin içindeki geçişler çağıran SAYILMAZ (P2.1).** Çağıran taraması, tanım çıkarıcının kullandığı AYNI maske
  fonksiyonunu kullanır (ikinci kopya yok): yorum, dize ve biçim belirteci (`f"{x:ad}"`, `$"{x,10:D13}"`) içindeki geçişler
  çağıran değildir; enterpolasyon delikleri (`f"{ad(1)}"`, `$"{Ad(1)}"`, Dart `'${ad(1)}'`) GERÇEK koddur ve sayılır.
  Sayılmayan geçişler gizlenmez, tek satırla beyan edilir: `NOT: 7 yorum/metin icindeki gecis sayilmadi` (Momentum
  `kanonikDize`: çağıran 5 adres → 1 adres; elenen 7 satırın hepsi yorum ya da dize, elle doğrulandı). Maske kurulamayan
  dosya (iç içe dize derinliği Python'un özyineleme sınırını aşarsa) ham metinden taranır ve bu da söylenir: `NOT: n dosyada
  maske kurulamadi - ham metin tarandi (o dosyada yorum/metin icindeki gecisler de sayildi)`. Maskenin başka bir istisnası
  araç kusurudur (`exit 3`), yutulmaz.
- **Bayatlık gizlenemez:** kod ağacı (çalışma ağacındaki dosya içerikleri; `git ls-files -s` DEĞİL — commit'siz/stage'siz
  düzenlemeyi görmez) değişip defter eskirse sorgu YİNE cevap verir ama ilk satır `ADRES DEFTERI BAYAT: <n> dosya
  degisti` olur ve `exit 1` döner. Defter yoksa `ADRES DEFTERI YOK`, `exit 1`.
- **Sorgu hızı: ucuz bayatlık yolu ve önbellek (P2.1).** Eskiden her sorgu bütün izlenen kod ağacını yeniden okuyup
  özetliyordu. Şimdi sorgu, **proje dışında** tutulan bir önbellek notuna dayanır (`<geçici dizin>/hafiza-adres-<proje
  yolunun SHA-256'sının ilk 16 hex'i>.json`, POSIX'te `0600`): bir dosyanın (mtime, boyut, **değişiklik zamanı**)
  önbellektekiyle aynıysa içeriği yeniden özetlenmez, çağıran araması yoksa (`--mahalle`) hiç okunmaz. Projeye dosya
  EKLENMEZ (geçici dizin proje ağacının içindeyse önbellek kapalıdır) ve `ADRES.tsv`'nin içeriği ve biçimi DEĞİŞMEZ.
  Önbellek yalnız bir nottur, bayatlığı gizleyemez: (1) defterin özetine bağlıdır (`--kur` defteri yenileyince eski önbellek
  kendiliğinden düşer); (2) **racy koruması** (git'in racy-git mantığı): mtime'ı ya da değişiklik zamanı sorgunun başladığı
  andan 3 sn'den yakın dosya önbelleğe GİRMEZ; (3) önbellek yok / bozuk / taşan sayılı / başka kullanıcıya ait /
  yazılamaz ise komut tam yola düşer — komut DÜŞMEZ, çıkış kodu değişmez, yalnız yavaşlar; (4) POSIX'te anahtara `st_ctime`
  girer: içerik yazmak da `os.utime`/`touch -r` ile mtime'ı GERİ almak da onu ilerletir (aynı boyut + eski mtime ile
  değişiklik görülür); (5) **Windows'ta** stdlib'de değişiklik zamanı yoktur (`st_ctime` oluşturma zamanıdır), bu yüzden
  NTFS/ReFS `ChangeTime` dosya başına `ctypes` ile (kernel32) okunur — dosya AÇILMAZ, yalnız nitelik tutamağı alınır.
  `ctypes` yüklenemezse, birim NTFS/ReFS değilse (FAT/exFAT) ya da dosya açılamazsa (uzun yol, paylaşım ihlali) o dosya
  önbelleğe girmez ve tam yoldan gider (yanlış-negatif yok). Çağıran aramasında ham bayt ön süzmesi vardır: ad ASCII ise
  ve dosyanın ham baytlarında geçmiyorsa dosya metne çevrilmez; UTF-16/32 BOM'lu, ortasında U+FEFF olan ya da ASCII olmayan
  adla latin-1 dosyada süzme KAPALIDIR (çağrı kaybolmaz). **Ölçüm** (10 Eki 2026, Windows, Python 3.12, sıralı-karışık 3
  koşunun ortancası, makine gürültülü — tek makine, genellenmez): fxa kopyası (4.937 kod dosyası) `adres track` önbelleksiz
  motorda 2,91 s → önbellekli SOĞUK (ilk sorgu, önbelleği kurar) 3,31 s → SICAK 1,52 s; Momentum (334 dosya) `adres
  kanonikDize` 0,56 s → 0,60 s → 0,41 s. Çıktı soğukta ve sıcakta önbelleksiz motorla BAYT BAYT aynıdır. **İlk sorgu eskisinden
  yavaştır** (önbelleği kurmanın bedeli); sorgu süresi yine projeyle büyür: her sorgu her kod dosyasını `lstat` eder ve
  `adres <ad>` çağıran araması için dosyaları ham bayt olarak okumaya devam eder — düşen, değişmemiş dosyaların yeniden
  özetlenmesi (SHA-256, metne çevirme) ve `--mahalle`'de okumanın kendisidir.
- **`--mahalle <dizin ya da önek>`** o yol önekindeki tanımların tek satırlık listesi (en çok 60 satır + `+N daha`).

`adres`: `0` bulundu / kuruldu · `1` bulunamadı, defter YOK ya da BOZUK, ya da BAYAT (cevap yine basılır) ·
`2` kullanım hatası / `arsiv` bir dosya (yapı bozuk) · `3` araç kusuru (`git ls-files` başarısız, git alt dizininde
`dubious ownership`, defter okunamadı, çıkarıcı ya da çağıran maskesi beklenmedik istisna). Bozuk defter (sayısal ama
anlamsız satır aralığı dahil) `exit 1 BOZUK`tur, asla `exit 3`/asılma. Takma adı yoktur (`hook` gibi).

**Bilinen sınır (baştan yazılır):** C#/Dart/TS/JS çıkarımı **desen tabanlıdır, AST kadar kesin DEĞİL** — dinamik
çağrı, aşırı yükleme, yansıma, string içi ad kaçar ya da fazla sayılır. Bilinen kayıplar: `#if` ile dengesiz süslü parantez,
JS nesne literalindeki yöntemler, çok bildirimli `int a, b;` (yalnız ilk ad), tırnaklı/hesaplanan enum üyeleri, C# 14
`extension(...)` blokları, adsız sınıf ifadesinin üyeleri, noktalı virgülsüz JS'te `(`/`[` ile başlayan satır devamı (JS'in
kendi ASI kuralı; `}` ardından satır başı `(`/`[` de), ilkleyicisiz `let x` ardından `[`, tek ifadede `exports.a = 1, exports.b = 2`
zincirinin yalnız ilk adı, ardışık `a<b` … `c>d` karşılaştırmaları (C# tür argümanı sanılır), TS'te bildirim başına ALAN adı olan
tipsiz ve noktalı virgülsüz `private x?` / `private y` alan çifti, satır başındaki regex literali. JSX yalnız `.tsx/.jsx/.js`'te maskelenir ve 100'ü
aşan iç içe JSX `ATLANDI sozdizimi` sayılır (kod sanılıp sonrası yutulmaz); tek bildirimde binlerce süslü literal (Dart `..a = {1}`
zinciri, üretilmiş kod) ikinci dereceden yavaşlar. **"Çağıran" listesi sözcük
eşleşmesidir, tip çözümlemesi DEĞİLDİR** (farklı tiplerin aynı adlı üyeleri ayrılmaz; yorum ve string içindeki geçişler
P2.1'den beri sayılmaz, ama sayılmadıkları `NOT:` ile söylenir); bu sınır çıktıda da basılır:
`NOT: cagiranlar sozcuk eslesmesidir`. Cevabın boyutu sorunun boyutuyla büyür; SÜRE projeyle büyür (sorgu hızı:
yukarıda). Ölçüm: `faz0/adres_mutanti.py` (dokuz kol — A-TANIM, A-CAGIRAN, A-PARMAK, A-BAYAT, A-DETERMINIZM, A-MASKE,
A-ATLA, A-ETKI, A-KOMUT-SATIRI; 57 sabotaj, her biri ayrı eksende sınanır).

**P2.1 ile eklenen sınırlar (ölçüldü, gizlenmez):** ağır patolojik girdi yine yavaştır — iç içe f-dize/`$"…"` derinlik ×
boyut ile ikinci dereceden büyür (100 iç içe dize × 20 KB = 39,9 s), Dart/C# desenlerinde çok uzun boşluk dizisi de ikinci
derecedendir (n=16000 ≈ 1,4 s/dosya) ve dosya başına zaman aşımı YOKTUR. TS/JS desenlerindeki kübik ve ikinci dereceden
geri izleme (bitmemiş yorum + uzun boşluk dizisi) kapatıldı (n=16000: 0,00–0,04 s; `TANIM-TS-SURE` ekseni 20 s zaman
aşımıyla ölçer). C# biçim belirtecinde kaçışlı çift tırnak (`\"`) çok nadir bir sınıfta yanlış okunur; parantezsiz `?:`
üçlü ifadesi belirteç sayılır (C# derleyicisi onu zaten reddeder). Atlama: `--mahalle <atlanan önek>` `BULUNAMADI` basar
ama `TARAMADI` notunu basmaz (not yalnız `adres <ad>` dalındadır); sonek eşleşmesi büyük/küçük harfe duyarlıdır (`A.CJS`
taranır) ve Windows'ta `a.MIN.js` ile `a.min.js` aynı dosyadır (dosya sistemi). Önbellek: proje ağacının içinde başka
birime bağlanmış (mount/junction) dizin denetlenmez; FAT/exFAT'ta Windows ChangeTime yolu kapalıdır (yalnız benzetimle
sınandı), Linux vfat/exfat'ta `st_ctime` güvenilirliği, `ChangeTime`'ı bilerek geri yazan araç (yönetici) ve macOS (POSIX
ile aynı kod yolu) ayrıca **ÖLÇÜLEMEDİ**.

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

- **Taslak ≠ karar: `karar-kaynagi` bloğu ADR'leri dört sınıf grubunda verir (P1, 6 Eki 2026) —
  BİLİNÇLİ DÖNÜŞ.** K-DURUM "motor durumu YORUMLAMAZ" demişti; ölçüm (Momentum kör okuma, R1 yanlış ×2)
  etiketin okuyucuya ulaştığını ama okuyucunun taslağın içeriğini yine karar diye aktardığını gösterdi.
  Bu yüzden motor artık durumu SINIFLAR — ama gizlenemez biçimde: (i) sınıf SABİT sözlükten gelir (aşağıda),
  (ii) her satır ham `[durum: …]` metnini AYNEN taşır ve sınıf yalnız bu görünen metinden türer (okuyucu
  motorun sınıflamasını ham beyanla her zaman karşılaştırabilir), (iii) **şüphede sınıf ASLA `GECERLI`
  değildir** (taslağın karar sanılması zararlıdır; kilitli kararın taslak sanılması ucuz hatadır).
  Dört başlık HER ZAMAN sayıyla basılır (`GECERLI KARARLAR (0)` dahil): `GECERLI KARARLAR` ·
  `KARAR DEGIL - TASLAK/BEKLEYEN` · `GECERSIZ` · `SINIFLANAMADI`; `derle`/`devral` ayrıca
  `KARAR SINIFI: GECERLI 2 · TASLAK 3 · GECERSIZ 0 · SINIFLANAMADI 0` yazar. Tavan (40) toplamdır,
  gruplar sabit sırada dolar, kırpılan sayı grup başına yazılır.
  **Sözlük ve ÖNCELİK (yukarıdan aşağı, ilk eşleşen kazanır; önce Türkçe katlama `İ ı→i`, `ş→s`,
  `ğ→g`, `ü→u`, `ö→o`, `ç→c`, sonra `lower()`; sözcük sınırlı eşleşme — `red` ≠ `kredi`):**
  1. `GECERSIZ` — superseded · yerine gecildi · yerine-gecildi · deprecated · rejected · reddedildi · red · iptal · withdrawn · obsolete
  2. `TASLAK` — taslak · draft · proposed · onerildi · oneri · onerilen · bekliyor · bekleyen · pending · wip · tartisma · discussion · inceleme · review · **degil** · **not accepted**
  3. `GECERLI` — kabul · accepted · kilitli · approved · onaylandi · final · adopted · yururlukte
  4. `SINIFLANAMADI` — geri kalan HER ŞEY (`BEYANSIZ` dahil)

  `TASLAK`, `GECERLI`'nin ÜSTÜNDE: `TASLAK v6 — KİLİTLİ DEĞİL` ve `GÖVDE YAZILDI — KİLİT BEKLİYOR`
  "kilit" kökünü taşır ve ikisi de karar DEĞİL. **Sınırlar:** sözlük dışı beyan `SINIFLANAMADI`'ya düşer;
  motor beyanın ANLAMINI ölçmez — `kabul` yazan bir taslak `GECERLI` görünür (`kabul edilmedi` / `not
  approved` sözlükte yok: `kabul`/`approved` GECERLI sayılır); sınıf 60 karakterlik GÖRÜNEN metinden
  türer, kırpılmış kuyruk sınıfı değiştirmez.

- **H14 büyük projede git'e yolları PARÇALI sorar (6 Eki 2026).** mozilla/fxa kopyasında (8.335 izlenen dosya,
  yolların toplamı ~509.000 karakter) `kapi` Windows komut satırı sınırında (~32.767 karakter) `exit 3`
  (`[WinError 206]`) veriyordu. `_git_son_ct` yolları girdi SIRASIYLA parçalara böler (her parçada karakter
  toplamı + 1 ayraç ≤ `_GIT_YOL_BUTCE` = 8.000; tek yol bütçeyi aşarsa kendi parçası) ve sonuç olarak parçaların
  EN BÜYÜK commit tarihini alır; tek parçaya sığan projede çıktı eskisiyle aynıdır. `_h12_hafiza_git_tarihi`
  (H12/H14'ün hafıza tarafı) BİLEREK dönüştürülmedi: yolları `HAFIZA_*.md` arşiv dosyaları kadardır
  (proje dosya sayısıyla büyümez; ~500 arşiv dosyasında sınıra yaklaşır) ve hata halinde exit 3 değil `None` döner.
  Sınır: `devral`'ın gömülü kapı çöküşünde exit 0 dönmesi bu işin kapsamı DIŞI. Kapı: `faz0/h14_parca_mutanti.py`
  (WIN-UZUN kolu yalnız Windows'ta ısırır; Linux/macOS'ta `OLCULEMEDI: bu platformda sinir yok` der).

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

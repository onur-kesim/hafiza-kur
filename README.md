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
  dosya `ATLANDI ikili`dir. Bir dosyada çıkarıcı **beklenmedik** istisna atarsa çıktı `ARAC KUSURU`
  der ve `exit 3` döner; mevcut SAĞLAM defter varsa EZİLMEZ, yoksa eksik defter yazılır (aşağıda "Eksik defter"). Dosyanın kendi
  sözdizimi hatası araç kusuru DEĞİLDİR: `ATLANDI sozdizimi`. Yol sütununda sekme/satır
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
  enjekte ederek ölçer (A-ETKI kolu, `ETKI-YUKLEME` ekseni). P5'ten beri `not` (damga, doğuşta bayat) ve `kapi` (H20) adres
  koduna YALNIZ uyarı üretmek için dokunur: oradaki her istisna `OLCULEMEDI`dir, hükümleri ve çıkış kodunu etkilemez (aşağıda).
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
- **Eksik defter (P5 KALEM 0).** Çıkarıcı bir dosyada beklenmedik istisna atınca (`exit 3`) eski motor defteri yine yazıyordu ve
  mevcut SAĞLAM defteri eksik olanla EZİYORDU (Cowork ölçümü: 566 B/5 tanımlı defter 423 B/2 tanımlıya düştü, ilk satır yine
  `KURULDU`). Şimdi: okunabilir sağlam defter varken `--kur` YAZMAZ — `ADRES DEFTERI KURULAMADI: n dosyada cikarici istisnasi` +
  `ESKI DEFTER KORUNDU: <yol> (<bayt> bayt, tanim <t>)` + `ATLANDI`/`ARAC KUSURU` satırları, `exit 3`. Sağlam defter YOKSA ya da
  BOZUKSA eksik defter yazılır, ilk satır `ADRES DEFTERI EKSIK KURULDU` der ve başlığa `cikarici=<n>` damgası girer (çıkarıcı
  kusuru yokken başlık ve çıktı BAYT BAYT eski). Başlığında `cikarici=` taşıyan EKSİK defter bir **sorguda** `güncel` SAYILMAZ
  (eskiden `ozet` kaynak ağacını yansıttığı için bayatlık yolu onu yakalamıyordu): `adres <ad>` / `--mahalle` önce defteri yeniden
  kurmayı dener; eksik değilse yazar (yazılamazsa bellekte kullanır) ve `ADRES DEFTERI YENIDEN KURULDU` basar, hâlâ eksikse
  `ADRES DEFTERI EKSIK: ...` der ve eski (eksik) defterle cevaplar. Yalnız ÇIKARICI kusuru eksik sayılır: dosyanın kendi sözdizimi
  hatası (`ATLANDI sozdizimi`) yeniden kurdurmaz. Sorgunun çıkış kodu değişmez; defter YOK/BOZUK/BAYAT davranışı AYNEN (sorguda
  otomatik kurulum yalnız bu eksik-defter hâli içindir).
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
yukarıda). Ölçüm: `faz0/adres_mutanti.py` (on yedi kol — A-TANIM, A-CAGIRAN, A-PARMAK, A-BAYAT, A-DETERMINIZM, A-MASKE,
A-ATLA, A-ETKI, A-EZME, A-EKSIK, P5-DAMGA, P5-H20, P5-DOGUS, P5-BIRLESIK, P5-SABIT, P5-SAYIM, A-KOMUT-SATIRI; 207 sabotaj, her
biri ayrı eksende sınanır; P5-BIRLESIK sabotaj koşusunda yalnız sabotajın KENDİ ekseninin vektörlerini koşar).

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

**Parmak izli atıf (P5; `adres` defterine dayanır)** — "kod değişti, defter eski kaldı" gizlenemez olsun diye: bir not bir kod
adresine atıf yapıyorsa o anki **gövde parmak izi** satır içine yazılır, `kapi` onu bugünkü izle karşılaştırır, `not` anında
sembolün yakın geçmişte değişip değişmediği söylenir. Üçü de **UYARIDIR**: engellemez, çıkış kodu DEĞİŞMEZ, yeni kod yok;
içlerindeki her istisna (çıkarıcı kusuru, git hatası, zaman aşımı dahil) `OLCULEMEDI`dir ve `not`/`kapi`nın başka hükmünü etkilemez.

```bash
python3 skill/scripts/hafiza.py adres --kok=<proje> --kur                                   # önce defter
python3 skill/scripts/hafiza.py not   --kok=<proje> --konu=genel-durum --metin='7. `HesaplaToplam` KDV iki kez ekler'
python3 skill/scripts/hafiza.py kapi  --kok=<proje>                                         # H20: damgalı atıflar gövdesi değişti mi
```

- **Damga (`not`).** Fragman metnindeki backtick'li belirteçler — H18'in tanımıyla AYNI (`_atif_cikar` kuralları; dil sabitleri
  hariç, aşağıda): tanımlayıcı
  `[A-Za-z_][A-Za-z0-9_]{3,}` ya da `yol:N` / `yol:N-M` — `ADRES.tsv`'de çözülürse (ad ya da `Tür.üye` son eki) kapanış
  backtick'inin hemen arkasına gövde parmak izi eklenir: `` `HesaplaToplam`#a3f9c1d2 ``. İz, defteri üreten AYNI fonksiyondan
  gelir ve dosyanın **canlı** çıkarımından hesaplanır (defterdeki satırdan değil; diske yazılmaz). Ad → dosya eşlemesi
  defterden, `yol:N` için satır → tanım eşlemesi dosyanın **canlı** çıkarımından yapılır (defter bayatsa yanlış sembole damga
  basılmasın); `yol:N` damgası N..M aralığını kapsayan **en dar** tanımındır (iç içe tanımda sınıf değil üye), ters aralık
  (`a.py:9-3`) çözülemez.
  **Birleşik damga (P5.2).** Bir AD 2–5 tanıma çözülürse (arayüz bildirimi + uygulama + test çifti, iki dosyada aynı ad, C#
  aşırı yükleme, Python `@x.setter` çifti) iz, tanımların tek tek gövde izlerinin SIRALANIP `\n` ile birleştirilmesinin SHA-256'sının
  ilk 8 hex'idir — dosya YOLU ize girmez (dosya adı/yeri değişince iz değişmez). TEK tanımda iz o tanımın kendi izidir (P5
  damgalarıyla bayt bayt aynı; mevcut TEKİL damga, adın tek tanımı kaldığı sürece geçersizleşmez — aynı adlı yeni bir kardeş
  tanım gelirse H20 `GOVDE DEGISTI` + `TANIM SAYISI DEGISTI` der). Damganın satır içi biçimi AYNI kalır (`` `Ad`#hex8 ``);
  kaç tanımdan geldiği yalnız konsolda görünür (örnek biçim): `ATIF DAMGALANDI: 1 (ShouldResyncAsync#9e41b07c [3 tanim])`. **Tavan 5:** 6+
  tanım → damga YOK, `ATIF COKLU: <ad> (k tanim, tavan 5) - damgalanmadi` + `DOGUSTA BAYAT: OLCULEMEDI (<ad> COKLU)`. Aday
  tanımlardan HERHANGİ birinin çıkarımı arızalıysa kısmi (eksik tanım kümesinden) iz YAZILMAZ: `ATIF OLCULEMEDI: <ad> (<sebep>)` (sebep: `CIKARICI` · `SOZDIZIMI` · `IKILI` · ...);
  adaylardan BİR KISMI canlı çıkarımda yoksa (dosya taşınmış/yeniden adlandırılmış, defter bayat) yine kısmi iz yazılmaz:
  `ATIF OLCULEMEDI: <ad> (DEFTER_BAYAT)` — `adres --kur` sonrası iz ölçülür. HEPSİ yoksa eski davranış (`DOSYA_YOK` /
  `COZULEMEDI`).
  `yol:N` belirteci iki dosyaya çözülür ya da bakılan satırın tam adı aşırı yüklüyse (aynı tam adlı birden çok gövde) yine damga
  YOK: `ATIF COKLU: <belirtec> (k tanim) - damgalanmadi` (k = dosya sayısı ya da aynı tam adlı gövde sayısı; satır tek tanıma aittir
  ama izi o ada bağlı kümeden ayrılamaz). Defter ATLANDI dosya taşıyorsa (sözdizimi hatası vb.) bir ADIN tanım kümesi EKSİK olabilir:
  damga yine basılır ama `ATIF NOT: defter ATLANDI dosya iceriyor - ad icin tanim kumesi EKSIK olabilir ...` satırı eklenir. Dil sabitleri (**`true false null None True False nil this self void undefined`**)
  backtick'li olsa da tanımlayıcı adayı SAYILMAZ (K5): satır YOK, damga YOK, H20 sayımı YOK — kodda o adda bir tanım olsa
  bile; tam eşleşme, büyük/küçük harf AYNEN (`trueValue`, `TRUE` listede değildir ve bugünkü gibi `COZULEMEDI` der).
  Bulunamadı → `ATIF COZULEMEDI: <ad>`; defter yok/bozuk/eksik, çıkarıcı
  kusuru ya da kök dışına kaçan defter yolu → `ATIF OLCULEMEDI: <sebep>`. Zaten `#hex8` taşıyan belirteç yeniden damgalanmaz
  (idempotent); kapanış backtick'ine bitişik ek (`` `ad`un ``, apostrofsuz) damgalanmaz (`... (bitisik sonek - damgalanmadi)`:
  damga ekle birleşip bir sonraki `not`ta tanınmazdı); çift/üçlü backtick aralıkları ve kod çitleri içindeki satırlar damgalanmaz;
  `derle` damgayı canlıya olduğu gibi taşır (metin dokunulmaz). Damgalananlar `ATIF DAMGALANDI: n (ad#iz, ...)` satırıyla
  söylenir (en çok 10 + `+N daha`); aday belirteç yoksa `not` çıktısı BAYT BAYT eskidir.
  **Bayat defter (P5.4).** Notta belirteç VARKEN ve defter okunabilirse `not` (K1 damga + K3 doğuşta bayat), `kapi` H20'nin
  bayatlık yoluyla AYNI geçişi (`_h20_taze`: `_adres_bugun` + değişen/yeni dosyaların bellekte yeniden çıkarımı; `not` önbelleği
  yazmaz) çalıştırır ve damgayı/doğuşta-bayat taramasını TAZE aday kümesinden verir: defter bayatken yeni dosyada aynı ad eklenmişse
  `[k+1 tanim]` damga basılır ve hemen `kapi` `GOVDE DEGISTI 0` der (sahte uyarı yok); K3 `<k+1> tanimdan 1'i son commit'te
  degisti` der (yeni tanım pencerede eklenmiştir). Taze küme ÇIKARILAMAZSA (bayat dosya sayısı 100 ya da boyutu 8 MiB aşılırsa,
  bayatlık ölçülemezse, defter `git` kaynaklıyken `.git`siz kopyada, yeni/değişen dosyanın çıkarıcısı kusurluysa) **damga BASILMAZ**:
  her aday için `ATIF OLCULEMEDI: <ad> (DEFTER_BAYAT)`, sebebi söyleyen `ATIF NOT: taze aday kumesi cikarilamadi (<durum>: <sebep>) -
  eksik kumeden damga/dogusta bayat VERILMEZ; hafiza.py adres --kur` ve `DOGUSTA BAYAT: OLCULEMEDI (DEFTER_BAYAT: ...)`; fragman
  gövdesi değişmez, exit 0. Yeni/değişen dosya çıkarılamıyorsa (sözdizimi hatası...) ve adı sözcük olarak içeriyorsa o ad için damga YOK
  (`OLCULEMEDI (DEFTER_BAYAT)`, K3 `OLCULEMEDI (<ad>: DEFTER_BAYAT)` der; tek tanımlı adın dosyası bozulmuşsa da: `COZULEMEDI` DEĞİL);
  adı içermiyorsa damga basılır (+ `ATIF NOT: defter ATLANDI ...`). Silinen/izlenmez
  dosyanın satırları `--kur` gibi düşer: tüm aday dosyalar silinmişse `ATIF COZULEMEDI` (eski `OLCULEMEDI (DOSYA_YOK)` değil).
  **Bedel:** damgasız (damgalanabilir) ADAY belirteç taşıyan her `not` kilidi TUTARKEN bir bayatlık geçişi (soğuk: tüm izlenen kod
  dosyalarının özeti; sıcak: stat) ve bayat dosyaların çıkarımını koşar — ölçülmüş sayılar sınır (18)'de; adaysız `not` bu bedeli ÖDEMEZ.
- **H20 (`kapi`).** Canlı defterdeki (H18 gibi yalnız `canli`; madde sınırları da H18'inkiyle AYNI, kod çiti içi satırlar hariç)
  **damgalı** atıfları okur — madde numarası taşımayan satırdaki damga da okunur (`satir N`): damga açık bir işarettir, gizlenemez.
  Her biri için ad → dosya eşlemesini `ADRES.tsv`'den, **bugünkü** gövde parmak izini o dosyanın canlı çıkarımından alır (bellekte;
  diske yazmaz — bayat ya da ezilmiş defter hükmü bozmaz). **Ad** için kapı anında defter satırlarının BUGÜNKÜ tüm tanımlarının
  birleşik izi damgayla karşılaştırılır (satır kayması/dosya taşıma değiştirmez; tanım EKLENMESİ ya da SİLİNMESİ izi değiştirir →
  `GOVDE DEGISTI`; bugün 6+ tanım `OLCULEMEDI [COKLU_TAVAN]`); `yol:N` için damga dosyadaki HERHANGİ bir tanımın izine eşitse aynı.
  **Bayat defter (P5.3).** Damgalı atıf VARKEN `kapi`, `adres <ad>` sorgusunun AYNI ucuz bayatlık yoluyla (`_adres_bugun`: izlenen
  kod dosyalarının içerik özeti; sorgu önbelleği yalnız OKUNUR, `kapi` hiçbir şey YAZMAZ) defterin güncel olup olmadığını ölçer.
  Bayatsa YALNIZ değişen/yeni dosyalar bellekte yeniden çıkarılır (izlenmeyen silinenlerin ve çıkarılamayan dosyaların satırları
  `--kur` gibi düşer; değişmeyen dosyaların defter satırları aynen kalır) → aday kümesi `adres --kur` sonrası kümeyle AYNIDIR ve
  hüküm aşağıdaki iki ayrışma (sınır 20-21) dışında `--kur` sonrası çıktıyla BAYT BAYT aynıdır (harness yeni dosya / tekil→çoklu / yeni tam ad /
  silinen / taşınan / izlenmez / `yol:N` / bozulan dosya vektörlerinde bayat çıktıyı `--kur` sonrasıyla karşılaştırır): yeni dosyada eklenen 4. tanım `GOVDE DEGISTI 1 [4 tanim]`, tekil adın yeni dosyadaki ikinci tanımı
  `[2 tanim] TANIM SAYISI DEGISTI`, aynı dosyada başka sınıfa eklenen aynı adlı üye, silinen/izlenmez olan dosya de görünür; taşınan
  dosya `ayni`dir; `yol:N` soneki yeni bir aynı adlı dosyayla iki dosyaya çözülürse `OLCULEMEDI [DOSYA_COK]`. Bayat defterde
  `0 degisti, 0 olculemedi` yalnız hüküm GERÇEKTEN `ayni` ise çıkar (aşağıdaki `izlenmeyen dosya` ve sınır 20 dışında: onlar
  `adres` evreninin / defterin kendi sınırlarıdır). **Taze küme çıkarılamazsa** — bayat dosya sayısı 100'ü ya da toplam boyutu
  8 MiB'ı aşarsa (`OLCULEMEDI [DEFTER_BAYAT]`), bayatlık ÖLÇÜLEMEZSE (`git ls-files` arızası, `SystemExit` dahil: `[DEFTER_BAYATLIK]`),
  defter `kaynak=git` iken `kapi` `.git`siz bir kopyada koşuyorsa (evren farklı: `[DEFTER_BAYATLIK]`) ya da yeni/değişen dosyanın
  çıkarıcısı KUSURLUYSA (araç arızası; `--kur` EKSİK defter yazardı: `[DEFTER_EKSIK]`) — kesin pozitifler (`GOVDE DEGISTI`) ve
  DAMGASIZ/COKLU sayımı KORUNUR, yalnız `ayni`/`SEMBOL YOK` o etikete düşer. **Çıkarılamayan yeni/değişen dosya** (sözdizimi hatası,
  ikili, 8 MB'tan büyük, link) o dosyanın tanımlarını BİLİNMEZ yapar: satırları düşer, `SEMBOL YOK` yerine `OLCULEMEDI
  [DEFTER_ATLANDI]` verilir ve adı sözcük olarak içeren çıkarılamayan dosya varken `ayni` de `OLCULEMEDI [DEFTER_ATLANDI]` olur
  (adı içermeyen dosya hükmü DEĞİŞTİRMEZ: gürültü yok; SÜREKLİ okunamayan dosya — defter zaten ATLANDI taşıyorsa — bayat koşuyu
  gürültülemez). Önbellek ve defter kapıdan yazılmaz; `git add` edilmemiş (izlenmeyen) yeni dosya `adres` evreninde yoktur.
  Çıktı tek özet + liste (ekran tavanı 20, HEPSİ sayılır; `--siki`de de UYARI):
  `H20: <a> atif | <d> GOVDE DEGISTI | <s> SEMBOL YOK | <o> OLCULEMEDI | <c> COKLU | <z> DAMGASIZ` ve her değişen için
  `H20: md.40 `ShouldResyncAsync` [3 tanim] #a3f9c1d2 -> #7be04c11 IDDIA KODDAN ESKI OLABILIR` (`[k tanim]` k = BUGÜNKÜ tanım
  sayısı, yalnız k ≥ 2'de; eski TEKİL damga + sonradan aynı adlı kardeş tanım gelirse satır `TANIM SAYISI DEGISTI (damgali govde
  duruyor)` der — hüküm yine `GOVDE DEGISTI`). (Maliyet: damgasız her AD belirteci için aday dosyalar canlı çıkarılır — farklı dosya sayısıyla doğrusal, dosya başına tek çıkarım;
  yüzlerce damgasız notu olan projede `kapi` saniyeler uzar; damgalı atıf varsa ayrıca tüm kod dosyalarının bayatlık geçişi koşar:
  sınır (18).) **DAMGASIZ** = madde içinde damga taşımayan ama damga ÜRETİLEBİLEN (1–5 tanım)
  tanımlayıcı/`yol:N` sayısıdır (gizlenemez; geriye dönük damgalama bu dilimde yoktur); **COKLU** = madde içinde damgasız ve
  damgalanamayan (6+ tanımlı ad, iki dosyaya çözülen `yol:N`, aşırı yüklü gövde) belirteç sayısıdır — eskiden hiçbir sayıya
  girmiyordu. **Sınıf = K1 hükmünün kuralı** (DEFTER indeksinden — bayatlık geçişi yalnız damgalı atıfların hükmünü etkiler, damgalı atıf
  varlığı bu sayımı DEĞİŞTİRMEZ; bayat defterde `not` taze kümeyle (P5.4) hüküm verdiğinden yeni dosyada eklenen tanım `not`ta damga/COKLU
  üretirken H20 sayımı onu defter indeksiyle DAMGASIZ görür — yalnız sayım ayrışır, hükümler sessiz değildir): damga üretilebilir → DAMGASIZ · COKLU · çözülürken araç
  kusuru / kısmi kayıp (`DEFTER_BAYAT`) → damgasız-OLCULEMEDI · çözülemedi (kod adresi değil) → SAYILMAZ. `<o> OLCULEMEDI`
  damgalı + damgasız ölçülemeyenlerin toplamıdır; damgasız ölçülemeyen VARSA ayrım görünür: `3 OLCULEMEDI (damgali 1, damgasiz 2)
  [CIKARICI:3]` (yoksa hepsi damgalıdır, çıktı eskisiyle aynı). **Değişmez (defter TAMAMKEN, madde içi çözülebilir belirteçler):**
  damgalı + COKLU + DAMGASIZ + damgasız-OLCULEMEDI toplamı çıkarıcı arızası enjeksiyonuyla AZALMAZ (damgasız belirteç artık
  sessizce düşmez); yalnız sağlamken `yok` olanlar (tanım dışı satıra bakan `yol:N`) kadar ARTABİLİR — arıza `yok` hükmünü
  veremez (`P5-SAYIM` kolu iki durumu ayrı pinler).
  `SEMBOL YOK` yalnız defter TAM kapsamlıyken (başlıkta `atlandi=0`) hükümdür; atlanan dosya varken kayıp sembol `OLCULEMEDI
  [DEFTER_ATLANDI]` sayılır. Canlıda hiç aday belirteç yoksa ya da defter yokken damgalı atıf yoksa H20 **sessizdir** (çıktı bayt bayt
  eski); madde içinde damgasız ama çözülebilen / COKLU / ölçülemeyen belirteç VARSA özet basılır (P5.2: 2–5 tanımlı adlar artık DAMGASIZ,
  6+ tanımlılar COKLU sayılır — eskiden sessizdiler). Defter yok/bozuk/eksikken damgalı atıflar `OLCULEMEDI [DEFTER_YOK|BOZUK|EKSIK:n]` diye SAYILIR (gizlenmez).
- **Doğuşta bayat (`not`).** Çözülen (1–5 tanım) her sembol için sembolün dosyasının **son N=5 commit**'indeki sürümleri
  (TEK `git cat-file --batch` çağrısı — dosya listesi komut satırına dizilmez, kök alt dizinse `rev-parse --show-prefix` önekiyle;
  geçmiş first-parent; aynı blob bir kez çıkarılır) AYNI çıkarıcıdan geçirilir; HEAD'den geriye ilk k (0 ≤ k < 5)
  için gövde komşu sürümden farklıysa `DIKKAT: <ad> govdesi k commit once degisti (<kisa-sha>) - iddiayi kodla teyit et`
  (k = değişikliği GETİREN commit'in HEAD'e uzaklığı; k=0 → `son commit'te degisti`; yalnız EN YAKIN değişim bildirilir).
  **Birleşik damgada (ad 2–5 tanım) HER tanım taranır ve TEK satır basılır:** `DIKKAT: <ad> 3 tanimdan 3'u 2 commit once degisti
  (4005380) - iddiayi kodla teyit et` (sayı = bugünkü tanımlardan pencerenin HERHANGİ bir sürümünde farklı gövdeyle bulunanlar;
  commit = EN YAKIN değişim; değişenler aynı yaşta değilse `... (<sha>) (en yakin; n tanim daha eski)`; pencerede aynı aday
  dosyada SİLİNEN tanım varsa `(+s silinen)`, yalnız silinen varsa `DIKKAT: <ad> pencerede s tanim silindi (k commit once,
  <sha>)`; TEK tanim / `yol:N`'de eski metin bayt bayt — ardışık sürümlerde ilk farklılık, silme/ekleme dahil). Çalışma
  ağacı HEAD'den farklıysa `DIKKAT: <ad> commit'lenmemis degisiklik tasiyor`; çalışma ağacı çıkarılamıyorsa bu hüküm
  VERİLMEZ (`OLCULEMEDI`). git yok / depo değil / sığ klonda geçmiş yetmiyorsa `DOGUSTA BAYAT: OLCULEMEDI (<sebep>)`.
  Git çağrıları terminal istemsiz ve zaman aşımlıdır (20 sn); bir `not`ta TÜM dosyaların sürümleri tek `cat-file --batch`
  çağrısındandır (dosya/sürüm sayısıyla çağrı sayısı büyümez; P5.2'den önce dosya başına 7+ `git show` vardı); toplam çıkarım
  bütçesi 15 sn'dir (aşılırsa kalan dosyalar `OLCULEMEDI` diye BEYAN edilir; `not` kilidi TUTARKEN çalışır) ve en çok 20 dosya
  için sorulur; tavan/bütçe yüzünden hükümsüz kalan belirteçlerin ADLARI satırda sayılır (`...; hukumsuz: ad1, ad2 +N daha`).
  N motorda SABİTTİR (`_DOGUS_N = 5`). Gerekçe vaka: Momentum md.40 — iddia `4359fa8`'de yazıldı,
  kodu değiştiren `4005380` iki commit önceydi (zaman/sıra kuralları bu vakaya YAPISAL olarak kördü; sembol parmak izi görür).

**P5 bilinen sınırlar (gizlenmez):** (1) **İddianın ANLAMI ölçülmez** — yalnız "dayandığı kod değişti" söylenir; gövde
değişmeden iddia bayat olabilir ya da gövde değişse iddia hâlâ doğru olabilir (yanlış alarm mümkündür). Sınıf/ad alanı adına
damga sınıfın TÜM gövdesinin izidir: ilgisiz bir üye değişince de `GOVDE DEGISTI` der. (2) **DAMGASIZ geriye dönük damgalanmaz**:
bu dilimden önce yazılmış notlar damgasızdır; H20 onları yalnız SAYAR. (3) **Birleşik damga tüm tanımları tek ize bağlar**
(P5.2): 2–5 tanımlı adın BİR tanımındaki değişiklik `GOVDE DEGISTI`dir ama HANGİ tanım olduğunu söylemez (H20 satırı yalnız
`[k tanim]` der; K3 yalnız kaç tanımın değiştiğini söyler) — gerçek vaka: Momentum `ShouldResyncAsync` = arayüz bildirimi +
gerçek metot + test çifti. **6+ tanımlı ad** (`Execute`, `Handle`…) damgalanmaz, doğuşta-bayat taramasına GİRMEZ (beyan edilir) ve
H20'de `COKLU` sayılır. Birleşik iz ilgisiz tanımları da kapsar: sınıf adı + kurucusu (aynı ad) ya da yalnız adı paylaşan ilgisiz
sınıfların üyeleri tek ize girer, birinin değişmesi hepsini uyarır. İki tanımın gövdelerinin YER DEĞİŞTİRMESİ (A↔B takası) küme
eşitliğidir: H20 `GOVDE DEGISTI 0` der (yol ize girmediği için taşıma ile aynı sonuç), K3 `2 tanimdan 2'si` der. `yol:N` belirteci aşırı yüklü bir gövdeye düşerse (eşit en dar
tanım) damgalanmaz. Aday kümesi tek kural: defter satırı sayısı > 5 ise (`k tanim` defter SATIR sayısıdır; defter bayatsa canlı
sayıdan farklı olabilir) ya da canlı tanım sayısı > 5 ise COKLU. **Sınıf + kurucu** (iç içe, aynı ad) birleşik kümeye girer: damga
sınıfın TÜM gövdesidir ve K3 kurucu değişiminde `2 tanimdan 2'si` der (ayrı dilim önerisi: başka bir ADAY tanımın içinde kalan
tanımı kümeden düşürmek). (4) Ad → dosya eşlemesi `ADRES.tsv`'den gelir, AMA bayat defterde (yeni dosyada eklenen ya da aynı dosyada başka sınıfa eklenen
aynı adlı üye, silinen/taşınan dosya) **H20 (P5.3) ve `not` (K1 damga + K3 doğuşta-bayat, P5.4) bellekte TAZE aday kümesini kullanır**
(tek yol: `_h20_taze`; aşağıdaki "Bayat defter" paragrafları): `not` aynı vakada `[k+1 tanim]` damgalar, ardından `kapi`
`GOVDE DEGISTI 0` der; taze küme çıkarılamazsa (100 dosya / 8 MiB tavanı, ölçüm arızası, `.git`siz kopya, çıkarıcı kusuru) `not`
damga BASMAZ: `ATIF OLCULEMEDI: <ad> (DEFTER_BAYAT)` + `ATIF NOT` (sebep) + `DOGUSTA BAYAT: OLCULEMEDI` — eksik kümeden damga ASLA
basılmaz. Aday belirteç yoksa `not` taze küme ÇIKARMAZ (çıktı ve süre eski). `git add` edilmemiş (izlenmeyen) yeni dosya `adres`
evreninde (`git ls-files`) yoktur: ne H20 ne `not` görür, `adres` de. (5) `yol:N` damgası "o satırın o günkü sahibi"dir; kod kayıp N. satır başka bir tanıma düşerse
`GOVDE DEGISTI` ya da `SEMBOL YOK` görünebilir (H18 `KAYMA`yı ayrıca söyler). (6) **N=5** sabittir; pencerenin dışındaki değişiklik
uyarılmaz (6. commit ve öncesi sessiz). Gövdesi aynı kalan dosya taşıma/yeniden adlandırma "yeni dosya" gibi `degisti` görünür
(birleşik damgada da: `3 tanimdan 1'i`; `git diff -M` eşlemesi ayrı dilim). Pencerede BAŞKA dosyadan silinen tanım K3'te
görünmez (aday kümesi defterden gelir); aynı aday dosyadaki silme görünür.
(7) Pencerede tek bir çıkarılamayan sürüm (WIP sözdizimi hatası, büyük/ikili dosya) o dosyanın doğuşta-bayat hükmünü `OLCULEMEDI`
yapar. (8) **post-commit kancası YOK** (kapsam dışı): commit'in dokunduğu sembollere atıf yapan satırları listelemek ayrı bir iştir.
(9) Eski motorun yazdığı EKSİK defterin başlığında `cikarici=` yoktur; onu `--kur` yeniler. (10) Not metni düz metindir: yorum/dize
maskesi yoktur, yalnız ``` / ~~~ çit satırları (liste işaretinden hemen sonra açılan çit ve girintili kod bloğu tanınmaz) ve çift
backtick aralıkları atlanır. (11) Tanınmayan belirteç biçimleri (Unicode tanımlayıcı, `Tür.üye`, `ad()`) sessizce atlanır —
H18'in dilbilgisidir. (12) **Dil sabitleri listesi** (`true false null None True False nil this self void undefined`; `nil` 3 harf:
zaten aday olamaz) yalnız `not`/H20'nin DAMGASIZ belirteçlerine uygulanır; H18 (`_atif_cikar`) bu listeden ETKİLENMEZ ve tanımlı
bir `None` (C# enum üyesi) artık YENİ damga almaz — eski damgası okunmaya devam eder. (13) H20'nin DAMGASIZ/COKLU/damgasız-
OLCULEMEDI sayımı yalnız numaralı madde içindekilerdir (damgalı atıf her satırda okunur); defter yok/bozuk/eksikken damgasız
belirteç SINIFLANAMAZ ve sayılmaz (damgalı atıf `[DEFTER_*]` sayılır). Çözülürken araç kusuru olan `yol:N` sağlamken `yok`
olacaksa `OLCULEMEDI` toplamı +1 artar (değişmez metnine bakın). (14) Damgasız `yol:N` silinmiş dosyaya bakıyorsa damgasız-
OLCULEMEDI `[DOSYA_YOK]` sayılır; damgalı karşılığı `SEMBOL YOK`tur. (15) **Git zaman aşımı** (tek çağrı 20 sn): Windows'ta
çağrının torunları (lazy-fetch, kimlik yardımcısı) boruları tutuyorsa `subprocess.run` zaman aşımından sonra da beklemeye devam
edebilir (ÖNCEDEN VAR: `adres`/`not` aynı yardımcıyı kullanır); `not` kilidi o sürece tutulur. (16) Çalışma ağacı ile blob arasında
`smudge`/`clean` süzgeci (LFS, `eol`) varsa `commit'lenmemis degisiklik` yanlış alarm verebilir; K3 git blob'unu süzgeçsiz okur.
(17) K1/H20 canlı çıkarımı (aday dosyalar) K3'ün 15 sn bütçesine bağlı değildir: ad başına ≤5 dosya çıkarılır.
(18b) **`not` yedek yolu (P5.4):** taze küme çıkarılamazsa H20 kesin pozitifleri korur (`yol:N`/tekil ad `son commit'te değişti`), `not` K1/K3
ise TÜM adaylar için `OLCULEMEDI` basar ve K3'ü bastırır (kesin pozitif de düşer; sessiz değil, `adres --kur` sonrası döner). Notta
damgasız aday yokken (yalnız damgalı belirteç) geçiş koşmaz ve K3 bayat defterle eski hükmü verir (P5.2 sınırı).
(18) **Bayatlık geçişinin maliyeti (P5.3):** damgalı atıf varsa `kapi` her koşuda TÜM izlenen kod dosyalarını bir kez gezer (içerik
özeti; sorgu önbelleği yalnız OKUNUR, `kapi` onu ISITMAZ). Soğukta dosya başına okuma + özet, sıcakta (aynı defter için bir
`adres <ad>` sorgusu önbelleği yazmışsa) dosya başına yalnız stat anahtarı (Windows/NTFS'te ChangeTime için dosya başına ek bir
dosya tanıtıcısı) — ölçüm (P5.3, Windows, 3-5 koşu ortancası, OS dosya önbelleği SICAK, 1 bayat dosya dahil): `kapi` Momentum'da
(457 kod dosyası, 2 damgalı atıf) 1,68 s → 2,06 s soğuk / 1,89 s sıcak; mozilla/fxa kopyasında (4937 kod dosyası, 12 damgalı atıf)
9,77 s → 12,01 s soğuk / 10,62 s sıcak. İşletim sistemi dosya önbelleği de soğuksa (ilk geçiş) yalnız `_adres_tara` geçişi fxa'da
13,6 s ölçüldü. Damgalı atıf yoksa geçiş KOŞMAZ (çıktı ve maliyet
P5.2 ile aynı). Bayat dosyaların bellekte yeniden çıkarımı 100 dosya / 8 MiB ile sınırlıdır (üstü `OLCULEMEDI [DEFTER_BAYAT]`);
SÜRE bütçesi YOKTUR (çıktı yük altında değişmesin). **`not` (P5.4) aynı geçişi KOŞAR — yalnız notta belirteç VARKEN** (adaysız `not`
geçişi koşmaz, çıktı ve süre eskiyle aynıdır) ve `not` kilidi TUTARKEN; önbelleği yazmaz. Ölçüm (P5.4, mozilla/fxa kopyası, 4937 kod
dosyası, Windows, 3 koşu ortancası, OS dosya önbelleği SICAK, defter güncel): adaysız `not` 0,34 s → 0,33 s (stat önbelleği boş)
/ 0,35 s → 0,35 s (dolu); ADAYLI `not` 0,69 s → 3,74 s (boş) / 0,76 s → 1,64 s (dolu). Çıktı dört durumda da bayt bayt aynı (defter
güncelken geçiş hüküm değiştirmez).
(19) Geçiş `adres`le AYNI dosya evrenini kullanır (`git ls-files`; git yoksa dosya sistemi). Defter `git` kaynaklıyken `kapi` `.git`siz
bir kopyada koşarsa evren farklıdır: taze küme çıkarılmaz, `OLCULEMEDI [DEFTER_BAYATLIK]` verilir (kesin pozitifler korunur;
`adres` aynı kopyada `BAYAT` der). (20) **Bayat durum `--kur`dan daha TUTUCUDUR (çıkarılamayan dosya):** başlığında `atlandi>0`
olan bir defterde (zaten ATLANDI dosya var: K1 `ATIF NOT` beyanı) `--kur` sonrası `ayni` hükmü kalıcı ATLANDI dosyadan
etkilenmez; bayat defterde ise ADI SÖZCÜK olarak içeren, bu koşuda çıkarılamayan YENİ/DEĞİŞEN dosya varken `ayni`
`OLCULEMEDI [DEFTER_ATLANDI]` olur. Defter ATLANDI taşırken YENİ okunamayan dosya ayırt EDİLEMEZ (başlık yalnız sayı taşır): o
koşuda hüküm değişmez. (21) **Bayat durum `--kur`dan daha CESURDUR (diskten silinen izlenen dosya):** `git rm` edilmemiş ama diskten
silinen izlenen dosyanın tanımları yoktur → bayat defterde damgalı atıf `SEMBOL YOK` (P5.2 `BIRLESIK-DOSYAYOK` ile pinli); `--kur` o
dosyayı ATLANDI (okunamadı) sayar ve aynı atıf `OLCULEMEDI [DEFTER_ATLANDI]` olur. Dosya yöneticisiyle git'e bildirmeden taşınan
dosya aynı sınıftır (yeni yolu izlenmez, `adres` evreninde yok).

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

- **Claude DIŞI asistanlar: `kur --asistan` / `devral --asistan` (P3, 17 Eki 2026, Onur kilidi).** Cursor/Codex/Gemini/Copilot'ta deftere
  giden TEK yol, o aracın kendi talimat dosyasıdır. `--asistan` (değersiz = dördü; `--asistan agents,cursor` = alt küme; anahtarlar
  `agents` · `gemini` · `cursor` · `copilot`; bilinmeyen anahtar exit 2 + geçerli liste, HİÇBİR yazımdan önce) şu dosyalara
  `> Canlı defter: <canlı> — …` işaretçisi + 4 satır açılış protokolünü yazar: `AGENTS.md` · `GEMINI.md` · `.cursor/rules/hafiza-kur.mdc`
  (frontmatter `description` + `alwaysApply: true`) · `.github/copilot-instructions.md`. **OPT-IN:** bayraksız TEK BAYT yazılmaz;
  `devral --kesif --asistan` yazacağı dosyaları ve hallerini basar, yazmaz. Dosya varsa **SONA** `<!-- hafiza-kur:asistan -->` …
  `<!-- /hafiza-kur:asistan -->` bloğu eklenir (mevcut baytlar önek olarak AYNEN kalır; LF/CRLF ve BOM korunur; son satırda newline yoksa
  önce yalnız o eklenir); yoksa yaratılır; tekrar koşum ikinci blok yazmaz (`ZATEN VAR`). YazılMAYANLAR ve her biri BEYAN edilir:
  yarım blok (`YARIM BLOK`), sembolik bağ/junction (`SEMBOLIK BAG`) ve git'in sembolik bağı — `core.symlinks=false` checkout'unda düz dosya görünür, index modu `120000`
  ölçülür (`SEMBOLIK BAG (git)`; git ölçemezse yazar ve `bag modu OLCULEMEDI` der) — bağ için H19 `kur` ÖNERMEZ: `sembolik bag -> hedef <h>;
  isaretciyi hedefe elle ekle` der, UTF-16 dosya (`KODLAMA`), isaretimizi taşımayan `hafiza-kur.mdc`
  (`CAKISMA`), kural evi olan dosya (`KURAL EVI`: işaretçi yolu geçerli). `.gitignore` yutuyorsa yazar ama `IZLENMEZ`, ölçemezse
  `OLCULEMEDI` der. Kayıt `.hafizarc` `asistan` listesi (yoksa `[]`). Başka aracın bölümüne (Graphify `## graphify`, `graphify.mdc`)
  DOKUNULMAZ. **H19:** listedeki her asistan dosyası için AYRI `H19: asistan dosyasi (<yol>) …` UYARISI (yok · işaret yok · işaret var
  ama canlı adı yok); çıkış kodu DEĞİŞMEZ; listede olmayan dosya için ses yok. **Sınırlar (gizlenmez):** Cursor `AGENTS.md`'yi de
  okur ⇒ `AGENTS.md` + `.mdc` birlikte yazılırsa işaretçi ÇİFT yüklenir (bilinçli) · `.cursor/rules/*.mdc` biçimi araç tarafından
  "legacy" sayılıyor, `RULE.md` klasör biçimi raporlarda çalışmıyor — biçim değişirse bayatlar · Gemini CLI varsayılan `GEMINI.md`'yi
  okur, `context.fileName` değişmişse okumaz (motor `~/.gemini`'yi OKUMAZ) · motor asistanın dosyayı GERÇEKTEN okuduğunu ÖLÇMEZ (E4
  işi) · kurulu projeye sonradan eklemek = `kur --asistan` (`devral` kurulu projede zaten reddeder) · H14: motorun YARATTIĞI ve dokunulmamış asistan dosyası proje değişikliği sayılmaz; **mevcut
  dosyaya ekleme H14 tarihini tazeler** (kullanıcı metni taşıyan dosya proje dosyasıdır) · yazılabilirlik yazımdan ÖNCE ölçülür (salt-okunur
  hedef → hiçbir şey yazılmadan exit 2 + yol); Windows'ta yalnız dosyanın salt-okunur bayrağı görülür, dizin izni ve root ÖLÇÜLEMEZ.
  Ölçüm: `faz0/asistan_mutanti.py` (16 kol, 13 sabotaj; gerçek-bağ kolu Windows'ta yetki yoksa OLCULEMEDI).

- **Satır sonu mührü (`.gitattributes` bloğu + H21, 19 Eki 2026, Onur kilidi).** Ölçüm (Windows 11, `core.autocrlf=true`): mühürlü
  defterler BAYT-TAM hash'lenir, git checkout LF'i CRLF'e çevirir ⇒ AYNI depo ikinci kez klonlanınca `kapi` exit 1 (`[H0] CIPA BOZULDU`
  + `defter MUHURSUZ degismis` ×N) — hiçbir tahrif yokken. **`kur` ve `devral`** kökteki `.gitattributes`'a işaretli blok yazar
  (`# hafiza-kur BASLA` … `# hafiza-kur BITIR`): `<arşiv dizini>/** -text` + her politika dosyası (`.hafizarc` · `KONULAR.md` ·
  `SAKLAMA_PLANI.md`) için `<ad> -text`. Kurallar SABİT liste değil, mühürlü kümeden TÜRETİLİR (`zincir_halka`nın `yuk` anahtarları;
  arşiv dizini `.hafizarc hafiza_dizini`ne göre değişir); `--asistan` dosyaları mühürlü değildir ⇒ listeye GİRMEZ. Dosya yoksa yaratılır;
  varsa yalnız SONA eklenir (mevcut baytlar önek olarak AYNEN kalır; LF/CRLF korunur); blok varsa yazılmaz (`ZATEN VAR`);
  idempotent `kur` mevcut projeyi de onarır. YazılMAYANLAR ve her biri BEYAN edilir (elle eklenecek satırlar basılır): yarım/ters sıralı blok
  (`YARIM BLOK`), okunamayan dosya (`OKUNAMADI`), sembolik bağ (`SEMBOLIK BAG`) ve git bağı (`SEMBOLIK BAG (git)`, index `120000`), UTF-16 (`KODLAMA`), dizin (`DOSYA DEGIL`),
  salt-okunur (`SALT-OKUNUR`); yazım hatası FATAL değil (`YAZILAMADI`); UTF-8 BOM'lu dosyada tam blok `ZATEN VAR` sayılır. `kur`/`devral` yazınca
  `.gitattributes`'i COMMIT'lemeni söyler (klon yalnız commit'li dosyayı taşır). `devral --kesif` yazacağı halini basar, yazmaz. **H21 (`kapi`):**
  mühürlü kümeden diskte VAR olan (izlenen ya da izlenmeyen) bir yol için `git check-attr text` `unset` DEĞİLSE
  `H21: satir sonu cevrimi muhurlu dosyayi bozabilir …` **UYARISI** (yalnız N kanalı; çıkış kodu DEĞİŞMEZ — Onur kilidi; mevcut
  Linux/macOS projelerini kırmızıya boğmamak için; satır izlenen/izlenmeyen sayısını AYRI verir). H21 hiçbir dalda SESSİZ DEĞİLDİR
  (20 Eki 2026, H21 SESSİZLİK): depo DEĞİLSE `H21: OLCULEMEDI (git deposu degil)`, git çalışmıyorsa `H21: OLCULEMEDI (git calistirilamiyor, .git var|yok)`,
  projeniz bir deponun ALT dizinindeyse `check-attr` alt dizinde GERÇEKTEN ölçülür (göreli yollarla; üst deponun `.gitattributes`'i de sayılır;
  uyarı `(alt dizin: ust depo …)` taşır; korumalıysa kökle aynı şekilde SESSİZDİR (23 Eki 2026, Onur kilidi: eski tek bilgi satırı gürültüydü; yalnız `klona girecek muhurlu yol YOK` bilgisi kalır); `.gitignore`'daki yollar klona girmez ⇒ sayılmaz ve yanlış alarm vermez; üst deponun COMMIT'SİZ `.gitattributes`'i de AYRI `commit'lenmemis` uyarısı üretir). Koruma çalışma ağacında görünür ama `.gitattributes` izlenmiyor/HEAD'den farklıysa AYRI `H21: .gitattributes commit'lenmemis …`
  UYARISI (ölçüldü: komitsiz blok kaynakta YEŞİL, klonda KIRMIZI). **Sınırlar (gizlenmez):** kullanıcı bloğu elle silerse `kapi` H21 ile uyarır
  ama `kapi` geri yazmaz (`kur` yeniden koşulunca blok yeniden eklenir) · H21 çalışma ağacının `check-attr` sonucuna bakar: yerel kaynaklar
  (`.git/info/attributes`, `core.attributesFile`) klona TAŞINMAZ ama koruma 'var' sayılır (ÖLÇÜLMEDİ) · `core.autocrlf=input`
  ve Git LFS ÖLÇÜLMEDİ · blok SONRASINA eklenen genel bir kural (`* text eol=crlf`) mühür kurallarını geçersiz kılar — H21 bunu
  `check-attr` ile görür (ölçüldü) · blok bir kez yazılır, sonradan GÜNCELLENMEZ (`ZATEN VAR`): ad alanı sonradan değişirse eski blok kalır,
  H21 eksik yollar için uyarır (ölçüldü) ve çözüm bloğu silip `kur`u yeniden koşmaktır · deseni güvenle yazılamayan yol (boşluk/özel karakter) `ATLANDI` diye beyan edilir. Ölçüm:
  `faz0/ikinci_klon_kapisi.py` (GERÇEK ikinci klon, `core.autocrlf=true`: tabanda KIRMIZI, düzeltmede YEŞİL; CI windows-latest) ·
  `faz0/gitattributes_muhur_mutanti.py` (12 hal, 10 sabotaj) · `faz0/gitattributes_uyari_mutanti.py` (5 hal, 4 sabotaj) ·
  `faz0/h21_sessizlik_mutanti.py` (19 hal [+1 sembolik bağ, POSIX/yetkili Windows], 20 sabotaj: M-S1 · M-S2 · M-S3 · M-S3b · M-S4 (TERSİNE ÇEVRİLDİ 23 Eki: korumalı alt dizinde bilgi satırı geri gelirse ısırır) · M-IGNORE · M-UST-KOMITSUZ · M-UST-SINIR · M-UST-ARA · M-UST-REAL · M-SAYI · M-UST-YOL · M-OLC-HATA · M-BIN-UST · M-OKU-H21 · M-OKU-H9 · M-OKU-SINIF · M-H9alt · M-H9depo · M-H9bin; her biri YALNIZ kendi dalını bozar).

- **H21 hiçbir dalda sessiz değil + H9 üç ayrı cümle (20 Eki 2026, Onur: "h21 düzeltmesini yapalım").** Ölçüm (Cowork, Windows 11, motor 3085c1a):
  (S1) proje bir deponun ALT dizininde ⇒ `kur` `alt\.gitattributes` yazdı ama `kapi` H21 satırı YOK ve **H9 "git YOK"** diyordu (git VAR, depo VAR —
  YANLIŞ TEŞHİS, P-1 sınıfı); (S2) depo değil ⇒ H21 sessiz; (S3) depo, hiç commit yok, koruma yok ⇒ H21 sessiz (izlenme süzgeci koruma yokluğunu
  ilk commit'e kadar gizliyordu). Düzeltme: H21 her dalda satır basar (yukarıdaki), **H9 `git kökte değil` dalı ÜÇ AYRI cümle**: git programı yok
  (`H9: git YOK (git programi PATH'te bulunamadi)`) · depo yok (`H9: bu dizin bir git deposu degil (ust dizinlerde de yok)`) · kök değil
  (`H9: git deposunun KOKU degil (ust depo: <top>)`); git yanıtsızsa `H9: git deposu OKUNAMADI: …`. Hüküm sınıfı (O) ve çıkış kodu DEĞİŞMEZ; yalnız METİN.
  **Seçim (alt dizin):** ÖLÇMEK `OLCULEMEDI` demekten ucuz çıktı — motor zaten kök'e göreli yollarla sorar ve git üst deponun özniteliklerini hesaba
  katar; ikinci klon ÜST deponun klonudur ve `alt/.gitattributes` orada geçerlidir. **Sınırlar (gizlenmez):** korumalı KÖK depoda H21 pozitif satır
  BASMAZ (sessizlik = ölçüldü ve koruma var); korumalı ALT dizinde de SESSİZ (23 Eki 2026 Onur kilidi; koruma kaynağı `.git/info/attributes`/`core.attributesFile` ise artık uyarı da YOK — kökteki mevcut sınırın aynısı) · git yanıtsız dalı (`H21: OLCULEMEDI (git deposu OKUNAMADI …)` / `H9: git deposu OKUNAMADI: …`) bozuk/hayalet üst `.git` ile TETİKLENİR ve sabotajlanır (M-OKU-*); gerçek `dubious ownership` bu makinede kurulamadı (aynı dal) · ustte `.git` VARKEN git `not a git repository` derse (bozuk HEAD, hayalet gitdir) `depo yok` DENMEZ, OKUNAMADI denir (bağımsız doğrulama bulgusu) · `.git/info/attributes` ve `core.attributesFile` korumayı 'var' gösterir ama klona taşınmaz (ÖLÇÜLMEDİ, taban da aynı) · kapı başına +2..6 git sorgusu (alt dizinde ≈ +0,3 sn; ÖLÇÜLDÜ) · TEMP'in ATALARINDA `.git` girdisi (dizin/gitfile, bozuk olsa da) varsa altın küme ve `h21_sessizlik_mutanti` OLCULEMEDI (exit 2) der (sahte FARK değil) · ata dizin yürümesi GERÇEK yoldan başlar (sembolik bağ ile verilen `--kok`; `h21_sessizlik_mutanti` bunu yalnız bağ kurulabilen platformda sınar) · ilgisiz bir üst `.gitattributes` commit'sizse (korumayı sağlayan o değilse) uyarı YİNE verilir (gürültü) · kökte `.git/info/attributes`/`core.attributesFile`/kök altındaki alt dizin `.gitattributes`i klonda görünmeyebilir ama H21 sessizdir (taban da aynı; ÖLÇÜLDÜ) ·
  H21 uyarı metni sayıları değişti (`izlenen N, izlenmeyen M`) · altın küme yeniden üretildi (14 kayıtta YALNIZ H9 cümlesi + H21 satırı; exit farkı 0).

- **Karar adres defteri (P4, 12 Eki 2026, Onur kilidi: yaklaşım KARAR ADRES DEFTERİ).** Ölçüm (Momentum `d4b5417`,
  kör okuma): karar sorularının cevabı projede YAZILIYDI, eksik olan ADRESTİ. `karar-kaynagi` bloğu (İKİNCİ blok YOK; P1 sınıf
  hükmü ve `KARAR SINIFI` satırı AYNEN) genişler: **(1) Kaynak keşfi** = karar dizini + kökte `IS-EMRI-*` · `GOREV-*` · `RFC-*` ·
  `DECISION*` · `ADR-*` (yalnız `.md`, harf duyarsız, alt dizin YOK; desen listesi SABİT) + `docs/decisions/*.md`; tavan 200 dosya
  (sıralı ilk 200 + `KARAR KAYNAGI: n dosya, 200 tarandi`); `.hafizarc`ta karar dizini YOKKEN de kök desenleri taranır; dosyalara
  DOKUNULMAZ. **(2) Kayıt:** kaynak başına `- K-<ad> · <ilk # başlık, 80 kr> · <ADR|IS-EMRI|GOREV|RFC|DECISION> · durum <P1 sınıfı |
  BEYANSIZ>` ve yalnız BULUNAN alanlar: `gerekce|bedel|alternatif <yol>:<N> (<başlık>)` (başlıkta `Gerekçe|Neden|Rationale|Why` ·
  `Bedel|Ödünleşim|Trade-off|Sonuçlar|Consequences|Kabul edilen` · `Alternatif|Reddedilen|Alternatives|Rejected`; Türkçe diyakritikten
  BAĞIMSIZ) ve satır içi `<alan> <yol>:<N> "<birebir alıntı, ≤160 kr>"` (satır başında ya da vurgu içinde anahtar + `:`; kırpılırsa
  `…` + `[kirpildi: n kr]`). Alansız kayıt `GEREKCESIZ <yol>` (SAYILIR). Blok sonu: `KARAR DEFTERI: <a> ADR + <b> IS-EMRI/diger
  tarandi · <k> karar · <g> GEREKCESIZ`. Motor YORUM YAPMAZ: adres + diskteki metin (yalnız backtick, `](`, `kararlar/NNNN-` kalıpları
  H4/H11 yüzünden etkisizleştirilir; ardışık boşluk tek). **Tavanlar:** TÜM blok gövdesi ≤ 8192 bayt (P1 gövdesi AYNEN kalır, kalan
  bütçe kayıtlara); kayıt SIRASI P4.1'de değişti (aşağıda); sığmayan
  `… +n kayit (listelenmedi; hepsi sayildi)`; aynı satır iki alanda tekrar alıntılanmaz; kod çitlerinin içi (CommonMark: `kod_disi`) taranmaz; dosyanın ilk 1 MiB'ı; eşleşme satırın
  40. karakterinden sonraysa alıntı eşleşen anahtardan başlar (`"…*Gerekçe: ...*"`); BOM atılır. **H7:** kalıcı-kural işareti (`ASLA`,
  `PAZARLIKSIZ`, ...) taşıyan satırın METNİ yazılmaz (motor blok maskesi onu sessizce düşürür ve kaydı "boş" gösterirdi), ADRESİ
  `(maskelendi: H7 isareti)` ile durur; okunamayan dosya `OLCULEMEDI <yol> (okunamadi)` (özette `· n OLCULEMEDI`). Karar dizini YOK ve
  kök kaynakları da KALMADIYSA (silindi/arşivlendi) `derle` bloğu KALDIRIR (bayat adres kalmaz).
  **Sınırlar (gizlenmez):** anlam ÖLÇÜLMEZ — başlıkta `Neden` geçiyorsa `gerekce` der (gerçekten gerekçe olup olmadığı okuyucunun
  işidir; ölçülmüş gürültü: "Neden bugüne kadar görünmedi:" satırı da alıntılanır) · commit mesajları KAPSAM DIŞI (Momentum'da `karar:` /
  `decision:` satırı 0 ölçüldü) · `IS_EMRI_*` (alt çizgi), `.txt`, `notlar/IS-EMRI-y.md` (kök dışı) kaynak DEĞİLDİR · 8 KB'a sığmayan kayıt
  listelenmez ama SAYILIR (Momentum `d4b5417`, P4.1: 29 karar, 20'si listelenir, 9'u `+9 kayit`; altın 4/4 adreslenir) · ham `[durum: …]` beyanı yalnız P1 gruplarındadır (kayıt satırı sınıfı taşır).
  **Kapı:** `faz0/karar_adres_kapisi.py` (CI) — dört ALTIN karardan (kör okumanın sorduğu) DÖRDÜ blokta adreslenmiş olmalı (P4.1: eşik 4;
  "gösterir" = aynı dosyaya işaret eden adres altın aralığın İÇİNDE; R3 için ayrıca alıntıda `COEP` — yalnız `## 3. GEREKÇE` başlığı
  YETMEZ); Momentum CI'da olmadığından ölçüt FIXTURE'a taşındı (dosya adı + satır konumu + biçim), `--momentum <dizin>` ham sonucu
  basar; kapı KENDİ ısırığını da sınar (satır kayması · `IS-EMRI-*` deseni düşmesi · sınıf 3 kapalı · eski sıra → hepsi KIRMIZI).

- **P4.1 (13 Eki 2026, Onur kilidi "iki bulguyu da hallet") — içeriksiz adres yanlış tahmine itmesin, 8 KB bütçe doğru kararları
  taşısın.** Ölçüm (kör okuma, `besli-paket\OLCUM_RAPORU_13EKIM_P4_BAGIMSIZ.md`): ADR 0004'ün gerçek gerekçesi L66'daydı
  (`🔴 **…gerekçesi COEP BLOKLAMASI DEĞİLDİR.**`), etiketli `Gerekçe:` olmadığı için alıntılanmadı; blokta yalnız `## 3. GEREKÇE`
  başlığı kaldı ve okuyucu gerçeğin TERSİNİ tahmin etti. **(1) Satır içi `gerekce` alıntı önceliği** (dosya başına ≤ 3, sırayla
  doldurulur): sınıf 1 etiketli `Gerekçe:`/`Neden:`/`Rationale:` · sınıf 2 satır BAŞINDA `Gerekçesi`/`Gerekçe`/`Neden` sözcüğü ·
  sınıf 3 `🔴` ya da `**` vurgusu + aynı sözcüklerden biri (sözcük sınırı: `_` sözcüğün parçası); aynı sınıfta `🔴` önce (ORİJİNAL
  satırdan), sonra satır sırası. Tablo (`|`) ve başlık satırları hiçbir sınıfa girmez; BAŞKA alanın (bedel/alternatif) etiketini taşıyan
  satır `gerekce` sınıf 2/3'e girmez. Yalnız BAŞLIK adresi kalan kayıtta (alıntı yok) başlık satırının sonuna
  `(yalniz baslik: icerik icin dosyayi ac)` yazılır: boşluk tahminle doldurulmaz. **(2) Sıralama** (deterministik): grup — alıntılı →
  yalnız başlık (H7 maskeli-yalnız dahil) → `GEREKCESIZ` → `OLCULEMEDI`; her grupta durum `GECERLI` → `BEYANSIZ` → `TASLAK` →
  `GECERSIZ`/`SINIFLANAMADI`; sonra dosya yolu. Bütçe aynı (TÜM gövde ≤ 8192 B); kesilenlerin durum dağılımı
  `listelenmedi: BEYANSIZ 9 · TASLAK 1` satırıyla beyan edilir. P1 gövdesi bütçeyi doldurmuşsa kayıt bölümü LİSTELENMEZ, özet satırı
  `… · kayitlar listelenmedi (butce)` der. **Kayıt tavanı:** tek kayıt ≤ 280 bayt — başlık + ilk alan satırı HER ZAMAN; `GECERLI`
  kayıtta her alanın İLK alıntısı da (bedel/alternatif dahil) kesilmez; alıntı satırları (alan sırasıyla) başlık adreslerinden ÖNCE
  gelir; kesilen satır sayısı (özet satırlarındaki sayılar dahil) başlık sonuna `(+n satir daha: kayit tavani; sayildi)` yazılır,
  H7 maskeli satır varsa `; H7 maskeli m`. **Ölçülmüş marj (Momentum `d4b5417`):** 29 karar, 20'si listelenir (alıntılı/yalnız-başlık
  hepsi), 9'u `+9 kayit` (GEREKCESIZ); blok 8095 bayt, tavana ~100 B — yeni bir alıntılı kayıt eklenince ilk düşen TASLAK ADR'dir (kapı
  bunu 4/4 ile ölçer, fixture aynı baskıyı taşır). **Sınırlar:** sınıf 3 gürültülüdür (başlık dışı her `🔴`/`**` + `gerekçe` satırı;
  `🔴` önceliği L66'yı öne alır) · alıntı ilk 160 karakterle sınırlıdır (L66'da "COEP BLOKLAMASI DEĞİLDİR" görünür, devamı dosyadadır) ·
  TASLAK kayıtta yalnız ilk satır garantidir (taslak karar DEĞİLDİR; ayrıntı dosyada).

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

- **H14 devralma anına KAYITLI muafiyet (19 Eki 2026, Onur kilidi).** Ölçüm (Momentum `d4b5417` + `devral`): hafıza damgası = bugün, uyuyan
  projenin son değişikliği 40 gün eski ⇒ ilk `kapi` HER ZAMAN `[H14] … ILERIDE` FAIL (sebepsiz kırmızı). Düz süre muafiyeti REDDEDİLDİ (o
  pencerede UYDURMA damgayı gizler). `devral` devralma olayını **mühürlü** kayda yazar: `DEVIR` zincir halkasının `ek`i (`devralma_tarihi` ISO
  gün + `proje_son_t` = devral anında `_h14_en_yeni` ile ÖLÇÜLEN proje son değişikliği, epoch); halka hash'i `ek`i kapsar, elle değişiklik
  halkayı KIRIK yapar ve kayıt SAYILMAZ. H14 `ILERIDE` kolu ÜÇ koşul BİRLİKTE tutarsa FAIL yerine **UYARI** basar (`[H14] UYARI devralma ani:
  proje <N> gundur uyuyor (devral <tarih>); proje degisince ya da damga ilerleyince normal hukum doner`; N hafıza damgasına göre gün; satır
  her `kapi`'de, yalnız N kanalı ⇒ exit DEĞİŞMEZ): (a) mühürlü kayıt var · (b) `t_son <= devralma_tarihi` · (c) şimdiki `en_yeni_t == proje_son_t`.
  Biri tutmazsa bugünkü FAIL birebir; GERİDE ve `es` kollarına dokunulmaz. **Sınırlar (gizlenmez):** `kur` ile kurulan uyuyan proje ve eski
  motorla `devral`'lanmış proje muafiyet ALMAZ · muafiyetin ömrü FİİLEN `devral` günüdür: o günden SONRAKİ bir günde koşan `derle` (exit 2 de
  olsa) damgayı ilerletir ⇒ muafiyet biter ve proje hâlâ uyuyorsa sebepsiz `ILERIDE` FAIL geri gelir (ÖLÇÜLDÜ; bugünkü FAIL BİREBİR korunur, satırında
  çıkış yolu ipucu YOK; çıkış: proje dosyasına dokunmak ya da `hafiza_gecikme_gun: 0`; kalıcı "uyuyor" beyanı TASARIM KARARIDIR, Onur kilidi ister);
  aynı gün `not`/`derle` etkisizdir · proje dosyası değişince de biter (bugün tarihli değişiklik H14'te `es` verir; FAIL ancak değişikliğin tarihi
  damganın `gecikme` günden gerisinde kalırsa döner) · UYARI'daki N hafıza damgasına göre gündür (geç günde bugünkü gün sayısından eksik görünür) ·
  zincir ANAHTARSIZDIR: hash'i yeniden hesaplanmış sahte halka ayırt EDİLEMEZ (bilinen sınır) · (c) git commit tarihi / mtime ölçümüne bağlıdır:
  projeyi kopyalayıp mtime'ları değiştirmek izlenmeyen/kirli dosyalarda muafiyeti düşürür (normal H14 hükmü — es/GERİDE/İLERİDE — döner; ÖLÇÜLDÜ:
  mtime'ı bugüne çekilen yeni dosya `es` verir, FAIL ancak tarih damgadan `gecikme` günden fazla geride kalırsa) · `devral`'dan sonra
  `KONULAR.md`/`SAKLAMA_PLANI.md`/`.hafizarc` MÜHÜRSÜZ düzenlenirse zincir doğrulanamaz ⇒ kayıt SAYILMAZ (ÖLÇÜLDÜ: `[H0] MÜHÜRSÜZ` + `[H14] ILERIDE`
  FAIL geri gelir; `muhur "gerekçe"` sonrası UYARI döner — `devral` triyajı bunu söyler). Ölçüm: `faz0/h14_devralma_mutanti.py` (6 hal, 5 sabotaj M-DV1…M-DV5; tabanda KIRMIZI, düzeltmede YEŞİL).

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
  gerekçesiyle yazılı). Motorda platforma özgü dallar üç
  yüzeydedir (`_surec_yasiyor`, `_boru_koptu_mu`, `adres` önbellek anahtarı `_adres_onb_anahtar`) ve
  `faz0/win_dal_mutanti.py` onları ölçer: envanter ve davranış kapıları temiz,
  **5/5 mutant ayrı eksende ısırıyor**. Ama o
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

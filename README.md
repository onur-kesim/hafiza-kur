# hafiza-kur

Taşınabilir bir **proje hafızası kapı sistemi**. Tek dosyalık saf Python motoru
(stdlib, sıfır bağımlılık) bir projenin hafıza dosyalarını yönetir ve **ölçer**.

> **Durum:** geliştirme aşamasında, **henüz kurulmadı ve yayımlanmadı.** Bu depo
> CI ölçümü ücretsiz koşabilsin diye publictir — bir yayın değildir. PyPI paketi,
> marketplace girişi ya da duyuru **yoktur**.

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

**Çıkış kodları** — `kapi`: `0` yeşil · `1` kırmızı · `2` kullanım hatası ·
`3` ölçüm yapılamadı, hüküm yok. `isir`: `0` hepsi ısırdı · `1` **kapı kör** ·
`2` ölçülemeyen mutant · `4` temiz sürüm zaten FAIL.

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
python3 hafiza.py isir --kok=deneme    # taze projede: 34/34 + 2 SINANMADI, exit 2
python3 hafiza.py not --kok=deneme --konu=genel-durum --metin="ilk not"
python3 hafiza.py derle --kok=deneme
python3 hafiza.py isir --kok=deneme    # derle sonrası: 36/36, exit 0
python3 t_y3.py                        # 20 senaryo, temiz hata
python3 t_y42.py                       # 58 senaryo
```

Mutant sayısını **bağlamsız okuma**: `36/36` yalnız `derle` koşulmuş projede
doğrudur. Taze bir projede `M-H1b` ve `M-DEVIR` ön-koşulsuz kalır — bu sağlıklı
bir projedir ve çıkış kodu `2`'dir.

Ortam sınıfını ölçmek için (root gerekir):

```bash
sudo bash faz0/ortam_olcum.sh          # root olmayan kullanıcı · dolu disk · salt-okunur
python3 faz0/sabotaj.py                # her fail() tek tek kapatılır -> kapsam envanteri
```

## Bilinen sınırlar

Bunlar gizlenmiyor; `skill/SKILL.md` §9'da tam listesi var. En önemlileri:

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

- **Platform hükmü eşit değildir.** CI, ölçüm bataryasının tamamını Linux ·
  Windows · macOS üzerinde `continue-on-error`suz koşar. Ama motorda platforma özgü
  tek dal `sys.platform == "win32"` altındadır ve **o dal henüz bir mutantla
  ölçülmemiştir** — doktrin gereği hükmü yoktur. macOS'a özgü kod yolu ise hiç
  yoktur; macOS'un bilinen mayını (dosya adlarında NFC/NFD ayrışması) bir kapıyla
  değil bir **kaçınma kuralıyla** yönetiliyor: disk adlarına Türkçe diyakritik
  konmuyor. Kural, kapı değil — ve kuralı zorlayan bir şey yok.
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

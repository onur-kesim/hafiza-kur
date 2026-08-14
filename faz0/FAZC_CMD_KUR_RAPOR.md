# FAZ C — `cmd_kur` BÖLMESİ (14 Ağustos 2026)

`cmd_*` sınıfının **ilk** bölmesi. Kapı bölmelerinden (`h1/h4/h10/h11/h12/h14`)
iskeleti aynı, **gözlem yüzeyi farklı** — ve fark her şeyi belirledi.

| | önce | sonra |
|---|---|---|
| `cmd_kur` | CC **27** · 91 satır | CC **1** · 8 satır |
| motor | `9b72160a…` · 5132 satır | `dffe3ce6…` · 5185 satır |
| ihlal (CC>20 ∪ satır>80) | 9 | **8** |
| fonksiyon | 200 | 207 |

`cmd_kur` artık CC>20 listesinde **yok**. Kalanların hepsi `cmd_*`:
`cmd_devral` 88 · `cmd_derle` 63 · `zincir_dogrula` 40 · `cmd_bloklastir` 39 ·
`cmd_emekli` 24.

## Yedi parça

```
_kur_on_kontrol   kok cozumu + v1 izi taramasi          OLUM
_kur_rc           ad · .hafizarc · rc · Y               DISK, OLUM~
_kur_kilit        yol on kontrol · kilit · zincir sarti DISK, OLUM~
_kur_dizinler     dizin iskeleti                        DISK
_kur_dosyalar     dosya iskeleti (en buyuk bolge)       DISK, OLUM~
_kur_halka        arsiv dizini tazele + zincir halkasi  DISK
_kur_rapor        dort satirlik rapor                   CIKTI
```

## ETKİ KAPISI — kanal kapısının `cmd_*` karşılığı

Kapı fonksiyonları hükmü `F/N/O` listelerine yazar; kanal kapısı *"kullandığın
listeyi imzada taşı"* der. `cmd_kur`da öyle bir liste **yoktur**. Etkisi üç yerde
görünür ve üçü de **imzadan sezilmez**:

| eksen | ne | nasıl ölçüldü |
|---|---|---|
| **DISK** | diske yazıyor mu | `yaz · makedirs · copyfile · zincir_halka · kilit_al · _beyan_yeni_satirlar · _arsiv_dizini_tazele` çağrısı |
| **CIKTI** | stdout'a basıyor mu | `print` |
| **OLUM** | süreci öldürebiliyor mu | `oldur` — doğrudan, ya da `~` = gövdesinde `oldur` geçen bir fonksiyonu çağırıyor |

**Beyan üretilir, yazılmaz.** Üreteç üç ekseni her koşumda AST ile ölçer ve
üretilen başlığa kendisi yazar. Elle yazılsaydı bayatlardı — *"belge de bir
arayüzdür ve yalan söyleyebilir"* dersinin doğrudan uygulaması. `OLUM~`
listesi de türetilir: kaynak taranıp gövdesinde `oldur` geçen fonksiyonlar
bulunur; elle liste tutulmaz.

Kapının üç dişi:

- **DISK taşıyan parça** imzasında `y` ya da `kok` taşımak zorunda.
- **TEK RAPORCU**: `CIKTI` ekseni tam bir parçada olabilir. İkincisi çıkarsa
  üreteç kırmızı yanar — *"çıktı nereden geliyor" sorusunun iki cevabı olamaz* (H5).
- **İNCE EBEVEYN**: bölmeden sonra `cmd_kur` gövdesinde doğrudan DISK/CIKTI/OLUM
  çağrısı kalamaz. Kalırsa ebeveyn hâlâ iş yapıyordur ve bölme yalancıdır.

## AD KAPISI (yeni) — ilk koşumda ısırdı

Kapı bölmelerinde parçalar `F/N/O` ve bir iki ad alıyordu. Burada yedi parça
arasında `kok · ad · rc · y · yeni_kurulum` dolaşıyor; bir parametreyi imzaya
koymayı unutmak, üretilen kodun **ancak koşturulunca** `NameError` vermesi
demek. Üreteç her bölgenin serbest adlarını AST ile çıkarır; imza + modül
globalleri dışında tek ad kalırsa **yazmaz**.

İlk koşumda `_kur_rapor` için `__file__` üzerinden **kırmızı** verdi. Ölçüldü:
`__file__` modül düzeyinde her zaman tanımlıdır ama `ast` ile görünmez (atama
yok, import yok). Bu bir **sahte kırmızıydı**, ve sahte kırmızı gerçek
kırmızıyı değersizleştirir (Y-4). Düzeltme kapıyı gevşetmek değil, global
kümesini tamamlamak oldu: `MODUL_DUNDER`.

## Ölçüm

```
TEMIZ KOL (ayni motor 2 kez)          FARK YOK
ESDEGERLIK (bolme oncesi = sonrasi)   FARK YOK — 10 halin ucusu de AYNI
hal sayisi / ayrik imza               10 / 10

  h_taze          exit 0 · 25 girdi   ilk kurulum
  h_idempotent    exit 0 · 25 girdi   ikinci kur: tazeleme dali
  h_kok_yok       exit 2 ·  0 girdi   kok yok -> ON KONTROL oldurur
  h_v1_izi        exit 2 ·  4 girdi   v1 izi -> ON KONTROL oldurur
  h_yol_ihlali    exit 2 ·  2 girdi   gunluk yerinde dosya -> KILIT bolgesi oldurur
  h_kilit_mesgul  exit 2 · 26 girdi   baskasinin kilidi -> KILIT oldurur
  h_bozuk_zincir  exit 2 · 25 girdi   0 baytlik zincir -> KILIT bolgesi oldurur
  h_arsiv_yok     exit 2 · 15 girdi   kurulu ama arsiv silinmis
  h_rc_bozuk      exit 2 · 25 girdi   tavan_kb metin -> RC bolgesi oldurur
  h_goreli_kok    exit 0 · 25 girdi   --kok=. (goreli)

  mutant                     ESKI YUZEY  YENI YUZEY  iz
  +  M-1 CAGRI on_kontrol      ISIRDI      ISIRDI     kok_yok, v1_izi
  +  M-2 KENAR yeni_kurulum    ISIRDI      ISIRDI     bozuk_zincir, arsiv_yok
  +  M-3 KENAR rc -> dizinler  KOR         ISIRDI     taze, idempotent, kilit_mesgul, …
  +  M-4 KENAR ad -> dosyalar  KOR         ISIRDI     taze, idempotent, kilit_mesgul, …
  +  M-5 CAGRI kilit           ISIRDI      ISIRDI     yol_ihlali, kilit_mesgul, …
  +  M-6 CAGRI halka           ISIRDI      ISIRDI     taze, idempotent, kilit_mesgul, …
  +  M-7 KENAR kok -> rapor    ISIRDI      ISIRDI     taze, idempotent, goreli_kok
  +  M-8 DONUS kok             ISIRDI      ISIRDI     goreli_kok

HUKUM: 8 mutantin hepsi ISIRDI (10 hal).   sure: 14 sn
```

**İki mutant yalnızca yeni yüzeyle görünüyor** — `M-3` (arşiv dizinleri sessizce
açılmıyor) ve `M-4` (canlı hafıza ve `CLAUDE.md` sessizce başka adla yazılıyor).
Kapı kalıbı olduğu gibi kopyalansaydı bu iki kenar **kör kalırdı ve kimse
bilmezdi.** Faz 1'de harness'ın masrafını hak ettiği ölçülmüştü; burada o ölçüm
gerçek bir bölmede karşılığını verdi.

## 🔴 İki kez SAHTE KIRMIZI — ikisi de düzeneğin kusuru

**1. Eşdeğerlik kapısı "bölme davranış değiştirdi" dedi.** Sebep bölme değildi:
`cmd_kur`un son satırı `os.path.basename(__file__)` basar ve iki motor
`hafiza_ONCE.py` / `hafiza_SONRA.py` adlarıyla duruyordu → stdout zorunlu
ayrıştı. *Prob ORTAMI mı ARACI mı ölçüyor* dersinin aynısı. Çözüm
**normalizasyon değil** — o, adın gerçekten değişmesini de gizlerdi. Çözüm
karşılaştırmayı like-ile-like yapmaya **zorlamak**: betikte artık bir **dosya
adı kapısı** var, iki motorun basename'i farklıysa `ÖLÇÜLEMEDİ` der ve durur.

**2. `M-8 DONUS kok` dokuz halin tamamında KAÇTI.** Körlük ilan etmeden önce
*"eşdeğer mutant mı?"* diye soruldu — **evet**: dokuz halin dokuzu da `--kok`u
mutlak veriyordu, `os.path.abspath` bir işlem yapmıyordu. Kaçış **kapının değil
GİRDİ KÜMESİNİN** eksiğiydi. `h_goreli_kok` eklendi, mutant gerçek oldu. Yan
kazanç: göreli `--kok` bu ana kadar **hiç ölçülmemişti**.

Not: aynı `--ad` verilseydi `h_goreli_kok`, `h_taze` ile birebir aynı üçlüyü
üretirdi (abspath göreliyi mutlağa çevirdiği için) ve HAL KAPISI "haller
ayrışmıyor" derdi. O özdeşlik zaten `abspath`in çalıştığının kanıtıdır; haller
ayrışsın diye ad değiştirildi.

## Bölme sonrası tam koşum (hepsi bu motorda ölçüldü)

```
isir            34/34 kosulan mutant ISIRIYOR · 2 SINANMADI (taze projede derle yok)
t_y3            20/20 senaryo TEMIZ HATA
t_y42           58 gecti · 0 kaldi · 0 yavas · 0 olculemedi   (root olmayan kullanici)
altin kume      FARK YOK — 22 olcum, kapi ciktisi ve cikis kodlari BIT-BIT ayni
karmasiklik     ihlal 9 -> 8 · cmd_kur CC>20 listesinden CIKTI
```

## ⚠️ EŞDEĞERLİK CI'DA ÖLÇÜLMEZ — ve bu bilinçli

Eşdeğerlik `--once` ile **bölme öncesi motoru** ister. Onu depoda tutmak
*"motorun ikinci kopyası olmaz"* kuralını kırardı. Eşdeğerlik bir **geçiş
kapısıdır, sürekli değil**: bir kez ölçüldü (on halin üçüsü de FARK YOK) ve
kanıtı bu belgede durur. CI işi **kenarları** ölçer. Bu bir kapsam boşluğu
değil, kapsamın sınırının **yazıya dökülmesidir**.

## SONRAKİ

Kalıp kanıtlandı. Sıradaki `cmd_emekli` (CC 24 · 87 satır) — en küçüğü.
`cmd_devral` (88) ve `cmd_derle` (63) en sona, çünkü kalıbın küçükte oturması
gerekiyor. Her biri kendi hal listesini ve kendi kenar mutantlarını ister;
**duran onay yalnız kapı bölmeleri içindi.**

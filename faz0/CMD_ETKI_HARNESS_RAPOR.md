# `cmd_*` SINIFI — FAZ 1: ETKİ İMZASI HARNESS'I (14 Ağustos 2026)

**Bu tur `cmd_kur`u BÖLMEZ.** Onaylanan sıra: **önce harness, sonra bölme.**
Gerekçe projenin kendi dersi — *bir prob ORTAMI mı ARACI mı ölçüyor.* Harness
bölmeden sonra yazılsaydı, bir mutant ısırdığında **bölmeyi mi yoksa komutu mu**
ölçtüğü belirsiz kalırdı. Önce bölünmemiş komuta karşı yazıldı ve ısırdığı
kanıtlandı.

## Neden yeni bir gözlem yüzeyi gerekti

Kapı mutantlarının yüzeyi `(exit, stdout)`tur ve salt-okunur `kapi` komutu için
doğrudur. `cmd_kur` · `cmd_derle` · `cmd_devral` · `cmd_bloklastir` · `cmd_emekli`
ise **etkilidir**: dosya yazar, taşır, kilit alır, zincire halka atar. Kopan bir
kenar **aynı stdout'u basıp diskte farklı bir ağaç bırakabilir.** Kapı kalıbını
olduğu gibi kopyalamak kör bir kapı üretmek olurdu.

```
ETKI IMZASI = (exit, stdout) + DISK AGACI MANIFESTOSU
```

Manifesto: her yol için (göreli yol, tip D/F/L, değer). Dosyalarda değer =
içeriğin sha256'sı, bağlantılarda hedef.

## 🔴 Normalizasyon ÖLÇÜLDÜ — ve ilk ölçüm YANILTTI

İki bağımsız `kur` koşumu (farklı kök) karşılaştırıldı. **Ard arda koşunca
"FARK YOK" çıktı ve araç tam determinist göründü** — ikisi de aynı saniyeye
düştüğü için. *Değişen niceliği KESMEYEN bir determinizm ölçümü hiçbir şey
ölçmez.* 2 saniye ara konunca gerçek göründü:

| adım | bulunan fark |
|---|---|
| ard arda | *(yok — yanıltıcı)* |
| 2 sn arayla | `_ZINCIR.jsonl` → `"t": "2026-08-14T07:59:45"` |
| zaman normalize edilince | aynı satırdaki `"halka"` — **`t`'yi de kapsayan hash**, türev olarak değişiyor |

Normalizasyon bu **üç alanla sınırlı**: `<ZAMAN>` · `<HALKA>` · `<ONCEKI>`.
Başka hiçbir şey değişmedi — `_CIPA.json`, `yuk` içindeki dosya SHA'ları,
tarihler, dizin yapısı, kök yolu (hiçbir dosyaya gömülü değil).

**Dosya SHA'ları NORMALİZE EDİLMEZ.** Kapı mutantları stdout'ta `<SHA>` yapar
çünkü orada SHA gürültüdür. Burada SHA **sinyaldir**: `_CIPA.json`'ın `sha` alanı
ve `_ZINCIR.jsonl`'in `yuk` alanı bu aracın tüm kanıt değeridir. Normalize
etseydik çıpa bozulması ve içerik tahrifi görünmez olurdu.
*Normalizasyon ne kadar genişse yüzey o kadar kördür.*

`halka`/`onceki` alan **adıyla** hedeflenir. "Her 64 haneli hex" gibi geniş bir
kalıp `yuk` içindeki dosya SHA'larını da yutardı — harness'ı asıl sinyaline kör
yapardı.

## 🔴 BİLİNEN KÖR NOKTA — varsayılmadı, ÖLÇÜLDÜ

`halka`/`onceki` normalize edildiği için, **yalnızca halka hash'ini bozan**
(girdilerine dokunmayan) bir kusur bu yüzeye görünmez. Bu kör nokta gizlenmedi:
`S-5 HALKA hash'i` mutantı tam olarak bunu yapar ve raporda **"IKISI DE KOR"**
satırı olarak durur. *Hedef engellemek değil, GİZLENEMEZ KILMAK.* Kapatmanın
doğru yolu zincir doğrulamasını ayrı bir kapıyla ölçmektir — bu harness'ın işi
değildir.

İkinci bilinen kör nokta: **dosya izinleri (mode) imzaya girmiyor.** Gerekçe umask
ve platform gürültüsü; Windows'ta zaten anlamsız. Kayıtlıdır; kapatılırsa önce
mutantla ölçülmelidir.

## ÖLÇÜM — harness masrafını HAK EDİYOR MU?

Her mutant için **iki yüzey birden** hesaplanır. Dört hücre mümkün ve dördü de
anlamlıdır; `ESKI ISIRDI · YENI KOR` **imkânsızdır** (yeni yüzey eskiyi kapsar) —
çıkarsa harness bozuktur ve betik bunu ayrıca ölçer.

```
  TEMIZ KOL (ayni motor 2 kez)   eski yuzey: FARK YOK · yeni yuzey: FARK YOK
  hal sayisi / ayrik imza        4 / 4
     h_taze         exit 0 · 25 girdi · ilk kurulum
     h_idempotent   exit 0 · 25 girdi · ikinci kur: tazeleme dali
     h_v1_izi       exit 2 · 4  girdi · v1 izi var -> oldur
     h_kok_yok      exit 2 · 0  girdi · kok yok -> oldur

  mutant (SESSIZ YAZIM)      ESKI YUZEY   YENI YUZEY   hukum
  +  S-1 KOVA filtresi          KOR         ISIRDI      YENI YUZEY KAZANDI
  +  S-2 arsiv dizini eksik     KOR         ISIRDI      YENI YUZEY KAZANDI
  +  S-3 DUZELTMELER bicimi     KOR         ISIRDI      YENI YUZEY KAZANDI
  +  S-4 kural dosyasi metni    KOR         ISIRDI      YENI YUZEY KAZANDI
  !  S-5 HALKA hash'i           KOR         KOR         IKISI DE KOR (bilinen kor nokta)
```

**Dört sessiz-yazım sabotajının dördü de `(exit, stdout)` yüzeyine görünmez.**
Bu artık bir iddia değil, ölçüm: kapı kalıbı etkili komutlarda yapısal olarak
kördür. Süre: **3,0 sn**.

Yakalanan farklar (harness'ın kendi çıktısından):

| mutant | görünen fark |
|---|---|
| S-1 | `arsiv/hafiza/_KOVA.json` DEGISTI · `_ZINCIR.jsonl` DEGISTI |
| S-2 | `arsiv/gorev` **VAR->YOK** |
| S-3 | `arsiv/hafiza/_DUZELTMELER.json` DEGISTI · `_ZINCIR.jsonl` DEGISTI |
| S-4 | `CLAUDE.md` DEGISTI |

`_ZINCIR.jsonl`'in de değişmesi doğrudur ve tesadüf değil: `yuk` alanı defter
SHA'larını taşır, dolayısıyla bir defter değişince zincir de değişir. Bu, `yuk`
alanını normalize etmemenin karşılığıdır.

## GÜN SINIRI KAPISI

Dosyalarda `bugun()` tarihi var. Referans ve mutant koşumları gece yarısını
geçerse imzalar **tarih yüzünden** ayrışır ve bu sahte bir fark olur. `imza()`
tarihi başta ve sonda okur; değişmişse hüküm `ÖLÇÜLEMEDİ`dir (exit 2), "temiz"
değil.

## SONRAKİ ADIM

Harness ısırdığı kanıtlandı. Şimdi `cmd_kur` bölünebilir; bölme mutantı bu
yüzeyi kullanacak. `cmd_kur`: CC 27 · 91 satır.

Açık: `ci_kapsam_kapisi.py` kapsamı DAR (`*_bolme_mutanti.py`) olduğu için
`cmd_etki_mutanti.py`'yi **kapsamıyor** — işi elle eklendi. Ölçüldü: kapsam
`faz0/*_mutanti.py`'ye genişletilirse **13 dosyanın 13'ü** zaten iş taşıyor,
yani **muafiyet gerekmez**. Karar Onur'da.

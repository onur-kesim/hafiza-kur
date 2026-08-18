# `kapsam_envanteri*.json` — HANGİSİ BUGÜNE AİT?

Bu dizinde artık **altı** kapsam envanteri var. Hepsi kanıttır, hiçbiri
üzerine yazılmaz — ama yalnızca biri bugünkü motoru ölçer.

| Dosya | Madde | Motor kimliği | O motorun `lineno`+kapı tutarlılığı | Durum |
|---|---|---|---|---|
| `kapsam_envanteri.json` | 60 | **yalnız yol** (`/home/claude/dogrulama/hafiza.py`) — SHA yok | kimliksiz | 🗄️ tarihsel |
| `sabotaj_rapor.json` | 61 | **yalnız yol** (`C:\dev\hafiza-kur\…`) — SHA yok | kimliksiz | 🗄️ tarihsel |
| `kapsam_envanteri_61283ff7.json` | 61 | `motor: 61283FF7…` | 61 / 61 (o motorda) | 🗄️ H11 bölmesiyle aşıldı |
| `kapsam_envanteri_9b72160a.json` | 61 | `motor: 9B72160A…` | 61 / 61 (o motorda) | 🗄️ **57/61 KAYMIŞ** — md.6→md.10 turları satırları kaydırdı, H16'dan ÖNCE bu tabanın kendisi bayattı (ölçüldü, ADR_H16_UYGULAMA_KISITI.md §5) |
| `kapsam_envanteri_81798e30.json` | 61 | `motor: 81798E30…` (SHA — `motor_yolu` altında ayrıca yol) | 61 / 61 | 🗄️ H16 ÖNCESİ taban (17 Ağu 2026, bu turda üretildi) |
| **`kapsam_envanteri_f77cff03.json`** | 64 | `motor: F77CFF03…` | **64 / 64** | ✅ **GÜNCEL** (17 Ağu 2026, H16 SONRASI) |

> `f77cff03` H16 YAPI kapısı eklendikten sonraki motordur (17 Ağu 2026).
> H16 ÖNCESİ/SONRASI **sabotaj diferansiyeli ÖLÇÜLDÜ: fail() 61 → 64 (N=3,
> `_kapi_h16`'nin üç `fail()` çağrısı) VE diğer 61'in `(kapı, kapı-içi-sıra)`
> bazında hükmü+sebebi BİREBİR AYNI** — bölme/ekleme kapsamı değiştirmedi,
> yalnızca satır numaralarını kaydırdı (bu turda da, her turda olduğu gibi).
> H16'nın 3 yeni `fail()`i bu turda **KAPSAMSIZ** görünüyor — bu bir kusur
> DEĞİL: `isir`in ESKİ mutant kataloğunda H16'ya özgü mutant yok (H16'yı
> ölçen `faz0/yapi_kapisi_mutanti.py`dir, 9/9 mutant ISIRDI — ayrı ölçüm).
> Eski dosyalar silinmedi: kanıt dosyası üzerine yazılmaz.

> 🔴 **KALEM E (18 Ağu 2026, H16-DÜZELTME-BRİEF.md §5.2) — bu YAPISALDIR:**
> `sabotaj.py` tek bir **temiz** şablon kurup her `fail()` satırını silerek
> `isir` koşuyor; H16 temiz projede hiç ateşlenmediği için satırı silinse
> `isir` fark etmez. **KAPSAMSIZ = `isir`ın temiz şablonu o satırı
> ateşlemiyor demektir; "hiç ölçülmüyor" demek DEĞİLDİR** — H16'yı
> `yapi_kapisi_mutanti.py` ölçer.

## 🔴 "GÜNCEL" bir tarihtir, bir ölçüm değil (üçüncü ısırık, 17 Ağu 2026)

`9b72160a` bu notta "✅ GÜNCEL" işaretliydi. Ölçüldü (H16 turu, ADR §5): o
61 kaydın `lineno` alanının bugünkü motorda **yalnızca 4'ü** gerçek bir
`fail(…)` çağrısına denk geliyordu — 57'si kaymıştı. İşaret bir kez doğruydu
ve sonra sessizce bayatladı; onu düzelten hiçbir mekanizma yoktu.

> Bir artefakta **"GÜNCEL" yazan her satırın yanında, o güncelliği O AN ölçen
> komut durur; komut yoksa işaret yazılmaz.**

Tazelik komutu (bu tablodaki `f77cff03` satırı için — motor değiştikçe SHA
da değişir, komut GÜNCELLENMEDEN kopyalanmaz):

```
python3 faz0/sabotaj.py --motor skill/scripts/hafiza.py \
    --json faz0/kapsam_envanteri_$(python3 -c "import hashlib;print(hashlib.sha256(open('skill/scripts/hafiza.py','rb').read()).hexdigest()[:8])").json
```

Çıktıdaki `fail_sayisi` bugünküyle (bu belgenin yazıldığı an: **64**) aynı
değilse, ya da yukarıdaki JSON dosya adı depoda YOKSA, bu tablo BAYATLAMIŞTIR
— "✅ GÜNCEL" satırını silin, yeni üretileni ekleyin, bu notu güncelleyin.

## Nasıl ölçüldü (14 Ağu 2026)

Beyandan değil artefakttan: her kaydın `lineno` alanı bugünkü
`skill/scripts/hafiza.py` içinde gerçekten bir `fail("<kapi>", …)` çağrısına
denk geliyor mu diye satır satır bakıldı. Eski iki dosyada **hiçbiri** tutmuyor —
Faz C bölmeleri satır numaralarını tamamen kaydırdı.

## 🔴 DÜZELTME: `sabotaj_rapor.json` TABAN DEĞİLDİR

Bir DEVİR notunda "kapsam_envanteri.json bayat — **taban: sabotaj_rapor.json**"
yazdı. Ölçüldü: `sabotaj_rapor.json` da bugünkü motora ait değil (0/61). O dosya
yalnızca **geçmişi belgelenmiş** olandır (`sabotaj_rapor_OKUMA_NOTU.md`,
`f149407` ağacı) — bu, "bugünün tabanı" ile aynı şey değil. Bağlamı olan bir
sayı, hâlâ **başka bir motorun** sayısıdır.

Ders sınıfı zaten defterde vardı: *sayı bağlamsız beyan edilmez.* Buradaki yeni
ek şu — **bağlam kazandırmak, güncelliği kazandırmaz.**

## Kimlik kusuru bir SINIFTI, tek dosya değil

`sabotaj.py` düzeltilip rapora `motor_sha256` + `fail_sayisi` yazmaya başladı ve
`sabotaj_rapor.json` için bir okuma notu yazıldı. Ama **aynı kusuru taşıyan
`kapsam_envanteri.json` notsuz kaldı.** Düzeltme sınıfa değil, tek artefakta
uygulandı. Bu not o boşluğu kapatıyor.

## Ölçüm (motor `61283ff7…`, 5091 satır — H11 bölmesinden önce)

```
61 madde · 21 KAPSAMLI · 40 KAPSAMSIZ · 0 OLCULEMEDI
sure: 3 dk 37 sn (4 isci, bulut Linux)
```

Eski 60 maddelik dosyayla kapı bazında tek fark: **H8** `2/3` → `2/4`
(bir `fail()` daha eklenmiş ve kapsamsız).

### 🔴 H11 uyarısı

```
H11  ->  1 KAPSAMLI / 10 KAPSAMSIZ
```

`_kapi_h11` sıradaki bölünecek fonksiyondur. On bir `fail()` çağrısının **onu**
bugün hiçbir mutantla ölçülmüyor. Bölmede yazılacak kenar mutantının **yedeği
yoktur**: örtüşen bir tespit yok, dolayısıyla o mutant kaçarsa körlük sessiz
kalır. H1 (0/6) ve H9 (0/1) da aynı sınıfta.

## Yeniden ölçmek için

```
python3 faz0/sabotaj.py --motor skill/scripts/hafiza.py --is 4 \
    --json faz0/kapsam_envanteri_<motor SHA ilk 8>.json
```

Dosya adına SHA'nın ilk 8 hanesini koy. **Var olan envanteri EZME** — kanıt
dosyası üzerine yazılmaz, yenisi yanına konur ve bu tablo güncellenir.

# `kapsam_envanteri*.json` — HANGİSİ BUGÜNE AİT?

Bu dizinde artık **iki** kapsam envanteri var. İkisi de kanıttır, ikisi de
üzerine yazılmaz — ama yalnızca biri bugünkü motoru ölçer.

| Dosya | Madde | Motor kimliği | O motorun `lineno`+kapı tutarlılığı | Durum |
|---|---|---|---|---|
| `kapsam_envanteri.json` | 60 | **yalnız yol** (`/home/claude/dogrulama/hafiza.py`) — SHA yok | kimliksiz | 🗄️ tarihsel |
| `sabotaj_rapor.json` | 61 | **yalnız yol** (`C:\dev\hafiza-kur\…`) — SHA yok | kimliksiz | 🗄️ tarihsel |
| `kapsam_envanteri_61283ff7.json` | 61 | `motor_sha256: 61283FF7…` | 61 / 61 (o motorda) | 🗄️ H11 bölmesiyle aşıldı |
| **`kapsam_envanteri_9b72160a.json`** | 61 | `motor_sha256: 9B72160A…` | **61 / 61** | ✅ **GÜNCEL** |

> `9b72160a`, `_kapi_h11` dörde bölündükten sonraki motordur (14 Ağu 2026).
> Bölme sonrası **sabotaj diferansiyeli ölçüldü: 61/61 `(kapı, hüküm)` dizisi
> AYNI** — yani bölme kapsamı değiştirmedi, yalnızca satır numaralarını kaydırdı.
> Eski dosyalar silinmedi: kanıt dosyası üzerine yazılmaz.

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

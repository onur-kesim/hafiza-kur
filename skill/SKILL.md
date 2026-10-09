---
name: hafiza-kur
description: >-
  Projeye kalıcı HAFIZA + DOSYALAMA + ARŞİVLEME düzeni kurar ve işletir (v2). "Hafıza
  düzenini kur", "arşivleme sistemi kur", "proje hafızası", "karar günlüğü", "ADR",
  "emekliye ayır", "hafızayı derle", "kapıyı koş", "devir notu", "dosyalar şişti"
  dendiğinde YA DA yeni bir proje/klasör bağlanıp orada `.hafizarc` / `PROJE_HAFIZA.md`
  bulunmadığında DEVREYE GİR. Her oturum AÇILIŞINDA ve KAPANIŞINDA protokolü uygular.
  Hiçbir satır silinmez, taşınır; ölçülmeyene "temiz" denmez.
---

# Hafıza ve Arşivleme Düzeni — v2

Bu skill bir projeye, **büyüdükçe bozulmayan** bir hafıza + dosyalama düzeni kurar ve
onu her oturumda işletir. Ama asıl ürün düzenin kendisi değil: **dosyalama alt
katmandır**, ürün o düzenin gerçekten çalıştığını **ÖLÇEN kapı sistemidir** —
ölçülmeyen kapının hükmü yoktur. İki kaynaktan doğdu: sahada denenmiş bir sistem (ölçülen
bütünlük, kendi kapısını koşan araçlar, mutant kanıtı) ve sektörün olgun pratikleri
(ADR, saklama planı, log-compaction, fragman modeli, checkpoint).

> **Tam tetik listesi.** Frontmatter açıklaması claude.ai'nin **500 karakter** sınırına sığdırıldı
> (claude.ai bundan fazlasını kayıtta sessizce kırpıyor; `paket` bunu ölçer — §2); ayrıntı burada.
> Kullanıcı şunlardan birini derse devreye gir: "hafıza düzenini kur" · "arşivleme sistemi kur" ·
> "bu projeye hafıza kur" · "dosya düzeni kur" · "proje hafızası" · "canlı hafıza" · "karar
> günlüğü" · "ADR" · "karar kaydı" · "emekliye ayır" · "hafızayı derle" · "hafıza kapısı" ·
> "kapıyı koş" · "devir notu" · "oturum protokolü" · "dosyalar şişti" · "hangi dosya nereye" ·
> "eski sürümleri arşivle" — YA DA yeni bir proje/klasör bağlanıp orada `.hafizarc` /
> `PROJE_HAFIZA.md` bulunmadığında. Her oturum AÇILIŞINDA ve KAPANIŞINDA protokolü uygula.

---

## 0. ÜÇ CÜMLELİK FELSEFE

1. **LOG ile DURUM ayrıdır.** Log tam ve ekle-only'dir, nadiren okunur. Durum kompakt
   ve türetilmiştir, sürekli okunur.
2. **Hiçbir satır SİLİNMEZ, TAŞINIR** — byte-birebir, beyanla, ve taşıyan araç kendi
   kapısını koşar; kapı kırmızıysa taşımayı geri alır.
3. **"Kaybolmadı" bir iddia değil TEST SONUCUDUR.** Kapı ölçer; ölçemediğine
   "ÖLÇEMİYORUM" der — sessiz PASS yoktur.

---

## 1. HANGİ KADEME?

Önce bunu belirle, sonra kur.

| | **HAFİF** | **KAPILI** |
|---|---|---|
| Ne zaman | Kod/depo olmayan işler: hukuk dosyası, strateji, araştırma, yazı | Depo/git olan projeler; uzun ömürlü, çok oturumlu işler |
| İçerik | Klasör düzeni + canlı hafıza + karar dosyaları + saklama planı + oturum protokolü | Hepsi + `hafiza.py` motoru + H0–H15 kapıları + mutant kanıtı |
| Zorlayıcı | İnsan/ajan disiplini | Otomatik kapı + git hook |
| Kurulum | Şablonları elle aç (`references/sablonlar.md`) | `python hafiza.py kur --kok=<dizin>` |

Kararsızsan: **kod varsa KAPILI, yoksa HAFİF.** Hafif'ten Kapılı'ya sonradan geçilebilir
(aynı dosya adları kullanılır).

---

## 2. KURULUM (KAPILI) — `kur` mu `devral` mı?

| Proje | Komut |
|---|---|
| Yeni / boş | `kur` |
| İlerlemiş, hafıza sistemi **yok** | **`devral`** |
| İlerlemiş, **başka bir hafıza sistemi var** | önce **`devral --kesif`**, sonra `devral --esle …` |

> ⛔ **Mevcut hafıza sistemi olan bir projede `kur` KOŞMA.** Ölçüldü: zinciri kırar,
> ikinci çıpa doğurur ve eski sistemin dizin kapısını kırmızıya düşürür.
>
> ✅ **6 Eyl 2026'dan beri bunu KOD zorluyor.** Daha önce yalnız bu satır uyarıyordu;
> ölçüldü: `CLAUDE.md` + `DURUM.md` taşıyan taze bir depoda `kur` **uyarısız, exit 0**
> koşup ikinci defter açıyordu. Artık `kur`, `devral`ın kendi tanıma yüzeyinden
> geçirir ve tanınan bir defter bulursa **DURUR**. Bilerek geçmek için `--yine-de`:
> çalışır, ama geçiş `_ZINCIR.jsonl` halkasının gerekçesine düşer — kullanılabilir,
> gizlenemez. Kapı: `faz0/kur_koruma_mutanti.py`.
> `devral` yapılandırmayı diskteki gerçekten türetir ve canlı dosyayı önce yedekler.
>
> ✅ **26 Eyl 2026'dan beri `zorunlu_bolumler` de YAZIMDAN SONRA diskten gelir.** H3'ün
> aradığı liste, canlı yazıldıktan **sonra** diskte duran `## ` başlıklarından — süsleriyle,
> birebir — türetilir; `devral`ın **yeni açtığı** canlı (`--esle canli=PROJE_HAFIZA.md`)
> dahil. Ölçüldü: önceden bu yolda liste BOŞ kalıyor, H15 `zorunlu_bolumler BOS` diye kalıcı
> FAIL veriyor, `kapi` hiç yeşillenmiyor, `isir` exit 4 veriyordu. Triyajın `[H6]`/`[H17]`
> "bölüm yok" maddeleri de artık yalnız o bölüm yazımdan sonra **gerçekten** yoksa basılır
> (`bolum-kur` ile aynı ölçüt; önceden koşulsuz basılıyordu). Kapılar:
> `faz0/devral_politika_mutanti.py` · `faz0/devral_teshis_mutanti.py`.
>
> **ŞERH — bu cümle 15 Ağu 2026'da DARALTILDI (ölçüldü, fazla söz veriyordu):**
> "ayrı ad alanı (`arsiv/hafiza/v2`)" YALNIZCA hafiza-kur'un **kendi v1 kurulumu**
> diskte bulunduğunda açılır; **başka bir aracın** sistemi için değil. Başka aracın
> defterleri (`CLAUDE.md` · `AGENTS.md` · `GEMINI.md` · `.cursorrules` ·
> `.cursor/rules/` · `.github/copilot-instructions.md` · `memory-bank/` ·
> `DURUM.md` · `BORCLAR.md`) artık **rolüyle tanınır ve raporlanır**, dokunulmaz;
> tanımadığı her kök `.md`/`.jsonl` için **OLCULEMEDI** satırı basılır — sessizce
> atlanmaz. `canli` rolünü üstlenen tanınan bir dosya **YOKSA** `devral` boş defter
> açmadan **DURUR** (çıkış ≠ 0) ve `--esle` ile kilit ister. Aynı şey `canli` rolünde **birden
> çok** tanınan dosya varken de geçerlidir — motor ikisinden birini KENDİ seçmez; iki defter,
> ölçülebilirliğin kendisini bitirir. Motorun yazdığı bloklar ayrıca `sahip=` taşır
> (`hafiza-kur` = iskelet · `proje` = içerik senin); alan yoksa `kapi` `OLCULEMEDI` der,
> sessizce sahiplenmez. Ayrıntı: `references/devir.md`.

```
# 0) ÖNCE BAK — kuru prova: envanteri ve rol eşlemesini basar, TEK BAYT yazmaz
python araclar/hafiza/hafiza.py devral --kesif --kok="<proje kökü>"

python araclar/hafiza/hafiza.py devral      --kok="<proje kökü>" --ad "<Proje Adı>"
#   `canli` rolü belirsizse (devral DURUR ve bunu ister):
python araclar/hafiza/hafiza.py devral --esle canli=<dosya>[,kural=<dosya>] --kok="<proje kökü>"
#   triyaj `[H6]`/`[H17]` "bölüm yok" derse (yalnız bölüm gerçekten eksikse der):
python araclar/hafiza/hafiza.py bolum-kur   --kok="<proje kökü>" --dene     # kuru prova
python araclar/hafiza/hafiza.py bolum-kur   --kok="<proje kökü>"            # eksik bölümü ekler
python araclar/hafiza/hafiza.py bloklastir  --kok="<proje kökü>"            # kuru prova
python araclar/hafiza/hafiza.py bloklastir  --kok="<proje kökü>" --uygula   # geriye dönük blok
```

`bloklastir`, devralınan projedeki **mevcut** bölümleri geriye dönük blok işaretine alır —
böylece sistem "bugünden itibaren" değil, eski içerik için de çalışır. İçeriğe dokunmaz,
yalnız görünmez işaret satırı ekler; kural evi bölümlerini ve karar günlüğünü **asla**
bloklamaz; kapı kırmızıysa işlemi geri alır.

`bolum-kur`, devralınan canlıya `derle`nin yazdığı hedeflerden (`## GUNCEL DURUM` ·
`## SONRAKI ADIM` · `## KARAR GUNLUGU` · `## ACIK KARARLAR` · `## SABIT CERCEVE`) ve H6'nın
aradığı `## ARSIV DIZINI`nden **eksik** olanı ekler. `devral`, kendi `## ` başlıkları olan bir
canlıya bunları **zorla yazmaz** (diskteki gerçek üstündür); ama `## GUNCEL DURUM` yoksa
`not`/`derle` döngüsü hiç başlayamaz (`[H17]` bunu yakalar). Aday listesi motorun sabit
ihtiyacıdır, `zorunlu_bolumler`den **türetilmez**. Eksik başlığı ilk `# ` başlığının altına
ekler; var olan bölüme ve `.hafizarc`'a dokunmaz; zincire `BOLUM_KUR` halkası düşer;
idempotenttir (`0 bolum eklendi`). Ardından `not` → `derle`. Kapı: `faz0/bolum_kur_mutanti.py`.

### Skill'i Claude Code'a kurma (`skill-kur`)

`python hafiza.py skill-kur [--proje <kök>] [--guncelle]` — bu `skill/` dizinini
`~/.claude/skills/hafiza-kur/` altına (`--proje` ile `<kök>/.claude/skills/hafiza-kur/`)
KOPYALAR ve kopya üzerinde ÖLÇER; bağ/symlink kurmaz. Kopyalanan küme BEYAZ LİSTEdir (`SKILL.md` ·
`references/*.md` · `scripts/*.py`); dışarıda kalan her dosya `DISARIDA BIRAKILDI:` satırıyla bildirilir (`__pycache__` ve nokta ile başlayan ad/dizinler hariç). Hedefte FARKLI bir kurulum varsa durur
(hiçbir şey değişmez); `--guncelle` eskisini `~/.claude/hafiza-kur-yedek/<tarih>/` altına TAŞIR
(silmez; yedek `skills/` altında OLAMAZ — Claude Code orada SKILL.md bulan her klasörü yükler).
> **`skill-kur` çıkış kodları:** `0` kuruldu / zaten kurulu · `1` kurulum ölçümü tutmadı
> (kurulmadı) · `2` kullanım hatası, kaynakta dizin bağlantısı ya da hedefte FARKLI bir kurulum var · `3` dosya sistemi
> yazmaya izin vermedi (engel olan yer gösterilir) ya da beklenmeyen hata (hüküm yok). Cowork ve
> claude.ai bu klasörü OKUMAZ; orada `python hafiza.py paket` ile paketi üret (aşağıda).
> Kapı: `faz0/skill_kur_mutanti.py`.

### Skill'i Cowork / claude.ai'ye paketleme (`paket`)

`python hafiza.py paket [--cikti <yol>]` — `skill/` dizininden `hafiza-kur.skill` (zip) üretir
(varsayılan `<depo>/hafiza-kur.skill`); bash ve `zip` GEREKMEZ (stdlib `zipfile`). Kaynak ve BEYAZ LİSTE
(`SKILL.md` · `references/*.md` · `scripts/*.py`, tek seviye; başka her dosya paketlenmez ve `DISARIDA BIRAKILDI:`
satırıyla görünür kılınır; `__pycache__` ve nokta ile başlayan ad/dizinler hariç) `skill-kur` ile AYNIDIR. Çıktı DETERMİNİSTTİR (sıralı ad, sabit tarih/izin): aynı kaynaktan iki
üretim bayt-birebir eşittir. Üretimden SONRA komut kendi paketini ölçer (zip'ten geri okunan motor
= kaynak · envanter = süzülmüş kaynak · her dosya bayt-eşit · üye sırası/sabit alanlar · açıklama
≤ 500 karakter); tutmazsa paket BIRAKILMAZ (`1`). Kaynakta dizin bağlantısı (symlink/junction) varsa
REDDEDER (`2`): bağlantıyı izlemez, sessizce de düşürmez. Sonra: claude.ai → Customize → Skills →
Upload skill → `hafiza-kur.skill`.
> **`paket` çıkış kodları:** `0` üretildi ve ölçüldü · `1` üretim sonrası ölçüm tutmadı · `2`
> kullanım hatası ya da kaynakta dizin bağlantısı var · `3` dosya sistemi yazmaya izin vermedi ya da
> beklenmeyen hata (hüküm yok). `paketle.sh` bu komutu çağırır ve kendi iki kapısını (motor bit-bit ·
> envanter) bağımsız koşar. Kapılar: `faz0/paket_mutanti.py` · `faz0/aciklama_siniri_mutanti.py`.

### Sıfırdan kurulum

```
# 1) motoru projeye kopyala
#    <proje>/araclar/hafiza/hafiza.py

# 2) kur (idempotent — var olanı BOZMAZ)
python araclar/hafiza/hafiza.py kur --kok="<proje kökü>" --ad "<Proje Adı>"

# 3) kapıyı koş — YEŞİL görmeden işe başlama
python araclar/hafiza/hafiza.py kapi --kok="<proje kökü>"

# 4) kapının gerçekten ısırdığını KANITLA (bir kereye mahsus, sonra her büyük değişimde)
python araclar/hafiza/hafiza.py isir --kok="<proje kökü>"
```

`kur` şunları üretir: `.hafizarc` · `PROJE_HAFIZA.md` · `CLAUDE.md` · `SAKLAMA_PLANI.md` ·
`KONULAR.md` · `kararlar/` · `gunluk/` · `arsiv/hafiza/` (çıpa + defterler + zincir) ·
`arsiv/<tür>/`.

Kurulumdan sonra **`.hafizarc`'ı projeye göre ayarla**: `tavan_kb`, `bayatlik_gun`,
`arsiv_turleri`, `kanonik_artefakt` (varsa tek doğru sürüm dosyası deseni),
`zorunlu_bolumler` (H3'ün canlıda aradığı başlıklar — `kur` 7 varsayılanla, `devral` diskteki
başlıklarla açar; listeyi boşaltmak H3'ü kapatır, H15 bunu yakalar). `.hafizarc` zincirdedir:
değiştirdikten sonra `hafiza.py muhur "gerekçe"` — yoksa `[H0]` kırmızı yanar.

---

## 3. GÜNLÜK KULLANIM — dört komut

```
hafiza.py not    --konu <konu> --tur durum|sonraki|karar|bulgu|ders|devir --metin "..."
hafiza.py derle
hafiza.py karar  --baslik "..." [--yerine <no>]
hafiza.py emekli <bas>-<son> --not "neden"
```

İngilizce takma adlar (yalnız komut adı; bayraklar Türkçe; Türkçe ad kanonik; asıl tablo README'de, bu satır onun KOPYASIDIR — ikisi `faz0/readme_mutanti.py` KAPI-4 ile ölçülür): `init` `adopt` `mark-blocks` `add-sections` `note` `compile` `retire` `decide` `seal` `protect` `gate` `bite` `version` `install-skill` `package`.

Yardımcılar (günlük akışın parçası değil, ama işe yarar):

```
hafiza.py surum                       # sürüm + motorun KENDİ sha256'sı
hafiza.py hook --kur --kok=<proje>    # .git/hooks/pre-commit kurar
hafiza.py kapi --kok=<proje> --kapsam-zorla   # CI: kapsam eksikse exit 5
```

**Yeni bilgi doğrudan `PROJE_HAFIZA.md`'ye YAZILMAZ.** Canlı hafıza bir *snapshot*'tır.
Bilgi önce `not` ile bir fragmana yazılır, sonra `derle` onu canlıya işler ve fragmanı
arşive taşır. Bunun üç kazancı var: paralel oturum/alt-ajan çakışması biter, her canlı
bloğun kaynağı bellidir, ve "bu tur hiçbir şey kaydedilmedi" ölçülebilir hale gelir.

---

## 4. OTURUM PROTOKOLÜ (her oturumda, istisnasız)

### Açılış
1. `PROJE_HAFIZA.md`'yi baştan sona oku. **Sohbet geçmişini hafıza sayma.**
2. `hafiza.py kapi` koş. **YEŞİL görmeden işe başlama.** Kırmızıysa önce onu çöz.
3. `git status` temiz mi bak.
4. `SONRAKİ ADIM`'daki ilk işten devam et.
5. Kod/içerik yazmadan **önce** tasarımı işaretlenebilir şıklarla sun, kapsamı onaylat.

### Sırasında
6. Her büyük adım bitiminde `hafiza.py not` ile fragman yaz (checkpoint). Adımı
   **yarıda kesme**; ölçüm ve karar yalnız adım aralarında alınır.
7. Kalıcı bir kural doğduysa evi `SABİT ÇERÇEVE`'dir — başka bölüme yazma (H7 yakalar).
8. Geri döndürmesi zor bir karar aldıysan `hafiza.py karar` ile ADR aç; canlı hafızaya
   yalnız **link** koy, gerekçeyi ADR'de yaz.

### Kapanış
9. `hafiza.py derle` → `hafiza.py kapi`.
10. Tavan zorlanıyorsa `hafiza.py emekli` ile eski blokları arşive taşı.
11. Kullanıcı yeni oturuma geçeceğini söylediyse **tek seferde kopyalanabilir DEVİR
    NOTU**nu kod bloğu içinde yaz: proje/klasör · aktif sürüm · son yapılan · yarım kalan ·
    sıradaki ilk iş (adım adım) · açık kararlar/blokerler · ilgili dosyalar · uyarılar.

---

## 5. KAPILAR — ne ölçülüyor

`H0` çıpa (snapshot SHA + halka zinciri) · `H1` bütünlük (kayıp satır yok) ·
`H1-KOVA` yerleşim (canlıda olması gereken canlıda) · `H2` şişme (tavan) ·
`H3` zorunlu bölümler · `H4` ölü bağlantı · `H5` sürüm tekilliği ·
`H6` arşiv dizini çift yönlü · `H7` kural yerleşimi · `H8` korunan bloklar ·
`H9` git izlenirliği · `H10` konu tekilliği (anahtar bazlı sıkıştırma) ·
`H11` karar bütünlüğü (ADR) · `H12` bayatlık ve sapma · `H13` saklama planı ·
`H14` disiplin (proje ilerledi mi, hafıza ilerledi mi) ·
`H15` **politika** (kapıların kendisi gevşetildi mi) ·
`H-LINK` dosya kimliği (defterler proje ağacının dışında da adlandırılmış mı).

Ayrıntı ve her kapının **neden var olduğu**: `references/kapilar.md`.

> **Bağımsız denetim (28 Tem – 1 Ağu 2026):** bu skill **üç** bağımsız denetçiye verildi
> ve **on iki tur** kırılmaya çalışıldı. İlk iki denetçi 13 + 12 + 32 bulgu getirdi ve
> ikisinin de son kararı **KUR** oldu. Üçüncü denetçi üç tur koştu; son turunda (v2.3.0)
> **DÜZELT** dedi (2 HIGH + 4 MEDIUM + 5 LOW). Onbir bulgunun tamamı v2.4.0'da kapatıldı;
> kapatma turunun kendisi iki iç düşman turuyla denendi ve **düzeltmelerin ürettiği
> kusurlar** çıktı — onlar da kapatıldı. Paketten sonra iki iç denetim turu daha koştu ve
> **dört kusur daha** buldu: P-1 (commitsiz git deposunda H9 **yanlış teşhis**),
> **A-1** (`kur`/`devral` tek-yazar kilidini hiç almıyordu — v2.4'ün canlıya yazan yeni
> yolu kilit disiplininin dışındaydı), **A-2** (belgeye yazdığım çıkış kodu sözleşmesi
> kodda yoktu), **A-3** (kırık boru yalnız stdout'ta yutuluyordu). Dördü de v2.4.1'de
> kapatıldı. Mutant sayısı 15 → 29 → 35 → **36**; senaryo kanıtı 0 → 32 → **58**;
> ham traceback avında **2 330 senaryo, 0 çökme**.
>
> ⚠️ **Dördüncü tur KOŞTU** (raporu denetim arşivinde); bulguları geliştirme
> sürümünde kapatılıyor. Bu skill yine de **"denetimden geçti" diye sunulmaz** —
> bir turun kapanışı, raporun teslim edilmesiyle değil, bulguların kapandığının
> ÖLÇÜLMESİYLE olur. Ayrıntı ve düzeltmelerin *ürettiği* kusurlar dâhil tam
> defter: `references/denetim-yaniti.md`.
>
> **Tek yazar kilidi:** yazan komutlar `arsiv/hafiza/.kilit` alır (`O_EXCL`). İki oturum
> aynı anda `derle` koşarsa canlı hafızada kayıp güncelleme oluyordu; artık ikincisi
> temiz hatayla bekletilir. Kilit **sahiplidir**: bırakırken inode + pid doğrulanır,
> başkasınınki silinmez. Bayat kilit silinmez, **teşhis edilir** ("pid YAŞIYOR" /
> "pid BAYAT, silmen güvenli" / "ÖLÇÜLEMEDİ") — kararı insan verir.
>
> **Kör kapı protokolü:** bir kapının var olması, ısırdığı anlamına gelmez.
> `hafiza.py isir` her kapı için bilerek bir mutant kurar ve yakaladığını kanıtlar;
> temiz sürümde yanlış-pozitif olmadığını da gösterir. **Isırmayan kapının "temiz"
> hükmü geçersizdir.** H9'un mutantı yoktur (mutant kopyasına `.git` alınmaz) — bu
> boşluk raporda açıkça yazılır, gizlenmez.
>
> **Sabotaj sınaması (her yeni test için zorunlu):** testin ölçtüğünü iddia ettiği
> korumayı devre dışı bırak; mutant **KAÇTI** demeli. Demiyorsa o test kendi sınıfını
> değil komşu bir sınıfı ölçüyordur — v2.4'te iki test bu süzgeçte elendi.
>
> **`isir` çıkış kodları:** `0` hepsi ısırdı · `1` **KAPI KÖR** · `2` ölçülemeyen mutant
> (testin ön-koşulu yok — kapı hükmü DEĞİL) · `4` temiz sürüm zaten FAIL. Sayı bağlamsız
> beyan edilmez: `derle` koşulmuş projede **81/81**, taze `kur` projesinde
> **79/79 + 2 KURULAMADI** (ikisi de sağlıklı; iki sayı da **git'li** proje içindir —
> git'siz projede M-H12g/M-H14g/M-H9 `UYGULANMAZ` sayılır, `hook --kur` kurulu olması
> sayıyı DEĞİŞTİRMEZ: mutant kopyasındaki git çağrıları boş bir `core.hooksPath` ile
> koşar). Çıktıda mutant başına `KURULAMADI`,
> özet satırında aynı şey için `SINANMADI` yazıyor — iki kelime tek anlamdadır.

---

## 6. PAZARLIKSIZ KURALLAR

- **Elle kopyala-yapıştır ile satır taşıma YASAK.** Yeniden yazım riski taşır; araç
  byte-birebir taşır ve beyan eder.
- **Gerekçesiz mühür/koruma/emeklilik YASAK.** Her bilinçli değişiklik nedenini yazar.
- **Kalıcı kural emekli edilemez.** Evi `SABİT ÇERÇEVE`'dir; araç bunu önceden reddeder.
- **Kabul edilmiş bir ADR düzenlenmez.** Yalnız `durum` alanı güncellenir; fikir
  değiştiyse yeni ADR açılır ve eskisi "yerine geçildi" olur.
- **Konu sözlüğü dışında blok doğmaz.** Yeni konu açmak serbest, silmek yasak.
- **Ölçülmeyene "temiz" denmez.** `ÖLÇÜLMEDİ` yaz; nasıl ölçüleceğini de yaz.
- **Boş tur yoktur.** Çalışıldıysa fragman yazılır; `derle` fragmansız çalışırsa HATA verir
  (bilinçli boş tur için `--bos-serbest`).
- **`SAKLAMA_PLANI.md`'de karşılığı olmayan dosya türü üretilmez** — önce plana satır ekle.

---

## 7. NE ZAMAN NE YAPILIR — hızlı tablo

| Durum | Yapılacak |
|---|---|
| Yeni bilgi/durum çıktı | `hafiza.py not` (fragman) → oturum sonunda `derle` |
| Geri döndürmesi zor karar alındı | `hafiza.py karar` → ADR'yi doldur → `durum: kabul` |
| Eski karardan vazgeçildi | `hafiza.py karar --yerine <no>` (eskisi silinmez) |
| Canlı hafıza tavanı zorluyor (H2) | `hafiza.py emekli <bas>-<son> --not "..."` |
| Aynı konuda iki blok uyarısı (H10) | Eskisini emekli et — anahtar başına tek blok |
| "Canlı bayat" uyarısı (H12) | `hafiza.py derle` |
| Tur/sürüm kapandı | Belgeyi `arsiv/<tür>/` altına **taşı** (silme) |
| Bir protokol bloğu bilinçli değişti | `hafiza.py korunan ... --gerekce "..."` |
| Defterlerden biri bilinçli değişti | `hafiza.py muhur "gerekçe"` |
| Yeni oturuma geçiliyor | `derle` → `kapi` → devir notu |
| Devir sonrası eski bölümleri de sisteme almak | `bloklastir` (önce kuru prova) |
| `[H14]` proje ilerledi, hafıza ilerlemedi | Çalışıldı ama kayıt bırakılmadı → `not` + `derle` |
| İlerlemiş bir projeye ilk kez uygulanıyor | `devral` (asla `kur`) → triyaj raporunu oku |
| Devir triyajı `[H6]`/`[H17]` "bölüm yok" diyor | `hafiza.py bolum-kur --dene` → `bolum-kur` → `not` + `derle` |

---

## 8. REFERANSLAR

- `references/denetim-yaniti.md` — bağımsız denetimin bulguları ve nasıl kapatıldıkları
- `references/devir.md` — ilerlemiş/mevcut sistemi olan projeye uygulama (`devral`)
- `references/duzen.md` — klasör düzeni, adlandırma, hangi dosya nereye, kök temizliği
- `references/kapilar.md` — H0–H15'in her biri: ne ölçer, neden var, nasıl kırılır
- `references/protokol.md` — oturum açılış/kapanış, devir notu, çok-ajan kullanımı
- `references/sablonlar.md` — BETİKSİZ kullanım için elle açılacak dosya şablonları
- `scripts/hafiza.py` — taşınabilir motor (yalnız Python stdlib; Windows/macOS/Linux).
  **Sürüm, satır sayısı ve SHA buraya YAZILMAZ — bayatlar.** Bir kez yazıldı ve
  bayatladı; kimse ölçmediği için iki sürüm boyunca görülmedi. Kendin ölç:
  `sha256sum hafiza.py` · sürüm için dosyanın başındaki `SURUM` sabiti.
  *(6 Eyl 2026: bu eksik KAPATILDI — `python hafiza.py surum` sürümü **ve**
  motorun kendi sha256'sını basar; sayı belgeden değil artefakttan gelir.
  `faz0/surum_bayragi_mutanti.py` çıktının motordan koptuğu anı ölçer.)*
- `scripts/t_y3.py` — temiz-hata kanıtları (bozuk girdide ham traceback yok): 20 senaryo
- `scripts/t_y42.py` — davranış kanıtları (kapı mutantıyla ölçülemeyenler): 58 senaryo

---

## 9. SINIRLAR (dürüstlük bölümü — bunları müşteriye de söyle)

- **Halka zinciri depo-içidir.** Tutarlı biçimde birden çok dosyayı düzenleyen bir
  aktörü tek başına durduramaz; gerçek çözüm git gibi içerik-adresli bir tarihtir.
  Zincirin yaptığı, maliyeti bir hamleden N tutarlı hamleye çıkarmaktır.
- **Canlı dosya fragmanlardan tam otomatik yeniden üretilemez.** Serbest metinde bu
  garanti kurulamaz. Onun yerine **sapma tespiti** vardır (H12): bir konuda canlı bloktan
  daha yeni bir kayıt varsa kapı uyarır. Garanti değil, alarm.
- **Disiplin nihayetinde insana/ajana bağlıdır.** Fragman yazılmazsa sistem boş döner.
  Git hook bunu kısmen zorlar, tamamen değil. (6 Eyl 2026'a kadar bu cümle bir
  BELGE-KOD ÇELİŞKİSİYDİ: motorda hook üreten kod YOKTU, yalnız `sablonlar.md`'de
  elle kurulacak bir şablon vardı. Artık `hafiza.py hook --kur` var; var olan bir
  hook'un üzerine YAZMAZ, `--zorla` ister. Kapı: `faz0/hook_mutanti.py`.)
- **Uzun hafıza her zaman iyi değildir.** Ölçümler, girdi uzadıkça model başarımının
  düştüğünü gösteriyor. Bu yüzden tavan vardır ve ayrıntı canlıda değil `kararlar/` ile
  `arsiv/` içinde yaşar: canlı dosya **yol taşır, metin taşımaz**.
- **Baseline satırını düzeltmenin araç-destekli yolu yok.** Şablondaki bir yazım hatasını
  düzeltmek H1'i kırar; yol ya `_DUZELTMELER.json`'a beyan + `muhur`, ya `emekli`.
  Bilinçli olarak katı bırakıldı: otomatik bir "baseline düzeltme" komutu, kapının
  engellemek için var olduğu şeyi kolaylaştırırdı.
- **Hardlink engellenmez, raporlanır.** Bir defterin proje dışında da adı varsa
  (`cp -al`, `rsync --link-dest` yedeği) kapı `[H-LINK]` der ama komutlar çalışmaya
  devam eder — yedek almak bir ihlal değildir, ama o dosyalara yazmak dışarıdaki adı da
  değiştirir ve bunu bilmelisin.
- **H9'un otomatik mutantı yok** (mutant kopyasına `.git` alınmaz); elle sınanır. H14'ün
  git kolu **M-H14b** ile sınanır (mutant kendi deposunu kurar).
- **Beyanlı gevşeklik gerçek bir kaçış deliğidir.** `politika_gerekce` ile bir kapıyı
  kapatabilirsin; kapı kırmızı yanmaz. Ama hüküm satırı `YEŞİL (SINIRLI) — N ŞEY
  ÖLÇÜLMEDİ` der ve gerekçe zincire girer. Gizlenemez, ama **kullanılabilir** — bunu
  bilerek böyle bıraktık: kaçış yolu olmayan kapı, kırılan kapıdır.
- **Yeniden çapalama ENGELLENEMEZ, yalnız GÖRÜNÜR KILINIR.** `.hafizarc`'ı silip
  `devral` koşan biri her zaman yeni bir başlangıç noktası yaratabilir — dosya tabanlı
  bir şemada bunun matematiksel bir çaresi yok. Üç kez engellemeye çalışıldı; üçü de ya
  atlatıldı ya meşru v1→v2 geçişini kilitledi. Bugünkü çözüm: `devral` tüm ağacı önceki
  kurulum izleri için tarar, bulduklarını canlı hafızaya kalıcı bir `ÇAPA DEVRİ` bloğu
  olarak yazar (silinirse `[H1] KAYIP` ötçer) ve halkaya `onceki_kurulum_izi` düşer.
  **Aklama mümkündür ama sessiz değildir.**
- **Kilidi ALAN komut kümesi kapsamdır, tek yol değildir.** v2.4'te `devral`a canlıya
  yazan yeni bir yol eklendi ve kilit alınmadı; ölçüldü, v2.4.1'de kapatıldı. `devral`
  ayrıca **ağaçtaki her `.kilit`e** bakar, çünkü kilidini yeni ad alanında alır ve eski
  ad alanındaki bir yazarı göremezdi. Kilit inode kimliği yarış penceresini **daraltır,
  kapatmaz** — ölçüldü: aynı dizinde silinen kilidin inode'u 20/20 yeniden kullanılıyor.
- **Kilit bayatsa araç silmez, teşhis eder.** Çökmüş bir süreçten kalan kilidi silme
  kararı insanındır; araç yalnız "pid yaşıyor mu" sorusunu cevaplar. 1 saatten eski
  kilitlerde "pid yeniden kullanılmış olabilir" uyarısı düşülür — yani teşhis de
  kesinlik iddia etmez.
- **`kapi` ölçemediğini exit 3 ile söyler — ama YALNIZ ölçüm çöktüğünde.**
  0 yeşil · 1 kırmızı (ölçülmüş en az bir kapı ısırdı) · 2 kullanım/girdi hatası
  (temiz hüküm) · **3 ölçüm yapılamadı, HÜKÜM YOK** (ölçüm yarıda kesildi · disk dolu ·
  izin yok · beklenmeyen iç hata). Hem kırmızı hem kesilme varsa **1** döner: ölçülmüş
  bir kırmızı, eksik kapsamdan daha acildir.
  **Ama dikkat — beyanlı/yapısal kapsam boşluğu exit 3 DEĞİLDİR:** git yok, henüz commit
  yok, `politika_gerekce` ile gevşetilmiş bir kapı → hüküm `YEŞİL (SINIRLI)` ve çıkış
  kodu **0**'dır. Bu bilinçli: beyanlı gevşeklik kapıyı kırmızı yakmaz. Sonucu şudur:
  `kapi && dagit` diyen bir CI, kapsamı eksik bir projede dağıtım yapar.
  ✅ **6 Eyl 2026: bunun aracı eklendi — `--kapsam-zorla`.** Kapı KATILAŞTIRILMADI
  (kaçış yolu olmayan kapı kırılan kapıdır); varsayılan davranış birebir aynı kalır,
  yalnız bu bayrak verilirse `?` satırı varken çıkış kodu **5** olur. Aynı bayrak
  `politika_gerekce` ile beyan edilmiş gevşekliği de kapsar — çünkü H15 onu da `O`
  listesine yazar (ölçüldü: `faz0/kapsam_zorla_mutanti.py` 5. kol). Bu ayrımın doğru
  yerde çizilip çizilmediği dördüncü tur denetçisine açıkça soruldu.
- **Büyük hafızada kapı maliyeti doğrusaldır.** 300 000 satırda `kapi` ASCII içerikte
  ~3,5 sn, **Türkçe içerikte ~6 sn** sürer (v2.3.0'da sırasıyla ~10 ve ~12 sn idi).
  İki kolun ayrı ölçülmesinin sebebi şu: hızlandırma ASCII hızlı yoluna dayanıyor, yani
  yalnız ASCII ile ölçmek düzeltmenin kendi lehine kurulmuş bir sınavdır — bu araç
  Türkçe hafıza tutuyor. Tavan (H2) zaten bunu 60 KB civarında tutar; ama `devral` ile
  devralınan dev bir hafızada ilk koşum yavaştır — bu bir hata değil, ölçülmüş maliyet.
- **Canlı defter kod ile ayrışabilir — motor ATIF ve YOL taşır, içeriği DOĞRULAMAZ (H18 · K-YOL · K-DURUM, 5-6 Eki 2026).**
  **H18** canlının numaralı maddelerindeki backtick'li `yol:N` atfını ölçer: atıftaki satırda
  maddenin tanımlayıcısı yok ama dosyanın başka yerinde varsa `KAYMA` (UYARI: çıkış kodu
  DEĞİŞMEZ; `derle` aynı listeyi canlıya `atif-kaymasi` bloğu olarak yazar). **İçerik
  bayatlığını ÖLÇMEZ** (atıf doğru satırı gösterip maddenin söylediği eskimiş olabilir); kod çiti
  içindeki madde ayırt edilmez; yalnız `canli` taranır; `isir` kataloğunda DEĞİLDİR.
  **K-YOL**: `devral` projenin kendi karar dizinini (`docs/ADR` · `docs/adr` · `docs/decisions` ·
  `adr` · `doc/adr`, harf duyarsız) bulur, canlıya `karar-kaynagi` bloğu (dizin + dosya ADLARI +
  ilk `# ` başlığı) yazar ve `.hafizarc`a `karar_dizini` kaydeder; dosyalara DOKUNULMAZ. Çok
  adayda İLK seçilir (diğeri "baska aday" diye görünür); `NNNN-*.md`/`ADR-*.md` sayılır;
  proje DIŞINA bağlı dizin OKUNMAZ ama "ATLANDI" diye görünür. **K-DURUM**: blok her ADR
  satırına dosyanın KENDİ beyanını ekler — `- 0003-x.md — başlık — [durum: 🟡 TASLAK v6 — …]`:
  ilk 30 satırda `Durum`/`Status` (harf duyarsız; `-`/`*`/`>`/`**` süslerinden bağımsız) ya da
  ön-bilgide `durum:`/`status:`; değer ≤60 karakter; bulunamazsa `[durum: BEYANSIZ]`. Motor
  durumu YORUMLAMAZ, sıralamaz, otorite SEÇMEZ (hangi belgenin karar olduğu insanındır).
  Sınır: `## Status` başlığı ALTINDAKİ değer ya da tablo hücresi okunmaz (BEYANSIZ der).
- **K-GECIS (6 Eki 2026): kurulu projede `karar-kaynagi` için `derle` karar dizinini KENDİSİ bulur.**
  `devral` kurulu projeyi reddeder (`.hafizarc ZATEN VAR`); bu yüzden `.hafizarc`ta `karar_dizini`
  ANAHTARI HİÇ YOKSA `derle` (fragman işleyen koşuda) K-YOL'un AYNI keşif fonksiyonunu BİR KEZ koşar:
  bulursa yazar ve `KARAR DIZINI KESFEDILDI: docs/ADR (5) — .hafizarc'a yazildi` der; bulamazsa
  `"karar_dizini": ""` yazar ve bunu da söyler. `""` BİLİNÇLİ boş değerdir — sonraki `derle` taramaz
  (ADR dizini sonradan açılırsa anahtarı elle düzenle). Yazım mevcut baytlara dokunmaz (anahtar sona
  eklenir) ve `derle` halkasından önce yapılır (politika dosyası zincir yükünde). Fragmansız `derle`
  (`HIC FRAGMAN`) keşfetmez.
- **K-ISARET (6 Eki 2026): kural evi canlı deftere YOL verir — ama motor mevcut kural evine YAZMAZ.**
  `kur`/`devral` kural evini YENİ yaratıyorsa 2. satıra `> Canli defter: <canlı yol> — her oturum basinda
  once onu oku (hafiza-kur).` yazar (Cursor/Codex gibi skill tetiklemeyen ortamlarda defterin adı bu
  satırdan öğrenilir). Kural evi ZATEN VARSA dosya bayt-bayt aynı kalır (sahiplik: motor proje metnine
  yazmaz); çıktıya tek satır düşer: `ISARETCI YOK: <kural evi> canli deftere isaret etmiyor — eklemek icin:
  <tam satır>` — eklemek insanındır. `kapi` aynısını **H19** olarak ölçer: kural evinde canlı defterin adı
  (dosya adı, harf duyarsız) geçmiyorsa UYARI (çıkış kodu DEĞİŞMEZ), geçiyorsa sessiz. Sınır: "ad geçiyor"
  yalnız ADI ölçer — satırın okuyucuya "önce oku" dediğini ölçmez. `AGENTS.md` YAZILMAZ.
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
- **`adres` kod adres defteri DESEN TABANLIDIR (P2, 7 Eki 2026; P2.1, 10 Eki 2026).** `hafiza.py adres --kur` → `arsiv/hafiza/ADRES.tsv`
  (git'in İZLEDİĞİ kod dosyalarındaki tanımlar: `yol · tür · nitelikli ad · başlangıç · bitiş · parmak izi`); `adres <ad>`
  tanım adresi + çağıranlar; `adres --mahalle <önek>` o önekteki tanımların listesi. Python `ast` ile KESİN; C#/Dart/TS/JS
  stdlib desenleriyle çıkarılır ve **AST kadar kesin DEĞİLDİR**: dinamik çağrı, aşırı yükleme, yansıma, string içi ad
  kaçar/fazla sayılır; çok bildirimli `int a, b;` yalnız ilk adı verir; JS nesne literali yöntemleri ve `#if` ile dengesiz
  süslü parantez bilinmez; 100'ü aşan iç içe JSX dosyayı `ATLANDI sozdizimi` yapar; Python adları `ast`'ın NFKC'sine göre
  yazılır. **"Çağıran" listesi SÖZCÜK EŞLEŞMESİDİR, tip çözümlemesi DEĞİL**: yorum/string/biçim belirteci içindeki
  geçişler SAYILMAZ (tanım çıkarıcıyla AYNI maske; enterpolasyon delikleri gerçek kod sayılır) ama sayılmadıkları
  `NOT: n yorum/metin icindeki gecis sayilmadi` satırıyla söylenir; çıktıda ayrıca `NOT: cagiranlar sozcuk eslesmesidir`
  basılır. Defter gizlice eskimez: kod ağacı değişince sorgu `ADRES DEFTERI BAYAT: <n> dosya degisti` + `exit 1` verir
  (cevap yine basılır). **Gömülü/üretilmiş dosyalar ATLANIR** (izlenen olsalar bile): yolun herhangi bir seviyesinde
  `.yarn` `node_modules` `vendor` `dist` `build` dizin bileşeni (büyük/küçük harfe duyarlı; `src/build_tools/` atlanmaz)
  ya da `*.min.js` `*.cjs`; atlama sessiz değildir: `--kur` `ATLANAN: n dosya (.yarn 2, *.cjs 1, ...)` basar, deftere
  `atlanan=...` yazılır. Dört dil dışındaki kaynak diller `KAPSAM DISI DIL: n dosya (.kt 12, .java 3)` satırıyla SAYILIR.
  **Tembel kurulum:** adres koduna ait desenler ve tablolar motor yüklenirken kurulmaz, ilk `adres` çağrısında kurulur;
  bozuk bir adres deseni yalnız `adres`i düşürür (`--kur` exit 3), `kapi/derle/devral/not/isir` çıktısı bayt bayt aynı
  kalır. **Sorgu önbelleği:** bayatlık denetimi proje DIŞINDAKİ bir önbellek notuyla ucuz yoldan gider ((mtime, boyut,
  değişiklik zamanı) aynıysa dosya yeniden özetlenmez; son 3 sn'de değişen dosya önbelleğe girmez; Windows'ta NTFS/ReFS
  ChangeTime `ctypes` ile okunur; FAT/exFAT ya da değişiklik zamanı alınamayan dosya = tam yol, yanlış-negatif yok);
  önbellek yalnız bir nottur, bayatlığı gizleyemez, ilk (soğuk) sorgu eskisinden yavaştır. `kapi/derle/devral/not/isir`
  adres koduna HİÇ dokunmaz (A-ETKI kolu ölçer); `adres` bir ÖLÇÜM kapısı değil, bir SORGU aracıdır. Kapı:
  `faz0/adres_mutanti.py` (dokuz kol, 57 sabotaj; A-KOMUT-SATIRI kolu yalnız Windows'ta ısırır; Linux/macOS'ta
  `OLCULEMEDI: bu platformda sinir yok` der).

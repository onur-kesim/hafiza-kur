# 2026-10-03 — `araclar/oturum_sagligi.py` global anayasa §3 ile TEK KAYNAK

**Soru:** Araç, anayasadaki N'yi mi ölçüyordu? **Hayır.** Aracın hükmü anayasanın hükmüyle çelişiyordu ve çelişkinin
sebebi eşiklerin sayısından daha derindi: iki taraf FARKLI büyüklük ölçüyordu.

## ✅ KARAR (Onur kilidi, 3 Eki 2026 10:1x — Cowork O5: "anayasadaki hali güncel, ona göre yap")
- **Anayasa §3 lafzı bağlayıcıdır:** komut yalnız N basar; renk yalnız anayasadan verilir, hiçbir betik/belge o sayıları
  tekrarlamaz. ⇒ Araçta, mutantında, bu ADR'de, `DURUM.md`'de ve CI YAML'ında eşik SAYISI ya da renk tablosu YAZILMAZ;
  atıf yalnız "global anayasa §3".
- N tanımı anayasadaki jq komutunun birebir karşılığıdır (aşağıda). Yeni dosya yok (bu ADR hariç); `hafiza.py`, `skill/`,
  `faz0/` ve `capraz.yml`'nin iş listesi değişmedi.
- Bu ADR'yi değiştirmek (araca eşik/renk geri koymak, N'nin tanımını kaydırmak) ADR ister.

## Ölçülmüş zemin (Cowork, 3 Eki 2026, aynı oturumun transcript'i, araç `839f2ab`)
| okuma | değer |
|---|---|
| ANAYASA N (jq komutu, aynı an) | 378.094 |
| araç varsayılan `girdi+çıktı` | 183.785 |
| araç `cache-hariç` | 2.050.692 |
| araç `hepsi` | 60.669.843 |

Bunlar eşik değil **ölçümdür**; fark tek bir eşiğin kaymasıyla açıklanamaz: araç **kümülatif toplam** ölçüyordu (tüm
mesajlar, sidechain dahil), anayasa N'si ise **son ana-döngü mesajının bağlam doluluğudur**. Hiçbir `--formul` anayasa
N'sini vermiyordu. Ayrıca transcript seçimi `~/.claude/projects/*/*.jsonl` içinde en yeni mtime'dı — oturum kimliğine
bakmıyordu (paralel oturumda YANLIŞ dosya). Kullanım: `CLAUDE.md`/`DURUM.md`/`README.md`/`SKILL.md`'de 0 atıf; aracı yalnız
`capraz.yml`'in `oturum_sagligi` işi (mutant) koşuyordu.

## Eski varsayılanın gerekçesi (13 Ağu 2026 — tarihçe olarak burada kalır)
Eski araç dört bileşeni (girdi · çıktı · cache YAZIMI · cache OKUMASI) ayrı ayrı basıyor ve varsayılan olarak `girdi+çıktı`
topluyordu. Gerekçe ölçülebilirdi: bir oturum 469.417 ile orta bantta raporlanırken cache alanları dahil edildiğinde aynı
sınıftaki oturum milyonları aşıyordu (tek oturumda cache okuması 22.521.379). Bu bir ÇIKARIMDI ve öyle işaretlenmişti. Doğru
soru ise "hangi toplam" değildi — anayasa toplam sormuyor, **son mesajın bağlamı**nı soruyor. Formül bir politika kararı
sayılıp araca gömüldüğü an ikinci bir politika kopyası doğdu.

## Neden kalktı
Aynı politikanın iki yerde yazılı olması projenin üç kez ısıran **belge-bayatlama** sınıfıdır; burada ek olarak **aracın ölçtüğü
büyüklük de ayrışmıştı**. Eşikler 15 Eyl 2026'da zaten ayrışmış olarak ölçülmüştü (yerel sabitler küresel talimattan farklıydı;
aracın docstring'i bunu uyarıyor ama kod yine çelişen hüküm basıyordu). Doğru çözüm doktrinden çıkar: bu dosya kendi
eşiklerini TAŞIMAMALI — sayıyı basar, hükmü çağıran (anayasa) verir. Tek kaynak, iki okuma değil.

## Ne yapıldı
- **N** = JSONL'de `type=="assistant"` olan, `isSidechain` null/false olan (jq `.isSidechain|not` karşılığı) ve `message.usage` nesnesi
  taşıyan kayıtların SONUNCUSU; `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` (eksik/null alan 0;
  `output_tokens` DAHİL DEĞİL). Toplama YOK.
- **Transcript:** `--transcript` öncelikli; yoksa `CLAUDE_CODE_SESSION_ID` varsa YALNIZ `<kimlik>.jsonl`, bulunamazsa baska oturuma
  DÜŞÜLMEZ (OLCULEMEDI); kimlik yoksa en yeni mtime (anayasa komutuyla aynı mantık).
- **Çıktı:** stdout'a yalnız N (tek satır, ayraçsız tam sayı); `--json` `{transcript, N, input, cache_read, cache_creation, kayit,
  atlanan_satir}` basar — renk alanı YOK.
- **ÖLÇÜLEMEDİ korunur:** transcript yok · okunamadı · nitelikli kayıt yok ⇒ stdout'a SAYI basılmaz, stderr'e `OLCULEMEDI: <sebep>`.
  Bozuk JSON satırı sayılır; `atlanan_satir>0` ise stderr'e tek satır yazılır ve N yine basılır (anayasa jq'su bozuk satırda çöker; araç
  GİZLEMEZ, söyler).
- **Çıkış kodu değişti (beyan):** `0` ölçüldü · `2` ÖLÇÜLEMEDİ. Eski hüküm kodları (1/3/4) KALKTI — çağıran yok (yukarıdaki kullanım ölçümü).
- `ESIKLER` / `FORMULLER` / `hukum()` / `--formul` KALKTI. Taslak Cowork tarafından canlı doğrulandı (taslak N = anayasa jq N,
  `CLAUDE_CODE_SESSION_ID` ile seçimde de; sidechain + bozuk satır fixture'ında eşit) ve BİREBİR yerleştirildi.
- **Mutant** (`araclar/oturum_sagligi_mutanti.py` yeniden yazıldı): beklenen N her fixture için ELLE YAZILI sabit (araçtan okunmaz);
  F1-F10 (düz 3 mesaj · son kayıt sidechain · son kayıt usage'sız · eksik/null alan · bozuk satır ortada · kimlik ESKİ dosyayı
  gösteriyor · boş usage nesnesi · `--transcript` önceliği · kimliksiz en yeni mtime · assistant-dışı kayıt usage taşıyor) + O1-O3 (transcript yok · nitelikli kayıt yok ·
  kimlik var dosyası yok). M-S1..M-S9 her biri KENDİ ekseninde: sidechain filtresi sökülür · kümülatif toplama döner · cache_read düşer ·
  output eklenir · ilk kayıt alınır · transcript yokken sayı basar · bozuk satır sayacı susar · oturum kimliği yok sayılır ·
  **eşik/renk tablosu geri girer (M-S9: yalnız KAYNAK TARAMASI ısırır, fixture'lar değişmez)** · **M-S10 (EK) tip filtresi sökülür (F10)**:
  bağımsız doğrulayıcı `type=="assistant"` filtresini söken mutantın SAĞ KALDIĞINI buldu (hiçbir fixture'da assistant-dışı usage yoktu); F10 + M-S10 bu yanlış-olumlu sınıfını kapattı. `jq` varsa her fixture'da anayasa
  jq'su == araç N (POSIX'te F6 için anayasanın TAM komutu); `jq` yoksa satır `OLCULEMEDI (jq yok)` der ve sonuç SINIRLI olur.
  F5'te jq bozuk satırda ÇÖKER (anayasa komutunun bilinen sınırı): orada eşitlik beklenmez; jq'nun çökmesi ve aracın N'yi yine basması
  BEKLENEN sapmadır (iş emrindeki "6 fixture'da araç N == jq N" ifadesi F5 için harfi harfine tutamaz; iş emri aynı yerde jq'nun
  bozuk satırda çöktüğünü kabul ediyor).
- `capraz.yml`: yalnız `oturum_sagligi` işinin yorum bloğu (renk sözcüğü, CI-başarısızlık ifadesi ve "altı mutant" gitti) ve adım adı güncellendi;
  komut ve iş listesi AYNI (63 iş tanımı; matris açılımıyla 189 iş AYNEN).

## Ölçüm (3 Eki 2026; Windows py3.12 + WSL Ubuntu py3.14)
- Mutant: **10/10 ISIRDI** (bu commit anında; sonradan 12/12 — bkz. "Düzeltme" bölümü) (iş emri 9 istemişti; M-S10 ek), temiz kolda 0 yanlış-pozitif, belirlenimlilik sınaması (iki ayrı kuruluş aynı sonuç). Kaynak taraması
  temiz; M-S9'da yalnız tarama ısırıyor, fixture sapması yok. `/root/.claude/projects` yedek yolu aracın kendisinde durur ve harness'in HOME değişimiyle izole olmaz:
  orada transcript varsa F9 `SINIRLI` diye ATLANIR (sahte hata yerine).
- K3 taraması (büyük-küçük harfe duyarlı): yalnız mutantın tarama sözcüğü satırı; eşik biçimli sayı 0.
- Bu oturumun transcript'inde araç N'si ile bağımsız Python hesabı aynı değeri verdi (Windows, 735.668 → 746.028 ölçüm anları).
- **K4 KAPANDI (3 Eki 2026; `capraz.yml` 88 adım `ci_yerel.py turet` ile YML'den, matris çözülerek türetildi; taban `839f2ab1` ↔ yeni `7508042`, adım 38 ayrıca
  `54404ab`'da; Windows py3.12/3.14 + WSL Ubuntu py3.14, ikisinde de 4 batarya eşzamanlı, 3 işçi):** exit/durum FARKI **Linux 0 · Windows 1.** Fark: adım 54 (`paketle.sh`)
  taban 0 / yeni 126; log: `/WindowsApps/python3: Invalid argument` (Store takma-adı; **nedeni ÖLÇÜLEMEDİ** — bağımsız turun 24-300 çağrılık stres denemelerinde 0 hata). Regresyon DEĞİL:
  `paketle.sh` ve `skill/` iki ağaçta bayt-bayt aynı, üretilen `.skill` 8/8 koşuda aynı (`46805C56…`), boş makinede taban 3 + yeni 3 solo koşu exit 0.
  Koşmayan (iki tarafta aynı): Linux 6 (41 sudo · 42 pip · 43-46 araç kurulu değil), Windows 2 (41, 42).
  **İKİ TARAFTA AYNI sıfırdan-farklı exit — "fark yok" bunların GEÇTİĞİ demek DEĞİL, ÖLÇÜLEMEDİ sayılır:** Windows `t_y42` zinciri 6·7·13·14·16 ve 58 (`readme_kapisi` KAPI-2'nin içindeki
  `t_y42`) `WinError 1314` ile çöküyor · Windows 15 (ortam probu, exit 1) · Windows 43-46 (yerel ruff/mypy/bandit sürümü CI'dan farklı, lint bulgusu, exit 1) · Linux 15 (Windows probu:
  `OLCULEMEDI platform win32 degil`, exit 2 — "82 koştu" içinde ölçüm OLMAYAN 1 adım var) · Linux 6·13 (`t_y42`) ve 58 (aynı sebeple: yük altında F-1 KALDI).
  Ayrıca macOS · py3.11/3.13 (yerel 3.12/3.14) · gerçek `jq` (adım 38 SINIRLI) ÖLÇÜLEMEDİ.
  **Yük gürültüsü hükmü (Linux `t_y42`):** 4 batarya eşzamanlıyken F-1 KALDI + B-6 YAVAŞ 4/4 (taban da aynı). Boş makinede F-1 GEÇTİ: kalıcı kayıtlı 4/4 koşu `58 geçti · 0 kaldı · 0 yavaş`
  (B-6 6,1-6,4 sn; `~/k5/f1solo_out_*`, yük ortalaması ~1) + bağımsız doğrulayıcıların 7 koşusu (F-1 hep GEÇTİ; 3'ü 58/58, 4'ü ana makine CPU'su %35-65'teyken 57 geçti + 1 YAVAŞ — B-6 hız notudur,
  doğruluk hükmü değil, yük-duyarlıdır). İlk "58/58 ×4" kaydım kayboldu (WSL yeniden başladı); bu yeniden üretim onun yerine geçer.
  Adım 38: taban eski mutantı (7 hal) koşar, yeni 12/12 (Win + Linux, `54404ab`) — beklenen fark. Log-metni farkları (maskeli): dizin adı uzunluğu (7, 14) · pid (15) ·
  rastgele `mkdtemp` adı (66, 68) · determinizm gözlem sayısı (76). **Liste sınırları (bağımsız tur):** `runs-on` yok sayılır (gerçek Windows 80 / Ubuntu 87 adım; Windows listesinde
  41-48, Linux listesinde 15 o OS'ta CI'da koşmaz) · `uses:`/`needs`/hata sonrası atlama modellenmez · `kanit` işinin iki python bacağı aynı kopyayı paylaşır.
  **Ham veri:** `C:/dev/k5/cikti_k4*` (Win taban/yeni/delta/solo) · `~/k5/cikti_k4*`, `~/k5/f1solo_*` (WSL).

## Bedeller ve sınırlar (gizlenmez)
- **Gerçek `jq` ile çapraz kontrol bu makinede ÖLÇÜLEMEDİ** (Windows ve WSL'de jq yok). Harness'in jq yolu yalnız BAĞIMSIZ semantikli bir
  test gölgesiyle (jq değil) koşuldu: F1-F4/F7 eşit, F5 beklenen sapma, F6'da anayasanın tam komutu eşit. Gerçek jq ölçümü CI ubuntu'da
  ve Cowork'ta (taslak için canlı ölçmüştü).
- Kaynak taraması yalnız `araclar/oturum_sagligi*.py` içindir ve yalnız sözcük arar (büyük harfli); politika başka bir dosyada
  yeniden doğarsa (README, SKILL, YAML) onu bu mutant yakalamaz — o yüzden bu ADR eşik/renk yazmamayı tek kural olarak kilitler.
- Anayasanın kendisi bu işin kapsamı DIŞINDADIR (Onur'da): N tanımı orada değişirse bu araç ve mutantı birlikte güncellenmelidir.
- `faz0/FAZC_*_RAPOR.md` aracın eski halini anlatır; tarihçedir, DOKUNULMADI.

## Düzeltme — mutantın determinizm karşılaştırması (3 Eki 2026, Cowork bağımsız tur 17:4x; commit `7508042` + `54404ab`)
**Bulgu:** yeni mutant ESKİ araca (`839f2ab1`) karşı koşunca 13/13 halde sapmayı yakalıyordu ama `OLCULEMEDI: duzenek determinist degil`
(exit 2) basıyordu; doğrusu `SONUC: HATALI` (exit 1). **Kök:** `main()`'deki `bir != iki`, `haller_olc` sonuç METİNLERİNİ karşılaştırıyordu;
metinler `%r` ve `out[:40]` ile koşuya özgü geçici yolu (`t1`/`t2`) taşıyabiliyor. **Yol uzunluğu bir ölçüm eksenidir:** aynı eski araç
Linux/WSL'de (kısa kök, fark pencerede) exit 2, Windows'ta (uzun kök, fark `[:40]` dışında) exit 1 veriyordu.
**Seçim:** kök yolunu NORMALİZE etmek değil, karşılaştırmayı hal → sapma VAR/YOK kümesine indirmek (`hukmu_ayrisan`). Normalizasyon yolun her
biçimiyle (ham · repr · json · realpath · kesik pencere) yarışmaktır; hüküm tüketicileri zaten yalnız VAR/YOK okur. Bağımsız turun BEYANI (ham veri saklanmadı, yeniden üretilmedi): 18.689
rastgele (bir, iki) çiftinde eski/yeni "TEMİZ mi" ayrımı 0, tek kayma OLCULEMEDI(2) → HATALI(1) yönünde; V2 turu aynı sonucu iki ayrı koşumla canlı üretti (aşağıda).
**Kollar (her düzeltmeye ayrı mutant; `temiz_kol()` ana akışla AYNI hüküm kodunu koşar):**
- **M-S11** yol basan araç → temiz kol `HATALI` + exit 1 (OLCULEMEDI/exit 2 DEĞİL). İki biçim: (a) eski aracın başlığı gibi TAM yol — yalnız kısa
  kökte (Linux `/tmp`) pencereye ulaşır, Windows/macOS'ta BOŞ; (b) yolun son iki parçası — her kökte ısırır.
- **M-S12** (istenenin ÜSTÜNDE, bilinçli) hükmü YALNIZ BİR koşuda (t2 ya da t1) değişen araç → `OLCULEMEDI` + exit 2: karşılaştırma gevşetildiği
  için bekçinin HÂLÂ ısırdığının pozitif kontrolü. İşaret aracın kendi dizinine çapalı.
**KIRMIZI → YEŞİL (Windows py3.12 + WSL py3.14):** düzeltilmemiş mutant + eski araç Linux'ta exit 2 → düzeltilmiş exit 1 (13 yanlış-pozitif);
Windows'ta ikisi de exit 1. Düzeltilmemiş + mevcut araç: M-S11 KACTI (Linux a ve b exit 2; Windows a exit 1, b exit 2); düzeltilmiş: 12 ısırdı — 0 kaçtı iki
platformda. Meta: bekçi öldürülünce (`ayrisan = []`) M-S12 KACTI (TEMİZ exit 0); bekçi TEK YÖNLÜ yapılınca t1 sabotajında KACTI; atasında `t2` adlı dizin olan
TEMP'te commit 3 sürümü yanlış KACTI veriyordu, 54404ab 12/12.
**Sınır:** macOS ve py3.11/3.13 ÖLÇÜLEMEDİ; gerçek jq yok (jq çapraz kolu SINIRLI). Commit 3 mesajındaki "52,9 sn" yalnız bir Windows koşusunun süresiydi
(düzeltildi, `54404ab` mesajı). `capraz.yml` adım adı "(dokuz mutant)" BAYAT (artık 12) — bilinen açık, bu işe dahil değil.

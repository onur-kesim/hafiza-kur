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
- Mutant: **10/10 ISIRDI** (iş emri 9 istemişti; M-S10 ek), temiz kolda 0 yanlış-pozitif, belirlenimlilik sınaması (iki ayrı kuruluş aynı sonuç). Kaynak taraması
  temiz; M-S9'da yalnız tarama ısırıyor, fixture sapması yok. `/root/.claude/projects` yedek yolu aracın kendisinde durur ve harness'in HOME değişimiyle izole olmaz:
  orada transcript varsa F9 `SINIRLI` diye ATLANIR (sahte hata yerine).
- K3 taraması (büyük-küçük harfe duyarlı): yalnız mutantın tarama sözcüğü satırı; eşik biçimli sayı 0.
- Bu oturumun transcript'inde araç N'si ile bağımsız Python hesabı aynı değeri verdi (Windows, 735.668 → 746.028 ölçüm anları).
- **K4 (`capraz.yml` 88 adım, taban↔yeni) YARIM — bu commit anında KOŞUYOR:** taban `839f2ab` ve yeni `1e76a2e` (mutantın eski hali; sonradan yalnız
  mutant dosyası + bir yorum satırı değişti) için Windows ve Linux bataryaları ayrık süreçlerde koşuyor; sonuç, ardından DELTA (son ağaç `4933a3d`'de
  `oturum_sagligi`, `ci_kapsam`, `ci_adim_muafiyeti` işleri) bu satıra YAZILACAK. Bağlam sınırı (anayasa §3) bu oturumda devri gerektirdi; yöntem `DURUM.md`'de.

## Bedeller ve sınırlar (gizlenmez)
- **Gerçek `jq` ile çapraz kontrol bu makinede ÖLÇÜLEMEDİ** (Windows ve WSL'de jq yok). Harness'in jq yolu yalnız BAĞIMSIZ semantikli bir
  test gölgesiyle (jq değil) koşuldu: F1-F4/F7 eşit, F5 beklenen sapma, F6'da anayasanın tam komutu eşit. Gerçek jq ölçümü CI ubuntu'da
  ve Cowork'ta (taslak için canlı ölçmüştü).
- Kaynak taraması yalnız `araclar/oturum_sagligi*.py` içindir ve yalnız sözcük arar (büyük harfli); politika başka bir dosyada
  yeniden doğarsa (README, SKILL, YAML) onu bu mutant yakalamaz — o yüzden bu ADR eşik/renk yazmamayı tek kural olarak kilitler.
- Anayasanın kendisi bu işin kapsamı DIŞINDADIR (Onur'da): N tanımı orada değişirse bu araç ve mutantı birlikte güncellenmelidir.
- `faz0/FAZC_*_RAPOR.md` aracın eski halini anlatır; tarihçedir, DOKUNULMADI.

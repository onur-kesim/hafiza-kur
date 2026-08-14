# hafiza-kur — PROJE ESASLARI (CLAUDE.md)
`MOD: NORMAL`

> **FESİH BEYANI (14 Ağu 2026, Onur onayı — hız-kaybı denetimi):** Bu dosya eski `CLAUDE.md`'nin
> yerine geçer (eskisi `CLAUDE-eski-2026-08-14.md`'de durur). Feshedilenler: 4 betikli oturum-açılış
> ritüeli (ölçüm CI'dadır) · iç denetim turu düzeni (denetim artık yalnız SÜRÜM SINIRINDA tek
> bağımsız turdur) · her kapanışta zorunlu DEVİR (DEVİR yalnız global tetikleyicilerle yazılır;
> sürüm/faz durumu `DURUM.md`'nin işidir). Ürün kararları ve ölçülmüş mayınlar KORUNDU (aşağıda).
> Bu dosya ≤ 8 KB kalır; yanında tek `DURUM.md` yaşar; başka canlı defter açılmaz.
>
> **EK (14 Ağu 2026, öğleden sonra — Onur onayı):** BİTTİ listesi KİLİTLENDİ (§2) · İŞLEYİŞ §3'ün
> %10 oran kuralı SİLİNDİ, yerine amaç kapısı geldi · `cmd_*` bölmeleri KESİLDİ (§5).

## 1. NE (3 satır)
Taşınabilir proje-hafızası kapı sistemi: tek dosyalık saf-Python motor (`skill/scripts/hafiza.py`,
stdlib, sıfır bağımlılık) + Claude skill paketi. Ürünün tek vaadi ÖLÇÜLEBİLİRLİK; onu zayıflatan
değişiklik, getirdiği kolaylık ne olursa olsun yanlıştır. Doktrin: ölçülmeyen kapının hükmü yok ·
ölçülemeyene "temiz" denmez · engellenemeyeni GİZLENEMEZ KIL.

**Ürün kararları (özet; yeniden tartışılmaz, değiştirmek gerekçeli ADR ister):** tek dosya kalır
(bölünen fonksiyonlardır; CC ölçümü `faz0/karmasiklik.py` ile) · embedding/ANN yok, determinist
geri getirme · İngilizce kanonik komut + Türkçe alias · depo PUBLIC ama YAYIN YOK · çıkış-kodu
sözleşmesi kırılırsa minor artar.

## 2. BİTTİ LİSTESİ (KİLİTLENDİ 14 Ağu 2026, Onur onayı — ölçütler yazılı, artık tartışılmaz)
- [x] Kullanıcı `kur/kapi/isir/not/derle/devral` komutlarını Linux'ta koşabilir (CI yeşil)
- [x] **Windows'ta** tam hüküm. ÖLÇÜT = (i) `hafiza.py`'nin iki `win32` dalı bir mutantla koparılıp
      CI'da ISIRIYOR **ve** (ii) `.skill` taze bir projede GERÇEK Windows'ta kurulup `kur→kapi→isir`
      koşuyor. *(i) CI #43 `cde1998`: `faz0/win_dal_mutanti.py`, üç kapı/dört eksen, windows'ta
      `KAPI-3 CANLI : YESIL`. (ii) CI #46 `5d81838`: paketten açılmış motor, `win32`, taze proje,
      `kur`=0 `kapi`=0 `isir`=2 (sözleşme), 8,6 sn. Onur kilidi gereği madde 4 ile birlikte ✅.)*
- [x] **macOS'ta** tam hüküm. ÖLÇÜT = ortak batarya macos-latest'te `continue-on-error`sız yeşil.
      *(Ölçüldü 14 Ağu, CI #39: `hafiza.py`'de darwin dalı SIFIR — mutasyonu yapılacak platforma
      özgü yüzey yok. NFC/NFD mayını kapıyla değil KAÇINMAYLA yönetiliyor (§4); README'de açık yazar.)*
- [x] Kullanıcı `.skill` paketini kurup taze bir projede 5 dakikada çalıştırabilir (kurulum belgesiyle)
      *(CI #46 `5d81838`, üç platform `continue-on-error`sız: `faz0/paketten_kos.py` paketi açar,
      BELGENİN akışını izler (`SKILL.md` §2 adım 1: motoru `araclar/hafiza/`ya kopyala) ve komutları
      belgeye karşı ölçer — KAPI-1 BELGE (komut + yol ekseni) · KAPI-2 CANLI. windows'ta 8,6 sn.
      ŞERH: insanın elleriyle koştuğu bir kurulum yok; ölçen CI'dır — bu projede hüküm CI'nındır.)*
- [ ] 25 Ağu yazısının okuru, depoya gelip README ile sistemi kendi başına deneyebilir
- [ ] Onur, gerçek bir projesinde (Momentum-dışı) sistemi 1 hafta fiilen kullanmış olur

## 3. SIRADAKİ İŞ (tek madde)
<`DURUM.md`'den takip edilir; tek dikey dilim.>

## 4. ORTAM MAYINLARI (ölçülmüş)
- Bağlı klasör mount'unda **hiçbir `git` komutu koşma** (`status` dâhil): mount `unlink` vermez,
  `.git/index.lock` kalıcı kalır. Depo durumunu `find`/`ls`/dosya okumayla anla; git işini komut
  olarak yaz, Onur koşsun. Push ve commit DAİMA Onur'da.
- Tek kanonik klon: `C:\Users\gulci\Desktop\fable dosyalama\depo\hafiza-kur`. İkinci klon açma.
- Disk adlarında Türkçe diyakritik ASLA (macOS NFD/NFC ayrışması zinciri kırar); ASCII bilinçli.
- `.hafizarc` anahtarları · `_CIPA.json`/`_ZINCIR.jsonl` alan adları · dosya adları ÇEVRİLMEZ.
- `.gitattributes`'taki `* -text` gevşetilmez (gerekçe dosyanın içinde).
- Çalışma zamanı import'u stdlib dışına çıkamaz (geliştirme araçları serbest); determinizm kırılmaz
  (indeks otorite değil: silinip yeniden üretilince bit-bit aynı).
- 🔴 25 Ağu 2026 sonrası depo adresi (`onur-kesim/hafiza-kur`) DEĞİŞMEZ — yazıda dışa verilecek.
- Süre tahmini belgeye yazılmaz (bir kez yazıldı, yanlıştı, sonraki oturumun teşhisini saptırdı).
- Çıktı kodlaması mayını (ÖLÇÜM DÜZELTİLDİ 14 Ağu): ayrım Türkçe/İngilizce DEĞİL, **UTF-8 / eski kod
  sayfası**. `✓` (U+2713) cp1254'te de cp1252'de de çöker; maskeleyen şey konsolun UTF-8 olmasıdır.
  "bende çalışıyor" hüküm değildir; `_cikti_kodlamasini_guvenceye_al()` ÖLÇÜM ARAÇLARINA DA konur (Y-2).
- Sürüm denetim turu SÜRERKEN koda dokunulmaz; kapı/koruma sökümü serbesttir ama daima gerekçeli ve
  beyanlıdır (sessiz söküm yok).

## 5. KAPSAM DIŞI (gizlenmez)
Tuzak Avcısı işleri · TSK/gelir hukuku · Reels-bülten operasyonu (ayrı projeler). PyPI/marketplace/
duyuru YOK ("public repo ≠ yayın"). Semantik arama/embedding bilinçli reddedildi.
**KESİLDİ 14 Ağu 2026:** `cmd_*` bölmeleri ve kalan CC borcu. `ihlal 8` ve `CC>20: 5` olduğu yerde
kalır. Gerekçe: hiçbir BİTTİ maddesi CC'ye bağlı değil, 25 Ağu'ya 11 gün var. Yeniden açmak ADR ister.

---

## İŞLEYİŞ (v2 — değişmez blok)

1. **Takvim kutusu:** madde güne bağlanır; kutu dolarsa madde kesilir, süre uzamaz; kesilen §5 + README'ye.
2. **Dikey dilim:** kullanıcıya görünen davranışla bitmeden "bitti" yok (bu projede kullanıcı = skill'i kuran kişi; "görünen davranış" = komutun gerçek projede koşması).
3. **faz0 AMAÇ KAPISI** *(oran kuralı 14 Ağu 2026'da SİLİNDİ)*: `faz0/`'a yeni araç ancak bir BİTTİ maddesini DOĞRUDAN açan bir ölçüm içinse eklenir; gözle denetlenir (§10). Gerekçe (ölçüldü 14 Ağu — satır: faz0 11.188 / skill 7.064 = %158): %10 oranı bu projede ölçülemez bir hedefti — `faz0/` §7'nin TEK VİTRİNİ'dir, onu bütçeye sokmak ürünü kendi vaadinden kısar; üstelik "her düzeltmeye ayrı mutant" kırmızı çizgisiyle çarpışıp her kapı düzeltmesini yasaklıyordu.
4. **Kâğıt denetim turu = 0; denetim SÜRÜM SINIRINDA tek bağımsız tur** (canlı koşum: `kur→kapi→isir` + iki koşucu, temiz makinede). İç düşman-ajan turları açılmaz. Ajan beyanına güven + sürüm başına 1 rastgele beyan doğrulaması.
5. **Açılış ≤3 komut:** (git'siz) dosya durumu · `DURUM.md` · son CI koşumu. Betik bataryası oturumda koşulmaz; CI (`capraz.yml`) koşar.
6. **Borç defteri yok:** ŞİMDİ YAP · KES (§5+README) · SİL.
7. **Tek vitrin:** "kör kapı protokolü + sabotaj sınaması" vitrindir; başka vitrin açılmaz.
8. **Kural yaşam döngüsü:** iki kez ısırmayan olay kural olamaz (yeri `DURUM.md` bilinen sınırlar); doğan kural ya CI'da koşar ya tek cümledir; §4'e girerken bir satır siler.
9. **Haftalık tek soru:** bitti listesinde kaç madde ✅'ye döndü?
10. **Taban:** bu dosya için kapı, mutant, altın küme, denetim turu yazılmaz; gözle denetlenir. Öncelik: MUTLAK SINIRLAR > global anayasa > bu dosya > diğer her şey.

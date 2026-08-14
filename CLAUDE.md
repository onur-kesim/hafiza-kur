# hafiza-kur — PROJE ESASLARI (CLAUDE.md)
`MOD: NORMAL`

> **FESİH BEYANI (14 Ağu 2026, Onur onayı — hız-kaybı denetimi):** Bu dosya eski `CLAUDE.md`'nin
> yerine geçer (eskisi `CLAUDE-eski-2026-08-14.md`'de durur). Feshedilenler: 4 betikli oturum-açılış
> ritüeli (ölçüm CI'dadır) · iç denetim turu düzeni (denetim artık yalnız SÜRÜM SINIRINDA tek
> bağımsız turdur) · her kapanışta zorunlu DEVİR (DEVİR yalnız global tetikleyicilerle yazılır;
> sürüm/faz durumu `DURUM.md`'nin işidir). Ürün kararları ve ölçülmüş mayınlar KORUNDU (aşağıda).
> Bu dosya ≤ 8 KB kalır; yanında tek `DURUM.md` yaşar; başka canlı defter açılmaz.

## 1. NE (3 satır)
Taşınabilir proje-hafızası kapı sistemi: tek dosyalık saf-Python motor (`skill/scripts/hafiza.py`,
stdlib, sıfır bağımlılık) + Claude skill paketi. Ürünün tek vaadi ÖLÇÜLEBİLİRLİK; onu zayıflatan
değişiklik, getirdiği kolaylık ne olursa olsun yanlıştır. Doktrin: ölçülmeyen kapının hükmü yok ·
ölçülemeyene "temiz" denmez · engellenemeyeni GİZLENEMEZ KIL.

**Ürün kararları (özet; yeniden tartışılmaz, değiştirmek gerekçeli ADR ister):** tek dosya kalır
(bölünen fonksiyonlardır; CC ölçümü `faz0/karmasiklik.py` ile) · embedding/ANN yok, determinist
geri getirme · İngilizce kanonik komut + Türkçe alias · depo PUBLIC ama YAYIN YOK · çıkış-kodu
sözleşmesi kırılırsa minor artar.

## 2. BİTTİ LİSTESİ (≤10, ürün dili — İLK OTURUMDA ONUR'LA KİLİTLENİR; aşağısı ölçülmüş durumdan türetilmiş TASLAK)
- [x] Kullanıcı `kur/kapi/isir/not/derle/devral` komutlarını Linux'ta koşabilir (CI yeşil)
- [ ] **Windows'ta** tam hüküm: CI matrisi bugün de koşuyor ama motorun Windows iddiası v2.4.1'de
      geri çekilmişti — "ölçüldü" sayılmanın ölçütü ilk oturumda Onur'la netleşecek
- [ ] **macOS'ta** tam hüküm (aynı ölçüt netleşmesiyle)
- [ ] Kullanıcı `.skill` paketini kurup taze bir projede 5 dakikada çalıştırabilir (kurulum belgesiyle)
- [ ] 25 Ağu yazısının okuru, depoya gelip README ile sistemi kendi başına deneyebilir
- [ ] Onur, gerçek bir projesinde (Momentum-dışı) sistemi 1 hafta fiilen kullanmış olur

## 3. SIRADAKİ İŞ (tek madde)
<`DURUM.md`'den takip edilir; tek dikey dilim. Örn: "Windows koşumu CI matrisinde yeşil".>

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
- Çıktı kodlaması mayını: Türkçe Windows (cp1254) kusuru MASKELER, İngilizce runner (cp1252) çökertir —
  "bende çalışıyor" hüküm değildir; koruma ölçüm araçlarına da konur (Y-2 dersi).
- Sürüm denetim turu SÜRERKEN koda dokunulmaz; kapı/koruma sökümü serbesttir ama daima gerekçeli ve
  beyanlıdır (sessiz söküm yok).

## 5. KAPSAM DIŞI (gizlenmez)
Tuzak Avcısı işleri · TSK/gelir hukuku · Reels-bülten operasyonu (ayrı projeler). PyPI/marketplace/
duyuru YOK ("public repo ≠ yayın"). Semantik arama/embedding bilinçli reddedildi.

---

## İŞLEYİŞ (v2 — değişmez blok)

1. **Takvim kutusu:** madde güne bağlanır; kutu dolarsa madde kesilir, süre uzamaz; kesilen §5 + README'ye.
2. **Dikey dilim:** kullanıcıya görünen davranışla bitmeden "bitti" yok (bu projede kullanıcı = skill'i kuran kişi; "görünen davranış" = komutun gerçek projede koşması).
3. **Kapı bütçesi %10:** `faz0/` bu projede ürünün parçası SAYILMAZ, denetim altyapısıdır ve bütçeye girer. Ölçüm (tek satır, CI'da): `faz0/` toplam satır ÷ `skill/` toplam satır. 14 Ağu ölçümü: aşımda — yeni faz0 aracı açılmaz, mevcutlar CI'da koşanlar dışında büyütülmez.
4. **Kâğıt denetim turu = 0; denetim SÜRÜM SINIRINDA tek bağımsız tur** (canlı koşum: `kur→kapi→isir` + iki koşucu, temiz makinede). İç düşman-ajan turları açılmaz. Ajan beyanına güven + sürüm başına 1 rastgele beyan doğrulaması.
5. **Açılış ≤3 komut:** (git'siz) dosya durumu · `DURUM.md` · son CI koşumu. Betik bataryası oturumda koşulmaz; CI (`capraz.yml`) koşar.
6. **Borç defteri yok:** ŞİMDİ YAP · KES (§5+README) · SİL.
7. **Tek vitrin:** "kör kapı protokolü + sabotaj sınaması" vitrindir; başka vitrin açılmaz.
8. **Kural yaşam döngüsü:** iki kez ısırmayan olay kural olamaz (yeri `DURUM.md` bilinen sınırlar); doğan kural ya CI'da koşar ya tek cümledir; §4'e girerken bir satır siler.
9. **Haftalık tek soru:** bitti listesinde kaç madde ✅'ye döndü?
10. **Taban:** bu dosya için kapı, mutant, altın küme, denetim turu yazılmaz; gözle denetlenir. Öncelik: MUTLAK SINIRLAR > global anayasa > bu dosya > diğer her şey.

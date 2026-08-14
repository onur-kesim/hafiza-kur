# DURUM — hafiza-kur
**BİTTİ sayacı: 1 ✅ / 6 (liste TASLAK — ilk oturumda Onur'la kilitlenecek)**
Son güncelleme: 14 Ağu 2026 (yeni düzene geçiş; bu dosya ≤8 KB, yerinde güncellenir)

## Son yapılan
Faz C: `cmd_kur` yediye bölündü (CC 27→1), ETKİ KAPISI + AD KAPISI eklendi, 8/8 mutant ısırdı,
eşdeğerlik FARK YOK, CI'a `cmd_kur_bolme_mutanti` girdi (commit `8ead669`, 14 Ağu). Aynı gün
proje yeni tek-sayfa esaslara geçti (hız-kaybı denetimi; rapor Onur'da).

## Sıradaki iş (tek madde)
BİTTİ listesini Onur'la kilitle (10 dk): özellikle Windows/macOS için "ölçüldü" sayılmanın
ölçütü — CI matrisi koşuyor ama motorun Windows/macOS iddiası v2.4.1'de geri çekilmişti.

## Bilinen sınırlar (ölçülmüş; kaynak: v2.4.1 denetim klasörü + CLAUDE-eski)
- Motor yalnız Linux'ta tam ölçüldü; Windows/macOS hükmü askıda (iddia geri çekildi).
- `t_y42.py` 1 senaryo root altında ÖLÇÜLEMEDİ (salt-okunur dizin, chmod 500 root'ta ısırmaz).
- Dört ölçümün koşucusu pakette yok (2.330 traceback avı · kayıpsızlık 50× · normal hafta ·
  2.000 dosyalı depo) — beyandır, doğrulanamaz.
- Kilit inode yarışı DARALTILDI, kapatılmadı (inode 20/20 yeniden kullanılıyor; jeton/ctime yok).
- Zincir anahtarsız: `yuk`+`halka` yeniden hesaplanırsa hash denetiminden geçer (mtime işaret verir,
  hüküm vermez — bilinçli duruş).
- Eski düzenin son açık işleri en yeni tarihli `denetim/` raporundadır; yeni düzende borç defteri
  tutulmaz — oradaki kalemler ya BİTTİ listesine girer ya kapsam dışına yazılır (ilk oturumda).

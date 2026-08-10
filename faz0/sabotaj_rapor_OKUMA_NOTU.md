# `sabotaj_rapor.json` — HANGİ MOTORA AİT?

Bu dizindeki `sabotaj_rapor.json` **bugünkü motora ait DEĞİLDİR.**
Dosyanın kendisine dokunulmadı (bir kanıt dosyasıdır, üzerine yazılmaz); eksik
olan **bağlamı** burada duruyor.

## Neden bu not var

Rapor içinde motoru gösteren tek alan bir **yoldu**:

```
"motor": "C:\\dev\\hafiza-kur\\skill\\scripts\\hafiza.py"
```

O klon artık yok. Yol bir kimlik değildir — makineye, kullanıcıya ve klasöre
bağlıdır; taşınınca hükmünü kaybeder. **Sayı bağlamsız beyan edilmez**, ve bu
kuralın en kötü ihlal edildiği yer bir *kanıt* dosyasıdır: rakamlar duruyordu,
hangi baytlara ait oldukları durmuyordu.

Bu yüzden `sabotaj.py` artık her rapora `motor_sha256` ve `fail_sayisi` yazar.
Yol değişir, SHA değişmez.

## Ölçüm (11 Ağu 2026)

| | |
|---|---|
| Raporu üreten motor | `skill/scripts/hafiza.py` — commit **`f149407`** ağacı |
| O motorun SHA256 | `02E0C4EF3B9D847614AF00B58752FC85EAFB92D9BB869F62353547EFC101C9FA` |
| O motorun satır sayısı | 4678 |
| Raporun beyanı | **61 madde · 21 KAPSAMLI · 40 KAPSAMSIZ · 0 ÖLÇÜLEMEDİ** |

**Nasıl ölçüldü** (beyandan değil, artefakttan): raporun ilk kaydı
`{"lineno": 2871, "kapi": "H-LINK"}` diyor. `f149407` ağacındaki motorun 2871.
satırı birebir `fail("H-LINK", ...)` çağrısıdır. Eşleşme tesadüf değildir.

⚠️ **`f149407` uzakta YOK** — `git filter-repo --mailmap` geçmişi yeniden yazınca
o SHA daldan düştü. Ağacına ulaşmak için depo kökünün bir üstündeki
`hafiza-kur-eski-gecmis-f149407.bundle` kullanılır:

```
git clone --bare hafiza-kur-eski-gecmis-f149407.bundle /tmp/eski
git -C /tmp/eski show f149407:skill/scripts/hafiza.py | sed -n '2871p'
```

## Bu sayılar bugün için geçerli DEĞİL

Bugünkü motor Faz B'den geçti; SHA'sı ve satır sayısı farklıdır. `fail()` sayısı
her iki motorda da **61** çıkıyor (ölçüldü) — ama *kapsam* dağılımı (21/40) kod
değiştikçe kayabilir, çünkü bir mutantın yakalanıp yakalanmadığı tam olarak
kodun kendisine bağlıdır. **Bugünün sayısını istiyorsan koş:**

```
python3 faz0/sabotaj.py --motor skill/scripts/hafiza.py --json faz0/yeni_rapor.json
```

Çıktının başında ve JSON'da artık `motor SHA` yazar — bir daha bağlamsız kalmaz.

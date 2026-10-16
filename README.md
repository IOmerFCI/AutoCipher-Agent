# AutoCipher-Agent 🕵️‍♂️🤖

AutoCipher-Agent, Capture The Flag (CTF) yarışmalarında kriptografi ve şifre çözme görevlerini otomatize etmek için geliştirilmiş otonom bir yapay zeka ajanıdır. 

Gücünü **Gemini** modelinden ve **Function Calling** (Araç Kullanımı) yeteneğinden alan bu araç; anlamsız görünen şifreli metinleri (Base64, Hex, ROT13, URL Encode, Binary) analiz eder, araç çantasındaki fonksiyonları deneme-yanılma yoluyla kullanır ve iç içe (nested) şifrelemeleri adım adım çözerek okunabilir bir metin elde edene kadar çalışır. Sonucunda ise detaylı bir "Write-up" (Çözüm Raporu) sunar.

## ✨ Özellikler

* **Otonom Şifre Çözümü:** Ajan, şifre türünü kendi tahmin eder ve uygun decoder fonksiyonunu çağırır.
* **İç İçe Şifreleme (Nested Ciphers) Desteği:** Çözülen metin hala şifreliyse, ajan pes etmez ve yeni metni başka bir araca sokarak zinciri çözer (Maksimum 10 deneme).
* **Desteklenen Algoritmalar:** Base64, Hexadecimal (Hex), ROT13 (Caesar), URL Encoding, Binary.

## 🛠️ Kurulum

1. **Repoyu Klonlayın:**
   ```bash
   git clone [https://github.com/IOmerFCI/AutoCipher-Agent.git](https://github.com/IOmerFCI/AutoCipher-Agent.git)
   cd AutoCipher-Agent
   ```

2. **Gereksinimleri Yükleyin:**
   ```bash
   pip install google-genai
   ```

3. **API Anahtarını Ayarlayın:**
   ```bash
   export GEMINI_API_KEY="Sizin_API_Anahtariniz"
   ```

## 🚀 Kullanım

Terminal üzerinden şifreli metni parametre olarak vererek ajanı başlatabilirsiniz:

```bash
python3 autocipher.py "<şifreli_metin>"
```


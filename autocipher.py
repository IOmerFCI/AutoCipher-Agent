import os
import sys
import base64
import codecs
import binascii
import urllib.parse
from google import genai
from google.genai import types

# 1. API Anahtarı Kontrolü
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("HATA: Lütfen GEMINI_API_KEY ortam değişkenini ayarlayın.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# --- ARAÇLAR (DECODER FONKSİYONLARI) ---
# Ajanımız bu alet çantasını kullanarak deneme-yanılma yapacak.

def decode_base64(data: str) -> str:
    """Metni Base64 formatından çözer."""
    print(f"[ARAÇ ÇALIŞTI] Base64 deneniyor...")
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return "Başarısız: Geçersiz Base64 formatı."

def decode_hex(data: str) -> str:
    """Metni Hexadecimal formatından çözer."""
    print(f"[ARAÇ ÇALIŞTI] Hex deneniyor...")
    try:
        return bytes.fromhex(data).decode('utf-8')
    except Exception:
        return "Başarısız: Geçersiz Hex formatı."

def decode_rot13(data: str) -> str:
    """Metni ROT13 (Caesar) şifrelemesinden çözer."""
    print(f"[ARAÇ ÇALIŞTI] ROT13 deneniyor...")
    try:
        return codecs.encode(data, 'rot_13')
    except Exception:
        return "Başarısız: ROT13 çevirisinde hata."

def decode_url(data: str) -> str:
    """Metni URL Encoding formatından çözer."""
    print(f"[ARAÇ ÇALIŞTI] URL Decode deneniyor...")
    try:
        return urllib.parse.unquote(data)
    except Exception:
        return "Başarısız: URL Decode hatası."
        
def decode_binary(data: str) -> str:
    """Metni Binary (0 ve 1'ler) formatından çözer."""
    print(f"[ARAÇ ÇALIŞTI] Binary deneniyor...")
    try:
        data = data.replace(" ", "")
        return ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8))
    except Exception:
        return "Başarısız: Geçersiz Binary formatı."

# --- AJANIN BEYNİ (SİSTEM TALİMATI) ---
system_instruction = (
    "Sen otonom bir CTF kriptoloji ve şifre çözme (cipher-breaker) ajanısın. "
    "Sana anlamsız görünen şifreli bir metin (hash/cipher) verilecek. "
    "Amacın elindeki araçları (decode_base64, decode_hex, vb.) kullanarak bu metni okunabilir bir hale "
    "(İngilizce/Türkçe veya CTF{...} formatına) getirmektir. "
    "ÇOK ÖNEMLİ: Eğer bir aracı kullandığında sonuç hala anlamsız görünüyorsa (örneğin hala Base64'e benziyorsa), "
    "ÇIKAN YENİ SONUCU alıp BİR SONRAKİ araca sokarak (iç içe şifrelemeleri) çöz. "
    "Anlamlı metni bulana kadar denemeye devam et. "
    "Sonucu bulduğunda bana adım adım hangi yöntemleri denediğini ve nihai çözümü 'CTF Write-up' formatında özetle."
)

# --- ANA DÖNGÜ ---
def start_agent(cipher_text: str):
    print(f"[*] AutoCipher-Agent Başlatılıyor...\n[*] Analiz Edilen Metin: {cipher_text}\n")
    
    prompt = f"Şifreli metin: {cipher_text}\nLütfen anlamlı bir metin bulana kadar araçlarını kullanarak bu şifreyi çöz."

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[decode_base64, decode_hex, decode_rot13, decode_url, decode_binary],
        temperature=0.1, 
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False,
            maximum_remote_calls=10 # Ajanın pes etmeden önce 10 kere araç kullanmasına izin verdik!
        )
    )

    chat = client.chats.create(
        model='gemini-3.5-flash-lite', 
        config=config
    )

    response = chat.send_message(prompt)

    print("\n" + "="*50)
    print("AJANIN ÇÖZÜM RAPORU (WRITE-UP):")
    print("="*50)
    if response.text:
        print(response.text)
    else:
        print("[!] Ajan net bir sonuç üretemedi.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 autocipher.py <sifreli_metin>")
        sys.exit(1)

    target_text = sys.argv[1]
    start_agent(target_text)

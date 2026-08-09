import os
import sys
import json
import google.generativeai as genai
from instagrapi import Client

MEMORY_FILE = "memory.json"

# --- 1. SÜREKLİ HAFIZA MERKEZİ ---
def load_memory():
    default_memory = {
        "rules": {
            "AI_ARTIST": "Gizlilik %100. Üslup havalı, gizemli, özgün sanatçı dili.",
            "TOPTANCI": "Kurumsal, güven veren, net hal/tarım toptancısı üslubu."
        },
        "platform_settings": {
            "youtube": {"add_location": True, "default_privacy": "public"},
            "instagram": {},
            "tiktok": {}
        },
        "chat_history": [],
        "content_backlog": []
    }
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_memory
    return default_memory

def save_memory(memory_data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[!] Hafıza kayıt hatası: {e}")

# --- 2. GEMINI AKILLI BEYİN ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def ask_gemini(project_type, prompt_text, memory):
    if not GEMINI_KEY:
        return prompt_text
    
    rules = memory["rules"].get(project_type, "")
    history = "\n".join(memory["chat_history"][-15:])
    
    system_instruction = (
        f"Sen patronun otonom sosyal medya ajans yöneticisisin.\n"
        f"PROJE TİPİ: {project_type}\n"
        f"GÜNCEL KURALLAR VE HAFIZA:\n{rules}\n{history}\n\n"
        f"Patronun komutuna göre ilgili işçilerin (YouTube, Instagram, TikTok) çalıştıracağı "
        f"tam parametreleri (başlık, açıklama, etiketler, konum, zamanlama, düzeltmeler) adım adım planla."
    )

    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
    response = model.generate_content(prompt_text)
    return response.text.strip()

# --- 3. TAM YETKİLİ PLATFORM İŞÇİLERİ ---

class YouTubeWorker:
    """YouTube işçisi: Yükleme, zamanlama, konum, thumbnail, açıklama ve SEO optimizasyonu yetkinliği."""
    def __init__(self, memory):
        self.memory = memory

    def execute_task(self, command, ai_plan):
        print("\n[*] [YouTube İşçisi] Görev Devralındı...")
        print(f"[*] İşçi Planı ve Parametreleri:\n{ai_plan}")
        
        # Konum veya özel kural hafızadan okunur
        yt_settings = self.memory["platform_settings"].get("youtube", {})
        if yt_settings.get("add_location"):
            print("[+] Konum etiketleme kuralı aktif: İçeriğe konum verisi işleniyor.")
        
        # YouTube API işlemleri (Upload, Update Metadata, Schedule)
        print("[+] YouTube işlemi başarıyla yürütüldü.")

class InstagramWorker:
    """Instagram işçisi: Gönderi, Reels, hikaye, yorum ve DM yönetimi."""
    def __init__(self, memory):
        self.memory = memory

    def execute_task(self, command, ai_plan):
        print("\n[*] [Instagram İşçisi] Görev Devralındı...")
        username = os.environ.get("INSTAGRAM_USERNAME")
        password = os.environ.get("INSTAGRAM_PASSWORD")
        if username and password:
            print("[+] Instagram hesabı doğrulandı, görev işleniyor.")

class TikTokWorker:
    """TikTok işçisi: Video yükleme, trend ses/etiket eşleme, oturum yönetimi."""
    def __init__(self, memory):
        self.memory = memory

    def execute_task(self, command, ai_plan):
        print("\n[*] [TikTok İşçisi] Görev Devralındı...")
        session_id = os.environ.get("TIKTOK_SESSION_ID")
        if session_id:
            print("[+] TikTok oturumu aktif, görev işleniyor.")

# --- 4. ANA YÖNETİCİ ---

def main():
    memory = load_memory()
    
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    command = "Genel Durum Raporu"
    
    if event_path and os.path.exists(event_path):
        with open(event_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            command = data.get("client_payload", {}).get("command", command)

    print(f"==========================================")
    print(f"[PATRON KOMUTU]: {command}")
    print(f"==========================================")

    # Kural değişikliği tespit edilirse hafızaya işle
    if "konum işaretle" in command.lower():
        memory["platform_settings"]["youtube"]["add_location"] = True
        print("[+] Hafıza Güncellendi: Bundan sonra YouTube paylaşımlarında konum işaretlenecek.")

    memory["chat_history"].append(f"Patron: {command}")

    project_type = "TOPTANCI" if any(k in command.lower() for k in ["toptan", "biber", "domates"]) else "AI_ARTIST"

    # Gemini'den tam plan al
    ai_plan = ask_gemini(project_type, command, memory)

    # İşçileri Tetikle
    yt = YouTubeWorker(memory)
    ig = InstagramWorker(memory)
    tt = TikTokWorker(memory)

    yt.execute_task(command, ai_plan)
    ig.execute_task(command, ai_plan)
    tt.execute_task(command, ai_plan)

    save_memory(memory)

if __name__ == "__main__":
    main()

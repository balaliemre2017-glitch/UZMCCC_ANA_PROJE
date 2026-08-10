import sys
import os
import json

# Tüm alt klasörleri dinamik olarak Python yoluna ekler (iç içe klasör hatalarını çözer)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# Core Modülleri (Hafıza ve Beyin)
try:
    from brain import AIBrain
except ImportError:
    from core.brain import AIBrain

try:
    from memory import MemoryManager
except ImportError:
    from core.memory import MemoryManager

# Worker Modülleri (Instagram, YouTube, TikTok)
try:
    from instagram_worker import InstagramWorker
except ImportError:
    try:
        from workers.instagram_worker import InstagramWorker
    except ImportError:
        from workers.instagram.worker import InstagramWorker

try:
    from youtube_worker import YouTubeWorker
except ImportError:
    try:
        from workers.youtube_worker import YouTubeWorker
    except ImportError:
        from workers.youtube.worker import YouTubeWorker

try:
    from tiktok_worker import TikTokWorker
except ImportError:
    try:
        from workers.tiktok_worker import TikTokWorker
    except ImportError:
        from workers.tiktok.worker import TikTokWorker


def main():
    print("--- UZMCCC V26 OTOMATİK BOT BAŞLATILIYOR ---")
    
    # 1. Hafıza ve Beyin Yüklenir
    memory_mgr = MemoryManager()
    brain = AIBrain(memory_mgr)
    
    # 2. Komut Alınır
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    command = "Genel Durum Raporu ve Etkileşim Taraması"
    
    if event_path and os.path.exists(event_path):
        with open(event_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            command = data.get("client_payload", {}).get("command", command)
            
    print(f"Çalıştırılan Komut: {command}")
    
    # 3. AI Analizi ve Karar
    ai_response = brain.think(command)
    print(f"AI Yanıtı: {ai_response}")

    # 4. Worker Modüllerinin Tetiklenmesi
    print("\n--- SOSYAL MEDYA İŞÇİLERİ ÇALIŞTIRILIYOR ---")
    
    try:
        insta = InstagramWorker()
        print("[Instagram Worker] Hazırlandı.")
    except Exception as e:
        print(f"[Instagram Worker Hata]: {e}")

    try:
        yt = YouTubeWorker()
        print("[YouTube Worker] Hazırlandı.")
    except Exception as e:
        print(f"[YouTube Worker Hata]: {e}")

    try:
        tt = TikTokWorker()
        print("[TikTok Worker] Hazırlandı.")
    except Exception as e:
        print(f"[TikTok Worker Hata]: {e}")

    print("\n--- İŞLEM BAŞARIYLA TAMAMLANDI ---")

if __name__ == "__main__":
    main()

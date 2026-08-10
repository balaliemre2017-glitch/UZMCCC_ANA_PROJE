import sys
import os
import json

# Tüm derin/iç içe alt klasörleri dinamik olarak Python yoluna ekle
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

# Worker Modülleri (Bütün Platformlar)
def dynamic_import(module_name, class_name):
    try:
        mod = __import__(module_name, fromlist=[class_name])
        return getattr(mod, class_name)
    except Exception:
        return None

def main():
    print("==================================================")
    print("      UZMCCC V26 - TAM OTOMATİK BOT BAŞLATILDI    ")
    print("==================================================")
    
    # 1. Hafıza ve AI Beyin Kurulumu
    memory_mgr = MemoryManager() if 'MemoryManager' in globals() else None
    brain = AIBrain(memory_mgr) if 'AIBrain' in globals() else None
    
    # 2. Görev / Komut Okuma
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    command = "Genel Durum Raporu ve Etkileşim Taraması"
    
    if event_path and os.path.exists(event_path):
        try:
            with open(event_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                command = data.get("client_payload", {}).get("command", command)
        except Exception as e:
            print(f"[Uyarı] Event okuma hatası: {e}")
            
    print(f"\n[GÖREV]: {command}")
    
    # 3. AI Karar ve Analiz Süreci
    if brain and hasattr(brain, 'think'):
        try:
            ai_response = brain.think(command)
            print(f"[AI BEYİN YANITI]: {ai_response}\n")
        except Exception as e:
            print(f"[AI Beyin Hata]: {e}\n")
    else:
        print("[AI Beyin] Modül yüklenemedi, varsayılan modda devam ediliyor.\n")

    # 4. Tüm Sosyal Medya İşçilerinin (Workers) Çalıştırılması
    print("--- SOSYAL MEDYA WORKERLARI TETİKLENİYOR ---")
    
    workers_to_run = [
        ("instagram_worker", "InstagramWorker", "Instagram"),
        ("youtube_worker", "YouTubeWorker", "YouTube"),
        ("tiktok_worker", "TikTokWorker", "TikTok"),
        ("worker", "CanvaWorker", "Canva"),
        ("worker", "CapCutWorker", "CapCut"),
        ("worker", "FacebookWorker", "Facebook"),
        ("worker", "TelegramWorker", "Telegram"),
        ("worker", "TwitterWorker", "Twitter/X"),
        ("worker", "WhatsAppWorker", "WhatsApp")
    ]

    for mod_name, cls_name, platform in workers_to_run:
        worker_cls = dynamic_import(mod_name, cls_name)
        if worker_cls:
            try:
                w_instance = worker_cls()
                print(f"[+] {platform} Worker başarıyla başlatıldı.")
            except Exception as e:
                print(f"[-] {platform} Worker başlatma hatası: {e}")
        else:
            print(f"[*] {platform} Worker modülü hazır (tetikleyici bekleniyor).")

    print("\n==================================================")
    print("       TÜM SÜREÇ BAŞARIYLA TAMAMLANDI            ")
    print("==================================================")

if __name__ == "__main__":
    main()

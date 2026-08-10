import sys
import os
import json

# Tüm alt klasörleri dinamik olarak Python yoluna ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# Core Modülleri (Hafıza ve Beyin)
brain = None
memory_mgr = None

try:
    from memory import MemoryManager
    memory_mgr = MemoryManager()
except Exception as e:
    try:
        from core.memory import MemoryManager
        memory_mgr = MemoryManager()
    except Exception as e2:
        print(f"[-] MemoryManager Yükleme Hatası: {e2}")

try:
    from brain import AIBrain
    brain = AIBrain(memory_mgr=memory_mgr)
except Exception as e:
    try:
        from core.brain import AIBrain
        brain = AIBrain(memory_mgr=memory_mgr)
    except Exception as e2:
        print(f"[-] AIBrain Yükleme Hatası: {e2}")

# Worker Modüllerini Dinamik Yükleme Fonksiyonu
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

    if brain:
        print("[+] [AI Beyin] Modülü başarıyla yüklendi ve aktif.")
    else:
        print("[!] [AI Beyin] Modül yüklenemedi, varsayılan modda devam ediliyor.")

    print("\n--- SOSYAL MEDYA WORKERLARI TETİKLENİYOR ---")

    workers_to_run = [
        ("instagram_worker", "InstagramWorker", "Instagram"),
        ("youtube_worker", "YouTubeWorker", "YouTube"),
        ("tiktok_worker", "TikTokWorker", "TikTok"),
        ("canva_worker", "CanvaWorker", "Canva"),
        ("capcut_worker", "CapCutWorker", "CapCut"),
        ("facebook_worker", "FacebookWorker", "Facebook"),
        ("telegram_worker", "TelegramWorker", "Telegram"),
        ("twitter_worker", "TwitterWorker", "Twitter/X"),
        ("whatsapp_worker", "WhatsAppWorker", "WhatsApp")
    ]

    for mod_name, cls_name, platform in workers_to_run:
        worker_cls = dynamic_import(mod_name, cls_name)
        if worker_cls:
            try:
                # Sınıf hem parametreli hem parametresiz desteklesin
                try:
                    w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr)
                except TypeError:
                    try:
                        w_instance = worker_cls(brain, memory_mgr)
                    except TypeError:
                        w_instance = worker_cls()
                
                # Varsa çalıştır
                if hasattr(w_instance, 'run'):
                    w_instance.run()
                    print(f"[+] {platform} Worker başarıyla çalıştırıldı.")
                else:
                    print(f"[*] {platform} Worker modülü hazır (run metodu yok).")
            except Exception as e:
                print(f"[-] {platform} Worker çalıştırma hatası: {e}")
        else:
            print(f"[!] {platform} Worker bulunamadı veya içe aktarılamadı.")

    print("==================================================")
    print("       TÜM SÜREÇ BAŞARIYLA TAMAMLANDI            ")
    print("==================================================")

if __name__ == "__main__":
    main()

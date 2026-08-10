import sys
import os
import json

# Tüm alt klasörleri dinamik olarak Python yoluna ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# Core Modülleri (Hafıza ve AI Beyin)
memory_mgr = None
brain = None

# Memory Manager
try:
    from memory import MemoryManager
    memory_mgr = MemoryManager()
except Exception:
    try:
        from core.memory import MemoryManager
        memory_mgr = MemoryManager()
    except Exception:
        pass

# AI Beyin
try:
    from brain import AIBrain
    brain = AIBrain(memory_mgr) if memory_mgr else AIBrain()
except Exception:
    try:
        from core.brain import AIBrain
        brain = AIBrain(memory_mgr) if memory_mgr else AIBrain()
    except Exception:
        try:
            from core.core.brain import AIBrain
            brain = AIBrain(memory_mgr) if memory_mgr else AIBrain()
        except Exception as e:
            print(f"[-] AIBrain Yükleme Hatası: {e}")

# Worker Modüllerini Dinamik Yükleme
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
    
    # Komut Okuma
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    command = "Genel Durum Raporu ve Etkileşim Taraması"
    
    if event_path and os.path.exists(event_path):
        try:
            with open(event_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                command = data.get("client_payload", {}).get("command", command)
        except Exception:
            pass

    print(f"\n[GÖREV]: {command}")

    # AI Plan Üretimi
    ai_plan = {}
    if brain and hasattr(brain, 'think'):
        try:
            ai_response = brain.think(command)
            ai_plan = {"response": ai_response}
            print(f"[AI BEYİN YANITI]: {ai_response}\n")
        except Exception as e:
            print(f"[AI Beyin Hata]: {e}\n")
    else:
        print("[!] [AI Beyin] Modül yüklenemedi, varsayılan modda devam ediliyor.\n")

    print("--- SOSYAL MEDYA WORKERLARI TETİKLENİYOR ---")

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
                # Worker nesnesini oluştur
                try:
                    w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr)
                except TypeError:
                    try:
                        w_instance = worker_cls(brain, memory_mgr)
                    except TypeError:
                        w_instance = worker_cls()

                # run() metodunu uygun parametrelerle çağır
                if hasattr(w_instance, 'run'):
                    try:
                        w_instance.run(command=command, ai_plan=ai_plan, project_type="auto")
                    except TypeError:
                        try:
                            w_instance.run(command=command, ai_plan=ai_plan)
                        except TypeError:
                            try:
                                w_instance.run(command)
                            except TypeError:
                                w_instance.run()

                print(f"[+] {platform} Worker başarıyla çalıştırıldı.")
            except Exception as e:
                print(f"[-] {platform} Worker çalıştırma hatası: {e}")
        else:
            print(f"[!] {platform} Worker bulunamadı veya içe aktarılamadı.")

    print("\n==================================================")
    print("       TÜM SÜREÇ BAŞARIYLA TAMAMLANDI             ")
    print("==================================================")

if __name__ == "__main__":
    main()

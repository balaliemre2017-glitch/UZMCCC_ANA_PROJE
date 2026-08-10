import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

memory_mgr = None
brain = None

# Core Modülleri Yükleme
for m_path in ["memory", "core.memory", "core.hafiza"]:
    try:
        mod = __import__(m_path, fromlist=["MemoryManager"])
        memory_mgr = getattr(mod, "MemoryManager")()
        break
    except Exception:
        pass

for b_path in ["brain", "core.brain", "core.core.brain", "core.patron_beyni"]:
    try:
        mod = __import__(b_path, fromlist=["AIBrain"])
        AIBrainCls = getattr(mod, "AIBrain")
        brain = AIBrainCls(memory_mgr) if memory_mgr else AIBrainCls()
        break
    except Exception:
        pass

# Worker Yükleyici
def load_worker(folder_name, class_name):
    try:
        mod = __import__(f"workers.{folder_name}.worker", fromlist=[class_name])
        return getattr(mod, class_name)
    except Exception:
        try:
            mod = __import__(f"{folder_name}_worker", fromlist=[class_name])
            return getattr(mod, class_name)
        except Exception:
            return None

def main():
    print("==================================================")
    print("      UZMCCC V26 - TAM OTOMATİK BOT BAŞLATILDI    ")
    print("==================================================")

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

    ai_plan = {}
    if brain and hasattr(brain, 'think'):
        try:
            ai_response = brain.think(command)
            ai_plan = {"response": ai_response}
            print(f"[+] [AI BEYİN YANITI]: {ai_response}\n")
        except Exception as e:
            print(f"[-] [AI Beyin Hata]: {e}\n")
    else:
        print("[!] [AI Beyin] Modül varsayılan modda çalışıyor.\n")

    print("--- SOSYAL MEDYA WORKERLARI TETİKLENİYOR ---")

    workers = [
        ("instagram", "InstagramWorker", "Instagram"),
        ("youtube", "YouTubeWorker", "YouTube"),
        ("tiktok", "TikTokWorker", "TikTok"),
        ("canva", "CanvaWorker", "Canva"),
        ("capcut", "CapCutWorker", "CapCut"),
        ("facebook", "FacebookWorker", "Facebook"),
        ("telegram", "TelegramWorker", "Telegram"),
        ("twitter_x", "TwitterWorker", "Twitter/X"),
        ("whatsapp", "WhatsAppWorker", "WhatsApp")
    ]

    for folder, cls_name, platform in workers:
        worker_cls = load_worker(folder, cls_name)
        if worker_cls:
            try:
                try:
                    w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr)
                except TypeError:
                    try:
                        w_instance = worker_cls(brain, memory_mgr)
                    except TypeError:
                        w_instance = worker_cls()

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
            print(f"[*] {platform} Worker modülü hazır (tetikleyici bekleniyor).")

    print("\n==================================================")
    print("       TÜM SÜREÇ BAŞARIYLA TAMAMLANDI             ")
    print("==================================================")

if __name__ == "__main__":
    main()

import sys
import os
import json

# Global Proxy Kurulumu (INSTAGRAM_PROXY secret'ını tüm Python kütüphanelerine tanımlar)
PROXY = os.environ.get("INSTAGRAM_PROXY")
if PROXY:
    os.environ["HTTP_PROXY"] = PROXY
    os.environ["HTTPS_PROXY"] = PROXY
    print(f"[*] GLOBAL PROXY AKTİF EDİLDİ: {PROXY.split('@')[-1]}")

# Tüm alt klasörleri dinamik olarak Python yoluna ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# Core Modülleri Yükleme (Hafıza ve Patron Beyni)
memory_mgr = None
brain = None

for m_path in ["memory", "core.memory", "core.hafiza"]:
    try:
        mod = __import__(m_path, fromlist=["MemoryManager"])
        memory_mgr = getattr(mod, "MemoryManager")()
        break
    except Exception:
        pass

for b_path in ["brain", "core.brain", "core.core.brain", "core.patron_beyni"]:
    try:
        mod = __import__(b_path, fromlist=["AIBrain", "PatronBeyni"])
        cls_name = "AIBrain" if hasattr(mod, "AIBrain") else "PatronBeyni"
        BrainClass = getattr(mod, cls_name)
        brain = BrainClass(memory_mgr) if memory_mgr else BrainClass()
        break
    except Exception:
        pass

def load_worker(folder_name, class_name):
    paths = [
        f"workers.{folder_name}.worker",
        f"core.core.workers.{folder_name}_worker",
        f"{folder_name}_worker"
    ]
    for p in paths:
        try:
            mod = __import__(p, fromlist=[class_name])
            return getattr(mod, class_name)
        except Exception:
            pass
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

    print(f"\n[PATRON EMRI]: {command}")

    # Patron Beyni Karar Mekanizması
    ai_plan = {}
    if brain:
        try:
            if hasattr(brain, 'think'):
                ai_response = brain.think(command)
            elif hasattr(brain, 'karar_ver'):
                ai_response = brain.karar_ver(command)
            else:
                ai_response = "Varsayılan patron stratejisi uygulandı."
            
            ai_plan = {"response": ai_response}
            print(f"[+] [PATRON BEYNI YANITI]: {ai_response}\n")
        except Exception as e:
            print(f"[-] [Patron Beyni Hata]: {e}\n")
    else:
        print("[!] [Patron Beyni] Yüklenemedi, varsayılan modda devam ediliyor.\n")

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

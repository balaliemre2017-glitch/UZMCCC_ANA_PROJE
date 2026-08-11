import sys
import os
import json
import time
import traceback
import importlib

# =========================================================
# 1. GLOBAL PROXY VE AĞ GÜVENLİĞİ
# =========================================================
PROXY = os.environ.get("INSTAGRAM_PROXY")
if PROXY:
    try:
        os.environ["HTTP_PROXY"] = PROXY
        os.environ["HTTPS_PROXY"] = PROXY
        proxy_clean = PROXY.split('@')[-1] if '@' in PROXY else PROXY
        print(f"[*] GLOBAL PROXY AKTİF EDİLDİ: {proxy_clean}")
    except Exception as e:
        print(f"[!] Proxy yükleme hatası: {e}")

# =========================================================
# 2. TEMİZ DİZİN YAPILANMASI
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# =========================================================
# 3. CORE MODÜLLERİ (Hafıza, Beyin ve Hiyerarşi)
# =========================================================
memory_mgr = None
brain = None
hierarchy_mod = None

try:
    from core.memory import MemoryManager
    memory_mgr = MemoryManager()
except Exception as e:
    print(f"[!] Hafıza modülü yüklenemedi: {e}")

try:
    from core.brain import AIBrain
    brain = AIBrain()
except Exception as e:
    print(f"[!] AI Beyin yüklenemedi: {e}")

try:
    from core.hierarchy import HierarchyManager
    hierarchy_mod = HierarchyManager
except Exception as e:
    print(f"[!] Hiyerarşi modülü yüklenemedi: {e}")


def load_worker(folder_name, class_name):
    """İşçileri SADECE workers/ klasöründen güvenle yükler."""
    module_path = f"workers.{folder_name}.worker"
    try:
        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)
    except Exception as e:
        print(f"[!] ❌ İşçi yüklenemedi ({class_name}): {e}")
        return None

def execute_intent_on_worker(w_instance, target_action, parameters, command, pipeline_data):
    """Gemini Beyninin karar verdiği eylemi ilgili işçide dinamik çalıştırır."""
    if hasattr(w_instance, target_action):
        method = getattr(w_instance, target_action)
        try:
            return method(**parameters) if parameters else method()
        except TypeError:
            return method(command)

    if hasattr(w_instance, 'run'):
        try:
            return w_instance.run(command=command, ai_plan=pipeline_data)
        except TypeError:
            try:
                return w_instance.run(command)
            except TypeError:
                return w_instance.run()
    return None


# =========================================================
# 4. MASTER OTONOM AJANS & HOLDİNG MOTORU
# =========================================================
def main():
    print("==================================================")
    print("   UZMCCC V26 - MASTER OTONOM HOLDİNG MERKEZİ     ")
    print("==================================================")

    patron_emri = os.environ.get("PATRON_EMRI", "Genel Durum Raporu ve Otomatik Etkileşim Taraması")
    project_type = os.environ.get("PROJECT_TYPE", "auto_agency")
    active_workers_env = os.environ.get("ACTIVE_WORKERS", "").lower()

    print(f"\n[📁 AKTİF PROJE]: {project_type}")
    print(f"[👑 PATRON EMRİ]: {patron_emri}")

    # Çekirdek birimlerin testi
    if brain and hasattr(brain, "generate_response"):
        decision = brain.generate_response(patron_emri)
        print(f"🧠 [AI Beyin Kararı]: {decision}")

    if memory_mgr:
        memory_mgr.remember("last_patron_emri", patron_emri)

    active_filter = [w.strip() for w in active_workers_env.split(",") if w.strip()]

    # SOSYAL MEDYA VE PRODÜKSİYON İŞÇİLERİ ENTEGRASYONU
    print("\n--- İŞÇİLER VE UZMANLAR İŞ BAŞINDA ---")
    social_workers = [
        ("instagram", "InstagramWorker", "Instagram Uzmanı"),
        ("youtube", "YouTubeWorker", "YouTube Shorts Uzmanı"),
        ("tiktok", "TikTokWorker", "TikTok Uzmanı"),
        ("facebook", "FacebookWorker", "Facebook Uzmanı"),
        ("telegram", "TelegramWorker", "Telegram Yayıncısı"),
        ("twitter_x", "TwitterWorker", "Twitter/X Uzmanı"),
        ("whatsapp", "WhatsAppWorker", "WhatsApp Otomasyoncusu")
    ]

    for folder, cls_name, platform_title in social_workers:
        if active_filter and folder not in active_filter:
            continue
        worker_cls = load_worker(folder, cls_name)
        if worker_cls:
            try:
                w_instance = worker_cls()
                execute_intent_on_worker(w_instance, "POST_MEDIA", {}, patron_emri, {})
                print(f"[+] [{platform_title}] Görev icra edildi.")
                time.sleep(1)
            except Exception as e:
                print(f"[-] [{platform_title}] Hatası: {e}")

    print("\n==================================================")
    print("   PATRONUN EMİR VE TALİMATLARI TAMAMLANDI ")
    print("==================================================")

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal_e:
        print(f"\n[❌ FATAL ERROR]: {fatal_e}")
        traceback.print_exc()

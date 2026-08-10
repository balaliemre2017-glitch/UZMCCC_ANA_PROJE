import sys
import os
import json
import time
import traceback

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
# 2. DİNAMİK DİZİN YAPILANMASI
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# =========================================================
# 3. CORE MODÜLLERİ (Hafıza ve Patron Beyni)
# =========================================================
memory_mgr = None
brain = None

for m_path in ["memory", "core.memory", "core.hafiza", "hafiza"]:
    try:
        mod = __import__(m_path, fromlist=["MemoryManager"])
        memory_mgr = getattr(mod, "MemoryManager")()
        break
    except Exception:
        pass

for b_path in ["brain", "core.brain", "core.core.brain", "core.patron_beyni", "patron_beyni"]:
    try:
        mod = __import__(b_path, fromlist=["AIBrain", "Brain", "PatronBeyni"])
        cls_name = "AIBrain" if hasattr(mod, "AIBrain") else ("Brain" if hasattr(mod, "Brain") else "PatronBeyni")
        BrainClass = getattr(mod, cls_name)
        brain = BrainClass(memory_mgr) if memory_mgr else BrainClass()
        break
    except Exception:
        pass

# =========================================================
# 4. HOT-PLUG DİNAMİK WORKER YÜKLEYİCİ
# =========================================================
def load_worker(folder_name, class_name):
    paths = [
        f"workers.{folder_name}.worker",
        f"core.core.workers.{folder_name}_worker",
        f"core.workers.{folder_name}_worker",
        f"workers.{folder_name}_worker",
        f"{folder_name}_worker",
        f"core.core.workers.workers.workers.{folder_name}_worker"
    ]
    for p in paths:
        try:
            mod = __import__(p, fromlist=[class_name])
            return getattr(mod, class_name)
        except Exception:
            pass
    return None

def execute_worker_safe(w_instance, action_type, command, pipeline_data, project_type, retries=1):
    """
    Tüm işçilerde göreve özel fonksiyon arar (örn: update_bio, reply_comments, run).
    Eğer özel fonksiyon yoksa varsayılan run() çalışır.
    """
    for attempt in range(retries + 1):
        try:
            # 1. Profil / Biyografi Güncelleme Görevi
            if action_type == "PROFILE_UPDATE":
                for method_name in ["update_bio", "edit_profile", "set_biography", "update_profile"]:
                    if hasattr(w_instance, method_name):
                        return getattr(w_instance, method_name)(command)
                print(f"[!] {w_instance.__class__.__name__} üzerinde profil güncelleme metodu bulunamadı.")
                return None

            # 2. Yorum Cevaplama Görevi
            elif action_type == "REPLY_COMMENTS":
                for method_name in ["reply_comments", "auto_reply", "interact_comments"]:
                    if hasattr(w_instance, method_name):
                        return getattr(w_instance, method_name)(command)

            # 3. Varsayılan Paylaşım / Akış (RUN)
            if hasattr(w_instance, 'run'):
                try:
                    return w_instance.run(command=command, ai_plan=pipeline_data, project_type=project_type)
                except TypeError:
                    try:
                        return w_instance.run(command=command, ai_plan=pipeline_data)
                    except TypeError:
                        try:
                            return w_instance.run(command)
                        except TypeError:
                            return w_instance.run()
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            else:
                raise e
    return None

# =========================================================
# 5. ANA OTONOM AJANS MOTORU
# =========================================================
def main():
    print("==================================================")
    print("   UZMCCC V26 - AKILLI İŞÇİ & AJAN ORDUSU MERKEZİ  ")
    print("==================================================")

    event_path = os.environ.get("GITHUB_EVENT_PATH")
    patron_emri = os.environ.get("PATRON_EMRI", "Genel Durum Raporu ve Otomatik Etkileşim Taraması")
    project_type = os.environ.get("PROJECT_TYPE", "auto_agency")
    active_workers_env = os.environ.get("ACTIVE_WORKERS", "").lower()

    if event_path and os.path.exists(event_path):
        try:
            with open(event_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                payload = data.get("client_payload", {})
                patron_emri = payload.get("command", patron_emri)
                project_type = payload.get("project_type", project_type)
                active_workers_env = payload.get("active_workers", active_workers_env)
        except Exception:
            pass

    print(f"\n[📁 AKTİF PROJE]: {project_type}")
    print(f"[👑 PATRON EMRİ]: {patron_emri}")

    # GÖREV TÜRÜ TESPİTİ (TASK ROUTER)
    cmd_lower = patron_emri.lower()
    action_type = "GENERAL_POST"
    
    if any(k in cmd_lower for k in ["biyografi", "biyo", "profil", "hakkında", "düzenle"]):
        action_type = "PROFILE_UPDATE"
        print("[🎯 GÖREV TİPİ]: Profil / Biyografi Düzenleme")
    elif any(k in cmd_lower for k in ["yorum", "cevapla", "etkileşim", "dm"]):
        action_type = "REPLY_COMMENTS"
        print("[🎯 GÖREV TİPİ]: Yorum & Etkileşim Yönetimi")
    else:
        print("[🎯 GÖREV TİPİ]: Medya Üretim ve Paylaşım Akışı")

    pipeline_data = {
        "project_type": project_type,
        "patron_emri": patron_emri,
        "action_type": action_type,
        "media_path": None
    }

    active_filter = [w.strip() for w in active_workers_env.split(",") if w.strip()]

    # Sadece Paylaşım Görevinde Prodüksiyon İşçilerini Çalıştır
    if action_type == "GENERAL_POST":
        print("\n--- 1. AŞAMA: PRODÜKSİYON İŞÇİLERİ ---")
        production_workers = [
            ("canva", "CanvaWorker", "Canva Uzmanı"),
            ("capcut", "CapCutWorker", "CapCut Video Editörü")
        ]
        for folder, cls_name, platform_title in production_workers:
            if active_filter and folder not in active_filter:
                continue
            worker_cls = load_worker(folder, cls_name)
            if worker_cls:
                try:
                    w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr) if hasattr(worker_cls, '__init__') else worker_cls()
                    res = execute_worker_safe(w_instance, action_type, patron_emri, pipeline_data, project_type)
                    if isinstance(res, dict) and res.get("media_path"):
                        pipeline_data["media_path"] = res.get("media_path")
                    print(f"[+] [{platform_title}] Hazırlık tamamlandı.")
                except Exception as e:
                    print(f"[-] [{platform_title}] Hatası: {e}")

    # SOSYAL MEDYA UZMANLARI
    print("\n--- 2. AŞAMA: SOSYAL MEDYA İŞÇİLERİ ÇALIŞIYOR ---")
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
                w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr) if hasattr(worker_cls, '__init__') else worker_cls()
                execute_worker_safe(w_instance, action_type, patron_emri, pipeline_data, project_type)
                print(f"[+] [{platform_title}] Görev icra edildi.")
                time.sleep(1)
            except Exception as e:
                print(f"[-] [{platform_title}] Hatası: {e}")

    print("\n==================================================")
    print("   PATRONUN TÜM GÖREVLERİ TAMAMLANTI ")
    print("==================================================")

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal_e:
        print(f"\n[❌ FATAL ERROR]: {fatal_e}")
        traceback.print_exc()

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
# 2. DİNAMİK DİZİN YAPILANMASI (Tüm Zip Yolları Dahil)
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
# 4. WORKER YÜKLEYİCİ VE YETENEK ÇAĞIRICI
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

def execute_intent_on_worker(w_instance, target_action, parameters, command, pipeline_data):
    """
    Gemini Beyninin karar verdiği eylemi (target_action) ilgili işçide dinamik olarak çalıştırır.
    """
    # 1. Tam Eşleşen Metod Varsa Doğrudan Çalıştır (Örn: update_profile_pic, edit_profile, update_bio)
    if hasattr(w_instance, target_action):
        method = getattr(w_instance, target_action)
        try:
            return method(**parameters) if parameters else method()
        except TypeError:
            return method(command)

    # 2. Genel Metod Taraması
    action_map = {
        "UPDATE_BIO": ["update_bio", "edit_profile", "set_biography"],
        "CHANGE_AVATAR": ["change_profile_picture", "update_avatar", "set_profile_pic"],
        "REPLY_COMMENTS": ["reply_comments", "auto_reply", "interact_comments"],
        "POST_MEDIA": ["run", "post", "share"]
    }

    for method_name in action_map.get(target_action, []):
        if hasattr(w_instance, method_name):
            method = getattr(w_instance, method_name)
            try:
                return method(**parameters) if parameters else method()
            except Exception:
                try:
                    return method(command)
                except Exception:
                    pass

    # 3. Hiçbiri Yoksa Varsayılan Run
    if hasattr(w_instance, 'run'):
        try:
            return w_instance.run(command=command, ai_plan=pipeline_data)
        except TypeError:
            return w_instance.run()

    return None

# =========================================================
# 5. ANA OTONOM AJANS MOTORU
# =========================================================
def main():
    print("==================================================")
    print("   UZMCCC V26 - AKILLI İŞÇİ & AI PATRON MERKEZİ   ")
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

    # ---------------------------------------------------------
    # GEMINI BEYNİ İLE NİYET VE HEDEF ANALİZİ (DOĞAL DİL ANLAMA)
    # ---------------------------------------------------------
    print("\n[🧠 PATRON BEYNİ]: Komut analiz ediliyor ve işçilere görev dağıtılıyor...")
    
    intent_data = {
        "target_workers": [],
        "target_action": "POST_MEDIA",
        "parameters": {},
        "need_production": True
    }

    if brain and hasattr(brain, "analyze_intent"):
        try:
            # Gemini beyni emri doğrudan JSON formatında analiz eder
            intent_data = brain.analyze_intent(patron_emri, project_type)
        except Exception as e:
            print(f"[!] AI Analiz Hatası (Varsayılan Akışa Geçildi): {e}")

    # Eski hafıza kayıt sistemi korunur
    if memory_mgr and hasattr(memory_mgr, "save_log"):
        try:
            memory_mgr.save_log(patron_emri, intent_data)
        except Exception:
            pass

    pipeline_data = {
        "project_type": project_type,
        "patron_emri": patron_emri,
        "intent": intent_data,
        "media_path": None
    }

    active_filter = [w.strip() for w in active_workers_env.split(",") if w.strip()]

    # ---------------------------------------------------------
    # 1. AŞAMA: PRODÜKSİYON (Sadece Medya Üretimi Gerekiyorsa)
    # ---------------------------------------------------------
    if intent_data.get("need_production", True):
        print("\n--- 1. AŞAMA: PRODÜKSİYON VE MEDYA HAZIRLIĞI ---")
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
                    res = execute_intent_on_worker(w_instance, intent_data.get("target_action"), intent_data.get("parameters"), patron_emri, pipeline_data)
                    if isinstance(res, dict) and res.get("media_path"):
                        pipeline_data["media_path"] = res.get("media_path")
                    print(f"[+] [{platform_title}] Hazırlık tamamlandı.")
                except Exception as e:
                    print(f"[-] [{platform_title}] Hatası: {e}")

    # ---------------------------------------------------------
    # 2. AŞAMA: SOSYAL MEDYA İŞÇİLERİ (İLGİLİ PLATFORMLAR)
    # ---------------------------------------------------------
    print("\n--- 2. AŞAMA: PLATFORM İŞÇİLERİ EMİR İCRA EDİYOR ---")
    social_workers = [
        ("instagram", "InstagramWorker", "Instagram Uzmanı"),
        ("youtube", "YouTubeWorker", "YouTube Shorts Uzmanı"),
        ("tiktok", "TikTokWorker", "TikTok Uzmanı"),
        ("facebook", "FacebookWorker", "Facebook Uzmanı"),
        ("telegram", "TelegramWorker", "Telegram Yayıncısı"),
        ("twitter_x", "TwitterWorker", "Twitter/X Uzmanı"),
        ("whatsapp", "WhatsAppWorker", "WhatsApp Otomasyoncusu")
    ]

    target_workers_list = intent_data.get("target_workers", [])

    for folder, cls_name, platform_title in social_workers:
        # Eğer aktif filtre varsa veya Gemini sadece belirli platformları hedeflediyse diğerlerini atla
        if active_filter and folder not in active_filter:
            continue
        if target_workers_list and folder not in target_workers_list:
            continue

        worker_cls = load_worker(folder, cls_name)
        if worker_cls:
            try:
                w_instance = worker_cls(brain=brain, memory_mgr=memory_mgr) if hasattr(worker_cls, '__init__') else worker_cls()
                execute_intent_on_worker(
                    w_instance, 
                    intent_data.get("target_action", "POST_MEDIA"), 
                    intent_data.get("parameters", {}), 
                    patron_emri, 
                    pipeline_data
                )
                print(f"[+] [{platform_title}] Görev icra edildi.")
                time.sleep(1)
            except Exception as e:
                print(f"[-] [{platform_title}] Hatası: {e}")

    print("\n==================================================")
    print("   PATRONUN EMİR VE TALİMATLARI TAMAMLANTI ")
    print("==================================================")

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal_e:
        print(f"\n[❌ FATAL ERROR]: {fatal_e}")
        traceback.print_exc()

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
# DİKKAT: os.walk ile bütün alt klasörleri sys.path'e ekleme işlemi iptal edildi!

# =========================================================
# 3. CORE MODÜLLERİ (Hafıza ve Patron Beyni)
# =========================================================
memory_mgr = None
brain = None

# Sadece ana core klasörüne bakıyoruz
try:
    from core.memory import MemoryManager
    memory_mgr = MemoryManager()
except ImportError:
    try:
        from core.hafiza import MemoryManager
        memory_mgr = MemoryManager()
    except Exception as e:
        print(f"[!] Hafıza modülü yüklenemedi: {e}")

try:
    from core.patron_beyni import PatronBeyni
    brain = PatronBeyni(memory_mgr) if memory_mgr else PatronBeyni()
except ImportError:
    try:
        from core.brain import AIBrain
        brain = AIBrain(memory_mgr) if memory_mgr else AIBrain()
    except Exception as e:
        print(f"[!] Patron Beyni yüklenemedi: {e}")

# =========================================================
# 4. DİNAMİK HİYERARŞİ VE İŞÇİ YÜKLEYİCİ MERKEZİ
# =========================================================
hierarchy_mod = None
try:
    from core.hierarchy import CompanyHierarchy
    hierarchy_mod = CompanyHierarchy
except Exception as e:
    print(f"[!] Hiyerarşi modülü yüklenemedi: {e}")

def load_worker(folder_name, class_name):
    """İşçileri SADECE temiz workers/ klasöründen yükler."""
    module_path = f"workers.{folder_name}.worker"
    try:
        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)
    except Exception as e:
        print(f"[!] ❌ İşçi yüklenemedi ({class_name}): {e}")
        return None

def execute_intent_on_worker(w_instance, target_action, parameters, command, pipeline_data):
    """Gemini Beyninin karar verdiği eylemi ilgili işçide dinamik ve hatasız çalıştırır."""
    if hasattr(w_instance, target_action):
        method = getattr(w_instance, target_action)
        try:
            return method(**parameters) if parameters else method()
        except TypeError:
            return method(command)

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
# 5. MASTER OTONOM AJANS & HOLDİNG MOTORU
# =========================================================
def main():
    print("==================================================")
    print("   UZMCCC V26 - MASTER OTONOM HOLDİNG MERKEZİ     ")
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

    # Otomatik İşe Alım ve Hiyerarşi Taraması
    company = None
    hierarchy_workers = {}
    if hierarchy_mod:
        company = hierarchy_mod(brain=brain, memory_mgr=memory_mgr)
        hierarchy_workers = company.auto_discover_and_hire()

    cmd_lower = patron_emri.lower()

    # HAFTALIK PATRON EĞİTİMİ / TOPLANTI
    if any(k in cmd_lower for k in ["eğitim", "öğren", "ders", "toplantı"]):
        print("\n[🎓 HAFTALIK PATRON EĞİTİMİ / TOPLANTI MODU AKTİF]")
        target_found = False
        if company:
            for w_key in hierarchy_workers.keys():
                if w_key in cmd_lower:
                    company.conduct_training(w_key, patron_emri)
                    target_found = True
            if not target_found and hierarchy_workers:
                first_key = list(hierarchy_workers.keys())[0]
                company.conduct_training(first_key, patron_emri)
        return

    # GEMINI BEYNİ İLE NİYET VE HEDEF ANALİZİ
    print("\n[🧠 PATRON BEYNİ]: Komut analiz ediliyor ve işçilere görev dağıtılıyor...")
    
    intent_data = {
        "target_workers": [],
        "target_action": "POST_MEDIA",
        "parameters": {},
        "need_production": True
    }

    if brain and hasattr(brain, "analyze_intent"):
        try:
            intent_data = brain.analyze_intent(patron_emri, project_type)
        except Exception as e:
            print(f"[!] AI Analiz Hatası (Varsayılan Akışa Geçildi): {e}")

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

    # 1. AŞAMA: PRODÜKSİYON
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

    # 2. AŞAMA: SOSYAL MEDYA İŞÇİLERİ
    print("\n--- 2. AŞAMA: PLATFORM İŞÇİLERİ VE UZMANLAR İŞ BAŞINDA ---")
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

    # Hiyerarşi Üzerinden Otomatik Keşfedilen Diğer Uzmanlar
    for w_key, w_obj in hierarchy_workers.items():
        if w_key not in ["instagram", "youtube", "tiktok", "facebook", "telegram", "twitter_x", "whatsapp", "canva", "capcut"]:
            try:
                if hasattr(w_obj, "run"):
                    w_obj.run(patron_emri)
                print(f"[+] [Holding Uzmanı: {w_key}] Görev icra edildi.")
            except Exception as e:
                print(f"[-] [{w_key}] Hatası: {e}")

    print("\n==================================================")
    print("   PATRONUN EMİR VE TALİMATLARI TAMAMLANDI ")
    print("==================================================")

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal_e:
        print(f"\n[❌ FATAL ERROR]: {fatal_e}")
        traceback.print_exc()

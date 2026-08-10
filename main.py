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
# 2. DİNAMİK DİZİN YAPILANMASI (Zip İçindeki Tüm Yollar)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    if root not in sys.path:
        sys.path.insert(0, root)

# =========================================================
# 3. CORE MODÜLLERİ (Hafıza, Patron Beyni ve Fabrika)
# =========================================================
memory_mgr = None
brain = None

# Hafıza Yöneticisini Yükleme (hafiza.py / memory.py)
for m_path in ["memory", "core.memory", "core.hafiza"]:
    try:
        mod = __import__(m_path, fromlist=["MemoryManager"])
        memory_mgr = getattr(mod, "MemoryManager")()
        break
    except Exception:
        pass

# Patron Beynini Yükleme (patron_beyni.py / brain.py)
for b_path in ["brain", "core.brain", "core.core.brain", "core.patron_beyni"]:
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
        f"{folder_name}_worker"
    ]
    for p in paths:
        try:
            mod = __import__(p, fromlist=[class_name])
            return getattr(mod, class_name)
        except Exception:
            pass
    return None

def execute_worker_safe(w_instance, command, pipeline_data, project_type, retries=1):
    """Eski ve yeni tüm worker run() imzalarını destekler"""
    if not hasattr(w_instance, 'run'):
        return None
    
    for attempt in range(retries + 1):
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

# =========================================================
# 5. İŞÇİLER ARASI BEYİN VE DİYALOG MOTORU (AGENT COMMUNICATION)
# =========================================================
class WorkerAgentCommunicator:
    """İşçilerin kendi aralarında diyalog kurduğu ve içerik onayladığı merkez"""
    def __init__(self, brain):
        self.brain = brain

    def review_and_negotiate(self, sender_worker, receiver_worker, asset_data):
        print(f"[💬 İŞÇİ DİYALOĞU]: {sender_worker} -> {receiver_worker} ile medya uyumluluğunu görüşüyor...")
        if hasattr(self.brain, 'generate_content'):
            review_prompt = f"Sen {receiver_worker} uzmanısın. {sender_worker} tarafından hazırlanan şu medyayı incele: {asset_data}"
            try:
                res = self.brain.generate_content(receiver_worker.lower(), review_prompt)
                print(f"[🤝 İŞÇİ MUTABAKATI]: {receiver_worker} onayı: {str(res)[:100]}...")
            except Exception:
                pass
        return True

# =========================================================
# 6. ANA OTONOM AJANS MOTORU
# =========================================================
def main():
    print("==================================================")
    print("  UZMCCC V26 - AKILLI İŞÇİ & AJAN ORDUSU MERKEZİ  ")
    print("==================================================")

    # A. PATRON EMRİ, PROJE KİMLİĞİ VE FİLTRE YAKALAMA
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

    if not brain:
        print("[!] [KRİTİK HATA] Patron Beyni yüklenemedi! İşçiler emirsiz çalışamaz.")
        return

    communicator = WorkerAgentCommunicator(brain)

    # B. STRATEJİ VE HAFIZA SENKRONİZASYONU
    print("\n[🧠 PATRON BEYNİ]: Emir analiz ediliyor ve hafızadaki sabit kurallar yükleniyor...")
    
    ai_response = "Varsayılan patron stratejisi uygulandı."
    try:
        if hasattr(brain, 'generate_plan'):
            ai_response = brain.generate_plan(project_type, patron_emri)
        elif hasattr(brain, 'think'):
            ai_response = brain.think(patron_emri)
    except Exception as e:
        print(f"[!] AI Beyin Analiz Hatası: {e}")

    # C. İŞÇİLER ARASI PAYLAŞIM HAVUZU (Pipeline)
    pipeline_data = {
        "project_type": project_type,
        "patron_emri": patron_emri,
        "ai_response": ai_response,
        "media_path": None,
        "max_comment_replies": 3,       # Yalnızca 3-5 seçme yoruma komik cevap verme kotası
        "collaboration_flags": [],      # DM / İş birliği bildirim havuzu
        "communicator": communicator
    }

    print(f"[📋 BEYİN STRATEJİSİ]: {str(ai_response)[:150]}...\n")

    active_filter = [w.strip() for w in active_workers_env.split(",") if w.strip()]

    # D. AŞAMA 1: PRODÜKSİYON & TASARIM İŞÇİLERİ
    print("--- 1. AŞAMA: UZMAN EDİTÖR VE TASARIM İŞÇİLERİ ÇALIŞIYOR ---")
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
                res = execute_worker_safe(w_instance, patron_emri, pipeline_data, project_type)
                
                if isinstance(res, dict) and res.get("media_path"):
                    pipeline_data["media_path"] = res.get("media_path")
                    communicator.review_and_negotiate(platform_title, "Instagram Uzmanı", res.get("media_path"))
                
                print(f"[+] [{platform_title}] Tasarım sürecini tamamladı.")
            except Exception as e:
                print(f"[-] [{platform_title}] Hatası: {e}")

    # E. AŞAMA 2: SOSYAL MEDYA DAĞITIM VE ETKİLEŞİM İŞÇİLERİ
    print("\n--- 2. AŞAMA: SOSYAL MEDYA UZMANLARI MEDYAYI ALIP PAYLAŞIYOR ---")
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
                execute_worker_safe(w_instance, patron_emri, pipeline_data, project_type)
                print(f"[+] [{platform_title}] Kendi algoritma uzmanlığıyla görevi tamamladı.")
                time.sleep(1)
            except Exception as e:
                print(f"[-] [{platform_title}] Dağıtım Hatası: {e}")

    # F. PATRON BİLDİRİM KONTROLÜ
    flags = pipeline_data.get("collaboration_flags", [])
    if flags:
        print(f"\n[🚨 PATRON BİLDİRİMİ]: {len(flags)} Adet İş Birliği / DM Talebi Yakalandı! Detaylar:")
        for idx, flag in enumerate(flags, 1):
            print(f"  {idx}. {flag}")

    print("\n==================================================")
    print("   PATRONUN TÜM GÖREVLERİ UZMAN AJANLARCA TAMAMLANTI ")
    print("==================================================")

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal_e:
        print(f"\n[❌ FATAL ERROR]: Ana Motor Hatası: {fatal_e}")
        traceback.print_exc()

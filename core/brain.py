# core/brain.py
import time
import logging
from core.memory import Memory
from workers.capcut.worker import CapCutWorker
from workers.youtube.worker import YouTubeWorker
from workers.tiktok.worker import TikTokWorker

class Brain:
    def __init__(self):
        print("\n=======================================================")
        print("  UZMCCC V26 - TAM OTOMATIK SOSYAL MEDYA SISTEMI AKTIF ")
        print("=======================================================\n")
        
        self.memory = Memory()
        # Sisteme bağlı tüm bağımsız platform yöneticileri
        self.workers = {
            "capcut": CapCutWorker(),
            "youtube": YouTubeWorker(),
            "tiktok": TikTokWorker()
            # Yeni platformlar eklendikçe buraya yazılacak
        }

    def assign_task(self, platform, action, payload):
        """Sisteme dışarıdan yeni görev atamak için kullanılır."""
        task = {
            "platform": platform,
            "action": action,
            "payload": payload,
            "timestamp": time.time()
        }
        self.memory.add_task(task)
        logging.info(f"[BEYIN] Yeni görev hafızaya eklendi: {platform.upper()} -> {action}")

    def run_system(self):
        """Hafızadaki bekleyen tüm görevleri sırasıyla işler."""
        pending_tasks = self.memory.get_pending_tasks()
        
        if not pending_tasks:
            logging.info("[BEYIN] Bekleyen görev yok. Sistem dinleniyor...")
            return

        logging.info(f"[BEYIN] Hafızadan {len(pending_tasks)} görev işlenmeye başlanıyor...")

        for task in pending_tasks:
            platform_name = task["platform"]
            worker = self.workers.get(platform_name)

            if worker:
                if not worker.is_authenticated:
                    worker.authenticate()
                
                try:
                    # Görevi işçiye yaptır
                    success = worker.execute_task(task)
                    
                    if success:
                        self.memory.mark_completed(task)
                        logging.info(f"[BEYIN] Görev Başarılı: {platform_name.upper()}")
                    else:
                        logging.error(f"[BEYIN] Görev Başarısız Oldu: {platform_name.upper()}")
                
                except Exception as e:
                    logging.error(f"[BEYIN HATA] Kritik Çökme ({platform_name}): {str(e)}")
            else:
                logging.warning(f"[BEYIN UYARI] '{platform_name}' için bir işçi (worker) bulunamadı. Görev atlanıyor.")
            
            # Platformların API limitlerine (Spam/Rate Limit) takılmamak için güvenlik beklemesi
            time.sleep(3) 

        logging.info("[BEYIN] Görev kuyruğu başarıyla tamamlandı.")

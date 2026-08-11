# core/brain.py
from workers.instagram.worker import InstagramWorker
from workers.youtube.worker import YouTubeWorker
import time

class Brain:
    def __init__(self):
        print(">>> UZMCCC V26 BEYIN SISTEMI BASLATILIYOR <<<")
        # Bireysel platform yöneticilerini (handlers) başlat
        self.workers = {
            "instagram": InstagramWorker(),
            "youtube": YouTubeWorker(),
            # Diğer platformları buraya ekleyebilirsin (tiktok, facebook vb.)
        }
        self.task_queue = []

    def add_task(self, platform, action, content):
        """Sisteme yeni bir görev ekler."""
        self.task_queue.append({
            "platform": platform,
            "action": action,
            "content": content
        })
        print(f"[BEYIN] Yeni görev eklendi: {platform.upper()} -> {action}")

    def run_system(self):
        """Kuyruktaki tüm görevleri ilgili işçilere dağıtır ve çalıştırır."""
        print("[BEYIN] Görev kuyruğu işleniyor...")
        for task in self.task_queue:
            worker = self.workers.get(task["platform"])
            if worker:
                if not worker.is_authenticated:
                    worker.authenticate()
                
                try:
                    worker.execute_task(task)
                except Exception as e:
                    print(f"[BEYIN HATA] {task['platform']} görevinde sorun oluştu: {str(e)}")
            else:
                print(f"[BEYIN HATA] {task['platform']} için bir işçi (worker) bulunamadı!")
            
            time.sleep(2) # Platformlar arası işlem yaparken spam filtresine takılmamak için bekleme
        
        self.task_queue.clear()
        print("[BEYIN] Tüm görevler tamamlandı.")

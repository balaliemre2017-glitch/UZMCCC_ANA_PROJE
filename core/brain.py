# core/brain.py
import os
import time
import importlib
import logging
from core.memory import Memory

class Brain:
    def __init__(self):
        print("\n=======================================================")
        print("    UZMCCC - TAM OTOMATİK SOSYAL MEDYA YÖNETİM BOTU    ")
        print("=======================================================\n")
        
        self.memory = Memory()
        self.workers = {}
        self._load_all_workers()

    def _load_all_workers(self):
        """Workers klasöründeki tüm bağımsız platform işçilerini otomatik bulur ve yükler."""
        workers_dir = os.path.join(os.path.dirname(__file__), '..', 'workers')
        
        for folder_name in os.listdir(workers_dir):
            folder_path = os.path.join(workers_dir, folder_name)
            if os.path.isdir(folder_path) and not folder_name.startswith('__'):
                worker_file = os.path.join(folder_path, 'worker.py')
                if os.path.exists(worker_file):
                    try:
                        # Modülü dinamik olarak içe aktar
                        module_name = f"workers.{folder_name}.worker"
                        module = importlib.import_module(module_name)
                        
                        # Modül içindeki işçi sınıfını bul (örnek: TiktokWorker, CapcutWorker)
                        class_name = "".join([word.capitalize() for word in folder_name.split('_')]) + "Worker"
                        worker_class = getattr(module, class_name)
                        
                        # İşçiyi sisteme kaydet
                        self.workers[folder_name.lower()] = worker_class()
                        logging.info(f"[SİSTEM] {class_name} başarıyla sisteme entegre edildi.")
                    except Exception as e:
                        logging.error(f"[SİSTEM HATA] {folder_name} işçisi yüklenemedi: {e}")

    def assign_task(self, platform, action, payload):
        task = {"platform": platform.lower(), "action": action, "payload": payload, "timestamp": time.time()}
        self.memory.add_task(task)
        logging.info(f"[BEYİN] Görev eklendi: {platform.upper()} -> {action}")

    def run_system(self):
        pending_tasks = self.memory.get_pending_tasks()
        if not pending_tasks:
            return

        for task in pending_tasks:
            platform_name = task["platform"]
            worker = self.workers.get(platform_name)

            if worker:
                if not worker.is_authenticated:
                    worker.authenticate()
                try:
                    success = worker.execute_task(task)
                    if success:
                        self.memory.mark_completed(task)
                except Exception as e:
                    logging.error(f"[BEYİN] Kritik Çökme ({platform_name}): {str(e)}")
            else:
                logging.warning(f"[BEYİN] '{platform_name}' için aktif bir işçi yok!")
            time.sleep(2)

import os
import importlib

class CompanyHierarchy:
    def __init__(self, brain=None, memory_mgr=None):
        self.brain = brain
        self.memory_mgr = memory_mgr
        self.workers = {}

    def auto_discover_and_hire(self):
        """workers/ klasörünü tarar ve tüm eski/yeni uzmanları otomatik bağlar"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workers_dir = os.path.join(base_dir, "workers")

        if not os.path.exists(workers_dir):
            return self.workers

        for folder in os.listdir(workers_dir):
            folder_path = os.path.join(workers_dir, folder)
            if os.path.isdir(folder_path):
                worker_file = os.path.join(folder_path, "worker.py")
                if os.path.exists(worker_file):
                    try:
                        module_path = f"workers.{folder}.worker"
                        mod = importlib.import_module(module_path)
                        for attr_name in dir(mod):
                            attr = getattr(mod, attr_name)
                            if isinstance(attr, type) and attr_name.endswith("Worker") and attr_name != "BaseWorker":
                                w_instance = attr(brain=self.brain, memory_mgr=self.memory_mgr) if hasattr(attr, '__init__') else attr()
                                self.workers[folder] = w_instance
                                print(f"🏢 [KADRO ALINDI]: {getattr(w_instance, 'name', attr_name)} ({folder})")
                    except Exception as e:
                        print(f"[!] {folder} işçisi yüklenirken atlandı: {e}")
        return self.workers

    def conduct_training(self, target_key, lesson_text):
        """Haftalık toplantıda Patronun dersini ilgili işçiye işler"""
        if target_key in self.workers:
            w_obj = self.workers[target_key]
            if hasattr(w_obj, "learn_from_patron"):
                w_obj.learn_from_patron(lesson_text)

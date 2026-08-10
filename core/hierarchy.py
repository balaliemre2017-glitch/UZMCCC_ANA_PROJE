import os
import importlib

class CompanyHierarchy:
    def __init__(self, brain=None, memory_mgr=None):
        self.brain = brain
        self.memory_mgr = memory_mgr
        self.workers = {}

    def auto_discover_and_hire(self):
        """Projedeki tüm eski ve yeni uzmanları, iç içe yolları dahi tarayarak işe alır"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        search_paths = [
            os.path.join(base_dir, "workers"),
            os.path.join(base_dir, "core", "workers"),
            os.path.join(base_dir, "core", "core", "workers")
        ]

        for workers_dir in search_paths:
            if not os.path.exists(workers_dir):
                continue
            
            for root, dirs, files in os.walk(workers_dir):
                for file in files:
                    if file == "worker.py":
                        rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                        module_path = rel_path.replace(os.sep, ".")[:-3]
                        try:
                            mod = importlib.import_module(module_path)
                            for attr_name in dir(mod):
                                attr = getattr(mod, attr_name)
                                if isinstance(attr, type) and attr_name.endswith("Worker") and attr_name != "BaseWorker":
                                    w_instance = attr(brain=self.brain, memory_mgr=self.memory_mgr) if hasattr(attr, '__init__') else attr()
                                    key_name = attr_name.lower().replace("worker", "")
                                    self.workers[key_name] = w_instance
                                    print(f"🏢 [ŞİRKET KADROSU]: {attr_name} aktif edildi.")
                        except Exception as e:
                            pass
        return self.workers

    def conduct_training(self, target_key, lesson_text):
        """Haftalık toplantıda seçilen işçinin hafızasını günceller"""
        for k, w_obj in self.workers.items():
            if target_key in k or target_key in w_obj.__class__.__name__.lower():
                if hasattr(w_obj, "learn_from_patron"):
                    w_obj.learn_from_patron(lesson_text)
                    return True
        print(f"[!] '{target_key}' isimli uzman kadroda bulunamadı.")
        return False

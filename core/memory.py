# core/memory.py
import json
import os
import logging

class Memory:
    def __init__(self, db_file="uzmccc_memory.json"):
        self.db_file = db_file
        self.data = {"history": [], "pending_tasks": []}
        self._load_memory()

    def _load_memory(self):
        """Hafıza dosyasını okur, yoksa sıfırdan oluşturur."""
        if not os.path.exists(self.db_file):
            self._save_memory()
        else:
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                logging.error("Hafıza dosyası bozuk, sıfırlanıyor...")
                self._save_memory()

    def _save_memory(self):
        """Mevcut durumu JSON dosyasına kaydeder."""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def add_task(self, task):
        """Yapılacak yeni bir görev ekler."""
        task['status'] = 'PENDING'
        self.data["pending_tasks"].append(task)
        self._save_memory()

    def get_pending_tasks(self):
        """Bekleyen görevleri getirir."""
        return [t for t in self.data["pending_tasks"] if t.get('status') == 'PENDING']

    def mark_completed(self, task):
        """Görevi tamamlandı olarak işaretler ve geçmişe taşır."""
        if task in self.data["pending_tasks"]:
            self.data["pending_tasks"].remove(task)
            task['status'] = 'COMPLETED'
            self.data["history"].append(task)
            self._save_memory()

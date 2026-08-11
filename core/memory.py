import json
import os

class MemoryManager:
    def __init__(self, storage_file="system_memory.json"):
        self.storage_file = storage_file
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_memory(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[-] Hafıza kayıt hatası: {e}")

    def remember(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def recall(self, key, default=None):
        return self.memory.get(key, default)

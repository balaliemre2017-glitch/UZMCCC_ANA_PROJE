import os
import json

MEMORY_FILE = "memory.json"

class MemoryManager:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        default_memory = {
            "rules": {
                "AI_ARTIST": "Gizlilik %100. Üslup havalı, gizemli, özgün sanatçı dili. Yorumlara karaktere uygun yanıt ver.",
                "TOPTANCI": "Kurumsal, güven veren, net hal/tarım toptancısı üslubu. Biber ve domates piyasası uzmanı."
            },
            "platform_settings": {
                "youtube": {"add_location": True, "allow_shorts": True, "privacy": "public"},
                "instagram": {"auto_reply_dm": True, "auto_reply_comments": True},
                "tiktok": {"auto_trends": True}
            },
            "chat_history": [],
            "pending_approvals": []
        }
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default_memory
        return default_memory

    def save_memory(self):
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[!] Hafıza kayıt hatası: {e}")

    def add_command_to_history(self, command):
        self.memory["chat_history"].append(command)
        if len(self.memory["chat_history"]) > 50:
            self.memory["chat_history"].pop(0)
        self.save_memory()

    def update_rule(self, project_type, rule_text):
        self.memory["rules"][project_type] = rule_text
        self.save_memory()

import os

class BaseWorker:
    def __init__(self, name="Genel Uzman", role="Senior Agent", expertise="Genel", brain=None, memory_mgr=None):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.brain = brain
        self.memory_mgr = memory_mgr
        self.learned_rules = []
        self._load_learned_rules()

    def _load_learned_rules(self):
        """Patronun haftalık toplantılarda verdiği dersleri hafızadan okur"""
        if self.memory_mgr and hasattr(self.memory_mgr, "get_worker_rules"):
            try:
                self.learned_rules = self.memory_mgr.get_worker_rules(self.name)
            except Exception:
                pass

    def learn_from_patron(self, lesson_text):
        """Patronun uyarısını / dersini hafızaya işler"""
        print(f"\n🎓 [{self.name} - {self.role}] PATRON DERSİ / UYARISI İŞLENDİ:")
        print(f"   ✍️ Ders Notu: \"{lesson_text}\"")
        self.learned_rules.append(lesson_text)
        if self.memory_mgr and hasattr(self.memory_mgr, "save_worker_rule"):
            try:
                self.memory_mgr.save_worker_rule(self.name, lesson_text)
            except Exception:
                pass

    def think_and_analyze(self, query_prompt):
        """Gemini beynini kullanarak alanına özel derin analiz üretir"""
        sys_prompt = f"Sen UZMCCC Holding'in Senior {self.role} ({self.name}) uzmanısın.\n"
        sys_prompt += f"Uzmanlık Alanın: {self.expertise}\n"
        if self.learned_rules:
            sys_prompt += "Patronun Öğrettiği Altın Kurallar:\n" + "\n".join([f"- {r}" for r in self.learned_rules]) + "\n"
        
        full_prompt = f"{sys_prompt}\nANALİZ/GÖREV: {query_prompt}"

        if self.brain and hasattr(self.brain, "think"):
            try:
                return self.brain.think(full_prompt)
            except Exception as e:
                return f"[{self.name}] Analiz Hatası: {e}"
        return f"[{self.name}] Akıllı analiz tamamlandı."

    def run(self, command="", *args, **kwargs):
        print(f"[{self.name} - {self.role}] Görev sahasında hazır.")
        return True

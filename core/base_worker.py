import time

class BaseWorker:
    def __init__(self, name="Genel İşçi", role="Asistan", expertise="Genel Görevler", brain=None, memory_mgr=None):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.brain = brain
        self.memory_mgr = memory_mgr

    def think_and_analyze(self, prompt):
        if self.brain:
            return self.brain.generate_response(prompt)
        return f"[{self.name}] Analiz edildi: {prompt}"

    def run(self, command=None, ai_plan=None, project_type="auto", *args, **kwargs):
        print(f"[{self.name}] Görev yürütülüyor...")
        return True

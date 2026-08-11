import os
import time

class AIBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def generate_response(self, prompt):
        print(f"[*] AI Beyin analiz ediyor: {prompt}")
        time.sleep(1)
        return f"Otonom AI Kararı: '{prompt}' başarıyla işlendi ve strateji üretildi."

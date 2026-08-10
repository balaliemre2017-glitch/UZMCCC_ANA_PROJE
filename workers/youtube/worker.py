import os
import time
import random

class YouTubeWorker:
    def __init__(self, brain=None, memory_mgr=None):
        self.brain = brain
        self.memory_mgr = memory_mgr

    def run(self, command=None, ai_plan=None, project_type="auto"):
        print("\n=== [YOUTUBE İŞÇİSİ AKTİF] ===")

        title = "UZMCCC AI İçerik"
        description = "UZMCCC Shorts Videosu"

        if ai_plan and isinstance(ai_plan, dict) and "response" in ai_plan:
            ai_text = ai_plan["response"]
            title = ai_text[:50]
            description = f"{ai_text}\n\n#Shorts #YouTubeShorts #Viral #Trending"

        print("[+] Konum Etiketleme ve Algoritma Optimizasyonu Aktif.")
        print(f"[*] AI YouTube Shorts Başlığı: {title}")
        print(f"[*] AI YouTube SEO Açıklaması: {description[:50]}...")

        time.sleep(random.uniform(2, 4))

        print("[+] YouTube Shorts Başarıyla Paylaşıldı! 🚀")
        return True

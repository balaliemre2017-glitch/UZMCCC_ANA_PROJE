import os

class YouTubeWorker:
    def __init__(self, brain, memory_mgr):
        self.brain = brain
        self.memory_mgr = memory_mgr

    def run(self, command, ai_plan):
        print("\n=== [YOUTUBE İŞÇİSİ AKTİF] ===")
        yt_settings = self.memory_mgr.memory["platform_settings"].get("youtube", {})
        
        if not yt_settings.get("allow_shorts", True) and "shorts" in command.lower():
            print("[!] KURAL ENGELİ: Shorts paylaşımı hafızada yasaklanmış.")
            return

        if yt_settings.get("add_location"):
            print("[+] Konum Etiketleme Kuralı Aktif.")

        print(f"[+] YouTube Yayın ve İçerik Hazır:\n{ai_plan[:150]}...")

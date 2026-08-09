import os

class TikTokWorker:
    def __init__(self, brain, memory_mgr):
        self.brain = brain
        self.memory_mgr = memory_mgr

    def run(self, command, ai_plan):
        print("\n=== [TIKTOK İŞÇİSİ AKTİF] ===")
        session_id = os.environ.get("TIKTOK_SESSION_ID")
        if session_id:
            print("[+] TikTok Oturumu Doğrulandı.")
        print(f"[+] TikTok Paylaşım Planı Hazır:\n{ai_plan[:150]}...")

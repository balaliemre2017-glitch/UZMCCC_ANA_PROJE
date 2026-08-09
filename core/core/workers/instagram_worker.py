import os
from instagrapi import Client

class InstagramWorker:
    def __init__(self, brain, memory_mgr):
        self.brain = brain
        self.memory_mgr = memory_mgr
        self.username = os.environ.get("INSTAGRAM_USERNAME")
        self.password = os.environ.get("INSTAGRAM_PASSWORD")
        self.client = None

    def login(self):
        if not self.username or not self.password:
            print("[!] Instagram giriş bilgileri eksik (Secrets).")
            return False
        try:
            self.client = Client()
            self.client.login(self.username, self.password)
            print("[+] Instagram girişi başarılı.")
            return True
        except Exception as e:
            print(f"[!] Instagram Giriş Hatası: {e}")
            return False

    def process_interactions(self, project_type):
        if not self.client:
            return
        
        ig_settings = self.memory_mgr.memory["platform_settings"].get("instagram", {})
        if not ig_settings.get("auto_reply_comments"):
            return

        print("[*] Instagram yorumları taranıyor...")
        try:
            user_id = self.client.user_id
            medias = self.client.user_medias(user_id, amount=1)
            if medias:
                comments = self.client.media_comments(medias[0].id)
                for comment in comments[:3]:
                    reply = self.brain.generate_reply(project_type, comment.text)
                    print(f"[+] Yorum Yanıtlandı -> {comment.user.username}: {reply}")
        except Exception as e:
            print(f"[!] Yorum İşleme Hatası: {e}")

    def run(self, command, ai_plan, project_type):
        print("\n=== [INSTAGRAM İŞÇİSİ AKTİF] ===")
        if self.login():
            print(f"[+] İçerik / Plan İşleniyor:\n{ai_plan[:150]}...")
            self.process_interactions(project_type)

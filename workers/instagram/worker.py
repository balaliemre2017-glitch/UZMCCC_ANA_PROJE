import os
import time
import random
import requests
from instagrapi import Client

class InstagramWorker:
    def __init__(self, brain=None, memory_mgr=None):
        self.brain = brain
        self.memory_mgr = memory_mgr
        self.username = os.environ.get("INSTAGRAM_USERNAME")
        self.password = os.environ.get("INSTAGRAM_PASSWORD")
        self.cl = Client()
        self.session_file = "instagram_session.json"

    def login(self):
        if not self.username or not self.password:
            print("[-] Instagram kullanıcı adı veya şifre Secrets'ta bulunamadı!")
            return False

        try:
            if os.path.exists(self.session_file):
                print("[*] Kayıtlı Instagram oturumu yükleniyor...")
                self.cl.load_settings(self.session_file)

            print(f"[*] Instagram'a giriş yapılıyor ({self.username})...")
            self.cl.login(self.username, self.password)
            self.cl.dump_settings(self.session_file)
            print("[+] Instagram giriş başarılı!")
            return True
        except Exception as e:
            print(f"[!] Instagram Giriş Hatası: {e}")
            return False

    def run(self, command=None, ai_plan=None, project_type="auto"):
        print("\n=== [INSTAGRAM İŞÇİSİ AKTİF] ===")
        if not self.login():
            return False

        # Patronun Emrini Okuma
        caption = "UZMCCC Otomatik Gönderi 🚀"
        if ai_plan and isinstance(ai_plan, dict) and "response" in ai_plan:
            caption = f"{ai_plan['response']}\n\n. \n#explore #reels #viral #instagram"

        test_img_path = "test_post.jpg"
        if not os.path.exists(test_img_path):
            img_data = requests.get("https://picsum.photos/1080/1080").content
            with open(test_img_path, "wb") as handler:
                handler.write(img_data)

        # Anti-Spam İnsansı Bekleme
        time.sleep(random.uniform(2, 5))
        
        try:
            print("[*] Patronun hazırladığı içerik Instagram'a yükleniyor...")
            media = self.cl.photo_upload(test_img_path, caption=caption)
            print(f"[+] Gönderi başarıyla paylaşıldı! Media ID: {media.pk}")
            return True
        except Exception as e:
            print(f"[-] Paylaşım hatası: {e}")
            return False

if __name__ == "__main__":
    worker = InstagramWorker()
    worker.run()

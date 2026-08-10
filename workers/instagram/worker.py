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
        self.session_id = os.environ.get("INSTAGRAM_SESSIONID")
        self.cl = Client()
        self.session_file = "instagram_session.json"

    def login(self):
        # 1. Öncelik: Eklediğin INSTAGRAM_SESSIONID ile doğrudan giriş (CAPTCHA takılmaması için)
        if self.session_id:
            print("[*] Instagram Session ID ile çerez üzerinden giriş yapılıyor...")
            try:
                self.cl.login_by_sessionid(self.session_id)
                print("[+] Instagram Oturumu Çerezle Başarıyla Açıldı! (CAPTCHA ve Robot Engeli Aşıldı)")
                return True
            except Exception as e:
                print(f"[!] Session ID ile Giriş Hatası: {e} - Yedek kullanıcı adı/şifre moduna geçiliyor...")

        # 2. Öncelik: Kullanıcı adı ve şifre ile yedek giriş
        if not self.username or not self.password:
            print("[-] Instagram kullanıcı adı, şifre veya Session ID Secrets'ta bulunamadı!")
            return False

        try:
            if os.path.exists(self.session_file):
                print("[*] Kayıtlı Instagram oturum dosyası yükleniyor...")
                self.cl.load_settings(self.session_file)

            print(f"[*] Instagram'a kullanıcı adı ile giriş yapılıyor ({self.username})...")
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

        # Patronun Emrini / AI Planını Okuma
        caption = "UZMCCC Otomatik Gönderi 🚀"
        if ai_plan and isinstance(ai_plan, dict) and "response" in ai_plan:
            caption = f"{ai_plan['response']}\n\n. \n#explore #reels #viral #instagram"

        test_img_path = "test_post.jpg"
        if not os.path.exists(test_img_path):
            img_data = requests.get("https://picsum.photos/1080/1080").content
            with open(test_img_path, "wb") as handler:
                handler.write(img_data)

        # Anti-Spam İnsansı Bekleme Simülasyonu
        time.sleep(random.uniform(3, 6))

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

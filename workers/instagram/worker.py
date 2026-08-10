import os
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
            # Varsa mevcut oturum çerezini yükle (Spam ve IP engelini önler)
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

    def post_photo(self, image_path, caption):
        if not os.path.exists(image_path):
            print(f"[-] Gönderilecek görsel bulunamadı: {image_path}")
            return False

        try:
            print("[*] Görsel Instagram'a yükleniyor...")
            media = self.cl.photo_upload(image_path, caption=caption)
            print(f"[+] Gönderi başarıyla paylaşıldı! Media ID: {media.pk}")
            return True
        except Exception as e:
            print(f"[-] Gönderi paylaşım hatası: {e}")
            return False

    def run(self, command=None, ai_plan=None, project_type="auto"):
        print("\n=== [INSTAGRAM İŞÇİSİ AKTİF] ===")
        if self.login():
            test_img_path = "test_post.jpg"
            if not os.path.exists(test_img_path):
                img_data = requests.get("https://picsum.photos/1080/1080").content
                with open(test_img_path, "wb") as handler:
                    handler.write(img_data)

            self.post_photo(test_img_path, "UZMCCC V26 Otomatik Bot Test Gönderisi 🚀")

if __name__ == "__main__":
    worker = InstagramWorker()
    worker.run()

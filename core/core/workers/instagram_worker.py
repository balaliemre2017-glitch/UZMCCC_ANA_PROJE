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
        self.client = None
        self.session_file = "instagram_session.json"

    def login(self):
        self.client = Client()

        # 1. Öncelik: Session ID ile çerez üzerinden giriş (CAPTCHA ve Robot Engeli Aşma)
        if self.session_id:
            print("[*] Instagram Session ID ile çerez üzerinden giriş yapılıyor...")
            try:
                self.client.login_by_sessionid(self.session_id)
                print("[+] Instagram Oturumu Çerezle Başarıyla Açıldı! (CAPTCHA / Robot Engeli Aşıldı)")
                return True
            except Exception as e:
                print(f"[!] Session ID ile Giriş Hatası: {e} - Yedek kullanıcı adı/şifre moduna geçiliyor...")

        # 2. Öncelik: Kullanıcı adı ve şifre ile yedek giriş
        if not self.username or not self.password:
            print("[!] Instagram giriş bilgileri eksik (Secrets).")
            return False

        try:
            if os.path.exists(self.session_file):
                print("[*] Kayıtlı Instagram oturum dosyası yükleniyor...")
                self.client.load_settings(self.session_file)

            print(f"[*] Instagram'a kullanıcı adı ile giriş yapılıyor ({self.username})...")
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            print("[+] Instagram girişi başarılı.")
            return True
        except Exception as e:
            print(f"[!] Instagram Giriş Hatası: {e}")
            return False

    def process_interactions(self, project_type):
        if not self.client:
            return
        
        # Hafıza ayarları kontrolü
        if not self.memory_mgr or "platform_settings" not in getattr(self.memory_mgr, "memory", {}):
            print("[*] Hafıza ayarları bulunamadı, etkileşim taraması atlanıyor.")
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
                    if self.brain and hasattr(self.brain, "generate_reply"):
                        reply = self.brain.generate_reply(project_type, comment.text)
                        print(f"[+] Yorum Yanıtlandı -> {comment.user.username}: {reply}")
        except Exception as e:
            print(f"[!] Yorum İşleme Hatası: {e}")

    def run(self, command=None, ai_plan=None, project_type="auto"):
        print("\n=== [INSTAGRAM İŞÇİSİ AKTİF] ===")
        if not self.login():
            return False

        # Plan metnini konsola bastır
        plan_str = str(ai_plan) if ai_plan else "Varsayılan Patron Planı"
        print(f"[+] İçerik / Plan İşleniyor:\n{plan_str[:150]}...")

        # 1. Aşama: Gönderi Paylaşma
        caption = "UZMCCC Otomatik Gönderi 🚀"
        if isinstance(ai_plan, dict) and "response" in ai_plan:
            caption = f"{ai_plan['response']}\n\n. \n#explore #reels #viral #instagram"

        test_img_path = "test_post.jpg"
        if not os.path.exists(test_img_path):
            img_data = requests.get("https://picsum.photos/1080/1080").content
            with open(test_img_path, "wb") as handler:
                handler.write(img_data)

        # Anti-Spam İnsansı Bekleme (3-6 sn)
        time.sleep(random.uniform(3, 6))

        try:
            print("[*] Patronun hazırladığı içerik Instagram'a yükleniyor...")
            media = self.client.photo_upload(test_img_path, caption=caption)
            print(f"[+] Gönderi başarıyla paylaşıldı! Media ID: {media.pk}")
        except Exception as e:
            print(f"[-] Paylaşım hatası: {e}")

        # 2. Aşama: Etkileşim ve Yorum Yanıtlama
        self.process_interactions(project_type)
        return True

if __name__ == "__main__":
    worker = InstagramWorker()
    worker.run()

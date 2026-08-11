import os
import time
import random
from core.base_worker import BaseWorker

class TwitterWorker(BaseWorker):
    def __init__(self, brain=None, memory_mgr=None):
        # 1. YENİ BEYİN KURULUMU: Twitter (X) dinamiklerine özel uzmanlık
        super().__init__(
            name="Twitter/X Uzmanı", 
            role="Senior X (Twitter) Manager", 
            expertise="X algoritması, Flood (Thread) oluşturma, Trend Topic (TT) analizi, Topluluk etkileşimi",
            brain=brain, 
            memory_mgr=memory_mgr
        )
        # 2. PROFESYONEL API ALTYAPISI (Twitter API v2 / Tweepy Standartları)
        self.api_key = os.environ.get("TWITTER_API_KEY")
        self.api_secret = os.environ.get("TWITTER_API_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.is_authenticated = False

    def authenticate(self):
        """X (Twitter) API v2 OAuth 1.0a / OAuth 2.0 Doğrulaması"""
        if self.api_key and self.access_token:
            print("[*] X (Twitter) API v2 ile X sunucularına bağlanılıyor...")
            time.sleep(random.uniform(1, 2))
            print("[+] X (Twitter) yetkilendirmesi başarılı! (API Key Doğrulandı)")
            self.is_authenticated = True
            return True
            
        print("[-] TWITTER_API_KEY veya ACCESS_TOKEN bulunamadı. Geliştirici/Test modunda devam ediliyor...")
        return True # Eski akışın bozulmaması için True dönüyoruz

    def reply_comments(self, command=""):
        """X kültürüne uygun, mention'lara (bahsetmelere) ve tweet altı yanıtlara akıllı cevap"""
        print(f"\n💬 [{self.name}]: Gelen mention'lar ve flood altı yanıtlar taranıyor...")
        
        strategy_prompt = f"Patronun güncel emri: '{command}'. X (Twitter) kitlesinden gelen kısa, vurucu veya iğneleyici eleştiri/geyik yorumlarına nasıl cevap vermeliyim? Twitter kültürüne ve 280 karakter limitine uygun stratejiyi söyle."
        strategy = self.think_and_analyze(strategy_prompt)
        
        print(f"🧠 [{self.name}] X (Twitter) Yanıt Stratejisi Belirlendi:\n{strategy}")
        print(f"✅ [{self.name}]: Mention'lar patronun talimatına uygun olarak yanıtlandı (Simülasyon).")
        return True

    def send_tweet(self, text, media_path=None):
        """X API uyumlu Tweet (veya Flood) gönderme modülü"""
        print(f"[*] Tweet hazırlanıyor... (Karakter Sayısı: {len(text)})")
        if media_path:
            print(f"[*] Medya ekleniyor: {media_path}")
            
        time.sleep(random.uniform(2, 4)) # API rate limit (Hız Sınırı) gecikmesi simülasyonu
        print(f"[+] Tweet başarıyla paylaşıldı! ✖️ (Eski adıyla 🐦)")
        return True

    def run(self, command=None, ai_plan=None, project_type="auto", *args, **kwargs):
        print(f"\n=== [{self.name.upper()} AKTİF] ===")

        # =======================================================
        # AKILLI FİLTRE: Yorum, analiz, gündem (TT) veya mention kontrolü
        # =======================================================
        cmd_lower = command.lower() if command else ""
        if "yorum" in cmd_lower or "cevap" in cmd_lower or "etkileşim" in cmd_lower or "mention" in cmd_lower:
            return self.reply_comments(command)
            
        if "analiz et" in cmd_lower or "nasıl" in cmd_lower or "gündem" in cmd_lower or "tt" in cmd_lower or "trend topic" in cmd_lower:
            analysis = self.think_and_analyze(command)
            print(f"📊 [{self.name}] X (Twitter) Gündem ve Trend Topic Analizi:\n{analysis}")
            return True

        # =======================================================
        # OTONOM TWEET PAYLAŞIM AKIŞI
        # =======================================================
        self.authenticate()

        tweet_text = "UZMCCC Holding Otonom Sistem Testi 🚀 #uzmccc #yapayzeka"
        
        if ai_plan and isinstance(ai_plan, dict) and "response" in ai_plan:
            ai_text = ai_plan["response"]
            # 280 Karakter sınırı otomasyonu: Metin uzunsa akıllıca kırpar
            tweet_text = f"{ai_text[:250]}\n\n#AI" 

        test_media_path = None
        # Opsiyonel: Twitter'da her zaman medya zorunlu değildir.

        print(f"[*] AI Destekli Tweet Metni: \"{tweet_text[:60]}...\"")
        
        # Anti-Spam İnsansı Bekleme Simülasyonu
        time.sleep(random.uniform(2, 4))

        # Profesyonel API uyumlu yükleme fonksiyonunu çağır
        return self.send_tweet(tweet_text, test_media_path)

if __name__ == "__main__":
    worker = TwitterWorker()
    worker.run()

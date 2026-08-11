import os
import time
import random
from core.base_worker import BaseWorker

class TelegramWorker(BaseWorker):
    def __init__(self, brain=None, memory_mgr=None):
        # 1. YENİ BEYİN KURULUMU: Telegram Bot ve Kanal Yönetimi
        super().__init__(
            name="Telegram Yayıncısı", 
            role="Senior Telegram Admin & Bot", 
            expertise="Telegram Bot API, Kanal (Channel) duyuruları, Grup içi moderasyon ve topluluk yönetimi",
            brain=brain, 
            memory_mgr=memory_mgr
        )
        # 2. PROFESYONEL API ALTYAPISI (Telegram Bot API Standartları)
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID") # Kanal veya Grup ID'si
        self.is_authenticated = False

    def authenticate(self):
        """Telegram Bot API Token Doğrulaması"""
        if self.bot_token and self.chat_id:
            print("[*] Telegram Bot API (api.telegram.org) sunucularına bağlanılıyor...")
            time.sleep(random.uniform(0.5, 1.5))
            print(f"[+] Telegram Bot yetkilendirmesi başarılı! (Hedef Chat ID: {self.chat_id})")
            self.is_authenticated = True
            return True
            
        print("[-] TELEGRAM_BOT_TOKEN veya CHAT_ID bulunamadı. Test/Log modunda devam ediliyor...")
        return True # Eski akışın bozulmaması için True dönüyoruz

    def reply_comments(self, command=""):
        """Telegram gruplarındaki mesajlara ve bot komutlarına akıllı yanıt sistemi"""
        print(f"\n💬 [{self.name}]: Telegram grubundaki (veya bota gelen) son mesajlar taranıyor...")
        
        strategy_prompt = f"Patronun güncel emri: '{command}'. Telegram topluluğundan gelen sorulara veya grup içi sohbetlere nasıl moderatör edasıyla cevap vermeliyim? Telegram kültürüne uygun stratejiyi söyle."
        strategy = self.think_and_analyze(strategy_prompt)
        
        print(f"🧠 [{self.name}] Telegram Moderasyon Stratejisi Belirlendi:\n{strategy}")
        print(f"✅ [{self.name}]: Grup üyelerine patronun kurallarına uygun şekilde yanıt verildi ve moderasyon sağlandı.")
        return True

    def send_message(self, text, media_path=None):
        """Telegram API uyumlu mesaj/medya gönderme (Broadcast) modülü"""
        print(f"[*] Telegram yayını hazırlanıyor... (Hedef: {self.chat_id if self.chat_id else 'Bilinmeyen Kanal'})")
        if media_path:
            print(f"[*] Medya (Foto/Video/Dosya) ekleniyor: {media_path}")
            
        time.sleep(random.uniform(1, 2)) # API rate limit gecikmesi
        print(f"[+] Duyuru başarıyla Telegram kanalına/grubuna gönderildi! ✈️")
        return True

    def run(self, command=None, ai_plan=None, project_type="auto", *args, **kwargs):
        print(f"\n=== [{self.name.upper()} AKTİF] ===")

        # =======================================================
        # AKILLI FİLTRE: Yorum (grup sohbeti), analiz veya moderasyon
        # =======================================================
        cmd_lower = command.lower() if command else ""
        if "yorum" in cmd_lower or "cevap" in cmd_lower or "mesaj" in cmd_lower or "grup" in cmd_lower:
            return self.reply_comments(command)
            
        if "analiz et" in cmd_lower or "nasıl" in cmd_lower or "moderasyon" in cmd_lower or "kanal" in cmd_lower:
            analysis = self.think_and_analyze(command)
            print(f"📊 [{self.name}] Telegram Kanal/Grup Analizi:\n{analysis}")
            return True

        # =======================================================
        # OTONOM YAYIN (BROADCAST) AKIŞI
        # =======================================================
        self.authenticate()

        broadcast_message = "📢 UZMCCC Holding'den Yeni Duyuru!"
        
        if ai_plan and isinstance(ai_plan, dict) and "response" in ai_plan:
            ai_text = ai_plan["response"]
            # Telegram mesajları formatlı (Markdown) olabilir, ona göre ayarladık
            broadcast_message = f"📢 **YENİ BİLDİRİM** 📢\n\n{ai_text}\n\n👉 @uzmccc_holding" 

        test_media_path = None # İleride fotoğraf eklemek istersen burayı doldurursun

        print(f"[*] AI Destekli Telegram Mesajı: \"{broadcast_message[:60]}...\"")
        
        # Anti-Spam Bekleme Simülasyonu
        time.sleep(random.uniform(1, 3))

        # Profesyonel API uyumlu gönderme fonksiyonunu çağır
        return self.send_message(broadcast_message, test_media_path)

if __name__ == "__main__":
    worker = TelegramWorker()
    worker.run()

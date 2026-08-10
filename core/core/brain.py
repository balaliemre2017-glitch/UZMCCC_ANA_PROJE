import os
import google.generativeai as genai

class AIBrain:
    def __init__(self, memory_manager=None):
        self.memory_mgr = memory_manager
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_plan(self, project_type="auto", command="Genel Durum Raporu ve Etkileşim Taraması"):
        if not self.api_key:
            return command
        
        rules = ""
        history = ""
        if self.memory_mgr and hasattr(self.memory_mgr, "memory"):
            rules = self.memory_mgr.memory.get("rules", {}).get(project_type, "")
            history = "\n".join(self.memory_mgr.memory.get("chat_history", [])[-10:])

        system_instruction = (
            f"Sen Patronun Otonom AI Ajans Beynisin.\n"
            f"PROJE KİMLİĞİ: {project_type}\n"
            f"SABİT KURALLAR: {rules}\n"
            f"GEÇMİŞ PATRON EMİRLERİ VE HAFIZA:\n{history}\n\n"
            f"Patronun verdiği komut doğrultusunda Instagram, YouTube, TikTok ve Ditto işçileri için "
            f"içerik metinleri, etiketler, başlıklar, konum ve aksiyon adımlarını eksiksiz hazırla."
        )

        try:
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
            response = model.generate_content(command)
            return response.text.strip()
        except Exception as e:
            print(f"[!] Brain Plan Üretim Hatası: {e}")
            return "Varsayılan patron stratejisi uygulandı."

    def generate_content(self, platform="instagram", topic="sosyal medya gelişimi"):
        """Platform bazlı hızlı içerik ve açıklama üretme metodu"""
        if not self.api_key:
            return {
                "response": "Otomatik Sosyal Medya Gönderisi 🚀\n#viral #trending #uzmccc",
                "title": "Sosyal Medya Otomasyonu",
                "caption": "Otomatik Sosyal Medya Gönderisi 🚀\n#viral #trending",
                "hashtags": "#viral #trending"
            }

        prompts = {
            "instagram": f"'{topic}' hakkında ilgi çekici, viral olabilecek 1 Türkçe Instagram gönderi açıklaması ve 5 popüler hashtag üret.",
            "youtube": f"'{topic}' konusuyla ilgili dikkat çekici 1 Türkçe Shorts başlığı ve SEO uyumlu açıklama üret.",
            "tiktok": f"'{topic}' konusu için Z kuşağının ilgisini çekecek kısa bir Türkçe TikTok açıklaması ve hashtagler üret."
        }
        
        prompt = prompts.get(platform, prompts["instagram"])

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            content_text = response.text.strip()
            return {
                "response": content_text,
                "title": content_text.split('\n')[0][:50],
                "caption": content_text,
                "hashtags": "#viral #trending #uzmccc"
            }
        except Exception as e:
            print(f"[!] AI Content Hatası: {e}")
            return {
                "response": "Günün Otomatik Sosyal Medya Stratejisi 🚀",
                "title": "Sosyal Medya Otomasyonu",
                "caption": "Günün Otomatik Sosyal Medya Stratejisi 🚀\n#viral #trending",
                "hashtags": "#viral #trending"
            }

    def generate_reply(self, project_type, follower_message):
        if not self.api_key:
            return "Teşekkürler!"
        
        rules = ""
        if self.memory_mgr and hasattr(self.memory_mgr, "memory"):
            rules = self.memory_mgr.memory.get("rules", {}).get(project_type, "")

        system_instruction = f"Sen {project_type} karakterisin. Kuralların: {rules}. Takipçiden gelen mesaja uygun, kısa ve net cevap ver."
        
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
            response = model.generate_content(follower_message)
            return response.text.strip()
        except Exception as e:
            print(f"[!] AI Reply Hatası: {e}")
            return "Çok teşekkürler! 😊"

# Eski importlarla geriye dönük uyumluluk (Brain adı verilirse de çalışır)
Brain = AIBrain

if __name__ == "__main__":
    b = AIBrain()
    print(b.generate_plan())

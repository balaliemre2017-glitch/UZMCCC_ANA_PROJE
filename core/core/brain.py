import os
import google.generativeai as genai

class AIBrain:
    def __init__(self, memory_manager):
        self.memory_mgr = memory_manager
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_plan(self, project_type, command):
        if not self.api_key:
            return command
        
        rules = self.memory_mgr.memory["rules"].get(project_type, "")
        history = "\n".join(self.memory_mgr.memory["chat_history"][-10:])

        system_instruction = (
            f"Sen Patronun Otonom AI Ajans Beynisin.\n"
            f"PROJE KİMLİĞİ: {project_type}\n"
            f"SABİT KURALLAR: {rules}\n"
            f"GEÇMİŞ PATRON EMİRLERİ VE HAFIZA:\n{history}\n\n"
            f"Patronun verdiği komut doğrultusunda Instagram, YouTube, TikTok ve Ditto işçileri için "
            f"içerik metinleri, etiketler, başlıklar, konum ve aksiyon adımlarını eksiksiz hazırla."
        )

        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
        response = model.generate_content(command)
        return response.text.strip()

    def generate_reply(self, project_type, follower_message):
        if not self.api_key:
            return "Teşekkürler!"
        
        rules = self.memory_mgr.memory["rules"].get(project_type, "")
        system_instruction = f"Sen {project_type} karakterisin. Kuralların: {rules}. Takipçiden gelen mesaja uygun, kısa ve net cevap ver."
        
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
        response = model.generate_content(follower_message)
        return response.text.strip()

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'core'))

import json
from brain import AIBrain
from memory import MemoryManager
from workers.instagram_worker import InstagramWorker
from workers.youtube_worker import YouTubeWorker
from workers.tiktok_worker import TikTokWorker
def main():
    # 1. Hafıza ve Beyin Yüklenir
    memory_mgr = MemoryManager()
    brain = AIBrain(memory_mgr)

    # 2. Komut Alınır
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    command = "Genel Durum Raporu ve Etkileşim Taraması"

    if event_path and os.path.exists(event_path):
        with open(event_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            command = data.get("client_payload", {}).get("command", command)

    print(f"==========================================")
    print(f"[PATRON EMRİ ALINDI]: {command}")
    print(f"==========================================")

    # 3. Kural Güncellemeleri Tespiti ve Hafıza Kaydı
    if "shorts atma" in command.lower():
        memory_mgr.memory["platform_settings"]["youtube"]["allow_shorts"] = False
        print("[+] KURAL HAFIZAYA İŞLENDİ: YouTube Shorts engellendi.")

    memory_mgr.add_command_to_history(f"Patron: {command}")

    # 4. Proje Türü Ayrımı
    project_type = "TOPTANCI" if any(k in command.lower() for k in ["toptan", "biber", "domates", "hal"]) else "AI_ARTIST"

    # 5. Gemini AI Plan Üretimi
    ai_plan = brain.generate_plan(project_type, command)

    # 6. İşçiler Sırayla Tetiklenir
    ig_worker = InstagramWorker(brain, memory_mgr)
    yt_worker = YouTubeWorker(brain, memory_mgr)
    tt_worker = TikTokWorker(brain, memory_mgr)

    ig_worker.run(command, ai_plan, project_type)
    yt_worker.run(command, ai_plan)
    tt_worker.run(command, ai_plan)

    print("\n[+] Tüm işçiler görevlerini tamamladı.")

if __name__ == "__main__":
    main()

# main.py
import logging
from core.brain import Brain

# Terminal ekranının temiz ve anlaşılır görünmesi için log ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

def main():
    uzmccc_bot = Brain()
    
    # 1. GÖREV: CapCut'a 9:16 dikey formatta, UZMANÇ filigranlı arabesk rap konseptli video ürettir.
    uzmccc_bot.assign_task(
        platform="capcut", 
        action="render_vertical_video", 
        payload={
            "concept": "arabesk rap klip",
            "ratio": "9:16",
            "watermark": "UZMANÇ"
        }
    )
    
    # 2. GÖREV: Üretilen bu videoyu TikTok'a yükle.
    uzmccc_bot.assign_task(
        platform="tiktok",
        action="upload_video",
        payload={
            "file_path": "output_video.mp4",
            "description": "Yeni parça yayında! #arabesk #rap #uzmccc"
        }
    )
    
    # Sistemi Ateşle (Hafızadaki tüm görevleri sırasıyla yapacak)
    uzmccc_bot.run_system()

if __name__ == "__main__":
    main()

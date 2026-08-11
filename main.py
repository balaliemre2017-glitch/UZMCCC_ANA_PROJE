# main.py
from core.brain import Brain

def main():
    print("=======================================")
    print("      UZMCCC OTOMATIK SOSYAL MEDYA     ")
    print("           YONETIM SISTEMI             ")
    print("=======================================")
    
    uzmccc_brain = Brain()
    
    # Test Görevleri Ekleyelim
    uzmccc_brain.add_task("instagram", "post_reel", "doga_manzarasi.mp4")
    uzmccc_brain.add_task("youtube", "upload_shorts", "doga_manzarasi_shorts.mp4")
    
    # Sistemi Ateşle
    uzmccc_brain.run_system()

if __name__ == "__main__":
    main()

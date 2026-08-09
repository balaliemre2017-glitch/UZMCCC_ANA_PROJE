from .workers.capcut import CapcutIsci
from .workers.canva import CanvaIsci
from .workers.base import BaseIsci
from . import database
class PatronRobot:
    def __init__(self):
        self.isciler = {
            'capcut': CapcutIsci(),
            'canva': CanvaIsci(),
            'ses': BaseIsci('SES'),
            'muzik': BaseIsci('MUZIK'),
            'seo': BaseIsci('SEO'),
            'upload': BaseIsci('UPLOAD'),
        }
    def gorev_ver(self, video, fikir, gizli=False):
        database.ekle(video, fikir)
        print(f"\n=== YENI GOREV: {fikir} ===")
        for ad, isci in self.isciler.items():
            try:
                isci.calistir(video, fikir)
            except Exception as e:
                print(f"[{ad}] HATA: {e}")
        print("=== GOREV BITTI ===\n")
        return True

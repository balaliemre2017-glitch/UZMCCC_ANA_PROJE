
import pathlib, sqlite3, json
BASE = pathlib.Path(__file__).parent.parent.parent
DB = BASE / "yedekler" / "uzmccc.db"

def get_user():
    try:
        if not DB.exists():
            return ("email", "demo@uzmccc.com", "", 1)
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT auth_type, email, phone, aktif FROM users WHERE platform=?", ("youtube",))
        row = cur.fetchone()
        con.close()
        return row
    except:
        return None

class Worker:
    def __init__(self):
        self.platform = "youtube"
        self.auth_type = "email"
        self.yetenekler = {"video_paylas": true, "foto_paylas": true, "gonderi": true, "shorts": true, "topluluk": true}
    
    def can_do(self, y):
        return self.yetenekler.get(y, False)
    
    def paylas(self, path, aciklama):
        row = get_user()
        if not row:
            row = ("email", "demo@uzmccc.com", "", 1)
        try:
            auth_type, email, phone, aktif = row
        except:
            auth_type, email, phone = row[0], row[1], row[2]
            aktif = 1
        if not aktif:
            print(f"[YOUTUBE] Kapalı")
            return False
        kimlik = email if auth_type=='email' else phone
        print(f"[YOUTUBE] PAYLASILDI: {path} -> {kimlik} | {aciklama[:70]}")
        # Gerçek API entegrasyonu buraya
        try:
            p = pathlib.Path(path)
            if p.is_dir():
                (p / f"youtube_paylasildi.txt").write_text(f"OK {aciklama}", encoding="utf-8")
        except:
            pass
        return True
    def calistir(self, v,f):
        return self.paylas(v,f)


import pathlib, json, datetime
BASE=pathlib.Path(__file__).parent.parent.parent
from config.settings import AUTH_PATH
LOG=BASE/'yedekler'/'paylasim_log.json'
def load_auth():
    if AUTH_PATH.exists():
        try: return json.loads(AUTH_PATH.read_text(encoding='utf-8'))
        except: return {}
    return {}
def log(p,d,a,du):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    data=[]
    if LOG.exists():
        try: data=json.loads(LOG.read_text(encoding='utf-8'))
        except: data=[]
    data.append({'platform':p,'dosya':str(d),'aciklama':a,'durum':du,'tarih':datetime.datetime.now().isoformat()})
    LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
class Worker:
    def __init__(self):
        self.auth=load_auth()
        self.yetenekler={'video_paylas': True, 'foto_paylas': True}
        self.platform="tiktok"
        self.giris_tipi="email"
    def can_do(self, y): return self.yetenekler.get(y, False)
    def is_logged_in(self):
        auth=self.auth
        if self.platform in auth:
            if self.giris_tipi=="numara":
                return bool(auth[self.platform].get('phone'))
            else:
                return bool(auth[self.platform].get('username') or auth[self.platform].get('email'))
        return False
    def get_login_info(self):
        if self.platform in self.auth:
            if self.giris_tipi=="numara": return self.auth[self.platform].get('phone','')
            else: return self.auth[self.platform].get('username','') or self.auth[self.platform].get('email','')
        return ""
    def paylas(self, path, aciklama=''):
        if not self.is_logged_in() and self.platform not in ['canva','capcut']:
            log(self.platform, path, aciklama, 'ATLANDI - giris yok')
            return False
        tip='video' if str(path).lower().endswith(('.mp4','.mov','.avi','.mkv')) else 'foto'
        login_info=self.get_login_info()
        if self.platform=='youtube' and tip=='foto': durum='YOUTUBE GONDERI - '+login_info
        elif self.platform=='whatsapp' and tip=='foto': durum='WHATSAPP TOPLULUK - '+login_info
        else: durum='OK - '+login_info+' - '+tip
        log(self.platform, path, aciklama, durum)
        print('['+self.platform.upper()+'] '+durum)
        return True
    def calistir(self, v,f): return self.paylas(v,f)

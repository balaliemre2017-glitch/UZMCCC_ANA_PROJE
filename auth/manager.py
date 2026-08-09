
import json
from config.settings import AUTH_PATH, YEDEKLER_DIR
from database.models import add_user, add_phone_login
YEDEKLER_DIR.mkdir(parents=True, exist_ok=True)
def load_auth():
    if AUTH_PATH.exists():
        try: return json.loads(AUTH_PATH.read_text(encoding='utf-8'))
        except: return {}
    return {}
def save_auth(data):
    old=load_auth()
    for k,v in data.items():
        if isinstance(v, dict) and k in old and isinstance(old[k], dict):
            old[k]={**old[k], **v}
        else:
            old[k]=v
    AUTH_PATH.write_text(json.dumps(old, indent=2, ensure_ascii=False), encoding='utf-8')
    if 'master' in data:
        m=data['master']; add_user(m.get('email',''), m.get('password',''), m.get('phone',''), 'master')
    for plat in ['youtube','instagram','tiktok','facebook','twitter_x','canva','capcut']:
        if plat in data and data[plat].get('username'):
            add_user(data[plat]['username'], '', '', plat)
    for plat in ['whatsapp','telegram']:
        if plat in data and data[plat].get('phone'):
            add_phone_login(plat, data[plat]['phone'], data[plat].get('username',''))
def get_master_email():
    return load_auth().get('master',{}).get('email','balaliemre2017@gmail.com')
def is_logged_in(platform):
    auth=load_auth()
    if platform in auth:
        if platform in ['whatsapp','telegram']:
            return bool(auth[platform].get('phone'))
        else:
            return bool(auth[platform].get('username') or auth[platform].get('email'))
    return False


import sys, pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
from flask import Flask, request, redirect, render_template_string
import json, shutil, datetime
from werkzeug.utils import secure_filename
from config.settings import AUTH_PATH, YEDEKLER_DIR, DB_PATH, ENV_PATH
from auth.manager import load_auth, save_auth, get_master_email
from database.models import get_conn
from core.patron_beyni import gorev_dagit, load_manifests
app=Flask(__name__)
UPLOAD=BASE_DIR/'uploads'
UPLOAD.mkdir(parents=True, exist_ok=True)
LOG=YEDEKLER_DIR/'paylasim_log.json'
def load_env():
    d={}
    if ENV_PATH.exists():
        for l in ENV_PATH.read_text(encoding='utf-8', errors='ignore').splitlines():
            if '=' in l and not l.strip().startswith('#'):
                try:
                    k,v=l.split('=',1)
                    if v.strip(): d[k.strip()]=v.strip()
                except: pass
    return d
def save_env(new_d):
    old=load_env()
    for k,v in new_d.items():
        if v and v.strip(): old[k]=v.strip()
    ENV_PATH.write_text('\n'.join([f"{k}={v}" for k,v in old.items()])+'\n', encoding='utf-8')
HTML = """
<html><head><meta charset="utf-8"><title>V25 SON HAL</title><style>
body{background:#0a0a0a;color:#0f0;font-family:Consolas;padding:15px}
.box{border:1px solid #0f0;background:#111;padding:12px;margin:8px 0;border-radius:8px}
.boxyt{border:2px solid #f00;background:#1a0000;padding:12px;margin:8px 0;border-radius:8px}
.boxpatron{border:2px solid #0ff;background:#001a22;padding:12px;margin:8px 0;border-radius:8px}
.boxauth{border:2px solid #f0f;background:#1a001a;padding:12px;margin:8px 0;border-radius:8px}
.btn{background:#0f0;color:#000;font-weight:bold;padding:8px 14px;border:0;cursor:pointer;border-radius:4px;margin:2px}
.btnyt{background:#f00;color:#fff;font-weight:bold;padding:8px 14px;border:0;cursor:pointer;border-radius:4px}
input,textarea{width:96%;background:#000;color:#0f0;border:1px solid #0f0;padding:7px;margin:3px 0;border-radius:4px}
pre{background:#000;border:1px dashed #0f0;padding:8px;white-space:pre-wrap;font-size:11px;max-height:200px;overflow:auto}
.isci{display:inline-block;border:1px solid #0f0;padding:8px 10px;margin:4px;border-radius:8px;background:#002200;min-width:200px;vertical-align:top}
</style></head><body>
<h2>✅ V25 SON HAL CALISIYOR - FIX OK</h2>
<div class=boxpatron>Master: {{email}} | Workers: {{worker_count}} | DB: {{db_var}}</div>
<div class=boxauth>
Master:<br><form method=POST action="/save_master"><input name=email value="{{email}}" style="width:40%"><input name=phone value="{{phone}}" style="width:20%"><button class=btn>KAYDET</button></form><br>
<div>
{% for plat, mf in workers.items() %}
<div class=isci><b>{{plat.upper()}}</b> {% if mf.giris_tipi=='numara' %}<span style="background:#f0f;color:#000;padding:2px 6px;border-radius:10px;font-size:10px">NUMARA</span>{% endif %}<br>
Durum: {{'VAR' if auth.get(plat) else 'YOK'}}<br>
{% if mf.giris_tipi=='numara' %}
No:<br><input id="phone_{{plat}}" value="{{auth.get(plat,{}).get('phone','')}}"><br>User:<br><input id="user_{{plat}}" value="{{auth.get(plat,{}).get('username','')}}"><br>
{% else %}
Email:<br><input id="user_{{plat}}" value="{{auth.get(plat,{}).get('username','') or auth.get(plat,{}).get('email','')}}"><br>
{% endif %}
{{mf.yetenekler|join(', ')}}<br><button class=btn onclick="savePlat('{{plat}}')">KAYDET</button></div>
{% endfor %}
</div>
</div>
<div class=box>API KEY<form method=POST action="/save_keys">YT:<br><input name=YOUTUBE_API_KEY value="{{env.get('YOUTUBE_API_KEY','')}}"><br>GEMINI:<br><input name=GEMINI_API_KEY value="{{env.get('GEMINI_API_KEY','')}}"><br><button class=btn>KAYDET</button></form></div>
<div class=boxyt><b>YUKLE Foto->YT Gonderi + WA Topluluk</b><form method=POST action="/upload" enctype="multipart/form-data"><input type=file name=foto required><br><textarea name=emir>foto attim youtubede gonderi kismina dussun whatsapta topluluk paylasimina</textarea><br><button class=btnyt>GONDER</button></form></div>
<div class=box><pre>{{log_text}}</pre></div>
<script>
function savePlat(plat){
  let phone=document.getElementById('phone_'+plat)?.value || '';
  let user=document.getElementById('user_'+plat)?.value || '';
  fetch('/save_platform',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({platform:plat,phone:phone,username:user})}).then(()=>location.reload());
}
</script>
</body></html>
"""
@app.route('/')
def idx():
    env=load_env(); auth=load_auth(); mans=load_manifests()
    email=get_master_email()
    conn=get_conn(); hafiza=conn.execute("SELECT * FROM hafiza ORDER BY id DESC LIMIT 10").fetchall(); conn.close()
    workers_display={}
    for plat, mf in mans.items():
        workers_display[plat]={'yetenekler': list(mf.get('yetenekler',{}).keys()), 'aktif': mf.get('aktif', True), 'giris_tipi': mf.get('giris_tipi','email')}
    log_text="Yok"
    if LOG.exists():
        try:
            data=json.loads(LOG.read_text(encoding='utf-8'))
            log_text="\n".join([f"{x['tarih'][11:19]} {x['platform']} {x['durum'][:70]}" for x in data[-12:][::-1]])
        except: pass
    return render_template_string(HTML, email=email, phone=auth.get('master',{}).get('phone',''), env=env, auth=auth, workers=workers_display, worker_count=len(mans), db_var=DB_PATH.exists(), log_text=log_text)
@app.route('/save_master', methods=['POST'])
def save_master():
    email=request.form.get('email','').strip(); phone=request.form.get('phone','').strip()
    if email: save_auth({'master':{'email':email,'phone':phone}})
    return redirect('/')
@app.route('/save_platform', methods=['POST'])
def save_platform():
    data=request.get_json(); plat=data.get('platform'); phone=data.get('phone',''); username=data.get('username','')
    save_auth({plat:{'phone':phone,'username':username}})
    return "ok"
@app.route('/save_keys', methods=['POST'])
def save_keys():
    new={}
    for k in ['YOUTUBE_API_KEY','GEMINI_API_KEY']:
        v=request.form.get(k,'').strip()
        if v: new[k]=v
    save_env(new)
    return redirect('/')
@app.route('/upload', methods=['POST'])
def upload():
    try:
        foto=request.files.get('foto')
        if not foto: return redirect('/')
        filename=secure_filename(foto.filename)
        ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path=UPLOAD/f"{ts}_{filename}"
        foto.save(str(save_path))
        emir=request.form.get('emir','')
        gorev_dagit(str(save_path), emir)
    except Exception as e:
        print(e)
    return redirect('/')
if __name__=='__main__':
    print("V25 SON HAL http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

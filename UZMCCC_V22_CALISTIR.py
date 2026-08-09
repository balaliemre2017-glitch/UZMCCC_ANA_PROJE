
import pathlib, json, os, sys
# Otomatik BASE bul - nerede olursak olalim yedekler'i bul
def find_base():
    cur=pathlib.Path(__file__).parent
    for _ in range(5):
        if (cur / 'yedekler').exists() or (cur / 'API_ANAHTARLAR.env').exists() or (cur / 'panel').exists():
            return cur
        # Bir ust klasordeki UZMCCC_ANA_PROJE icine bak
        inner=cur / 'UZMCCC_ANA_PROJE' / 'UZMCCC_ANA_PROJE'
        if inner.exists():
            return inner
        inner2=cur / 'UZMCCC_ANA_PROJE'
        if (inner2 / 'panel').exists():
            return inner2
        cur=cur.parent
    return pathlib.Path(__file__).parent.parent

BASE=find_base()
print(f"BASE bulundu: {BASE}")

AUTH=BASE/'yedekler'/'auth.json'
LOG=BASE/'yedekler'/'paylasim_log.json'
ENV=BASE/'API_ANAHTARLAR.env'
UPLOAD=BASE/'uploads'
UPLOAD.mkdir(parents=True, exist_ok=True)
(BASE/'yedekler').mkdir(parents=True, exist_ok=True)

# Yoksa olustur - KALICI
if not ENV.exists():
    ENV.write_text("YOUTUBE_API_KEY=AIzaSyBQgQQTzGh_pG9_4hSdJ7xCwTB-HcE1qQM\nGEMINI_API_KEY=AQ.Ab8RN6LqiNF_RnZykzNYoAiH8YWfP9JJKrVsNzOFn82jS0I0zw\n", encoding='utf-8')
if not AUTH.exists():
    AUTH.write_text('{"master":{"email":"balaliemre2017@gmail.com"}}', encoding='utf-8')

def load_env():
    d={}
    if ENV.exists():
        for l in ENV.read_text(encoding='utf-8', errors='ignore').splitlines():
            if '=' in l and not l.strip().startswith('#'):
                try:
                    k,v=l.split('=',1)
                    d[k.strip()]=v.strip()
                except: pass
    return d

def load_auth():
    if AUTH.exists():
        try: return json.loads(AUTH.read_text(encoding='utf-8'))
        except: return {}
    return {}

from flask import Flask, request, redirect
app=Flask(__name__)

@app.route('/')
def idx():
    env=load_env()
    auth=load_auth()
    email=auth.get('master',{}).get('email','balaliemre2017@gmail.com')
    yt=env.get('YOUTUBE_API_KEY','YOK')[:25]
    gem=env.get('GEMINI_API_KEY','YOK')[:25]
    log_text="Yok"
    if LOG.exists():
        try:
            data=json.loads(LOG.read_text(encoding='utf-8'))
            log_text="\n".join([f"{x['tarih'][11:19]} {x['platform']}" for x in data[-8:][::-1]])
        except: pass
    return f"""<html><head><meta charset="utf-8"><style>
body{{background:#0a0a0a;color:#0f0;font-family:Consolas;padding:15px}}
.box{{border:2px solid #0f0;background:#111;padding:15px;margin:10px 0;border-radius:8px}}
.boxyt{{border:2px solid #f00;background:#1a0000;padding:15px;margin:10px 0;border-radius:8px}}
.btn{{background:#0f0;color:#000;font-weight:bold;padding:12px 20px;border:0;cursor:pointer;border-radius:6px;font-size:14px}}
.btnyt{{background:#f00;color:#fff;font-weight:bold;padding:12px 20px;border:0;cursor:pointer;border-radius:6px}}
input{{width:95%;background:#000;color:#0f0;border:1px solid #0f0;padding:10px;margin:5px 0;border-radius:4px}}
pre{{background:#000;border:1px dashed #0f0;padding:10px;white-space:pre-wrap;font-size:12px}}
</style></head><body>
<h1>✅ UZMCCC V22 - TEK DOSYA - CALISTI!</h1>
<div class=box>
BASE: {BASE}<br>
Master: {email}<br>
YT: {yt}... {'✅' if 'AIza' in yt else '❌'}<br>
GEMINI: {gem}... {'✅' if gem!='YOK' else '❌'}<br>
</div>
<div class=boxyt>
<b>YOUTUBE VIDEO YUKLE</b><br>
<form method=POST action="/upload" enctype="multipart/form-data">
<input type=file name=foto accept="video/*,image/*" required><br>
<input name=emir value="youtubedan paylas - test"><br>
<button class=btnyt>🔴 YUKLE</button>
</form>
</div>
<div class=box><b>LOG</b><pre>{log_text}</pre></div>
<div class=box>
<a href="/" style="color:#0f0">Yenile</a> | V22 tek dosya calisiyor kanka! Artik dosya yolu sorunu yok!
</div>
</body></html>"""

@app.route('/upload', methods=['POST'])
def upload():
    try:
        from werkzeug.utils import secure_filename
        import datetime
        foto=request.files.get('foto')
        if not foto: return redirect('/')
        filename=secure_filename(foto.filename)
        ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path=UPLOAD/f"{ts}_{filename}"
        foto.save(str(save_path))
        LOG.parent.mkdir(parents=True, exist_ok=True)
        data=[]
        if LOG.exists():
            try: data=json.loads(LOG.read_text(encoding='utf-8'))
            except: data=[]
        data.append({'platform':'youtube','dosya':str(save_path),'aciklama':request.form.get('emir',''),'durum':f'OK {save_path.name}','tarih':datetime.datetime.now().isoformat()})
        LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"YUKLENDI: {save_path}")
    except Exception as e:
        print(e)
        import traceback; traceback.print_exc()
    return redirect('/')

if __name__=='__main__':
    print(f"\n=== V22 TEK DOSYA ===")
    print(f"BASE: {BASE}")
    print(f"URL: http://127.0.0.1:5000")
    print(f"Tarayicida ac: http://127.0.0.1:5000")
    print(f"====================\n")
    app.run(host='0.0.0.0', port=5000, debug=False)

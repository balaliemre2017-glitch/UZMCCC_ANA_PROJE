
from flask import Flask, request, redirect, render_template_string, jsonify
import pathlib, sqlite3, json
from datetime import datetime
from werkzeug.utils import secure_filename
BASE = pathlib.Path(__file__).parent
from core.patron_beyni import emir_coz_gelismis, dagit_gorev, get_active_workers
from core.hafiza import get_hafiza

app = Flask(__name__)
DB = BASE / "yedekler" / "uzmccc.db"
UPLOAD = BASE / "uploads"
CIKTI = BASE / "cikti"
for p in [UPLOAD, CIKTI, BASE / "yedekler"]:
    p.mkdir(exist_ok=True)

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, platform TEXT UNIQUE, auth_type TEXT, email TEXT, phone TEXT, aktif INTEGER DEFAULT 1, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    con.execute("CREATE TABLE IF NOT EXISTS gecmis (id INTEGER PRIMARY KEY, emir TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    con.execute("CREATE TABLE IF NOT EXISTS loglar (id INTEGER PRIMARY KEY, platform TEXT, dosya TEXT, durum TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    for plat, auth in [("youtube","email"),("instagram","email"),("facebook","email"),("tiktok","email"),("twitter_x","email"),("whatsapp","phone"),("telegram","phone"),("canva","email"),("capcut","email"),("github","email")]:
        con.execute("INSERT OR IGNORE INTO users(platform, auth_type, email, aktif) VALUES(?,?,?,1)", (plat, auth, "balaliemre2017@gmail.com" if auth=="email" else ""))
    con.execute("INSERT OR IGNORE INTO users(platform, auth_type, email, aktif) VALUES('master','email','balaliemre2017@gmail.com',1)")
    con.commit()
    con.close()
init_db()

HTML = """
<html><head><meta charset="utf-8"><title>UZMCCC V26 BOT</title>
<style>body{background:#050505;color:#0f0;font-family:Consolas;padding:12px} .box{border:1px solid #0f0;background:#0a1a0a;padding:12px;margin:10px 0;border-radius:10px} .box-yt{border:2px solid #f00;background:#1a0000} .btn{background:#0f0;color:#000;font-weight:900;padding:10px 18px;border:0;border-radius:6px} .btn-yt{background:#f00;color:#fff;padding:12px 20px;border:0;border-radius:6px;font-weight:900} input,textarea{width:95%;background:#000;color:#0f0;border:1px solid #0f0;padding:8px;border-radius:6px} .isci{display:inline-block;border:1px solid #0f0;padding:8px;margin:4px;border-radius:8px;background:#002200;min-width:180px} pre{background:#000;border:1px dashed #0f0;padding:8px;max-height:180px;overflow:auto}</style></head><body>
<h1>UZMCCC V26 - TAM OTOMATIK BOT</h1>
<div class=box> Aktif: {{active}} | Repo: balaliemre2017-glitch/UZMCCC_ANA_PROJE | Sohbet analizi: V6+V25 birlesik</div>
<div class=box-yt><b>TEK EMIR -> HER YER</b><br><form method=POST action="/emir" enctype="multipart/form-data"><textarea name=emir rows=3 placeholder="foto attim youtubede gonderi whatsapp topluluk, veya: hepsi icin karincalar grevde videosu yap" required></textarea><br><input type=file name=dosya><br><button class=btn-yt>PATRONA GONDER</button></form></div>
<div class=box>{% for plat, auth, email, phone, aktif in users %}{% if plat!='master' %}<div class=isci><b>{{plat}}</b> {{'🟢' if aktif else '🔴'}}<br><small>{{email or phone}}</small><form method=POST action="/toggle/{{plat}}"><button class=btn>{{'KAPAT' if aktif else 'AC'}}</button></form></div>{% endif %}{% endfor %}</div>
<div class=box><pre>{{gecmis}}</pre><pre>{{log}}</pre><pre>{{paketler}}</pre></div>
</body></html>
"""

@app.route('/')
def idx():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT platform, auth_type, email, phone, aktif FROM users")
    users = cur.fetchall()
    cur.execute("SELECT emir FROM gecmis ORDER BY id DESC LIMIT 10")
    gecmis = cur.fetchall()
    cur.execute("SELECT platform, durum FROM loglar ORDER BY id DESC LIMIT 10")
    logs = cur.fetchall()
    con.close()
    paketler = [p.name for p in CIKTI.iterdir() if p.is_dir()][:10]
    return render_template_string(HTML, users=users, active=len([u for u in users if u[4]==1 and u[0]!='master']), gecmis="\n".join([g[0] for g in gecmis]), log="\n".join([f"{l[0]} {l[1][:60]}" for l in logs]), paketler="\n".join(paketler))

@app.route('/emir', methods=['POST'])
def emir():
    txt = request.form.get('emir','')
    f = request.files.get('dosya')
    path = "no_file"
    if f and f.filename:
        p = UPLOAD / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(f.filename)}"
        f.save(str(p))
        path = str(p)
    if txt:
        dagit_gorev(path, txt)
        con = sqlite3.connect(DB)
        con.execute("INSERT INTO gecmis(emir) VALUES(?)", (txt,))
        con.commit()
        con.close()
    return redirect('/')

@app.route('/toggle/<plat>', methods=['POST'])
def toggle(plat):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT aktif FROM users WHERE platform=?", (plat,))
    r = cur.fetchone()
    if r:
        con.execute("UPDATE users SET aktif=? WHERE platform=?", (0 if r[0]==1 else 1, plat))
        con.commit()
    con.close()
    return redirect('/')

@app.route('/api/emir', methods=['POST'])
def api_emir():
    data = request.get_json() or {}
    txt = data.get('emir','')
    analiz = emir_coz_gelismis(txt)
    sonuc = dagit_gorev("api", txt)
    return jsonify({"analiz": analiz, "sonuc": sonuc})

if __name__ == '__main__':
    print("V26 BOT - http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)


import pathlib, sqlite3
BASE = pathlib.Path(__file__).parent.parent
DB = BASE / "yedekler" / "uzmccc.db"
def get_hafiza(limit=50):
    if not DB.exists():
        return {"gecmis": []}
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT emir, tarih FROM gecmis ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return {"gecmis": [{"emir": r[0], "tarih": r[1]} for r in rows]}

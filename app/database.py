import sqlite3, pathlib
DB = pathlib.Path(__file__).parent / "uzmccc.db"
def init():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS gorevler (id INTEGER PRIMARY KEY, video TEXT, fikir TEXT, durum TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    con.commit(); con.close()
def ekle(video, fikir):
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO gorevler(video,fikir,durum) VALUES(?,?,?)",(video,fikir,"bekliyor"))
    con.commit(); con.close()
init()

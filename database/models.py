
import sqlite3, pathlib
from config.settings import DB_PATH, YEDEKLER_DIR
YEDEKLER_DIR.mkdir(parents=True, exist_ok=True)
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, phone TEXT, platform TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS phone_logins (id INTEGER PRIMARY KEY, platform TEXT, phone TEXT, username TEXT, UNIQUE(platform, phone))")
    conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS hafiza (id INTEGER PRIMARY KEY, emir TEXT, detay TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit(); conn.close()
    print("[DB] OK")
def add_user(email,password="",phone="",platform="master"):
    conn=get_conn(); conn.execute("INSERT OR REPLACE INTO users(email,password,phone,platform) VALUES(?,?,?,?)",(email,password,phone,platform)); conn.commit(); conn.close()
def add_phone_login(platform,phone,username=""):
    conn=get_conn(); conn.execute("INSERT OR REPLACE INTO phone_logins(platform,phone,username) VALUES(?,?,?)",(platform,phone,username)); conn.commit(); conn.close()
def log_hafiza(emir,detay=""):
    conn=get_conn(); conn.execute("INSERT INTO hafiza(emir,detay) VALUES(?,?)",(emir,detay)); conn.commit(); conn.close()
init_db()

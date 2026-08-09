from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import pathlib
from .patron import PatronRobot

app = FastAPI(title="UZMCCC PRO")
patron = PatronRobot()
FRONT = pathlib.Path(__file__).parent.parent / "frontend" / "index.html"

@app.get("/", response_class=HTMLResponse)
def panel():
    return FRONT.read_text(encoding='utf-8')

@app.post("/calistir")
def calistir(video: str = Form(...), fikir: str = Form(...), gizli: str = Form(None)):
    try:
        patron.gorev_ver(video, fikir, gizli=bool(gizli))
        return {"durum": "ok", "mesaj": "6 işçi çalıştı! CMD loguna bak!"}
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

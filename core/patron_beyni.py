
"""
UZMCCC V26 - SÜPER PATRON BEYNİ - TAM ANALİZ SONUCU
Bu sohbetin tamamı analiz edildi: V6 + V25 + GitHub savaşı
Amaç: Otomatik sosyal medya botu - tek emir tüm platformlar
"""
import re, pathlib, sqlite3, json
from datetime import datetime

BASE = pathlib.Path(__file__).parent.parent
DB = BASE / "yedekler" / "uzmccc.db"

PLATFORMS = ["youtube", "instagram", "facebook", "tiktok", "twitter_x", "whatsapp", "telegram", "canva", "capcut", "github"]
ALIASES = {
    "yt": "youtube", "youtube": "youtube",
    "insta": "instagram", "ig": "instagram", "instagram": "instagram",
    "fb": "facebook", "facebook": "facebook",
    "tiktok": "tiktok", "tt": "tiktok",
    "twitter": "twitter_x", "x": "twitter_x", "twitter_x": "twitter_x",
    "wa": "whatsapp", "whatsapp": "whatsapp",
    "tg": "telegram", "telegram": "telegram",
    "canva": "canva", "kapak": "canva",
    "capcut": "capcut", "kesim": "capcut",
    "github": "github", "git": "github"
}

def get_active_workers():
    if not DB.exists():
        return PLATFORMS.copy()
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT platform, auth_type, email, phone, aktif FROM users WHERE aktif=1")
        rows = cur.fetchall()
        con.close()
        active = []
        for plat, auth_type, email, phone, aktif in rows:
            if plat == 'master':
                continue
            if auth_type == 'email' and email:
                active.append(plat)
            elif auth_type == 'phone' and phone:
                active.append(plat)
            elif plat in ['canva','capcut','github']:
                active.append(plat)
        return active if active else PLATFORMS.copy()
    except:
        return PLATFORMS.copy()

def emir_coz_gelismis(emir_text: str):
    raw = emir_text
    emir = emir_text.lower().strip()
    secilen = set()

    if any(k in emir for k in ["hepsi", "tümü", "full", "her yer"]):
        secilen = set(get_active_workers())
    else:
        for alias, plat in ALIASES.items():
            if alias in emir:
                # kısa aliaslar için kelime sınırı
                if alias in ["wa","ig","tt","fb","x"]:
                    if alias in emir.split():
                        secilen.add(plat)
                else:
                    if alias in emir:
                        secilen.add(plat)

    # Otomatik mantık - bu sohbette çok istendi
    if any(k in emir for k in ["foto", "resim", "fotograf"]):
        secilen.update(["youtube", "instagram", "facebook", "whatsapp"])
    if any(k in emir for k in ["video", "reels", "shorts"]):
        secilen.update(["youtube", "instagram", "tiktok", "facebook", "capcut"])

    if not secilen:
        secilen = set(get_active_workers())

    # Konu ayıkla
    konu = raw
    for alias in ALIASES.keys():
        konu = re.sub(rf"\b{alias}\b", "", konu, flags=re.IGNORECASE)
    for w in ["hepsi", "sadece", "için", "ve", "ile", "yap", "at", "gönder", "paylaş", "düşsün", "kısmına"]:
        konu = re.sub(rf"\b{w}\b", "", konu, flags=re.IGNORECASE)
    konu = re.sub(r"\s+", " ", konu).strip()
    if len(konu) < 3:
        konu = "karıncalar grevde - UZMCCC otomatik"

    tip = "foto" if "foto" in emir else "video" if "video" in emir else "karisik"
    zamanlama = "hemen"

    return {
        "platforms": list(secilen),
        "konu": konu,
        "tip": tip,
        "zamanlama": zamanlama,
        "raw": raw,
        "active_workers": get_active_workers()
    }

def dagit_gorev(video_path, emir_text, log_callback=None):
    analiz = emir_coz_gelismis(emir_text)
    print(f"\n[PATRON V26] Emir: {emir_text} -> Konu: {analiz['konu']} -> Hedefler: {analiz['platforms']}")

    results = []
    try:
        from .fabrika import calistir_fabrika
        fabrika_sonuc = calistir_fabrika(analiz["platforms"], analiz["konu"], tip=analiz["tip"])
    except Exception as e:
        print(f"[FABRIKA HATA] {e}")
        fabrika_sonuc = {"paket": "hata", "path": str(BASE / "yedekler")}

    for plat in analiz["platforms"]:
        worker_path = BASE / f"workers/{plat}/worker.py"
        if worker_path.exists():
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(f"{plat}_w26", str(worker_path))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                isci = mod.Worker()
                kaynak = fabrika_sonuc.get("path", video_path)
                isci.paylas(kaynak, analiz["konu"])
                results.append(plat)
                if DB.exists():
                    con = sqlite3.connect(DB)
                    con.execute("INSERT INTO loglar(platform, dosya, durum) VALUES(?,?,?)", (plat, str(kaynak), f"OK - {analiz['konu'][:80]}"))
                    con.execute("INSERT INTO gecmis(emir) VALUES(?)", (f"{plat}: {analiz['konu']}",))
                    con.commit()
                    con.close()
            except Exception as e:
                print(f"[{plat}] HATA: {e}")

    print(f"[PATRON] BİTTİ: {results}\n")
    return {"hedefler": analiz["platforms"], "sonuclar": results, "analiz": analiz, "fabrika": fabrika_sonuc}


import json, pathlib
from datetime import datetime
BASE = pathlib.Path(__file__).parent.parent
CIKTI_DIR = BASE / "cikti"
CIKTI_DIR.mkdir(exist_ok=True)

def calistir_fabrika(platforms, konu, tip="karisik"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    paket_adi = f"{timestamp}_{konu[:25].replace(' ','_')}"
    paket_yolu = CIKTI_DIR / paket_adi
    paket_yolu.mkdir(parents=True, exist_ok=True)

    # Canva
    (paket_yolu / "kapak.png").write_bytes(b"PNG_FAKE_" + konu.encode()[:50])
    (paket_yolu / "canva.json").write_text(json.dumps({"title": konu.upper(), "konu": konu}, ensure_ascii=False, indent=2), encoding="utf-8")
    # CapCut
    (paket_yolu / "video_kurgu.json").write_text(json.dumps({"topic": konu, "captions": True}, ensure_ascii=False), encoding="utf-8")
    # Ses & Açıklama
    (paket_yolu / "ses_metni.txt").write_text(f"{konu} - UZMCCC V26 otomatik", encoding="utf-8")
    (paket_yolu / "aciklama.txt").write_text(f"{konu} #uzmccc #viral", encoding="utf-8")
    (paket_yolu / "ses.srt").write_text(f"1\n00:00:00,000 --> 00:00:03,000\n{konu}", encoding="utf-8")

    for plat in platforms:
        (paket_yolu / f"{plat}_rapor.json").write_text(json.dumps({"platform": plat, "konu": konu, "status": "HAZIR"}, ensure_ascii=False, indent=2), encoding="utf-8")

    final = {"paket": paket_adi, "konu": konu, "platforms": platforms, "tip": tip, "klasor": str(paket_yolu)}
    (paket_yolu / "FINAL.json").write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"success": True, "paket": paket_adi, "path": str(paket_yolu), "final": final}

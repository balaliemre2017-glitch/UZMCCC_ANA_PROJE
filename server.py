import os
import sys
import subprocess
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# --- 1. PROFESYONEL LOGLAMA SİSTEMİ ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("UZMANCCC_API")

app = Flask(__name__)
CORS(app)  # Panelin (HTML) farklı portlardan veya IP'lerden istek atabilmesini sağlar

# --- 2. ANA SAYFAYI (PANELİ) DOĞRUDAN SUNMA (404 HATASINI BİTİREN KISIM) ---
@app.route('/')
def serve_index():
    """127.0.0.1:5000 adresine girildiğinde index.html panelini ekrana getirir."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base_dir, 'index.html')

# --- 3. SİSTEM DURUM KONTROLÜ (HEALTH CHECK) ---
@app.route('/api/status', methods=['GET'])
def status_check():
    """Panelin sunucuyla bağlantısının stabil olup olmadığını kontrol ettiği uç nokta."""
    return jsonify({
        'durum': 'aktif',
        'versiyon': 'UZMANCCC V26',
        'sistem_saati': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# --- 4. ANA KOMUTA VE TETİKLEME MERKEZİ ---
@app.route('/api/komut-gonder', methods=['POST'])
def komut_gonder():
    """Panelden gelen patron emirlerini alıp main.py motorunu arka planda tetikler."""
    try:
        data = request.json
        worker = data.get('target_worker', 'all')
        patron_emri = data.get('patron_emri', '').strip()

        if not patron_emri:
            logger.warning("Panelden boş emir gönderilmeye çalışıldı. Reddedildi.")
            return jsonify({'hata': 'Patron emri boş olamaz!'}), 400

        logger.info(f"👑 EMİR KABUL EDİLDİ | Hedef: {worker.upper()} | İçerik: {patron_emri}")

        # Ortam değişkenlerini (Environment Variables) projeye uygun olarak hazırla
        env = os.environ.copy()
        env['PATRON_EMRI'] = patron_emri
        env['ACTIVE_WORKERS'] = worker if worker != 'all' else ''
        env['PROJECT_TYPE'] = 'auto_agency'

        # İşletim sistemindeki doğru Python komutunu ve main.py yolunu dinamik olarak bul
        python_cmd = sys.executable 
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(base_dir, 'main.py')

        if not os.path.exists(main_py_path):
            logger.error(f"Kritik Hata: {main_py_path} bulunamadı!")
            return jsonify({'hata': 'main.py motoru bulunamadı! Dizin yapısını kontrol edin.'}), 500

        # main.py motorunu arka planda asenkron olarak başlat 
        subprocess.Popen(
            [python_cmd, main_py_path], 
            env=env,
            cwd=base_dir
        )

        return jsonify({
            'mesaj': f"Sistem motoru tetiklendi. '{patron_emri}' emri işçilere dağıtılıyor...",
            'hedef': worker
        }), 200

    except Exception as e:
        logger.error(f"❌ BEKLENMEYEN SUNUCU HATASI: {str(e)}")
        return jsonify({'hata': f'Sistem iç hatası: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" 🚀 UZMANCCC HOLDİNG - MERKEZİ API SUNUCUSU AKTİF")
    print(" 🛡️  Versiyon: V26 Otonom Dijital Ajans")
    print(" 🌐 Panel Adresi: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

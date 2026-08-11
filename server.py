# server.py
from flask import Flask, request, jsonify, render_template
import logging
from core.memory import Memory
from core.brain import Brain
import threading

app = Flask(__name__, template_folder='.')
memory = Memory()

# Beyin sistemini arka planda çalıştıracak fonksiyon
def bot_loop():
    bot_brain = Brain()
    while True:
        bot_brain.run_system()
        time.sleep(10) # Her 10 saniyede bir yeni görev var mı diye kontrol eder

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "pending": memory.get_pending_tasks(),
        "history": memory.data.get("history", [])
    })

@app.route('/api/add_task', methods=['POST'])
def add_task():
    data = request.json
    platform = data.get('platform')
    action = data.get('action')
    payload = data.get('payload', {})
    
    if platform and action:
        task = {"platform": platform, "action": action, "payload": payload, "status": "PENDING"}
        memory.add_task(task)
        return jsonify({"status": "success", "message": "Görev bota iletildi."})
    return jsonify({"status": "error", "message": "Eksik bilgi!"}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("UZMCCC Web Paneli Başlatılıyor... http://127.0.0.1:5000 adresine gidin.")
    
    # Botu arka planda ayrı bir iş parçacığı (thread) olarak başlat
    bot_thread = threading.Thread(target=bot_loop, daemon=True)
    bot_thread.start()
    
    # Web sunucusunu başlat
    app.run(port=5000, debug=False)

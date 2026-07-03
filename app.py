from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import webbrowser
import psutil
import requests
import os

app = Flask(__name__)
CORS(app)

ELEVENLABS_API_KEY = "sk_c34fd250879a45fa77ae55740805bf2b8025a1cbd8792b6b"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def stacy_bicara(teks):
    """Fungsi untuk mengubah teks menjadi suara ElevenLabs dan memutarnya via afplay Mac"""
    print(f"[STACY VOICE] Mengonversi teks ke suara: '{teks}'")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": teks,
        "model_id": "eleven_multilingual_v2",  
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            nama_file = "stacy_voice.mp3"
            
            with open(nama_file, "wb") as f:
                f.write(response.content)
            
            os.system(f"afplay {nama_file}")
    
            if os.path.exists(nama_file):
                os.remove(nama_file)
        else:
            print(f"[ERROR ELEVENLABS] Gagal mengambil audio: {response.text}")
    except Exception as e:
        print(f"[ERROR VOICE SYSTEM] Terjadi kesalahan: {str(e)}")

@app.route('/perintah', methods=['POST'])
def terima_perintah():
    data = request.json
    teks_perintah = data.get("perintah", "").lower()
    print(f"[STACY LOG] Menerima perintah: {teks_perintah}")
    
    # Logika merespons perintah
    if "vs code" in teks_perintah or "vscode" in teks_perintah:
        subprocess.Popen(["code"], shell=True)
        respon_teks = "Alright Miss, opening VS Code."
        stacy_bicara(respon_teks)
        return jsonify({"status": "SUCCESS", "respon": respon_teks})
        
    elif "spotify" in teks_perintah:
        subprocess.run(["open", "-a", "Spotify"])
        respon_teks = "Alright Miss, opening Spotify."
        stacy_bicara(respon_teks)
        return jsonify({"status": "SUCCESS", "respon": respon_teks})
        
    elif "google" in teks_perintah:
        webbrowser.open("https://www.google.com")
        respon_teks = "Alright Miss, opening Google."
        stacy_bicara(respon_teks)
        return jsonify({"status": "SUCCESS", "respon": respon_teks})
        
    else:
        respon_teks = "Sorry Miss, we don't have that command yet, wanna add it to the system?"
        stacy_bicara(respon_teks)
        return jsonify({"status": "UNKNOWN", "respon": respon_teks})


@app.route('/status-sistem', methods=['GET'])
def status_sistem():
    cpu_usage = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    disk = psutil.disk_usage('/')
    storage_free_gb = round(disk.free / (1024 ** 3), 1)
    
    baterai = psutil.sensors_battery()
    bat_persen = baterai.percent if baterai else 100
    bat_charging = baterai.power_plugged if baterai else False

    return jsonify({
        "cpu": cpu_usage,
        "ram": ram_usage,
        "storage_free": storage_free_gb,
        "baterai": {
            "persen": bat_persen,
            "charging": bat_charging
        }
    })

if __name__ == '__main__':
    import threading
    import os

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        greeting_text = "System online... Hello Miss, Stacy is ready to assist you, What are we going to do today?"
        threading.Thread(target=stacy_bicara, args=(greeting_text,), daemon=True).start()
    
    app.run(host='127.0.0.1', port=5000, debug=True)
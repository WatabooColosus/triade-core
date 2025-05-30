# Wataboo·TRÍADE·Ω
# main.py — Backend Central Tríade
from flask import Flask, request, jsonify
from flask_cors import CORS
from drive_handler import upload_file_to_drive
import os
import json
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Nueva ruta segura dentro del repo
LOG_PATH = os.path.join("logs", "triade_log.json")
os.makedirs("logs", exist_ok=True)

def log_message(content):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content
    }
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([log_entry], f, indent=4, ensure_ascii=False)

    # Git commit simbólico
    try:
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "✍ Registro simbólico actualizado"], check=True)
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    message = data.get("message", "")
    log_message({"type": "text", "message": message})
    return jsonify({"response": f"🧠 Tríade recibió: '{message}'"})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file:
        file_id, file_url = upload_file_to_drive(file)
        log_message({
            "type": "file",
            "filename": file.filename,
            "file_id": file_id,
            "file_url": file_url
        })
        return jsonify({"file_id": file_id, "file_url": file_url})
    return jsonify({"error": "No se recibió archivo"}), 400

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "activo",
        "triade": "conectada",
        "dominio_frontend": "https://tiendaxiaomi.online",
        "dominio_backend": "https://triade-core.onrender.com"
    })

if __name__ == "__main__":
    log_message({"type": "sistema", "message": "🟢 Tríade inició localmente"})
    app.run(debug=True)

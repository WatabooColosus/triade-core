# === backend/main.py ===
from flask import Flask, request, jsonify
from drive_handler import upload_file_to_drive
import json
import os
import subprocess  # Para ejecutar comandos Git
from datetime import datetime

app = Flask(__name__)

LOG_PATH = "../data/triade_log.json"

# Función para registrar mensaje en archivo y hacer commit a Git
# 👉 Aquí se hace la petición de acceso a Git (vía subprocess)
def log_message(content):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content
    }
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r+") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
    else:
        with open(LOG_PATH, "w") as f:
            json.dump([log_entry], f, indent=4)

    # 🔄 Commit simbólico a Git
    try:
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "✍ Aprendizaje simbólico registrado"], check=True)
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    message = data.get("message", "")
    log_message({"type": "text", "message": message})
    return jsonify({"response": f"He recibido tu mensaje: '{message}'"})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        # 👉 Aquí se hace la petición de acceso a Google Drive
        file_id, file_url = upload_file_to_drive(file)
        log_message({"type": "file", "filename": file.filename, "file_id": file_id})
        return jsonify({"file_id": file_id, "file_url": file_url})
    return jsonify({"error": "No se recibió archivo"}), 400

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "activo", "triade": "conectada"})

if __name__ == "__main__":
    app.run(debug=True)
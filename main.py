# Wataboo·TRÍADE·Ω — main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from drive_handler import upload_file_to_drive
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

LOG_PATH = "data/triade_log.json"
os.makedirs("data", exist_ok=True)  # Asegura la carpeta

# Función para registrar interacciones simbólicas y hacer commit
def log_message(content):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry, indent=4) + ",\n")

    # Configurar Git y registrar
    try:
        subprocess.run(["git", "config", "--global", "user.email", "agenciadigitalwataboo@gmail.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "WatabooColosus"], check=True)
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "✍ Registro simbólico actualizado"], check=True)
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
        file_id, file_url = upload_file_to_drive(file)
        log_message({"type": "file", "filename": file.filename, "file_id": file_id})
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

# Mensaje inicial simbólico
log_message({"type": "sistema", "message": "🟢 Tríade inició correctamente en Render"})

if __name__ == "__main__":
    app.run(debug=True)

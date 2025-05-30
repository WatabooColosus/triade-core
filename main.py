# === backend/main.py ===
from flask import Flask, request, jsonify
from flask_cors import CORS
from drive_handler import upload_file_to_drive
from googleapiclient.http import MediaFileUpload
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

LOG_PATH = "triade_log.json"

# Función para registrar mensaje/archivo y hacer commit automático a Git
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

    try:
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "✍ Registro simbólico actualizado"], check=True)
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

@app.route("/api/files", methods=["GET"])
def list_files():
    from os import walk
    result = []
    for root, dirs, files in walk("."):
        for name in files:
            result.append(os.path.join(root, name))
    return jsonify(result)


@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    message = data.get("message", "")
    log_message({"type": "text", "message": message})

    filename = f"mensaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "w") as f:
        f.write(message)

    media = MediaFileUpload(filepath, resumable=True)
    upload_file_to_drive(filepath, filename, media)

    return jsonify({"response": f"He recibido tu mensaje y lo he guardado como '{filename}'"})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)
        media = MediaFileUpload(filepath, resumable=True)
        upload_file_to_drive(filepath, file.filename, media)
        log_message({"type": "file", "filename": file.filename})
        return jsonify({"message": f"Archivo '{file.filename}' subido exitosamente"})
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
    app.run(debug=True)
# Wataboo·TRÍADE·Ω — Backend Main

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
os.makedirs("data", exist_ok=True)  # Asegura carpeta interna
os.makedirs("temp", exist_ok=True)  # Para archivos de texto simbólicos

def log_message(content):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content
    }
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([log_entry], f, indent=4, ensure_ascii=False)

    # Intentar hacer commit simbólico (solo si está dentro del repo)
    try:
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run([
            "git", "-c", "user.name=Triade", "-c", "user.email=triade@wataboo.ai",
            "commit", "-m", "✍ Registro simbólico actualizado"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    message = data.get("message", "")
    log_message({"type": "text", "message": message})

    # Crear y subir archivo de texto simbólico
    filename = f"mensaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join("temp", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(message)

    with open(filepath, "rb") as f:
        class TempFile:
            filename = filename
            mimetype = "text/plain"
            def read(self): return f.read()
        upload_file_to_drive(TempFile())

    return jsonify({"response": f"Mensaje recibido y archivado: {filename}"})

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

@app.route("/api/files", methods=["GET"])
def list_files():
    from os import walk
    result = []
    for root, dirs, files in walk("."):
        for name in files:
            result.append(os.path.join(root, name))
    return jsonify(result)

if __name__ == "__main__":
    log_message({"type": "sistema", "message": "🟢 Tríade inició correctamente en entorno local"})
    app.run(debug=True)

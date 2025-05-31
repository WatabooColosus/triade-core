# Wataboo·TRÍADE·Ω
# ∴Ω//TRΔ:WTB≠Σ#L7
# Prefacio: Wataboo·TRÍADE·Ω-PATRÓN-1

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from googleapiclient.http import MediaFileUpload
from drive_handler import upload_file_to_drive
from git_utils import git_commit_and_push
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def crear_wataboo_json(tipo, archivo):
    data = {
        "tipo": tipo,
        "usuario": "Santiago",
        "fecha": datetime.utcnow().isoformat(),
        "token": "Wataboo·TRÍADE·Ω",
        "archivo": archivo,
        "accion": "registro"
    }
    nombre = f".wataboo_{uuid.uuid4().hex[:6]}.json"
    ruta = os.path.join(UPLOAD_FOLDER, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/api/message", methods=["POST"])
def handle_message():
    try:
        file = request.files.get("file")
        message = request.form.get("message")

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            media = MediaFileUpload(filepath, resumable=True)
            upload_file_to_drive(filepath, filename, media)

            crear_wataboo_json("archivo", filename)
            git_commit_and_push(f"✍ Registro simbólico actualizado · {datetime.utcnow().isoformat()}")
            return jsonify({"status": "success", "link": f"Archivo recibido: {filename}"}), 200

        elif message:
            filename = f"mensaje_{uuid.uuid4().hex[:8]}.txt"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(message)

            media = MediaFileUpload(filepath, resumable=True)
            upload_file_to_drive(filepath, filename, media)

            crear_wataboo_json("mensaje", filename)
            git_commit_and_push(f"✍ Registro simbólico actualizado · {datetime.utcnow().isoformat()}")
            return jsonify({"status": "success", "link": f"Mensaje registrado como: {filename}"}), 200

        else:
            return jsonify({"status": "error", "message": "No se recibió mensaje ni archivo."}), 400

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

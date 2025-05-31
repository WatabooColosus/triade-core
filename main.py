# Wataboo·TRÍADE·Ω
# ∴Ω//TRΔ:WTB≠Σ#L7
# Prefacio: Wataboo·TRÍADE·Ω-PATRÓN-1

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from googleapiclient.http import MediaFileUpload
from drive_handler import upload_file_to_drive
from git_utils import commit_and_push_changes
from config import UPLOAD_FOLDER
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

            commit_and_push_changes(f"✍ Archivo recibido: {filename}")
            return jsonify({"status": "success", "link": f"Archivo registrado como: {filename}"}), 200

        elif message:
            filename = f"mensaje_{uuid.uuid4().hex[:8]}.txt"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(message)

            media = MediaFileUpload(filepath, resumable=True)
            upload_file_to_drive(filepath, filename, media)

            commit_and_push_changes(f"✍ Mensaje simbólico registrado: {filename}")
            return jsonify({"status": "success", "link": f"Mensaje registrado como: {filename}"}), 200

        else:
            return jsonify({"status": "error", "message": "No se recibió mensaje ni archivo."}), 400

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

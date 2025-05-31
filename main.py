from flask import Flask, request, jsonify
from flask_cors import CORS
from drive_handler import upload_file_to_drive
import os
import json
import datetime
import git

app = Flask(__name__)
CORS(app)

LOG_PATH = os.path.join(os.getcwd(), "triade_log.json")
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def log_message(data):
    now = datetime.datetime.now().isoformat()
    data["timestamp"] = now

    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(data)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    try:
        repo = git.Repo(os.getcwd())
        repo.git.add(LOG_PATH)
        repo.git.commit("-m", "✍ Registro simbólico actualizado")
    except Exception as e:
        print("[GIT ERROR]", e)

@app.route("/api/message", methods=["POST"])
def handle_message():
    if "file" in request.files:
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        class TempFile:
            def __init__(self, filepath, filename):
                self.filepath = filepath
                self.filename = filename

        upload_file_to_drive(TempFile(filepath, file.filename))
        log_message({"type": "file", "filename": file.filename})

        return jsonify({"status": "Archivo recibido y enviado a Drive."})

    elif "message" in request.json:
        message = request.json["message"]
        filename = f"mensaje_{datetime.datetime.now().isoformat()}.txt"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "w") as f:
            f.write(message)

        class TempFile:
            def __init__(self, filepath, filename):
                self.filepath = filepath
                self.filename = filename

        upload_file_to_drive(TempFile(filepath, filename))
        log_message({"type": "text", "message": message})

        return jsonify({"status": "Mensaje recibido y enviado a Drive."})

    return jsonify({"error": "No se recibió ni archivo ni mensaje."}), 400

if __name__ == "__main__":
    app.run(debug=True)

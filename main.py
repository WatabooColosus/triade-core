from flask import Flask, request, jsonify
from flask_cors import CORS
from drive_handler import upload_file_to_drive
import os
import json
import git
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Rutas internas
DATA_PATH = "data"
LOG_PATH = os.path.join(DATA_PATH, "triade_log.json")
TEMP_PATH = os.path.join(DATA_PATH, "temp")

# Asegurar carpetas necesarias
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(TEMP_PATH, exist_ok=True)

# Función: Registro simbólico en archivo y Git
def log_message(message_data):
    # Cargar mensajes existentes
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append({
        "timestamp": datetime.now().isoformat(),
        "data": message_data
    })

    with open(LOG_PATH, "w") as f:
        json.dump(messages, f, indent=2)

    # Intentar subir a Git si es parte del repositorio
    try:
        repo = git.Repo(search_parent_directories=True)
        repo.index.add([LOG_PATH])
        repo.index.commit("✍ Registro simbólico actualizado")
    except Exception as e:
        print(f"[GIT ERROR] {e}")

# Ruta: raíz simple
@app.route("/")
def index():
    return "🧠 Tríade Core API activa"

# Ruta: procesamiento de mensajes y archivos
@app.route("/api/message", methods=["POST"])
def handle_message():
    if "file" in request.files:
        file = request.files["file"]
        file_id, file_url = upload_file_to_drive(file)
        log_message({"type": "archivo", "filename": file.filename, "url": file_url})
        return jsonify({"status": "archivo subido", "url": file_url})

    data = request.get_json()
    message = data.get("message", "")

    # Guardar como archivo de texto temporal
    filename = f"mensaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(TEMP_PATH, filename)
    with open(filepath, "w") as f:
        f.write(message)

    # Crear archivo temporal simulando file-like object
    class TempFile:
        def __init__(self, path, name):
            self.path = path
            self.filename = name
            self.mimetype = "text/plain"
        def read(self):
            with open(self.path, "rb") as f:
                return f.read()

    upload_file_to_drive(TempFile(filepath, filename))
    log_message({"type": "texto", "contenido": message})

    return jsonify({"status": "mensaje recibido", "contenido": message})

# Arranque local (opcional)
if __name__ == "__main__":
    print("🚀 Servidor Flask ejecutándose en local")
    app.run(debug=True)

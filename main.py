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
        subprocess.run(["git", "config", "--global", "user.email", "triade@wataboo.ai"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Tríade Wataboo"], check=True)
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "✍ Registro simbólico actualizado"], check=True)
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

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

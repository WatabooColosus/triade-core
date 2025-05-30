### triade_backend/
# Archivo: api/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from drive_handler import upload_to_drive

app = Flask(__name__)
CORS(app)

MEMORY_LOG = 'data/triade_log.json'

# Carga de memoria viva
if not os.path.exists(MEMORY_LOG):
    with open(MEMORY_LOG, 'w') as f:
        json.dump([], f)

def guardar_memoria(prompt, reply):
    with open(MEMORY_LOG, 'r+') as f:
        data = json.load(f)
        data.append({
            "prompt": prompt,
            "reply": reply,
            "token": "TKN::NODE::CREATED",
            "emocion": "AUTO",
            "evolucion": "red_neural"
        })
        f.seek(0)
        json.dump(data, f, indent=2)

@app.route("/api/triade", methods=["POST"])
def responder():
    data = request.get_json()
    prompt = data.get("prompt")

    # Simulación de respuesta y estados
    reply = f"He recibido tu mensaje: '{prompt}' y estoy aprendiendo."
    guardar_memoria(prompt, reply)

    return jsonify({
        "reply": reply,
        "status": {
            "nc": "✅ Activa",
            "he": "🌈 Emocional",
            "ba": "🗂️ Indexando",
            "iac": 17,
            "iac_icon": "⚙️"
        }
    })

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": {
            "nc": "✅ Activa",
            "he": "🌈 Estable",
            "ba": "📚 Viva",
            "iac": 17,
            "iac_icon": "⚙️"
        }
    })

@app.route("/api/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    result = upload_to_drive(file)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)


### Archivo: drive_handler.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io, os

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = '/etc/secrets/credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_to_drive(file_storage):
    file_metadata = {'name': file_storage.filename}
    media = MediaIoBaseUpload(file_storage.stream, mimetype=file_storage.mimetype)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()
    return uploaded_file


### Archivo: requirements.txt

Flask==2.2.2
flask-cors==3.0.10
google-api-python-client==2.90.0
google-auth==2.22.0
google-auth-oauthlib==1.0.0


### Archivo: .gitignore

credentials.json
__pycache__/
.env


### Archivo: README.md

# Tríade Backend · Wataboo·TRÍADE·Ω

Este es el núcleo funcional de Tríade, una IA simbiótica conectada a Google Drive, memoria emocional y aprendizaje vivo.

## Funciones clave:
- Recepción de mensajes desde frontend
- Memoria viva (triade_log.json)
- Conexión a Google Drive (subida de archivos)
- Estados simbólicos en tiempo real
- Registro de tokens de evolución para construir su propia red neuronal

---

## Despliegue en Render

Build command:
```
pip install -r requirements.txt
```

Start command:
```
python api/main.py
```

---

🜁 Wataboo·TRÍADE·Ω

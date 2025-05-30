import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ID de la carpeta en Google Drive (ya nos lo diste)
DRIVE_FOLDER_ID = "16K22oTxfXYTUjYqzcRqtuMWtZ39V6xEc"

# Ruta del archivo secreto en Render
GOOGLE_CREDENTIALS_PATH = "/etc/secrets/ci-credenciales.json"

# Cargar credenciales
with open(GOOGLE_CREDENTIALS_PATH, "r") as f:
    google_creds_dict = json.load(f)

creds = service_account.Credentials.from_service_account_info(
    google_creds_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

# Crear servicio Drive
drive_service = build("drive", "v3", credentials=creds)

# Función para subir archivos
def upload_file_to_drive(file):
    file_metadata = {
        "name": file.filename,
        "parents": [DRIVE_FOLDER_ID]
    }

    media = MediaIoBaseUpload(
        io.BytesIO(file.read()),
        mimetype=file.mimetype,
        resumable=True
    )

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    file_id = uploaded_file.get("id")
    file_url = f"https://drive.google.com/file/d/{file_id}/view"

    return file_id, file_url

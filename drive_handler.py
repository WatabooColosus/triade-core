# === backend/drive_handler.py ===
import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Carga de credenciales desde variable de entorno (Render)
google_creds_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
google_creds_dict = json.loads(google_creds_str)

credentials = service_account.Credentials.from_service_account_info(
    google_creds_dict,
    scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)

# Puedes definir una carpeta de destino en Drive aquí
FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")  # opcional

def upload_file_to_drive(file):
    file_metadata = {
        'name': file.filename,
    }
    if FOLDER_ID:
        file_metadata['parents'] = [FOLDER_ID]

    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.mimetype)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    file_id = uploaded_file.get('id')
    file_url = f"https://drive.google.com/file/d/{file_id}/view"
    return file_id, file_url
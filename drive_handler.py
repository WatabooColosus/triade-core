# === backend/drive_handler.py ===
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_PATH = '../credentials/credentials.json'

# 👉 Aquí se hace la autenticación con Google Drive
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(file):
    # Carga del archivo a carpeta específica (puedes definir FOLDER_ID)
    file_metadata = {
        'name': file.filename,
        # 👉 Si quieres subir a carpeta específica, descomenta y coloca el ID:
        # 'parents': ['TU_FOLDER_ID_AQUÍ']
    }
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.mimetype)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    file_id = uploaded_file.get('id')
    file_url = f"https://drive.google.com/file/d/{file_id}/view"
    return file_id, file_url

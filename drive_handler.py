import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

GOOGLE_CREDENTIALS_PATH = "/etc/secrets/ci-credenciales.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Leer y cargar credenciales
with open(GOOGLE_CREDENTIALS_PATH, "r") as f:
    google_creds_dict = json.load(f)

credentials = service_account.Credentials.from_service_account_info(
    google_creds_dict,
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)
GOOGLE_FOLDER_ID = "16K22oTxfXYTUjYqzcRqtuMWtZ39V6xEc"

def upload_file_to_drive(filepath, filename, media):
    try:
        # Verificar si el archivo ya existe en la carpeta
        existing_files = drive_service.files().list(
            q=f"'{GOOGLE_FOLDER_ID}' in parents and name = '{filename}' and trashed = false",
            spaces="drive",
            fields="files(id, name)"
        ).execute()

        for file in existing_files.get("files", []):
            drive_service.files().delete(fileId=file["id"]).execute()

        file_metadata = {
            "name": filename,
            "parents": [GOOGLE_FOLDER_ID]
        }
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()

        print("📂 Archivo subido a Drive:", uploaded_file["webViewLink"])
        return uploaded_file["id"], uploaded_file["webViewLink"]

    except HttpError as e:
        print("[Drive ERROR]", e)
        return None, None

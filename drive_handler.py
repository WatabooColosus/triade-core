import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GOOGLE_CREDENTIALS_PATH = "/etc/secrets/ci-credenciales.json"
DRIVE_FOLDER_ID = "16K22oTxfXYTUjYqzcRqtuMWtZ39V6xEc"

with open(GOOGLE_CREDENTIALS_PATH, "r") as f:
    creds_dict = json.load(f)

credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/drive.file"],
)

drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(file_obj):
    file_metadata = {
        "name": file_obj.filename,
        "parents": [DRIVE_FOLDER_ID],
    }
    media = MediaFileUpload(file_obj.filepath)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    print(f"✅ Archivo subido: {uploaded_file.get('webViewLink')}")

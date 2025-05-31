import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Ruta a las credenciales (Render debe montarlas como secret)
GOOGLE_CREDENTIALS_PATH = "/etc/secrets/ci-credenciales.json"
DRIVE_FOLDER_ID = "16K22oTxfXYTUjYqzcRqtuMWtZ39V6xEc"

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(temp_file):
    file_metadata = {
        "name": temp_file.name,
        "parents": [DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(temp_file.path, mimetype="text/plain")

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()

    print(f"✅ Archivo subido: {uploaded_file.get('webViewLink')}")

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

GOOGLE_CREDENTIALS_PATH = "/etc/secrets/ci-credenciales.json"  # debe coincidir exactamente
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

with open(GOOGLE_CREDENTIALS_PATH, "r") as f:
    google_creds_dict = json.load(f)
    creds = service_account.Credentials.from_service_account_info(google_creds_dict, scopes=SCOPES)

drive_service = build("drive", "v3", credentials=creds)

def upload_file_to_drive(file_obj):
    file_metadata = {"name": file_obj.filename}
    media = {"mimeType": "application/octet-stream", "body": file_obj.read()}
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
    return uploaded_file.get("id"), uploaded_file.get("webViewLink")

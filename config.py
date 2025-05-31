import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "uploads"

# Configuración de Git
GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL", "agenciadigitalwataboo@gmail.com")
GIT_USER_NAME = os.getenv("GIT_USER_NAME", "WatabooColosus")
GIT_TARGET_BRANCH = os.getenv("GIT_BRANCH", "main")

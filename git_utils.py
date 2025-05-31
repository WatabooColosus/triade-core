# git_utils.py
import os
import subprocess

GIT_USER_NAME = "WatabooColosus"
GIT_USER_EMAIL = "agenciadigitalwataboo@gmail.com"

def git_commit_and_push(message="✍ Registro simbólico actualizado"):
    try:
        subprocess.run(["git", "config", "--global", "user.email", GIT_USER_EMAIL], check=True)
        subprocess.run(["git", "config", "--global", "user.name", GIT_USER_NAME], check=True)

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("🚀 Push realizado correctamente.")
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

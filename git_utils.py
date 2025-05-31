# === git_utils.py ===
import subprocess

def push_to_git(message):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "agenciadigitalwataboo@gmail.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "WatabooColosus"], check=True)

        subprocess.run(["git", "add", "uploads"], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Cambios enviados al repositorio remoto.")

    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)
        return False

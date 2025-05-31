import subprocess
from config import GIT_USER_EMAIL, GIT_USER_NAME, GIT_TARGET_BRANCH

def commit_and_push_changes(commit_message):
    try:
        subprocess.run(["git", "config", "--global", "user.email", GIT_USER_EMAIL], check=True)
        subprocess.run(["git", "config", "--global", "user.name", GIT_USER_NAME], check=True)
        subprocess.run(["git", "add", "uploads"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", GIT_TARGET_BRANCH], check=True)
        print("✅ Cambios subidos a Git con éxito.")
    except subprocess.CalledProcessError as e:
        print("[GIT ERROR]", e)

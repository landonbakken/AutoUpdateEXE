from pathlib import Path
import os
import requests
import subprocess
import json

with open("config.json", "r") as file:
    config = json.load(file)

#file system setup
EXE_DIR = Path(os.getenv("APPDATA")) / config["DIR"]
EXE_DIR.mkdir(parents=True, exist_ok=True)
EXE = config["EXE"]
DATA_FILE = EXE_DIR / "version.txt"
EXE_PATH = EXE_DIR / EXE

#repo setup
RELEASE_URL = f"https://api.github.com/repos/{config["USER"]}/{config["REPO"]}/releases/latest"

#get the local version
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        localVersion = f.read()
else:
    localVersion = -1
    
headers = {"User-Agent": "PythonScript"}
response = requests.get(RELEASE_URL, headers=headers)
release = response.json()
gitVersion = release["tag_name"]

#update
if gitVersion != localVersion:
    #get the exe info
    exe_asset = None
    for asset in release["assets"]:
        if asset["name"].endswith(".exe"):
            exe_asset = asset
            break
    download_url = exe_asset["browser_download_url"]
    
    #download it
    r = requests.get(download_url)
    with open(EXE_PATH, "wb") as f:
        f.write(r.content)
    
    #update version
    with open(DATA_FILE, "w") as f:
        f.write(gitVersion)
    
subprocess.run([EXE_PATH])
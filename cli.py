import requests
import json
import os
import shutil
from art import *

TO_ROOT = os.getcwd()
TO_MODS = "E:/ReadyOrNot/ReadyOrNot/Content/Paks/"
TO_REPO = "E:/ReadyOrNot/ReadyOrNot/Content/Paks/REPO/"
VANILLA = ["mod.io",
           "pakchunk0-WindowsNoEditor.pak",
           "pakchunk1-WindowsNoEditor.pak",
           "pakchunk2-WindowsNoEditor.pak",
           "pakchunk3-WindowsNoEditor.pak",
           "pakchunk4-WindowsNoEditor.pak",
           "pakchunk5-WindowsNoEditor.pak",
           "pakchunk6-WindowsNoEditor.pak",
           "pakchunk7-WindowsNoEditor.pak",
           "pakchunk8-WindowsNoEditor.pak",
           "pakchunk9-WindowsNoEditor.pak",
           "pakchunk10-WindowsNoEditor.pak",
           "pakchunk11-WindowsNoEditor.pak",
           "pakchunk12-WindowsNoEditor.pak",
           "pakchunk13-WindowsNoEditor.pak",
           "pakchunk14-WindowsNoEditor.pak",
           "pakchunk15-WindowsNoEditor.pak",
           "pakchunk16-WindowsNoEditor.pak",
           "pakchunk17-WindowsNoEditor.pak",
           "pakchunk18-WindowsNoEditor.pak",
           "pakchunk19-WindowsNoEditor.pak",
           "pakchunk20-WindowsNoEditor.pak",
           "REPO"]

class User:
    def __init__(self, user_name: str, user_id: str = None):
        self.user_name = user_name
        self.user_id = user_id

def active_mod(mod_name) -> None:
    os.chdir(TO_REPO)
    shutil.copy(mod_name, TO_MODS)

def list_mods() -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/mods"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    mods = json.loads(response.text).get('body')
    REMOTE = json.loads(mods)

    return REMOTE

def upload(file_name) -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/mods"

    data = { 
        "file_name": f"{file_name}"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response = json.loads(response.text)
    response = json.loads(response.get('body'))

    object_name = response.get('object_name')
    presigned_url = response.get('presigned_url')
    fields = response.get('fields')

    url = presigned_url.get('url')
    fields = presigned_url.get('fields')

    with open(TO_MODS + file_name, 'rb') as f:
        files = {'file': (file_name, f)}
        http_response = requests.post(url, data=fields, files=files)

    print(f'{file_name} upload HTTP status code: {http_response.status_code}')

def download(file_name) -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/mods"

    data = {
        "key": f"{file_name}"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.patch(url, data=json.dumps(data), headers=headers)
    
    response = json.loads(response.text)
    response = json.loads(response.get('body'))

    presigned_url = response.get('presigned_url')
    fields = response.get('fields')

    response = requests.get(presigned_url, data=fields)
    if response.status_code == 200:
        os.chdir(TO_REPO)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"{file_name} downloaded")
    else:
        print('Download failed')

def register() -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/user"

    user_name = input("Enter your user name: ")
    data = { 
        "user_name": f"{user_name}"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print("Created account")

def login() -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/user"

    user_name = input("Enter your user name: ")
    data = {
        "user_name": f"{user_name}"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, data=json.dumps(data), headers=headers)
    response = json.loads(response.text)

    userData = response.get('body')
    userData = json.loads(userData)

    user = User(userData.get('UserName'), userData.get('UserID'))

    return user

def start_sync(ACTIVE) -> None:
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/session"

    session_id = input("Enter session ID: ")
    data = {
        "session_id": f"{session_id}",
        "mod_list": ACTIVE
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, data=json.dumps(data), headers=headers)

    print(response.text)

def join_sync() -> None:
    session_id = input("Enter session ID: ")
    url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/session"
    data = {
        "session_id": session_id
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, data=json.dumps(data), headers=headers)
    response = json.loads(response.text)
    response = json.loads(response.get('body'))
    response = response[0]
    
    SYNC_LIST = response.get('ModList')

    return SYNC_LIST

def splash_screen() -> None:
    Art = text2art("Mod-Man")
    print(Art)

def main() -> None:
    splash_screen()

    print("1. Login")
    print("2. Register")
    print("3. Exit")
    
    choice = input("Enter choice: ")

    if choice == "1":
        user = login()

        ACTIVE = []
        REPO = []

        os.chdir(TO_MODS)
        for data in os.listdir():
            if data not in VANILLA:
                ACTIVE.append(data)

        os.chdir(TO_REPO)
        for data in os.listdir():
            REPO.append(data)

        print("1. Start sync")
        print("2. Join sync")

        choice = input("Enter choice: ")

        if choice == "1":
            REMOTE = list_mods()
            start_sync(ACTIVE)

            for mod in ACTIVE:
                if mod not in REMOTE:
                    upload(mod)

        elif choice == "2":
            SYNC_LIST = join_sync()
            REMOTE = list_mods()

            for mod in SYNC_LIST:
                if mod not in ACTIVE:
                    if mod in REPO:
                        active_mod(mod)
                    else:
                        if mod in REMOTE:
                            download(mod)
                            active_mod(mod)

    elif choice == "2":
        register()

    elif choice == "3":
        exit()

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
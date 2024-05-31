import requests
import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from art import *


class ReadyOrMod:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("ReadyOrMod")
        root.geometry("800x600")

        self.ACTIVE = []
        self.SYNC_LIST = []
        self.REPO = []
        self.REMOTE = []

        self.TO_ROOT = ""
        self.TO_MODS = ""
        self.TO_REPO = ""

        self.VANILLA = ["mod.io",
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


        # Function -> Select Directory
        def select_directory() -> None:
            directory = filedialog.askdirectory()
            if directory:
                text_field.config(state="normal")
                text_field.delete(0, tk.END)
                text_field.insert(0, directory)
                text_field.config(state="readonly")
            else:
                self.update_message_box("No directory selected...select game directory to continue\n")
                

            # CONFIGURE THE DIRECTORIES
            self.TO_ROOT = directory
            self.TO_MODS = os.path.join(self.TO_ROOT, "ReadyOrNot", "Content", "Paks")
            self.TO_REPO = os.path.join(self.TO_ROOT, "ReadyOrNot", "Content", "Paks", "REPO")

            # check if the REPO folder exists -> if not, create it
            if not os.path.exists(self.TO_REPO):
                os.makedirs(self.TO_REPO) # Create the REPO folder
                self.REPO = [] # Empty list as there are no mods in the REPO folder
            else:
                self.REPO = os.listdir(self.TO_REPO) # List all mods in the REPO folder

            # add all mods that are currently active -> in the MODS folder -> to the ACTIVE list
            for data in os.listdir(self.TO_MODS):
                if data not in self.VANILLA:
                    self.ACTIVE.append(data)

            # Update the message box
            self.update_message_box(f"Game directory: {directory}")

            # List all mods in the local REPO 
            self.update_message_box(f"Mods in local REPO: \n")
            for mod in self.REPO:
                self.update_message_box(f"{mod}")
            self.update_message_box(f"================\n")

            # List all active mods
            self.update_message_box(f"ACTIVE mods: \n")
            for mod in self.ACTIVE:
                self.update_message_box(f"{mod}")
            self.update_message_box(f"================\n")


        def get_session_id() -> str:
                """
                Function to get the session ID from the user
                """
                session_id = tk.simpledialog.askstring("Session ID", "Enter the session ID:")
                return session_id


        # Function -> Select Mods
        def create_session_add_new() -> None:
            # Check if the repository directory has been selected
            if os.path.exists(self.TO_REPO): 
                file_paths = filedialog.askopenfilenames(
                    initialdir=self.TO_REPO,  # Start in the REPO folder
                    title="Select Mod Files",
                    filetypes=[("PAK files", "*.pak")]  # Allow all file types and .pak
                )

            # If files were selected
            if file_paths:  
                # extract only the file names from the full path
                file_names = [os.path.basename(path) for path in file_paths]
                
                for mod in file_names:
                    self.ACTIVE.append(mod)  # Add the selected files to the ACTIVE list

            self.update_message_box(f"Resetting mod status to Vanilla...\n")
            self.update_message_box(f"================\n")

            # reset mod configuration to Vanilla
            os.chdir(self.TO_MODS)
            for data in os.listdir():
                if data not in self.VANILLA:
                    os.remove(data)
            
            self.update_message_box(f"Activating selected mods...\n")
            self.update_message_box(f"================\n")

            # activate the selected mods
            for mod in self.ACTIVE:
                self.activate_mod(mod)

            self.REMOTE = self.list_mods()  # List all mods in the S3 bucket

            # synchronize the ACTIVE list with the REMOTE list
            # if new mod has been added by the user that is not present in remote
            self.update_message_box(f"Synchronizing with remote...\n")
            for mod in self.ACTIVE:
                if mod not in self.REMOTE:
                    self.update_message_box(f"Uploading {mod} to remote...\n")
                    self.upload(mod)  # Upload the mod to the S3 bucket
                else:
                    self.update_message_box(f"{mod} already exists in remote...\n")
            
            self.update_message_box(f"Sync complete\n")
            self.update_message_box(f"================\n")

            # Update the message box
            self.update_message_box(f"ACTIVE mods: \n")
            for mod in self.ACTIVE:
                self.update_message_box(f"{mod}")

            # Get the session ID from the user to set as join key
            session_id = get_session_id()

            # Create a new session with the ACTIVE list
            self.start_sync(self.ACTIVE)
            self.update_message_box(f"Session created with ID: {session_id}\n")

        # Function -> Add Existing Mods
        def create_session_add_existing() -> None:
            self.REMOTE = self.list_mods()  # List all mods in the S3 bucket

            # synchronize the ACTIVE list with the REMOTE list
            # if new mod has been added by the user that is not present in remote
            self.update_message_box(f"Synchronizing with remote...\n")
            for mod in self.ACTIVE:
                if mod not in self.REMOTE:
                    self.update_message_box(f"Uploading {mod} to remote...\n")
                    self.upload(mod)  # Upload the mod to the S3 bucket
                else:
                    self.update_message_box(f"{mod} already exists in remote...\n")
            
            self.update_message_box(f"Sync complete\n")
            self.update_message_box(f"================\n")

            # list ACTIVE mods
            self.update_message_box(f"ACTIVE mods: \n")
            for mod in self.ACTIVE:
                self.update_message_box(f"{mod}")
                self.update_message_box(f"================\n")

            # Get the session ID from the user to set as join key
            session_id = get_session_id()

            # Create a new session with the ACTIVE list
            self.start_sync(self.ACTIVE)
            self.update_message_box(f"Session created with ID: {session_id}\n")


        def join_session() -> None:
            # Get the session ID from the user to join the session
            session_id = get_session_id()

            # Join the session with the provided session ID
            self.update_message_box(f"Joining session with ID: {session_id}\n")

            # Get the list of mods in the session
            self.SYNC_LIST = self.join_sync(session_id)

            # Get the list of mods in the remote S3 bucket
            self.REMOTE = self.list_mods()

            self.update_message_box(f"Synchronizing mods...\n")

            for mod in self.SYNC_LIST:
                if mod not in self.ACTIVE:
                    if mod in self.REPO:
                        self.update_message_box(f"Activating {mod}...\n")
                        self.activate_mod(mod)

                    else:
                        if mod in self.REMOTE:
                            self.update_message_box(f"Downloading {mod}...\n")
                            self.download(mod)

                            self.update_message_box(f"Activating {mod}...\n")
                            self.activate_mod(mod)

                self.update_message_box(f"{mod} already active\n")

            self.update_message_box(f"Sync complete\n")
            self.update_message_box(f"================\n")


        # Header for ASCII art
        header_frame = tk.Frame(root, bg="#000000")  # Black background for better contrast
        header_frame.pack(fill=tk.X)

        # ASCII art
        art = text2art("ReadyOrMod")
        ascii_label = tk.Label(header_frame, text=art, fg="#FFFFFF", bg="#000000", font=("Courier", 12))
        ascii_label.pack()

        # Subheader Frame -> Directory selection
        subheader_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=5)
        subheader_frame.pack(fill=tk.X)  # Fill horizontally

        # Text Field -> Directory path
        text_field = tk.Entry(subheader_frame, width=50, state="readonly")  # Uneditable
        text_field.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Button -> Select Directory
        button = tk.Button(subheader_frame, text="Select Directory", command=select_directory, font=("Arial", 10))
        button.pack(side=tk.LEFT)

        # Content frame
        content_frame = tk.Frame(root)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left content frame
        left_frame = tk.Frame(content_frame, bg="#ffffff", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Expand to fill

        # Divider
        divider = tk.Frame(content_frame, width=2, bg="#808080")  # Gray divider
        divider.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))  # Stick to left, fill vertically

        # Right content frame
        right_frame = tk.Frame(content_frame, bg="#ffffff", padx=10, pady=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Expand to fill 

        # Buttons
        # Create Session -> Add New
        create_session_button_add_new = tk.Button(left_frame, text="Create Session (Add New)", command=create_session_add_new, width=20, height=2, font=("Arial", 14))
        create_session_button_add_new.pack(pady=(0, 10))
        # create_session_button_add_new.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create Session -> Add Existing
        create_session_button_add_existing = tk.Button(left_frame, text="Create Session (Add Existing)", command=create_session_add_existing, width=20, height=2, font=("Arial", 14))
        # create_session_button_add_existing.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        create_session_button_add_existing.pack()

        # Join Session
        join_session_button = tk.Button(right_frame, text="Join Session", command=join_session, width=20, height=2, font=("Arial", 14))
        join_session_button.pack(pady=(0, 10))

        # Message Box
        message_frame = tk.Frame(root, bg="#f0f0f0")  # Light gray background
        message_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        self.message_text = tk.Text(message_frame, wrap=tk.WORD, state="disabled") 
        self.message_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_message_box("Select the game directory to begin...")


    def update_message_box(self, message: str) -> None:
        """
        Function to simplify updating the message box

        Args:
            message (str): The message to display
        """
        self.message_text.config(state="normal")
        self.message_text.insert(tk.END, message + "\n")
        self.message_text.see(tk.END)
        self.message_text.config(state="disabled")


    def activate_mod(self, mod_name: str) -> None:
        """
        Copy the mod from the REPO folder
        to the MODS folder to activate it

        Args:
            mod_name (str): The name of the mod to activate
        """
        os.chdir(self.TO_REPO)
        shutil.copy(mod_name, self.TO_MODS)


    def list_mods() -> list[str]:
        """
        List all mods in the S3 bucket
        
        Returns:
            list[str]: The list of mods in the S3 bucket folder
        """
        url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/mods"
        headers = {'Content-Type': 'application/json'}

        response = requests.get(url, headers=headers)

        mods = json.loads(response.text).get('body')
        REMOTE = json.loads(mods)

        return REMOTE


    def start_sync(self, ACTIVE: list[str]) -> None:
        """
        Start the synchronization process by creating a new session with the ACTIVE list

        Args:
            ACTIVE (list[str]): The list of active mods
        """
        url = "https://aizl9103i1.execute-api.ca-central-1.amazonaws.com/test/session"

        session_id = input("Enter session ID: ")
        data = {
            "session_id": f"{session_id}",
            "mod_list": ACTIVE
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.put(url, data=json.dumps(data), headers=headers)

        self.update_message_box(f"{response.text}")


    def join_sync(self, session_id: str) -> list[str]:
        """
        Join an existing synchronization session by providing the session ID and getting the mod list

        Args:
            session_id (str): The session ID to join

        Returns:
            list[str]: The list of mods in the synchronization session
        """
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


    def upload(self, file_name: str) -> None:
        """
        Upload a mod to the S3 bucket given the file name

        Args:
            file_name (str): The name of the file to upload
        """
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

        with open(self.TO_MODS + file_name, 'rb') as f:
            files = {'file': (file_name, f)}
            http_response = requests.post(url, data=fields, files=files)

        self.update_message_box(f"{file_name} upload HTTP status code: {http_response.status_code}")


    def download(self, file_name: str) -> None:
        """
        Download a mod from the S3 bucket given the file name
        
        Args:
            file_name (str): The name of the file to download
        """
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
            os.chdir(self.TO_REPO)
            with open(file_name, 'wb') as f:
                f.write(response.content)
            self.update_message_box(f"{file_name} downloaded")
        else:
            self.update_message_box(f"Download failed -> {file_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReadyOrMod(root)
    root.mainloop()
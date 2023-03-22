import json
import os

import customtkinter
import requests as requests


class Update:
    def __init__(self, app):
        self.app = app

        self.updates_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.updates_frame_1.grid_columnconfigure(0, weight=1)

        self.updates_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.updates_frame_2.grid_columnconfigure(0, weight=1)

        self.upd_libraries_group = customtkinter.CTkLabel(self.updates_frame_1, corner_radius=0, text="Libraries:")
        self.upd_libraries_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_group = customtkinter.CTkLabel(self.updates_frame_2, corner_radius=0, text="Application:")
        self.upd_application_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_libraries_button = customtkinter.CTkButton(self.updates_frame_1, text="Update Libraries",
                                                            command=self.update_libs)
        self.upd_libraries_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_folder_button = customtkinter.CTkButton(self.updates_frame_1, text="Open Folder",
                                                         command=self.open_folder)
        self.upd_folder_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_button = customtkinter.CTkButton(self.updates_frame_2, text="Update Application")
        self.upd_application_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.path+"\\lib"))

    def update_libs(self):
        answer = requests.get("https://api.github.com/repos/Lazy-World/warframe-ahk/contents/libraries").content
        json_answer = json.loads(answer.decode("utf-8"))
        # pprint(json_answer)
        for item in json_answer:
            if item["name"] != "game_settings.ahk":
                filename = self.app.path+"\\lib\\" + item["name"]
                r = requests.get(item["download_url"])
                with open(filename, 'wb') as f:
                    f.write(r.content)

import json
import os

import customtkinter
import requests as requests


class Workshop:
    def __init__(self, app):
        self.app = app

        self.scripts = {}

        self.workshop_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.workshop_frame_1.grid_columnconfigure(0, weight=1)

        self.workshop_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.workshop_frame_2.grid_columnconfigure(0, weight=1)

        self.ws_script_list = customtkinter.CTkScrollableFrame(self.workshop_frame_1, label_text="Workshop Scripts")
        self.ws_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.scrollable_frame_switches_2 = []

        self.ws_load_button = customtkinter.CTkButton(self.workshop_frame_1, text="Download Selected Items",
                                                      command=self.download_workshop)
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.ws_explorer_button = customtkinter.CTkButton(self.workshop_frame_2, text="Open Folder",
                                                          command=self.open_folder)
        self.ws_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.ws_refresh_button = customtkinter.CTkButton(self.workshop_frame_2, text="Refresh List",
                                                         command=self.refresh)
        self.ws_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.refresh()

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.path+"\\workshop"))

    def get_names(self):
        answer = requests.get("https://api.github.com/repos/Lazy-World/warframe-ahk/contents/").content
        json_answer = json.loads(answer.decode("utf-8"))
        for item in json_answer:
            if item["name"][-3:] == "ahk":
                self.scripts[item["name"]] = item["download_url"]

    def download_workshop(self):
        for switch in self.scrollable_frame_switches_2:
            if switch.get() == 1:
                filename = self.app.path + "\\workshop\\" + switch._text
                r = requests.get(self.scripts[switch._text])
                with open(filename, 'wb') as f:
                    f.write(r.content)
        self.app.active_scripts_window.refresh()

    def refresh(self):
        if self.scrollable_frame_switches_2:
            for switch in self.scrollable_frame_switches_2:
                switch.destroy()
            self.scrollable_frame_switches_2.clear()
        self.get_names()
        for i, name in enumerate(self.scripts.keys()):
            switch = customtkinter.CTkCheckBox(master=self.ws_script_list, text=name)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            self.scrollable_frame_switches_2.append(switch)
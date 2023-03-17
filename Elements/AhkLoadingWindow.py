import getpass
import json
import os
import threading
import customtkinter
import win32api
from Elements.ctk_toplevel import CTkToplevel


def find_autohotkey():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    name = "AutoHotkey.exe"
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            if name in files:
                return os.path.join(root, name)


class AhkLoadingWindow(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.geometry("300x100")
        self.title("LazyHub")
        self.label_1 = customtkinter.CTkLabel(self, text="Trying to find AutoHotkey.exe on your PC...")
        self.label_1.pack(side="top", padx=20, pady=20)
        self.path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.main_app = main_app
        self.iconbitmap("cat.ico")
        threading._start_new_thread(self.generate_ini, ())

    def generate_ini(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(self.path + "\\hub.ini"):
            self.main_app.ahk = find_autohotkey()
            with open(self.path + "\\hub.ini", "w") as file:
                self.main_app.json_settings = {"Version": "3.0", "ahk_path": self.main_app.ahk}
                json.dump(self.main_app.json_settings, file)

        with open(self.path + "\\hub.ini", "r") as file:
            self.main_app.json_settings = json.load(file)

        if "ahk_path" not in self.main_app.json_settings.keys():
            self.main_app.ahk = find_autohotkey()
            self.main_app.json_settings["ahk_path"] = self.main_app.ahk
            with open(self.path + "\\hub.ini", "w") as file:
                json.dump(self.main_app.json_settings, file)
        else:
            self.main_app.ahk = self.main_app.json_settings["ahk_path"]
        self.main_app.ini = open(self.path + "\\hub.ini", 'r')
        self.main_app.active_scripts_window.path_label.configure(text="AutoHotkey.exe path: "+self.main_app.ahk)
        self.main_app.loading_finished()

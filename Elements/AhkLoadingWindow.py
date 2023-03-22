import getpass
import json
import os
import threading
import customtkinter
import win32api
from Elements.ctk_toplevel import CTkToplevel
from _tkinter import TclError


class AhkLoadingWindow(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.geometry("300x100")
        self.title("LazyHub")
        self.resizable(width=False, height=False)
        self.label_1 = customtkinter.CTkLabel(self, text="Trying to find AutoHotkey.exe on your PC...")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
        self.label_2 = customtkinter.CTkLabel(self, text="Current dir: ", justify="left")
        self.label_2.grid(row=1, column=0, padx=10, sticky="w")
        self.label_3 = customtkinter.CTkLabel(self, text="", width=200)
        self.label_3.grid(row=1, column=1)
        self.path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.main_app = main_app
        self.iconbitmap("cat.ico")
        threading._start_new_thread(self.generate_ini, ())

    def generate_ini(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(self.path + "\\hub.ini"):
            self.main_app.ahk = self.find_autohotkey()
            with open(self.path + "\\hub.ini", "w") as file:
                self.main_app.json_settings = {"Version": "3.0", "ahk_path": self.main_app.ahk}
                json.dump(self.main_app.json_settings, file)

        with open(self.path + "\\hub.ini", "r") as file:
            try:
                self.main_app.json_settings = json.load(file)
            except:
                self.main_app.ahk = self.find_autohotkey()
                self.main_app.json_settings = {"Version": "3.0", "ahk_path": self.main_app.ahk}

        if "ahk_path" not in self.main_app.json_settings.keys() or self.main_app.json_settings["ahk_path"] is None \
                or not self.main_app.json_settings["ahk_path"]:
            self.main_app.ahk = self.find_autohotkey()
            self.main_app.json_settings["ahk_path"] = self.main_app.ahk
            with open(self.path + "\\hub.ini", "w") as file:
                json.dump(self.main_app.json_settings, file)
        else:
            self.main_app.ahk = self.main_app.json_settings["ahk_path"]
        self.main_app.ini = open(self.path + "\\hub.ini", 'r')
        if len(self.main_app.ahk) > 30:
            text = self.main_app.ahk[:self.main_app.ahk.find("\\") + 1] + "...\\" + \
                   self.main_app.ahk[self.main_app.ahk.rfind("\\") + 1:]
        else:
            text = self.main_app.ahk
        self.main_app.active_scripts_window.path_label.configure(text="AutoHotkey.exe path: " + text, cursor="hand2")
        self.main_app.active_scripts_window.path_label.bind("<Button-1>", self.main_app.open_path)
        if self.winfo_exists():
            self.main_app.loading_finished()

    def find_autohotkey(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        name = "AutoHotkey.exe"
        for drive in drives:
            for root, dirs, files in os.walk(drive):
                path = os.path.join(root)
                if path.count("\\") > 1:
                    extra_path = "...\\"
                else:
                    extra_path = ""
                label_text = drive + extra_path + path[path.rfind("\\") + 1:]
                if len(label_text) > 30:
                    label_text = label_text[:30] + "..."
                try:
                    self.label_3.configure(text=label_text, anchor="w")
                except TclError:
                    pass

                if name in files:
                    return os.path.join(root, name)

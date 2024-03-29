import json
import os
import customtkinter
import win32api
from Elements.ctk_toplevel import CTkToplevel
from _tkinter import TclError


class AhkLoadingWindow(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.geometry("300x100")
        self.title("LazyHub")
        self.geometry(f"+{main_app.winfo_rootx()}+{main_app.winfo_rooty()}")
        self.resizable(width=False, height=False)
        self.withdraw()
        self.grab_set()
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Trying to find AutoHotkey.exe on your PC...")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

        self.label_2 = customtkinter.CTkLabel(self.main_frame, text="Current dir: ", justify="left")
        self.label_2.grid(row=1, column=0, padx=10, sticky="w")

        self.label_3 = customtkinter.CTkLabel(self.main_frame, text="", width=200)
        self.label_3.grid(row=1, column=1)

        self.main_app = main_app
        self.iconbitmap("assets\\cat.ico")

    def generate_ini(self):
        if not os.path.exists(self.main_app.workshop_path+"\\hub.ini"):
            self.main_app.ahk = self.find_autohotkey()
            self.main_app.json_settings = {"Version": self.main_app.version, "ahk_path": self.main_app.ahk,
                                           "theme": "System"}
        else:
            with open(self.main_app.workshop_path+"\\hub.ini", "r") as file:
                try:
                    self.main_app.json_settings = json.load(file)
                except json.JSONDecodeError:
                    self.main_app.ahk = self.find_autohotkey()
                    self.main_app.json_settings = {"Version": self.main_app.version, "ahk_path": self.main_app.ahk,
                                                   "theme": customtkinter.get_appearance_mode()}

        if "ahk_path" not in self.main_app.json_settings.keys() or self.main_app.json_settings["ahk_path"] is None \
                or not self.main_app.json_settings["ahk_path"]:
            self.main_app.ahk = self.main_app.json_settings["ahk_path"] = self.find_autohotkey()
        else:
            self.main_app.ahk = self.main_app.json_settings["ahk_path"]

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
        self.deiconify()
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
                    self.main_app.json_settings = {"Version": self.main_app.version,
                                                   "theme": "System"}
                    raise Exception

                if name in files:
                    return os.path.join(root, name)

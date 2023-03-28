import subprocess
from os import listdir
from os.path import isfile, join
from tkinter.filedialog import askopenfilename
import customtkinter
import os


class ActiveScripts:
    def __init__(self, app):
        self.app = app

        self.scripts = []

        self.active_scripts = []

        self.active_scripts_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_1.grid_columnconfigure(0, weight=1)
        self.active_scripts_frame_1.grid_rowconfigure(0, weight=1)

        self.active_scripts_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_2.grid_columnconfigure(0, weight=1)

        self.as_script_list = customtkinter.CTkScrollableFrame(self.active_scripts_frame_1, label_text="Your Scripts")
        self.as_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.scrollable_frame_switches = []

        self.as_load_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Load Selected Items",
                                                      command=self.load_script)
        self.as_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.as_delete_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Delete Selected Items",
                                                        command=self.delete_script)
        self.as_delete_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.as_explorer_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Open Folder",
                                                          command=self.open_folder)
        self.as_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_refresh_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Refresh List",
                                                         command=self.refresh)
        self.as_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_unload_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Unload All",
                                                        command=self.unload_all)
        self.as_unload_button.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_editpath_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Edit Ahk Path",
                                                          command=self.edit_path)
        self.as_editpath_button.grid(row=3, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.path_label = customtkinter.CTkLabel(self.active_scripts_frame_1,
                                                 text="AutoHotkey.exe path: ")
        self.path_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.workshop_path))

    def get_names(self):
        return [f for f in listdir(self.app.workshop_path) if
                isfile(join(self.app.workshop_path, f))]

    def refresh(self):
        if self.scrollable_frame_switches:
            for switch in self.scrollable_frame_switches:
                switch.destroy()
            self.scrollable_frame_switches.clear()
        self.scripts = self.get_names()
        for i, name in enumerate(self.scripts):
            switch = customtkinter.CTkCheckBox(master=self.as_script_list, text=name)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            self.scrollable_frame_switches.append(switch)

    def load_script(self):
        for switch in self.scrollable_frame_switches:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                subprocess.Popen([self.app.ahk, filename])

    def delete_script(self):
        for switch in self.scrollable_frame_switches:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                os.remove(filename)
        self.refresh()

    def unload_all(self):
        process_name = self.app.ahk[self.app.ahk.rfind("\\") + 1:]
        subprocess.Popen(["taskkill", "/F", "/IM", process_name])

    def edit_path(self):
        path = askopenfilename()
        if not path:
            return
        path = path.replace("/", "\\")
        self.app.ahk = path
        self.app.json_settings["ahk_path"] = path
        if len(self.app.ahk) > 30:
            text = self.app.ahk[:self.app.ahk.find("\\") + 1] + "...\\" + \
                   self.app.ahk[self.app.ahk.rfind("\\") + 1:]
        else:
            text = self.app.ahk
        self.app.active_scripts_window.path_label.configure(text="AutoHotkey.exe path: " + text, cursor="hand2")
        self.app.active_scripts_window.path_label.bind("<Button-1>", self.app.open_path)

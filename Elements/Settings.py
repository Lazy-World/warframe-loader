import os
import tkinter
import webbrowser

import customtkinter

from Elements.ConfirmationPopup import ConfirmationPopup


class Settings:
    def __init__(self, app):
        self.app = app
        self.settings_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.settings_frame_1.grid_columnconfigure(0, weight=1)
        self.settings_frame_1.grid_rowconfigure(0, weight=1)

        self.settings_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.settings_frame_2.grid_columnconfigure(0, weight=1)

        self.items_list = customtkinter.CTkScrollableFrame(self.settings_frame_1)
        self.items_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew", columnspan=2)
        self.changes = []

        self.save_button = customtkinter.CTkButton(self.settings_frame_1, text="Save changes", state="disabled",
                                                   command=self.save)
        self.save_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), columnspan=2, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.settings_frame_1, text="AHK key names:")
        self.label_1.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="w")

        self.label_2 = customtkinter.CTkLabel(self.settings_frame_1,
                                              text="https://www.autohotkey.com/docs/v1/KeyList.htm",
                                              cursor="hand2")
        self.label_2.grid(row=3, column=0, padx=(20, 10), sticky="w")

        self.label_3 = customtkinter.CTkLabel(self.settings_frame_1,
                                              text="https://www.autohotkey.com/docs/v1/Hotkeys.htm",
                                              cursor="hand2")
        self.label_3.grid(row=4, column=0, padx=(20, 10), sticky="w")

        self.label_2.bind("<Button-1>", lambda x: webbrowser.open(self.label_2.cget("text")))
        self.label_3.bind("<Button-1>", lambda x: webbrowser.open(self.label_3.cget("text")))

        self.upd_settings_button = customtkinter.CTkButton(self.settings_frame_2, text="Update game settings",
                                                           command=self.update_libs)
        self.upd_settings_button.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.open_folder_button = customtkinter.CTkButton(self.settings_frame_2, text="Open Folder",
                                                          command=self.open_folder)
        self.open_folder_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.lines = None
        self.generate_settings()

        self.confirm_window = ConfirmationPopup(self.app)
        self.confirm_window.withdraw()

    def generate_settings(self):
        self.lines = None
        self.changes = []
        settings = self.app.lib_path + "\\" + "game_settings.ahk"
        if os.path.isfile(settings):
            with open(settings, "r") as file:
                self.lines = file.readlines()
        if self.lines:
            for i, line in enumerate(self.lines):
                if line == "\n":
                    self.changes.append(line)
                    continue
                if "=" not in line:
                    label = customtkinter.CTkLabel(self.items_list, text=line[line.rfind(";") + 1:],
                                                   font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=i, column=0, pady=5, sticky="w", columnspan=2)
                    self.changes.append(line)
                else:
                    label = customtkinter.CTkLabel(self.items_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    placeholder = tkinter.StringVar(value=line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    placeholder.trace("w", lambda x, y, z: self.text_callback())
                    dialog = customtkinter.CTkEntry(self.items_list, textvariable=placeholder,
                                                    placeholder_text=label.cget("text"))

                    dialog.grid(row=i, column=1, padx=50, pady=5)
                    self.changes.append(dialog)

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.lib_path))

    def update_libs(self):
        self.confirm_window.geometry(f"+{self.app.winfo_rootx() + 500}+{self.app.winfo_rooty()}")
        self.confirm_window.grab_set()
        self.confirm_window.deiconify()

    def save(self):
        settings = self.app.lib_path + "\\" + "game_settings.ahk"
        result = []
        with open(settings, "r") as f:
            file = f.readlines()
        for change in self.changes:
            if type(change) is str:
                result.append(change)
            else:
                for line in file:
                    if change.cget("placeholder_text") in line:
                        spaces = " " * (15 - len(change.get()))
                        line = line[:line.find("=") + 2] + change.get() + spaces + line[line.rfind(";"):]
                        result.append(line)
                        break
        with open(settings, "w") as f:
            f.writelines(result)

        self.save_button.configure(state="disabled")

    def text_callback(self):
        self.save_button.configure(state="normal")

import os
import tkinter

import customtkinter
import webbrowser
from Elements.ctk_toplevel import CTkToplevel


class EditSettings(CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.main_app = app
        self.geometry("460x320")
        self.title("LazyHub")
        self.iconbitmap("cat.ico")
        self.withdraw()
        self.resizable(width=False, height=False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="AHK key names:")
        self.label_1.grid(row=0, column=0, padx=5, sticky="n", rowspan=2)

        self.label_2 = customtkinter.CTkLabel(self.main_frame, text="https://www.autohotkey.com/docs/v1/KeyList.htm",
                                              cursor="hand2")
        self.label_2.grid(row=0, column=1, padx=5, sticky="w")

        self.label_3 = customtkinter.CTkLabel(self.main_frame, text="https://www.autohotkey.com/docs/v1/Hotkeys.htm",
                                              cursor="hand2")
        self.label_3.grid(row=1, column=1, padx=5, sticky="w")

        self.label_2.bind("<Button-1>", lambda x: webbrowser.open(self.label_2.cget("text")))
        self.label_3.bind("<Button-1>", lambda x: webbrowser.open(self.label_3.cget("text")))

        self.items_list = customtkinter.CTkScrollableFrame(self.main_frame)
        self.items_list.grid(row=2, column=0, padx=5, pady=(10, 0), sticky="nsew", columnspan=2)
        self.changes = []

        self.save_button = customtkinter.CTkButton(self.main_frame, text="Save changes", state="disabled",
                                                   command=self.save)
        self.save_button.grid(row=3, column=0, padx=5, pady=(10, 0), sticky="w")

        self.lines = None
        settings = self.main_app.lib_path + "\\" + "game_settings.ahk"
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

                    dialog.grid(row=i, column=1, padx=100, pady=5, sticky="e")
                    self.changes.append(dialog)

    def save(self):
        settings = self.main_app.lib_path + "\\" + "game_settings.ahk"
        result = []
        with open(settings, "r") as f:
            file = f.readlines()
        for change in self.changes:
            if type(change) is str:
                result.append(change)
            else:
                for line in file:
                    if change.cget("placeholder_text") in line:
                        spaces = " " * (10-len(change.get()))
                        line = line[:line.find("=")+2] + change.get() + spaces + line[line.rfind(";"):]
                        result.append(line)
                        break
        with open(settings, "w") as f:
            f.writelines(result)

        self.save_button.configure(state="disabled")

    def text_callback(self):
        self.save_button.configure(state="normal")

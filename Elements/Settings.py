import os
import subprocess
import tkinter
import customtkinter
import win32api

from Elements.ConfirmationPopup import ConfirmationPopup

mouse_keys = {1: "LButton", 3: "RButton", 2: "MButton", 4: "XButton1", 5: "XButton2"}


class Settings:
    def __init__(self, app):
        self.binding = None
        self.app = app
        self.image = tkinter.PhotoImage(file="assets\\loading.gif", format=f"gif -index {0}")
        self.settings_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.settings_frame_1.grid_columnconfigure(0, weight=1)
        self.settings_frame_1.grid_rowconfigure(0, weight=1)

        self.settings_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.settings_frame_2.grid_columnconfigure(0, weight=1)

        self.items_list = customtkinter.CTkScrollableFrame(self.settings_frame_1)
        self.items_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew", columnspan=2)
        self.changes = []

        self.save_button = customtkinter.CTkButton(self.settings_frame_1, text="Save changes",
                                                   command=self.save)
        self.save_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), columnspan=2, sticky="nsew")

        self.upd_settings_button = customtkinter.CTkButton(self.settings_frame_2, text="Update game settings",
                                                           command=self.update_libs)
        self.upd_settings_button.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_settings_button_processing = customtkinter.CTkButton(self.settings_frame_2, state="disabled",
                                                                      text="Processing...",
                                                                      image=self.image)

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
                    label.grid(row=i, column=0, pady=5, sticky="nsew", columnspan=2)
                    self.changes.append(line)
                else:
                    label = customtkinter.CTkLabel(self.items_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    placeholder = tkinter.StringVar(value=line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    dialog = customtkinter.CTkEntry(self.items_list, textvariable=placeholder, state="disabled",
                                                    placeholder_text=label.cget("text"))
                    if dialog.cget("placeholder_text").replace(" ", "").replace("\n", "") == "Averageingamefps":
                        dialog.configure(state="normal")
                        placeholder.trace("w", lambda x, y, z: self.text_callback())
                    else:
                        dialog.bind("<Button-1>", lambda event, d=dialog: self.key_bind(event, d))
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

    def text_callback(self):
        self.save_button.configure(state="normal")

    def key_bind(self, event, element):
        if self.binding:
            return
        win32api.LoadKeyboardLayout('00000409', 1)
        element.cget("textvariable").set("<Press Key>")
        self.binding = True
        self.app.bind("<KeyPress>", lambda ev, el=element: self.keyboard_bind(ev, el))
        self.app.bind("<ButtonPress>", lambda ev, el=element: self.mouse_bind(ev, el))
        self.app.bind("<MouseWheel>", lambda ev, el=element: self.mouse_wheel_bind(ev, el))

    def mouse_bind(self, event, element):
        try:
            key = mouse_keys[event.num]
        except:
            self.app.unbind("<KeyPress>")
            self.app.unbind("<ButtonPress>")
            self.app.unbind("<MouseWheel>")
            self.binding = False
            return
        if element.cget("textvariable").get() == key:
            self.app.unbind("<KeyPress>")
            self.app.unbind("<ButtonPress>")
            self.app.unbind("<MouseWheel>")
            self.binding = False
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.app.unbind("<KeyPress>")
        self.app.unbind("<ButtonPress>")
        self.app.unbind("<MouseWheel>")
        self.binding = False

    def keyboard_bind(self, event, element):
        key = subprocess.check_output([self.app.ahk, self.app.lib_path + "\\key_decode.ahk", f'{event.keycode}']) \
            .decode("utf-8")
        if element.cget("textvariable").get() == key:
            self.app.unbind("<KeyPress>")
            self.app.unbind("<ButtonPress>")
            self.app.unbind("<MouseWheel>")
            self.binding = False
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.app.unbind("<KeyPress>")
        self.app.unbind("<ButtonPress>")
        self.app.unbind("<MouseWheel>")
        self.binding = False

    def mouse_wheel_bind(self, event, element):
        key = None
        if event.delta > 0:
            key = "WheelUp"
        if event.delta < 0:
            key = "WheelDown"
        if element.cget("textvariable").get() == key:
            self.app.unbind("<KeyPress>")
            self.app.unbind("<ButtonPress>")
            self.app.unbind("<MouseWheel>")
            self.binding = False
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.app.unbind("<KeyPress>")
        self.app.unbind("<ButtonPress>")
        self.app.unbind("<MouseWheel>")
        self.binding = False

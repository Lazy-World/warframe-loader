import getpass
import json
import threading
import tkinter
from itertools import cycle
import customtkinter
import os
import requests
from PIL import Image

from Elements.ActiveScripts import ActiveScripts
from Elements.Workshop import Workshop
from Elements.Settings import Settings
from Elements.AhkLoadingWindow import AhkLoadingWindow
from Elements.UpdatesPopup import UpdatePopup

customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


def get_online_version():
    answer = requests.get(
        "https://raw.githubusercontent.com/Lazy-World/warframe-ahk/LazyHub/LazyHub/latest.txt").content
    return answer.decode("utf-8")[:-1]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.workshop_path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.lib_path = self.workshop_path + "\\libraries"
        self.settings_path = self.workshop_path + "\\settings"
        self.ahk = None
        self.online_version = get_online_version()
        self.version = "3.0.7"
        self.json_settings = {}
        self.scrollable_frame_switches = None
        self.scrollable_frame = None
        self.geometry(f"{750}x{400}")
        self.minsize(width=750, height=400)
        self.title("LazyHub")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.img = customtkinter.CTkImage(Image.open("assets\\cat.png"), size=(30, 30))
        self.check_path()

        self.iconbitmap("assets\\cat.ico")
        # elements
        self.tab_groups = []
        self.tab_groups_names = ["active_scripts", "workshop", "game_settings"]
        self.tab_elements = []
        #################################
        # Navigation
        #################################
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="LazyHub v" + self.version, anchor="s",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=1, padx=(0, 10), pady=20)

        self.img_frame = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.img, compound="center")
        self.img_frame.grid(row=0, column=0, padx=0, pady=20)

        self.buttons = [
            {"text": "Your Scripts", "command": self.active_scripts_button_event},
            {"text": "Workshop", "command": self.workshop_button_event},
            {"text": "Game Settings", "command": self.settings_button_event}
        ]

        for i, button_data in enumerate(self.buttons):
            self.tab_groups.append(customtkinter.CTkButton(
                self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                text=button_data["text"], fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"), anchor="w", command=button_data["command"]
            ))
            self.tab_groups[i].grid(row=i + 1, column=0, sticky="ew", columnspan=2)

        # Settings
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=10, pady=(10, 10), columnspan=2)

        self.reload_button_icon_anim = []
        for i in range(0, 30):
            self.reload_button_icon_anim.append(tkinter.PhotoImage(file="assets\\loading.gif",
                                                                   format=f"gif -index {i}"))

        self.reload_button_icon_anim = cycle(self.reload_button_icon_anim)
        #################################
        # Your Scripts Frame
        #################################

        self.active_scripts_window = ActiveScripts(self)

        #################################
        # Workshop Frame
        #################################

        self.workshop_window = Workshop(self)

        #################################
        # Settings Frame
        #################################

        self.settings_window = Settings(self)

        self.loading_window = AhkLoadingWindow(self)
        self.loading_window.protocol("WM_DELETE_WINDOW", self.loading_terminated)

        self.update_popup = UpdatePopup(self)
        self.update_popup.protocol("WM_DELETE_WINDOW", self.close_update_popup)
        if self.online_version != self.version:
            self.loading_window.grab_release()
            self.update_popup.grab_set()
            self.update_popup.deiconify()
        else:
            self.close_update_popup()

        # set default values
        self.select_frame_by_name("active_scripts")
        self.protocol("WM_DELETE_WINDOW", self.save_settings)
        self.set_appearance()

    def loading_finished(self):
        self.loading_window.grab_release()
        self.loading_window.withdraw()
        self.set_appearance()

    def close_update_popup(self):
        self.update_popup.grab_release()
        self.loading_window.grab_set()
        threading._start_new_thread(self.loading_window.generate_ini, ())
        self.update_popup.destroy()

    def loading_terminated(self):
        self.loading_window.grab_release()
        self.loading_window.destroy()

    def save_settings(self):
        with open(self.workshop_path+"\\hub.ini", "w") as file:
            json.dump(self.json_settings, file)
        self.destroy()

    def select_frame_by_name(self, name):
        # set button color for selected button
        for i, tab in enumerate(self.tab_groups):
            tab.configure(fg_color=("gray75", "gray25") if name == self.tab_groups_names[i] else "transparent")

        # show selected frame
        if name == "active_scripts":
            self.active_scripts_window.active_scripts_frame_1.grid(row=0, column=1, sticky="nsew")
            self.active_scripts_window.active_scripts_frame_2.grid(row=0, column=2, sticky="nsew")
            self.active_scripts_window.cfg_back()
        else:
            self.active_scripts_window.active_scripts_frame_1.grid_forget()
            self.active_scripts_window.active_scripts_frame_2.grid_forget()
        if name == "workshop":
            self.workshop_window.workshop_frame_1.grid(row=0, column=1, sticky="nsew")
            self.workshop_window.workshop_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.workshop_window.workshop_frame_1.grid_forget()
            self.workshop_window.workshop_frame_2.grid_forget()
        if name == "game_settings":
            self.settings_window.settings_frame_1.grid(row=0, column=1, sticky="nsew")
            self.settings_window.settings_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.settings_window.settings_frame_1.grid_forget()
            self.settings_window.settings_frame_2.grid_forget()

    def active_scripts_button_event(self):
        self.select_frame_by_name("active_scripts")

    def workshop_button_event(self):
        self.select_frame_by_name("workshop")

    def settings_button_event(self):
        self.select_frame_by_name("game_settings")

    def check_path(self):
        if not os.path.exists(self.workshop_path):
            os.makedirs(self.workshop_path)
        if not os.path.exists(self.settings_path):
            os.makedirs(self.settings_path)
        if not os.path.exists(self.lib_path):
            os.makedirs(self.lib_path)

    def open_path(self, event):
        if self.ahk is not None:
            path = os.path.realpath(self.ahk[:self.ahk.rfind("\\") + 1])
            os.startfile(path)
        else:
            pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.json_settings["theme"] = new_appearance_mode

    def set_appearance(self):
        if not os.path.exists(self.workshop_path+"\\hub.ini"):
            return
        with open(self.workshop_path+"\\hub.ini", "r") as file:
            try:
                json_settings = json.load(file)
                if "theme" not in json_settings.keys():
                    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
                    self.appearance_mode_menu.set("System")
                else:
                    customtkinter.set_appearance_mode(json_settings["theme"])
                    self.appearance_mode_menu.set(json_settings["theme"])
            except json.JSONDecodeError:
                customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
                self.appearance_mode_menu.set("System")


if __name__ == "__main__":
    app = App()
    app.update()
    app.active_scripts_window.refresh()
    app.mainloop()

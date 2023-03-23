import getpass
import json
import customtkinter
import os
from Elements.ActiveScripts import ActiveScripts
from Elements.Workshop import Workshop
from Elements.Update import Update
from Elements.Settings import Settings
from Elements.AhkLoadingWindow import AhkLoadingWindow

customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.ahk = None
        self.json_settings = {}
        self.scrollable_frame_switches = None
        self.scrollable_frame = None
        self.geometry(f"{750}x{400}")
        self.title("LazyHub")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.iconbitmap("cat.ico")
        # elements
        self.tab_groups = []
        self.tab_groups_names = ["active_scripts", "workshop", "updates", "game_settings"]
        self.tab_elements = []
        #################################
        # Navigation
        #################################
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="LazyHub v3.0", compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.buttons = [
            {"text": "Your Scripts", "command": self.active_scripts_button_event},
            {"text": "Workshop", "command": self.workshop_button_event},
            {"text": "Updates", "command": self.updates_button_event},
            {"text": "Game Settings", "command": self.settings_button_event}
        ]

        for i, button_data in enumerate(self.buttons):
            self.tab_groups.append(customtkinter.CTkButton(
                self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                text=button_data["text"], fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"), anchor="w", command=button_data["command"]
            ))
            self.tab_groups[i].grid(row=i + 1, column=0, sticky="ew")

        # Settings
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        #################################
        # Your Scripts Frame
        #################################

        self.active_scripts_window = ActiveScripts(self)

        #################################
        # Workshop Frame
        #################################

        self.workshop_window = Workshop(self)

        #################################
        # Updates Frame
        #################################

        self.update_window = Update(self)

        #################################
        # Settings Frame
        #################################

        self.settings_window = Settings(self)

        self.loading_window = AhkLoadingWindow(self)
        self.loading_window.protocol("WM_DELETE_WINDOW", self.loading_terminated)
        self.loading_window.grab_set()
        # set default values
        self.select_frame_by_name("active_scripts")
        self.protocol("WM_DELETE_WINDOW", self.save_settings)

    def loading_finished(self):
        self.loading_window.withdraw()
        self.loading_window.grab_release()
        self.deiconify()

    def loading_terminated(self):
        self.loading_window.grab_release()
        if not os.path.exists(self.path + "\\hub.ini"):
            with open(self.path + "\\hub.ini", "w") as file:
                self.json_settings = {"Version": "3.0", "theme": customtkinter.get_appearance_mode()}
                json.dump(self.json_settings, file)
        self.loading_window.destroy()

    def save_settings(self):
        with open(self.path + "\\hub.ini", "w") as file:
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
            self.active_scripts_window.refresh()
        else:
            self.active_scripts_window.active_scripts_frame_1.grid_forget()
            self.active_scripts_window.active_scripts_frame_2.grid_forget()
        if name == "workshop":
            self.workshop_window.workshop_frame_1.grid(row=0, column=1, sticky="nsew")
            self.workshop_window.workshop_frame_2.grid(row=0, column=2, sticky="nsew")
            self.workshop_window.refresh()
        else:
            self.workshop_window.workshop_frame_1.grid_forget()
            self.workshop_window.workshop_frame_2.grid_forget()
        if name == "updates":
            self.update_window.updates_frame_1.grid(row=0, column=1, sticky="nsew")
            self.update_window.updates_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.update_window.updates_frame_1.grid_forget()
            self.update_window.updates_frame_2.grid_forget()
        if name == "settings":
            self.settings_window.settings_frame_1.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_window.settings_frame_1.grid_forget()

    def active_scripts_button_event(self):
        self.select_frame_by_name("active_scripts")

    def workshop_button_event(self):
        self.select_frame_by_name("workshop")

    def updates_button_event(self):
        self.select_frame_by_name("updates")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def check_path(self):
        if not os.path.exists(self.path + "\\lib"):
            os.mkdir(self.path + "\\lib")
        if not os.path.exists(self.path + "\\workshop"):
            os.mkdir(self.path + "\\workshop")

    def open_path(self, event):
        if self.ahk is not None:
            path = os.path.realpath(self.ahk[:self.ahk.rfind("\\") + 1])
            os.startfile(path)
        else:
            pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.json_settings["theme"] = new_appearance_mode


if __name__ == "__main__":
    app = App()
    app.update()
    if "theme" not in app.json_settings.keys():
        app.json_settings["theme"] = "System"
        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        app.appearance_mode_menu.set("System")
    else:
        customtkinter.set_appearance_mode(app.json_settings["theme"])  # Modes: "System" (standard), "Dark", "Light"
        app.appearance_mode_menu.set(app.json_settings["theme"])
    app.check_path()
    app.mainloop()

import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.scrollable_frame_switches = None
        self.scrollable_frame = None
        self.geometry(f"{750}x{400}")
        self.title("LazyHub")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # elements
        self.tab_groups = []
        self.tab_groups_names = ["active_scripts", "workshop", "updates"]
        self.tab_elements = []

        #################################
        # Navigation
        #################################
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="LazyHub v3.0", compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.buttons = [
            {"text": "Your Scripts", "command": self.active_scripts_button_event},
            {"text": "Workshop", "command": self.workshop_button_event},
            {"text": "Updates", "command": self.updates_button_event}
        ]

        for i, button_data in enumerate(self.buttons):
            self.tab_groups.append(customtkinter.CTkButton(
                self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                text=button_data["text"], fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"), anchor="w", command=button_data["command"]
            ))
            self.tab_groups[i].grid(row=i+1, column=0, sticky="ew")

        # Settings
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"], command=change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        #################################
        # Your Scripts Frame
        #################################
        self.active_scripts_frame_1 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_1.grid_columnconfigure(0, weight=1)

        self.active_scripts_frame_2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_2.grid_columnconfigure(0, weight=1)

        # elements
        self.as_script_list = customtkinter.CTkScrollableFrame(self.active_scripts_frame_1, label_text="Your Scripts")
        self.as_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.scrollable_frame_switches = []
        for i in range(10):
            switch = customtkinter.CTkCheckBox(master=self.as_script_list, text=f"7:0{i} avg")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            self.scrollable_frame_switches.append(switch)

        self.as_load_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Load Selected Items")
        self.as_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.as_explorer_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Open Folder")
        self.as_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_refresh_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Refresh List")
        self.as_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_unload_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Unload All")
        self.as_unload_button.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        #################################
        # Workshop Frame
        #################################
        self.workshop_frame_1 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.workshop_frame_1.grid_columnconfigure(0, weight=1)

        self.workshop_frame_2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.workshop_frame_2.grid_columnconfigure(0, weight=1)

        # elements
        self.ws_script_list = customtkinter.CTkScrollableFrame(self.workshop_frame_1, label_text="Workshop Scripts")
        self.ws_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.scrollable_frame_switches_2 = []
        for i in range(10):
            switch = customtkinter.CTkCheckBox(master=self.ws_script_list, text=f"7:0{i} avg")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            self.scrollable_frame_switches_2.append(switch)

        self.ws_load_button = customtkinter.CTkButton(self.workshop_frame_1, text="Download Selected Items")
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.ws_explorer_button = customtkinter.CTkButton(self.workshop_frame_2, text="Open Folder")
        self.ws_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.ws_refresh_button = customtkinter.CTkButton(self.workshop_frame_2, text="Refresh List")
        self.ws_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        #################################
        # Updates Frame
        #################################
        self.updates_frame_1 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.updates_frame_1.grid_columnconfigure(0, weight=1)

        self.updates_frame_2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.updates_frame_2.grid_columnconfigure(0, weight=1)

        self.upd_libraries_group = customtkinter.CTkLabel(self.updates_frame_1, corner_radius=0, text="Libraries:")
        self.upd_libraries_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_group = customtkinter.CTkLabel(self.updates_frame_2, corner_radius=0, text="Application:")
        self.upd_application_group.grid(row=0, column=1, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_libraries_button = customtkinter.CTkButton(self.upd_libraries_group, text="Update Libraries")
        self.upd_libraries_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_folder_button = customtkinter.CTkButton(self.upd_libraries_group, text="Open Folder")
        self.upd_folder_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_button = customtkinter.CTkButton(self.upd_application_group, text="Update Application")
        self.upd_application_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        # set default values
        self.select_frame_by_name("active_scripts")
        self.appearance_mode_menu.set("System")

    def select_frame_by_name(self, name):
        # set button color for selected button
        for i, tab in enumerate(self.tab_groups):
            tab.configure(fg_color=("gray75", "gray25") if name == self.tab_groups_names[i] else "transparent")

        # show selected frame
        if name == "active_scripts":
            self.active_scripts_frame_1.grid(row=0, column=1, sticky="nsew")
            self.active_scripts_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.active_scripts_frame_1.grid_forget()
            self.active_scripts_frame_2.grid_forget()
        if name == "workshop":
            self.workshop_frame_1.grid(row=0, column=1, sticky="nsew")
            self.workshop_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.workshop_frame_1.grid_forget()
            self.workshop_frame_2.grid_forget()
        if name == "updates":
            self.updates_frame_1.grid(row=0, column=1, sticky="nsew")
            self.updates_frame_2.grid(row=0, column=2, sticky="nsew")
        else:
            self.updates_frame_1.grid_forget()
            self.updates_frame_2.grid_forget()

    def active_scripts_button_event(self):
        self.select_frame_by_name("active_scripts")

    def workshop_button_event(self):
        self.select_frame_by_name("workshop")

    def updates_button_event(self):
        self.select_frame_by_name("updates")


if __name__ == "__main__":
    app = App()
    app.mainloop()

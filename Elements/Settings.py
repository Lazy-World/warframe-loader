import os
import customtkinter

from Elements.ConfirmationPopup import ConfirmationPopup
from Elements.EditSettings import EditSettings


class Settings:
    def __init__(self, app):
        self.app = app
        self.settings_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.settings_frame_1.grid_columnconfigure(0, weight=1)

        self.game_settings_group = customtkinter.CTkLabel(self.settings_frame_1, corner_radius=0, text="Game settings:")
        self.game_settings_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_settings_button = customtkinter.CTkButton(self.settings_frame_1, text="Update game settings",
                                                           command=self.update_libs)
        self.upd_settings_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.edit_settings_button = customtkinter.CTkButton(self.settings_frame_1, text="Edit game settings",
                                                            command=self.edit_settings)
        self.edit_settings_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.open_folder_button = customtkinter.CTkButton(self.settings_frame_1, text="Open Folder",
                                                          command=self.open_folder)
        self.open_folder_button.grid(row=3, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.loading_window = ConfirmationPopup(self.app)
        self.loading_window.withdraw()

        self.edit_sessings_window = EditSettings(self.app)
        self.edit_sessings_window.protocol("WM_DELETE_WINDOW", self.close_settings_popup)

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.lib_path))

    def update_libs(self):
        self.loading_window.geometry(f"+{self.app.winfo_rootx()+300}+{self.app.winfo_rooty()}")
        self.loading_window.grab_set()
        self.loading_window.deiconify()

    def edit_settings(self):
        self.edit_sessings_window.geometry(f"+{self.app.winfo_rootx() + 300}+{self.app.winfo_rooty()}")
        self.edit_sessings_window.deiconify()
        self.edit_sessings_window.grab_set()
        # if os.path.exists(self.app.path + "\\lib\\game_settings.ahk"):
        # subprocess.Popen(["Notepad.exe", self.app.path+"\\lib\\game_settings.ahk"])

    def close_settings_popup(self):
        self.edit_sessings_window.grab_release()
        self.edit_sessings_window.withdraw()
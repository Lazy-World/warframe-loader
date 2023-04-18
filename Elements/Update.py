import json
import os
import threading
import tkinter

import customtkinter
import requests as requests

from Elements.NoUpdatesRequired import NoUpdatesRequired
from Elements.DownloadUpdate import DownloadWindow


class Update:
    def __init__(self, app):
        self.condition = None
        self.app = app

        self.updates_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.updates_frame_1.grid_columnconfigure(0, weight=1)

        self.updates_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.updates_frame_2.grid_columnconfigure(0, weight=1)

        self.upd_libraries_group = customtkinter.CTkLabel(self.updates_frame_1, corner_radius=0, text="Libraries:")
        self.upd_libraries_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_group = customtkinter.CTkLabel(self.updates_frame_2, corner_radius=0, text="Application:")
        self.upd_application_group.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_libraries_button = customtkinter.CTkButton(self.updates_frame_1, text="Update Libraries",
                                                            command=self.update_libs_event)
        self.upd_libraries_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_libraries_button_processing = customtkinter.CTkButton(self.updates_frame_1, state="disabled",
                                                                       text="Processing...",
                                                                       image=tkinter.PhotoImage(
                                                                           file="assets\\loading.gif",
                                                                           format=f"gif -index {0}"))

        self.upd_folder_button = customtkinter.CTkButton(self.updates_frame_1, text="Open Folder",
                                                         command=self.open_folder)
        self.upd_folder_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.upd_application_button = customtkinter.CTkButton(self.updates_frame_2, text="Update Application",
                                                              command=self.update_application)
        self.upd_application_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.no_upd_r_window = NoUpdatesRequired()
        self.no_upd_r_window.protocol("WM_DELETE_WINDOW", self.close_no_upd)

        self.upd_download_window = None

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.path + "\\lib"))

    def update_libs_event(self):
        threading._start_new_thread(self.update_libs, ())

    def update_libs(self):
        self.condition = False
        self.upd_libraries_button.configure(state="disabled")
        self.upd_libraries_button.grid_forget()
        self.upd_libraries_button_processing.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.app.after(50, self.processing_animation, self.condition)

        self.app.check_path()
        answer = requests.get("https://api.github.com/repos/Lazy-World/warframe-ahk/contents/libraries").content
        json_answer = json.loads(answer.decode("utf-8"))
        for item in json_answer:
            if item["name"] != "game_settings.ahk" and item["name"] != "key_decode.ahk":
                filename = self.app.path + "\\lib\\" + item["name"]
                r = requests.get(item["download_url"])
                with open(filename, 'wb') as f:
                    f.write(r.content)

        self.condition = True
        self.upd_libraries_button.configure(state="normal")
        self.upd_libraries_button_processing.grid_forget()
        self.upd_libraries_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

    def processing_animation(self, condition):
        if not self.condition:
            self.upd_libraries_button_processing.configure(
                image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation, self.condition)
        else:
            return

    def update_application(self):
        if self.app.version == self.app.online_version:
            self.no_upd_r_window.geometry(f"+{self.app.winfo_rootx() + 500}+{self.app.winfo_rooty()}")
            self.no_upd_r_window.grab_set()
            self.no_upd_r_window.deiconify()
        else:
            self.upd_download_window = DownloadWindow(self.app)
            self.upd_download_window.protocol("WM_DELETE_WINDOW", self.close_upd)
            threading._start_new_thread(self.upd_download_window.download, ())

    def close_no_upd(self):
        self.no_upd_r_window.grab_release()
        self.no_upd_r_window.withdraw()

    def close_upd(self):
        self.upd_download_window.grab_release()
        self.upd_download_window.destroy()

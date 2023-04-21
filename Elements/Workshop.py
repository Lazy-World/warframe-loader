import json
import os
import threading
import tkinter
import customtkinter
import requests as requests

from Elements.DownloadUpdate import DownloadWindow
from Elements.NoUpdatesRequired import NoUpdatesRequired


class Workshop:
    def __init__(self, app):
        self.condition = None
        self.app = app

        self.scripts = {}

        self.workshop_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.workshop_frame_1.grid_columnconfigure(0, weight=1)
        self.workshop_frame_1.grid_rowconfigure(0, weight=1)

        self.workshop_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.workshop_frame_2.grid_columnconfigure(0, weight=1)

        self.ws_script_list = customtkinter.CTkScrollableFrame(self.workshop_frame_1, label_text="Workshop Scripts")
        self.ws_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.scrollable_frame_switches_2 = []
        self.image = tkinter.PhotoImage(file="assets\\loading.gif", format=f"gif -index {0}")
        self.ws_load_button = customtkinter.CTkButton(self.workshop_frame_1, text="Download Selected Items",
                                                      command=self.download_workshop_event)
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.ws_load_button_processing = customtkinter.CTkButton(self.workshop_frame_1, state="disabled",
                                                                 text="Processing...",
                                                                 image=self.image)

        self.ws_refresh_button = customtkinter.CTkButton(self.workshop_frame_2, text="Refresh List",
                                                         command=self.refresh_event)
        self.ws_refresh_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.ws_refresh_button_processing = customtkinter.CTkButton(self.workshop_frame_2, state="disabled",
                                                                    text="Processing...",
                                                                    image=self.image)
        self.upd_libraries_button = customtkinter.CTkButton(self.workshop_frame_2, text="Update Libraries",
                                                            command=self.update_libs_event)
        self.upd_libraries_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.upd_libraries_button_processing = customtkinter.CTkButton(self.workshop_frame_2, state="disabled",
                                                                       text="Processing...",
                                                                       image=self.image)
        self.upd_application_button = customtkinter.CTkButton(self.workshop_frame_2, text="Update Application",
                                                              command=self.update_application)
        self.upd_application_button.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.no_upd_r_window = NoUpdatesRequired()
        self.no_upd_r_window.protocol("WM_DELETE_WINDOW", self.close_no_upd)

        self.upd_download_window = None

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.workshop_path))

    def get_names(self):
        answer = requests.get("https://api.github.com/repos/Lazy-World/warframe-ahk/contents/").content
        json_answer = json.loads(answer.decode("utf-8"))
        for item in json_answer:
            if item["name"][-3:] == "ahk":
                self.scripts[item["name"]] = item["download_url"]

    def download_workshop_event(self):
        threading._start_new_thread(self.download_workshop, ())

    def download_workshop(self):
        self.condition = False
        self.ws_refresh_button.configure(state="disabled")
        self.upd_libraries_button.configure(state="disabled")
        self.ws_load_button.grid_forget()
        self.ws_load_button_processing.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.app.after(50, self.processing_animation_load, self.condition)

        self.app.check_path()
        for switch in self.scrollable_frame_switches_2:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                r = requests.get(self.scripts[switch.cget("text")])
                with open(filename, 'wb') as f:
                    f.write(r.content)
                switch.configure(border_color="#31dea4", fg_color="#31dea4")

        self.download_cfg()
        self.condition = True
        self.ws_refresh_button.configure(state="normal")
        self.upd_libraries_button.configure(state="normal")
        self.ws_load_button_processing.grid_forget()
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

    def download_cfg(self):
        def cfg_equal(script):
            if not os.path.exists(cfg):
                return False
            with open(self.app.settings_path + f"\\cfg_{script}") as file:
                current_cfg = file.readlines()
            for i in range(len(current_cfg)):
                current_cfg[i] = current_cfg[i].replace(" ", "").rstrip()
                if "=" in current_cfg[i]:
                    current_cfg[i] = current_cfg[i][:current_cfg[i].find("=")] + current_cfg[i][
                        current_cfg[i].rfind(";")]

            online_cfg = requests.get(f"https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/settings/"
                                      f"{'cfg_' + script}").content.decode("utf-8").splitlines()

            for i in range(len(online_cfg)):
                online_cfg[i] = online_cfg[i].replace(" ", "").rstrip()
                if "=" in online_cfg[i]:
                    online_cfg[i] = online_cfg[i][:online_cfg[i].find("=")] + online_cfg[i][online_cfg[i].rfind(";")]

            if online_cfg == current_cfg:
                return True
            else:
                return False

        for switch in self.scrollable_frame_switches_2:
            if switch.get() == 1:
                cfg = self.app.settings_path + "\\cfg_" + switch.cget("text")
                if not os.path.exists(cfg) or not cfg_equal(switch.cget('text')):
                    rq = requests.get(f"https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/settings/"
                                      f"{'cfg_' + switch.cget('text')}")
                    with open(cfg, 'wb') as f:
                        f.write(rq.content)

    def refresh_event(self):
        threading._start_new_thread(self.refresh, ())

    def processing_animation_refresh(self, condition):
        if not self.condition:
            self.ws_refresh_button_processing.configure(image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation_refresh, self.condition)
        else:
            return

    def processing_animation_load(self, condition):
        if not self.condition:
            self.ws_load_button_processing.configure(image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation_load, self.condition)
        else:
            return

    def refresh(self):
        self.condition = False
        self.ws_load_button.configure(state="disabled")
        self.upd_libraries_button.configure(state="disabled")
        self.ws_refresh_button.grid_forget()
        self.ws_refresh_button_processing.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.app.after(50, self.processing_animation_refresh, self.condition)

        if self.scrollable_frame_switches_2:
            for switch in self.scrollable_frame_switches_2:
                switch.grid_forget()
            self.scrollable_frame_switches_2.clear()
        self.get_names()
        active_scripts = self.app.active_scripts_window.get_names()
        for i, name in enumerate(self.scripts.keys()):
            script = requests.get(f"https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/{name}").content \
                .decode("utf-8")
            if name in active_scripts:
                color = "#f2ba38"
                active = tkinter.IntVar(value=1)
            else:
                color = "#000000"
                active = tkinter.IntVar(value=0)
            for ahk in active_scripts:
                with open(self.app.workshop_path + "\\" + ahk, "r") as file:
                    local_script = file.read()
                if local_script == script:
                    color = "#31dea4"
                    active = tkinter.IntVar(value=1)
                    break
            switch_color = "#31dea4"
            if color == "#f2ba38":
                switch_color = "#f2ba38"
            switch = customtkinter.CTkCheckBox(master=self.ws_script_list, text=name, border_color=color,
                                               variable=active, fg_color=switch_color)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            self.scrollable_frame_switches_2.append(switch)

        self.condition = True
        self.ws_load_button.configure(state="normal")
        self.upd_libraries_button.configure(state="normal")
        self.ws_refresh_button_processing.grid_forget()
        self.ws_refresh_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

    def update_libs_event(self):
        threading._start_new_thread(self.update_libs, ())

    def update_libs(self):
        self.condition = False
        self.ws_load_button.configure(state="disabled")
        self.ws_refresh_button.configure(state="disabled")
        self.upd_libraries_button.grid_forget()
        self.upd_libraries_button_processing.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.app.after(50, self.processing_animation_libs, self.condition)

        self.app.check_path()
        answer = requests.get("https://api.github.com/repos/Lazy-World/warframe-ahk/contents/libraries").content
        json_answer = json.loads(answer.decode("utf-8"))
        for item in json_answer:
            if item["name"] != "game_settings.ahk" and item["name"] != "key_decode.ahk":
                filename = self.app.lib_path + "\\" + item["name"]
                r = requests.get(item["download_url"])
                with open(filename, 'wb') as f:
                    f.write(r.content)

        self.condition = True
        self.ws_refresh_button.configure(state="normal")
        self.ws_load_button.configure(state="normal")
        self.upd_libraries_button_processing.grid_forget()
        self.upd_libraries_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

    def processing_animation_libs(self, condition):
        if not self.condition:
            self.upd_libraries_button_processing.configure(
                image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation_libs, self.condition)
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

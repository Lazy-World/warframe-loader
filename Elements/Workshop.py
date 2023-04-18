import json
import os
import threading
import tkinter
import customtkinter
import requests as requests


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

        self.ws_load_button = customtkinter.CTkButton(self.workshop_frame_1, text="Download Selected Items",
                                                      command=self.download_workshop_event)
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.ws_load_button_processing = customtkinter.CTkButton(self.workshop_frame_1, state="disabled",
                                                                 text="Processing...",
                                                                 image=tkinter.PhotoImage(
                                                                     file="assets\\loading.gif",
                                                                     format=f"gif -index {0}"))

        self.ws_load_cfg_button = customtkinter.CTkButton(self.workshop_frame_1, text="Download Selected Items Сonfigs",
                                                          command=self.download_cfg_event)
        self.ws_load_cfg_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.ws_load_cfg_button_processing = customtkinter.CTkButton(self.workshop_frame_1, state="disabled",
                                                                     text="Processing...",
                                                                     image=tkinter.PhotoImage(
                                                                         file="assets\\loading.gif",
                                                                         format=f"gif -index {0}"))

        self.ws_explorer_button = customtkinter.CTkButton(self.workshop_frame_2, text="Open Folder",
                                                          command=self.open_folder)
        self.ws_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.ws_refresh_button = customtkinter.CTkButton(self.workshop_frame_2, text="Refresh List",
                                                         command=self.refresh_event)
        self.ws_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.ws_refresh_button_processing = customtkinter.CTkButton(self.workshop_frame_2, state="disabled",
                                                                    text="Processing...",
                                                                    image=tkinter.PhotoImage(
                                                                        file="assets\\loading.gif",
                                                                        format=f"gif -index {0}"))
        # self.refresh()

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
        self.ws_load_cfg_button.configure(state="disabled")
        self.ws_load_button.grid_forget()
        self.ws_load_button_processing.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.app.after(50, self.processing_animation_load, self.condition)

        self.app.check_path()
        for switch in self.scrollable_frame_switches_2:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                r = requests.get(self.scripts[switch.cget("text")])
                with open(filename, 'wb') as f:
                    f.write(r.content)

        self.condition = True
        self.ws_refresh_button.configure(state="normal")
        self.ws_load_cfg_button.configure(state="normal")
        self.ws_load_button_processing.grid_forget()
        self.ws_load_button.grid(row=1, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

    def download_cfg_event(self):
        threading._start_new_thread(self.download_cfg, ())

    def download_cfg(self):
        self.condition = False
        self.ws_refresh_button.configure(state="disabled")
        self.ws_load_button.configure(state="disabled")
        self.ws_load_cfg_button.grid_forget()
        self.ws_load_cfg_button_processing.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.app.after(50, self.processing_animation_load_cfg, self.condition)

        self.app.check_path()
        for switch in self.scrollable_frame_switches_2:
            if switch.get() == 1:
                cfg = self.app.workshop_path + "\\settings\\cfg_" + switch.cget("text")
                rq = requests.get(f"https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/settings/"
                                  f"{'cfg_'+switch.cget('text')}")
                with open(cfg, 'wb') as f:
                    f.write(rq.content)

        self.condition = True
        self.ws_refresh_button.configure(state="normal")
        self.ws_load_button.configure(state="normal")
        self.ws_load_cfg_button_processing.grid_forget()
        self.ws_load_cfg_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

    def refresh_event(self):
        threading._start_new_thread(self.refresh, ())

    def processing_animation_refresh(self, condition):
        if not self.condition:
            self.ws_refresh_button_processing.configure(image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation_refresh, self.condition)
        else:
            return

    def processing_animation_load_cfg(self, condition):
        if not self.condition:
            self.ws_load_cfg_button_processing.configure(image=next(self.app.reload_button_icon_anim))
            self.app.after(50, self.processing_animation_load_cfg, self.condition)
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
        self.ws_load_cfg_button.configure(state="disabled")
        self.ws_refresh_button.grid_forget()
        self.ws_refresh_button_processing.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")
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
        self.ws_load_cfg_button.configure(state="normal")
        self.ws_refresh_button_processing.grid_forget()
        self.ws_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

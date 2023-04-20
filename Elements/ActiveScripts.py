import json
import subprocess
import tkinter
from os import listdir
import ast
import win32api
from PIL import Image
from os.path import isfile, join
from tkinter.filedialog import askopenfilename
import customtkinter
import os

mouse_keys = {1: "LButton", 3: "RButton", 2: "MButton", 4: "XButton1", 5: "XButton2"}


class ActiveScripts:
    def __init__(self, app):
        self.value_chosen = None
        self.binding = False
        self.lines = []
        self.changes = []
        self.app = app
        self.current_cfg = None
        self.scripts = []

        self.active_scripts = []

        self.active_scripts_frame_1 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_1.grid_columnconfigure(0, weight=1)
        self.active_scripts_frame_1.grid_rowconfigure(0, weight=1)

        self.active_scripts_frame_2 = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.active_scripts_frame_2.grid_columnconfigure(0, weight=1)

        self.as_script_list = customtkinter.CTkScrollableFrame(self.active_scripts_frame_1, label_text="Your Scripts")
        self.as_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.scrollable_frame_switches = []
        self.scrollable_frame_labels = []

        self.path_label = customtkinter.CTkLabel(self.active_scripts_frame_1, text="AutoHotkey.exe path: ")

        self.path_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.as_load_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Load Selected Items",
                                                      command=self.load_script)
        self.as_load_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.cfg_save_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Save",
                                                       command=self.save_cfg)
        self.back_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Back",
                                                   command=self.cfg_back)
        self.as_delete_button = customtkinter.CTkButton(self.active_scripts_frame_1, text="Delete Selected Items",
                                                        command=self.delete_script)
        self.as_delete_button.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.as_explorer_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Open Folder",
                                                          command=self.open_folder)
        self.as_explorer_button.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_refresh_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Refresh List",
                                                         command=self.refresh)
        self.as_refresh_button.grid(row=1, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_unload_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Unload All",
                                                        command=self.unload_all)
        self.as_unload_button.grid(row=2, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.as_editpath_button = customtkinter.CTkButton(self.active_scripts_frame_2, text="Edit Ahk Path",
                                                          command=self.edit_path)
        self.as_editpath_button.grid(row=3, column=1, padx=(10, 20), pady=(10, 0), sticky="nsew")

        self.configure = customtkinter.CTkImage(Image.open("assets\\configure.png"), size=(30, 30))
        self.configure_2 = customtkinter.CTkImage(Image.open("assets\\configure_2.png"), size=(30, 30))

    def open_folder(self):
        self.app.check_path()
        os.startfile(os.path.realpath(self.app.workshop_path))

    def save_cfg(self):
        cfg = self.app.settings_path+"\\" + self.current_cfg
        result = []
        with open(cfg, "r") as f:
            file = f.readlines()
        for change in self.changes:
            if type(change) is str:
                result.append(change)
            elif type(change) is customtkinter.CTkEntry:
                for line in file:
                    if change.cget("placeholder_text") in line:
                        line = line[:line.find("=") + 2] + change.get() + " " + line[line.rfind(";"):]
                        result.append(line)
                        break
            elif type(change) is list:
                for line in file:
                    if change[0] in line:
                        if type(change[1]) is list:
                            if type(change[1][0]) is customtkinter.StringVar:
                                line = line[:line.find("=") + 2] \
                                       + str([int(change[1][0].get()), int(change[1][1].get())]) \
                                       + " " + line[line.rfind(";"):]
                                result.append(line)
                                break
                            else:
                                line = line[:line.find("=") + 2] + json.dumps(change[1]) + " " + line[line.rfind(";"):]
                                result.append(line)
                                break
                        elif type(change[1]) is customtkinter.StringVar:
                            line = line[:line.find("=") + 2] + change[1].get() + " " + line[line.rfind(";"):]
                            result.append(line)
                            break
        with open(cfg, "w") as f:
            f.writelines(result)
        self.cfg_back()

    def cfg_back(self):
        self.as_script_list.destroy()
        self.as_script_list = customtkinter.CTkScrollableFrame(self.active_scripts_frame_1, label_text="Your Scripts")
        self.as_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.as_delete_button.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.as_load_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.cfg_save_button.grid_forget()
        self.back_button.grid_forget()
        self.current_cfg = None
        self.as_script_list.configure(label_text="Your Scripts")
        self.refresh()

    def get_names(self):
        return [f for f in listdir(self.app.workshop_path) if
                isfile(join(self.app.workshop_path, f)) and f != "hub.ini"]

    def refresh(self):
        if self.scrollable_frame_switches:
            for child in self.as_script_list.winfo_children():
                child.grid_forget()
            self.scrollable_frame_switches.clear()
        self.scripts = self.get_names()
        for i, name in enumerate(self.scripts):
            switch = customtkinter.CTkCheckBox(master=self.as_script_list, text=name)
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")
            switch_label = customtkinter. \
                CTkLabel(master=self.as_script_list, text="", image=self.configure)
            switch_label.grid(row=i, column=1, padx=10, pady=(0, 20), sticky="nsew")
            switch_label.bind("<Button-1>", lambda event, script="cfg_" + name: self.configure_script(script))
            switch_label.bind("<Enter>", lambda event, sw=switch_label: sw.configure(image=self.configure_2))
            switch_label.bind("<Leave>", lambda event, sw=switch_label: sw.configure(image=self.configure))
            self.scrollable_frame_switches.append(switch)
            self.scrollable_frame_labels.append(switch_label)

    def configure_script(self, script):
        self.current_cfg = script
        self.as_script_list.destroy()
        self.as_script_list = customtkinter.CTkScrollableFrame(self.active_scripts_frame_1, label_text=script[4:])
        self.as_script_list.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.as_delete_button.grid_forget()
        self.as_load_button.grid_forget()
        self.cfg_save_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.back_button.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")

        self.lines = []
        self.changes = []
        action = None
        cfg = self.app.settings_path + "\\" + script
        if os.path.isfile(cfg):
            with open(cfg, "r") as file:
                self.lines = file.readlines()
        if self.lines:
            for i, line in enumerate(self.lines):
                if line == "\n":
                    self.changes.append(line)
                    continue
                if "@Bind" in line:
                    self.changes.append(line)
                    action = "Bind"
                    continue
                elif "@Array" in line:
                    self.changes.append(line)
                    action = "Array"
                    continue
                elif "@Boolean" in line:
                    self.changes.append(line)
                    action = "Boolean"
                    continue
                elif "@Value" in line:
                    self.changes.append(line)
                    action = "Value"
                    continue
                elif "@MouseMove" in line:
                    self.changes.append(line)
                    action = "MouseMove"
                    continue
                elif "@Tab" in line:
                    self.changes.append(line)
                    action = "Tab"
                    continue
                elif "@Title" in line:
                    self.changes.append(line)
                    label = customtkinter.CTkLabel(self.as_script_list, text=line[8:],
                                                   font=customtkinter.CTkFont(weight="bold"))
                    label.grid(row=i, column=0, pady=5, sticky="nsew", columnspan=3)
                    continue
                if action == "Bind":
                    label = customtkinter.CTkLabel(self.as_script_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    placeholder = tkinter.StringVar(value=line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    dialog = customtkinter.CTkEntry(self.as_script_list, textvariable=placeholder, state="disabled",
                                                    placeholder_text=label.cget("text"))
                    dialog.bind("<Button-1>", lambda event, d=dialog: self.key_bind(event, d))
                    dialog.grid(row=i, column=1, padx=10, pady=5, sticky="w", columnspan=2)
                    self.changes.append(dialog)
                if action == "Array":
                    values = ast.literal_eval(line[line.find("["):line.rfind("]") + 1])
                    self.value_chosen = None

                    def text_callback(event):
                        if combobox_var.get() in values or (combobox_var.get() == "" and not self.value_chosen):
                            combobox_var.set("")
                            return
                        elif self.value_chosen:
                            for it in range(len(values)):
                                if values[it] == self.value_chosen:
                                    if combobox_var.get() == "":
                                        values.remove(values[it])
                                    else:
                                        values[it] = combobox_var.get()
                                    self.value_chosen = None
                        else:
                            values.append(combobox_var.get())
                        combobox_var.set("")
                        combobox.configure(values=values)

                    def combobox_callback(choice):
                        self.value_chosen = choice

                    label = customtkinter.CTkLabel(self.as_script_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    combobox_var = customtkinter.StringVar(value="")
                    combobox = customtkinter.CTkComboBox(self.as_script_list,
                                                         command=combobox_callback,
                                                         values=values,
                                                         variable=combobox_var)
                    combobox.bind("<Return>", lambda ev: text_callback(ev))
                    combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w", columnspan=2)
                    self.changes.append([label.cget("text"), values])
                if action == "Boolean":
                    label = customtkinter.CTkLabel(self.as_script_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    var = customtkinter.StringVar(value=line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    switch = customtkinter.CTkSwitch(self.as_script_list, text="", variable=var,
                                                     onvalue="True", offvalue="False")
                    switch.grid(row=i, column=1, padx=30, pady=5, sticky="w", columnspan=2)
                    self.changes.append([label.cget("text"), var])
                if action == "Value":
                    label = customtkinter.CTkLabel(self.as_script_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    placeholder = tkinter.StringVar(value=line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    dialog = customtkinter.CTkEntry(self.as_script_list, textvariable=placeholder,
                                                    placeholder_text=label.cget("text"))
                    dialog.grid(row=i, column=1, padx=10, pady=5, sticky="w", columnspan=2)
                    self.changes.append(dialog)
                if action == "MouseMove":
                    label = customtkinter.CTkLabel(self.as_script_list, text=line[line.rfind(";") + 1:])
                    label.grid(row=i, column=0, pady=5, sticky="w")
                    array = ast.literal_eval(line[line.find("=") + 1:line.rfind(";")].replace(" ", ""))
                    placeholder1 = tkinter.StringVar(value=array[0])
                    placeholder2 = tkinter.StringVar(value=array[1])
                    dialog1 = customtkinter.CTkEntry(self.as_script_list, textvariable=placeholder1, width=60,
                                                     placeholder_text=label.cget("text"))
                    dialog1.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    dialog2 = customtkinter.CTkEntry(self.as_script_list, textvariable=placeholder2, width=60,
                                                     placeholder_text=label.cget("text"))
                    dialog2.grid(row=i, column=2, padx=10, pady=5, sticky="e")
                    self.changes.append([label.cget("text"), [placeholder1, placeholder2]])

    def load_script(self):
        for switch in self.scrollable_frame_switches:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                subprocess.Popen([self.app.ahk, filename])

    def delete_script(self):
        for switch in self.scrollable_frame_switches:
            if switch.get() == 1:
                filename = self.app.workshop_path + "\\" + switch.cget("text")
                os.remove(filename)
        self.refresh()

    def key_bind(self, event, element):
        if self.binding:
            return
        win32api.LoadKeyboardLayout('00000409', 1)
        element.cget("textvariable").set("<Press Key>")
        self.binding = True
        self.app.bind("<KeyPress>", lambda ev, el=element: self.keyboard_bind(ev, el))
        self.app.bind("<ButtonPress>", lambda ev, el=element: self.mouse_bind(ev, el))
        self.app.bind("<MouseWheel>", lambda ev, el=element: self.mouse_wheel_bind(ev, el))

    def unload_all(self):
        process_name = self.app.ahk[self.app.ahk.rfind("\\") + 1:]
        subprocess.Popen(["taskkill", "/F", "/IM", process_name])

    def edit_path(self):
        path = askopenfilename()
        if not path:
            return
        path = path.replace("/", "\\")
        self.app.ahk = path
        self.app.json_settings["ahk_path"] = path
        if len(self.app.ahk) > 30:
            text = self.app.ahk[:self.app.ahk.find("\\") + 1] + "...\\" + \
                   self.app.ahk[self.app.ahk.rfind("\\") + 1:]
        else:
            text = self.app.ahk
        self.app.active_scripts_window.path_label.configure(text="AutoHotkey.exe path: " + text, cursor="hand2")
        self.app.active_scripts_window.path_label.bind("<Button-1>", self.app.open_path)

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

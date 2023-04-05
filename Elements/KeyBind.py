import subprocess
import tkinter
import customtkinter
from Elements.ctk_toplevel import CTkToplevel

mouse_keys = {1: "LButton", 3: "RButton", 2: "MButton", 4: "XButton1", 5: "XButton2"}


class KeyBind(CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.geometry("150x150")
        self.title("LazyHub")
        self.iconbitmap("cat.ico")
        self.resizable(width=False, height=False)
        self.withdraw()

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.pack(anchor="center", expand=True)

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Press bind key here")
        self.label_1.pack(anchor="center")
        self.protocol("WM_DELETE_WINDOW", self.close)

    def mouse_bind(self, event, element):
        try:
            key = mouse_keys[event.num]
        except:
            self.grab_release()
            self.withdraw()
            return
        if element.cget("textvariable").get() == key:
            self.grab_release()
            self.withdraw()
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.grab_release()
        self.withdraw()
        self.app.settings_window.save_button.configure(state="normal")

    def key_bind(self, event, element):
        key = subprocess.check_output([self.app.ahk, self.app.lib_path+"\\key_decode.ahk", f'{event.keycode}']).decode("utf-8")
        if element.cget("textvariable").get() == key:
            self.grab_release()
            self.withdraw()
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.grab_release()
        self.withdraw()
        self.app.settings_window.save_button.configure(state="normal")

    def mouse_wheel_bind(self, event, element):
        key = None
        if event.delta > 0:
            key = "WheelUp"
        if event.delta < 0:
            key = "WheelDown"
        if element.cget("textvariable").get() == key:
            self.grab_release()
            self.withdraw()
            return
        placeholder = tkinter.StringVar(value=key)
        element.configure(textvariable=placeholder)
        self.grab_release()
        self.withdraw()
        self.app.settings_window.save_button.configure(state="normal")

    def close(self):
        self.grab_release()
        self.withdraw()

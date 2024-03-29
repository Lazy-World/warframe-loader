import threading
import customtkinter
import requests
from Elements.ctk_toplevel import CTkToplevel


class ConfirmationPopup(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.condition = False
        self.main_app = main_app
        self.geometry("150x100")
        self.title("LazyHub")
        self.resizable(False, False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Are you sure?")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.button_1 = customtkinter.CTkButton(self.main_frame, text="Yes", command=self.confirm_event, width=50)
        self.button_1.grid(row=1, column=0, padx=10, pady=10)

        self.button_2 = customtkinter.CTkButton(self.main_frame, text="No", command=self.decline, width=50)
        self.button_2.grid(row=1, column=1, padx=10, pady=10)

        self.iconbitmap("assets\\cat.ico")
        self.protocol("WM_DELETE_WINDOW", self.decline)

    def confirm_event(self):
        threading._start_new_thread(self.confirm, ())

    def confirm(self):
        self.condition = False
        self.main_app.settings_window.upd_settings_button.configure(state="disabled")
        self.main_app.settings_window.upd_settings_button.grid_forget()
        self.main_app.settings_window.upd_settings_button_processing.grid(row=0, column=0,
                                                                          padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.main_app.after(50, self.processing_animation, self.condition)

        self.withdraw()
        self.grab_release()
        self.main_app.check_path()
        settings = self.main_app.lib_path + "\\game_settings.ahk"
        key_decode = self.main_app.lib_path + "\\key_decode.ahk"
        r1 = requests.get("https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/libraries/game_settings.ahk")
        with open(settings, 'wb') as f:
            f.write(r1.content)
        for child in self.main_app.settings_window.items_list.winfo_children():
            child.grid_forget()
        self.main_app.settings_window.generate_settings()

        self.condition = True
        self.main_app.settings_window.upd_settings_button.configure(state="normal")
        self.main_app.settings_window.upd_settings_button_processing.grid_forget()
        self.main_app.settings_window.upd_settings_button.grid(row=0, column=0, padx=(20, 20), pady=(10, 0),
                                                               sticky="nsew")

    def decline(self):
        self.withdraw()
        self.grab_release()

    def processing_animation(self, condition):
        if not self.condition:
            self.main_app.settings_window.upd_settings_button_processing.\
                configure(image=next(self.main_app.reload_button_icon_anim))
            self.main_app.after(50, self.processing_animation, self.condition)
        else:
            return

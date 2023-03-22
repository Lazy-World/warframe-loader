import getpass
import customtkinter
import requests
from Elements.ctk_toplevel import CTkToplevel


class ConfirmationPopup(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.geometry("150x100")
        self.title("LazyHub")
        self.resizable(False, False)
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Are you sure?")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.button_1 = customtkinter.CTkButton(self.main_frame, text="Yes", command=self.confirm, width=50)
        self.button_1.grid(row=1, column=0, padx=10, pady=10)
        self.button_1 = customtkinter.CTkButton(self.main_frame, text="No", command=self.decline, width=50)
        self.button_1.grid(row=1, column=1, padx=10, pady=10)
        self.path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.iconbitmap("cat.ico")
        self.protocol("WM_DELETE_WINDOW", self.decline)

    def confirm(self):
        filename = self.main_app.path + "\\lib\\game_settings.ahk"
        r = requests.get("https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/libraries/game_settings.ahk")
        with open(filename, 'wb') as f:
            f.write(r.content)
        self.withdraw()
        self.grab_release()

    def decline(self):
        self.withdraw()
        self.grab_release()

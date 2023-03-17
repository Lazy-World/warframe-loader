import getpass
import customtkinter
import requests
from Elements.ctk_toplevel import CTkToplevel


class ConfirmationPopup(CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.geometry("180x200")
        self.title("LazyHub")
        self.label_1 = customtkinter.CTkLabel(self, text="Are you sure?")
        self.label_1.grid(row=0, column=0, padx=20, pady=20)
        self.button_1 = customtkinter.CTkButton(self, text="Yes", command=self.confirm)
        self.button_1.grid(row=1, column=0, padx=20, pady=20)
        self.button_1 = customtkinter.CTkButton(self, text="No", command=self.decline)
        self.button_1.grid(row=2, column=0, padx=20, pady=20)
        self.path = 'C:\\Users\\%s\\AppData\\Roaming\\LazyHub' % getpass.getuser()
        self.iconbitmap("cat.ico")
        self.protocol("WM_DELETE_WINDOW", self.decline)

    def confirm(self):
        filename = self.main_app.path + "\\lib\\game_settings.ahk"
        r = requests.get("https://raw.githubusercontent.com/Lazy-World/warframe-ahk/main/libraries/game_settings.ahk")
        with open(filename, 'wb') as f:
            f.write(r.content)
        self.withdraw()

    def decline(self):
        self.withdraw()

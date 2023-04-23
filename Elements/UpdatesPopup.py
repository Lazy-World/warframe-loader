import customtkinter
from Elements.ctk_toplevel import CTkToplevel


class UpdatePopup(CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.geometry("210x150")
        self.title("LazyHub")
        self.geometry(f"+{app.winfo_rootx()}+{app.winfo_rooty()}")
        self.iconbitmap("assets\\cat.ico")
        self.withdraw()
        self.resizable(width=False, height=False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="New version of LazyHub avaliable")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.update_now = customtkinter.CTkButton(self.main_frame, text="Download",
                                                  command=self.download_update)
        self.update_now.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.update_later = customtkinter.CTkButton(self.main_frame, text="Download Later",
                                                    command=self.app.close_update_popup)
        self.update_later.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def download_update(self):
        self.app.close_update_popup()
        self.app.workshop_window.update_application()

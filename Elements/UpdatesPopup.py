import customtkinter
from Elements.ctk_toplevel import CTkToplevel


class UpdatePopup(CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.geometry("250x80")
        self.title("LazyHub")
        self.geometry(f"+{app.winfo_rootx()}+{app.winfo_rooty()}")
        self.iconbitmap("assets\\cat.ico")
        self.withdraw()
        self.resizable(width=False, height=False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="New version of LazyHub avaliable\n "
                                                                    "You can download it on Updates menu")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

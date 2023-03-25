import customtkinter
from Elements.ctk_toplevel import CTkToplevel


class NoUpdatesRequired(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("180x80")
        self.title("LazyHub")
        self.iconbitmap("cat.ico")
        self.withdraw()
        self.resizable(width=False, height=False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="There is no updates")
        self.label_1.grid(row=0, column=0, padx=35, pady=10, sticky="nsew")

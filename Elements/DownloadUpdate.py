import _tkinter
import os
import customtkinter
import requests

from Elements.ctk_toplevel import CTkToplevel


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


class DownloadWindow(CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.geometry("260x150")
        self.main_app = app
        self.title("LazyHub")
        self.iconbitmap("cat.ico")
        self.grab_set()
        self.downloads = get_download_path()
        self.geometry(f"+{app.winfo_rootx() + 500}+{app.winfo_rooty()}")
        self.resizable(width=False, height=False)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=self._fg_color)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Downloading latest version of LazyHub")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.progress_bar = customtkinter.CTkProgressBar(self.main_frame, width=240)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.progress_bar.set(0)

        self.open_folder_button = customtkinter.CTkButton(self.main_frame, text="Open folder", width=240,
                                                          state="disabled", command=self.open_folder)
        self.open_folder_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def download(self):
        with open(self.downloads+"\\"+"LazyHub_v." + self.main_app.online_version + ".exe", 'wb') as f:
            response = requests.get(
                "https://raw.githubusercontent.com/Lazy-World/warframe-ahk/LazyHub/LazyHub/LazyHub.exe", stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    try:
                        self.progress_bar.set(done / 50)
                    except _tkinter.TclError:
                        f.close()
                        os.remove(f.name)
                        return
        try:
            self.label_1.configure(text="Latest version downloaded")
            self.open_folder_button.configure(state="normal")
        except _tkinter.TclError:
            return

    def open_folder(self):
        os.startfile(self.downloads)

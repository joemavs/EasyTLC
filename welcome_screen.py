import tkinter as tk
from tkinter import filedialog
from PIL import Image

class WelcomeScreen:

    def __init__(self, master, on_start_callback):
        self.master = master  # 'master' is the main window (root)
        self.on_start_callback = on_start_callback
        self.master.title("EasyTLC")
        self.setup_ui()

    def setup_ui(self):

        label = tk.Label(self.master, text="Welcome to EasyTLC", font=("Arial", 16)) # Creates welcome label
        label.pack(padx=20, pady=20)

        upload_button = tk.Button(self.master, command=self.browse_files, text='Upload TLC Image') # Adds upload button
        upload_button.pack(padx = 20, pady = 20)


    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("All Files", "*.*"),))
        try:
            image = Image.open(filename)
            self.on_start_callback(image)
        except:
            print("This file could not be opened")







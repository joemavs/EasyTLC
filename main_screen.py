import tkinter as tk
from PIL import ImageTk

class MainScreen:

    def __init__(self, master, image):
        self.master = master  # 'master' is the main window (root)
        self.image = image
        self.setup_ui()
        self.wait_for_sf_click()
    def setup_ui(self):

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)  # Add padding for better appearance

        self.label = tk.Label(self.frame, text="Please mark where the solvent front is", font=("Arial", 16))
        self.label.pack()

        # Get width and height bounds of user screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Resize image using PIL
        self.image.thumbnail((screen_width*0.8,screen_height*0.8))

        # Create a Canvas to hold the image and draw on it
        self.canvas_width = self.image.width  # Use the resized image width
        self.canvas_height = self.image.height  # Use the resized image height
        self.canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        image_tk = ImageTk.PhotoImage(self.image)
        self.image_tk = image_tk  # Store it as an instance attribute

        # Center the image in the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.image_tk.width()
        image_height = self.image_tk.height()

        # Calculate the top-left corner coordinates for centering the image
        x = (canvas_width - image_width) // 2
        y = (canvas_height - image_height) // 2
        print(x)
        print(y)

        # Create the image on the canvas at the calculated coordinates
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.master.update()
        # Get current window width and height
        self.win_width = self.master.winfo_width()
        win_height = self.master.winfo_height()

        x = (screen_width // 2) - (self.win_width // 2)
        y = (screen_height // 2) - (win_height // 2)

        self.master.geometry(f"{self.win_width}x{win_height}+{x}+{y}")  # Center it

    def wait_for_sf_click(self):
        self.master.bind("<Button-1>", lambda event: self.click_handler(event, "solvent front"))

    def wait_for_bl_click(self):
        self.label.config(text="Now, mark where the baseline is")
        self.master.bind("<Button-1>", lambda event: self.click_handler(event, "baseline"))

    def click_handler(self, event, line):
        print(f"Mouse clicked at ({event.x}, {event.y})")

        # Add section that checks if this is desired

        self.master.unbind("<Button-1>")  # Stop listening for clicks
        self.show_line(event.y)

        if line == "solvent front":
            self.y_solvent_front = event.y
            self.wait_for_bl_click()
        elif line == "baseline":
            self.baseline = event.y




    def show_line(self, y_coord):
        print(y_coord)
        self.canvas.create_line(0, y_coord, self.win_width, y_coord)




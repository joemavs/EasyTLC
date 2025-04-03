import tkinter as tk

import cv2
import numpy as np
from PIL import ImageTk, Image
from skimage.measure import label, regionprops
from skimage.color import label2rgb


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


        # Create the image on the canvas at the calculated coordinates
        self.rgb_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

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
            self.solvent_front_y = event.y
            self.wait_for_bl_click()
        elif line == "baseline":
            self.baseline_y = event.y
            self.spot_detection()




    def show_line(self, y_coord):
        print(y_coord)
        self.canvas.create_line(0, y_coord, self.win_width, y_coord)

    def spot_detection(self):
        self.label.config(text="")
        hsv_image = self.image.convert("HSV")

        # Convert to a numpy array
        hsv_array = np.array(hsv_image)
        mask_bool = self.threshold_yellow(hsv_array)
        labeled_image = label(mask_bool)

        # Extract region properties
        props = regionprops(labeled_image)

        # Create list of centroids y vals
        centroid_y = []
        print(f"Number of detected blobs: {len(props)}")
        for i, prop in enumerate(props, start=1):
            print(f"Blob {i}: Area={prop.area}, Centroid={prop.centroid}")
            centroid_y.append(prop.centroid[0])

        for y_val in centroid_y:
            rf_value = self.calculate_rf(y_val)
            if 0.35 < rf_value < 0.66:
                print("detected")


        binary_array = (mask_bool.astype(np.uint8)) * 255
        binary_pil = Image.fromarray(binary_array, mode="L")
        self.mask_photo = ImageTk.PhotoImage(binary_pil)

        self.canvas.itemconfig(self.rgb_image, image=self.mask_photo)

    def threshold_yellow(self, hsv_array):
        """
        Binarizes an image to detect yellow regions based on HSV thresholds.
        Pixels within the defined range for yellow are set to 1 (white), others to 0 (black).

        Returns a binary image highlighting yellow regions.
        """

        # Define threshold ranges - Need UV light to edit this and perfect as it changes
        lower_bound = np.array([0, 50, 50])
        upper_bound = np.array([30, 255, 255])

        # Threshold the HSV image using cv2.inRange
        mask = cv2.inRange(hsv_array, lower_bound, upper_bound)

        # Convert the cleaned mask to a boolean array (True where yellow is detected)
        mask_bool = mask > 0
        return mask_bool

    def calculate_rf(self,centroid_y):
        rf = (self.baseline_y - centroid_y) / (self.baseline_y - self.solvent_front_y)
        return rf











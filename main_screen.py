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
        self.oval_ids = []
        self.line_ids = []
        self.setup_ui()
        self.crop()

    def setup_ui(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)  # Add padding for better appearance

        self.label = tk.Label(self.frame, text="Please click on the corners of the TLC plate", font=("Arial", 16))
        self.label.pack()

        # Get width and height bounds of user screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Resize image using PIL
        self.image.thumbnail((screen_width * 0.8, screen_height * 0.8))

        # Create a Canvas to hold the image and draw on it
        self.canvas_width = self.image.width  # Use the resized image width
        self.canvas_height = self.image.height  # Use the resized image height
        self.canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        image_tk = ImageTk.PhotoImage(self.image)
        self.image_tk = image_tk  # Store it as an instance attribute

        # Create the image on the canvas at the top-left corner
        self.rgb_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.master.update()
        # Get current window width and height
        self.win_width = self.master.winfo_width()
        win_height = self.master.winfo_height()

        x = (screen_width // 2) - (self.win_width // 2)
        y = (screen_height // 2) - (win_height // 2)

        self.master.geometry(f"{self.win_width}x{win_height}+{x}+{y}")  # Center the window

    def crop(self):
        """
        Allows the user to manually select a rectangular region in an image by clicking four corners.
        """
        self.corners = []
        self.master.bind("<Button-1>", lambda event: self.corner_click_handler(event))

    def corner_click_handler(self, event):
        print(f"Mouse clicked at ({event.x}, {event.y})")
        x, y = event.x, event.y
        self.corners.append((x, y))
        # Draw a small red circle at the clicked point
        r = 3  # radius for the marker
        oval_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='red', outline='red')
        self.oval_ids.append(oval_id) # Append to list of oval ids

        if len(self.corners) == 4:
            print("Selected points:", self.corners)
            self.master.unbind("<Button-1>")  # Stop listening for clicks

            # Remove the markers
            for oid in self.oval_ids:
                self.canvas.delete(oid)

            x_min_crop = min(val[0] for val in self.corners)
            x_max_crop = max(val[0] for val in self.corners)
            y_min_crop = min(val[1] for val in self.corners)
            y_max_crop = max(val[1] for val in self.corners)



            # Crop the image using PIL's crop method
            self.cropped_image_pil = self.image.crop((x_min_crop, y_min_crop, x_max_crop, y_max_crop))

            # Convert the cropped PIL image to a Tkinter PhotoImage
            self.cropped_image = ImageTk.PhotoImage(self.cropped_image_pil)

            # Update the canvas image with the new cropped image
            self.canvas.itemconfig(self.rgb_image, image=self.cropped_image)

            # Calculate the new center position
            canvas_center_x = self.canvas_width // 2
            canvas_center_y = self.canvas_height // 2
            cropped_img_width = self.cropped_image.width()
            cropped_img_height = self.cropped_image.height()

            self.canvas.config(width=cropped_img_width, height=cropped_img_height)

            # Resize the main window to fit the new canvas size
            new_win_width = cropped_img_width + 20  # add padding
            new_win_height = cropped_img_height + 20
            self.master.geometry(f"{self.master.winfo_width()}x{new_win_height}");
            self.wait_for_sf_click()

    def wait_for_sf_click(self):
        self.label.config(text="Please mark where the solvent front is")
        self.master.bind("<Button-1>", lambda event: self.click_handler(event, "solvent front"))

    def wait_for_bl_click(self):
        self.label.config(text="Now, mark where the baseline is")
        self.master.bind("<Button-1>", lambda event: self.click_handler(event, "baseline"))

    def click_handler(self, event, line):
        print(f"Mouse clicked at ({event.x}, {event.y})")
        self.master.unbind("<Button-1>")  # Stop listening for clicks
        self.show_line(event.y)

        if line == "solvent front":
            self.solvent_front_y = event.y
            self.wait_for_bl_click()
        elif line == "baseline":
            self.baseline_y = event.y
            self.spot_detection()

    def show_line(self, y_coord):
        print("Line at y =", y_coord)
        line_id = self.canvas.create_line(0, y_coord, self.win_width, y_coord)
        self.line_ids.append(line_id)

    def spot_detection(self):
        self.label.config(text="")
        # Convert the cropped image to HSV using PIL
        hsv_image = self.cropped_image_pil.convert("HSV")
        hsv_array = np.array(hsv_image)
        mask_bool = self.threshold_yellow(hsv_array)
        # Label connected components in the binary mask
        labeled_image = label(mask_bool)

        # Remove blobs with area smaller than 100
        for region in regionprops(labeled_image):
            if region.area < 100:
                labeled_image[labeled_image == region.label] = 0
        # Re-label the filtered image
        labeled_image = label(labeled_image > 0)



        # Extract region properties from the filtered, labeled image
        props = regionprops(labeled_image)
        print(f"Number of detected blobs after filtering: {len(props)}")
        j = 0
        for i, prop in enumerate(props):
            print(f"Blob {i+1}: Area={prop.area}, Centroid={prop.centroid}")
            rf_value = self.calculate_rf(prop.centroid[0])
            if 0.35 < rf_value < 0.6:
                print("detected")
                j = j+1

            else:
                labeled_image[labeled_image == regionprops(labeled_image)[j].label] = 0



        # Create the labelled overlay using label2rgb
        rgb_array = np.array(self.cropped_image_pil)
        labelled_overlay = label2rgb(labeled_image, image=rgb_array, bg_label=0, alpha=0.5)
        # Convert the overlay to uint8 and then to a PIL image
        labelled_overlay_uint8 = (labelled_overlay * 255).astype(np.uint8)
        labelled_pil = Image.fromarray(labelled_overlay_uint8)
        self.labelled_photo = ImageTk.PhotoImage(labelled_pil)

        # Remove sf and baseline lines
        for l_id in self.line_ids:
            self.canvas.delete(l_id)

        # Update the canvas image to show the labelled components overlay
        self.canvas.itemconfig(self.rgb_image, image=self.labelled_photo)

    def threshold_yellow(self, hsv_array):
        """
        Binarizes an image to detect yellow regions based on HSV thresholds.
        """
        lower_bound = np.array([0, 30, 50])
        upper_bound = np.array([30, 255, 255])
        mask = cv2.inRange(hsv_array, lower_bound, upper_bound)
        mask_bool = mask > 0
        return mask_bool

    def calculate_rf(self, centroid_y):
        rf = (self.baseline_y - centroid_y) / (self.baseline_y - self.solvent_front_y)
        return rf
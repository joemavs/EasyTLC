import tkinter as tk
from welcome_screen import WelcomeScreen
class MainApp:
    def __init__(self):
        # Create the main application window
        self.root = tk.Tk()
        self.show_welcome_screen()         # Calls function that shows welcome screen


    def show_welcome_screen(self):
        self.welcome_screen = WelcomeScreen(self.root, self.on_welcome_done)    # Initialize the welcome screen object and pass the main window to it


    def run(self):
        # Start the application's main event loop
        self.root.mainloop()

    def on_welcome_done(self, image):
        # Code to transition to the next screen
        self.


if __name__ == "__main__":
    app = MainApp()
    app.run()

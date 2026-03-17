# This is a comment
"""
Uses the Pillow library to create a simple image editor with a GUI built using Tkinter
The user can open an image, apply filters, and save the edited image.
"""

# verifyDeps.py is a separate file that checks the integrity of the requirements.txt file before installing dependencies
# Made it separate to avoid any potential issues with importing modules before they are installed
# Also allows for better separation of concerns and keeps the main application code cleaner, and easier reuseability of the dependency verification code in other projects if needed
from verifyDeps import ensure_dependencies

# verify + install dependencies first
ensure_dependencies()

### Imports
# tkinter is used for the GUI and file dialogs
import tkinter as tk
from tkinter import filedialog

# PIL (Pillow) is used for image processing and manipulation
from PIL import Image, ImageTk

# I forgot how class worked and needed to relearn them, so I made a class for the main application to keep everything organized and encapsulated
# Sadly or gladly depending on how you look at it, I did review classes and junk.


# SketchyShop class is the main application class that contains all the functionality for the image editor
class SketchyShop:
    def __init__(self, root):

        # The root variable is the main window of the application, and we set the title of the window to "Sketchyshop"
        self.root = root
        self.root.title("Sketchyshop")

        # The image variable will hold the currently loaded image, and the photo variable will hold the PhotoImage object that is used to display the image on the canvas
        self.image = None
        self.photo = None

        # Canvas where the image is displayed
        self.canvas = tk.Canvas(root, width=800, height=600, bg="gray20")
        self.canvas.pack()

        # Buttons
        frame = tk.Frame(root)
        frame.pack()

        # all da buttons. Each for the different functions of the image editor, each button doing there function
        tk.Button(frame, text="Open", command=self.open_image).pack(side=tk.LEFT)
        tk.Button(frame, text="Save", command=self.save_image).pack(side=tk.LEFT)
        tk.Button(frame, text="Grayscale", command=self.grayscale).pack(side=tk.LEFT)
        tk.Button(frame, text="Sepia", command=self.sepia).pack(side=tk.LEFT)
        tk.Button(frame, text="Lighten", command=self.lighten).pack(side=tk.LEFT)
        tk.Button(frame, text="Darken", command=self.darken).pack(side=tk.LEFT)

    ### These functions are all pretty self explanatory, but I'll explain them anyway for the sake of completeness and I'll explain what they actually do in the code comments

    # The display_image function converts the PIL image to a PhotoImage for Tkinter, resizes the canvas to fit the image, and then displays the image centered on the canvas
    def display_image(self):
        # Convert the PIL image to a PhotoImage for Tkinter
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.image.width, height=self.image.height)
        # Clear the canvas and display the image centered
        # self.canvas.delete("all")
        self.canvas.create_image(
            self.image.width // 2, self.image.height // 2, image=self.photo
        )

    # The open_image function opens a file dialog to select an image file, loads the image using PIL, converts it to RGB mode, and then displays it on the canvas
    def open_image(self):

        # Open a file dialog to select an image file, and then load the image using PIL and convert it to RGB mode (to ensure it has 3 color channels) before displaying it on the canvas
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        # If a file was selected, we load the image using PIL, convert it to RGB mode, to have a 3 color channels, and then display it on the canvas
        if path:
            self.image = Image.open(path).convert("RGB")
            self.display_image()

    # The save_image function opens a file dialog to select a save location and file name, and then saves the current image to that location using PIL
    def save_image(self):

        # If there is no image loaded, we return early and do nothing
        if not self.image:
            return

        # Open a file dialog to select a save location and file name, and then save the current image to that location using PIL
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )

        # If a save location was selected, we save the current image to that location using PIL
        if path:
            self.image.save(path)

    # The grayscale function applies a grayscale filter to the current image by calculating the luminance of each pixel and setting the red, green, and blue channels to that luminance value, effectively converting the image to shades of gray. After processing all pixels, it updates the displayed image on the canvas.
    def grayscale(self):

        # If there is no image loaded, we return early and do nothing
        if not self.image:
            return

        # We load the pixel data of the image into a variable called pixels, which allows us to access and modify the color values of each pixel in the image
        pixels = self.image.load()

        # We loop through each pixel in the image using nested loops, where y iterates over the height of the image and x iterates over the width of the image.
        # For each pixel, we retrieve the red, green, and blue color values, calculate the luminance using a weighted average formula, and then set the color channels of that pixel to the calculated luminance value, effectively converting it to a shade of gray. Same crap.
        for y in range(self.image.height):
            for x in range(self.image.width):
                r, g, b = pixels[x, y]
                lum = int(r * 0.299 + g * 0.587 + b * 0.114)

                # We set the color channels of that pixel to the calculated luminance value, effectively converting it to a shade of gray
                pixels[x, y] = (lum, lum, lum)

        # After processing all pixels, we call the display_image function to update the displayed image on the canvas with the newly applied grayscale filter
        self.display_image()

    # The sepia function applies a sepia filter to the current image by calculating new red, green, and blue values for each pixel using a specific formula that gives the image a warm, brownish tone. It processes each pixel in the image, updates the color values accordingly, and then updates the displayed image on the canvas.
    def sepia(self):

        # If there is no image loaded, we return early and do nothing
        if not self.image:
            return

        # We load the pixel data of the image into a variable called pixels, which allows us to access and modify the color values of each pixel in the image
        pixels = self.image.load()

        # We loop through each pixel in the image using nested loops, where y iterates over the height of the image and x iterates over the width of the image.
        # For each pixel, we retrieve the red, green, and blue color values, calculate
        for y in range(self.image.height):
            for x in range(self.image.width):
                r, g, b = pixels[x, y]

                # We calculate new red, green, and blue values for each pixel using a specific formula that gives the image a warm, brownish tone. The formula is based on a common sepia filter algorithm that applies different weights to the original color channels to achieve the desired effect.
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                # We set the color channels of that pixel to the newly calculated sepia values, ensuring that we cap the values at 255 to prevent overflow and maintain valid color values. This effectively applies the sepia filter to the image.
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))

        # After processing all pixels, we call the display_image function to update the displayed image on the canvas with the newly applied sepia filter
        self.display_image()

    # The lighten function increases the brightness of the current image by adding a fixed value to the red, green, and blue color channels of each pixel, while ensuring that the resulting values do not exceed 255. It processes each pixel in the image, updates the color values accordingly, and then updates the displayed image on the canvas.
    def lighten(self):

        # If there is no image loaded, we return early and do nothing
        if not self.image:
            return

        # We load the pixel data of the image into a variable called pixels, which allows us to access and modify the color values of each pixel in the image
        pixels = self.image.load()

        # We loop through each pixel in the image using nested loops, where y iterates over the height of the image and x iterates over the width of the image.
        # For each pixel, we retrieve the color values, add a fixed value (in this case, 20) to each channel to increase the brightness, and then set the color channels of that pixel to the new values, ensuring that we cap the values at 255 to prevent overflow and maintain valid color values. This effectively lightens the image.
        for y in range(self.image.height):
            for x in range(self.image.width):
                r, g, b = pixels[x, y]

                # We add a fixed value (in this case, 20) to each channel to increase the brightness, and then set the color channels of that pixel to the new values
                pixels[x, y] = (min(r + 20, 255), min(g + 20, 255), min(b + 20, 255))

        # After processing all pixels, we call the display_image function to update the displayed image on the canvas with the newly applied lightening effect
        self.display_image()

    # The darken function decreases the brightness of the current image by subtracting a fixed value from the color channels of each pixel
    def darken(self):

        # If there is no image loaded, we return early and do nothing
        if not self.image:
            return

        # We load the pixel data of the image into a variable called pixels, which allows us to access and modify the color values of each pixel in the image
        pixels = self.image.load()

        # Copy and pasted, we loop through each pixel in the image using nested loops, where y iterates over the height of the image and x iterates over the width of the image.
        # For each pixel, we retrieve the color values, subtract
        for y in range(self.image.height):
            for x in range(self.image.width):
                r, g, b = pixels[x, y]

                # We subtract a fixed value, in this case, 20, from each channel to decrease the brightness, and then set the color channels of that pixel to the new values
                pixels[x, y] = (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))

        # After processing all pixels, we call the display_image function to update the displayed image on the canvas with the newly applied darkening effect
        self.display_image()


# Finally, we create the main application window, instantiate the SketchyShop class with that window, and start the Tkinter main loop to run the application
root = tk.Tk()
# We create the main application window, instantiate the SketchyShop class with that window, and start the Tkinter main loop to run the application
app = SketchyShop(root)
# We start the Tkinter main loop to run the application, which keeps the window open and responsive to user interactions until the user closes it
root.mainloop()

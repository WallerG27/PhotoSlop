"""
images.py
Updared version of Kenneth Lambert's teaching library.

Supports more than just GIF

Supports:
GIF, PNG, JPG, JPEG, BMP, TIFF

Requires:
pip install pillow tkinterdnd2
> I really didn't want to force people to how to download something
> verifyDeps.py is a security check and downloads the files automatically
> Keeps the application safe from injection attacks, and also makes it easier for users to get started.
"""

# importlib is used to dynamically import the PIL library after ensuring dependencies are installed
import importlib

# We import the PIL library after ensuring dependencies are installed, which allows us to use the Image and ImageTk modules from the PIL library to work with images in our application. This dynamic import is necessary because we want to ensure that the required dependencies are installed before we attempt to use them, and it also helps to prevent potential issues with missing or incompatible libraries.
import subprocess

# sys is used to get the path to the current Python executable, which is needed to run the pip install command
import sys

# We import the PIL library after ensuring dependencies are installed, which allows us to use the Image and ImageTk modules from the PIL library to work with images in our application. This dynamic import is necessary because we want to ensure that the required dependencies are installed before we attempt to use them, and it also helps to prevent potential issues with missing or incompatible libraries.
from verifyDeps import ensure_dependencies

# verify + install dependencies first
ensure_dependencies()

# Now safe to import
import os
import tkinter as tk

# We import the Image and ImageTk modules from the PIL library, which are used to work with images in our application. The Image module provides functionality for opening, manipulating, and saving images, while the ImageTk module allows us to convert PIL images into a format that can be displayed in Tkinter applications. By importing these modules after ensuring that the required dependencies are installed, we can safely use their functionality in our application without worrying about missing or incompatible libraries.
from PIL import Image as PILImage
from PIL import ImageTk


# ImageView is a subclass of tk.Canvas that creates a new window to display an image. It has methods to close the window and check if it is closed. The Image class represents an image and provides methods to get its dimensions, get and set pixel values, draw the image in a window, save the image to a file, clone the image, and provide a string representation of the image. The Image class uses the PIL library to handle image manipulation and display.
class ImageView(tk.Canvas):
    # The __init__ method initializes the ImageView by creating a new top-level window, setting its title and size based on the dimensions of the image, and packing the canvas into the window. It also stores a reference to the image and initializes a closed flag to track whether the window has been closed.
    def __init__(self, image, title="Image"):
        # We create a new top-level window using tk.Toplevel, which allows us to have multiple windows in our application. We set the protocol for the window's close event to call the close method of the ImageView class, which will
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)

        # We call the superclass constructor
        super().__init__(master, width=image.getWidth(), height=image.getHeight())

        # We set the title of the window to the provided title, and we make the window non-resizable to maintain the aspect ratio of the displayed image. Finally, we pack the canvas into the window to make it visible.
        master.title(title)
        master.resizable(False, False)
        self.pack()

        # We store a reference to the image and initialize a closed flag to track whether the window has been closed. This allows us to manage the state of the window and ensure that we can properly close it when needed, as well as check if it is still open before attempting to display or manipulate the image.
        self.master = master
        self.image = image
        self.closed = False

    # The close method sets the closed flag to True, destroys the master window, and sets the canvas reference in the image to None. This ensures that when the window is closed, we properly clean up resources and prevent any further interactions with the closed window or its associated image.
    def close(self):
        self.closed = True
        self.master.destroy()
        self.image.canvas = None

    # The isClosed method simply returns the value of the closed flag, allowing other parts of the application to check if the window has been closed before attempting to interact with it or display the image. This helps to prevent errors and ensure that we are only working with valid, open windows when displaying or manipulating images.
    def isClosed(self):
        return self.closed


# The Image class represents an image and provides methods to get its dimensions, get and set pixel values, draw the image in a window, save the image to a file, clone the image, and provide a string representation of the image. The Image class uses the PIL library to handle image manipulation and display.
class Image:
    def __init__(self, *args):

        # We initialize the canvas reference to None, which will be used to store a reference to the ImageView canvas when the image is drawn. This allows us to manage the display of the image and ensure that we can properly update or close the window when needed.
        self.canvas = None

        # Load from file
        if len(args) == 1:
            filename = args[0]

            # We check if the specified file exists using os.path.exists. If the file does not exist, we raise an exception to inform the user that the file was not found. This helps to prevent errors and ensure that we are working with valid image files when attempting to load and display them.
            if not os.path.exists(filename):
                raise Exception("File not found")

            # If the file exists, we use the PIL library to open the image file and convert it to RGB format. We store the resulting PIL image object in the self.pil attribute, and we also store the filename for reference. This allows us to work with the image data and display it in our application using the PIL library's functionality.
            self.pil = PILImage.open(filename).convert("RGB")
            self.filename = filename

        # Create blank image
        else:
            width, height = args
            self.pil = PILImage.new("RGB", (width, height), (255, 255, 255))
            self.filename = "image.png"

        # We get the width and height of the image from the PIL image object and store them in the self.width and self.height attributes. This allows us to easily access the dimensions of the image when needed, such as when displaying it in a window or manipulating its pixel data.
        self.width, self.height = self.pil.size
        self.photo = None

    # The getWidth method simply returns the width of the image
    def getWidth(self):
        return self.width

    # The getHeight method simply returns the height of the image
    def getHeight(self):
        return self.height

    # The getPixel method takes x and y coordinates as input and returns the color value of the pixel at those coordinates in the image. It uses the PIL library's getpixel method to retrieve the color value, which is returned as a tuple of (red, green, blue) values. This allows us to access and manipulate the color data of individual pixels in the image.
    def getPixel(self, x, y):
        return self.pil.getpixel((x, y))

    # The setPixel method takes x and y coordinates and a color value as input, and sets the color of the pixel at those coordinates in the image to the specified color. It uses the PIL library's putpixel method to update the color value of the pixel, which allows us to modify the image by changing the color data of individual pixels.
    def setPixel(self, x, y, color):
        self.pil.putpixel((x, y), tuple(map(int, color)))

    # The draw method displays the image in a window. It creates an ImageView if one doesn't already exist for the image.
    def draw(self):

        # If there is no existing canvas (i.e., ImageView) for this image, we create a new ImageView instance, passing the current image and its filename as parameters. This allows us to display the image in a new window using the ImageView class, which handles the creation and management of the window and canvas for displaying the image.
        if not self.canvas:
            self.canvas = ImageView(self, self.filename)

        # We convert the PIL image to a format that can be displayed in Tkinter using ImageTk.PhotoImage, and we store the resulting PhotoImage object in the self.photo attribute. This allows us to display the image on the canvas of the ImageView window using Tkinter's image handling capabilities.
        self.photo = ImageTk.PhotoImage(self.pil)

        # We use the create_image method of the canvas to display the image at the center of the canvas, using the self.photo attribute as the image source. This allows us to render the image in the window and make it visible to the user.
        self.canvas.create_image(self.width // 2, self.height // 2, image=self.photo)

        # Finally, we call the mainloop method of the root Tkinter window to start the event loop and keep the application running, allowing the window to remain open and responsive to user interactions until the user closes it.
        _root.mainloop()

    # The save method saves the image to a file. If a filename is provided as an argument, it updates the self.filename attribute before saving. It uses the PIL library's save method to write the image data to the specified file, allowing us to save our modified images to disk for later use or sharing.
    def save(self, filename=None):

        # If a filename is provided as an argument, we update the self.filename attribute to the new filename. This allows us to specify a different file name when saving the image, giving us flexibility in how we manage and organize our saved images.
        if filename:
            self.filename = filename

        # We use the save method of the PIL image object to save the image to the specified filename. This writes the image data to disk, allowing us to preserve our changes and access the saved image file later.
        self.pil.save(self.filename)

    # The clone method creates a new Image instance with the same dimensions as the current image, and it copies the pixel data from the current image to the new image using the copy method of the PIL image object. This allows us to create a duplicate of the image that can be modified independently without affecting the original image.
    def clone(self):

        # A new Image instance is created with the same dimensions as the current image, and we copy the pixel data from the current image to the new image using the copy method of the PIL image object
        # This allows us to create a duplicate of the image that can be modified independently without affecting the original image.
        new = Image(self.width, self.height)
        new.pil = self.pil.copy()
        return new

    # The __str__ method provides a string representation of the image, including its filename (if available) and its dimensions (width and height). This allows us to easily print or display information about the image in a human-readable format
    def __str__(self):

        # We initialize an empty string variable called rep, which will be used to build the string representation of the image.
        # If the image has a filename, we append the filename information to the rep string
        # Then, we append the width and height of the image to the rep string
        rep = ""
        if self.filename:
            rep += f"File name: {self.filename}\n"

        # We append the width and height of the image to the rep string, providing information about the dimensions of the imag        rep += f"Width: {self.width}\nHeight: {self.height}"

        # Finally, we return the complete string representation of the image, which includes its filename and its dimensions
        return rep

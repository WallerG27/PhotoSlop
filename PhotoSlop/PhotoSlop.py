# verifyDeps.py is a separate file that checks the integrity of the requirements.txt file before installing dependencies
# Made it separate to avoid any potential issues with importing modules before they are installed
# Also allows for better separation of concerns and keeps the main application code cleaner, and easier reuseability of the dependency verification code in other projects if needed
from verifyDeps import ensure_dependencies

# verify + install dependencies first
ensure_dependencies()

### Imports
# tkinter is used for the GUI and file dialogs
import tkinter as tk
from tkinter import Menu, filedialog, simpledialog

# PIL (Pillow) is used for image processing and manipulation
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Handle size for the resize handles
# I already know need to move this so it scales with the canvas size, but I want to sent this update and work on it later
HANDLE_SIZE = 10


# Class for the PhotoSlop application
class PhotoSlop:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoSlop")

        # Layout
        main = tk.Frame(root)
        main.pack(fill=tk.BOTH, expand=True)

        # Left panel (canvas and toolbar)
        left = tk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right panel (layer list)
        right = tk.Frame(main, width=220, bg="#1e1e1e")
        right.pack(side=tk.RIGHT, fill=tk.Y)

        # Toolbar
        toolbar = tk.Frame(left, bg="#2a2a2a")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Canvas
        self.canvas = tk.Canvas(left, bg="#1a1a1a")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Layer panel
        self.layer_list = tk.Listbox(right, bg="#2a2a2a", fg="white")
        self.layer_list.pack(fill=tk.BOTH, expand=True)
        self.layer_list.bind("<<ListboxSelect>>", self.select_from_list)

        # Layer controls
        for text, cmd in [
            ("Up", self.layer_up),
            ("Down", self.layer_down),
            ("Rename", self.rename_layer),
            ("Delete", self.delete_layer),
        ]:
            tk.Button(right, text=text, command=cmd).pack(fill=tk.X)

        # State
        self.layers = []
        self.selected_layer = None

        # Zoom and pan state
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Drag state
        self.mode = None
        self.handle = None
        self.drag_start = None

        # Toolbar buttons
        tk.Button(toolbar, text="Add Image", command=self.add_image).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Add Text", command=self.add_text).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Filters", command=self.show_filters).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Save", command=self.save_image).pack(side=tk.LEFT)
        # I might update this to the scroll wheel
        tk.Button(toolbar, text="+", command=self.zoom_in).pack(side=tk.LEFT)
        tk.Button(toolbar, text="-", command=self.zoom_out).pack(side=tk.LEFT)

        # Mouse
        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<Button-3>", self.start_pan)
        self.canvas.bind("<B3-Motion>", self.pan_canvas)

    # -------------------------
    # Layers
    # -------------------------
    def add_image(self):
        # Open file dialog to select an image
        path = filedialog.askopenfilename()
        # Return if no file was selected
        if not path:
            return
        # Load the image and convert to RGBA
        img = Image.open(path).convert("RGBA")

        # Add the image layer to the layers list
        self.layers.append(
            {
                "name": f"Image {len(self.layers)}",
                "type": "image",
                "image": img,
                "x": 200,
                "y": 200,
                "width": img.width,
                "height": img.height,
            }
        )

        # Update the layer list and render the canvas
        self.update_layer_list()
        self.render()

    # Add a text layer to the layers list and render the canvas
    def add_text(self):
        # Prompt the user to enter text
        text = simpledialog.askstring("Text", "Enter text:")
        # Return if no text was entered
        if not text:
            return

        # Add the text layer to the layers list
        self.layers.append(
            {
                "name": f"Text {len(self.layers)}",
                "type": "text",
                "text": text,
                "x": 200,
                "y": 200,
                "width": 300,
                "height": 60,
            }
        )

        # Update the layer list and render the canvas
        self.update_layer_list()
        self.render()

    # Update the layer list to reflect the current layers
    def update_layer_list(self):
        # Clear the layer list and insert each layer's name
        self.layer_list.delete(0, tk.END)
        # Iterate through the layers and insert each one's name
        for l in self.layers:
            self.layer_list.insert(tk.END, l["name"])

    # Handle layer selection from the listbox
    def select_from_list(self, e):
        # Get the selected index and update the selected layer
        idx = self.layer_list.curselection()
        # If an index is selected, update the selected layer and render
        if idx:
            self.selected_layer = self.layers[idx[0]]
            self.render()

    # Get the selected index from the layer list
    def get_selected_index(self):
        # Return the selected index, or None if no selection
        s = self.layer_list.curselection()
        return s[0] if s else None

    # Move the selected layer up in the stack
    def layer_up(self):
        # Swap the selected layer with the one below it, if possible
        i = self.get_selected_index()
        # If the selected layer is not the last one, swap it with the one below
        if i is not None and i < len(self.layers) - 1:
            # Swap the layers
            self.layers[i], self.layers[i + 1] = self.layers[i + 1], self.layers[i]
            self.update_layer_list()
            self.layer_list.selection_set(i + 1)
            self.render()

    # Move the selected layer down in the stack
    def layer_down(self):
        # Swap the selected layer with the one above it, if possible
        i = self.get_selected_index()
        # If the selected layer is not the first one, swap it with the one above
        if i is not None and i > 0:
            # Swap the layers
            self.layers[i], self.layers[i - 1] = self.layers[i - 1], self.layers[i]
            self.update_layer_list()
            self.layer_list.selection_set(i - 1)
            self.render()

    # Rename the selected layer
    def rename_layer(self):
        # Prompt the user to enter a new name for the selected layer
        if not self.selected_layer:
            return
        # Show a dialog to enter the new name
        name = simpledialog.askstring("Rename", "New name:")

        # If the user entered a name, update the layer and render
        if name:
            self.selected_layer["name"] = name
            self.update_layer_list()

    # Delete the selected layer
    def delete_layer(self):
        # Get the selected index and delete the layer if one is selected
        i = self.get_selected_index()
        # If an index is selected, delete the layer and update the list and canvas
        if i is not None:
            # Remove the layer from the list and reset the selected layer
            del self.layers[i]
            self.selected_layer = None
            self.update_layer_list()
            self.render()

    # -------------------------
    # Rendering
    # -------------------------
    def render(self):
        # Clear the canvas and draw each layer
        self.canvas.delete("all")  # test this
        base = Image.new("RGBA", (1280, 720), (25, 25, 25))
        draw = ImageDraw.Draw(base)

        # Draw each layer on the base image
        for layer in self.layers:
            # Calculate the layer's position and size on the canvas
            sx = layer["x"] * self.zoom + self.offset_x
            sy = layer["y"] * self.zoom + self.offset_y
            sw = layer["width"] * self.zoom
            sh = layer["height"] * self.zoom

            # Draw the layer based on its type
            if layer["type"] == "image":
                img = layer["image"].resize((int(sw), int(sh)))
                base.paste(img, (int(sx), int(sy)), img)

            # Draw text on the base image
            elif layer["type"] == "text":
                size = int(sh)
                # Choose a font based on the layer's size
                try:
                    font = ImageFont.truetype("arial.ttf", size)
                # Fall back to the default font if a custom font is not available
                except:
                    font = ImageFont.load_default()
                # Draw the text on the base image
                draw.text((sx, sy), layer["text"], fill="white", font=font)

            # Draw a selection border around the selected layer
            if layer == self.selected_layer:
                draw.rectangle([sx, sy, sx + sw, sy + sh], outline="#00ffcc", width=2)
                self.draw_handles(draw, sx, sy, sw, sh)

        # Convert the base image to a Tkinter-compatible format and display it on the canvas
        self.tk_image = ImageTk.PhotoImage(base)
        # Delete any existing canvas content and draw the new image
        self.canvas.delete("all")
        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    # Draw selection handles for a layer on the canvas
    def draw_handles(self, draw, x, y, w, h):
        # Draw 8 small rectangles around the layer to indicate selection
        size = HANDLE_SIZE / self.zoom
        # Define the 8 points around the layer's bounding box
        points = [
            (x, y),
            (x + w / 2, y),
            (x + w, y),
            (x, y + h / 2),
            (x + w, y + h / 2),
            (x, y + h),
            (x + w / 2, y + h),
            (x + w, y + h),
        ]
        # Draw each point as a small rectangle
        for px, py in points:
            draw.rectangle([px - size, py - size, px + size, py + size], fill="#00ffcc")

    # -------------------------
    # SAVE (the real upgrade)
    # -------------------------
    def save_image(self):
        # Prompt the user to select a file path and save the image
        path = filedialog.asksaveasfilename(defaultextension=".png")
        # If the user cancels, return
        if not path:
            return

        # Create a new image with a black background
        base = Image.new("RGBA", (1280, 720), (25, 25, 25))
        draw = ImageDraw.Draw(base)

        # Draw each layer onto the base image
        for layer in self.layers:
            # Get the layer's position and size
            x, y = layer["x"], layer["y"]
            w, h = int(layer["width"]), int(layer["height"])

            # Draw the layer based on its type
            if layer["type"] == "image":
                img = layer["image"].resize((w, h))
                base.paste(img, (int(x), int(y)), img)

            # Draw text if the layer is a text layer
            elif layer["type"] == "text":
                # Draw the text with a white fill
                try:
                    font = ImageFont.truetype("arial.ttf", int(h))
                # Use the default font if a custom font fails to load
                except:
                    font = ImageFont.load_default()
                # Draw the text on the base image
                draw.text((x, y), layer["text"], fill="white", font=font)

        # Save the base image to the specified path
        base.save(path)

    # -------------------------
    # Mouse
    # -------------------------
    def mouse_down(self, e):
        # Record the mouse position when the user clicks
        self.mouse_start = (e.x, e.y)  # Test is too
        x = (e.x - self.offset_x) / self.zoom
        y = (e.y - self.offset_y) / self.zoom

        # Reset the selected layer and mode, then find the clicked layer
        self.selected_layer = None
        self.mode = "move"
        self.handle = None

        # Find the clicked layer by iterating through the layers in reverse order
        for layer in reversed(self.layers):
            lx, ly = layer["x"], layer["y"]
            lw, lh = layer["width"], layer["height"]

            # Check if the click is within the layer's bounds
            if lx <= x <= lx + lw and ly <= y <= ly + lh:
                self.selected_layer = layer

                # Determine if the click is on a handle or the layer itself
                handles = {
                    "nw": (lx, ly),
                    "n": (lx + lw / 2, ly),
                    "ne": (lx + lw, ly),
                    "w": (lx, ly + lh / 2),
                    "e": (lx + lw, ly + lh / 2),
                    "sw": (lx, ly + lh),
                    "s": (lx + lw / 2, ly + lh),
                    "se": (lx + lw, ly + lh),
                }

                # Check if the click is on a handle, and set the mode accordingly
                for name, (hx, hy) in handles.items():
                    # If the click is close to a handle, set the mode to "resize" and record the handle
                    if abs(x - hx) < 10 and abs(y - hy) < 10:
                        self.mode = "resize"
                        self.handle = name

                # If the click is not on a handle, set the mode to "move"
                if self.handle is None:
                    self.mode = "move"

                # Exit the loop after finding the handle or mode
                break

        # Record the drag start position and render the canvas
        self.drag_start = (x, y)
        self.render()

    # Handle mouse drag events - move or resize the selected layer
    def mouse_drag(self, e):
        # If no layer is selected, do nothing
        if not self.selected_layer:
            return

        # Calculate the current position based on the mouse position and zoom
        x = (e.x - self.offset_x) / self.zoom
        y = (e.y - self.offset_y) / self.zoom

        # Calculate the change in position since the last drag event
        dx = x - self.drag_start[0]
        dy = y - self.drag_start[1]

        # Update the layer's position or size based on the mode
        l = self.selected_layer

        # If in move mode, update the layer's position
        if self.mode == "move":
            l["x"] += dx
            l["y"] += dy

        # If in resize mode, update the layer's size based on the handle
        elif self.mode == "resize":
            if "e" in self.handle:
                l["width"] += dx
            if "s" in self.handle:
                l["height"] += dy
            if "w" in self.handle:
                l["x"] += dx
                l["width"] -= dx
            if "n" in self.handle:
                l["y"] += dy
                l["height"] -= dy

            # Clamp the width and height to a minimum of 10 pixels
            l["width"] = max(10, l["width"])
            l["height"] = max(10, l["height"])

        # Record the new drag start position and render the canvas
        self.drag_start = (x, y)
        self.render()

    # -------------------------
    # Pan
    # -------------------------
    def start_pan(self, e):
        self.drag_start = (e.x, e.y)

    # Pan the canvas based on the mouse drag distance
    def pan_canvas(self, e):
        dx = e.x - self.drag_start[0]
        dy = e.y - self.drag_start[1]

        # Update the offset based on the drag distance
        self.offset_x += dx
        self.offset_y += dy

        # Record the new drag start position and render the canvas
        self.drag_start = (e.x, e.y)
        self.render()

    # -------------------------
    # Zoom
    # -------------------------
    # Zoom in the canvas by a factor of 1.2
    def zoom_in(self):
        self.zoom *= 1.2
        self.render()

    # Zoom out the canvas by a factor of 1.2
    def zoom_out(self):
        self.zoom /= 1.2
        self.render()

    # -------------------------
    # Filters
    # -------------------------
    # Show a menu of filters for the selected image layer
    def show_filters(self):
        # If no layer is selected or the layer is not an image, do nothing
        if not self.selected_layer or self.selected_layer["type"] != "image":
            return

        # Create a menu with Grayscale and Sepia options
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label="Grayscale", command=self.grayscale)
        menu.add_command(label="Sepia", command=self.sepia)
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    # Apply a grayscale filter to the selected image layer
    def grayscale(self):
        # Convert the image to grayscale and update the layer
        img = self.selected_layer["image"]
        self.selected_layer["image"] = img.convert("L").convert("RGBA")
        self.render()

    # Apply a sepia filter to the selected image layer
    def sepia(self):
        # Convert the image to sepia and update the layer
        img = self.selected_layer["image"]
        pixels = img.load()
        # Iterate over each pixel and apply the sepia filter
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255), a)
        # Render the updated image
        self.render()


# Create the main window and run the application
root = tk.Tk()
app = PhotoSlop(root)
root.mainloop()

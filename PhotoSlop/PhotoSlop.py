# This is a comment
from images import Image

# Ends the menu
QUIT = ""
# Holds the possible inputs
COMMANDS = ("1", "2", "3", "4", "5", "")
# Prints the possible inputs
MENU = """How do you want the results?:
1   Lighten or Darken
2   Shapen the Image
3   Filters
4   Grey scale
5   Enlarge The image
ENTER   Quit the program"""

global image


def runCommand(command):
    """Selects and runs a command."""
    if command == "1":  # Lighten or Darken
        lightOrDark()
    elif command == "2":  # Shapen the Image
        sharpen(image)
    elif command == "3":  # Filters
        print("WIP")
    elif command == "4":  # Grey scale
        print("WIP")

    elif command == "5":  # Enlarge The image
        image.draw()


def acceptCommand():
    """Inputs and returns a legitimate command number."""
    while True:
        command = input("\nEnter a number: ")
        if not command in COMMANDS:
            print("Error: command not recognized")
        else:
            return command


### All the filters
def grayscale(image):
    """Converts an image to grayscale using the
    psychologically accurate transformations."""
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            r = int(r * 0.299)
            g = int(g * 0.587)
            b = int(b * 0.114)
            lum = r + g + b
            image.setPixel(x, y, (lum, lum, lum))


def grayscale2(image):
    """Converts an image to grayscale using the crude average
    of the r, g, and b"""
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)

            lum = (r + g + b) // 3
            image.setPixel(x, y, (lum, lum, lum))


def colorFilter(image, rgbTriple):
    """Adds the given rgb values to each pixel after normalizing."""
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            red = min((red + rgbTriple[0]), 255)
            green = min((green + rgbTriple[1]), 255)
            blue = min((blue + rgbTriple[2]), 255)
            image.setPixel(x, y, (red, green, blue))


def lighten(image, amount):
    """Lightens image by amount."""
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            red = min(int(red + amount), 255)
            green = min(int(green + amount), 255)
            blue = min(int(blue + amount), 255)
            image.setPixel(x, y, (red, green, blue))


def darken(image, amount):
    """Darkens image by amount."""
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            red = max(int(red - amount), 0)
            green = max(int(green - amount), 0)
            blue = max(int(blue - amount), 0)
            image.setPixel(x, y, (red, green, blue))


def enlarge(image, scale):
    """Builds and returns a copy of the image which is larger
    by the factor."""
    imageCopy = image.clone()
    newWidth = int(image.getWidth() * scale)
    newHeight = int(image.getHeight() * scale)
    for y in range(newHeight):
        for x in range(newWidth):
            leftPixel = image.getPixel(int(x / scale), int(y / scale))
            rightPixel = image.getPixel(
                image.getWidth() - int(x / scale) - 1, int(y / scale)
            )
            imageCopy.setPixel(x, y, leftPixel)
            imageCopy.setPixel(newWidth - x - 1, y, rightPixel)
    return imageCopy


def posterize(image, rgb):
    coloredPixel = rgb
    whitePixel = (255, 255, 255)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (r, g, b) = image.getPixel(x, y)
            average = (r + g + b) // 3
            if average < 128:
                image.setPixel(x, y, coloredPixel)
            else:
                image.setPixel(x, y, whitePixel)


def sepia(image):
    """Converts an image to sepia."""
    grayscale(image)
    for y in range(image.getHeight()):
        for x in range(image.getWidth()):
            (red, green, blue) = image.getPixel(x, y)
            if red < 63:
                red = int(red * 1.1)
                blue = int(blue * 0.9)
            elif red < 192:
                red = int(red * 1.15)
                blue = int(blue * 0.85)
            else:
                red = min(int(red * 1.08), 255)
                blue = int(blue * 0.93)
            image.setPixel(x, y, (red, green, blue))


def sharpen(image):
    """Builds and returns a sharpened image.  Expects an image
    and two integers (the degree to which the image should be sharpened and the
    threshold used to detect edges) as arguments."""
    """Builds and returns a new image in which the edges of
    the argument image are highlighted and the colors are
    reduced to black and white."""

    degree = int(input("to what degree do you want to sharpen the image? "))
    threshold = int(input("What the threshold? "))

    def average(triple):
        (r, g, b) = triple
        return (r + g + b) // 3

    # blackPixel = (0, 0, 0)
    # whitePixel = (255, 255, 255)
    sharpen = image.clone()
    for y in range(image.getHeight() - 1):
        for x in range(1, image.getWidth()):
            oldPixel = image.getPixel(x, y)
            leftPixel = image.getPixel(x - 1, y)
            bottomPixel = image.getPixel(x, y + 1)
            oldLum = average(oldPixel)
            leftLum = average(leftPixel)
            bottomLum = average(bottomPixel)

            (red, green, blue) = image.getPixel(x, y)
            newred = max((red - degree), 0)
            newgreen = max((green - degree), 0)
            newblue = max((blue - degree), 0)
            if abs(oldLum - leftLum) > threshold or abs(oldLum - bottomLum) > threshold:
                sharpen.setPixel(x, y, (newred, newgreen, newblue))
            else:
                sharpen.setPixel(x, y, (red, green, blue))
    return sharpen
    # outline = outline


def lightOrDark():
    choice = input("Do you want to lighten or darken the image? (L, D, or M fo menu) ")
    amount = int(input("By how much? "))
    if choice == "L":
        lighten(image, amount)
    elif choice == "D":
        darken(image, amount)
    elif choice == "M":
        menu()
    else:
        print("Invalid choice")
        lightOrDark()


def menu():
    while True:
        print("Sketchyshop!")
        print(MENU)
        command = acceptCommand()  # Checks the input was vaild
        runCommand(command)  # After it was shown to be vaild it runs it
        if command == QUIT:  # if command was quit it, well, quits
            break


def main():
    global image
    filename = input("Enter the image file name: ")
    image = Image(filename)
    menu()


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nProgram closed.")

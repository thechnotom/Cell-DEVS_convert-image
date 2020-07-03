from PIL import Image
import sys
import json

if (len(sys.argv) != 1 and len(sys.argv) != 2):
    print("Usage: python3 convertImage.py [<config file>]")
    sys.exit(0)

configFile = "config.json"
if (len(sys.argv) == 2):
    configFile = sys.argv[1]

# Load configuration from file
config = ""
with open(configFile, "r") as f:
    config = f.read()
config = json.loads(config)

TOLERANCE = config["tolerance"]
cellColour = config["colours"]

def getLuminance (pixel):
    return (pixel[0] * 0.3) + (pixel[1] * 0.59) + (pixel[2] * 0.11)

def correctColour (pixel):
    pixel = list(pixel)
    for i in range(0, len(pixel)):
        if (abs(pixel[i]) < TOLERANCE):
            pixel[i] = 0
        elif (abs(pixel[i]) > TOLERANCE):
            pixel[i] = 255
        else:
            print("correctColour: Unable to correct colour: {0}".format(pixel))
    return pixel

def getColourString (pixel):
    pixel = correctColour(pixel)
    for i in pixel:
        if (i != 0 and i != 255):
            return "255,255,255"
    return str(pixel[0]) + "," + str(pixel[1]) + "," + str(pixel[2])

image = Image.open(config["files"]["input"], "r")
width, height = image.size
pixels = list(image.getdata())

if (not image.mode == "RGB"):
    print("WARNING: image is not RGB")

for i in pixels:
    if (getColourString(i) == "other"):
        print("Unrecognized colour: {0} -> utilizing as AIR".format(i))

cells = []
for x in range (0, width):
    for y in range (0, height):
        pixel = pixels[(width * y) + x]
        colour = getColourString(pixel)
        if (colour == "255,255,255"):
            continue
        cells.append(str(x) + "," + str(y) + "=" + str(cellColour[colour]["concentration"]) + "," +
                     str(cellColour[colour]["type"]) + "," + str(cellColour[colour]["counter"]))

with open(config["files"]["output"], "w") as f:
    for i in range(0, len(cells)):
        f.write(cells[i])
        if (i != len(cells) - 1):
            f.write("\n")

print("Complete (model data stored in \"{0}\")".format(config["files"]["output"]))
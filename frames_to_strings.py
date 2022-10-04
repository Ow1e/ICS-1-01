from PIL import Image
import json
import os
from tqdm import tqdm

"""
Thx https://levelup.gitconnected.com/how-to-convert-an-image-to-ascii-art-with-python-in-5-steps-efbac8996d5e
I did some changes to this for colour support, typos and other stuff
"""

ascii_characters_by_surface = "#$@&"

KEYS = {
    "rgb": "\u001b[47;1m\u001b[37;1m",
    "r": "\u001b[41;1m\u001b[31;1m",
    "g": "\u001b[42;1m\u001b[32;1m",
    "b": "\u001b[44;1m\u001b[34;1m",
    "rg": "\u001b[42;1m\u001b[42m", # Red + Green = Green
    "rb": "\u001b[45;1m\u001b[35;1m", # Red + Blue = Magenta
    "gb": "\u001b[46;1m\u001b[33;1m", # Green + Blue = Yellow
    "": "\u001b[47m"
}

def convert_to_ascii_art(image):
    ascii_art = []
    (width, height) = image.size
    depth = 0 # Depth for colours, finds average and sets it as minimum so half the screen is always coloured
    depth_array = []
    for y in range(0, height - 1):
        for x in range(0, width - 1):
            px = image.getpixel((x, y))
            (r, g, b) = px
            depth_array.append(r+g+b)


    depth = 70

    for y in range(0, height - 1):
        line = ''
        for x in range(0, width - 1):
            px = image.getpixel((x, y))
            line += convert_pixel_to_character(px, depth=depth)
        ascii_art.append(line)
    return {"text": ascii_art, "depth": depth}

def dictate_rgb(r, g, b, base = 80):
    rt = r >= base
    bt = b >= base
    gt = g >= base
    red, blue, green = "", "", ""
    if rt: red = "r"
    if bt: blue = "b"
    if gt: green = "g"

    sel = f"{red}{green}{blue}"

    #if r+g+b == (base/2)*3 and sel == "":
    #    sel = f""

    return KEYS[sel]


def convert_pixel_to_character(pixel, depth = 80):
    (r, g, b) = pixel
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_by_surface) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return dictate_rgb(r, g, b, depth)+ascii_characters_by_surface[index]+"\u001b[0m"

if __name__ == '__main__':
    i = 0
    working = True
    frames = []
    print("Loading Frames")
    while working:
        print(i)
        image = Image.open(f'frames/frame_{i}.png')
        frames.append(convert_to_ascii_art(image))
        i += 1
        working = os.path.exists(f"frames/frame_{i}.png")

    print("Packetizing")
    packet = {
        "frames": frames
    }

    print("Saving")
    with open("frames.json", "w") as f:
        json.dump(packet, f)
import json
from time import sleep

with open("frames.json") as f:
    data = json.load(f)

dump = ""

FPS = 30
NATIVE = 30

for n, i in enumerate(data["frames"]):
    text  = ""
    for l in i["text"]:
        text += l+"\n"
    sleep(1/FPS)
    print("\n"+text, end="")
import json
from strip_ansi import strip_ansi

print("Importing JSON")

with open("frames.json") as f:
    data = json.load(f)

print("Imported")

BASE = """
' Adaptive OpenCV to ASCII/UTF-8 Charecters + Translation to SmallBasic
' I used https://software-solutions-online.com/vba-escape-characters/ for finding terminal attribute charecters
' Notes: Windows Terminal has a weird font so charecters are compressed

' This is the Char for a new line break
NEW_LINE = Text.GetCharacter(10)

{}

Sub RunFrame
    i = 1
    l = 0
    While l < 10
        TextWindow.Write(NEW_LINE)
        l = l+1
    EndWhile
    While i < Text.GetLength(frame)
        char = Text.GetSubText(frame, i, 1)
        If char = "R" Then
            TextWindow.ForegroundColor = "red"
        ElseIf char = "G" Then
            TextWindow.ForegroundColor = "green"
        ElseIf char = "B" Then
            TextWindow.ForegroundColor = "blue"
        ElseIf char = "W" Then
            TextWindow.ForegroundColor = "white"
        ElseIf char = "A" Then
            TextWindow.ForegroundColor = "green"
        ElseIf char = "M" Then
            TextWindow.ForegroundColor = "magenta"
        ElseIf char = "Y" Then
            TextWindow.ForegroundColor = "yellow"
        ElseIf char = "B" Then
            TextWindow.ForegroundColor = "lightgrey"
        ElseIf char = "N" Then
            TextWindow.ForegroundColor = ""
            TextWindow.Write(NEW_LINE)
        Else
            TextWindow.Write(char)
        EndIf
        i = i+1
    EndWhile 
EndSub

{}
"""

KEYS = {
    "W": "\u001b[47;1m\u001b[37;1m", # White
    "R": "\u001b[41;1m\u001b[31;1m", # Red
    "G": "\u001b[42;1m\u001b[32;1m", # Green
    "B": "\u001b[44;1m\u001b[34;1m", # Blue
    "A": "\u001b[42;1m\u001b[42m", # Red + Green = Green
    "M": "\u001b[45;1m\u001b[35;1m", # Red + Blue = Magenta
    "Y": "\u001b[46;1m\u001b[33;1m", # Green + Blue = Yellow (Teal Background + Yellow Text)
    "B": "\u001b[47m", # This is L White, but could be black with white text
    "N": "\n", # In SmallBasic should also reset other stuff
}

def replace_frame(frame):
    text = ""
    for i in frame:
        t = i
        for l in KEYS:
            t = t.replace(KEYS[l], l)
        text += t + "N"
    return text

frames = []
ends = []

for n, i in enumerate(data["frames"]):
    frames.append(f'frame{n} = "{strip_ansi(replace_frame(i["text"]))}"\n')
    ends.append(f"frame = frame{n}\nRunFrame()\nProgram.Delay(33)\n")

frames_str = ""
for i in frames:
    frames_str += i

ends_str = ""
for i in ends:
    ends_str += i

file = BASE.format(frames_str, ends_str)
with open("export.sb", "w") as f:
    f.write(file)
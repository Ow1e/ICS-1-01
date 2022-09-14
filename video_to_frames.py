"""This turns a video into frames, and downscales the image too"""

import cv2
from tqdm import tqdm
from time import sleep
import os

SLICE = 7

def vidtrans(vidcap):
    success = True
    images = []
    while success:
        success,image = vidcap.read()
        if success:
            images.append(image)
    return images

def take_image(img):
    scale_percent = SLICE # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

if __name__ == "__main__":
    if not os.path.exists("frames"):
        print("Taking Video...")
        video = cv2.VideoCapture('allstar.mp4')
        frames = vidtrans(video)
        os.mkdir("frames")
        for i, frame in tqdm(enumerate(frames)):
            cv2.imwrite(f"frames/frame_{i}.png", take_image(frame))

# OCRSCREEN
# The PyAutoGUI library covered in Chapter 23 can take scrrenshots and save them to an image, while the Pillow library covered in Chapter 21 can crop images. 
# PyAutoGUI also has a MouseInfo application for finding XY coordinates on screen.
# Write a program named ocrscreen.py that takes a screenshot, crops the image to just the text portion in the screenshot, then passes it on to 
# PyTesseract for OCR. The progam should append the recognized text to the end of a text file name output.txt.

import time

import pyautogui
from PIL import Image
import pytesseract as tess


# The coordinates for the text portion. Change as needed:
LEFT = 200
TOP = 200
RIGHT = 1000
BOTTOM = 800

print('switch to your target window!')
n = 5
while n >= 0:
    time.sleep(1) 
    print(n)
    n -= 1

# Capture a screenshot:
img = pyautogui.screenshot()

# Crop the screenshot to the text portion:
img = img.crop((LEFT, TOP, RIGHT, BOTTOM))

# Run OCR on the cropped image:
text = tess.image_to_string(img, lang='eng')

# Add the OCR text to the end of output.txt
with open('output.txt', 'a') as text_file:
    text_file.write(text)



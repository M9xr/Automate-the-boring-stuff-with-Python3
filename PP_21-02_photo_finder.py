# Identifying Photo Folder on the Hard Drive
# I have a bad habit of transferring files from my digital camer to temporary 
# folders somewhere on the hard drive and then forgetting about these folders. 
# It would be nice to write a program that could scan the entire hard drive and find thsese leftover photo folders.
# Write a program that goes through every folder on your hard drive and finds potential photo folders.
# Of cours, first'll have to define what you consider a "photo folder" to be; let's say that it's any folder where more than half
# of the files are photos. And how do you define what files are photos?
# First, a photo file must have the file extention .png or .jpg. Also, photos are large images; a photo file's width and height
# must both be larger than 500 pixels. This is a safe bet, since most digital camera photos are several thousand pixels in width and height.
# As hint, here's rough skeleton of what this program might look like:

# Import modules and write comments to descirbe this program.

import os
import sys

from PIL import Image

def main():
    for folder_name, subfolders, filenames in os.walk("/home/"):
        num_photo_files = 0
        num_non_photo_files = 0
        for filename in filenames:
            # Check if the file extension isn't .png .jpg.
            if not filename.endswith(('.png', '.jpg')):
                num_non_photo_files += 1
                continue # Skip to the next filename.

            # Open image using Pillow.
            image_path = os.path.join(folder_name, filename)
            try:
                the_image = Image.open(image_path)
            except Exception:
                num_non_photo_files += 1
                continue
            # Check if the width & height are larger than 500.
            width, height = the_image.size
            if width > 500 and height > 500:
                # Image is large enough to be considered a photo.
                num_photo_files += 1
            else:
                # Image is too small to be a photo.
                num_non_photo_files += 1
    
        # If more than half of files were photos,
        # print the absolute path of the folder.
        if num_photo_files > num_non_photo_files:
            print(folder_name)

if __name__ == "__main__":
    main()

# It's not uncommon for a few unneeded but humongous files or folder to take up the bulk of the space on you hard drive.
# If you're trying to free up room on your computer, it's more effective to identify the largest unneeded files first.
# Write a program that walks through a folder tree and searches for exceptionally large files or folders - say,
# ones that have a file size of more than 100MB. (Remember that, to get a file's size, you can use os.path.getsize() from the os module.)
# Print these files with their absolute path to the screen.

import os, sys
from pathlib import Path

# Configuration
THRESHOLD = 100 * 1024 * 1024   # 100MB
MB = 1024 * 1024 


destination = input('Where to look for large files (more than 100MB)? >> ')
destination = Path(destination)
# Check if the folder exists
if not destination.exists():
    print('Error: ' + str(destination) + ' doesn\'t exist\n')
    sys.exit(1)
if not destination.is_dir():
    print('Error: ' + str(destination) + ' is not a directory\n')
    sys.exit(1)


# Storage for folder sizes
dir_sizes = {}
file_counter = 0
for folder_name, subfolders, files in os.walk(destination, topdown=False):
    folder_path = Path(folder_name)
    total_size = 0
    
    # Add file sizes
    for file in files:
        file_path = folder_path/file
        try:
            size = file_path.stat().st_size
        except (PermissionError, FileNotFoundError):
            continue
        total_size += size
        # Check if the file is above the threshold
        if size > THRESHOLD:
            file_counter += 1
            print(f"{file_counter:3}. FILE {file_path.resolve()} - {size / MB:.2f} MB")

    # Add subfolder sizes
    for subfolder in subfolders:
        subfolder_path = folder_path/subfolder
        total_size += dir_sizes.get(subfolder_path, 0)

    
    # Store this subfolder total size
    dir_sizes[folder_path] = total_size

    # Check if the folder is large
    if total_size > THRESHOLD:
        file_counter += 1
        print(f"{file_counter:3}. FOLDER {folder_path.resolve()} - {total_size / MB:.2f} MB")

print(f"\nFound {file_counter} large items.")

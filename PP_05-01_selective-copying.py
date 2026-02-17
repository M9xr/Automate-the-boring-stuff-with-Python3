# Write a program that walks through a folder tree and searches for files with
# a certian extention (such as .pdf or .jpg). Copy these files from their current 
# location to a new folder.

import os, shutil, sys, send2trash
from pathlib import Path

source = input('In which folder to search for files?\n')
source = Path(source)
# Check whether the folder exists
if not source.exists():
    print(str(source) + " doesn't exist\n")
    sys.exit(1)
if not source.is_dir():
    print('Error: ' + str(source) + ' is not a directory\n')
    sys.exit(1)

extension = input('What extension to look for?\n')
# Normalize the extension
if len(extension) == 0:
    print("Error: extension cannot be empty")
    sys.exit(1)
extension = extension.lower()
if extension[0] != '.':
    extension = '.' + extension 
    
destination = input('Where to copy?\n')
destination = Path(destination)
if destination.resolve() == source.resolve():
    print('Error: destination cannot be the same as source\n')
    sys.exit(1)
if destination.resolve().is_relative_to(source.resolve()):
    print("Error: destination cannot be inside source.")
    sys.exit(1)
if destination.exists():
    print(str(destination) + ' already exists, options:\nsend it to bin and create a new folder?: yes(y) no(n),\nadd files to the existing folder?: add(a)')
    answer = input('y/n/a?: ').strip().lower()  # Handles accidential spaces and big letters. 
    # Program sends the file to trash, rather than deleting it - for safety reason.
    if answer == 'y':
        send2trash.send2trash(destination)
        destination.mkdir()
    elif answer == 'a':
        pass
    else:
        sys.exit(1)
else:
    destination.mkdir()

# Copy the files to the destinaiton. Make sure files won't overwrite each other when they have the same name
file_counter = 0
for folder_name, subfolders, files in os.walk(source):
    for file in files:
        source_file = Path(folder_name)/file
        if source_file.suffix.lower() == extension:
            # If file with this name exists, add suffix.
            if (destination / file).exists():
                suffix_counter = 1
                file_name = Path(file)
                while True:
                    new_name = file_name.stem + '(' + str(suffix_counter) + ')'+ file_name.suffix
                    if not (destination / new_name).exists():
                        break
                    suffix_counter += 1
                shutil.copy(source_file, destination / new_name)
            else:
                shutil.copy(source_file, destination)
            file_counter += 1

print(f'Copied {file_counter} files\n')    




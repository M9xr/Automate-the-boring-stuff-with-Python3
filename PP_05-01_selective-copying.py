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
    
#TODO: LATER, check whether the destination is not inside a subfolder of source.
destination = input('Where to copy?\n')
destination = Path(destination)
if destination == source:
    print('Error: destination cannot be the same as source\n')
    sys.exit(1)
if destination.exists():
    # For now, it is safer to exit the program, rather than deleting files.
    print(str(destination) + ' already exists, send it to bin and create a new folder? yes(y) no(n)')
    answer = input('y/n?: ')
    if answer == 'y':
        send2trash.send2trash(destination)
        destination.mkdir(exist_ok=True)
    else:
        sys.exit(1)
else:
    destination.mkdir()

for folder_name, subfolders, files in os.walk(source):
    #TODO: if file extension matches the extension user provided, copy the file to the destination
    for file in files:
        source_file = Path(folder_name)/file
        #TODO: I need to check whether file with the name already exsits in the destination, if so, add a growing prefix of suffix.
       #if file.lower().endswith(extension):
        if source_file.suffix.lower() == extension:
            if (destination / file).exists():
                counter = 1
                file_name = Path(file)
                while True:
                    new_name = file_name.stem + '(' + str(counter) + ')'+ file_name.suffix
                    if not (destination / new_name).exists():
                        break
                    counter += 1
                shutil.copy(source_file, destination / new_name)
            else:
                shutil.copy(source_file, destination)

    




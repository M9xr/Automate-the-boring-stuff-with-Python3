# Say your boss email you thousands of files with American-style dates (MM-DD-YYYY) in their names and needs them renamed
# to European style dates (DD-MM-YYYY). This boring task could take all day to do by hand! Instead, write a progrma that does the following: 
#   1. Searches all filenames in the current working directory and all subdirectories to American-style dates. Use the os.walk() function to
#      go through the subfolders.
#   2. Uses regular expressions to identify filenames with the MM-DD-YYYY pattern in them - for example, spam12-31-1900.txt. Assume the
#      months and days always use to digits, and that files with non-date matches don't exist. (You won't find files named something like 99-99-9999.txt.)
#   3. When a filename is found, rename the file with the month and day swapped to make it European-style. Use the shutil.move() function to do the renaming.

import os, shutil, re

pattern = re.compile(r'(.*?)(\d{2})-(\d{2})-(\d{4})(.*)')

source = os.getcwd()

for folder_name, subfolders, files in os.walk(source):
    for file in files:
        match = pattern.match(file)
        if match:
            old_path = os.path.join(folder_name, file)
            new_name = f"{match.group(1)}{match.group(3)}-{match.group(2)}-{match.group(4)}{match.group(5)}"
            new_path = os.path.join(folder_name, new_name)

            if file != new_name:
                print(old_path, "->", new_path)
                shutil.move(old_path, new_path)



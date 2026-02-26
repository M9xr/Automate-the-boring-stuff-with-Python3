# Write a program that finds all files with a given prefix, such as spam001.txt, spam002.txt, and so on, in a single folder
# and locates any gaps in the numbering (such as if there is a spam001.txt and spam003.txt but no spam002.txt).
# Have the program rename all the later files to close this gap.
# As an added challenge, write another progrma that can insert gaps into numbered files (and bump up the numbers in the filenemes after the gap)
# so that a new file can be inserted.

import sys, re, shutil
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
"""
extension = input('What extension to look for?\n')
# Normalize the extension
if len(extension) == 0:
    print("Error: extension cannot be empty")
    sys.exit(1)
extension = extension.lower()
if extension[0] != '.':
    extension = '.' + extension
"""
# This is a basic renumbering program. 
# It assumes that all files in the folder have the same base like "spam001.txt", "spam002.txt", where the base is "spam"
# TODO: Make it more roboust, find all all different bases and renumber them properly 
#pattern = re.compile(r'spam(\d{3}).txt')
#pattern = re.compile(rf'^spam(\d{{3}}){re.escape(extension)}$')

pattern = re.compile(r"^(spam)(\d+)(\.txt)$")
files = []
for file in source.iterdir():
    match = pattern.match(file.name)
    if match:
        number = int(match.group(2))
        files.append((number, file))

files.sort()

for expected, (actual_number, file_path) in enumerate(files, start=1):
    if actual_number != expected:
        new_name = f"spam{expected:03}.txt"
        file_path.rename(source / new_name)









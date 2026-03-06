# Write a program that finds all files with a given prefix, such as spam001.txt, spam002.txt, and so on, in a single folder
# and locates any gaps in the numbering (such as if there is a spam001.txt and spam003.txt but no spam002.txt).
# Have the program rename all the later files to close this gap.
# As an added challenge, write another program that can insert gaps into numbered files (and bump up the numbers in the filenemes after the gap)
# so that a new file can be inserted.

import sys, re, random
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

pattern = re.compile(r'^spam(\d{3})\.txt$')


# Extract all the files with the prefix
files = []
for file in source.iterdir():
    match = pattern.match(file.name)
    if match:
        number = int(match.group(1))
        files.append((number, file)) 
number_of_files = len(files)

if number_of_files == 0:
    print('No match found, exiting.\n')
    sys.exit(1)

# Randomize the number of gaps
number_of_gaps = random.randint(1, number_of_files)

# Randomize which files to replace with gaps
gaps_placement = []
while len(gaps_placement) < number_of_gaps:
    file_number = random.randint(1, number_of_files)
    if file_number not in gaps_placement: 
        gaps_placement.append(file_number)

# Sort gaps
gaps_placement.sort()

# Make the list start from the higest number
files.sort(reverse=True)

# Make the final layout for files
final_length = number_of_files + number_of_gaps
final_positions = [p for p in range(1, final_length + 1) if p not in gaps_placement]

# Some debug info
print("Gaps:", gaps_placement)
print("Final positions:", final_positions)

# Move the files 
for number, path in files:
    new_number = final_positions[number - 1]
    if new_number != number:
        print(f"{path.name} -> spam{new_number:03}.txt")
        new_name = f"spam{new_number:03}.txt"
        new_path = source / new_name
        path.rename(new_path)


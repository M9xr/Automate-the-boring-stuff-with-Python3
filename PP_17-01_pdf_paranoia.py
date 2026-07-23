# PDF Paranoia
# Using the os.walk() function from Chapter 11, write a script that will go through every PDF in a folder (and its subfolders) and encrypt the PDFs using a password provided on the command line.
# Save each encrypted PDF with an _encrypted.pdf suffix added to the original filename. Before deleting the original file, have the program attempt to read and decrypt the new file to ensure that it was 
# encrypted correctly.
# Then, write a program that finds all encrypted PDFs in a folder (and its subfolders) and creates a decrypted copy of the PDF using a provided password. IF the password is incorrect, the program
# should print a message to the user and continue to the next PDF.

import pypdf, os, sys 
from pathlib import Path

if len(sys.argv) != 2:
    print(f"{sys.argv[0]}: Encrypts recursively all pdfs starting from CWD. Usage: {sys.argv[0]} <password>")
    sys.exit(1)

password = sys.argv[1]

for folder, subfolders, filenames in os.walk('.'):
    the_dir = Path(folder)
    print('Current folder:', folder)
    for sub in subfolders:
        print('Subfolder:', sub)
    for filename in filenames:
        print('File:', filename)
        if filename.lower().endswith('.pdf'):
            try:
                reader = pypdf.PdfReader(the_dir/filename)
                if reader.is_encrypted:
                    print(f"{filename} is already encrypted, skipping.")
                    continue
                writer = pypdf.PdfWriter()
                writer.append(the_dir / filename)
                writer.encrypt(password, algorithm='AES-256') # Encrypting
                new_name = filename[0:len(filename) - 4] # New name without .pdf extension
                new_name = new_name + '_encrypted.pdf'
                with open(the_dir / new_name, 'wb') as file:
                    writer.write(file)

                reader = pypdf.PdfReader(the_dir / new_name)

                if reader.decrypt(password):
                    try:                  
                        os.remove(the_dir / filename)
                        print(f"{new_name} is encrypted, deleting {filename}")
                    except FileNotFoundError:
                        print(f"{filename} somehow vaninshed!")
                    except PermissionError:
                        print(f"Permission Error, can't remove {filename}")

                else:
                    print("Something went wrong")
            except (pypdf.errors.PdfStreamError, pypdf.errors.FileNotDecryptedError) as e:
                print(f"Skipping {filename}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error reading {filename} : {e}")
                continue

print("----------------Encrypting complete-----------------")
# PART II

for folder, subfolders, filenames in os.walk('.'):
    the_dir = Path(folder)
    print('Current folder:', folder)
    for sub in subfolders:
        print('Subfolder:', sub)
    for filename in filenames:
        print('File:', filename)
        if filename.lower().endswith('.pdf'):
            try:
                reader = pypdf.PdfReader(the_dir/filename)
                if reader.is_encrypted:
                    if reader.decrypt(password):
                        writer = pypdf.PdfWriter()
                        writer.append(reader)
                        if filename.lower().endswith('_encrypted.pdf'):
                            new_name = filename[0:len(filename) - len('_encrypted.pdf')] # removing _encrypted.pdf from the name
                        else:
                            new_name = filename[0:len(filename) - len('.pdf')] # removing ".pdf" from the name
                        new_name = new_name + '_decrypted.pdf'
                        with open(the_dir / new_name, 'wb') as file:
                            writer.write(file)
                    else:
                        print(f"Provided password for {filename} is incorrect")
            except (pypdf.errors.PdfStreamError, pypdf.errors.FileNotDecryptedError) as e:
                print(f"Skipping {filename}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error reading {filename} : {e}")
                continue







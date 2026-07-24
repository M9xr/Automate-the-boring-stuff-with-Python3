# PDF Password Breaker
# Say you have an encrypted PDF that you've forgotten the password to, but you remember it was a single English word.
# Trying to guess your forgotten password is quite a boring task. Instead, you can write a program that will decrypt the PDF by trying 
# every possible English word until it finds one that works. This is called a brute-force password attack. Download the text file dictionary.txt from
# the book's online resources. This dictionary file contains over 44,000 English words, with one word perl line.
# Using the file-reading skills you learned in Chapter 10, create a list of word strings by reading this file. Then, loop over each word in this list, passing
# it to the decrypt() method. You should try both the uppercase and lowercase form of each word. (On my laptop, going through all 88,000 uppercase and lowercase words from the dictionary file takes
# a couple of minutes. This is why you shouldn't use a simple English word for you passwords.)

import pypdf, sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"{sys.argv[0]} - PDF Password Breaker: Usage: {sys.argv[0]} <filename>")
    sys.exit(1)

filename = sys.argv[1]
reader = pypdf.PdfReader(filename) # Open the file to be decrypted
word_list = Path('dictionary.txt').read_text().splitlines()  # Split words into a nice list
for word in word_list:
    try:
        print(f'Trying {word}')
        if reader.decrypt(word).name != 'NOT_DECRYPTED':
            print(f"{filename} decrypted, the password is {word}")
            sys.exit(0)
        word = word[0].upper() + word[1:]
        if reader.decrypt(word).name != 'NOT_DECRYPTED':
            print(f"{filename} decrypted, the password is {word}")
            sys.exit(0)
    except Exception as e:
        print(f"Something went wrong on password <{word}>\nError code:{e}")
print(f"Decryption of {filename} failed.")







# This is a guess the number game.

import random
import pyttsx3


# Initialize engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(phrase):
    print(phrase)
    engine.say(phrase)
    engine.runAndWait()

secret_number = random.randint(1, 20)
speak('I am thinking of a number between 1 and 20.')

# Ask the player to guess 6 times.
for guesses_taken in range(1, 7):
    speak('Take a guess.')
    guess = int(input('>'))
    if guess < secret_number:
        speak(f'Your guess {guess} is too low.')
    elif guess > secret_number:
        speak(f'Your guess {guess} is too high.')
    else:
        break # This condition is the correct guess!

if guess == secret_number:
    speak('Good job! You got it in ' + str(guesses_taken) + ' guesses!')
else:
    speak('Nope. The number was ' + str(secret_number))

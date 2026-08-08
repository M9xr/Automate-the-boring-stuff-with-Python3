# Prettified Stopwatch
# Expand the stopwatch project from this chapter so that is uses the rjust() and ljust() string methods to "prettify" to output. (These methoda were covered in Chapter 8.)
# Next, use the pyperclip module introduced in Chapter 8 to copy the text output to the clipboard so that the user can quickly paste the output to a text file or email.

import time
import pyperclip

# Display the program's instructions.
print('Press ENTER to begin and to mark laps. Ctrl-C quits.')
input() # Press Enter to begin.
print('Started.')
start_time = time.time() # Get the first lap's start time.
last_time = start_time
lap_number = 1

# Start tracking the lap times.
strings_to_paste = []
try:
    while True:
        input()
        lap_time = round(time.time() - last_time, 2)
        total_time = round(time.time() - start_time, 2)
        lap_number_print = str(lap_number).rjust(4)
        total_time_print = str(total_time).rjust(7)
        lap_time_print = str(lap_time).rjust(5)
        string_time = f'Lap #{lap_number_print}: {total_time_print}(  {lap_time_print})'
        print(string_time, end='')
        strings_to_paste.append(string_time)
        lap_number += 1
        last_time = time.time() # Reset the last lap time.
except KeyboardInterrupt:
    # Handle the Ctrl-C exeption to keep its error message from displaying.
    final_string = '\n'.join(strings_to_paste)
    pyperclip.copy(final_string)
    pyperclip.paste()
    print('\nDone.')



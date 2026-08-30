# Email-Based Computer Control
# Write a program that checks an email or ntfy account every 15 minutes for
# any instructions you send it and executes those instructions automatically.
# For example, BitTorrent is a peer-to-peer downloading system. Using free
# BitTorrent software such as qBittornet, you can download large media files on your home computer.
# If you send the program a (completely legal, not at all piratical) BitTorrent link, the program will eventually check its email or look for nfty notifications, find
# the message, extract the link, and then launch qBittorent to start downloading the file. This way, you can have your home computer begin downloads while you're away and finish the
# (completely legal, not at all piratical) download by the time you return home.
# Chapter 19 covered how to launch programs on your computer using the subprocess.Popen() function. For example, the following call would launch the qBittorent program, along with a torrent file:
#   qbProcess = subprocess.Popen(['C:\\Program Files (x86)\\qBittorrent\\
#   qbittorrent.exe', 'shakespeare_complete_works.torrent'])
# Of course, you'll want the program to make sure that emails come from you. In particual, you might want to require that the emails contian a password, since it is fairly trivial for hackers to fake a "from"
# address in emails. The program should delete the emails it finds so that it doesn't repeat insturctions every time it checks the email account. As an extra feature,
# have the program email or text you a confirmaiton every time it executes a command. Since you won't be sitting in front of the computer that is running the program, it's a good idea to use the logging functions
# (see Chapter 5) to write a text file log that you can check if errors come up.
# The qBittornet program (as well as other BitTorrent applications) has a feature that enables it to quit automatically after the download completes.
# Chapter 19 explained how you can determine when a launched aplicaiton has quit with wait() method for Popen object. The wait() method call will block until qBittorent has stopped, and then your program can email
# or text you a notification that the download has completed.
# There are plenty of possible features you could add to this project. If you get stuck, you can download an example implementation of this progrma from https://nostarch.com/automate-boring-stuff-python-3rd-edition.

from pathlib import Path
import requests
import ezgmail
import json
import time
import datetime
import subprocess
import logging

logging.basicConfig(filename='EmailAndNTFY_checker.log', level=logging.DEBUG, format='%(asctime)s  -  %(levelname)s  -  %(message)s')
logging.debug('Start of program')


p = Path('command_credentials.txt')
credentials = p.read_text().splitlines()
command_password = credentials[0]
NFTY_server = credentials[1]

logging.debug('Credentials loaded')

def execute_command(message, software_type):
    
    logging.debug('Processing command from %s', software_type)

    if software_type == "email":
        print("Comparing password from email...")
        lines = message.splitlines()
        if len(lines) < 2:
            logging.debug('Invalid email command: fewer than 2 lines')
            print("Invalid email command")
            return 
        password = lines[0].strip()
        command = lines[1].strip()        
    elif software_type == "ntfy":
        print("Comparing password from ntfy...")
        lines = message.split()
        if len(lines) < 2:
            logging.debug('Invalid ntfy command: fewer than 2 fields')
            print("Invalid ntfy command")
            return 
        password = lines[0].strip()
        command = " ".join(lines[1:])
    else:
        logging.debug('Unsupported software type: %s', software_type)
        print(f"Program don't support {software_type}.")
        return

    logging.debug('Command received from %s: %s', software_type, command)

    if password != command_password:
        logging.debug('Password verification failed for %s', software_type)
        print('Wrong password or message in unrelated, exiting')
        return 

    logging.debug('Password verified for %s', software_type)

    try:
        logging.debug('Executing command: %s', command)
        print("running command")
        subprocess.run(command, shell = True, check = True)
        logging.debug('Command completed successfully')
        return 
    except Exception as e:
        logging.exception('Command execution failed')
        print(f"Error: {e}")
        return 

while True:
    logging.debug('Starting email check')
    for thread in ezgmail.unread():
        logging.debug('Unread email thread found')
        for message in thread.messages:
            logging.debug('Processing email: %s', message.subject)
            execute_command(message.body, "email")
            message.markAsRead()
            logging.debug('Email marked as read')


    logging.debug('Starting NTFY check')
    resp = requests.get(NFTY_server + '&since=15m')
    resp.raise_for_status()
    logging.debug('NTFY request successful')

    notifications = []

    for json_text in resp.text.splitlines():
        notifications.append(json.loads(json_text))

    logging.debug('Received %d NTFY notifications', len(notifications))

    last_stop = 0

    for i in range(len(notifications) -1, -1, -1):
        if notifications[i]["message"] == "StopExecuting":
            last_stop = i + 1
            logging.debug(
                'Found StopExecuting marker at notification %d',
                i
            )
            break

    for notification in notifications[last_stop:]:
        execute_command(notification["message"], "ntfy")
    
    if not notifications or notifications[-1]["message"] != "StopExecuting":
        logging.debug('Sending StopExecuting marker')
        requests.post(NFTY_server, "StopExecuting")
    

    dt = datetime.datetime.now()
    if dt.minute < 10:
        minutes = '0' + str(dt.minute)
    else:
        minutes = dt.minute

    logging.debug('Email/NTFY checked')
    print(f"Email/ntfy checker {dt.hour}:{minutes} Nothing to do.")
    logging.debug('Sleeping for 15 minutes')
    time.sleep(900) # Wait 15 minutes for next commands.




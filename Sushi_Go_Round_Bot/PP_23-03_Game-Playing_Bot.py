# Game-Playing Bot
"""
There is an old Flash game called Sushi Go rOund. The game involves clicking the correct ingredient buttons to fill customers' sushi orders.
The faster you fill orders without mistakes, the more points you get. This is a perfectly suited for a GUI automation program - and a way to cheat
to a high score! Although Flash is discontinures as a product, there are instrucitons for playing it offline on your computer and a list of websites that
host the Sushi Go Round game at https://github.com/asweigart/sushigoroundbot.
That GitHub repo also has the Python source code for a game-playing bot.
"""

import os
import logging

import pyautogui
import pyscreeze
from playwright.sync_api import sync_playwright
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.info) # uncomment to block debug log messages

# Food order constants (don't change these: the image filenames depend on these specific values)
ONIGIRI = 'onigiri'
GUNKAN_MAKI = 'gunkan_maki'
CALIFORNIA_ROLL = 'california_roll'
SALMON_ROLL = 'salmon_roll'
SHRIMP_SUSHI = 'shrimp_sushi'
UNAGI_ROLL = 'unagi_roll'
DRAGON_ROLL = 'dragon_roll'
COMBO = 'combo'
#ALL_ORDER_TYPES = (ONIGIRI, GUNKAN_MAKI, CALIFORNIA_ROLL, SALMON_ROLL, SHRIMP_SUSHI, UNAGI_ROLL, DRAGON_ROLL, COMBO)
ALL_ORDER_TYPES = (ONIGIRI, GUNKAN_MAKI, CALIFORNIA_ROLL)

# Ingredient constants (don't change these: the image filenames depend on these specific values)
SHRIMP = 'shrimp'
RICE = 'rice'
NORI = 'nori'
ROE = 'roe'
SALMON = 'salmon'
UNAGI = 'unagi'
RECIPE = {ONIGIRI:         {RICE: 2, NORI: 1},
          CALIFORNIA_ROLL: {RICE: 1, NORI: 1, ROE: 1},
          GUNKAN_MAKI:     {RICE: 1, NORI: 1, ROE: 2},
          SALMON_ROLL:     {RICE: 1, NORI: 1, SALMON: 2},
          SHRIMP_SUSHI:    {RICE: 1, NORI: 1, SHRIMP: 2},
          UNAGI_ROLL:      {RICE: 1, NORI: 1, UNAGI: 2},
          DRAGON_ROLL:     {RICE: 2, NORI: 1, ROE: 1, UNAGI: 2},
          COMBO:           {RICE: 2, NORI: 1, ROE: 1, SALMON: 1, UNAGI: 1, SHRIMP: 1},}


INVENTORY = {SHRIMP: 5, RICE: 10,
             NORI: 10,  ROE: 10,
             SALMON: 5, UNAGI: 5}


GAME_LINK = "https://www.crazygames.com/game/sushi-go-round"

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)


def handle_cookie_consent(page):
    """Sourcepoint CMP consent banners render inside an iframe. May not always appear."""
    consent_iframe = page.locator("iframe[id^='sp_message_iframe']")

    try:
        consent_iframe.wait_for(state="attached", timeout=5000)
    except Exception:
        print("No cookie consent banner detected, skipping.")
        return

    try:
        frame = page.frame_locator("iframe[id^='sp_message_iframe']")
        frame.get_by_role("button", name="Agree & Continue").click(timeout=8000)
        print("Cookie consent accepted.")
    except Exception:
        print("Consent iframe found, but button click failed.")


def click_play_button(page):
    game_frame_element = page.query_selector("iframe[src*='games.crazygames.com']")
    frame = game_frame_element.content_frame()
    play_button = frame.get_by_role("button", name="Play Now")

    box = play_button.bounding_box()
    if box:
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2
        page.mouse.move(x, y)
        page.wait_for_timeout(200)
        page.mouse.click(x, y)
        print("Play button clicked via raw coordinates.")
    else:
        print("Could not get bounding box for Play button.")


def navigate_game_menu():
    pos = None
    # click on Play
    logging.info('Looking for Play button...')
    while True: # loop because it could be the blue or pink Play button displayed at the moment.
        try:
            pos = pyautogui.locateOnScreen(imPath('play_button.png'))
        except pyautogui.ImageNotFoundException:
            pos = None
        if pos is not None:
            break
        pyautogui.sleep(1)
    pyautogui.click(pos, duration=0.25)
    logging.info('Clicked on Play button.')

    # click on Continue
    while True:
        try:
            pos = pyautogui.locateOnScreen(imPath('continue_button.png'))
        except pyautogui.ImageNotFoundException:
            pos = None
            break
        pyautogui.sleep(1)
    pyautogui.click(pos, duration=0.25)
    logging.info('Clicked on Continue button.')

    # click on Skip
    logging.info('Looking for Skip button...')
    while True: # loop because it could be the yellow or red Skip button displayed at the moment.
        try:
            pos = pyautogui.locateOnScreen(imPath('skip_button.png'))
        except pyautogui.ImageNotFoundException:
            pos = None
        if pos is not None:
            break
        pyautogui.sleep(1)
    pyautogui.click(pos, duration=0.25)
    logging.info('Clicked on Skip button.')

    # click on Continue
    while True:
        try:
            pos = pyautogui.locateOnScreen(imPath('continue_button3.png'))
        except pyautogui.ImageNotFoundException:
            logging.info('Looking for continue_button.png image')
            pos = None
        if pos is not None:
            break
        pyautogui.sleep(1)
    pyautogui.click(pos, duration=0.25)
    logging.info('Clicked on Continue button.')


# Create an amont dictionary
HOW_MANY = {ONIGIRI: 0, GUNKAN_MAKI: 0, CALIFORNIA_ROLL: 0, SALMON_ROLL: 0, SHRIMP_SUSHI: 0, UNAGI_ROLL: 0, DRAGON_ROLL: 0, COMBO: 0}
def get_orders():
    # Get all PNGs, and append values to dictionary
    for order in ALL_ORDER_TYPES:
        try:
            HOW_MANY[order] = len(list(pyautogui.locateAllOnScreen(imPath(order + '_order.png'))))
        except (pyautogui.ImageNotFoundException, pyscreeze.ImageNotFoundException):
            HOW_MANY[order] = 0


    for order in ALL_ORDER_TYPES:
        print(f'{order}:{HOW_MANY[order]}')


def prepare_orders():
    for order in HOW_MANY:
        if HOW_MANY[order] > 0:
            logging.info(f'Trying to prepare ***{order}***')
            for ingredient in RECIPE[order]:
                if INVENTORY[ingredient] < 2:
                    print("O MOJ BOZE!")
                    logging.info(f"Ordering {ingredient}...")
                    pyautogui.click(imPath('phone.png'))
                    if ingredient == RICE:
                        pyautogui.click(imPath("rice_order_menu.png"))
                        pyautogui.click(imPath("rice_order_button.png"))
                    else:
                        pyautogui.click(imPath("topping_order_menu.png"))
                        pyautogui.click(imPath(ingredient + "_order_button.png"))
                    pyautogui.click(imPath( "normal_delivery_button.png"))
                    pyautogui.sleep(10)
                    if ingredient == RICE or ingredient == ROE or ingredient == NORI:
                        INVENTORY[ingredient] += 10
                    else:
                        INVENTORY[ingredient] += 5

                n = RECIPE[order][ingredient]
                logging.info(f"{ingredient}s needed {n}")
                while n > 0:
                    logging.info(f'Clicking on {ingredient}')
                    pyautogui.click(imPath(ingredient + '.png'))
                    n = n - 1
                    INVENTORY[ingredient] -= 1
                    logging.info(f'ingredient {INVENTORY[ingredient]} left')
                    #logging.info(f"n is equal to {n}")
            logging.info(f'Rolling {order}')
            #pyautogui.sleep(10)
            while True:
                try:
                    pyautogui.click(imPath("clear_mat.png"))
                    pyautogui.sleep(1)
                    break;
                except (pyautogui.ImageNotFoundException):
                    print("AJJAJA")
                    pyautogui.sleep(1)


import time

NOT_FOUND = (pyscreeze.ImageNotFoundException, pyautogui.ImageNotFoundException)

def clear_place():

    #locate top right corner, then click from right to left.
    region = pyautogui.locateOnScreen(imPath("close.png"))
    
#    pyautogui.sleep(1999)
    topRightX = region[0] + region[2]
    topRightY = region[1]
    logging.info(f"Top right pixel is {topRightX}:{topRightY}")
    pyautogui.click(imPath("close.png"))
    logging.info(f"region[2] is {region[2]}, region[3] is {region[3]}")
    pyautogui.move(region[2]/2, - region[3]/2)
    pyautogui.move(-562, 0)
    pyautogui.move(81, 182)
    pyautogui.click()
    pyautogui.move(71, 0)
    pyautogui.click()
    pyautogui.move(95, 0)
    pyautogui.click()
    pyautogui.move(90, 0)
    pyautogui.click()
    pyautogui.move(87, 0)
    pyautogui.click()
    pyautogui.move(82, 0)
    pyautogui.click()


    


# 81:184, 158:182, 247:182, 337:182, 424:182, 506:182


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(GAME_LINK)
    
        handle_cookie_consent(page)
        click_play_button(page)
        navigate_game_menu()
        #start_serving()

        while True:
            get_orders()
            prepare_orders()
            clear_place()
            



if __name__ == "__main__":
    main()

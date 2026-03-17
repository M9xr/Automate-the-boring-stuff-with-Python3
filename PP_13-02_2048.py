# The game 2048 is a simple game in which you combine tiles by sliding them up, down, left, or right with the arrow keys.
# You can actually get a fairly high score by sliding tiles in random directions. Write a program that will open the game
# at https://play2048.co and keep sending up, right, down, and left keystrokes to automatically play the game.

from playwright.sync_api import sync_playwright
import random, time
with sync_playwright() as playwright:
    browser = playwright.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto('https://play2048.co')

# close cookie popup
    try:
        btn = page.get_by_role("button", name="Reject all")
        btn.wait_for(timeout=10000)
        btn.click()
        print("Cookies popup closed")
    except Exception as e:
        print(f"Cookies popup NOT closed: {e}")


    pattern = [
        "ArrowDown",
        "ArrowRight",
        "ArrowDown",
        "ArrowRight",
        "ArrowDown",
        "ArrowRight",
        "ArrowDown",
        "ArrowRight",
        "ArrowDown",
        "ArrowRight",
        "ArrowDown",
        "ArrowRight",
        "ArrowLeft"
    ]

    i = 0
    while True:
        if i % 750 == 0: # Tiles in the game sometime blocks themselves, so only legal move is up. (It takes some time, so user also can himself press ArrowUp key)
            page.keyboard.press("ArrowUp")
        page.keyboard.press(pattern[i % len(pattern)])
        i += 1
        time.sleep(0.035)


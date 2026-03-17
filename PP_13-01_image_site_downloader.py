# Write a program that goes to a photo-sharing site like Flickr or Imgur, searches for category of photo, and then
# downloads all the resulting images. You could write a program that works with any photo site that has a search feature.

# My choice is pixabay.com
from playwright.sync_api import sync_playwright
import requests, bs4, sys, os, time

# Check if the user provided a value 
if len(sys.argv) != 2:
    print(f"{sys.argv[0]}: download all resulting images from pixabay.com\nUsage: {sys.argv[0]} USER_INPUT_FOR_SEARCHING\n")
    sys.exit(1)

search_term = sys.argv[1]

playwright = sync_playwright().start()
browser = playwright.firefox.launch(headless=False)
page = browser.new_page()
page.goto('https://pixabay.com')
page.get_by_placeholder("Search for free Images, Videos, Music & more").fill(sys.argv[1])
page.keyboard.press("Enter")
page.wait_for_load_state("networkidle")

# Scroll to load more images
for _ in range(5):
    page.mouse.wheel(0, 5000)
    page.wait_for_timeout(1500)

web_url = page.url


html = page.content()
soup = bs4.BeautifulSoup(html, "html.parser")

# Select images
img_elems = soup.select("a[href^='/photos/'] img")
if len(img_elems) < 1:
    print('No images found\n')
    sys.exit(1)


# Make a new dir for downloaded contnet
folder_name = f'downloaded_{search_term}'
os.makedirs(folder_name, exist_ok=True) # Folder for the new content

MAX_DOWNLOADS = 30  # Max photos we want to download
downloads = 0 # how many already downloaded



for img in img_elems:
    if downloads >= MAX_DOWNLOADS:
        break

    srcset = img.get("srcset")
    if srcset:
        # get all available versions, then chose one with the highest resolution
        img_url = srcset.split(",")[-1].split()[0]
    else:
        img_url = img.get("src") or img.get("data-lazy")
   

    if not img_url or not img_url.startswith("http"):
        continue

    print(f"Downloading {img_url}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(img_url, headers=headers)
        res.raise_for_status()

        filename = os.path.join(folder_name, f"{search_term}{downloads}.jpg" )

        with open(filename, "wb") as f:
            for chunk in res.iter_content(100000):
                f.write(chunk)
        downloads += 1
        time.sleep(0.2)
    except Exception as e:
        print(f"Failed: {e}")

browser.close()
playwright.stop()



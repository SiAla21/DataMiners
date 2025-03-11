from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os
import time

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Initialize WebDriver (use your WebDriver setup from earlier)
driver = webdriver.Chrome(options=chrome_options)

# Create folders for images
if not os.path.exists("pinterest_images"):
    os.makedirs("pinterest_images")

# Pinterest URL (update if needed)
url = "https://www.pinterest.com/ideas/football-tournament-poster-design/934995818443/"

# Function to download image
def download_image(url, image_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = f"pinterest_images/{image_name}.jpg"
            with open(image_path, "wb") as file:
                file.write(response.content)
            print(f"Image saved: {image_path}")
        else:
            print(f"Failed to download image {url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Scrape all images from Pinterest link
def scrape_pinterest_images():
    driver.get(url)
    time.sleep(3)  # Give the page time to load

    # Find all image elements
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Download images
    for i, img in enumerate(images):
        image_url = img.get_attribute("src")
        if image_url:
            download_image(image_url, f"image_{i+1}")

# Start scraping
scrape_pinterest_images()

# Close the browser after scraping
driver.quit()

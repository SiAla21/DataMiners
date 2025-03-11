import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Define the Pinterest URL
url = "https://www.pinterest.com/search/pins/?q=soccer%20merchandise%20ideas%20images&rs=typed"

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Pinterest page
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time if necessary

# Scroll to load all images
scroll_pause_time = 2  # Pause between scrolls
screen_height = driver.execute_script("return window.screen.height;")  # Get screen height
i = 1

while True:
    # Scroll down by one screen height
    driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
    i += 1
    time.sleep(scroll_pause_time)
    
    # Check if we've reached the bottom of the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if screen_height * i > new_height:
        break

# Create a directory to save the images (if it doesn't exist)
if not os.path.exists('marchandise_images'):
    os.makedirs('marchandise_images')

# Find all image elements
images = driver.find_elements(By.TAG_NAME, 'img')

# Download and save all images
for index, img in enumerate(images):
    try:
        # Get the image URL
        image_url = img.get_attribute('src')
        if image_url and image_url.startswith('http'):
            # Extract the image filename from the URL
            image_name = f"image_{index + 153}.jpg"
            image_path = os.path.join('marchandise_images', image_name)
            
            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_response.content)
                print(f"Downloaded: {image_name}")
            else:
                print(f"Failed to download image: {image_url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Close the WebDriver
driver.quit()

print("Scraping completed. Images saved to pinterest_images directory.")
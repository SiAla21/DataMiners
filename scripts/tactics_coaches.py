import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Function to get the next available image number
def get_next_image_number(directory):
    # List all files in the directory
    files = os.listdir(directory)
    # Filter out only image files (assuming they are named image_XX.jpg)
    image_files = [f for f in files if f.startswith('image_') and f.endswith('.jpg')]
    # Extract the numbers from the filenames
    numbers = [int(f.split('_')[1].split('.')[0]) for f in image_files]
    # Find the highest number
    if numbers:
        return max(numbers) + 1
    else:
        return 1  # If no images exist, start from 1

# Function to scrape images from a single URL
def scrape_images(url, directory, start_index):
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

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Find all image elements
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Download and save all images
    for img in images:
        try:
            # Get the image URL
            image_url = img.get_attribute('src')
            if image_url and image_url.startswith('http'):
                # Generate the image name
                image_name = f"image_{start_index}.jpg"
                image_path = os.path.join(directory, image_name)
                
                # Download the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                    print(f"Downloaded: {image_name}")
                    start_index += 1  # Increment the index for the next image
                else:
                    print(f"Failed to download image: {image_url}")
        except Exception as e:
            print(f"Error downloading image: {e}")

    # Close the WebDriver
    driver.quit()
    return start_index  # Return the updated index for the next URL

# Directory to save images
directory = "tactics_images"

# Get the next available image number
start_index = get_next_image_number(directory)

# List of URLs to scrape
urls = [
    "https://www.pinterest.com/pin/836965912035696440/",
    "https://www.pinterest.com/pin/735564551675540657/",
"https://www.pinterest.com/pin/993395630280673387/",
"https://www.pinterest.com/pin/702561610634364843/",
"https://www.pinterest.com/pin/293085888269310819/",
"https://www.pinterest.com/pin/12666442695984845/",
"https://www.pinterest.com/pin/1091700765917843010/",
"https://www.pinterest.com/pin/1028228158671025176/",
"https://www.pinterest.com/pin/600667669085471479/",
"https://www.pinterest.com/pin/157977899426143524/",
"https://www.pinterest.com/pin/621707923538161497/"
    # Add up to 10 URLs here
]

# Loop through each URL and scrape images
for i, url in enumerate(urls):
    print(f"Processing URL {i + 1}: {url}")
    start_index = scrape_images(url, directory, start_index)
    print(f"Scraping completed for URL {i + 1}. Images saved to {directory} directory.")

print("All scraping completed.")
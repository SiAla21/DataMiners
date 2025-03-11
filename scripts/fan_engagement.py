import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define the URL of the Reddit football page
url = "https://www.reddit.com/r/football/"

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Reddit page
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time if necessary

# Create a directory to save the images (if it doesn't exist)
if not os.path.exists('reddit_images'):
    os.makedirs('reddit_images')

# Initialize lists to store article details
image_urls = []
descriptions = []
source_links = []
image_paths = []

# Find all post elements
posts = driver.find_elements(By.CSS_SELECTOR, 'div.col-start-1.col-end-2.row-start-2.row-end-3')
for post in posts:
    try:
        # Get the description (title of the post)
        title_tag = post.find_element(By.CSS_SELECTOR, 'a.block.font-semibold')
        description = title_tag.text.strip() if title_tag else 'No description'
        descriptions.append(description)
        
        # Get the source link
        source_tag = post.find_element(By.CSS_SELECTOR, 'a.post-link')
        source_link = source_tag.get_attribute('href') if source_tag else 'No source link'
        source_links.append(source_link)
        
        # Get the image URL (if available)
        image_tag = post.find_element(By.CSS_SELECTOR, 'img') if post.find_elements(By.CSS_SELECTOR, 'img') else None
        image_url = image_tag.get_attribute('src') if image_tag else 'No image URL'
        image_urls.append(image_url)
        
        # Download and save the image (if image URL is available)
        if image_url != 'No image URL':
            try:
                # Extract the image filename from the URL
                image_name = os.path.basename(image_url)
                image_path = os.path.join('reddit_images', image_name)
                
                # Download the image
                image_response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"})
                if image_response.status_code == 200:
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                    image_paths.append(image_path)
                else:
                    print(f"Failed to download image: {image_url}")
                    image_paths.append('Failed to download')
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")
                image_paths.append('Error downloading')
        else:
            image_paths.append('No image path')
    except Exception as e:
        print(f"Error processing a post: {e}")

# Close the WebDriver
driver.quit()

# Create a DataFrame to store the details
data = pd.DataFrame({
    'Image URL': image_urls,
    'Description': descriptions,
    'Source Link': source_links,
    'Image Path': image_paths
})

# Save the DataFrame to a CSV file
data.to_csv('reddit_articles.csv', index=False)

print("Scraping completed. Data saved to reddit_articles.csv")
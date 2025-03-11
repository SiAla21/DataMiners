import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the URL of the SponsorUnited news page
url = "https://www.sponsorunited.com/news"

# Define headers to simulate a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the HTML content of the page
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Create a directory to save the images (if it doesn't exist)
if not os.path.exists('sponsorunited_images'):
    os.makedirs('sponsorunited_images')

# Initialize lists to store article details
image_urls = []
descriptions = []
source_links = []
image_paths = []

# Find all article elements
for article in soup.find_all('div', class_='blog5_item'):
    # Get the image URL
    image_tag = article.find('img', class_='img-abs')
    if image_tag and image_tag.get('src'):
        image_url = image_tag['src']
    else:
        image_url = 'No image URL'
    image_urls.append(image_url)
    
    # Get the description (title of the article)
    title_tag = article.find('h3', class_='heading-style-h5')
    description = title_tag.get_text(strip=True) if title_tag else 'No description'
    descriptions.append(description)
    
    # Get the source link
    link_tag = article.find('a', class_='blog5_title-link')
    if link_tag and link_tag.get('href'):
        source_link = link_tag['href']
    else:
        source_link = 'No source link'
    source_links.append(source_link)
    
    # Download and save the image (if image URL is available)
    if image_url != 'No image URL':
        try:
            # Extract the image filename from the URL
            image_name = os.path.basename(image_url)
            image_path = os.path.join('sponsorunited_images', image_name)
            
            # Download the image
            image_response = requests.get(image_url, headers=headers)
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
    
    # Add a delay to avoid being blocked
    time.sleep(1)  # 1-second delay between requests

# Create a DataFrame to store the details
data = pd.DataFrame({
    'Image URL': image_urls,
    'Description': descriptions,
    'Source Link': source_links,
    'Image Path': image_paths
})

# Save the DataFrame to a CSV file
data.to_csv('sponsorunited_articles.csv', index=False)

print("Scraping completed. Data saved to sponsorunited_articles.csv")
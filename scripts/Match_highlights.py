import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the BBC Sport Football page
url = "https://www.bbc.com/sport/football"

# Fetch the HTML content of the page
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Create a directory to save the images
if not os.path.exists('match_highlights'):
    os.makedirs('match_highlights')

# Initialize lists to store image details
image_urls = []
descriptions = []
source_links = []
image_paths = []

# Find all image elements
for img in soup.find_all('img'):
    # Get the image URL
    img_url = img.get('src')
    if img_url and 'http' in img_url:
        image_urls.append(img_url)
        
        # Get the closest description or caption
        description = img.find_previous(['h2', 'p'])
        descriptions.append(description.get_text() if description else 'No description')
        
        # Get the source or credit for the image
        source = img.find_parent('a')
        source_links.append(source.get('href') if source else 'No source link')
        
        # Download and save the image
        img_data = requests.get(img_url).content
        img_name = os.path.basename(img_url)
        img_path = os.path.join('match_highlights', img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        image_paths.append(img_path)

# Create a DataFrame to store the details
df = pd.DataFrame({
    'Image URL': image_urls,
    'Description': descriptions,
    'Source Link': source_links,
    'Image Path': image_paths
})

# Save the DataFrame to a CSV file
df.to_csv('match_highlights.csv', index=False)

print("Scraping completed. Data saved to match_highlights.csv")
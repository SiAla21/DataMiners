import os
import requests
from bs4 import BeautifulSoup
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL for available coaches
BASE_URL = "https://www.transfermarkt.com/trainer/verfuegbaretrainer/statistik"

# Headers to mimic a real browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Create a directory to save images
IMAGE_DIR = 'managers_images'
os.makedirs(IMAGE_DIR, exist_ok=True)

# CSV file to store metadata
METADATA_FILE = 'managers_photos_metadata.csv'

# Use a session to maintain headers and cookies
session = requests.Session()
session.headers.update(HEADERS)


def scrape_page(url):
    """Fetch and parse a single page"""
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

    return BeautifulSoup(response.content, 'html.parser')


def download_image(img_url, coach_name):
    """Download and save an image, returning its local file path"""
    if not img_url.startswith("http"):
        img_url = "https:" + img_url  # Fix relative URLs

    img_filename = f"{coach_name.replace(' ', '_')}.jpg"
    img_path = os.path.join(IMAGE_DIR, img_filename)

    try:
        img_data = session.get(img_url).content
        with open(img_path, 'wb') as handler:
            handler.write(img_data)
        logging.info(f"Saved image for {coach_name} at {img_path}")
        return img_path
    except Exception as e:
        logging.error(f"Error downloading image {img_url}: {e}")
        return "no_image.jpg"  # Placeholder if download fails


def extract_row_data(row):
    """Extracts details from a single row"""
    try:
        img_tag = row.find('img', class_='bilderrahmen-fixed')
        if not img_tag:
            return None

        img_url = img_tag.get('src', '').strip()
        coach_name = img_tag.get('title', '').strip()
        if not coach_name:
            return None

        # Download the image and get its path
        img_path = download_image(img_url, coach_name)

        # Extract nationality and other details
        nationality_tag = row.find('img', class_='flaggenrahmen')
        nationality = nationality_tag.get('title', 'Unknown') if nationality_tag else 'Unknown'

        cells = row.find_all('td', class_='zentriert')
        if len(cells) < 5:
            return None  # Not enough data

        age = cells[0].text.strip()
        matches = cells[1].text.strip()
        wins = cells[2].text.strip()
        draws = cells[3].text.strip()
        losses = cells[4].text.strip()

        return [coach_name, nationality, age, matches, wins, draws, losses, img_path]
    except Exception as e:
        logging.error(f"Error processing row: {e}")
        return None


def main():
    """Main function to scrape multiple pages"""
    with open(METADATA_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Nationality', 'Age', 'Matches', 'Wins', 'Draws', 'Losses', 'Image Path'])  # CSV Header

        page_number = 1
        while True:
            page_url = f"{BASE_URL}?page={page_number}"
            logging.info(f"Scraping page {page_number}: {page_url}")

            soup = scrape_page(page_url)
            if not soup:
                break

            rows = soup.find_all('tr', class_=['odd', 'even'])
            if not rows:
                logging.info("No more rows found. Ending scrape.")
                break  # Stop when no more rows exist

            for row in rows:
                row_data = extract_row_data(row)
                if row_data:
                    writer.writerow(row_data)

            page_number += 1  # Move to next page

    logging.info(f"Scraping completed! Data saved in '{METADATA_FILE}'")
    logging.info(f"All images have been saved in '{IMAGE_DIR}'")


# Run the scraper
if __name__ == "__main__":
    main()

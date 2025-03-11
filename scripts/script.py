import requests
from bs4 import BeautifulSoup
import csv
import time

# URL of the page you want to scrape
URL = "https://www.med.tn/medecin/kinesitherapeute"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Function to extract doctor information from a page
def scrape_page(url):
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    doctors = soup.find_all("div", class_="card-doctor-block")

    data = []
    for doctor in doctors:
        try:
            name = doctor.find("div", class_="list__label--name").text.strip()
            specialty = doctor.find("div", class_="list__label--spee").text.strip()
            location = doctor.find("div", class_="list__label--adr").text.strip()

            # Extract services offered
            services = [tag.text.strip() for tag in doctor.select(".widget_tag_cloud .tagcloud")]

            # Extract profile link
            profile_link = doctor.find("a")["href"]
            full_profile_link = f"https://www.med.tn{profile_link}"

            # Store in a list
            data.append([name, specialty, location, ", ".join(services), full_profile_link])

        except AttributeError:
            continue  # Skip if any information is missing

    return data

# Function to scrape multiple pages
def scrape_multiple_pages(base_url, num_pages=5):
    all_data = []
    
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")
        page_url = f"{base_url}?page={page}"
        all_data.extend(scrape_page(page_url))
        time.sleep(2)  # Sleep to avoid being blocked

    return all_data

# Scrape first 5 pages (adjust as needed)
scraped_data = scrape_multiple_pages(URL, num_pages=5)

# Save data to a CSV file
csv_filename = "doctors.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Specialty", "Location", "Services", "Profile Link"])
    writer.writerows(scraped_data)

print(f"✅ Data saved to {csv_filename}")

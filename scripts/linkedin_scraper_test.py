from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Configure Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
chrome_driver_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"


# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL of the page you want to scrape
BASE_URL = "https://www.med.tn/medecin/kinesitherapeute"

# Function to extract doctor information from a page
def scrape_page(url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

    # Wait for the doctor cards to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-doctor-block"))
    )

    doctors = driver.find_elements(By.CLASS_NAME, "card-doctor-block")
    data = []

    for doctor in doctors:
        try:
            # Extract the name of the doctor
            name = doctor.find_element(By.CLASS_NAME, "list__label--name").text.strip()

            # Extract the specialty
            specialty = doctor.find_element(By.CLASS_NAME, "list__label--spee").text.strip()

            # Extract the location
            location = doctor.find_element(By.CLASS_NAME, "list__label--adr").text.strip()

            # Extract services offered
            services = [tag.text.strip() for tag in doctor.find_elements(By.CSS_SELECTOR, ".widget_tag_cloud .tagcloud")]

            # Extract profile link
            profile_link = doctor.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Store in a list
            data.append([name, specialty, location, ", ".join(services), profile_link])

        except Exception as e:
            print(f"Error processing a doctor: {e}")
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
scraped_data = scrape_multiple_pages(BASE_URL, num_pages=5)

# Save data to a CSV file
csv_filename = "kinesitherapeute.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Specialty", "Location", "Services", "Profile Link"])
    writer.writerows(scraped_data)

print(f"✅ Data saved to {csv_filename}")

# Close the WebDriver
driver.quit()
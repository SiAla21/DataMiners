from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL to scrape
URL = "https://www.med.tn/medecin/kinesitherapeute"
driver.get(URL)

# Wait for JavaScript to load
time.sleep(5)  # Adjust if needed

# Extract doctor cards
doctor_cards = driver.find_elements(By.CLASS_NAME, "card-doctor-block")

data = []
for card in doctor_cards:
    try:
        name = card.find_element(By.CLASS_NAME, "list__label--name").text.strip()
        specialty = card.find_element(By.CLASS_NAME, "list__label--spee").text.strip()
        location = card.find_element(By.CLASS_NAME, "list__label--adr").text.strip()
        
        # Extract profile link
        profile_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        data.append([name, specialty, location, profile_link])

    except Exception as e:
        print(f"Error extracting doctor: {e}")

# Save data to CSV
csv_filename = "kinesitherapeutes.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Specialty", "Location", "Profile Link"])
    writer.writerows(data)

print(f"✅ Data successfully scraped and saved to {csv_filename}")

# Close browser
driver.quit()

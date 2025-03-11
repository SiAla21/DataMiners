import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page to scrape
url = "https://www.med.tn/medecin/medecin-du-sport/"

# Create directories for images and metadata
image_dir = "doctor_images"
os.makedirs(image_dir, exist_ok=True)
metadata_file = "doctor_metadata.csv"

# Open the CSV file to save metadata
with open(metadata_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Name", "Specialization", "Address", "Bio", "Tags", "Image Path"])

    # Navigate to the page
    driver.get(url)

    # Wait for the page to load (adjust sleep time if necessary)
    driver.implicitly_wait(10)

    # Find all doctor cards
    doctor_cards = driver.find_elements(By.CLASS_NAME, "card-doctor-block")

    for card in doctor_cards:
        try:
            # Extract doctor name
            name = card.find_element(By.CLASS_NAME, "list__label--name").text.strip()

            # Extract specialization
            specialization = card.find_element(By.CLASS_NAME, "list__label--spee").text.strip()

            # Extract address
            address = card.find_element(By.CLASS_NAME, "list__label--adr").text.strip()

            # Extract bio
            bio = card.find_element(By.CLASS_NAME, "list__bio").text.strip()

            # Extract tags
            tags = ", ".join(
                [tag.text.strip() for tag in card.find_elements(By.CLASS_NAME, "tagcloud")]
            )

            # Extract image URL
            img_tag = card.find_element(By.TAG_NAME, "img")
            img_url = img_tag.get_attribute("src")

            # Download and save the image
            img_name = f"{name.replace(' ', '_')}.jpg"
            img_path = os.path.join(image_dir, img_name)
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as handler:
                handler.write(img_data)

            # Save metadata to CSV
            writer.writerow([name, specialization, address, bio, tags, img_path])

            print(f"✅ Saved data for {name}")

        except Exception as e:
            print(f"❌ Error processing a doctor card: {e}")

# Close the WebDriver
driver.quit()

print(f"✅ All images have been saved in the directory: {image_dir}")
print(f"✅ Metadata has been saved to: {metadata_file}")
import os
import csv
import requests
from bs4 import BeautifulSoup

# Base URL for Transfermarkt search results
base_url = "https://www.transfermarkt.com/detailsuche/spielerdetail/suche/53662063"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Directory to save images
image_dir = "players_images_caf"
os.makedirs(image_dir, exist_ok=True)  # Create directory if not exists

# CSV file to store metadata
csv_filename = "players_caf_data.csv"

# Number of pages (Transfermarkt pagination suggests there are 10 pages)
total_pages = 10

# Open CSV file to write player data
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Position", "Date of Birth (Age)", "Nationality", "Club", "Market Value (€)", "Image Filename", "Profile Link"])

    for page in range(1, total_pages + 1):
        page_url = f"{base_url}/page/{page}" if page > 1 else base_url
        print(f"📄 Scraping page {page} of {total_pages}...")

        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all rows containing player data
            players = soup.find_all("tr", class_=["odd", "even"])

            for player in players:
                # Extract player name
                name_tag = player.find("td", class_="hauptlink").find("a")
                name = name_tag.text.strip() if name_tag else "Unknown"

                # Extract player profile link
                profile_link = "https://www.transfermarkt.com" + name_tag["href"] if name_tag else "No link"

                # Extract player position
                position_tag = player.find_all("td")[1].find_all("td")[-1]
                position = position_tag.text.strip() if position_tag else "Unknown"

                # Extract player birthdate (age)
                age_tag = player.find_all("td")[2]
                birth_date_age = age_tag.text.strip() if age_tag else "Unknown"

                # Extract nationality
                nationality_tag = player.find_all("td")[3].find("img")
                nationality = nationality_tag["title"] if nationality_tag else "Unknown"

                # Extract club
                club_tag = player.find_all("td")[4].find("a")
                club = club_tag["title"] if club_tag else "Unknown"

                # Extract market value
                market_value_tag = player.find_all("td")[-1]
                market_value = market_value_tag.text.strip() if market_value_tag else "Unknown"

                # Extract player image URL
                img_tag = player.find("img", class_="bilderrahmen-fixed")
                img_url = img_tag["src"] if img_tag else None

                if img_url:
                    # Define image file name
                    img_filename = f"{name.replace(' ', '_')}.jpg"
                    img_path = os.path.join(image_dir, img_filename)

                    # Download and save image
                    img_response = requests.get(img_url, headers=headers)
                    if img_response.status_code == 200:
                        with open(img_path, "wb") as img_file:
                            img_file.write(img_response.content)

                else:
                    img_filename = "No image available"

                # Write player data to CSV
                writer.writerow([name, position, birth_date_age, nationality, club, market_value, img_filename, profile_link])

        else:
            print(f"❌ Failed to retrieve page {page}")

print(f"✅ Scraping complete! Images saved in '{image_dir}', CSV saved as '{csv_filename}'.")

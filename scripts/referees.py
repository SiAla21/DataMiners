import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the UEFA Champions League referees, we'll append page numbers later
BASE_URL = "https://www.transfermarkt.com/uefa-champions-league/schiedsrichter/pokalwettbewerb/CL?page="

# Set headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to scrape the referees from a specific page
def scrape_referees():
    referee_list = []
    page_number = 1  # Start from page 1
    max_pages = 13   # Max number of pages to scrape

    while page_number <= max_pages:
        print(f"Scraping page {page_number}...")
        # Construct the URL for the current page
        url = BASE_URL + str(page_number)
        
        # Send request to the website
        response = requests.get(url, headers=HEADERS)
        
        # If the response status is not OK, break the loop
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Exiting.")
            break
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find all rows with referee data (they should be either "odd" or "even")
        referees = soup.find_all("tr", class_=["odd", "even"])

        # If no referees are found, break the loop (indicating no more pages)
        if not referees:
            print("No more referees found. Exiting.")
            break

        for referee in referees:
            try:
                # Find the referee's name and profile URL
                name_tag = referee.find("td", class_="hauptlink").find("a")
                if not name_tag:
                    continue  # Skip if no name is found

                name = name_tag.text.strip()
                profile_url = "https://www.transfermarkt.com" + name_tag["href"]

                # Extract other details
                nationality = referee.find_all("td")[2].find("img")["title"] if referee.find_all("td")[2].find("img") else "N/A"
                age = referee.find_all("td")[3].text.strip()
                matches_officiated = referee.find_all("td")[4].text.strip()
                yellow_cards = referee.find_all("td")[5].text.strip()
                second_yellows = referee.find_all("td")[6].text.strip()
                red_cards = referee.find_all("td")[7].text.strip()
                penalties_given = referee.find_all("td")[8].text.strip()

                # Store in dictionary
                referee_data = {
                    "Name": name,
                    "Age": age,
                    "Nationality": nationality,
                    "Matches Officiated": matches_officiated,
                    "Yellow Cards": yellow_cards,
                    "Second Yellow Cards": second_yellows,
                    "Red Cards": red_cards,
                    "Penalties Given": penalties_given,
                    "Profile URL": profile_url
                }
                referee_list.append(referee_data)
            
            except Exception as e:
                print(f"Error scraping a row: {e}")

        # Move to the next page
        page_number += 1

    # Save the data to CSV
    df = pd.DataFrame(referee_list)
    df.to_csv("uefa_champions_league_referees.csv", index=False)
    print("Scraping completed! Data saved in 'uefa_champions_league_referees.csv'")

# Run the function to scrape referees
scrape_referees()

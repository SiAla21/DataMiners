import requests
from bs4 import BeautifulSoup

URL = "https://www.med.tn/medecin/kinesitherapeute"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    html_content = response.text
    print(html_content[:500])  # Print first 500 characters of the page
else:
    print(f"Failed to retrieve page, status code: {response.status_code}")

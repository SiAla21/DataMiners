import os
import requests
import csv
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin

# URL de base
base_url = "https://www.transfermarkt.com/popel/wertvollstespieler/marktwertetop"

# En-têtes pour simuler une requête de navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Créer un dossier pour stocker les images
if not os.path.exists('joueurs_images'):
    os.makedirs('joueurs_images')

# Ouvrir un fichier CSV pour sauvegarder les métadonnées
metadata_file = "joueurs_metadata.csv"
with open(metadata_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Écrire l'en-tête
    writer.writerow(["Nom", "Position", "Nationalité", "Âge", "Club", "Valeur marchande", "Chemin image"])

    # Fonction pour extraire les données d'une page
    def extract_page_data(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver toutes les lignes du tableau des joueurs
        rows = soup.find_all('tr', class_=['odd', 'even'])

        # Parcourir chaque ligne pour extraire les données
        for row in rows:
            try:
                # Extraire l'image du joueur
                img_tag = row.find('img', class_='bilderrahmen-fixed')
                if img_tag:
                    img_url = img_tag['src']
                    player_name = img_tag['title']

                    # Télécharger et sauvegarder l'image
                    img_name = f"{player_name.replace(' ', '_')}.jpg"
                    img_path = os.path.join('joueurs_images', img_name)
                    try:
                        img_data = requests.get(img_url).content
                        with open(img_path, 'wb') as handler:
                            handler.write(img_data)
                        print(f"✅ Image sauvegardée pour {player_name} à {img_path}")
                    except Exception as e:
                        print(f"❌ Échec du téléchargement de l'image pour {player_name}: {e}")
                        img_path = "N/A"  # Si le téléchargement échoue, définir le chemin sur "N/A"

                    # Extraire les autres métadonnées
                    position = row.find('td', class_='hauptlink').text.strip()
                    age = row.find_all('td', class_='zentriert')[1].text.strip()

                    # Extraire les nationalités
                    nationalities = [img['title'] for img in row.find_all('img', class_='flaggenrahmen')]

                    # Extraire le club
                    club_tag = row.find('a', href=lambda x: x and '/startseite/verein/' in x)
                    club = club_tag['title'] if club_tag else "N/A"

                    # Extraire la valeur marchande
                    market_value = row.find('a', href=lambda x: x and '/marktwertverlauf/spieler/' in x).text.strip()

                    # Sauvegarder les métadonnées dans le CSV
                    writer.writerow([player_name, position, ', '.join(nationalities), age, club, market_value, img_path])
                    print(f"✅ Données sauvegardées pour {player_name}")

            except Exception as e:
                print(f"❌ Erreur lors du traitement d'une ligne : {e}")

    # Fonction pour extraire les liens de pagination
    def get_pagination_links(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('ul', class_='tm-pagination')
        if pagination:
            links = pagination.find_all('a', href=True)
            # Récupérer les liens uniques
            unique_links = set()
            for link in links:
                full_url = urljoin(base_url, link['href'])
                unique_links.add(full_url)
            return sorted(unique_links)  # Trier les liens pour un ordre cohérent
        return []

    # Commencer par la première page
    current_url = base_url
    visited_pages = set()

    # Boucler sur toutes les pages
    while current_url:
        if current_url in visited_pages:
            break  # Éviter les boucles infinies
        visited_pages.add(current_url)

        print(f"Extraction de la page : {current_url}")
        extract_page_data(current_url)

        # Récupérer les liens de pagination
        pagination_links = get_pagination_links(current_url)
        if not pagination_links:
            break  # Si aucune pagination n'est trouvée, arrêter

        # Passer à la prochaine page non visitée
        next_url = None
        for link in pagination_links:
            if link not in visited_pages:
                next_url = link
                break

        current_url = next_url

        # Pause pour éviter de surcharger le serveur
        sleep(2)

print(f"✅ Toutes les images ont été sauvegardées dans le répertoire : joueurs_images")
print(f"✅ Les métadonnées ont été sauvegardées dans : {metadata_file}")
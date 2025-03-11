import os
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode headless (sans interface graphique)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialisation du WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de la page à scraper
base_url = "https://www.transfermarkt.com/statistik/vertragslosespieler"

# Créer des répertoires pour les images et les métadonnées
image_dir = "joueurs_images"
os.makedirs(image_dir, exist_ok=True)  # Créer le répertoire s'il n'existe pas
metadata_file = "joueurs_metadata.csv"

# Ouvrir le fichier CSV pour sauvegarder les métadonnées
with open(metadata_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Écrire l'en-tête
    writer.writerow(["Nom", "Position", "Nationalité", "Âge", "Contrat expire", "Valeur marchande", "Chemin image"])

    # Boucler sur toutes les pages
    page = 1
    while True:
        print(f"Extraction de la page {page}...")
        url = f"{base_url}/page/{page}"
        driver.get(url)

        # Attendre que la page se charge
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "items"))
        )

        # Trouver toutes les lignes du tableau des joueurs
        rows = driver.find_elements(By.CSS_SELECTOR, 'tr.odd, tr.even')

        # Si aucune ligne n'est trouvée, arrêter la boucle
        if not rows:
            print("Fin des pages.")
            break

        # Parcourir chaque ligne pour extraire les données
        for row in rows:
            try:
                # Extraire l'image du joueur
                img_tag = row.find_element(By.CSS_SELECTOR, 'img.bilderrahmen-fixed')
                img_url = img_tag.get_attribute('data-src')
                player_name = img_tag.get_attribute('title')

                # Télécharger et sauvegarder l'image
                img_name = f"{player_name.replace(' ', '_')}.jpg"
                img_path = os.path.join(image_dir, img_name)
                try:
                    img_data = requests.get(img_url).content
                    with open(img_path, "wb") as handler:
                        handler.write(img_data)
                    print(f"✅ Image sauvegardée pour {player_name} à {img_path}")
                except Exception as e:
                    print(f"❌ Échec du téléchargement de l'image pour {player_name}: {e}")
                    img_path = "N/A"  # Si le téléchargement échoue, définir le chemin sur "N/A"

                # Extraire les autres métadonnées
                position = row.find_element(By.CSS_SELECTOR, 'td.hauptlink').text.strip()
                nationality = row.find_element(By.CSS_SELECTOR, 'img.flaggenrahmen').get_attribute('title')
                age = row.find_elements(By.CSS_SELECTOR, 'td.zentriert')[1].text.strip()
                contract_expires = row.find_elements(By.CSS_SELECTOR, 'td.zentriert')[2].text.strip()
                market_value = row.find_element(By.CSS_SELECTOR, 'td.hauptlink.rechts').text.strip()

                # Sauvegarder les métadonnées dans le CSV
                writer.writerow([player_name, position, nationality, age, contract_expires, market_value, img_path])
                print(f"✅ Données sauvegardées pour {player_name}")

            except Exception as e:
                print(f"❌ Erreur lors du traitement d'une ligne : {e}")

        # Passer à la page suivante
        page += 1

# Fermer le WebDriver
driver.quit()

print(f"✅ Toutes les images ont été sauvegardées dans le répertoire : {image_dir}")
print(f"✅ Les métadonnées ont été sauvegardées dans : {metadata_file}")
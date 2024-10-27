import requests
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Importation de tqdm pour la barre de progression
import configparser

# Charger les configurations depuis le fichier config.ini
config = configparser.ConfigParser()
config.read('config.ini')

STEAM_API_KEY = config['STEAM']['API_KEY']
STEAM_ID = config['STEAM']['STEAM_ID']

# Fonction pour obtenir la liste de jeux possédés par l'utilisateur
def get_owned_games():
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("response", {}).get("games", [])

# Fonction pour obtenir des détails sur chaque jeu via Steam Store API
def get_game_details(appid):
    url = f"https://store.steampowered.com/api/appdetails/"
    params = {"appids": appid}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data[str(appid)]["success"]:
            return data[str(appid)]["data"]
    except Exception as e:
        print(f"Erreur lors de la récupération des détails pour le jeu {appid}: {e}")
    return {}

# Fonction pour exporter les données des jeux dans un fichier CSV
def export_games_to_csv(games):
    with open("steam_games_info.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Game Name", "App ID", "Developers"])

        # Utilisation de ThreadPoolExecutor pour paralléliser les appels API
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Utilisation de tqdm pour suivre la progression
            with tqdm(total=len(games), desc="Progression", unit="jeu") as pbar:
                futures = {executor.submit(get_game_details, game["appid"]): game for game in games}
                
                for future in as_completed(futures):
                    game = futures[future]
                    appid = game.get("appid")
                    name = game.get("name")
                    
                    try:
                        details = future.result()
                        if details:
                            developers = ", ".join(details.get("developers", []))
                            writer.writerow([name, appid, developers])
                    except Exception as e:
                        print(f"Erreur lors de l'écriture des données pour le jeu {name} (ID: {appid}): {e}")
                    
                    pbar.update(1)  # Met à jour la barre de progression à chaque jeu terminé

# Exécution
games = get_owned_games()
export_games_to_csv(games)
print("Exportation des informations de jeux dans steam_games_info.csv terminée.")
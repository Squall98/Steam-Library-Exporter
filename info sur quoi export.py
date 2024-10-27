import requests
import json

# Choisissez un AppID pour un jeu populaire (ex. : 570 pour Dota 2, 730 pour CS:GO)
appid = 570

url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
response = requests.get(url)
data = response.json()

# Fonction pour formater et afficher les champs de façon structurée
def format_fields(details, indent=0):
    result = ""
    for key, value in details.items():
        # Ajouter une indentation pour la lisibilité
        result += " " * indent + f"{key}: "
        
        if isinstance(value, dict):
            result += "\n" + format_fields(value, indent + 4)
        elif isinstance(value, list):
            result += "[\n"
            for item in value:
                if isinstance(item, dict):
                    result += format_fields(item, indent + 4) + "\n"
                else:
                    result += " " * (indent + 4) + f"{item},\n"
            result += " " * indent + "]\n"
        else:
            result += f"{value}\n"
    return result

# Vérifie si les détails sont disponibles et les formate
if data[str(appid)]["success"]:
    details = data[str(appid)]["data"]
    formatted_details = format_fields(details)

    # Enregistrement dans un fichier pour faciliter la lecture
    with open("steam_game_fields.txt", "w", encoding="utf-8") as file:
        file.write("Champs disponibles pour l'AppID " + str(appid) + ":\n\n")
        file.write(formatted_details)
    
    print("Les champs disponibles ont été enregistrés dans 'steam_game_fields.txt'")
else:
    print(f"Les détails pour le jeu avec l'AppID {appid} n'ont pas été trouvés.")

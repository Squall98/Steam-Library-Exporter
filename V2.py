import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import configparser
import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Chemin du fichier de configuration
CONFIG_FILE = "config.ini"

# Charger ou créer le fichier de configuration
def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        config["STEAM"] = {"API_KEY": "", "STEAM_ID": ""}
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    return config

# Sauvegarder les informations saisies dans le fichier de configuration
def save_config(api_key, steam_id):
    config = configparser.ConfigParser()
    config["STEAM"] = {"API_KEY": api_key, "STEAM_ID": steam_id}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

# Fonction pour obtenir la liste de jeux possédés par l'utilisateur
def get_owned_games(api_key, steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
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
def export_games_to_csv(api_key, steam_id, selected_fields, save_path, progress_bar):
    games = get_owned_games(api_key, steam_id)
    progress_bar["maximum"] = len(games)
    with open(save_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(selected_fields)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(get_game_details, game["appid"]): game for game in games}

            for i, future in enumerate(as_completed(futures), 1):
                game = futures[future]
                appid = game.get("appid")
                name = game.get("name")
                row = []

                try:
                    details = future.result()
                    if details:
                        if "Game Name" in selected_fields:
                            row.append(name)
                        if "App ID" in selected_fields:
                            row.append(appid)
                        if "Developers" in selected_fields:
                            developers = ", ".join(details.get("developers", []))
                            row.append(developers)
                        if "Release Date" in selected_fields:
                            release_date = details.get("release_date", {}).get("date", "N/A")
                            row.append(release_date)
                        if "Publishers" in selected_fields:
                            publishers = ", ".join(details.get("publishers", []))
                            row.append(publishers)
                        if "Genres" in selected_fields:
                            genres = ", ".join([genre["description"] for genre in details.get("genres", [])])
                            row.append(genres)
                        if "Price" in selected_fields:
                            price = details.get("price_overview", {}).get("final", 0) / 100 if details.get("price_overview") else "Free"
                            row.append(price)
                        if "Metacritic Score" in selected_fields:
                            metacritic = details.get("metacritic", {}).get("score", "N/A")
                            row.append(metacritic)

                        writer.writerow(row)
                except Exception as e:
                    print(f"Erreur lors de l'écriture des données pour le jeu {name} (ID: {appid}): {e}")

                # Mise à jour de la barre de progression
                progress_bar["value"] = i
                root.update_idletasks()

# Interface graphique avec tkinter
def run_gui():
    # Charger la configuration existante
    config = load_config()
    api_key = config["STEAM"].get("API_KEY", "")
    steam_id = config["STEAM"].get("STEAM_ID", "")

    def browse_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    def run_export():
        api_key_input = api_entry.get().strip()
        steam_id_input = steamid_entry.get().strip()
        save_path = file_entry.get().strip()
        selected_fields = [field for field, var in fields.items() if var.get()]

        if not api_key_input or not steam_id_input or not save_path or not selected_fields:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs et sélectionner au moins un champ.")
            return

        # Sauvegarder les informations dans le fichier config.ini
        save_config(api_key_input, steam_id_input)

        # Lancer l'exportation avec la barre de progression
        export_games_to_csv(api_key_input, steam_id_input, selected_fields, save_path, progress_bar)
        messagebox.showinfo("Succès", f"Exportation terminée dans {save_path}")

    # Création de la fenêtre principale
    global root
    root = tk.Tk()
    root.title("Exportation de la Bibliothèque Steam")
    root.geometry("400x550")

    # Entrée pour la clé API Steam
    tk.Label(root, text="Steam API Key:").pack(pady=5)
    api_entry = tk.Entry(root, width=50)
    api_entry.insert(0, api_key)
    api_entry.pack()

    # Entrée pour le SteamID
    tk.Label(root, text="Steam ID:").pack(pady=5)
    steamid_entry = tk.Entry(root, width=50)
    steamid_entry.insert(0, steam_id)
    steamid_entry.pack()

    # Sélection du fichier CSV
    tk.Label(root, text="Fichier de sortie (CSV):").pack(pady=5)
    file_frame = tk.Frame(root)
    file_frame.pack()
    file_entry = tk.Entry(file_frame, width=38)
    file_entry.pack(side=tk.LEFT)
    file_button = tk.Button(file_frame, text="Parcourir", command=browse_file)
    file_button.pack(side=tk.RIGHT)

    # Options de champs à exporter
    tk.Label(root, text="Champs à exporter:").pack(pady=5)
    fields = {
        "Game Name": tk.BooleanVar(value=True),
        "App ID": tk.BooleanVar(value=True),
        "Developers": tk.BooleanVar(value=True),
        "Release Date": tk.BooleanVar(value=False),
        "Publishers": tk.BooleanVar(value=False),
        "Genres": tk.BooleanVar(value=False),
        "Price": tk.BooleanVar(value=False),
        "Metacritic Score": tk.BooleanVar(value=False)
    }
    for field, var in fields.items():
        tk.Checkbutton(root, text=field, variable=var).pack(anchor="w")

    # Barre de progression
    tk.Label(root, text="Progression de l'exportation:").pack(pady=5)
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Bouton pour lancer l'exportation
    export_button = tk.Button(root, text="Exporter", command=run_export)
    export_button.pack(pady=20)

    root.mainloop()

# Exécution de l'interface graphique
run_gui()

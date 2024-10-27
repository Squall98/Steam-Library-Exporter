import sys
import configparser
import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QGroupBox,
                             QPushButton, QCheckBox, QFileDialog, QProgressBar, QMessageBox, QScrollArea)

# Chemin du fichier de configuration
CONFIG_FILE = "config.ini"

# Charger ou créer le fichier de configuration
def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section("STEAM"):
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
    response = requests.get(url, params=params)
    data = response.json()
    if data[str(appid)]["success"]:
        return data[str(appid)]["data"]
    return {}

# Classe de la fenêtre principale de l'application PyQt5
class SteamAppExporter(QWidget):
    def __init__(self):
        super().__init__()

        # Charger la configuration existante
        config = load_config()
        self.api_key = config["STEAM"].get("API_KEY", "")
        self.steam_id = config["STEAM"].get("STEAM_ID", "")

        # Configurer l'interface
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Champs pour la clé API et Steam ID
        layout.addWidget(QLabel("Steam API Key:"))
        self.api_entry = QLineEdit(self.api_key)
        layout.addWidget(self.api_entry)

        layout.addWidget(QLabel("Steam ID:"))
        self.steamid_entry = QLineEdit(self.steam_id)
        layout.addWidget(self.steamid_entry)

        # Sélection du fichier CSV
        self.file_button = QPushButton("Sélectionner un fichier CSV de sortie")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Label pour afficher le chemin du fichier sélectionné
        self.file_path_label = QLabel("")
        layout.addWidget(self.file_path_label)

        # GroupBox pour les options de champs à exporter
        self.fields = self.create_fields_group()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.fields)
        layout.addWidget(scroll_area)

        # Barre de progression
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Bouton d'exportation
        self.export_button = QPushButton("Exporter")
        self.export_button.clicked.connect(self.run_export)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
        self.setWindowTitle("Steam Library Exporter")
        self.setGeometry(400, 200, 400, 700)

    def create_fields_group(self):
        group_box = QGroupBox("Champs à exporter")
        fields_layout = QVBoxLayout()

        # Liste des champs disponibles, groupés par catégories
        self.field_checkboxes = {
            "Informations générales": {
                "name": QCheckBox("Nom du jeu"),
                "steam_appid": QCheckBox("App ID"),
                "required_age": QCheckBox("Âge requis"),
                "is_free": QCheckBox("Gratuit"),
            },
            "Descriptions": {
                "detailed_description": QCheckBox("Description détaillée"),
                "about_the_game": QCheckBox("À propos du jeu"),
                "short_description": QCheckBox("Brève description"),
                "supported_languages": QCheckBox("Langues supportées"),
                "reviews": QCheckBox("Avis des utilisateurs"),
            },
            "Médias": {
                "header_image": QCheckBox("Image principale"),
                "website": QCheckBox("Site officiel"),
                "screenshots": QCheckBox("Captures d'écran"),
                "movies": QCheckBox("Vidéos"),
            },
            "Éditeurs et développeurs": {
                "developers": QCheckBox("Développeurs"),
                "publishers": QCheckBox("Éditeurs"),
            },
            "Plateformes et support": {
                "platforms": QCheckBox("Plateformes"),
                "support_info": QCheckBox("Informations de support"),
            },
            "Scores et recommandations": {
                "metacritic": QCheckBox("Score Metacritic"),
                "recommendations": QCheckBox("Recommandations"),
            },
            "Détails du contenu": {
                "categories": QCheckBox("Catégories"),
                "genres": QCheckBox("Genres"),
                "content_descriptors": QCheckBox("Descripteurs de contenu"),
                "release_date": QCheckBox("Date de sortie"),
                "background": QCheckBox("Image de fond"),
            }
        }

        # Ajouter chaque catégorie avec ses options
        for category, fields in self.field_checkboxes.items():
            category_box = QGroupBox(category)
            category_layout = QVBoxLayout()
            for field_name, checkbox in fields.items():
                category_layout.addWidget(checkbox)
            category_box.setLayout(category_layout)
            fields_layout.addWidget(category_box)

        group_box.setLayout(fields_layout)
        return group_box

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(f"Fichier sélectionné : {file_path}")

    def run_export(self):
        api_key = self.api_entry.text().strip()
        steam_id = self.steamid_entry.text().strip()
        save_path = self.file_path
        selected_fields = [field_name for category in self.field_checkboxes.values() for field_name, checkbox in category.items() if checkbox.isChecked()]

        if not api_key or not steam_id or not save_path or not selected_fields:
            QMessageBox.warning(self, "Avertissement", "Veuillez remplir tous les champs et sélectionner au moins un champ.")
            return

        # Sauvegarder les informations dans le fichier config.ini
        save_config(api_key, steam_id)

        # Lancer l'exportation avec la barre de progression
        games = get_owned_games(api_key, steam_id)
        self.progress_bar.setMaximum(len(games))
        
        with open(save_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(selected_fields)
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(get_game_details, game["appid"]): game for game in games}
                for i, future in enumerate(as_completed(futures), 1):
                    game = futures[future]
                    row = []

                    try:
                        details = future.result()
                        if details:
                            for field in selected_fields:
                                value = details.get(field, "N/A")
                                if isinstance(value, list):
                                    row.append(", ".join(str(v) for v in value))
                                elif isinstance(value, dict):
                                    row.append(", ".join(f"{k}: {v}" for k, v in value.items()))
                                else:
                                    row.append(value)
                            writer.writerow(row)
                    except Exception as e:
                        print(f"Erreur lors de l'écriture des données pour le jeu {game['name']} (ID: {game['appid']}): {e}")

                    self.progress_bar.setValue(i)

        QMessageBox.information(self, "Succès", f"Exportation terminée dans {save_path}")

# Exécution de l'application PyQt5
app = QApplication(sys.argv)
window = SteamAppExporter()
window.show()
sys.exit(app.exec_())

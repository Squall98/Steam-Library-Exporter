French version : 

# Steam Library Exporter

*Steam Library Exporter* est une application permettant d'extraire les informations des jeux possédés dans une bibliothèque Steam et de les exporter au format CSV. L'application est conçue avec une interface graphique en PyQt5, permettant une utilisation intuitive pour sélectionner et exporter les informations souhaitées.

## Fonctionnalités

- **Extraction des informations** de la bibliothèque Steam d'un utilisateur.
- **Sélection des champs à exporter** (nom du jeu, développeurs, plateformes, etc.).
- **Export au format CSV** des données sélectionnées.
- **Interface graphique moderne** en PyQt5 pour faciliter l'utilisation.
- **Stockage sécurisé des informations d'API**, incluant la clé API Steam et le SteamID, dans un fichier de configuration.

## Prérequis

- **Python 3.7** ou plus récent
- **Compte Steam** avec une bibliothèque de jeux
- **Clé API Steam** – [Générez votre clé API Steam](https://steamcommunity.com/dev/apikey)

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/votreutilisateur/steam-library-exporter.git
   cd steam-library-exporter
   ```

2. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

3. Configurez votre clé API Steam et SteamID dans `config.ini` en suivant l'exemple fourni.

## Utilisation

1. **Lancez l'application** en exécutant :

   ```bash
   python main.py
   ```

2. **Interface utilisateur** : Une fois l'application ouverte, sélectionnez les informations à extraire pour chaque jeu.
3. **Export CSV** : Cliquez sur le bouton pour générer et sauvegarder un fichier CSV avec les données.

## Configuration

Créez un fichier `config.ini` dans le répertoire principal pour sauvegarder vos informations d'identification Steam :

```ini
[steam]
api_key = VOTRE_CLE_API
steamid = VOTRE_STEAMID
```

## Contribution

Les contributions sont les bienvenues ! Suivez ces étapes pour contribuer :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b nouvelle-fonctionnalite`).
3. Effectuez vos modifications et validez-les (`git commit -m "Ajout d'une nouvelle fonctionnalité"`).
4. Poussez votre branche (`git push origin nouvelle-fonctionnalite`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.


English version :

# Steam Library Exporter

*Steam Library Exporter* is an application designed to extract information about games owned in a Steam library and export them to a CSV file. The application features a PyQt5 graphical interface, providing an intuitive way to select and export the desired information.

## Features

- **Extract information** from a user's Steam library.
- **Select fields to export** (game name, developers, platforms, etc.).
- **Export data in CSV format** for easy use and sharing.
- **Modern graphical interface** in PyQt5 for user-friendly experience.
- **Secure API information storage**, including the Steam API key and SteamID, saved in a configuration file.

## Prerequisites

- **Python 3.7** or higher
- **Steam account** with a game library
- **Steam API Key** – [Generate your Steam API Key here](https://steamcommunity.com/dev/apikey)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/steam-library-exporter.git
   cd steam-library-exporter
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Steam API Key and SteamID in `config.ini` as shown in the provided example.

## Usage

1. **Run the application** by executing:

   ```bash
   python main.py
   ```

2. **User Interface**: Once the application opens, select the information to extract for each game.
3. **CSV Export**: Click the button to generate and save a CSV file with the extracted data.

## Configuration

Create a `config.ini` file in the main directory to save your Steam credentials:

```ini
[steam]
api_key = YOUR_API_KEY
steamid = YOUR_STEAMID
```

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the project.
2. Create a branch for your feature (`git checkout -b new-feature`).
3. Make your modifications and commit them (`git commit -m "Add new feature"`).
4. Push your branch (`git push origin new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


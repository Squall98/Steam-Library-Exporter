[![](https://img.icons8.com/color/48/000000/france.png) French Version](#french-version) | [![](https://img.icons8.com/color/48/000000/great-britain.png) English Version](#english-version)


## ![FR](https://img.icons8.com/color/24/000000/france.png) French Version

# Steam Library Exporter

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.4-brightgreen)
![MIT License](https://img.shields.io/badge/License-MIT-yellow)

*Steam Library Exporter* est une application permettant d'extraire les informations des jeux possédés dans une bibliothèque Steam et de les exporter au format CSV. L'application est conçue avec une interface graphique en PyQt5, permettant une utilisation intuitive pour sélectionner et exporter les informations souhaitées.

## Sommaire
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Comment ça marche ?](#comment-ça-marche)
- [Licence](#licence)

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

## Comment ça marche ?

Entrez votre clé API 🔑 - Pour se connecter à Steam.
Choisissez les champs à exporter 📝 - Personnalisez les informations récupérées.
Sélectionnez un fichier de sortie CSV 📂 - Choisissez où sauvegarder les données.
Cliquez sur Exporter ! 🚀 - Le programme génère un fichier CSV avec les informations de votre bibliothèque Steam.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.


## ![GB](https://img.icons8.com/color/24/000000/great-britain.png) English Version

# Steam Library Exporter

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.4-brightgreen)
![MIT License](https://img.shields.io/badge/License-MIT-yellow)

*Steam Library Exporter* is an application that allows you to extract information about games owned in a Steam library and export it to CSV format. Designed with a PyQt5 graphical interface, this application provides an intuitive experience for selecting and exporting the desired information.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [License](#license)

## Features

- **Extract game information** from a user's Steam library.
- **Select fields to export** (game name, developers, platforms, etc.).
- **Export selected data** to CSV format.
- **Modern graphical interface** built with PyQt5 for ease of use.
- **Secure storage of API information**, including the Steam API key and SteamID in a configuration file.

## Requirements

- **Python 3.7** or higher
- **Steam account** with a game library
- **Steam API Key** – [Generate your Steam API key here](https://steamcommunity.com/dev/apikey)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/steam-library-exporter.git
   cd steam-library-exporter


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
## How It Works

Enter your API key 🔑 - Connect to Steam.
Choose fields to export 📝 - Customize the information to retrieve.
Select an output CSV file 📂 - Choose where to save the data.
Click Export! 🚀 - The program generates a CSV file with your Steam library information.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


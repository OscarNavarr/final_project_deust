# 🚀 Guide pour Démarrer le Serveur FastAPI

Ce guide vous explique comment lancer le serveur FastAPI pour le projet de simulation de robot.

## 📦 Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- Python 3.8 ou plus récent
- `pip` (gestionnaire de paquets Python)
- FastAPI et Uvicorn

## 🔧 Installation des dépendances

Ouvrez un terminal et tapez :

```bash
pip install fastapi uvicorn jinja2 requests sqlite3
```


## 1 Créer un environnement virtuel

Ceci permet d’isoler les dépendances de votre projet.

Dans le terminal, tapez :

```bash
python3 -m venv venv
```

## 2 Activer l’environnement virtuel

Linux/macOS :


```bash
source venv/bin/activate
```
Windows (CMD) :
```bash
venv\Scripts\activate.bat
```
Windows (PowerShell) :
```bash
venv\Scripts\Activate.ps1
```

## 4 Lancer le serveur 
Dans le terminal (en étant dans le dossier du projet), tapez :
```bash
uvicorn main:app --reload --host 0.0.0.0
``` 

## 5 Lancer le contrôleur
Dans une autre ongle du terminal, exécuter la commande pour initialiser l'environnement virtuel et après exécuter cette commande:
```bash
python3 simulator_gui.py
``` 
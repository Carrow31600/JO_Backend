# JO_Backend

Backend du site web de vente de billets pour les Jeux Olympiques de Paris 2024 
Framework :  Django et Django REST Framework (DRF), il fournit une API REST sécurisée pour la gestion des utilisateurs, billets et commandes.


## Prérequis

- Python 3.12  
- pip 
- Virtualenv  
- SQLite (en local)  
- MySQL (en production sur PythonAnywhere)  

## Installation locale (développement)

### 1. Cloner le projet

git clone https://github.com/ton-compte/JO_Backend.git

cd JO_Backend

### 2. Créer l'environnement virtuel

python -m venv venv

venv\Scripts\activate      # Windows

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Configurer les variables 'environnement

Un fichier .env est utilisé . Exemple de configuration par défaut pour le développement local :

SECRET_KEY=django-insecure-change_me

DEBUG=True

DATABASE_NAME=db.sqlite3

En production, DEBUG doit être mis à False et la configuration MySQL doit être ajoutée.

## Lancer le projet

### 1.Faire les migrations

python manage.py migrate

### 2. Créer un superutilisateur

python manage.py createsuperuser

### 3. Lancer le serveur

python manage.py runserver

Le serveur sera disponible à l’adresse : http://127.0.0.1:8000

# Documentation API

Outil : drf-yasg

Swagger UI → http://127.0.0.1:8000/swagger/

ReDoc → http://127.0.0.1:8000/redoc/

# Lancer les tests

python manage.py test

# Déploiement (pythonanywhere)

## 1. Créer une base MySQL sur PythonAnywhere

## 2. Adapter le fichier .env avec la configuration MySQL

SECRET_KEY=changer_cette_clef

DEBUG=False

DATABASE_ENGINE=mysql

DATABASE_NAME=nom_de_la_base

DATABASE_USER=ton_utilisateur

DATABASE_PASSWORD=ton_mot_de_passe

DATABASE_HOST=nom_du_serveur

DATABASE_PORT=3306

## 3. Lancer les migrations et collecter les fichiers statiques

python manage.py migrate

python manage.py collectstatic




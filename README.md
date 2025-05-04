# Projet StockFast

## Introduction

Création d'un application web pour gérer les stocks de produits.

- gestion des utilisateurs
- gestion des produits
- gestion des quantités par entrepôt
- gestion des alertes
- gestion des données

Gestion du projet : [lien notion](https://mathieu24dev.notion.site/Gestion-de-stock-x-Django-1e6c4218a91480dea221c17419013a28?pvs=4)

## Installation

```bash
# cloner le projet
git clone https://github.com/math-dev-24/stock-django
cd stock-django

# créer un virtualenv
virtualenv venv
source venv/bin/activate

# installer les dépendances
pip install -r requirements.txt

# créer la base de données
python manage.py makemigrations
python manage.py migrate

# Chargement des fixtures
python manage.py loaddata categories.json
python manage.py loaddata companies.json
python manage.py loaddata products.json
python manage.py loaddata prices.json
```

# Fonctionnalités
1. Catalogue produits
Création, consultation, modification et suppression des fiches produits (EAN ou identifiant unique (SKU), libellé, description, prix de référence, seuil d'alerte).

2. Multi-entrepôts / boutiques
Possibilité d'enregistrer plusieurs points de vente ou dépôts et de suivre les quantités disponibles par site.

3. Mouvements de stock
Entrées, sorties, historisation avec horodatage.

4. Alertes seuil critique
Génération d'un rapport au format JSON contenant les produits en rupture de stock.

5. Affichage des données
Affichage des données de façon lisible et agréable pour l'utilisateur avec la librairie Rich.

# Base de données
![Schéma de base de données](./demo/bdd.png)

# Demo 
### Vue accueil
![HomePage](./demo/home.png)

### Vue dashboard
![Dashboard](./demo/dashboard.png)

## Vue catalogue produits
![catalogue-product](./demo/list-product.png)

![catalogue-product](./demo/list-product-2.png)

## Vue détaillée produit
![detail-product](./demo/detail-product.png)

## Update produit 
![update-product](./demo/update-product.png)

## Flux de commande
![order](./demo/flux.png)

## Inventaire
![inventory](./demo/inventory.png)
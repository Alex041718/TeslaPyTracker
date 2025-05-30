# Application Flask avec MongoDB

Cette application est une API RESTful construite avec Flask et MongoDB suivant une architecture en couches.

## Structure du projet

```
project/
├── app/
│   ├── __init__.py          # Factory pattern pour créer l'application Flask
│   ├── config.py            # Configuration de l'application
│   ├── controllers/         # Gestion des routes et des requêtes HTTP
│   │   └── user_controller.py
│   ├── services/            # Logique métier
│   │   └── user_service.py
│   ├── models/              # Interaction avec la base de données
│   │   └── user_model.py
│   ├── schemas/             # Validation et sérialisation des données
│   │   └── user_schema.py
│   └── utils/               # Fonctions utilitaires
│       └── helpers.py
├── tests/                   # Tests unitaires
│   └── test_user.py
├── run.py                   # Point d'entrée de l'application
└── requirements.txt         # Dépendances du projet
```

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel Python:
   ```
   python3 -m venv venv
   source venv/bin/activate  
   ```
3. Installer les dépendances:
   ```
   pip install -r requirements.txt
   ```
4. S'assurer que MongoDB est installé et en cours d'exécution
5. Lancer l'application:
   ```
   python3 run.py
   ```

## Endpoints API

- `GET /api/users/` - Récupérer tous les utilisateurs
- `GET /api/users/<id>` - Récupérer un utilisateur spécifique
- `POST /api/users/` - Créer un nouvel utilisateur
- `PUT /api/users/<id>` - Mettre à jour un utilisateur
- `DELETE /api/users/<id>` - Supprimer un utilisateur

## Tests

Exécuter les tests unitaires:
```
python -m pytest
```
# Tesla Tracker Python

Application de suivi des prix Tesla Model 3 d'occasion avec visualisation graphique des données.

## Architecture

Le projet est composé de trois services principaux :

- **API Backend (Flask)** : Gère les requêtes, le traitement des données et l'accès à la base de données
- **Frontend (React)** : Interface utilisateur pour la visualisation des données
- **Batch Scheduler** : Service de collecte automatique des données Tesla

## Technologies

### Backend
- Python 3.x
- Flask (API REST)
- MongoDB (Base de données)
- Flask-CORS (Gestion des CORS)
- Flask-PyMongo (Interface MongoDB)
- Flask-Smorest (Documentation API)

### Frontend
- React 19
- TypeScript
- Vite
- Recharts (Graphiques)
- SASS
- Axios (Requêtes HTTP)

## Installation

### Prérequis
- Docker
- Docker Compose
- Git

### Configuration

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/TeslaTrackerPython.git
cd TeslaTrackerPython
```

2. Créez le fichier `.env` à partir du modèle :
```bash
cp .env.example .env
```

3. Modifiez les variables d'environnement dans `.env` selon vos besoins

### Démarrage

1. Construisez et démarrez les conteneurs :
```bash
docker-compose up -d
```

2. Vérifiez que tous les services sont en cours d'exécution :
```bash
docker-compose ps
```

## Services

### API Backend (port 5555)

L'API expose une interface Swagger UI accessible à :
```
http://localhost:5555/api/docs/swagger
```

#### Endpoints Principaux

- `GET /api/graphs/min-price` : Évolution du prix minimum des Tesla
  - Paramètres :
    - year (optionnel) : Année à filtrer
    - version (optionnel) : Version Tesla spécifique
    - points (optionnel, défaut: 25) : Nombre de points pour le graphe

### Frontend (port 5173)

Interface utilisateur accessible à :
```
http://localhost:5173
```

### Batch Scheduler

Service automatisé qui :
- Collecte les données Tesla à intervalles réguliers
- Stocke les informations dans MongoDB
- Configuration des tâches dans `app/batch_config.json`

## Structure du Projet

```
.
├── app/                    # Backend Flask
│   ├── controllers/        # Contrôleurs API
│   ├── services/          # Logique métier
│   ├── schemas/          # Schémas de validation
│   └── dto/              # Objets de transfert de données
├── spa/                   # Frontend React
│   ├── src/              # Code source React
│   │   ├── components/   # Composants React
│   │   ├── api/         # Services API
│   │   └── dto/         # Types TypeScript
└── docker-compose.yml    # Configuration Docker
```

## Déploiement sur Raspberry Pi

Pour les instructions de déploiement sur Raspberry Pi, consultez [RASPBERRY_PI.md](RASPBERRY_PI.md).

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout de ma fonctionnalité'`)
4. Push vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Créez une Pull Request
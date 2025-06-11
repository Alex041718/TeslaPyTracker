# Tesla Tracker Python

## API Documentation avec Swagger UI

L'application expose une interface Swagger UI qui permet de :
- Explorer les endpoints disponibles
- Tester les requêtes directement depuis l'interface
- Consulter les schémas de données
- Comprendre les paramètres acceptés par chaque endpoint

### Accès à l'Interface Swagger

Une fois l'application démarrée avec Docker Compose :
```bash
docker-compose up -d
```

L'interface Swagger UI est accessible à :
```
http://localhost:${PORT}/api/docs/swagger
```
où ${PORT} est le port défini dans votre fichier .env

### Endpoints Disponibles

#### Graphes
- `GET /api/graphs/min-price` : Évolution du prix minimum des Tesla
  - Paramètres :
    - year (optionnel) : Année à filtrer
    - version (optionnel) : Version Tesla spécifique
    - points (optionnel, défaut: 25) : Nombre de points souhaités pour le graphe

La réponse inclut :
- Métadonnées (nombre total de points, points normalisés)
- Points du graphe (timestamp, prix, description)
- Liens de navigation

## Configuration du Service Systemd sur Raspberry Pi

Pour assurer que l'application continue de fonctionner après la déconnexion SSH et redémarre automatiquement après un reboot, suivez ces étapes pour configurer un service systemd.

### Prérequis

- Docker et Docker Compose installés sur le Raspberry Pi
- Droits sudo sur le Raspberry Pi
- Le projet cloné dans un répertoire sur le Raspberry Pi

### Étapes d'Installation

1. **Créer le fichier service systemd**

```bash
sudo nano /etc/systemd/system/tesla-tracker.service
```

2. **Copier la configuration suivante** (ajustez le chemin et l'utilisateur selon votre configuration)

```ini
[Unit]
Description=Tesla Tracker Docker Compose
Requires=docker.service
After=docker.service network.target

[Service]
Type=oneshot
RemainAfterExit=yes
User=pi
Group=docker
WorkingDirectory=/home/pi/TeslaPyTracker
ExecStart=/usr/bin/docker compose up --detach --build
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

3. **Activer et démarrer le service**

```bash
# Recharger la configuration systemd
sudo systemctl daemon-reload

# Activer le service pour qu'il démarre au boot
sudo systemctl enable tesla-tracker.service

# Démarrer le service
sudo systemctl start tesla-tracker.service
```

### Commandes Utiles

**Vérifier l'état du service :**
```bash
sudo systemctl status tesla-tracker.service
```

**Consulter les logs :**
```bash
# Voir les logs en temps réel
journalctl -u tesla-tracker.service -f

# Voir les dernières entrées
journalctl -u tesla-tracker.service -n 50
```

**Redémarrer le service :**
```bash
sudo systemctl restart tesla-tracker.service
```

**Arrêter le service :**
```bash
sudo systemctl stop tesla-tracker.service


git pull && sudo systemctl restart tesla-tracker.service
```

### Résolution des Problèmes Courants

1. **Le service ne démarre pas**
   - Vérifiez les logs : `journalctl -u tesla-tracker.service -n 50`
   - Vérifiez que les chemins dans le fichier service sont corrects
   - Assurez-vous que l'utilisateur a les droits nécessaires
   - Si vous obtenez une erreur USER (status=217), exécutez :
     ```bash
     sudo usermod -aG docker pi
     sudo chown -R pi:pi /home/pi/TeslaPyTracker
     ```

2. **Erreur de permission Docker**
   - Assurez-vous que votre utilisateur fait partie du groupe docker :
     ```bash
     sudo usermod -aG docker votre_utilisateur
     ```
   - Déconnectez-vous et reconnectez-vous pour que les changements prennent effet

3. **Les conteneurs ne redémarrent pas automatiquement**
   - Vérifiez que `restart: always` est configuré dans docker-compose.yml pour chaque service
   - Assurez-vous que le service systemd a `Restart=always` dans sa configuration

### Notes Importantes

- Le service redémarrera automatiquement en cas d'erreur après 10 secondes (configurable via `RestartSec`)
- Les logs sont conservés dans journald et peuvent être consultés même après un redémarrage
- Le service démarre automatiquement au boot du Raspberry Pi
- La connexion SSH peut être fermée sans affecter le fonctionnement des conteneurs


Mode rootless Docker : si vous utilisez Docker en mode non-root (rootless), le démon Docker s’arrête par défaut quand la session utilisateur se termine. Dans ce cas, il faut activer le linger pour que le service continue de tourner après déconnexion. Exécutez par exemple :
```bash
sudo loginctl enable-linger pi
```
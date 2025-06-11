# Déploiement sur Raspberry Pi

Guide détaillé pour déployer Tesla Tracker Python sur un Raspberry Pi.

## Prérequis

- Raspberry Pi (3 ou plus récent recommandé)
- Docker et Docker Compose installés
- Droits sudo
- Git installé

## Installation

1. **Clonez le projet**
```bash
git clone https://github.com/votre-username/TeslaTrackerPython.git
cd TeslaTrackerPython
```

2. **Configuration du service systemd**

Créez le fichier service :
```bash
sudo nano /etc/systemd/system/tesla-tracker.service
```

Ajoutez la configuration suivante :
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
WorkingDirectory=/home/pi/TeslaTrackerPython
ExecStart=/usr/bin/docker compose up --detach --build
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

3. **Activation du service**

```bash
# Recharger la configuration systemd
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable tesla-tracker.service

# Démarrer le service
sudo systemctl start tesla-tracker.service
```

## Gestion du Service

### Commandes Utiles

**Vérifier l'état du service :**
```bash
sudo systemctl status tesla-tracker.service
```

**Consulter les logs :**
```bash
# Temps réel
journalctl -u tesla-tracker.service -f

# Dernières entrées
journalctl -u tesla-tracker.service -n 50
```

**Redémarrer le service :**
```bash
sudo systemctl restart tesla-tracker.service
```

**Arrêter le service :**
```bash
sudo systemctl stop tesla-tracker.service
```

**Mettre à jour et redémarrer :**
```bash
git pull && sudo systemctl restart tesla-tracker.service
```

## Résolution des Problèmes

### 1. Le service ne démarre pas
- Vérifiez les logs : `journalctl -u tesla-tracker.service -n 50`
- Vérifiez les chemins dans le fichier service
- Assurez-vous que l'utilisateur a les droits nécessaires
- Si erreur USER (status=217) :
  ```bash
  sudo usermod -aG docker pi
  sudo chown -R pi:pi /home/pi/TeslaTrackerPython
  ```

### 2. Erreur de permission Docker
```bash
sudo usermod -aG docker votre_utilisateur
# Déconnectez-vous et reconnectez-vous
```

### 3. Mode rootless Docker
Si vous utilisez Docker en mode non-root, activez le linger :
```bash
sudo loginctl enable-linger pi
```

## Notes Importantes

- Le service redémarre automatiquement en cas d'erreur après 10 secondes
- Les logs sont conservés dans journald
- Le service démarre automatiquement au boot
- La connexion SSH peut être fermée sans affecter les conteneurs
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ca-certificates

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production


# Commande pour démarrer l'application
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} run:app"]
# Utiliser une image de base Python
FROM python:3.10-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration et de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Définir le PYTHONPATH pour inclure le répertoire /app
ENV PYTHONPATH=/app

# Commande par défaut pour exécuter le script principal
CMD ["python", "scripts/main.py"]

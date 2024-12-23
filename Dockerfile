# Utiliser une image de base officielle de Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirement.txt

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
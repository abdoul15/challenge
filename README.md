# Projet d'Ingestion et de Traitement de Données

## 📚 Contexte
Ce projet a pour but de concevoir une architecture de données permettant d'ingérer, de nettoyer et de croiser des données issues de différentes sources, principalement une API (TMDB) et un fichier CSV. L'objectif final est de fournir un jeu de données utilisable pour des analyses et des modélisations par des data scientists ou des analystes métiers.

## 🛠️ Prérequis
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 Installation
1. **Cloner le dépôt** :
    ```bash
    git clone https://github.com/abdoul15/challenge.git
    cd challenge
    ```

2. **Créer le fichier `.env`** :
    Ajoutez les informations suivantes :
    ```env
    TMDB_API_KEY=f85659b0221cb3d47786757dcc8c0fc4
    DATABASE_URL=postgresql+psycopg2://postgres:xavite@postgres:5432/my_movies
    ```

    ⚠️ **Attention** : Ne jamais mettre de clés API ou d'informations sensibles dans un dépôt git. Ceci est fait ici uniquement pour des besoins de tests rapides.

3. **Construire et démarrer les conteneurs Docker** :
    ```bash
    docker-compose up --build -d
    ```

4. **Exécuter le conteneur postgres** :
    ```bash
    docker exec -it [container-name or id] bash
    ```
    Puis :
    ```bash
    psql -h localhost -p 5432 -U postgres -d my_movies
    ```

5. **Initialiser Superset** :
    ```bash
    docker exec -it superset superset db upgrade
    docker exec -it superset superset init
    ```

    Ouvrez votre navigateur à [http://localhost:8088](http://localhost:8088) et connectez-vous avec les informations d'identification administrateur : `admin` & `admin`.

    Si cela ne fonctionne pas, alors créez un utilisateur :
    Utilisez la commande suivante pour créer un nouvel utilisateur administrateur. Remplacez `your_username`, `your_password`, `your_email`, `your_first_name`, et `your_last_name` par les valeurs souhaitées.
    ```bash
    docker exec -it superset superset fab create-admin \
      --username your_username \
      --firstname your_first_name \
      --lastname your_last_name \
      --email your_email \
      --password your_password
    ```

6. **Redémarrer Superset** :
    ```bash
    docker-compose restart superset
    ```

---

N'hésitez pas à contribuer à ce projet en soumettant des issues ou des pull requests. Bon codage ! 🎉

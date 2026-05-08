# reverseproxy-traefik-dockerapp

Configuration simple de reverse proxy Traefik avec deux applications Flask et une base de données PostgreSQL.

## Architecture

```
Internet
   |
   v
Traefik (port 9443)
   |-- /blue   -->  blue  (Flask, port 8080)  [fond bleu]
   |-- /green  -->  green (Flask, port 8081)  [fond vert]
                       |
                       v
                      db (PostgreSQL, reseau interne uniquement)
```

| Service  | Image / Build         | Couleur | Role                          |
|----------|-----------------------|---------|-------------------------------|
| traefik  | traefik:v3.3          | -       | Reverse proxy / load balancer |
| blue     | ./blue (Flask)        | #1565C0 | Application Blue              |
| green    | ./green (Flask)       | #2E7D32 | Application Green             |
| db       | postgres:17-alpine    | -       | Base de donnees PostgreSQL    |

## Prerequis

- [Docker](https://docs.docker.com/get-docker/) >= 24
- [Docker Compose](https://docs.docker.com/compose/) v2

## Demarrage rapide

```bash
# 1. Copier et adapter les variables d'environnement
cp .env.example .env

# 2. Lancer la stack
docker compose up -d

# 3. Verifier que tous les services sont up
docker compose ps
```

Les applications sont alors accessibles sur :

- **blue**  --> http://localhost:9443/blue
- **green** --> http://localhost:9443/green
- **Dashboard Traefik** --> http://localhost:9090

Tests de sante :

- **blue liveness**         --> http://localhost:9443/blue/health
- **green liveness**        --> http://localhost:9443/green/health
- **blue deep health (DB)** --> http://localhost:9443/blue/db-check
- **green deep health (DB)**--> http://localhost:9443/green/db-check

`/health` verifie uniquement que l'application repond (sans acces DB).

`/db-check` verifie l'application + la connectivite PostgreSQL via create/insert/select.

## Variables d'environnement

| Variable          | Valeur par defaut | Description                      |
|-------------------|-------------------|----------------------------------|
| POSTGRES_USER     | appuser           | Utilisateur PostgreSQL           |
| POSTGRES_PASSWORD | *(obligatoire)*   | Mot de passe PostgreSQL          |
| POSTGRES_DB       | appdb             | Nom de la base de donnees        |

## Securite

> Ces notes s'appliquent principalement aux deploiements exposes sur un reseau.

| Point                          | Risque                                                                                      | Recommandation                                                                                      |
|--------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Dashboard Traefik (`insecure`) | Le dashboard est accessible sans authentification sur le port 9090.                         | Supprimer `insecure: true` et proteger le dashboard avec un middleware `basicAuth` en production.   |
| Socket Docker monte            | Traefik monte `/var/run/docker.sock` en lecture seule, ce qui donne acces a l'API Docker.   | Utiliser un proxy de socket (ex. [socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)) pour limiter les droits en production. |
| Mot de passe PostgreSQL        | `POSTGRES_PASSWORD` est obligatoire et doit etre defini dans `.env`.                        | Utiliser un mot de passe fort et ne jamais commiter le fichier `.env`.                              |

## Arret

```bash
# Arreter la stack (conserve les volumes)
docker compose down

# Arreter et supprimer les volumes (efface les donnees)
docker compose down -v
```

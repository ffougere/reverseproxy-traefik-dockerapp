# reverseproxy-traefik-dockerapp

Configuration simple de reverse proxy Traefik avec deux applications et une base de données PostgreSQL.

## Architecture

```
Internet
   │
   ▼
Traefik (port 80)
   ├── app1.localhost  →  app1
   └── app2.localhost  →  app2
                              │
                              ▼
                             db (PostgreSQL, réseau interne uniquement)
```

| Service  | Image                  | Rôle                        |
|----------|------------------------|-----------------------------|
| traefik  | traefik:v3.3           | Reverse proxy / load balancer |
| app1     | nginxdemos/hello       | Application 1               |
| app2     | nginxdemos/hello       | Application 2               |
| db       | postgres:17-alpine     | Base de données PostgreSQL  |

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/) v2

## Démarrage rapide

```bash
# 1. Copier et adapter les variables d'environnement
cp .env.example .env

# 2. Lancer la stack
docker compose up -d

# 3. Vérifier que tous les services sont up
docker compose ps
```

Les applications sont alors accessibles sur :

- **app1** → http://app1.localhost
- **app2** → http://app2.localhost
- **Dashboard Traefik** → http://localhost:8080

> **Note** : `*.localhost` est résolu nativement par la plupart des systèmes d'exploitation modernes. Si ce n'est pas le cas, ajoutez les entrées suivantes dans votre fichier `/etc/hosts` :
> ```
> 127.0.0.1  app1.localhost
> 127.0.0.1  app2.localhost
> ```

## Variables d'environnement

| Variable          | Valeur par défaut | Description                      |
|-------------------|-------------------|----------------------------------|
| POSTGRES_USER     | appuser           | Utilisateur PostgreSQL           |
| POSTGRES_PASSWORD | *(obligatoire)*   | Mot de passe PostgreSQL          |
| POSTGRES_DB       | appdb             | Nom de la base de données        |

## Sécurité

> Ces notes s'appliquent principalement aux déploiements exposés sur un réseau.

| Point                          | Risque                                                                                      | Recommandation                                                                                      |
|--------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Dashboard Traefik (`insecure`) | Le dashboard est accessible sans authentification sur le port 8080.                         | Supprimer `insecure: true` et protéger le dashboard avec un middleware `basicAuth` en production.   |
| Socket Docker monté            | Traefik monte `/var/run/docker.sock` en lecture seule, ce qui donne accès à l'API Docker.   | Utiliser un proxy de socket (ex. [socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)) pour limiter les droits en production. |
| Mot de passe PostgreSQL        | `POSTGRES_PASSWORD` est obligatoire et doit être défini dans `.env`.                        | Utiliser un mot de passe fort et ne jamais commiter le fichier `.env`.                              |

## Arrêt

```bash
# Arrêter la stack (conserve les volumes)
docker compose down

# Arrêter et supprimer les volumes (⚠ efface les données)
docker compose down -v
```

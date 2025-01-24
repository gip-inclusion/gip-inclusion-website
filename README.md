# Site Web du GIP de l'inclusion

## Prérequis

- Python [(version)](./python-version)
- [docker](https://docs.docker.com/get-started/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installer les pre-commit hooks

```sh
pre-commit install
```

On peut faire un premier test en faisant tourner :

```sh
pre-commit run --all-files
```

## Installation

Le projet peut se lancer en local ou avec Docker.

### En local

#### Lancer les containers

```sh
docker-compose up
```

#### Définir les variables d'environnement

```sh
cp .env.example .env
$EDITOR .env
```

#### Créer un environnement virtuel

```sh
# Configurer et activer l'environnement virtuel
uv venv
. .venv/bin/activate
uv pip sync --require-hashes requirements.txt
```

#### Copier les variables d'environnement

```sh
cp .env.example .env
```

#### Configurer le bucket

```sh
python manage.py configure_bucket
```

#### Lancer le serveur

```sh
python manage.py runserver
```

#### Lancer les migrations

```sh
python manage.py migrate
```

#### Effectuer les tests

Les tests unitaires peuvent être lancés avec `make test-units`, les
tests E2E avec `make test-e2e`, les deux avec `make test`.

Pour les tests E2E, si vous n'utilisez pas Docker, il vous faudra
[Firefox](https://www.mozilla.org/fr/firefox/download/thanks/) et
[`geckodriver`](https://github.com/mozilla/geckodriver/releases)
accessibles sur votre machine pour lancer les tests E2E.  Sur MacOS,
vous pouvez les installer via [brew](https://brew.sh/) avec la commande: `brew install geckodriver`.

Vous pouvez également générer un rapport sur la couverture de tests :
```sh
coverage run manage.py test --settings config.settings_test
```

#### Mettre à jour les paquets Python

```
uv pip compile --generate-hashes requirements.in -o requirements.txt
```

### Premier lancement

Pour initialiser le site avec notamment la page d'accueil au bon format :
```sh
python manage.py loaddata cms/fixtures/fixtures.json
```

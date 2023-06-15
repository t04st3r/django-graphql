[![CircleCI](https://circleci.com/gh/t04st3r/django-graphql.svg?style=shield)](https://app.circleci.com/pipelines/github/t04st3r/django-graphql) [![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


# Django graphQL
Just a sample project on how to expose graphQL API with Django

## Install
To run django locally you need python version to `3.11.3` and pipenv, you can use [pyenv](https://github.com/pyenv/pyenv) to set your desired python version.

### Run containers
Django needs postgres and redis container to be
up and running, to do so clone the project, enter in the project folder and hit:
```bash
docker compose up postgres redis
```

### Install django deps and run django server
inside the project folder make sure you use python 3.11.3
```bash
python --version
```
you should see
```bash
Python 3.11.3
```
install requirements (listed inside `Pipfile`) by
```bash
pipenv install
```
To run tests you will need also dev dependencies
```bash
pipenv install --dev
```
Create a `.env` file using the `.env.example` file and changing the url to be `localhost` in the following env variables
```env
POSTGRES_HOST
REDIS_URL
```
Your `.env` file should be something like this
```env
#django
ENV=dev
DJANGO_DEBUG=True
SECRET_KEY='supersecretkey'

#db
POSTGRES_USER=postgres
POSTGRES_DB=app_db
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432

#redis
REDIS_URL=redis://localhost:6379/0

```

Once done enter inside your pipenv virtual environment by
```bash
pipenv shell
```
Run migrations with
```bash 
python manage.py migrate
```
Or (if you have `make` installed) by
```bash
make migrate
```
Everything is done! You can now start the server with
```bash
python manage.py runserver
```
Or
```bash
make run-dev
```
## How does it works
This apps gather data from [Public Holiday API](https://date.nager.at/Api) via a django command, you can populate PublicHoliday models with
```bash
python manage.py populate_models
```
Or
```bash
make populate-models
```
For each command run a random country is selected and all the public holidays for that country would be fetched and stored in the db

# GraphQL
To test some graphQL queries against the API just connect with the browser to
```bash
http://localhost:8000/graphql
```
Possible queries can be: 

- fetching all the Public Holiday models via `allHolidays`

```gql
query {
    allHolidays {
        id
        name
        localName
        country
        date
    }
}
```

- fetching all the Public Holiday filtered by country via `holidayByCountry` (in the example models are filtered by Italy country)

```gql
query {
    holidayByCountry(country: "IT"){
        id
        localName
        name
        country
    }
}
```
- Mutate the localName of a PublicHoliday via `updatePublicHoliday` (in the example the `localName` field of the model with ID 1 is changed to "Pizza")

```gql
mutation MyMutation {
    updatePublicHoliday(id: "1", localName: "Pizza") {
        publicHoliday {
            id
            localName
        }
    }
}
```

## Testing
Testing requirements can be installed by
```bash
pipenv install --dev
```
To run the ruff linter on your codebase hit
```bash
make lint
```
pre-commit (that in turn will run ruff check) can be installed as well with
```bash
pre-commit install
``` 
You can run django tests by simply run
```bash
pytest
```
To simulate the [testing pipeline](https://app.circleci.com/pipelines/github/t04st3r/django-graphql) in CircleCI just run
```bash
docker compose run django ci
```
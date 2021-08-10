# whispers

[![CI](https://github.com/pyritewolf/whispers/actions/workflows/main.yml/badge.svg)](https://github.com/pyritewolf/whispers/actions/workflows/main.yml)

A small tool to merge chats from different sources

## Development

1. Clone the project
2. Copy `.env.sample` to an `.env` file
3. Run `./dev-setup.sh`
   - Make sure to run this command every time you update your working branch!
5. Run `docker-compose up` (make sure to have docker & docker-compose)
6. Visit http://localhost:5000 (or http://ui.whispers.lvh.me:5000 if you're using [dockerdev](https://github.com/waj/dockerdev))!

### Running tests

If you want to run the test suite locally, use the following command:

```zsh
docker-compose run --rm -e POSTGRES_DB='whispers_test' api pytest
```

### Interacting with the Database

#### Creating new backend apps with models

If you're creating an app on the backend and it contains models, you'll need to set up a couple of things to make sure migrations work. To begin with, in your app's `models.py` make sure to import the app's declarative base and creating your models based off that:

```python
from db.base_model import BaseModel

class YourCoolModel(Base):
    __tablename__ = "super_cool_models"
    id = Column(Integer, primary_key=True, index=True)
    # all your fun model attributes go here
```

After that, head over to `db.env` and import your models on the top section of the file:

```python
from users import models
from yourcoolapp import models
```

That's about it! Migrations should auto-generate correctly with that set up!

#### Generating & running migrations

As part of our everyday work, data models may change from time to time. When you change a model in the backend, make sure to run the following code to generate any necessary Alembic migrations:

```zsh
docker-compose run --rm api alembic revision --autogenerate -m "Migration name here!"
```

When possible, keep the migration name descriptive!

When a new migration file is available, apply it by running

```zsh
./dev-setup.sh
```

If you want to run them manually you can also do:

```zsh
docker-compose run --rm api alembic upgrade head # to move migrations forward
docker-compose run --rm api alembic downgrade -1 # to roll back 1 version
```

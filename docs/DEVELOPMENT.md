# Development

1. Clone the project
2. Copy `.env.sample` to an `.env` file (check out [this section](#Environment-variables) for more info)
3. Run `./dev-setup.sh`
   - Make sure to run this command every time you update your working branch!
4. Run `docker-compose up` (make sure to have docker & docker-compose)
5. Visit http://localhost:5000 (or http://ui.whispers.lvh.me:5000 if you're using [dockerdev](https://github.com/waj/dockerdev))!

## Running tests

If you want to run the test suite locally, use the following command:

```zsh
docker-compose run --rm -e POSTGRES_DB='whispers_test' api pytest
```

## Interacting with the Database

### Creating new backend apps with models

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

### Generating & running migrations

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

### Environment variables

Most mandatory env variables for development can be simply copied from the sample file. The following variables are optional, and you can fill them out if you want specific features to work.

- **Mailing variables**
  - `MAILGUN_KEY` and `MAILGUN_DOMAIN`: These are two basic keys you can get in [Mailgun](https://app.mailgun.com/app/dashboard).
  - `EMAILS_FROM_NAME` and `EMAILS_FROM_ADDRESS`: The name and email address that will be associated with any emails sent out. The address must be in the same domain as `MAILGUN_DOMAIN`.
- **Youtube integration variables**
  - `GOOGLE_OAUTH_CLIENT` and `GOOGLE_OAUTH_SECRET`: You can get these by creating an app in the [Google Developer console](https://console.cloud.google.com/), in the Credentials section. Make sure to enable the Youtube API in the Library, and to set up `{your dev domain}/oauth/google/callback` as a redirect URI. More  on this [here](https://developers.google.com/youtube/v3/live/guides/auth/server-side-web-apps).

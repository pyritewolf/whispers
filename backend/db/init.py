import sys

import sqlalchemy
import alembic.config
from pydantic import PostgresDsn

from config import settings


databases_to_create = [
    settings.POSTGRES_DB,
    settings.POSTGRES_TEST_DB,
]

engine = sqlalchemy.create_engine(
    PostgresDsn.build(
        scheme="postgresql",
        host=settings.POSTGRES_HOST,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        path=f"/postgres",
        port=settings.POSTGRES_PORT,
    )
)
connection = engine.connect()
connection.execute("commit")

# Query for existing databases
existing_databases = connection.execute("SELECT datname FROM pg_database;")
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [
    d[0] for d in existing_databases if d[0] in databases_to_create
]

if "--hard" in sys.argv:
    print("Initializing DBs with --hard option")
    print("All preexisting data will now be deleted...")
    for database in existing_databases:
        connection.execute(f"DROP DATABASE {database}")
        connection.execute("commit")
        print(f"Dropped database {database} 🔥")
    existing_databases = []

for database in databases_to_create:
    if database not in existing_databases:
        connection.execute(f"CREATE DATABASE {database}")
        connection.execute("commit")
        print(f"Created database {database} 😎")
    else:
        print(f"Database {database} already exists 🥳")

alembic.config.main(argv=["upgrade", "head"])

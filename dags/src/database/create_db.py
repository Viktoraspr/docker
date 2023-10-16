from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from dags.src.constants.credentials import URL


def drop_db(url=URL):
    engine = create_engine(url)
    if database_exists(engine.url):
        drop_database(engine.url)


def create_db(url=URL):
    engine = create_engine(url)
    if not database_exists(engine.url):
        create_database(engine.url)


if __name__ == "__main__":
    drop_db()
    create_db()

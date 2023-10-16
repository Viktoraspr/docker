from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.constants.credentials import URL
from src.database.database import Job


class DBConnection:
    def __init__(self, url=URL):
        self.url = url
        self.engine = create_engine(self.url)
        base: Any = declarative_base()
        base.metadata.create_all(bind=self.engine)
        self.session_ = sessionmaker(bind=self.engine)
        self.session = self.session_()

    def add_value_to_db(self, job):
        self.session.add(job)
        self.session.commit()

    def add_values_to_db(self, jobs: list):
        self.session.add_all(jobs)
        self.session.commit()

    def check_if_job_exists_in_db(self, link_to_job):
        return self.session.query(Job).filter_by(link_to_job=link_to_job).one_or_none()

    def get_values_from_job_table(self):
        return self.session.query(Job).all()

    def close_session(self):
        self.session.close()

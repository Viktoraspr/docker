from datetime import datetime
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

from src.constants.credentials import URL

Base: Any = declarative_base()
engine = create_engine(URL)


class Job(Base):
    """
    Class describe table 'cities' in database
    """
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    portal = Column(String(50))
    company = Column(String(80))
    job_title = Column(String(80))
    link_to_job = Column(String(200))
    job_type = Column(String(120), default='')
    region = Column(String(100))
    salary = Column(String(100))
    timestamp = Column(DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'Job (id={self.id!r}, name={self.job_title!r}, portal={self.portal})'


Base.metadata.create_all(engine)

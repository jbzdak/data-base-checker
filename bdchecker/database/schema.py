import datetime

__author__ = 'jb'

from settings import ENGINE

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Binary, Boolean, DateTime

Base = declarative_base()

Session = sessionmaker(bind = ENGINE)


class Grade(Base):

    __tablename__ = 'grade'

    pk = Column(Integer, primary_key=True)

    date = Column(DateTime, default=datetime.datetime.now)

    instance = Column(String())

    user_id = Column(String())

    unit = Column(String())
    task = Column(String())

    submission_args = Column(String())
    submission_kwargs = Column(String())
    submission_metadata = Column(Binary())

    passed = Column(Boolean())
    grade = Column(Integer())


class PassCodes(Base):

    __tablename__ = 'pass'

    user_id = Column(String(), primary_key=True)
    user_password = Column(String())



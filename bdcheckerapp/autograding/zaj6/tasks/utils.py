# -*- coding: utf-8 -*-

from csv import reader, unix_dialect
from io import StringIO

from os import path

from subprocess import SubprocessError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, TIMESTAMP, FLOAT
from bdchecker.api import MultiUserSessionTest, SessionTest
from bdchecker.db_utils import load_script

CURRDIR = path.split(__file__)[0]

DATADIR = path.join(path.split(CURRDIR)[0], 'data')

Base = declarative_base()

class DataPointHistory(Base):
    __tablename__ = "DATA_POINT_HISTORY"

    data_source = Column(Integer(), primary_key=True)
    point_type = Column(Integer(), primary_key=True)
    date = Column(TIMESTAMP(), primary_key=True)
    insert_timestamp = Column(TIMESTAMP(), primary_key=True)
    value = Column(FLOAT(precision=64))

class DataPointCurrent(Base):
    __tablename__ = "DATA_POINT_CURRENT"

    data_source = Column(Integer(), primary_key=True)
    point_type = Column(Integer(), primary_key=True)
    date = Column(TIMESTAMP(), primary_key=True)
    #insert = Column(TIMESTAMP(), primary_key=True)
    value = Column(FLOAT(precision=64))

class DataPointCurrentView(Base):
    __tablename__ = "DATA_POINT_CURRENT_VIEW"

    data_source = Column(Integer(), primary_key=True)
    point_type = Column(Integer(), primary_key=True)
    date = Column(TIMESTAMP(), primary_key=True)
    #insert = Column(TIMESTAMP(), primary_key=True)
    value = Column(FLOAT(precision=64))

class OurDialect(unix_dialect):
    delimiter = ';'

def load_ds(session):
    session.execute('DELETE FROM "DATA_SOURCE";')
    with open(path.join(DATADIR, 'ds.csv')) as f:
        l = list(reader(f, OurDialect))
        r = iter(l)
        r.__next__() # SKIP header
        session.execute(
            'INSERT INTO "DATA_SOURCE"(id, name, abbreviation) VALUES '
            '(:id, :name, :abb)', [{"id":row[0], "name": row[1], 'abb': row[3]} for row in r]
        )

def load_pt(session):
    session.execute('DELETE FROM "POINT_TYPE";')
    with open(path.join(DATADIR, 'pt.csv')) as f:
        r = iter(reader(f, OurDialect))
        r.__next__() # SKIP header
        session.execute(
            'INSERT INTO "POINT_TYPE"(id, name, normalizable) VALUES '
            '(:id, :name, true)', [{"id":row[0], "name": row[1]} for row in r]
        )

def __random_table_id(session, table):
    res = session.execute('SELECT id from "{table}" ORDER BY random() LIMIT 1'.format(table=table))
    return res.first()[0]

def random_point_type(session):
    return __random_table_id(session, "POINT_TYPE")

def random_data_source(session):
    return __random_table_id(session, "DATA_SOURCE")

class Zaj6TaskChecker(SessionTest):

    dph = DataPointHistory

    dphc = DataPointCurrent
    dphcv = DataPointCurrentView

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.additional_output_list = []
        if not "script" in cls.kwargs:
            raise ValueError("Proszę podać skrypt stawiający bazę danych jako argument --script")
        try:
            load_result = load_script(StringIO(cls.kwargs['script']), cls.db_name, cls.db_name)
            pattern = '='*30 + '\nPSQL output\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + load_result.decode('utf-8') + pattern)
        except SubprocessError as e:
            pattern = '='*30 + '\nPSQL error\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + e.output.decode('utf-8') + pattern)


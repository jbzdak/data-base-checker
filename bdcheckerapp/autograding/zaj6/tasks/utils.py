# -*- coding: utf-8 -*-
from io import StringIO
from subprocess import SubprocessError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, TIMESTAMP, FLOAT
from bdchecker.api import MultiUserSessionTest, SessionTest
from bdchecker.db_utils import load_script

Base = declarative_base()

class DataPointHistory(Base):
    __tablename__ = "DATA_POINT_HISTORY"

    data_source = Column(Integer(), primary_key=True)
    point_type = Column(Integer(), primary_key=True)
    date = Column(TIMESTAMP(), primary_key=True)
    insert = Column(TIMESTAMP(), primary_key=True)
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


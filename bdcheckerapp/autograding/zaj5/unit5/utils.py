# -*- coding: utf-8 -*-
from io import StringIO
from subprocess import SubprocessError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from bdchecker.api import MultiUserSessionTest
from bdchecker.db_utils import load_script

Base = declarative_base()

class Users(Base):
    __tablename__ = "USERS"

    username = Column(String())
    is_admin = Column(Integer())
    password = Column(String())


class Zaj5TaskChecker(MultiUserSessionTest):

    ROLES = {
        "user": ["user"],
        "admin": ["admin"]
    }

    Users = Users

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not "script" in cls.kwargs:
            raise ValueError("Proszę podać skrypt stawiający bazę danych jako argument --script")
        try:
            load_script(StringIO(cls.kwargs['script']), cls.db_name, cls.db_name)
        except SubprocessError as e:
            cls.additional_output_list.append(e.output)


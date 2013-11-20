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

    username = Column(String(), primary_key=True)
    is_admin = Column(Integer())
    password = Column(String())

class UserList(Base):

    __tablename__ = "LIST_USERS"
    username = Column(String(), primary_key=True)


class Zaj5TaskChecker(MultiUserSessionTest):

    ROLES = {
        "user": ["user"],
        "admin": ["admin"]
    }

    Users = Users

    UserList = UserList

    def get_user(self, username, session=None):
        if session is None:
            session = self.session
        else:
            session = self.get_session(session)
        return session.query(self.Users).filter(self.Users.username==username).first()

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


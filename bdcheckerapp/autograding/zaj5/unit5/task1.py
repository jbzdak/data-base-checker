# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError, ProgrammingError
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):

        def test_has_table(self):
            self.assert_has_table("USERS", "Tabela \"USERS\" nie istnieje")

        def test_admin_can_insert_user(self):

            admin = self.get_session("admin")

            try:

                admin.add(self.Users(username="foo", is_admin=0, password="bar"))
                admin.add(self.Users(username="bar", is_admin=1, password="baz"))

                admin.flush()

            except Exception as e:
                raise  AssertionError("Użytkownikowi admin nie udało się dodać wierszy do tabeli USERS") from e

        def test_user_cant_insert_user(self):

            user = self.get_session("user")

            with self.assertRaises(ProgrammingError, msg="Użytkownikowi user udało się wstawić wiersz do tabeli USERS"):
                user.add(self.Users(username="foo", is_admin=0, password="bar"))
                user.flush()

        def test_user_cant_insert_admin(self):

            user = self.get_session("user")

            with self.assertRaises(ProgrammingError, msg="Użytkownikowi user udało się wstawić wiersz do tabeli USERS"):
                user.add(self.Users(username="foo", is_admin=1, password="bar"))
                user.flush()


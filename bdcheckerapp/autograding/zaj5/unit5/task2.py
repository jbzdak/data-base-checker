# -*- coding: utf-8 -*-
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql.expression import select
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker, UserList


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):

        def test_has_table(self):
            self.assert_has_table("USERS", "Tabela \"USERS\" nie istnieje")

        def test_view_is_empty_at_the_beginning(self):
            self.assertEqual(len(list(self.session.query(UserList.username))), 0,
                             msg="Widok \"LIST_USERS\" powinien być pusty zaraz po stworzeniu schematu")

        def test_user_exists_in_view_after_we_add_to_table(self):
            self.session.add(self.Users(username="foo", is_admin=0, password="bar"))
            self.assertEqual(list(self.session.query(self.UserList.username)), [("foo",)])


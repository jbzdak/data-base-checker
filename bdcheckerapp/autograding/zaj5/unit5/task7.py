# -*- coding: utf-8 -*-
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker, UserList

import crypt

class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):

        def test_has_procedura(self):
            self.assert_has_procedure("add_user")
            self.assert_has_procedure("check_password")


        def test_view_is_empty_at_the_beginning(self):
            self.assertEqual(len(list(self.session.query(UserList.username))), 0,
                             msg="Widok \"LIST_USERS\" powinien być pusty zaraz po stworzeniu schematu")

        def test_check_password(self):
            self.session.add(self.Users(username="foo", is_admin=1, password="bar"))
            self.session.flush()

            self.assertTrue(self.session.execute("SELECT check_password('foo', 'bar')").first()[0])
            self.assertFalse(self.session.execute("SELECT check_password('foo', 'baz')").first()[0])





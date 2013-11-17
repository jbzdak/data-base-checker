# -*- coding: utf-8 -*-
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker, UserList

import crypt

class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):


        def test_view_is_empty_at_the_beginning(self):
            self.assertEqual(len(list(self.session.query(UserList.username))), 0,
                             msg="Widok \"LIST_USERS\" powinien być pusty zaraz po stworzeniu schematu")

        def test_password_encoding(self):
            self.session.add(self.Users(username="foo", is_admin=1, password="bar"))
            self.session.flush()
            user = self.get_user("foo")
            self.assertEqual(crypt.crypt('bar', user.password), user.password)





# -*- coding: utf-8 -*-
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TaskChecker(Zaj5TaskChecker):

        def test_has_table(self):
            self.assert_has_table("USERS", "Tabela \"USERS\" nie istnieje")

        def test_admin_can_insert_user(self):

            admin = self.get_session("admin")

            admin.add(self.Users(username="foo", is_admin=0, password="bar"))
            admin.add(self.Users(username="bar", is_admin=1, password="baz"))

            admin.flush()


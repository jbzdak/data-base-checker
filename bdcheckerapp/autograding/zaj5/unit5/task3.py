# -*- coding: utf-8 -*-
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker, UserList


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):

        def test_has_procedure(self):
            self.assert_has_procedure("add_user")

        def test_view_is_empty_at_the_beginning(self):
            self.assertEqual(len(list(self.session.query(UserList.username))), 0,
                             msg="Widok \"LIST_USERS\" powinien być pusty zaraz po stworzeniu schematu")

        def test_user_role_can_add_users(self):
            user = self.get_session("user")
            try:
                user.execute("SELECT add_user('foo', 'bar');")
                user.flush()
            except Exception as e:
                raise AssertionError("Rola \"user\" nie mogła wywołać unkcji add_user") from e
            self.assertEqual(list(user.query(self.UserList.username)), [("foo",)], msg="Po wykonaniu metody add_user nie było użytkownika w bazie danych")

        def test_user_is_created_properly(self):
            self.session.execute("SELECT add_user('foo', 'bar');")
            self.assertEqual(
                list(self.session.query(self.Users.username, self.Users.is_admin)), [("foo", 0)],
                msg="Po stworzeniu użytkownika za pomocą add_user okazało się że nie został on stworzony poprawnie.")


# -*- coding: utf-8 -*-
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj5.unit5.utils import Zaj5TaskChecker, UserList


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj5TaskChecker):

        def test_has_procedura(self):
            self.assert_has_procedure("add_user")
            self.assert_has_procedure("change_user")

        def test_view_is_empty_at_the_beginning(self):
            self.assertEqual(len(list(self.session.query(UserList.username))), 0,
                             msg="Widok \"LIST_USERS\" powinien być pusty zaraz po stworzeniu schematu")

        def test_user_role_can_add_users(self):
            user = self.get_session("user")
            try:
                user.execute("SELECT add_user('foo', 'bar');")
                user.execute("SELECT change_user('foo', 'baz');")
                user.flush()
            except Exception as e:
                raise AssertionError("Rola \"user\" nie mogła wywołać unkcji change_user") from e
            self.assertEqual(list(user.query(self.UserList.username)), [("foo",)], msg="Po wykonaniu metody add_user nie było użytkownika w bazie danych")

        def test_password_is_changes(self):
            self.session.execute("SELECT add_user('foo', 'bar');")
            self.session.flush()
            pass_before = self.get_user('foo').password
            self.session.execute("SELECT change_user('foo', 'baz');")
            pass_after = self.get_user('foo').password
            self.session.flush()
            self.assertFalse(pass_before == pass_after, "Change password nie zmieniło hasła")

        def test_cant_change_admin_user(self):
            self.session.add(self.Users(username="foo", is_admin=1, password="bar"))
            self.session.flush()
            with self.assertRaises(Exception, msg="Program nie zgłosił błędu po próbie zmiany hasła administratora"):
                self.session.execute("SELECT del('foo', 'baz');")
                self.session.flush()



from sqlalchemy.orm import Query
from bdchecker.api import SessionTest
from units.unit3.meta.data import TAGS
from units.unit3.meta.orm import Tag

__author__ = 'jb'

from .util import NewDatabaseTaskChecker, Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 1

    display_stdout = False

    class TestSuite(Zaj3TestSuite):

        def test_tag_table_exists(self):
            list(Query(Tag, self.session))

        def test_tag_table_contents(self):
            result = list(Query(Tag, self.session).order_by("key"))
            self.assertEqual(result, TAGS)




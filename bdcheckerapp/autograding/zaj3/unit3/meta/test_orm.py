import unittest
import uuid
from sqlalchemy.orm import sessionmaker, Query
from bdchecker import db_utils
from bdchecker.api import SessionTest
import settings
from units.unit3.meta import orm
from units.unit3.meta.orm import Student, Tag



__author__ = 'jb'




class TestBase(unittest.TestCase):
    CLEANUP = True

    # @classmethod
    # def setUpClass(cls):
    #     cls.create_db("task2-" + str(uuid.uuid4()))

    @classmethod
    def create_db(cls, db):
        cls.db = db
        db_utils.drop_database(cls.db, ignore_exists=True)
        db_utils.drop_user(cls.db, ignore_exists=True)
        db_utils.create_user(cls.db, cls.db)
        db_utils.create_database(cls.db, cls.db)
        cls.engine = settings.create_engine_for(cls.db, cls.db, cls.db)


    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
        if cls.CLEANUP:
            db_utils.drop_database(cls.db)
            db_utils.drop_user(cls.db)

# class TestOrmCreation(TestBase):
#
#
#
#     def test_creation(self):
#         orm.Base.metadata.create_all(self.engine)



class TestOrm(TestBase, SessionTest):

    @classmethod
    def setUpClass(cls):
        cls.create_db("task2-" + str(uuid.uuid4()))
        super().setUpClass()
        orm.Base.metadata.create_all(cls.engine)

    def test_create_invalid_student(self):
        stud = Student()
        stud.name = "foo"
        stud.surname = "bar"
        stud.gender = 'da'
        stud.message = "das"
        stud.status = 12
        self.session.add(stud)
        self.session.flush()

class TestSchema(TestBase, SessionTest):

    CLEANUP = False

    ROLLBACK = False

    @classmethod
    def setUpClass(cls):
        cls.create_db("task2-test_schema")
        super().setUpClass()
        orm.Base.metadata.create_all(cls.engine)

    def test_create_tags(self):
        from units.unit3.meta.data import TAGS
        for t in TAGS:
            self.session.add(t)
        self.session.flush()

        result = list(Query(Tag, self.session).order_by("key"))

        self.assertEqual(result, TAGS)





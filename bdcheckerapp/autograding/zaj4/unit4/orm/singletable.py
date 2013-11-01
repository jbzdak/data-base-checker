
from sqlalchemy import Column, String, SmallInteger, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

SingleTableBase = declarative_base()


class Tag(SingleTableBase):
    __tablename__ = "TAG"
    # id = Column(Integer(), primary_key=True)
    key = Column(String(), primary_key=True)
    label = Column(String())

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __eq__(self, other):
        return self.key == other.key and self.label == other.label

    def __str__(self):
        return "{}:{}".format(self.key, self.label)

    __repr__ = __str__

    __unicode__ = __str__


class Student(SingleTableBase):
    __tablename__ = "STUDENT"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    surname = Column(String())
    gender = Column(SmallInteger())
    status = Column(String(), ForeignKey("TAG.key"))
    message = Column(String())


class Pracownik(SingleTableBase):
    __tablename__ = "PRACOWNIK"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    surname = Column(String())
    gender = Column(SmallInteger())
    tel_no = Column(String())


class PracaDyplomowa(SingleTableBase):
    __tablename__ = "PRACA_DYPLOMOWA"
    tytul = Column(String(), nullable=False)
    type = Column(String(), ForeignKey("TAG.key"), primary_key=True)
    student_id = Column(Integer(), ForeignKey("STUDENT.id"), nullable=False, primary_key=True)
    promotor_id = Column(Integer(), ForeignKey("PRACOWNIK.id"), nullable=True)


class Osoba(SingleTableBase):
    __tablename__ = "OSOBA"
    id = Column(Integer(), primary_key=True)
    type = Column(String(), ForeignKey("TAG.key"), nullable=False)
    name = Column(String())
    surname = Column(String())
    gender = Column(SmallInteger())
    status = Column(String(), ForeignKey("TAG.key"))
    message = Column(String())
    tel_no = Column(String())


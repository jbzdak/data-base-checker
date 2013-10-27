from contextlib import contextmanager
import datetime

__author__ = 'jb'

from .schema import Session, PassCodes, Grade
import hashlib

# class NoSuchUserException(Exception): pass
#
# class InvalidPassword(Exception): pass
#
# class InvalidSupervisorPassword(Exception): pass

@contextmanager
def with_session():
    s = Session()
    try:
        yield s
        s.commit()
    finally:
        s.close()


def check_supervisor_password(supervisor_pass):
    with with_session() as session:
        supervisor = session.query(PassCodes).get('007')
        if not supervisor.user_password == supervisor_pass:
            raise ValueError("Invalid supervisor password")


def set_password(user_id, supervisor_pass, password):
    with with_session() as session:
        if user_id == "007":
            raise ValueError("No such user")
        user = session.query(PassCodes).get(user_id)
        check_supervisor_password(supervisor_pass)
        if user is None:
            user = PassCodes()
            user.user_id = user_id
        user.user_password = password
        session.add(user)


def check_password(user_id, password, unit_id=None):
    if user_id is None:
        return
    with with_session() as session:
        user = session.query(PassCodes).get(user_id)
        if user is None:
            raise ValueError("No such user")

        if user.user_password != password:
            try:
                if unit_id:
                    date = password["date"]
                    digest = password["digest"]
                    hasher = hashlib.sha256()
                    key = "{}.{:%Y-%m-%d}.{}".format(unit_id, date,
                                                     user.user_password)
                    hasher.update(key.encode("utf-8"))
                    if datetime.date.today() - date > datetime.timedelta(days=3):
                        raise ValueError
                    if hasher.hexdigest() == digest:
                        return
            except (KeyError, ValueError):
                pass
            raise ValueError("Password invalid fr user {}".format(user_id))


def _save_single_grade(session, user_id, unit, task, passed, grade, data_pack):
    g = Grade()
    g.user_id = user_id
    g.unit = unit
    g.task = task
    g.instance = data_pack.instance
    g.passed = passed
    g.grade = grade
    g.submission_args = str(data_pack.args)
    g.submission_kwargs = str(data_pack.kwargs)
    session.add(g)


def save_grade(user_id_1, user_id_2, unit, task, passed, grade, data_pack):
    with with_session() as s:
        _save_single_grade(s, user_id_1, unit, task, passed, grade, data_pack)
        if user_id_2 is not None:
            _save_single_grade(s, user_id_2, unit, task, passed, grade, data_pack)

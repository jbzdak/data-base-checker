from getpass import getuser
from io import StringIO
import os
from tempfile import gettempdir
import uuid
from sqlalchemy.exc import ProgrammingError
from django.conf import settings
from contextlib import contextmanager
import subprocess

@contextmanager
def connect(using=settings.SCHEMA_CHECKER_ENGINE, auto_commit=None):
    conn = using.connect()
    if auto_commit:
        conn.connection.set_session(autocommit=True)
    try:
        yield conn
    finally:
        conn.close()

def create_role(name, password):
    with connect(using=settings.SCHEMA_CHECKER_ENGINE, auto_commit=True) as conn:
        conn.execute('CREATE USER "{}" PASSWORD \'{}\''.format(name, password))

def drop_role(name, ignore_exists = False):
    try:
        with connect(using=settings.SCHEMA_CHECKER_ENGINE, auto_commit=True) as conn:
            conn.execute('DROP ROLE "{}"'.format(name))
    except ProgrammingError:
        if not ignore_exists:
            raise

def create_database(name, owner = None):
    with connect(using=settings.SCHEMA_CHECKER_ENGINE, auto_commit=True) as conn:
        if owner:
            conn.execute('CREATE DATABASE "{}" OWNER "{}"'.format(name, owner))
        else:
            conn.execute('CREATE DATABASE "{}"'.format(name))


def drop_database(name, ignore_exists=False):
    try:
        with connect(using=settings.SCHEMA_CHECKER_ENGINE, auto_commit=True) as conn:
            conn.execute('DROP DATABASE "{}"'.format(name))
    except ProgrammingError:
        if not ignore_exists:
            raise

GRANT_ALL_SCRIPT = """
GRANT ALL ON ALL TABLES IN SCHEMA public TO "{username}";
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "{username}";
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO "{username}";
"""

def load_script(script_file_name, database_name, change_owner_to=None):
    del_script_file = False
    try:
        if isinstance(script_file_name, StringIO):
            file = os.path.join(gettempdir(), str(uuid.uuid4()))
            del_script_file = True
            with open(file, 'w') as f:
                script_file_name.seek(0)
                f.write(script_file_name.read())
            script_file_name = file
        call = ['psql','-Ppager=off', '-qnte', '-f', script_file_name, database_name]
        print(call)
        subprocess.check_output(call)
    finally:
        try:
            if del_script_file:
                os.remove(script_file_name)
        except Exception:
            pass

    if change_owner_to is not None:
        load_script(StringIO(GRANT_ALL_SCRIPT.format(username=change_owner_to)),
                    database_name, None)


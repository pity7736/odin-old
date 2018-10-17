import subprocess

from pytest import fixture

from src import settings


@fixture(scope='session')
def create_db():
    print('creating database...')
    sql_file = f'{settings.ROOT_DIR}/create_db.sql'
    subprocess.call(['psql', '-U', settings.DB_USER, '-h', settings.DB_HOST, '-f', sql_file])

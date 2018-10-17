import subprocess

from pytest import fixture


@fixture(scope='session')
def create_db():
    print('creating database...')
    sql_file = '/home/pity/development/odin/create_db.sql'
    subprocess.call(['psql', '-U', 'odin', '-h', 'localhost', '-f', sql_file])

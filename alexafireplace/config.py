import os

basedir = os.path.abspath(os.path.dirname(__file__))


with open('{}/secret_key.txt'.format(basedir), 'r') as f:
    SECRET_KEY = f.read()[:-1]

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(basedir, 'fireplace.db'))

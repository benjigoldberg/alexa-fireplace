import os

basedir = os.path.abspath(os.path.dirname(__file__))


with open('{}/secret_key.txt'.format(basedir), 'rb') as f:
    SECRET_KEY = f.read()

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(basedir, 'fireplace.db'))

"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
from os import getenv

from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from instance import ENVIRONMENTS
from myapp import create_app, db

ENV = getenv('BUCKETLIST_ENV') or 'development'
APP = create_app(ENVIRONMENTS.get(ENV))

MIGRATE = Migrate(APP, db)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

if __name__ == '__main__':
    MANAGER.run()

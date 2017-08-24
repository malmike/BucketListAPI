"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
from os import getenv, path
from sys import argv
from unittest import TestLoader, TextTestRunner
from coverage import Coverage
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
import nose

from instance import ENVIRONMENTS
from myapp import create_app, db

ENV = getenv('BUCKETLIST_ENV') or 'development'


if len(argv) > 1 and argv[1] == "nosetests":
    ENV = "testing"


APP = create_app(ENVIRONMENTS.get(ENV))
COV = Coverage(
    branch=True,
    include='myapp/*',
    omit=[
        'tests/*',
        'instance/*',
        'manage.py'
    ]
)


MIGRATE = Migrate(APP, db)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)


@MANAGER.command
def testing():
    """
    Calls run_tests method which runs the tests
    """
    if run_tests():
        return 0
    return 1


@MANAGER.add_command
class NoseCommand(Command):
    """
    Class enables running of tests using nose tests and basing on the
    arguments passed will generate a coverage report and coverage xml file
    """
    name = 'nosetests'
    capture_all_args = True

    def run(self, arguments):
        if not arguments:
            nose.main(argv=['tests'])
        else:
            nose.main(argv=arguments)


if __name__ == '__main__':
    MANAGER.run()

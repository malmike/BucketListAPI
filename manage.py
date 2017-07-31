"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
from os import getenv, path
from sys import argv
from unittest import TestLoader, TextTestRunner
from coverage import Coverage
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from instance import ENVIRONMENTS
from myapp import create_app, db

ENV = getenv('BUCKETLIST_ENV') or 'development'

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
    Calls and runs the tests
    """
    tests = TestLoader().discover('tests', pattern='test*.py')
    result = TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@MANAGER.command
def test_coverage():
    """
    Runs tests with coverage
    """
    COV.start()
    tests = TestLoader().discover('tests', pattern='test*.py')
    result = TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        COV.use_cache(True)
        COV.stop()
        COV.save()
        print('Coverage report:')
        COV.report()
        basedir = path.abspath(path.dirname(__file__))
        covdir = path.join(basedir, 'htmlcov')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.xml_report()
        return 0
    return 1


if __name__ == '__main__':
    MANAGER.run()

"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
import os
import sys
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from instance import ENVIRONMENTS
from myapp import create_app, db


ENV = os.getenv('BUCKETLIST_ENV') or 'development'
app = create_app(ENVIRONMENTS.get(ENV))

COV = coverage.Coverage(
    branch = True,
    include = 'myapp/*',
    omit = [
        'tests/*',
        'instance/*'
    ]
)


MIGRATE = Migrate(app, db)
MANAGER = Manager(app)
MANAGER.add_command('db', MigrateCommand)


@MANAGER.command
def testing():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@MANAGER.command
def test_coverage():
    COV.start()
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        COV.use_cache(True)
        COV.stop()
        COV.save()
        print('Coverage report:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.xml_report()
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    MANAGER.run()

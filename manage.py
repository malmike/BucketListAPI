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

ERR_STRING = """\n\tOption not provided
        Enter: 'python manage.py --help'
        to get list of available options
        """

try:
    if sys.argv[1] and sys.argv[1] in ENVIRONMENTS:
        app = create_app(ENVIRONMENTS.get(sys.argv[1]))
    elif sys.argv[1] and sys.argv[1] == '--help':
        print ('\n\nUsage:')
        print ('\t"python run.py <environment>"')
        print ('\t\tEnvironment Options:\n\t\t\t development \n\t\t\t production \n\t\t\t testing')
        exit()
    else:
        print (ERR_STRING)
        exit()

except IndexError:
    print (ERR_STRING)
    exit()

COV = coverage.Coverage(
    branch = True,
    include = 'myapp',
    omit = [
        'tests/*',
        'instance/*'
    ]
)


MIGRATE = Migrate(app, db)
MANAGER = Manager(app)
MANAGER.add_command('db', MigrateCommand)

@MANAGER.command
def development():
    app.run()

@MANAGER.command
def testing():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@MANAGER.command
def cov():
    COV.start()
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity = 1).run(tests)
    if result.wasSuccessful():
        COV.use_cache(True)
        COV.stop()
        COV.save()
        # print('Coverage report:')
        # COV.report()
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # covdir = os.path.join(basedir, 'tmp/coverage')
        # COV.html_report(directory=covdir)
        # print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    MANAGER.run()

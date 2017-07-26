"""
Script contains commands that can be called from the command line
to a Manager instance, for the flask application
"""
import sys
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from instance import environments
from myapp import create_app, db

err_string = """\n\tOption not provided
        Enter: 'python manage.py --help'
        to get list of available options
        """

try:
    if sys.argv[1] and sys.argv[1] in environments:
        app = create_app(environments.get(sys.argv[1]))
    elif sys.argv[1] and sys.argv[1] == '--help':
        print ('\n\nUsage:')
        print ('\t"python run.py <environment>"')
        print ('\t\tEnvironment Options:\n\t\t\t development \n\t\t\t production \n\t\t\t testing')
        exit()
    else:
        print (err_string)
        exit()

except IndexError:
    print (err_string)
    exit()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def development():
    app.run()

@manager.command
def testing():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()

"""
File used to start the application
"""
from os import getenv

from instance import ENVIRONMENTS
from myapp import create_app

env = getenv('BUCKETLIST_ENV') or 'development'
app = create_app(ENVIRONMENTS.get(env))

if __name__ == '__main__':
    app.run()
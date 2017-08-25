# BucketListAPI
[![Codeship Status for malmike/BucketListAPI](https://app.codeship.com/projects/77766f50-54e4-0135-1058-2a73e0087811/status?branch=master)](https://app.codeship.com/projects/235425)
[![Coverage Status](https://coveralls.io/repos/github/malmike/BucketListAPI/badge.svg?branch=master)](https://coveralls.io/github/malmike/BucketListAPI?branch=master)
[![Code Health](https://landscape.io/github/malmike/BucketListAPI/master/landscape.svg?style=flat)](https://landscape.io/github/malmike/BucketListAPI/master)
[![Code Climate](https://codeclimate.com/github/malmike/BucketListAPI/badges/gpa.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Issue Count](https://codeclimate.com/github/malmike/BucketListAPI/badges/issue_count.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/057f34a9f5374707b86d72378320f2ba)](https://www.codacy.com/app/malmike/BucketListAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=malmike/BucketListAPI&amp;utm_campaign=Badge_Grade)

This is an API for a bucket list designed using flask framework for python

### Set up
You should have [git](https://git-scm.com/), [python](https://docs.python.org/), [pip](https://pypi.python.org/pypi/pip), [postgresql](https://www.postgresql.org/docs/current/static/tutorial.html), [virtualenv](https://virtualenv.pypa.io/en/stable/) installed
##### These instractions are specific to a linux or unix based machine
1. Open your terminal
2. Clone the project using `git clone https://github.com/malmike/BucketlistAPI`
3. Run `createdb bucketlist_api_dev` and `create test_db`
4. Change to the project directory using `cd BucketlistAPI`
5. Create a virtual environment for the project using the command `virtualenv .venv` and start it using `source .venv/bin/activate` and using the command `deactivate` to stop the virtual environment
6. Install packages using `pip install -r requirements.txt`
7. You can run tests using the command `nosetests tests --with-coverage --cover-erase --cover-package="myapp" --cover-package="instance" --cover-xml`
8. To launch the application you should first apply migrations in order to create the database whose process is shown below
9. Run the application using `python manage.py runserver`
10. You can access the api documentation at `http://localhost:5000/api/v1`

### Command for creation of the database and applying migrations to it
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py db --help


### Specifications for the API are shown below

| EndPoint | Functionality | Public Access |
| -------- | ------------- | ------------- |
| [ POST /auth/login ](#) | Logs a user in | FALSE |
| [ POST /auth/register ](#) | Register a user | FALSE |
| [ POST /auth/logout ](#) | Logs a user out | TRUE |
| [ POST /bucketlists/ ](#) | Create a new bucket list | TRUE |
| [ GET /bucketlists/ ](#) | List all the created bucket lists | TRUE |
| [ GET /bucketlists/\<id> ](#) | Get single bucket list | TRUE |
| [ PUT /bucketlists/\<id> ](#) | Update this bucket list | TRUE |
| [ DELETE /bucketlists/\<id> ](#) | Delete this single bucket list | TRUE |
| [ POST /bucketlists/\<id>/items/ ](#) | Create a new item in bucket list | TRUE |
| [ PUT /bucketlists/\<id>/items/<item_id> ](#) | Update a bucket list item | TRUE |
| [ DELETE /bucketlists/\<id>/items/<item_id> ](#) | Delete an item in a bucket list | TRUE |
| [ GET /bucketlists?limit=\<number> ](#) | Gets a number of bucket lists relative to the value passed in number. Maximum records is 100 | TRUE |
| [ GET /bucketlists?q=\<bucketlist_name> ](#) | Search for bucket list with the same name as that passed in bucketlist_name | TRUE |

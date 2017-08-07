# BucketListAPI
[![Codeship Status for malmike/BucketListAPI](https://app.codeship.com/projects/77766f50-54e4-0135-1058-2a73e0087811/status?branch=master)](https://app.codeship.com/projects/235425)
[![Test Coverage](https://codeclimate.com/github/malmike/BucketListAPI/badges/coverage.svg)](https://codeclimate.com/github/malmike/BucketListAPI/coverage)
[![Code Health](https://landscape.io/github/malmike/BucketListAPI/master/landscape.svg?style=flat)](https://landscape.io/github/malmike/BucketListAPI/master)
[![Code Climate](https://codeclimate.com/github/malmike/BucketListAPI/badges/gpa.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Issue Count](https://codeclimate.com/github/malmike/BucketListAPI/badges/issue_count.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/057f34a9f5374707b86d72378320f2ba)](https://www.codacy.com/app/malmike/BucketListAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=malmike/BucketListAPI&amp;utm_campaign=Badge_Grade)

This is an API for a bucket list designed using flask framework for python

### Command for creation of the database and applying migrations to it
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py db --help


### Specifications for the API are shown below

| EndPoint | Functionality |
| -------- | ------------- |
| [ POST /auth/login ](#) | Logs a user in |
| [ POST /auth/register ](#) | Register a user |
| [ POST /bucketlists/ ](#) | Create a new bucket list |
| [ GET /bucketlists/ ](#) | List all the created bucket lists |
| [ GET /bucketlists/\<id> ](#) | Get single bucket list |
| [ PUT /bucketlists/\<id> ](#) | Update this bucket list |
| [ DELETE /bucketlists/\<id> ](#) | Delete this single bucket list |
| [ POST /bucketlists/\<id>/items/ ](#) | Create a new item in bucket list |
| [ PUT /bucketlists/\<id>/items/<item_id> ](#) | Update a bucket list item |
| [ DELETE /bucketlists/\<id>/items/<item_id> ](#) | Delete an item in a bucket list |
| [ GET /bucketlists?limit=\<number> ](#) | Gets a number of bucket lists relative to the value passed in number. Maximum records is 100 |
| [ GET /bucketlists?q=\<bucketlist_name> ](#) | Search for bucket list with the same name as that passed in bucketlist_name |

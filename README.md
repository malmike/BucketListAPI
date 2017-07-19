# BucketListAPI
[![Build Status](https://travis-ci.org/malmike/BucketListAPI.svg?branch=master)](https://travis-ci.org/malmike/BucketListAPI)
[![Coverage Status](https://coveralls.io/repos/github/malmike/BucketListAPI/badge.svg?branch=master)](https://coveralls.io/github/malmike/BucketListAPI?branch=master)
[![Code Health](https://landscape.io/github/malmike/BucketListAPI/master/landscape.svg?style=flat)](https://landscape.io/github/malmike/BucketListAPI/master)
[![Code Climate](https://codeclimate.com/github/malmike/BucketListAPI/badges/gpa.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Issue Count](https://codeclimate.com/github/malmike/BucketListAPI/badges/issue_count.svg)](https://codeclimate.com/github/malmike/BucketListAPI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/057f34a9f5374707b86d72378320f2ba)](https://www.codacy.com/app/malmike/BucketListAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=malmike/BucketListAPI&amp;utm_campaign=Badge_Grade)

This is an API for a bucket list designed using flask framework for python

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

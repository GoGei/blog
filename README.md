# Simple blog project
## Project to train in DRF and JS AJAX

## Features

- Use django rest framework as backend
- Access to DRF via jquery
- Render html particles with js data and django render views
- Fab commands are provided
- Swagger and redoc documentation is provided

## Installation
Setup environment
```sh
cd blog
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Create local config file
```sh
mkdir config
cd config/
touch __init__.py local_settings.py
```
Example of local_settings.py
```sh
from settings import *  # important

SECRET_KEY = 'your key'

DATABASES['default']['NAME'] = '<db_name>'        # redefine if necessary
DATABASES['default']['USER'] = '<db_user_name>'   # redefine if necessary
DATABASES['default']['PASSWORD'] = '<db_user_password>'

# url options
SITE_URL = 'blog.local' # specify site base url
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = '1131'  # specify port if necessary 
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

# debug options
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
```
Create database
```sh
sudo su postgres
psql
CREATE USER <db_user_name> WITH ENCRPPTED PASSWORD '<db_user_password>' superuser;
CREATE DATABASE <db_name> WITH OWNER <db_user_name> ENCODING 'UTF8';
```
Set hosts
```sh
sudo vim /etc/hosts
127.0.0.1               <SITE_URL>
127.0.0.1           api.<SITE_URL>
```
example
```sh
127.0.0.1               blog.local
127.0.0.1           api.blog.local
```

# Useful fab commands
**fab runserver** - start server \
**fab dump_db** - dump current database to .sql script in dumps/ folder \
**fab restore_db** - restore last found .sql file in dumps/ folder to EMPTY database \
**fab deploy_local** - deploy project
- branch (main by default)
- git checkout and pull from the branch
- install requirements.txt
- migrate database
- collect static

**fab check** - scan code in project \
**fab create_graph_models** - create class diagram of the project to graphs/ \
- parameters: Classes to display in .dot file \
- parameters example: fab create_graph_models:User,Post,PostLike

# Useful scripts
## fill_db_with_test_data

command: `./manage.py fill_db_with_test_data -c <bool> -uc <int> -cc <int> -pc <int> -mc <int> -plc <int> -clc <int>` \
example: `./manage.py fill_db_with_test_data -c True -uc 10 -cc 8 -pc 6 -mc 4 -plc 4 -clc 11` \
output:
> DB cleaned \
> Successfully filled in DB  \
> Categories: 8 \
> Users: 13 \
> Posts: 480 \
> Comments: 1920

**-c** - clean_db - if True remove all Posts, Comments and related objects like Likes and Comments. \
Also clean Users that are not staff and superusers. \
**-uc** - user_counter - how many not staff and superuser users to create \
**-cc** - category_counter - how many categories to create \
**-pc** - post_counter - how many posts create per categories for each user \
**-mc** - comments_counter - how many comments create for each post \
**-plc** - post_like_counter - each nth post will be liked \
**-clc** - comment_like_counter - each nth comment will be liked \

## clear_db

command: `./manage.py clear_db -s <bool> -u <bool>` \
example: `./manage.py clear_db -s True -u True` \
output:
> DB cleaned Posts and Categories with related objects \
> DB cleaned Users with filter {'is_staff': True, 'is_superuser': True}

# API
Base URL: http://api.<SITE_URL>:<HOST_PORT>
### DRF url
pattern: Base URL/v1/ \
example: http://api.blog.local:1131/v1/
### Swagger
pattern: Base URL/swagger/ \
example: http://api.blog.local:1131/swagger/
### Swagger
pattern: Base URL/redoc/ \
example: http://api.blog.local:1131/redoc/

# Toolbar
Add this to config/local_settings.py
```sh
# toolbar options
DEBUG_TOOLBAR = True
if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

# Testing
Constants needed to set up: \
Required: \
DATABASE_TEST_NAME=<db_for_test_name> \
DATABASE_TEST_USER=<db_for_test_user_name> \
DATABASE_TEST_PSW=<db_for_test_user_password> \
Optional: \
DATABASE_TEST_HOST=<db_host> (localhost by default) \

### Tests counter: **101**
### Files coverage: **90%**
### Lines coverage: **96%**
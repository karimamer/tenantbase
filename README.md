# tenantbase
Stack of choice
===================
* Programming Language Python 3.7
* memcahe
* sqllite
* aiohttp
* svelte
* aiosqlite

### Decision making

##### Programming Language:
I choose python over other Languages Due to
  * familiarity
  * fast iteration
  * Mature web echo system

##### Data Store:
I choose memcahce and sqlite to meet the challenge

#### web framework:
I choose aiohttp
  * aysnc first
  * can scale easily to a million user https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
  * lightweight
  * easy to use and iterate on

Structure
===============
```
(level one)
TenatBase ---|  (level two A)
|            |-> TenatBase -|(level three)
|            |              |-> __init__.py
|            |              |-> main.py
|            |              |-> tbase_cache.db  
|            |              |-> web.py
|            |              |-> interfaces ->|(level 4)
|            |                               |->sql_interface.py
|            |                               |-> memcache_interface.py
|            |                               |-> __init__.py
|            |
|            |-> poetry.lock
|            |-> pyproject.toml
|            |
|            |
|            |(level two B)
|            |-> tests  ->|
|                         |-> init.py
|-> README.md             |-> test_tenatbase.py
|-> .flake8
|-> .pre-commit-config.yaml
|-> .pyproject.toml
```
#### Folder structure
##### TenatBase

is the head folder

##### Level one
**TenatBase**

* READ.md
* .pyproject.toml -> black formatter config
* .pre-commit-config.yaml
* .flake8 -> flake8 config

##### Level two A
**TenatBase**

* TenatBase folder containg The app
* Folder to contain tests unfrotently i didnt' get to write any
* poetry.lock contains my packages
* pyproject.toml contains poetry config

##### level two B
**tests*
* init.py
* test_tenatbase.py

##### level 3

* __init__.py
* main.py contains the code to run the CMD
* tbase_cache.db sqldb sqldatabase
* web.py run tofire up the server
* interfaces folder that contains all interfaces with 3 party systems

##### level 4

* sql_interface.py code that interfaces with sqllite
* memcache_interface.py code that interfaces with memcahce
* __init__.py


Installation
====================
*  install sqlite
*  install memcache
*  Install poetry https://poetry.eustace.io/
*  run poetry install
*  run poetry shell
* start memcache
* python run main to run cmd
* run python web.py to run webserver 

Code Doc
================


### Models
#### key value Table
 * id -> UUID Field
 * key  -> timestamp
 * value -> timestamp

### interfaces
```
* sql interface that contains 4 functions 
                                        | -> get_value_from_sql
                                        | -> delete_value_from_sql
                                        | -> insert_value_into_sql
                                        | -> get_all_values
* memcache interace that contains four function
                                        | -> set_memcahce
                                        | -> get_from_memcahce
                                        | -> delete_from_memcahce
```
### web
```
 contains web views
                    | -> health_check -> to check if the service is running 
                    | -> get_value -> get on value for a givien key
                    | -> set_value -> add key and value pair 
                    | -> delete_value - > delete from sql and memecahe
                    | -> get_values -> get all value in cache 
```


URLS
================
### Create key value pair
POST http://127.0.0.1:800/set-value
Body ex -> {"key":"code", "value":"test}

### GET value
GET http://127.0.0.1:8000/get-value
Body ex -> {"key":"code"}

### delete value
Delete http://127.0.0.1:8000/delete-value

### get all key and values 
GET  http://127.0.0.1:8000/get-values


# how to scale 
====================

to scale we will need to answer some questions firt ?
* Does the database of choice support fast key access ?
* is the database able to handle the amount of data we plan to store ?
* how many read and writes we are planning to do on a single node ?
* how do we expand the cluster given expected growth ?
* what is the maintaince process ?

After answering these questions we will be able to choose the right database for our needs 

I choose aiohttp since it can scale to a million requests easily
we will need to use a better logging tool like sentry 
we will need of course to add it our CI//CD

Things I could have done better
================================
* better project planning 
* url name scheme may feel inconsistent
* add tests

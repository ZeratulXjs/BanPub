# BanPub

A demo API for archiving banana cultivars in a germplasm

## Usage info

This an API written in python using the Flask-RESTPlus framework. It uses PostgreSQL for data persistence.

Users can submit and view submitted cultivar entries in the database (CRUD functionality).

Development was on Ubuntu 18.04 using Python 3.6.
Updates on Windows 10 using Python 3.6

yoooo

The API uses the following core dependencies/modules;

```linux
Python 3.6
Flask
Flask-RESTPlus
SQLAlchemy
PostgreSQL

```

The complete list of dependencies and their versions can be found in the `requirements.txt` file.

## Running the API

1; Clone this repo to a local directory;

`clone https://github.com/ZeratulXjs/BanPub.git`

2; Install PostgreSQL. Add a new system user and create the Postgres database that the API will use;
    You can change the password to whatever you like, then change it in the banApi.py app too.

```
user@acc:~/BanPub$ sudo apt -y install postgresql postgresql-contrib

user@acc:~/BanPub$ sudo -i -u postgres psql

postgres=# CREATE USER ***** WITH PASSWORD '*****';

postgres=# CREATE DATABASE ***** OWNER *****;

\q
```

3; Create a virtual environment to take advantage of sandboxing and other (newer) versions of Python. Install pip first if you don't have it.

```linux
user@acc:~/BanPub$ sudo apt-get install python-pip python-dev build-essential

user@acc:~/BanPub$ sudo pip install --upgrade pip

user@acc:~/BanPub$ sudo pip install --upgrade virtualenv

user@acc:~/BanPub$ virtualenv -r python3.6 venv-3.6

user@acc:~/BanPub$ source venv-3.6/bin/activate

(venv-3.6) user@acc:~/BanPub$
```

4; Once the bash (terminal) prompt shows the virtual environment is running, install the API dependencies from the requirements file.

```linux
(venv-3.6) user@acc:~/BanPub$ pip install -r requirements.txt
```

5; Now the API can be tested out. 

Since it uses Flask-RESTplus, it's self documenting and can be tested in the browser, no need for Postmaan.

Enjoy!

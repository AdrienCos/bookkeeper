# Bookkeeper

This is the SQLAlchemy code used to interface Sentinel to its database

## Installing

This library is not intended to be installed and used as standalone, it should only be done to modify it.

* Create a new virtual environment: `virtualenv venv`
* Activate it: `source venv/bin/activate`
* Install the libary in development mode: `pip install -e .`

## Usage

* Make sure you have an accessible SQL database (e.g. a local Postgres instance)
* Import the `bookkeeper.sql.create_session()` function
* Create a new session with this function, by passing it the URL of your database (see [here](https://docs.sqlalchemy.org/en/13/core/engines.html) for more info on that) with `session = create_session($URL)`
* Query the information you need with the functions in `bookkeeper.helpers`

## Structure

This library uses [SQLAlchemy](https://www.sqlalchemy.org/) to inteface with any SQL database you are using. It is split into two files:

* `sql.py` is in charge of defining the SQL schema, the different tables, their fields, and their relationships.
* `helpers.py` provides a set of high-level functions that perform queries to retrieve the information you want. If these functions do not meet all your needs, you can create new ones and add them to the library.
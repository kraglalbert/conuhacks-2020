# conuhacks-2020

## Setup

A virtual environment can be created with either `virtualenv` (python 2) or `venv` (python 3). For `venv`:

```
python3 -m venv env

source env/bin/activate 
```

The second line activates the virtual environment, and you can type `deactivate` to exit the environment. 

To install dependencies from a `requirements.txt` file, do this:

```
pip install -r /path/to/requirements.txt
```

To see all installed modules:

```
pip list
```

Generate a requirements.txt file by running this command:

```
pip freeze > requirements.txt
```

Run a database migration:

```
python manage.py db migrate -m "migration details"

python manage.py db upgrade
```

Fix an issue where DB is not synced with proper migration:

https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date

## Features

* Categories for different activities
* Employees can host events for other employees in their company
* Coffee dates

Domain model:

* User
* Event (location, category, name, description, tags, host[User], attendees[User], company[Company])
* Category [enum]
* Company

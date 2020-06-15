# ddapp

## Set up the app

Make sure Python 3 and [psycopg2](https://pypi.org/project/psycopg2/) are installed.

Set up a containerized instance of PostgreSQL:

```
docker run -d -p 5432:5432 -e PG_USER=devuser -e PG_PASSWORD=password -e PG_DATABASE=ddapp --name=ddapp crunchydata/crunchy-postgres-appdev
```

If you have a SQL script to implement the database schema check that `devuser` is the schema owner.
 
Otherwise execute these statements after setting up the database:
```
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO devuser;
GRANT ALL PRIVILEGES ON ALL sequences IN SCHEMA public TO devuser;
```

Set up a virtual environment and add to project:

Django 2.2.12
[django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/install.html)

Start a new project:

`django-admin startproject ddmanager`

Start a new app:

`py manage.py startapp manager`

Run the **initial migration** to create database tables needed by default Django applications:

`py manage.py migrate`

Add the app and crispy_forms to `INSTALLED_APPS` in **settings.py**:

```
INSTALLED_APPS = [
    'manager',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]
```

Set database connection parameters:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ddapp',
        'USER': 'devuser',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Make sure you've also set a template pack (CSS framework) in settings.py:

`CRISPY_TEMPLATE_PACK = 'bootstrap4'`

Create a superuser before creating any models (or doing anything really):

`python manage.py createsuperuser`

Use `inspectdb` to autogenerate a Django model module to standard output. On the command line
you can pipe it to models.py:

`py manage.py inspectdb > models.py`

## Other notes

Our registration template (/manager/templates/manager/register.html) is namespaced just in case
# Django-dbfilestorage

[![CircleCI](https://circleci.com/gh/tyrelsouza/django-dbfilestorage.svg?style=svg)](https://circleci.com/gh/tyrelsouza/django-dbfilestorage) [![codecov](https://codecov.io/gh/tyrelsouza/django-dbfilestorage/branch/master/graph/badge.svg)](https://codecov.io/gh/tyrelsouza/django-dbfilestorage)

Custom file storage for Django that stores file data and content type in the database.
Easy to use for testing remote storages when you're in a transition stage between Local and something like Amazon S3.

Intended to be used in tests, never in production.

## TESTING

I use Pyenv and Tox to support Python2.7.13 and Python3.6.3

```
pip install -r requirements-dev.txt
pyenv install 2.7.13 3.5.4 3.6.3
tox
```

Or you can run individually with your shell python using `python setup.py test`

## INSTALLATION

```
pip install django-dbfilestorage
```

Then in your project's `settings.py` file, add `'dbfilestorage'` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'dbfilestorage'
)
```

Next, if you want to set this globally, set the setting:

```python
DEFAULT_FILE_STORAGE='dbfilestorage.storage.DBFileStorage'
```

Or you can set it individually on a field: [Django Docs](https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField.storage)

```python
from dbfilestorage.storage import DBFileStorage

class SomeClass(models.Model):
    file = models.FileField(upload_to=u'anywhere',
        storage=DBFileStorage())
```


## TODO

- Test that this works on a fake model, not just the storage file.
- Different django versions.

## Signing Key
You can find my signing key at [TyrelSouza.com](https://tyrelsouza.com/koken/?/pages/pgp-keys/)

I will sign everything with 0x769A1BC78A2DDEE2


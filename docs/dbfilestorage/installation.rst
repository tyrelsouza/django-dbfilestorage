Installation
============

In your project's `settings.py` file, add `'dbfilestorage'` to your `INSTALLED_APPS`:

.. code:: python

    INSTALLED_APPS = (
        ...
        'dbfilestorage'
    )


Next, if you want to set this globally, set the setting:

.. code:: python

    DEFAULT_FILE_STORAGE='dbfilestorage.storage.DBFileStorage'


Or you can set it individually on a field: `Django Docs <https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField.storage>`_

.. code:: python

    from dbfilestorage.storage import DBFileStorage

    class SomeClass(models.Model):
        file = models.FileField(upload_to=u'anywhere',
            storage=DBFileStorage())

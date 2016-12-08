Usage
=====

Backstory
---------

The use case for this may be very small. At my company for our project we have
a giant test fixture, and we test file upload and creation. At the inception of
this module, I was working on changing our backend system to support Amazon S3
filestorage. I was getting frustrated with testing the assumption that a file
would exist on the hard drive, and not "somewhere else" so I started this module.

At first, I was going to use the BLOB field, but the way that we dump and load
our test fixtures didn't dump BLOBs by default.

Thus, the current implementation was born.


On to the Usage!
----------------

The normal usage for this is almost exactly the same for local file storage.
The user will upload a file the exact same way, and except for the url being an
md5 string, everything works exactly the same.

Saving file
~~~~~~~~~~~

The save method does most of the 'magic'. It stores the contents of the file as
a base64 string.  It then takes the filename, and tries to get the mimetype from
that (for rendering purposes). Then it takes the md5 of the read file and uses
that as the "unique" key to access the file. Then it checks if the file exists
and if it doesn't, it will create the entry in the database.

Example from Tests:

.. code:: python

    DBFileStorage.save("kris.jpg", file_object)

There will then be an entry in the database `50f3bfa6b91668789acab5f0a733fb3a`
that has the content of the `kris.jpg` file in it, with the content_type of
`image/jpeg`.

Opening file
~~~~~~~~~~~~

This file will then be accessible by the model field's `.open()` as normal.
The `.open()` returns a ContentFile of the base64 decoded data, so it should
work everywhere that a normal file would.

Viewing file with browser ( .url() )
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I've provided a `dbstorage_file` view that will render the file.

It gets the file object from the database referenced by the md5 (the
filefield.url() will provide this) automatically. It then returns a
HttpResponse of the decoded file and content type. Very straightforward.

Other operations
~~~~~~~~~~~~~~~~

Everything else, such as `.path()`, `.delete()`, `.size()`, `.exists()` are
exactly the same, in usage as normal.

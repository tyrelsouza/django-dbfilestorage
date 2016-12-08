import hashlib
import os

from dbfilestorage.models import DBFile

from django.core.files.storage import default_storage
from django.test import TestCase, Client
from django.test.utils import override_settings

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FILE_STORAGE = "dbfilestorage.storage.DBFileStorage"


@override_settings(DEFAULT_FILE_STORAGE=DEFAULT_FILE_STORAGE)
class DBFileTest(TestCase):
    def setUp(self):
        self.filename = "kris.jpg"
        self.filepath = os.path.join(PROJECT_ROOT, "test_files", self.filename)
        self.md5 = hashlib.md5(open(self.filepath, 'rb').read()).hexdigest()

    def _upload(self):
        with open(self.filepath, 'rb') as f:
            return default_storage.save(self.filepath, f)

    def test_upload(self):
        """ Test that the file storage uploads and puts in DB Properly """
        name = self._upload()
        self.assertEqual(name, self.md5)
        self.assertTrue(DBFile.objects.filter(name=name).exists())

    def test_equality(self):
        """ Test that the DB entry matches what is expected from the file """
        name = self._upload()

        with open(self.filepath, 'rb') as f:
            dbf = DBFile.objects.get(name=name)
            self.assertEqual(dbf.b64.decode("base64"),
                             f.read())
            self.assertEqual(dbf.content_type, 'image/jpeg')

    def test_open(self):
        """ Test that the storage mechanism can upload """
        name = self._upload()

        dbf = default_storage.open(name)
        with open(self.filepath, 'rb') as f:
            self.assertEqual(dbf.read(), f.read())

    def test_exists(self):
        """ Test that the storage mechanism can check existance """
        name = self._upload()

        self.assertTrue(default_storage.exists(name))

    def test_delete(self):
        """ Test Deletion """
        name = self._upload()
        self.assertTrue(DBFile.objects.filter(name=name).exists())
        default_storage.delete(name)
        self.assertFalse(DBFile.objects.filter(name=name).exists())

    def test_path(self):
        """ Test the path is just the md5 name """
        name = self._upload()
        path = default_storage.path(name)
        self.assertEqual(name, path)
        self.assertNotIn(self.filename, path)

    def test_size(self):
        """ Ensure we can get the proper size """
        name = self._upload()
        size = default_storage.size(name)
        self.assertGreater(size, 0)

    def test_url(self):
        """ Test that the url returned is the md5 path not the filename """
        name = self._upload()
        self.assertIn(self.md5, default_storage.url(name))

    def test_view(self):
        client = Client()
        name = self._upload()
        url = default_storage.url(name)
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)

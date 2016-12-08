import hashlib
import os

from dbfilestorage.models import DBFile

from django.core.files.storage import default_storage
from django.test import TestCase
from django.test.utils import override_settings

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


class DBFileTest(TestCase):
    def setUp(self):
        self.filename = "kris.jpg"
        self.filepath = os.path.join(PROJECT_ROOT, "test_files", self.filename)
        self.md5 = hashlib.md5(open(self.filepath, 'rb').read()).hexdigest()

    def _upload(self):
        with open(self.filepath, 'rb') as f:
            return default_storage.save(self.filepath, f)

    @override_settings(
        DEFAULT_FILE_STORAGE="dbfilestorage.storage.DBStorage")
    def test_upload(self):
        """ Test that the file storage uploads and puts in DB Properly """
        name = self._upload()
        self.assertEqual(name, self.md5)
        self.assertTrue(DBFile.objects.filter(name=name).exists())

    @override_settings(
        DEFAULT_FILE_STORAGE="dbfilestorage.storage.DBStorage")
    def test_equality(self):
        """ Test that the DB entry matches what is expected from the file """
        name = self._upload()
        with open(self.filepath, 'rb') as f:
            dbf = DBFile.objects.get(name=name)
            self.assertEqual(dbf.b64.decode("base64"),
                             f.read())
            self.assertEqual(dbf.content_type, 'image/jpeg')

    @override_settings(
        DEFAULT_FILE_STORAGE="dbfilestorage.storage.DBStorage")
    def test_open(self):
        """ Test that the storage mechanism can upload """
        name = self._upload()
        dbf = default_storage.open(name)
        with open(self.filepath, 'rb') as f:
            self.assertEqual(dbf.read(), f.read())

    @override_settings(
        DEFAULT_FILE_STORAGE="dbfilestorage.storage.DBStorage")
    def test_exists(self):
        """ Test that the storage mechanism can check existance """
        name = self._upload()
        self.assertTrue(default_storage.exists(name))

import hashlib
import os

from dbfilestorage.models import DBFile

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
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
        self._upload()

    def _upload(self):
        with open(self.filepath, 'rb') as f:
            return default_storage.save(self.filepath, f)

    def test_upload(self):
        """ Test that the file storage uploads and puts in DB Properly """
        self.assertTrue(DBFile.objects.filter(name=self.md5).exists())

    def test_no_duplicate_upload(self):
        """ Test that it won't make a new file if it already exists """
        # uploads once in setup already
        name2 = self._upload()
        self.assertEqual(self.md5, name2)

    def test_equality(self):
        """ Test that the DB entry matches what is expected from the file """
        with open(self.filepath, 'rb') as f:
            dbf = DBFile.objects.get(name=self.md5)
            self.assertEqual(dbf.b64.decode("base64"),
                             f.read())
            self.assertEqual(dbf.content_type, 'image/jpeg')

    def test_open(self):
        """ Test that the storage mechanism can upload """
        dbf = default_storage.open(self.md5)
        with open(self.filepath, 'rb') as f:
            self.assertEqual(dbf.read(), f.read())

    def test_exists(self):
        """ Test that the storage mechanism can check existance """
        self.assertTrue(default_storage.exists(self.md5))

    def test_delete(self):
        """ Test Deletion """
        self.assertTrue(DBFile.objects.filter(name=self.md5).exists())
        default_storage.delete(self.md5)
        self.assertFalse(DBFile.objects.filter(name=self.md5).exists())

    def test_path(self):
        """ Test the path is just the md5 name """
        path = default_storage.path(self.md5)
        self.assertEqual(self.md5, path)
        self.assertNotIn(self.filename, path)

    def test_size(self):
        """ Ensure we can get the proper size """
        size = default_storage.size(self.md5)
        self.assertGreater(size, 0)

    def test_url(self):
        """ Test that the url returned is the md5 path not the filename """
        self.assertIn(self.md5, default_storage.url(self.md5))

    def test_view(self):
        client = Client()
        url = default_storage.url(self.md5)
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_admin(self):
        my_admin = User.objects.create_superuser(
            username='tester',
            email='test@test.com',
            password='top_secret')
        client = Client()
        client.login(username=my_admin.username, password='top_secret')
        url = reverse("admin:dbfilestorage_dbfile_changelist")
        resp = client.get(url)
        self.assertContains(resp, self.md5)

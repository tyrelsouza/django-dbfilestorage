# -*- coding: utf-8 -*-
import os

from dbfilestorage.models import DBFile

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
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

        self._upload()

    def _upload(self):
        with open(self.filepath, 'rb') as f:
            return default_storage.save(self.filepath, f)

    def test_upload(self):
        """ Test that the file storage uploads and puts in DB Properly """
        self.assertTrue(DBFile.objects.filter(name=self.filepath).exists())

    def test_content_file(self):
        """ Test that this code works with ContentFile as well """
        content_file = ContentFile(u"ƊBStørage")
        default_storage.save("unicode", content_file)
        unicode_file = DBFile.objects.get(name="unicode")
        self.assertEqual(unicode(unicode_file),
            "unicode <application/octet-stream>")

    def test_no_duplicate_upload(self):
        """ Test that it won't make a new file if it already exists """
        # uploads once in setup already
        name2 = self._upload()
        self.assertEqual(self.filepath, name2)

    def test_equality(self):
        """ Test that the DB entry matches what is expected from the file """
        with open(self.filepath, 'rb') as f:
            dbf = DBFile.objects.get(name=self.filepath)
            self.assertEqual(dbf.b64.decode("base64"), f.read())
            self.assertEqual(dbf.content_type, 'image/jpeg')

    def test_open(self):
        """ Test that the storage mechanism can upload """
        dbf = default_storage.open(self.filepath)
        with open(self.filepath, 'rb') as f:
            self.assertEqual(dbf.read(), f.read())

    def test_exists(self):
        """ Test that the storage mechanism can check existance """
        self.assertTrue(default_storage.exists(self.filepath))

    def test_delete(self):
        """ Test Deletion """
        self.assertTrue(DBFile.objects.filter(name=self.filepath).exists())
        default_storage.delete(self.filepath)
        self.assertFalse(DBFile.objects.filter(name=self.filepath).exists())
        # Also test that calling delete on something that doesn't exist,
        # errors silently
        self.assertFalse(DBFile.objects.filter(name="Nothing").exists())
        default_storage.delete("Nothing")

    def test_size(self):
        """ Ensure we can get the proper size """
        size = default_storage.size(self.filepath)
        self.assertGreater(size, 0)

    def test_raw_save(self):
        CONTENT_DATA_1 = u"Here's some stuff! ƊBStørage - ONE"
        CONTENT_DATA_2 = u"Here's some stuff! ƊBStørage - TWO"
        FILE_NAME = "saveable.txt"
        self.assertFalse(DBFile.objects.filter(name=FILE_NAME).exists())

        # -- Save to a _new_ file
        content_file = ContentFile(CONTENT_DATA_1.encode("utf-8"))
        default_storage.save(FILE_NAME, content_file)
        self.assertTrue(DBFile.objects.filter(name=FILE_NAME).exists())

        with default_storage.open(FILE_NAME, "rb") as f:
            read_back = f.read().decode("utf-8")
        self.assertEqual(read_back, CONTENT_DATA_1)

        # -- Save to an _existing_ file
        content_file = ContentFile(CONTENT_DATA_2.encode("utf-8"))
        default_storage.save(FILE_NAME, content_file)
        self.assertTrue(DBFile.objects.filter(name=FILE_NAME).exists())
        with default_storage.open(FILE_NAME, "rb") as f:
            read_back = f.read().decode("utf-8")
        self.assertEqual(read_back, CONTENT_DATA_2)

        # -- Clean up after ourselves
        default_storage.delete(FILE_NAME)
        self.assertFalse(DBFile.objects.filter(name=FILE_NAME).exists())

    def test_url(self):
        """ Test that the url returned is the filename """
        self.assertIn(self.filename, default_storage.url(self.filename))

    def test_view(self):
        client = Client()
        url = default_storage.url(self.filepath)
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
            
    def test_view_fails(self):
        client = Client()
        url = default_storage.url("failure")
        resp = client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_admin(self):
        my_admin = User.objects.create_superuser(
            username='tester',
            email='test@test.com',
            password='top_secret')
        client = Client()
        client.login(username=my_admin.username, password='top_secret')
        url = reverse("admin:dbfilestorage_dbfile_changelist")
        resp = client.get(url)
        self.assertContains(resp, self.filepath)

    def test_mtime(self):
        """ Ensure we can get the modified time """
        mtime = default_storage.modified_time(self.filepath)
        self.assertIsNotNone(mtime)

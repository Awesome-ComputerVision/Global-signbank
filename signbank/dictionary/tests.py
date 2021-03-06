import datetime
from signbank.dictionary.models import *
from signbank.dictionary.adminviews import *

from django.contrib.auth.models import AnonymousUser, User, Group, Permission, UserManager, GroupManager, PermissionsMixin
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test.client import encode_multipart, encode_file
import unittest
import json
from django.test import Client
from django.core.urlresolvers import reverse
from django.http import HttpResponse, SimpleCookie
from django.contrib.messages.storage.base import BaseStorage, Message
from django.contrib.messages.storage.cookie import Message, MessageDecoder, MessageEncoder
from django.core.management import call_command
from django.db import connection
from django.db.models import Q
from django.test.utils import setup_test_environment
from django.contrib import messages
from django.utils.safestring import SafeData, mark_safe

import guardian
from guardian.shortcuts import get_objects_for_user, assign_perm
from guardian.models import UserObjectPermission, GroupObjectPermission

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

class ImportExportTests(TestCase):

    # Three test case scenario's for exporting ECV via the DatasetListView with DEFAULT_DATASET
    #       /datasets/available/?dataset_name=DEFAULT_DATASET&export_ecv=ECV
    # 1. The user is logged in and has permission to change dataset
    # 2. The user is logged in but does not have permission to change dataset
    # 3. The user is not logged in

    def setUp(self):

        # a new test user is created for use during the tests
        self.user = User.objects.create_user('test-user', 'example@example.com', 'test-user')

    def test_DatasetListView_ECV_export_permission_change_dataset(self):

        print('Test DatasetListView export_ecv with permission change_dataset')

        dataset_name = DEFAULT_DATASET
        print('Test Dataset is: ', dataset_name)

        # Give the test user permission to change a dataset
        test_dataset = Dataset.objects.get(name=dataset_name)
        assign_perm('change_dataset', self.user, test_dataset)
        print('User has permmission to change dataset.')

        client = Client()

        logged_in = client.login(username='test-user', password='test-user')

        url = '/datasets/available?dataset_name='+dataset_name+'&export_ecv=ECV'

        response = client.get(url)

        loaded_cookies = response.cookies.get('messages').value
        decoded_cookies = decode_messages(loaded_cookies)
        json_decoded_cookies = json.loads(decoded_cookies, cls=MessageDecoder)
        json_message = json_decoded_cookies[0]
        print('Message: ', json_message)

        self.assertEqual(str(json_message), 'ECV ' + dataset_name + ' successfully updated.')

    def test_DatasetListView_ECV_export_no_permission_change_dataset(self):

        print('Test DatasetListView export_ecv without permission')

        dataset_name = DEFAULT_DATASET
        print('Test Dataset is: ', dataset_name)

        client = Client()

        logged_in = client.login(username='test-user', password='test-user')

        url = '/datasets/available?dataset_name='+dataset_name+'&export_ecv=ECV'

        response = client.get(url)

        loaded_cookies = response.cookies.get('messages').value
        decoded_cookies = decode_messages(loaded_cookies)
        json_decoded_cookies = json.loads(decoded_cookies, cls=MessageDecoder)
        json_message = json_decoded_cookies[0]
        print('Message: ', json_message)

        self.assertEqual(str(json_message), 'No permission to export dataset.')

    def test_DatasetListView_not_logged_in_ECV_export(self):

        print('Test DatasetListView export_ecv anonymous user not logged in')

        dataset_name = DEFAULT_DATASET
        print('Test Dataset is: ', dataset_name)

        client = Client()

        url = '/datasets/available?dataset_name=' + dataset_name + '&export_ecv=ECV'

        response = client.get(url)

        loaded_cookies = response.cookies.get('messages').value
        decoded_cookies = decode_messages(loaded_cookies)
        json_decoded_cookies = json.loads(decoded_cookies, cls=MessageDecoder)
        json_message = json_decoded_cookies[0]
        print('Message: ', json_message)

        self.assertEqual(str(json_message), 'Please login to use this functionality.')


# Helper function to retrieve contents of json-encoded message
def decode_messages(data):
    if not data:
        return None
    bits = data.split('$', 1)
    if len(bits) == 2:
        hash, value = bits
        return value
    return None

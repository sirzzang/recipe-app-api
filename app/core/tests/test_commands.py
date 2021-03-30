from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        '''test wating for db when db is available'''
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # what mock object does
            gi.return_value = True  # return the specified value
            call_command('wait_for_db')  # minitor how many times called
            self.assertEqual(gi.call_count, 1)  # `getitem` only called once?

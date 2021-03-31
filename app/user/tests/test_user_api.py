from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


# helper function
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# test class
class PublicUsersApiTests(TestCase):
    '''test the users API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''test creating user with valid payload'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  # unwind and GET user
        self.assertTrue(user.check_password(payload['password']))  # check PW
        self.assertNotIn('password', res.data)  # for security

    def test_user_exists(self):
        '''test creating a user that already exists fails'''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass'
        }
        create_user(**payload)  # 미리 만들기

        res = self.client.post(CREATE_USER_URL, payload)  # 존재하는 유저 POST 요청

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  # bad

    def test_password_too_short(self):
        '''test that the password must be more than 5 characters'''
        payload = {
            'email': 'sirzzang@naver.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()  # returns True when the user exists
        self.assertFalse(user_exists)

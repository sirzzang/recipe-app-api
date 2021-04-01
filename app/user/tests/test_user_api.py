from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# url constant variables
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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
            'password': 'pw',
            'name': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()  # returns True when the user exists
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''test that a token is created for the user'''
        payload = {
            'email': 'sirzzang@naver.com',
            'password': 'testpass'
        }
        create_user(**payload)  # helper function for creating user
        res = self.client.post(TOKEN_URL, payload)  # response for token url

        self.assertIn('token', res.data)  # check if 'token' key in response
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''test that token is not created if invalid credentials are given'''
        create_user(email='test@gmail.com', password='testpass')
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test that token is not created if user does not exists'''
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''test that email and password are required'''
        res = self.client.post(
            TOKEN_URL, {'email': 'sirzzang@gmail.com', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrived_user_unauthorized(self):
        '''test that authentication is required for users'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    '''test API requests that require authentication'''

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''test retrieving profile for logged in user'''
        res = self.client.get(ME_URL)  # HTTP response

        self.assertEqual(res.status_code, status.HTTP_200_OK)  # HTTP 200 ok
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        '''test that POST is not allowed on the me url'''
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''test updating the user profile for authenticated user'''
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)  # PATCH method

        self.user.refresh_from_db()  # refresh database

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

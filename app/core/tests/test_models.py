from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@naver.com', password='testpass123'):
    '''create a sample user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''test creating a new user with an email is successful'''
        email = 'sirzzang@naver.com'  # test email
        password = 'testpassword123'  # test password
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assert user is created
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''test the email for a new user is normalized'''
        email = 'sirzzang@NAVER.COM'
        user = get_user_model().objects.\
            create_user(email, 'test123')  # throwaway string assigned as pw

        # check if email normalized
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        '''test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'sirzzang@naver.com',
            'test123'
        )

        # superuser, staff 확인
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'  # name that will be used in the system
        )

        self.assertEqual(str(tag), tag.name)

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''test creating a new user with an email is successful'''
        email = 'sirzzang@naver.com' # test email
        password = 'testpassword123' # test password
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
            create_user(email, 'test123') # throwaway string assigned as pw
        
        self.assertEqual(user.email, email.lower()) # check if email normalized
        
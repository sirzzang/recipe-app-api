from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase): # inherit TestCase

    def setUp(self):
        self.client = Client() # client
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        ) # admin
        self.client.force_login(self.admin_user) # admin user logged in
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='test user for name'
        ) # super user for testing
    
    def test_users_listed(self):
        '''test that users are listed on user page'''
        url = reverse('admin:core_user_changelist') # user url list page
        res = self.client.get(url) # test clienet HTTP GET request

        # check if the response contains user name, email
        self.assertContains(res, self.user.name) 
        self.assertContains(res, self.user.email)   


from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from unittest.mock import patch

class SignupTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_signup(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirmPassword': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    def test_failed_signup(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'password123',
            'confirmPassword':"" #wrong confirm password
        })
        self.assertEqual(response.status_code, 302)

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        

    def test_failed_login(self):
        
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        

class UpdateProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    def test_update_profile(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('updateProfile'), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'fName': 'Updated',
            'lName': 'User'
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updateduser@example.com')
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'User')
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('userProfile'))

class GraduationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('Profile.views.STUDENT_INFO')
    def test_successful_graduation(self, mock_STUDENT_INFO):
        mock_STUDENT_INFO.return_value = {
            'hasAccount': True,
            'hasOutStandingBalance': False,
            'error': False
        }
        
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        
        response = self.client.get(reverse('graduation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Profile/graduation.html')
        self.assertTrue(response.context['noOutStandingBalance'])
        

    @patch('Profile.views.STUDENT_INFO')
    def test_failed_graduation(self, mock_STUDENT_INFO):

        mock_STUDENT_INFO.return_value = None
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('graduation'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

class RetryLibraryAccountCreationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('Profile.views.retryLibraryAccountCreation')
    def test_successful_retry(self, mock_REGISTER_LIBRARY_ACCOUNT):
        mock_REGISTER_LIBRARY_ACCOUNT.return_value = True 

        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('libraryAccountCreate'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('userProfile'))
        

    @patch('Profile.views.REGISTER_LIBRARY_ACCOUNT')
    def test_failed_retry(self, mock_REGISTER_LIBRARY_ACCOUNT):
        mock_REGISTER_LIBRARY_ACCOUNT.return_value = False
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')

        response = self.client.get(reverse('libraryAccountCreate'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('userProfile'))
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class AccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
    
    def test_signup_view(self):
        response = self.client.post(reverse('cos_accounts:signup'), {
            'username': 'newuser',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_invalid_data(self):
        response = self.client.post(reverse('cos_accounts:signup'), {
            'username': '',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(User.objects.filter(username='').exists())

    def test_signin_view(self):
        response = self.client.post(reverse('cos_accounts:signin'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_signin_invalid_credentials(self):
        response = self.client.post(reverse('cos_accounts:signin'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cos_accounts:logout'))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_change_password(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('cos_accounts:change_password'), {
            'old_password': 'password123',
            'new_password1': 'Newpassword456',
            'new_password2': 'Newpassword456'
        })
        self.assertEqual(response.status_code, 302)  
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Newpassword456'))

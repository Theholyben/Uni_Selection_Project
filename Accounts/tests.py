from django.test import TestCase

# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # کاربر ادمین
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123456',
            role='ADMIN'
        )
        
        # کاربر دانشجو
        self.student_user = User.objects.create_user(
            username='student',
            password='student123456',
            role='STUDENT'
        )
        
        # کاربر استاد
        self.professor_user = User.objects.create_user(
            username='professor',
            password='prof123456',
            role='PROFESSOR'
        )

    def test_1_admin_can_login_successfully(self):
        """تست ۱: مدیر باید بتونه با موفقیت لاگین کنه و توکن بگیره"""
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'admin', 'password': 'admin123456'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_2_student_can_login_successfully(self):
        """تست ۲: دانشجو هم باید بتونه لاگین کنه (احراز هویت عمومی)"""
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'student', 'password': 'student123456'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_3_professor_can_login_successfully(self):
        """تست ۳: استاد هم باید بتونه لاگین کنه"""
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'professor', 'password': 'prof123456'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_4_invalid_credentials_return_401(self):
        """تست ۴: اطلاعات اشتباه → خطای 401"""
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'admin', 'password': 'wrongpass'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)


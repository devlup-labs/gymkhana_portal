from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from oauth.models import UserProfile


class KonnektURLsTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create(username='test_user', first_name='test')
        cls.user_profile = UserProfile.objects.create(user=cls.user, roll='B00CS000', dob=timezone.now(),
                                                      phone='1234567890', branch='CSE')

    def test_konnekt_url_without_logged_in_case_1(self):
        """url without logged in user case: index page"""
        # url without login --> redirect to login page
        response = self.client.get(reverse('konnekt:index'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('konnekt:index'))

    def test_konnekt_url_without_looged_in_case_2(self):
        """url without logged in user case: search page"""
        response = self.client.get(reverse('konnekt:search'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('konnekt:search'))

    def test_konnekt_index_url_with_logged_in(self):
        """index url with logged in user"""
        self.client.force_login(self.user)
        # index url --> index page used
        response = self.client.get(reverse('konnekt:index'), follow=True)
        self.assertTemplateUsed(response, 'konnekt/index.html')
        self.client.logout()

    def test_konnekt_search_url_with_logged_in_case_1(self):
        """search url with logged in user and query=None"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('konnekt:search'), follow=True)
        self.assertTemplateUsed(response, 'konnekt/search.html')
        self.client.logout()

    def test_konnekt_search_url_with_logged_in_case_2(self):
        """search url with logged in user and with query"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('konnekt:search') + '?q=test', follow=True)
        self.assertTemplateUsed(response, 'konnekt/search.html')
        self.client.logout()


class KonnektQueryTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='test_user', first_name='test')
        cls.user_profile = UserProfile.objects.create(user=cls.user, roll='B00CS000', dob=timezone.now(),
                                                      phone='1234567890', branch='CSE')

    def test_konnekt_query_case_1(self):
        """case: query None"""
        self.assertEqual(UserProfile.objects.search(None).count(), 0)

    def test_konnekt_query_case_2(self):
        """case: query term < 3"""
        self.assertEqual(UserProfile.objects.search('tes').count(), 0)

    def test_konnekt_query_case_3(self):
        """case: query term >= 3"""
        self.assertEqual(UserProfile.objects.search('test').count(), 1)

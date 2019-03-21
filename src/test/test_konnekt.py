from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from oauth.models import UserProfile


class KonnektTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.user = User.objects.create(username='test_user', first_name='test')
        cls.user_profile = UserProfile.objects.create(user=cls.user, roll='B00CS000', dob=timezone.now(),
                                                      phone='1234567890', branch='CSE')

    def test_konnekt_url(self):
        """url without logged in user """
        # url without login --> redirect to login page
        response = self.client.get(reverse('konnekt:index'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('konnekt:index'))
        response = self.client.get(reverse('konnekt:search'), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('konnekt:search'))

        """url with logged in user"""
        self.client.force_login(self.user)
        # index url --> index page used
        response = self.client.get(reverse('konnekt:index'), follow=True)
        self.assertTemplateUsed(response, 'konnekt/index.html')
        # search url & with no query
        response = self.client.get(reverse('konnekt:search'), follow=True)
        self.assertTemplateUsed(response, 'konnekt/search.html')
        # search url & with query & term <= 3
        response = self.client.get(reverse('konnekt:search') + "?q=tes", follow=True)
        self.assertTemplateUsed(response, 'konnekt/search.html')
        # search url & with query & term > 3
        response = self.client.get(reverse('konnekt:search') + "?q=test", follow=True)
        self.assertTemplateUsed(response, 'konnekt/search.html')

    def test_konnekt_query(self):
        self.assertEqual(UserProfile.objects.search(None).count(), 0)
        self.assertEqual(UserProfile.objects.search('tes').count(), 0)
        self.assertEqual(UserProfile.objects.search('test').count(), 1)

from django.test import TestCase
from django.contrib.auth.models import User
from test.test_assets import get_random_date
from news.models import News, Update
from oauth.models import UserProfile


class NewsModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Object of news and update model
        cls.usr = User.objects.create(username='user_1')
        cls.user = UserProfile.objects.create(user=cls.usr, dob=get_random_date())
        cls.news = News.objects.create(title='news_1', date=get_random_date())
        cls.update = Update.objects.create(title='update_1')

    def test_news_str_method(self):
        """Test news model __Str__ method"""
        self.assertEqual(self.news.__str__(), 'news_1')

    def test_update_str_method(self):
        """Test update model __str__ method"""
        self.assertEqual(self.update.__str__(), 'update_1')

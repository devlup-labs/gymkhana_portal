from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from news.models import News, Update
from oauth.models import UserProfile


class NewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Object of news and update model
        cls.usr = User.objects.create(username='test_user_1')
        cls.user = UserProfile.objects.create(user=cls.usr, dob=timezone.now())
        cls.news = News.objects.create(title='news_1', date=timezone.now())
        cls.update = Update.objects.create(title='update_1')

    def test_object_creation(self):
        # News model
        self.assertEqual(self.news.__str__(), 'news_1')

        # Update Model
        self.assertEqual(self.update.__str__(), 'update_1')

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from forum.models import Topic, Answer
from oauth.models import UserProfile


class ForumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create client for test
        cls.client = Client()
        cls.user_1 = User.objects.create(username='test_user', first_name='test', last_name='user')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, roll='B00CS000', dob=timezone.now())

        # create object of it
        cls.topic_1 = Topic.objects.create(author=cls.user_profile_1, title='abc')
        cls.answer_1 = Answer.objects.create(topic=cls.topic_1, author=cls.user_profile_1)

    def test_object_creation(self):
        self.assertEqual(self.topic_1.__str__(), 'abc')
        self.assertEqual(self.answer_1.__str__(), 'On: abc by Test ')

    def test_forum_urls_without_login(self):
        # without login --> redirect to login page
        response = self.client.get(reverse('forum:index'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:index'))

        response = self.client.get(reverse('forum:answered-by-user'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:answered-by-user'))

        response = self.client.get(reverse('forum:add_topic'))
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('forum:add_topic'))

        response = self.client.get(self.topic_1.get_absolute_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_absolute_url())

        response = self.client.get(self.topic_1.get_edit_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_edit_url())

        response = self.client.get(self.topic_1.get_delete_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.topic_1.get_delete_url())

        response = self.client.get(self.answer_1.get_delete_url())
        self.assertRedirects(response, reverse('login') + "?next=" + self.answer_1.get_delete_url())

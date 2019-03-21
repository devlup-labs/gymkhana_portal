from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from oauth.models import UserProfile, SocialLink


class OauthTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a client for test
        cls.client = Client()

        # make a user with user profile data
        cls.user_1 = User.objects.create(username='test_user')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, roll='B17CS014', dob=timezone.now(),
                                                        phone='1234567890', branch='CSE')
        cls.link_1 = SocialLink.objects.create(user=cls.user_1, social_media='YT', link='iitj.ac.in')
        cls.link_2 = SocialLink.objects.create(user=cls.user_1, social_media='AB', link='iitj.ac.in')

        # user with no user profile data
        cls.user_2 = User.objects.create(username='test_user_2')

    def test_object_creation(self):
        # UserProfile Model
        self.assertEqual(self.user_profile_1.__str__(), 'B17CS014 ()')
        self.assertEqual(self.user_profile_1.get_absolute_url(), '/account/B17CS014/')
        self.assertEqual(self.user_profile_1.skills_as_list, '')
        self.user_profile_1.skills = 'C'
        self.user_profile_1.save()
        self.assertEqual(self.user_profile_1.skills_as_list, ['C'])

        # SocialLink model
        self.assertEqual(self.link_1.get_absolute_url(), self.user_profile_1.get_absolute_url())
        self.assertEqual(self.link_1.__str__(), ' - YouTube')
        self.assertEqual(self.link_1.get_fai(), 'fa fa-youtube')
        self.assertEqual(self.link_2.get_fai(), 'fa fa-link')
        self.assertEqual(self.link_1.get_sm_ic(), 'yt-ic')
        self.assertEqual(self.link_2.get_sm_ic(), '')

    def test_oauth_register(self):
        """All possibilities of creation of user"""
        # register url without logged in user --> will redirect to login page
        response = self.client.get(reverse('oauth:register'), follow=True)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('oauth:register'))

        # register url with logged in user & with user profile data --> will redirect to profile page
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('oauth:register'), follow=True)
        self.assertRedirects(response, reverse('oauth:detail', kwargs={'roll': self.user_profile_1.roll}))

        # register url with logged in user & with no user profile data & data not provided --> error in page
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('oauth:register'))
        self.assertTemplateUsed(response, 'oauth/register.html')

        # register url with logged in user & with no user profile data & data provided & dob < 13 year --> error in page
        # & will not create user profile object
        dob = str(timezone.now().year) + "-" + str(timezone.now().month) + "-" + str(
            timezone.now().day)  # dob < 13 year
        data = {'phone': ['1234567890'], 'gender': ['M'], 'dob': [dob], 'prog': ['BT'], 'branch': ['CSE'],
                'year': ['1'], 'roll': ['B17CS013']}
        response = self.client.post(reverse('oauth:register'), data, follow=True)
        self.assertTemplateUsed(response, 'oauth/register.html')
        self.assertFalse(UserProfile.objects.filter(user=self.user_2).exists())

        # register url with logged in user & no user profile data & data provided & dob > 13 year --> create object
        # & redirect to forum page
        data = {'phone': ['1234567890'], 'gender': ['M'], 'dob': ['2000-07-31'], 'prog': ['BT'], 'branch': ['CSE'],
                'year': ['1'], 'roll': ['B17CS013']}
        response = self.client.post(reverse('oauth:register'), data, follow=True)
        self.assertRedirects(response, reverse('forum:index'))
        self.assertTrue(UserProfile.objects.filter(user=self.user_2).exists())

        UserProfile.objects.get(user=self.user_2).delete()
        self.client.logout()

    def test_oauth_activate(self):
        """All possibilities of activation of account"""
        # get activation link url --> will get link
        response = self.client.get(reverse('oauth:get-act-link', kwargs={'roll': self.user_profile_1.roll}))
        self.assertTemplateUsed(response, 'oauth/account_activation_email.html')

        # hit url with email confirmed true --> will redirect ro invalid link page
        response = self.client.get(self.user_profile_1.get_activation_url)
        self.assertTemplateUsed(response, 'oauth/invalid_activation.html')

        # hit url with email confirmed false --> will logout user and redirect to profile page
        self.user_profile_1.email_confirmed = False
        self.user_profile_1.save()
        self.client.force_login(self.user_1)
        response = self.client.get(self.user_profile_1.get_activation_url, follow=True)
        self.user_profile_1 = UserProfile.objects.get(user=self.user_1)
        self.assertTrue(self.user_profile_1.email_confirmed)
        self.assertRedirects(response, reverse('login') + "?next=" + self.user_profile_1.get_absolute_url())

        # hit url with email wrong token and uidb64 --> invalid token
        response = self.client.get(reverse('oauth:activate', kwargs={'uidb64': b'YQ', 'token': 'abc-abd'}))
        self.assertTemplateUsed(response, 'oauth/invalid_activation.html')

    def oauth_sociallink_add(self):
        """All possibilities of social link add url"""
        # social link add without logged in user --> ask for login
        data = {'social_media': ['TW'], 'link': ['https://iitj.ac.in']}
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-add'))

        self.client.force_login(self.user_1)

        # social link add with logged in user --> will create object and will redirect to profile page
        # data = {'social_media': ['TW'], 'link': ['https://iitj.ac.in']}
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
        self.assertTrue(SocialLink.objects.filter(user=self.user_1, social_media='TW').exists())

        # social link add which already exist --> will do nothing and remain on that page
        data = {'social_media': ['TW'], 'link': ['https://facebook.com']}
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertTemplateUsed(response, 'oauth/sociallink_create.html')
        self.assertEqual(SocialLink.objects.get(user=self.user_1, social_media='TW').link, 'https://iitj.ac.in')

        self.client.logout()

    def oauth_sociallink_update(self):
        """All possibilities of social link update url"""
        # social link update without logged in user --> ask for login
        kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        data = {'social_media': ['TW'], 'link': ['https://twitter.com']}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-edit', kwargs=kwargs))

        self.client.force_login(self.user_1)

        # social link edit with user own it and exist --> will change it and redirect to profile page
        # data = {'social_media': ['TW'], 'link': ['https://twitter.com']}
        # kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
        self.assertEqual(SocialLink.objects.get(user=self.user_1, social_media='TW').link, 'https://twitter.com')

        # social link edit & social media not exist --> will not create object and redirect to 404 page
        data = {'social_media': ['FB'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_1.username, 'social_media': 'FB'}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
        self.assertFalse(SocialLink.objects.filter(user=self.user_1, social_media='FB').exists())
        self.assertEqual(response.status_code, 404)

        # social link edit & user doesn't own & media doesn't exist --> response 404
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 404)

        SocialLink.objects.create(user=self.user_2, social_media='TW', link='https://twitter.com')
        # social link edit & user doesn't own & media exist --> response Permission Denied
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)

        SocialLink.objects.get(user=self.user_2, social_media="TW").delete()
        self.client.logout()

    def oauth_sociallink_delete(self):
        """All possibilities of social link delete url"""
        # social link delete without logged in user --> ask for login
        kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        data = {'social_media': ['TW'], 'link': ['https://twitter.com']}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-delete', kwargs=kwargs))

        self.client.force_login(self.user_1)

        # social link delete with user own it and exist --> will delete it and redirect to profile page
        # data = {'social_media': ['TW'], 'link': ['http://twitter.com']}
        # kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
        self.assertFalse(SocialLink.objects.filter(user=self.user_1, social_media='TW').exists())

        # social link delete & social media not exist --> redirect to 404 page
        data = {'social_media': ['FB'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_1.username, 'social_media': 'FB'}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data, follow=True)
        self.assertEqual(response.status_code, 404)

        # social link delete & user doesn't own & media doesn't exist --> response 404
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 404)

        SocialLink.objects.create(user=self.user_2, social_media='TW', link='https://twitter.com')
        # social link delete & user doesn't own & media exist --> response Permission Denied
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)

        SocialLink.objects.get(user=self.user_2, social_media="TW").delete()
        self.client.logout()

    def test_oauth_sociallink(self):
        self.oauth_sociallink_add()
        self.oauth_sociallink_update()
        self.oauth_sociallink_delete()

    def oauth_profile_detail(self):
        """Possibilities of profile details"""
        # profile detail url & user is not logged in --> login url
        response = self.client.get(self.user_profile_1.get_absolute_url(), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + self.user_profile_1.get_absolute_url())

        # profile detail url & user has no user profile data --> redirect to register page
        self.client.force_login(self.user_2)
        response = self.client.get(self.user_profile_1.get_absolute_url(), follow=True)
        self.assertRedirects(response, reverse('oauth:register'))

        # profile detail url & user has user profile data --> template used oauth/profile_detail.html
        self.client.force_login(self.user_1)
        response = self.client.get(self.user_profile_1.get_absolute_url(), follow=True)
        self.assertTemplateUsed(response, 'oauth/profile_detail.html')

        self.client.logout()

    def oauth_profile_edit(self):
        data = {'phone': ['0987654321'], 'year': ['1'], 'hometown': ['XYZ'], 'skills': [''], 'about': ['']}
        """Possibilities of profile edit"""
        # profile edit without logged in user --> ask for login
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_1.roll}), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:edit',
                                                                             kwargs={'roll': self.user_profile_1.roll}))

        # profile edit url & user has no user profile data --> redirect to register page
        self.client.force_login(self.user_2)
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_1.roll}), data, follow=True)
        self.assertRedirects(response, reverse('oauth:register'))

        self.client.force_login(self.user_1)

        # profile edit & user doesn't own it & profile not exist --> response 404
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': 'B11CS011'}), data, follow=True)
        self.assertEqual(response.status_code, 404)

        self.user_profile_2 = UserProfile.objects.create(user=self.user_2, roll='B17CS000', dob=timezone.now(),
                                                         phone='1234567890', branch='CSE')
        # profile edit & user doesn't own & profile exist --> response permission denied
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_2.roll}), data, follow=True)
        self.assertEqual(response.status_code, 403)

        self.user_profile_2.delete()

        # profile edit & user own it --> will change it and redirect to detail page
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_1.roll}), data, follow=True)
        self.assertRedirects(response, reverse('oauth:detail', kwargs={'roll': self.user_profile_1.roll}))
        self.assertEqual(UserProfile.objects.get(user=self.user_1).phone, '0987654321')

        self.client.logout()

    def test_oauth_profile(self):
        self.oauth_profile_detail()
        self.oauth_profile_edit()

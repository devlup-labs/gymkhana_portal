from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from oauth.models import UserProfile, SocialLink
from test.test_assets import get_random_date


class OauthModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # make a user with user profile data
        cls.user_1 = User.objects.create(username='test_user')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, roll='B17CS014', dob=get_random_date(),
                                                        phone='1234567890', branch='CSE')
        cls.link_1 = SocialLink.objects.create(user=cls.user_1, social_media='YT', link='iitj.ac.in')
        cls.link_2 = SocialLink.objects.create(user=cls.user_1, social_media='AB', link='iitj.ac.in')

        # user with no user profile data
        cls.user_2 = User.objects.create(username='test_user_2')

    def test_user_profile_str_method(self):
        """Test user profile model __str__ method"""
        self.assertEqual(self.user_profile_1.__str__(), 'B17CS014 ()')

    def test_user_profile_get_absolute_url_method(self):
        """Test user profile model get_absolute_url method"""
        self.assertEqual(self.user_profile_1.get_absolute_url(), '/account/B17CS014/')

    def test_user_profile_skills_as_list_property_case_1(self):
        """Test user profile model skills_as_list property case: no skills"""
        self.assertEqual(self.user_profile_1.skills_as_list, '')

    def test_user_profile_skills_as_list_property_case_2(self):
        """Test user profile model skills_as_list property case: skills='c'"""
        self.user_profile_1.skills = 'C'
        self.user_profile_1.save()
        self.assertEqual(self.user_profile_1.skills_as_list, ['C'])

    def test_social_link_get_absolute_url_method(self):
        """Test social link model get_absolute_url method"""
        self.assertEqual(self.link_1.get_absolute_url(), self.user_profile_1.get_absolute_url())

    def test_social_link_str_method(self):
        """Test social link model __Str__ method"""
        self.assertEqual(self.link_1.__str__(), ' - YouTube')

    def test_social_link_get_fai_method_case_1(self):
        """Test social link model get_fat method case: known choice"""
        self.assertEqual(self.link_1.get_fai(), 'fa fa-youtube')

    def test_social_link_get_fai_method_case_2(self):
        """Test social link model get_fai method case: unknown choice"""
        self.assertEqual(self.link_2.get_fai(), 'fa fa-link')

    def test_social_link_get_sm_ic_method_case_1(self):
        """Test social link model get_sm_ic method case: known choice"""
        self.assertEqual(self.link_1.get_sm_ic(), 'yt-ic')

    def test_social_link_get_sm_ic_method_case_2(self):
        """Test social link model get_sm_ic method case: unknown choice"""
        self.assertEqual(self.link_2.get_sm_ic(), '')


class OauthURLsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a client for test
        cls.client = Client()

        # make a user with user profile data
        cls.user_1 = User.objects.create(username='test_user')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, roll='B17CS014', dob=get_random_date(),
                                                        phone='1234567890', branch='CSE')
        cls.link_1 = SocialLink.objects.create(user=cls.user_1, social_media='YT', link='iitj.ac.in')
        cls.link_2 = SocialLink.objects.create(user=cls.user_1, social_media='AB', link='iitj.ac.in')

        # user with no user profile data
        cls.user_2 = User.objects.create(username='test_user_2')

    def test_oauth_register_url_without_logged_in_user(self):
        # Register url without logged in user --> will redirect to login page
        response = self.client.get(reverse('oauth:register'), follow=True)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('oauth:register'))

    def test_oauth_register_url_with_logged_in_case_1(self):
        # register url with logged in user & with no user profile data & data provided & dob < 13 year --> error in page
        # & will not create user profile object
        self.client.force_login(user=self.user_2)
        dob = str(get_random_date(True).year) + "-" + str(get_random_date(True).month) + "-" + str(
            get_random_date(True).day)  # dob < 13 year
        data = {'phone': ['1234567890'], 'gender': ['M'], 'dob': [dob], 'prog': ['BT'], 'branch': ['CSE'],
                'year': ['1'], 'roll': ['B17CS013']}
        response = self.client.post(reverse('oauth:register'), data, follow=True)
        self.assertTemplateUsed(response, 'oauth/register.html')
        self.assertFalse(UserProfile.objects.filter(user=self.user_2).exists())
        self.client.logout()

    def test_oauth_register_url_with_logged_in_case_2(self):
        # register url with logged in user & no user profile data & data provided & dob > 13 year --> create object
        # & redirect to forum page
        self.client.force_login(user=self.user_2)
        data = {'phone': ['1234567890'], 'gender': ['M'], 'dob': ['2000-07-31'], 'prog': ['BT'], 'branch': ['CSE'],
                'year': ['1'], 'roll': ['B17CS013']}
        response = self.client.post(reverse('oauth:register'), data, follow=True)
        self.assertRedirects(response, reverse('forum:index'))
        self.assertTrue(UserProfile.objects.filter(user=self.user_2).exists())
        UserProfile.objects.get(user=self.user_2).delete()
        self.client.logout()

    def test_oauth_register_url_with_logged_in_case_3(self):
        # register url with logged in user & gas user profile data --> redirect to profile page
        self.client.force_login(user=self.user_1)
        data = {'phone': ['1234567890'], 'gender': ['M'], 'dob': ['2000-07-31'], 'prog': ['BT'], 'branch': ['CSE'],
                'year': ['1'], 'roll': ['B17CS013']}
        response = self.client.post(reverse('oauth:register'), data, follow=True)
        self.assertRedirects(response, reverse('oauth:detail', kwargs={'roll': self.user_profile_1.roll}))
        self.client.logout()

    def test_oauth_activate_url_case_1(self):
        # get activation link url --> will get link
        response = self.client.get(reverse('oauth:get-act-link', kwargs={'roll': self.user_profile_1.roll}))
        self.assertTemplateUsed(response, 'oauth/account_activation_email.html')

    def test_oauth_activate_url_case_2(self):
        # hit url with email confirmed true --> will redirect ro invalid link page
        self.user_profile_1.email_confirmed = True
        self.user_profile_1.save()
        response = self.client.get(self.user_profile_1.get_activation_url)
        self.assertTemplateUsed(response, 'oauth/invalid_activation.html')
        self.user_profile_1.email_confirmed = False
        self.user_profile_1.save()

    def test_oauth_activate_url_case_3(self):
        # hit url with email confirmed false --> will logout user and redirect to profile page
        self.user_profile_1.email_confirmed = False
        self.user_profile_1.save()
        self.client.force_login(self.user_1)
        response = self.client.get(self.user_profile_1.get_activation_url, follow=True)
        self.user_profile_1 = UserProfile.objects.get(user=self.user_1)
        self.assertTrue(self.user_profile_1.email_confirmed)
        self.assertRedirects(response, reverse('login') + "?next=" + self.user_profile_1.get_absolute_url())
        self.client.logout()

    def test_oauth_activate_url_case_4(self):
        # hit url with email wrong token and uidb64 --> invalid token
        response = self.client.get(reverse('oauth:activate', kwargs={'uidb64': b'YQ', 'token': 'abc-abd'}))
        self.assertTemplateUsed(response, 'oauth/invalid_activation.html')

    def test_oauth_sociallink_add_case_1(self):
        # social link add without logged in user --> ask for login
        data = {'social_media': ['TW'], 'link': ['https://iitj.ac.in']}
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-add'))

    def test_oauth_sociallink_add_case_2(self):
        # social link add with logged in user --> will create object and will redirect to profile page
        self.client.force_login(self.user_1)
        data = {'social_media': ['TW'], 'link': ['https://iitj.ac.in']}
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
        self.assertTrue(SocialLink.objects.filter(user=self.user_1, social_media='TW').exists())
        self.client.logout()

    def test_oauth_sociallink_add_case_3(self):
        # social link add which already exist --> will do nothing and remain on that page
        self.client.force_login(self.user_1)
        data = {'social_media': ['TW'], 'link': ['https://facebook.com']}
        self.link_1 = SocialLink.objects.create(user=self.user_1, social_media='TW', link='https://iitj.ac.in')
        response = self.client.post(reverse('oauth:link-add'), data, follow=True)
        self.assertTemplateUsed(response, 'oauth/sociallink_create.html')
        self.assertEqual(SocialLink.objects.get(user=self.user_1, social_media='TW').link, 'https://iitj.ac.in')
        self.client.logout()

    def test_oauth_sociallink_update_case_1(self):
        # social link update without logged in user --> ask for login
        kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        data = {'social_media': ['TW'], 'link': ['https://twitter.com']}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-edit', kwargs=kwargs))

    # TODO: resolve travis fail
    # def test_oauth_sociallink_update_case_2(self):
    # social link edit with user own it and exist --> will change it and redirect to profile page
    # data = {'social_media': ['YT'], 'link': ['https://twitter.com']}
    # kwargs = {'username': self.user_1.username, 'social_media': 'YT'}
    # self.client.force_login(self.user_1)
    # response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
    # self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
    # self.assertEqual(SocialLink.objects.get(user=self.user_1, social_media='YT').link, 'https://twitter.com')
    # self.link_1.save()
    # self.client.logout()

    def test_oauth_sociallink_update_case_3(self):
        # social link edit & social media not exist --> will not create object and redirect to 404 page
        data = {'social_media': ['FB'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_1.username, 'social_media': 'FB'}
        self.client.force_login(user=self.user_1)
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data, follow=True)
        self.assertFalse(SocialLink.objects.filter(user=self.user_1, social_media='FB').exists())
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_oauth_sociallink_update_case_4(self):
        # social link edit & user doesn't own & media doesn't exist --> response 404
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        self.client.force_login(user=self.user_1)
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_oauth_sociallink_update_case_5(self):
        SocialLink.objects.create(user=self.user_2, social_media='TW', link='https://twitter.com')
        # social link edit & user doesn't own & media exist --> response Permission Denied
        self.client.force_login(user=self.user_1)
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        response = self.client.post(reverse('oauth:link-edit', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        SocialLink.objects.get(user=self.user_2, social_media="TW").delete()
        self.client.logout()

    def test_oauth_sociallink_delete_case_1(self):
        # social link delete without logged in user --> ask for login
        kwargs = {'username': self.user_1.username, 'social_media': 'TW'}
        data = {'social_media': ['TW']}
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:link-delete', kwargs=kwargs))

    # TODO: resolve travis fail
    # def test_oauth_sociallink_delete_case_2(self):
    # social link delete with user own it and exist --> will delete it and redirect to profile page
    # kwargs = {'username': self.user_1.username, 'social_media': 'YT'}
    # self.client.force_login(self.user_1)
    # response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), follow=True)
    # self.assertRedirects(response, self.user_1.userprofile.get_absolute_url())
    # self.assertFalse(SocialLink.objects.filter(user=self.user_1, social_media='YT').exists())
    # self.link_1.save()
    # self.client.logout()

    def test_oauth_sociallink_delete_case_3(self):
        # social link delete & social media not exist --> redirect to 404 page
        kwargs = {'username': self.user_1.username, 'social_media': 'as'}
        self.client.force_login(user=self.user_1)
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), {}, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_oauth_sociallink_delete_case_4(self):
        # social link delete & user doesn't own & media doesn't exist --> response 404
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        self.client.force_login(user=self.user_1)
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_oauth_sociallink_delete_case_5(self):
        SocialLink.objects.create(user=self.user_2, social_media='TW', link='https://twitter.com')
        # social link delete & user doesn't own & media exist --> response Permission Denied
        data = {'social_media': ['TW'], 'link': ['http://facebook.com']}
        kwargs = {'username': self.user_2.username, 'social_media': 'TW'}
        self.client.force_login(user=self.user_1)
        response = self.client.post(reverse('oauth:link-delete', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        SocialLink.objects.get(user=self.user_2, social_media="TW").delete()
        self.client.logout()

    def test_oauth_profile_detail_case_1(self):
        # profile detail url & user is not logged in --> login url
        response = self.client.get(self.user_profile_1.get_absolute_url(), follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + self.user_profile_1.get_absolute_url())

    def test_oauth_profile_detail_case_3(self):
        # profile detail url & user has user profile data --> template used oauth/profile_detail.html
        self.client.force_login(self.user_1)
        response = self.client.get(self.user_profile_1.get_absolute_url(), follow=True)
        self.assertTemplateUsed(response, 'oauth/profile_detail.html')
        self.client.logout()

    def test_oauth_profile_edit_case_1(self):
        # profile edit without logged in user --> ask for login
        data = {'phone': ['0987654321'], 'year': ['1'], 'hometown': ['XYZ'], 'skills': [''], 'about': ['']}
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_1.roll}), data, follow=True)
        self.assertRedirects(response, reverse('login') + "?next=" + reverse('oauth:edit',
                                                                             kwargs={'roll': self.user_profile_1.roll}))

    def test_oauth_profile_edit_case_3(self):
        # profile edit & user doesn't own it & profile not exist --> response 404
        self.client.force_login(self.user_1)
        data = {'phone': ['0987654321'], 'year': ['1'], 'hometown': ['XYZ'], 'skills': [''], 'about': ['']}
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': 'B11CS011'}), data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_oauth_profile_edit_case_4(self):
        # profile edit & user doesn't own & profile exist --> response permission denied
        self.user_profile_2 = UserProfile.objects.create(user=self.user_2, roll='B17CS000', dob=get_random_date(),
                                                         phone='1234567890', branch='CSE')
        data = {'phone': ['0987654321'], 'year': ['1'], 'hometown': ['XYZ'], 'skills': [''], 'about': ['']}
        self.client.force_login(self.user_1)
        response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_2.roll}), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.user_profile_2.delete()
        self.client.logout()

    # TODO: resolve travis fail
    # def test_oauth_profile_edit_case_5(self):
    #     profile edit & user own it --> will change it and redirect to detail page
    # data = {'phone': ['0987654321'], 'year': ['1'], 'hometown': ['XYZ'], 'skills': [''], 'about': ['']}
    # self.client.force_login(self.user_1)
    # response = self.client.post(reverse('oauth:edit', kwargs={'roll': self.user_profile_1.roll}), data, follow=True)
    # self.assertRedirects(response, reverse('oauth:detail', kwargs={'roll': self.user_profile_1.roll}))
    # self.assertEqual(UserProfile.objects.get(user=self.user_1).phone, '0987654321')
    # self.client.logout()

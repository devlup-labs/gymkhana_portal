from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from test.test_assets import get_random_date, get_temporary_image, TEST_MEDIA_ROOT
from main.models import FacultyAdvisor, Society, Club, Activity, Senate, SenateMembership, SocialLink, Contact
from main.forms import ContactForm
from oauth.models import UserProfile


class MainModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fa = FacultyAdvisor.objects.create(name='test_fa')
        cls.society_1 = Society.objects.create(name='society', slug='society_1', year='2000', is_active=True)
        cls.club_1 = Club.objects.create(name='club_1', society=cls.society_1, slug='club_1')
        cls.activity_1 = Activity.objects.create(name='activity_1', club=cls.club_1)
        cls.user_1 = User.objects.create(username='user_1')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, dob=get_random_date(), roll='B00CS000')
        cls.senate_1 = Senate.objects.create(name='senate_1', year='2000', slug='senate_1')
        cls.senate_membership_1 = SenateMembership.objects.create(senate=cls.senate_1, userprofile=cls.user_profile_1)
        cls.social_link_1 = SocialLink.objects.create(club=cls.club_1, social_media='YT', link='https://youtube.com')
        cls.social_link_2 = SocialLink.objects.create(club=cls.club_1, social_media='AB', link='https://youtube.com')
        cls.contact_1 = Contact.objects.create(name='user')

    def test_faculty_advisor_str_method(self):
        """Test Faculty Advisor __str__ method"""
        self.assertEqual(self.fa.__str__(), 'test_fa')

    def test_society_str_method(self):
        """Test Society __str__ method"""
        self.assertEqual(self.society_1.__str__(), 'society - 2000')

    def test_club_str_method(self):
        """Test Club __str__ method"""
        self.assertEqual(self.club_1.__str__(), 'club_1 - 2000')

    def test_club_year_property(self):
        """Test club year property"""
        self.assertEqual(self.club_1.year, '2000')

    def test_club_active_property(self):
        """Test club is_active property"""
        self.assertTrue(self.club_1.is_active)

    def test_activity_str_method(self):
        """Test activity __str__ method"""
        self.assertEqual(self.activity_1.__str__(), 'activity_1 - club_1')

    def test_senate_str_method(self):
        """Test senate __str__ method"""
        self.assertEqual(self.senate_1.__str__(), 'senate_1 - 2000')

    def test_senate_membership_str_method(self):
        """Test senate membership __str__ method"""
        self.assertEqual(self.senate_membership_1.__str__(), '')

    def test_social_link_str_method_case_1(self):
        """Test social link __str__ method case: known choice"""
        self.assertEqual(self.social_link_1.__str__(), 'club_1 - YouTube')

    def test_social_link_str_method_case_2(self):
        """Test social link __str__ method case: unknown choice"""
        self.assertEqual(self.social_link_2.__str__(), 'club_1 - AB')

    def test_social_link_get_fai_method_case_1(self):
        """Test social link get_fai method case: known choice"""
        self.assertEqual(self.social_link_1.get_fai(), 'fa fa-youtube')

    def test_social_link_get_fai_method_case_2(self):
        """Test social link get_fai method case: unknown choice"""
        self.assertEqual(self.social_link_2.get_fai(), 'fa fa-link')

    def test_social_link_get_am_ic_method_case_1(self):
        """Test social link get_sm_ic method case: known choice"""
        self.assertEqual(self.social_link_1.get_sm_ic(), 'yt-ic')

    def test_social_link_get_am_ic_method_case_2(self):
        """Test social link get_sm_ic method case: unknown choice"""
        self.assertEqual(self.social_link_2.get_sm_ic(), '')

    def test_contact_str_method(self):
        """Test contact _str__ method"""
        self.assertEqual(self.contact_1.__str__(), 'user - ')


class MainURLsTestCase(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUpTestData(cls):
        cls.test_image = get_temporary_image()

        cls.client = Client()

        cls.fa = FacultyAdvisor.objects.create(name='test_fa')
        cls.society_1 = Society.objects.create(name='society', slug='society_1', year='2000', is_active=True,
                                               cover=cls.test_image.name)
        cls.club_1 = Club.objects.create(name='club_1', society=cls.society_1, slug='club_1')
        cls.activity_1 = Activity.objects.create(name='activity_1', club=cls.club_1)
        cls.user_1 = User.objects.create(username='user_1')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, dob=get_random_date(), roll='B00CS000')
        cls.senate_1 = Senate.objects.create(name='senate_1', year='2000', slug='senate_1')
        cls.senate_membership_1 = SenateMembership.objects.create(senate=cls.senate_1, userprofile=cls.user_profile_1)
        cls.social_link_1 = SocialLink.objects.create(club=cls.club_1, social_media='YT', link='https://youtube.com')
        cls.social_link_2 = SocialLink.objects.create(club=cls.club_1, social_media='AB', link='https://youtube.com')
        cls.contact_1 = Contact.objects.create(name='user')

    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_url(self):
        """Test all main url with maintenance mode true"""
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 503)

        response = self.client.get(reverse('main:office-bearers'))
        self.assertEqual(response.status_code, 503)

        response = self.client.get(reverse('main:contact'))
        self.assertEqual(response.status_code, 503)

        response = self.client.get(reverse('main:contact_list'))
        self.assertEqual(response.status_code, 503)

        response = self.client.get(self.society_1.get_absolute_url())
        self.assertEqual(response.status_code, 503)

        response = self.client.get(self.senate_1.get_absolute_url())
        self.assertEqual(response.status_code, 503)

        response = self.client.get(self.club_1.get_absolute_url())
        self.assertEqual(response.status_code, 503)

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_1(self):
        """test all urls with maintenance mode false case: office_bearers"""
        response = self.client.get(reverse('main:office-bearers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/office.html')

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_2(self):
        """case: contact"""
        response = self.client.get(reverse('main:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_3(self):
        """case: contact"""
        data = {'name': 'ABC', 'email': 'abc@iitj.ac.in', 'phone': '9876543210', 'subject': 'abc',
                'message': 'xys'}
        response = self.client.post(reverse('main:contact'), data, follow=True)
        self.assertRedirects(response, reverse('main:contact'))

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_4(self):
        """case: contact list"""
        response = self.client.get(reverse('main:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact_list.html')

    @override_settings(MAINTENANCE_MODE=False, MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_main_app_urls_case_5(self):
        """case: society"""
        response = self.client.get(self.society_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/society.html')

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_6(self):
        """case: senate"""
        response = self.client.get(self.senate_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/senate.html')

    @override_settings(MAINTENANCE_MODE=False)
    def test_main_app_urls_case_7(self):
        """case: club"""
        response = self.client.get(self.club_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/club.html')

    @override_settings(MAINTENANCE_MODE=False, MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_main_app_urls_case_8(self):
        """case: index"""
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')


class MainFormsTestCase(TestCase):
    def test_contact_form(self):
        data = {'name': 'ABC', 'email': 'abc@iitj.ac.in', 'phone': '9876543210', 'subject': 'abc',
                'message': 'xys'}
        self.assertTrue(ContactForm(data=data).is_valid())
        response = self.client.post(reverse('main:contact'), data, follow=True)
        self.assertRedirects(response, reverse('main:contact'))

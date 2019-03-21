from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from main.models import FacultyAdvisor, Society, Club, Activity, Senate, SenateMembership, SocialLink, Contact
from main.forms import ContactForm
from oauth.models import UserProfile


class MainAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.fa = FacultyAdvisor.objects.create(name='test_fa')
        cls.society_1 = Society.objects.create(name='society', slug='society_1', year='2000', is_active=True)
        cls.club_1 = Club.objects.create(name='club_1', society=cls.society_1, slug='club_1')
        cls.activity_1 = Activity.objects.create(name='activity_1', club=cls.club_1)
        cls.user_1 = User.objects.create(username='user_1')
        cls.user_profile_1 = UserProfile.objects.create(user=cls.user_1, dob=timezone.now(), roll='B00CS000')
        cls.senate_1 = Senate.objects.create(name='senate_1', year='2000', slug='senate_1')
        cls.senate_membership_1 = SenateMembership.objects.create(senate=cls.senate_1, userprofile=cls.user_profile_1)
        cls.social_link_1 = SocialLink.objects.create(club=cls.club_1, social_media='YT', link='https://youtube.com')
        cls.social_link_2 = SocialLink.objects.create(club=cls.club_1, social_media='AB', link='https://youtube.com')
        cls.contact_1 = Contact.objects.create(name='user')

    def test_object_creation(self):
        self.assertEqual(self.fa.__str__(), 'test_fa')
        self.assertEqual(self.society_1.__str__(), 'society - 2000')
        self.assertEqual(self.club_1.__str__(), 'club_1 - 2000')
        self.assertEqual(self.club_1.year, '2000')
        self.assertTrue(self.club_1.is_active)
        self.assertEqual(self.activity_1.__str__(), 'activity_1 - club_1')
        self.assertEqual(self.senate_1.__str__(), 'senate_1 - 2000')
        self.assertEqual(self.senate_membership_1.__str__(), '')
        self.assertEqual(self.social_link_1.__str__(), 'club_1 - YouTube')
        self.assertEqual(self.social_link_2.__str__(), 'club_1 - AB')
        self.assertEqual(self.social_link_1.get_fai(), 'fa fa-youtube')
        self.assertEqual(self.social_link_2.get_fai(), 'fa fa-link')
        self.assertEqual(self.social_link_1.get_sm_ic(), 'yt-ic')
        self.assertEqual(self.social_link_2.get_sm_ic(), '')
        self.assertEqual(self.contact_1.__str__(), 'user - ')

    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_url(self):
        """test all url with maintenance mode true"""
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
    def test_main_app_urls(self):
        """test all urls with maintenance mode false"""
        response = self.client.get(reverse('main:office-bearers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/office.html')

        response = self.client.get(reverse('main:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')

        response = self.client.get(reverse('main:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact_list.html')

        response = self.client.get(self.society_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/society.html')

        response = self.client.get(self.senate_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/senate.html')

        response = self.client.get(self.club_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/club.html')

        # society has versatile image field whose photo file creating issue in main:index url problem so remove that
        # object while hitting that particular url and then create it
        self.society_1.delete()
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.society_1.save()

    def test_contact_form(self):
        data = {'name': 'ABC', 'email': 'abc@iitj.ac.in', 'phone': '9876543210', 'subject': 'abc',
                'message': 'xys'}
        self.assertTrue(ContactForm(data=data).is_valid())
        response = self.client.post(reverse('main:contact'), data, follow=True)
        self.assertRedirects(response, reverse('main:contact'))

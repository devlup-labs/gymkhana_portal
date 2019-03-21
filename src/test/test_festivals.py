from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.test.client import Client
from festivals.models import Festival, EventCategory, Event, SocialLink
from test.test_assets import get_temporary_image, get_temporary_html, TEST_TEMPLATES, TEST_MEDIA_ROOT


class FestivalsTestCase(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUpTestData(cls):
        # create test image in temporary folder of operating system
        cls.testImage = get_temporary_image()

        # create test html file
        cls.testHtml = get_temporary_html()

        # Create a client for test
        cls.client = Client()

        # Festival with published false and no event category list associated with it
        cls.festival_1 = Festival.objects.create(name='festival_1', slug='festival_1', photo=cls.testImage.name)
        cls.link = SocialLink.objects.create(festival=cls.festival_1, social_media='FB', link='iitj.ac.in')

        # Festival with published true and no events category list associated with it
        cls.festival_2 = Festival.objects.create(name='festival_2', slug='festival_2', published=True,
                                                 photo=cls.testImage.name)
        SocialLink.objects.create(festival=cls.festival_2, social_media='FB', link='iitj.ac.in')

        # Festival with published true and with events category list associated with it
        cls.festival_3 = Festival.objects.create(name='festival_3', slug='festival_3', published=True,
                                                 photo=cls.testImage.name)
        cls.event_category_1 = EventCategory.objects.create(name='event_category_1', slug='eventCategory-1',
                                                            festival=cls.festival_3)
        cls.event_1 = Event.objects.create(event_category=cls.event_category_1, name='event_1',
                                           slug='event-1', unique_id='event-1')
        SocialLink.objects.create(festival=cls.festival_3, social_media='FB', link='iitj.ac.in')

        # Festival with published true and with event category associated with it and with custom html true
        cls.festival_4 = Festival.objects.create(name='festival_4', slug='festival_4', published=True,
                                                 use_custom_html=True, custom_html=cls.testHtml.name.split('/')[-1],
                                                 photo=cls.testImage.name)
        cls.event_category_2 = EventCategory.objects.create(name='event_category_2', slug='eventCategory-2',
                                                            festival=cls.festival_4)
        cls.event_2 = Event.objects.create(event_category=cls.event_category_2, name='event_2',
                                           slug='event-2', unique_id='event-2')
        SocialLink.objects.create(festival=cls.festival_4, social_media='FB', link='iitj.ac.in')

    def test_festivals_object_creation(self):
        # Festival model
        self.assertEqual(self.festival_1.__str__(), "festival_1")
        self.assertEqual(self.festival_1.get_name_display(), "Festival_1")
        with self.assertRaises(ValidationError):
            Festival.objects.create(name='festival_5', use_custom_html=True).clean()

        # EventCategory model
        self.assertEqual(self.event_category_1.__str__(), "event_category_1")

        # Event model
        self.assertEqual(self.event_1.__str__(), "event_1")

        # SocialLink model
        self.assertEqual(self.link.__str__(), 'festival_1 - Facebook')
        link = SocialLink.objects.create(festival=self.festival_1, social_media='AB')
        self.assertEqual(link.get_fai(), 'fa fa-link')
        self.assertEqual(link.get_sm_ic(), '')

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls(self):
        # Hit all possible url of festival app without logged in client
        response = self.client.get(self.festival_1.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/coming_soon.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.festival_2.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/coming_soon.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.festival_3.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/index.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.festival_4.get_absolute_url())
        self.assertTemplateUsed(response, self.festival_4.custom_html.name)
        self.assertEqual(response.status_code, 200)

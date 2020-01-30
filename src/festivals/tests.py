from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, Client
from festivals.models import Festival, EventCategory, Event, SocialLink
from test.test_assets import TEST_MEDIA_ROOT, get_temporary_image, get_temporary_html, TEST_TEMPLATES


class FestivalsModelsTestCase(TestCase):
    @classmethod
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUpTestData(cls):
        # create test image in temporary folder of operating system
        cls.testImage = get_temporary_image()

        # create test html file
        cls.testHtml = get_temporary_html()

        # Festival with published false and no event category list associated with it
        cls.festival = Festival.objects.create(name='festival_1', slug='festival_1', photo=cls.testImage.name)
        cls.link = SocialLink.objects.create(festival=cls.festival, social_media='FB', link='iitj.ac.in')
        cls.event_category = EventCategory.objects.create(name='event_category_1', slug='eventCategory-1',
                                                          festival=cls.festival)
        cls.event = Event.objects.create(event_category=cls.event_category, name='event_1',
                                         slug='event-1', unique_id='event-1')

    def test_festival_str_method(self):
        """Test festival model __str__ method"""
        self.assertEqual(self.festival.__str__(), "festival_1")

    def test_festival_get_name_display_method(self):
        """Test festival model get name display method"""
        self.assertEqual(self.festival.get_name_display(), "Festival_1")

    def test_festival_clean_method(self):
        """Test festival model clea method test (object with custom html true but no html file associated with it)"""
        with self.assertRaises(ValidationError):
            Festival.objects.create(name='festival_5', use_custom_html=True).clean()

    def test_event_category_str_method(self):
        """Test event category model __str__ method"""
        self.assertEqual(self.event_category.__str__(), "event_category_1")

    def test_event_str_method(self):
        """Test event model __str__ method"""
        self.assertEqual(self.event.__str__(), "event_1")

    def test_social_link_str_method(self):
        """Test social link model __str__ method"""
        self.assertEqual(self.link.__str__(), 'festival_1 - Facebook')

    def test_social_link_get_fai_method(self):
        """Test social link model get_fai and get_sm_ic method"""
        link = SocialLink.objects.create(festival=self.festival, social_media='AB')
        self.assertEqual(link.get_fai(), 'fa fa-link')
        self.assertEqual(link.get_sm_ic(), '')


class FestivalsURLsTestCase(TestCase):
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

        # Festival with published true, without event category associated with it and with custom html true
        cls.festival_5 = Festival.objects.create(name='festival_5', slug='festival_5', published=True,
                                                 use_custom_html=True, custom_html=cls.testHtml.name.split('/')[-1],
                                                 photo=cls.testImage.name)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls_case_1(self):
        """Hit url with published=False"""
        response = self.client.get(self.festival_1.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/coming_soon.html')
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls_case_2(self):
        """Hit url with published=True and no events"""
        response = self.client.get(self.festival_2.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/coming_soon.html')
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls_case_3(self):
        """Hit url with published=True and with events"""
        response = self.client.get(self.festival_3.get_absolute_url())
        self.assertTemplateUsed(response, 'festivals/index.html')
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls_case_4(self):
        """Hit url with published=True and with events and custom_html=True"""
        response = self.client.get(self.festival_4.get_absolute_url())
        self.assertTemplateUsed(response, self.festival_4.custom_html.name)
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT, TEMPLATES=TEST_TEMPLATES, MAINTENANCE_MODE=False)
    def test_festivals_urls_case_5(self):
        """Hit url with published=True, without events and custom_html=True"""
        response = self.client.get(self.festival_5.get_absolute_url())
        self.assertTemplateUsed(response, self.festival_5.custom_html.name)
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from events.models import Event
from test.test_assets import get_random_date


class EventsModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create event object
        cls.event_1 = Event.objects.create(name='event_1', date=get_random_date())

    def test_event_str_method(self):
        """Test event model __str__ method"""
        self.assertEqual(self.event_1.__str__(), 'event_1')

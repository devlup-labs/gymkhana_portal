from django.test import TestCase
from events.models import Event
from django.utils import timezone


class EventsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Test event
        cls.event_1 = Event.objects.create(name='test_event_1', date=timezone.now())

    def test_events(self):
        # Events model
        self.assertEqual(self.event_1.__str__(), 'test_event_1')

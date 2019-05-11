from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from gymkhana.wsgi import application


class WSGITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory()

    @override_settings(MAINTENANCE_MODE=False)
    def test_wsgi_request(self):
        request = self.request.get(reverse('main:index'))
        response = application.get_response(request)
        self.assertEqual(response.status_code, 200)

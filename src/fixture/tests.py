from django.core.management import call_command
from django.test import TestCase, override_settings
from fixture.management.commands.createfixture import Command
from django.conf import settings


class FixtureTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.args = []
        cls.opts = {}

    @override_settings(DEBUG=True)
    def test_command(self):
        args = self.args
        opts = self.opts
        settings.DEBUG = True
        # run command for first time
        call_command('createfixture', *args, **opts)

        # run command for second time to see if it generates error or not
        call_command('createfixture', *args, **opts)

        settings.DEBUG = False

    def test_create_object_function(self):
        with self.assertRaises(ValueError):
            Command.create_objects(None)

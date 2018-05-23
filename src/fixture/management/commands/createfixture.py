from django.core.management.base import BaseCommand, CommandError
import  os

class Command(BaseCommand):
    help = 'Generates dummy data for testing purposes'

    def handle(self, *args, **options):
        os.chdir("fixture")
        exec(open('fixture.py').read())
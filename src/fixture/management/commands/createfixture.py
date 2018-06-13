from django.core.management.base import BaseCommand

from fixture.activityfixture import ActivityFactory
from fixture.contactfixture import ContactFactory
from fixture.eventfixture import EventFactory
from fixture.festivalfixture import FestivalFactory
from fixture.senatemembershipfixture import SenateMembershipFactory
from fixture.answerfixture import AnswerFactory


class Command(BaseCommand):
    help = 'Generates dummy data for testing purposes'

    def handle(self, *args, **options):
        self.create_fixtures()

    def create_fixtures(self):
        # self.create_objects(UserProfileFactory, 50)
        # self.create_objects(SocietyFactory)
        # self.create_objects(ClubFactory, 10)
        self.create_objects(ActivityFactory)
        self.create_objects(EventFactory)
        self.create_objects(FestivalFactory, 4)
        # self.create_objects(SenateFactory, 1)
        self.create_objects(SenateMembershipFactory)
        self.create_objects(ContactFactory)
        # self.create_objects(TopicFactory)
        self.create_objects(AnswerFactory, 20)

    @staticmethod
    def create_objects(klass=None, object_count=5):
        if klass is not None:
            for i in range(object_count):
                klass.create()
        else:
            raise ValueError("klass argument cannot be null")

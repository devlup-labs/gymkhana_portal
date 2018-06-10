from django.core.management.base import BaseCommand
from fixture.activityfixture import ActivityFactory
from fixture.contactfixture import ContactFactory
from fixture.eventfixture import EventFactory
from fixture.festivalfixture import FestivalFactory
from fixture.senatemembershipfixture import MemberWithSenateFactory
from fixture.answerfixture import AnswerFactory
from fixture.topicfixture import TopicFactory
from fixture.clubfixture import ClubFactory
import random
from main.models import UserProfile


class Command(BaseCommand):
    help = 'Generates dummy data for testing purposes'

    def handle(self, *args, **options):
        self.create_fixtures()

    def create_fixtures(self):
        self.create_objects(ActivityFactory)
        self.create_objects(EventFactory)
        self.create_objects(FestivalFactory, 4)
        self.create_objects(ClubFactory, m2m=True)
        self.create_objects(MemberWithSenateFactory)
        self.create_objects(ContactFactory)
        self.create_objects(AnswerFactory, 20, m2m=True)
        self.create_objects(TopicFactory, 5, m2m=True)

    @staticmethod
    def create_objects(klass=None, object_count=5, m2m=False):
        if klass is not None and m2m is False:
            for i in range(object_count):
                klass.create()
        elif klass is not None and m2m is True:
            for i in range(object_count):
                multiple_users = (UserProfile.objects.get(roll='B16CS%d' % random.randint(0, 10)),
                                  UserProfile.objects.get(roll='B16CS%d' % random.randint(10, 20)),
                                  )
                klass.create(users=multiple_users)
        else:
            raise ValueError("klass argument cannot be null")

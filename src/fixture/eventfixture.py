import factory
from fixture.clubfixture import ClubFactory
from test.test_assets import get_random_date


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'events.Event'

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=30)
    location = factory.Faker('city')
    date = get_random_date()
    club = factory.SubFactory(ClubFactory)

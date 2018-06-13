import factory
from fixture.clubfixture import ClubFactory


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Activity'

    name = factory.Faker('sentence', nb_words=2)
    club = factory.SubFactory(ClubFactory)
    description = factory.Faker('sentence', nb_words=30)
    custom_html = factory.Faker('sentence', nb_words=20)

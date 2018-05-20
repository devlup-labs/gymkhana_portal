
import factory
import random
from main.models import Club

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'events.Event'

    name = factory.Faker('sentence', nb_words=4)
    description =factory.Faker('sentence', nb_words=30)
    location =factory.Faker('city')
    date = factory.Faker('date')
    club = Club.objects.all()[random.randint(0, 3)]

EventFactory()
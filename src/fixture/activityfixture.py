import factory
import random
from main.models import Club


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Activity'

    name = factory.Faker('sentence', nb_words=2)
    club = Club.objects.all()[random.randint(0, 3)]
    description = factory.Faker('sentence', nb_words=30)
    custom_html = factory.Faker('sentence', nb_words=20)


ActivityFactory()
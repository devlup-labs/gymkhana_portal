import factory
import random


class FestivalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Festival'

    name = random.choice(['IGNS', 'VRCHS', 'SPNDN', 'NMBL'])
    # photo = VersatileImageField(upload_to='festival')
    about = factory.Faker('sentence', nb_words=30)
    link = factory.Faker('url')

import factory
import random


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Contact'

    name = factory.Faker('sentence', nb_words=4)
    email = factory.Faker('email')
    phone = random.randint(80000000, 99999999)
    subject = factory.Faker('sentence', nb_words=4)
    message = factory.Faker('sentence', nb_words=30)

import factory
import random

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]


class FestivalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Festival'

    name = random.choice(['IGNS', 'VRCHS', 'SPNDN', 'NMBL'])
    photo = factory.django.ImageField(color=random.choice(COLOUR))
    about = factory.Faker('sentence', nb_words=30)
    link = factory.Faker('url')

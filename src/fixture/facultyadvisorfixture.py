import factory
import random

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]


class FacultyAdvisorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.FacultyAdvisor'

    name = factory.Faker('sentence', nb_words=2)
    avatar = factory.django.ImageField(color=random.choice(COLOUR))

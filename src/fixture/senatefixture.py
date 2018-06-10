import factory
import random
from fixture.facultyadvisorfixture import FacultyAdvisorFactory

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]

SKIN = [
    'white-skin', 'black-skin', 'cyan-skin', 'mdb-skin', 'deep-purple-skin', 'navy-blue-skin', 'pink-skin',
    'indigo-skin', 'light-blue-skin', 'grey-skin']


class SenateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Senate'

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=30)
    cover = factory.django.ImageField(color=random.choice(COLOUR))
    skin = random.choice(SKIN)
    # members = models.ManyToManyField(UserProfile, through='SenateMembership',through_fields=('senate', 'userprofile'))
    coordinator_student = factory.SubFactory(FacultyAdvisorFactory)
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Sequence(lambda n: 'senate-%d' % n)
    is_active = True
    year = random.randint(2009, 2018)

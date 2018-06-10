import factory
import random
from fixture.userfixture import UserProfileFactory
from fixture.facultyadvisorfixture import FacultyAdvisorFactory

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]
SKIN = [
    'white-skin', 'black-skin', 'cyan-skin', 'mdb-skin', 'deep-purple-skin', 'navy-blue-skin', 'pink-skin',
    'indigo-skin', 'light-blue-skin', 'grey-skin']


class SocietyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Society'
        django_get_or_create = ('name', 'description', 'secretary', 'custom_html', 'slug', 'is_active', 'year',)

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=30)
    cover = factory.django.ImageField(color=random.choice(COLOUR))
    skin = random.choice(SKIN)
    secretary = factory.SubFactory(UserProfileFactory)
    joint_secretary = factory.SubFactory(UserProfileFactory)
    mentor = factory.SubFactory(UserProfileFactory)
    faculty_advisor = factory.SubFactory(FacultyAdvisorFactory)
    # gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Sequence(lambda n: 'soc-%d' % n)
    is_active = True
    year = random.randint(2009, 2018)

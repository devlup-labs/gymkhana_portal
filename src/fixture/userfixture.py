import factory
import random
from test.test_assets import get_random_date

SKILL = ['machinist', 'pipefitter', 'welder', 'tool and die maker', 'boilermaker',
         'millwright', 'ironworker', 'plumber', 'electrician', 'auto mechanic',
         'carpenter', 'glazier', 'rigger', 'patternmaker', 'sheetmetal worker',
         'tile setter', 'pipelayer', 'model maker', 'brickmason', 'steel worker']

COLOUR = ["yellow", "black", "purple", "red", "orange", "green", '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1',
          '#c6dbef', '#deebf7', '#f7fbff'
          ]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username', 'is_active')

    username = factory.Sequence(lambda n: 'user%d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = True
    is_active = True
    email = factory.Faker('email')


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'oauth.UserProfile'
        django_get_or_create = (
            'user', 'roll', 'dob', 'gender', 'prog', 'year', 'phone', 'hometown', 'branch', 'skills', 'about',)

    email_confirmed = True
    prog = random.choice(['BT', 'MT', 'MSc', 'PhD'])
    roll = factory.Sequence(lambda n: 'B16CS%d' % n)
    user = factory.SubFactory(UserFactory)
    dob = get_random_date()
    gender = random.choice(['M', 'F'])
    year = random.choice(['1', '2', '3', '4', '5'])
    phone = random.randint(6000000000, 9999999999)
    avatar = factory.django.ImageField(color=random.choice(COLOUR))
    cover = factory.django.ImageField(color=random.choice(COLOUR))
    hometown = factory.Faker('city')
    branch = random.choice(['CSE', 'EE', 'ME'])
    skills = random.choice(SKILL) + ',' + random.choice(SKILL) + ',' + random.choice(SKILL)
    about = factory.Faker('sentence', nb_words=5)

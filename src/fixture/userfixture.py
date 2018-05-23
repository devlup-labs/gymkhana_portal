import factory
import random

SKILL = ['machinist', 'pipefitter', 'welder', 'tool and die maker', 'boilermaker',
         'millwright', 'ironworker', 'plumber', 'electrician', 'auto mechanic',
         'carpenter', 'glazier', 'rigger', 'patternmaker', 'sheetmetal worker',
         'tile setter', 'pipelayer', 'model maker', 'brickmason', 'steel worker']


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username', 'is_active')

    username = random.randint(100000000000000, 999999999999999)
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
    roll = random.randint(100000000000000, 999999999999999)
    user = UserFactory()
    dob = factory.Faker('date')
    gender = random.choice(['M', 'F'])
    year = random.choice(['1', '2', '3', '4', '5'])
    phone = random.randint(80000000, 99999999)
    # avatar = VersatileImageField(upload_to='avatar', blank=True, null=True)
    # cover = VersatileImageField(upload_to='cover', blank=True, null=True)
    hometown = factory.Faker('city')
    branch = random.choice(['CSE', 'EE', 'ME'])
    skills = random.choice(SKILL) + ',' + random.choice(SKILL) + ',' + random.choice(SKILL)
    about = factory.Faker('sentence', nb_words=5)


UserProfileFactory()

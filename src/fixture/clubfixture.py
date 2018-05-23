import factory
import random
from oauth.models import UserProfile
from main.models import Society


class ClubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Club'
        django_get_or_create = ('name',)

    name = factory.Faker('sentence', nb_words=2)
    society = Society.objects.all()[random.randint(0, 3)]
    ctype = random.choice(['C', 'T'])
    description = factory.Faker('sentence', nb_words=30)
    # cover = VersatileImageField(upload_to='club_%Y', blank=True, null=True,
    # skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
    captain = UserProfile.objects.all()[random.randint(0, 30)]
    vice_captain_one = UserProfile.objects.all()[random.randint(0, 30)]
    vice_captain_two = UserProfile.objects.all()[random.randint(0, 30)]
    mentor = UserProfile.objects.all()[random.randint(0, 30)]
    # core_members.objects.set(UserProfile.objects.all()[random.randint(0, 30)])
    # gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
    resources_link = factory.Faker('url')
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Faker('sentence', nb_words=1)
    published = True


ClubFactory()

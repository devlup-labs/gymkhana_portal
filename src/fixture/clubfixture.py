import factory
import random
from .societyfixture import SocietyFactory
from .userfixture import UserProfileFactory


class ClubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Club'
        django_get_or_create = ('name',)

    name = factory.Faker('sentence', nb_words=2)
    society = factory.SubFactory(SocietyFactory)
    ctype = random.choice(['C', 'T'])
    description = factory.Faker('sentence', nb_words=30)
    # cover = VersatileImageField(upload_to='club_%Y', blank=True, null=True,
    # skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
    captain = factory.SubFactory(UserProfileFactory)
    vice_captain_one = factory.SubFactory(UserProfileFactory)
    vice_captain_two = factory.SubFactory(UserProfileFactory)
    mentor = factory.SubFactory(UserProfileFactory)
    # core_members.objects.set(UserProfile.objects.all()[random.randint(0, 30)])
    # gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
    resources_link = factory.Faker('url')
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Sequence(lambda n: 'club-%d' % n)
    published = True

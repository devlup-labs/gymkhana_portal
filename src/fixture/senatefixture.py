import factory
import random


class SenateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Senate'

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=30)
    # cover = VersatileImageField('Cover', upload_to='society_%Y', help_text="Upload high quality picture")
    # skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
    # members = models.ManyToManyField(UserProfile, through='SenateMembership',
    # through_fields=('senate', 'userprofile'))
    # coordinator_student = models.ForeignKey(FacultyAdvisor, blank=True, null=True, default=None,
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Sequence(lambda n: 'senate-%d' % n)
    is_active = True
    year = random.randint(2009, 2018)

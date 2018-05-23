import factory
import random
from oauth.models import UserProfile


class SocietyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.Society'
        django_get_or_create = ('name', 'description', 'secretary', 'custom_html', 'slug', 'is_active', 'year',)

    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=30)
    # cover = VersatileImageField('Cover', upload_to='society_%Y', help_text="Upload high quality picture")
    # skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
    secretary = UserProfile.objects.all()[random.randint(0, 30)]
    joint_secretary = UserProfile.objects.all()[random.randint(0, 30)]
    mentor = UserProfile.objects.all()[random.randint(0, 30)]
    # faculty_advisor = models.ForeignKey(FacultyAdvisor, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    # gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
    custom_html = factory.Faker('sentence', nb_words=20)
    slug = factory.Faker('sentence', nb_words=1)
    is_active = True
    year = random.randint(2009, 2018)

SocietyFactory()
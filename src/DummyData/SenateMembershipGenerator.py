
import factory
import random
from main.models import Senate
from oauth.models import UserProfile

class SenateMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.SenateMembership'
    senate = Senate.objects.all()[0]
    userprofile = UserProfile.objects.all()[random.randint(0, 30)]
    role = random.choice(['SECY', 'SER'])
    year = random.choice(['1', '2', '3', '4'])

SenateMembershipFactory()
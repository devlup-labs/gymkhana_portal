import factory
import random
from fixture.senatefixture import SenateFactory
from fixture.userfixture import UserProfileFactory


class SenateMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.SenateMembership'

    senate = factory.SubFactory(SenateFactory)
    userprofile = factory.SubFactory(UserProfileFactory)
    role = random.choice(['SECY', 'SER'])
    year = random.choice(['1', '2', '3', '4'])


class MemberWithSenateFactory(UserProfileFactory):
    members = factory.RelatedFactory(SenateMembershipFactory, 'userprofile')

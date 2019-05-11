import factory
import random
from fixture.userfixture import UserProfileFactory

TAG = ['android', 'win', 'ios', 'mac', 'tv', 'mi', 'cube', 'django', 'python', 'c', 'c++', 'perl', 'neo4j'

       ]


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Topic'

    author = factory.SubFactory(UserProfileFactory)
    category = random.choice(['Q', 'F'])
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('sentence', nb_words=30)
    tags = random.choice(TAG) + ',' + random.choice(TAG) + ',' + random.choice(TAG)
    slug = factory.Sequence(lambda n: 'topic-%d' % n)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:  # pragma: no use
            return

        if extracted:
            for user in extracted:
                self.upvotes.add(user)

import factory
import random
from fixture.userfixture import UserProfileFactory


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Topic'

    author = factory.SubFactory(UserProfileFactory)
    category = random.choice(['Q', 'F'])
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('sentence', nb_words=30)
    # tags = models.CharField(max_length=30, blank=True, null=True, default=None)
    # upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='topic_upvotes')
    slug = factory.Sequence(lambda n: 'topic-%d' % n)

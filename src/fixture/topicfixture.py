import factory
import random
from oauth.models import UserProfile

class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Topic'

    author = UserProfile.objects.all()[random.randint(0, 30)]
    category = random.choice(['Q', 'F'])
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('sentence', nb_words=30)
    # tags = models.CharField(max_length=30, blank=True, null=True, default=None)
    # upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='topic_upvotes')
    slug = factory.Faker('sentence', nb_words=1)


TopicFactory()
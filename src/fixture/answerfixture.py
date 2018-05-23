
import factory
import random
from oauth.models import UserProfile
from forum.models import Topic

class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Answer'

    topic = Topic.objects.all()[random.randint(0, 3)]
    author = UserProfile.objects.all()[random.randint(0, 30)]
    content = factory.Faker('sentence', nb_words=100)
    # upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='answer_upvotes')


AnswerFactory()
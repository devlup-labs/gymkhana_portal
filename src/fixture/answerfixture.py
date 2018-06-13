import factory
from fixture.topicfixture import TopicFactory
from fixture.userfixture import UserProfileFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Answer'

    topic = factory.SubFactory(TopicFactory)
    author = factory.SubFactory(UserProfileFactory)
    content = factory.Faker('sentence', nb_words=100)
    # upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='answer_upvotes')

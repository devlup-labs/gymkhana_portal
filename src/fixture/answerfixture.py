import factory
from fixture.topicfixture import TopicFactory
from fixture.userfixture import UserProfileFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Answer'

    topic = factory.SubFactory(TopicFactory)
    author = factory.SubFactory(UserProfileFactory)
    content = factory.Faker('sentence', nb_words=100)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:  # pragma: no use
            return

        if extracted:
            for user in extracted:
                self.upvotes.add(user)

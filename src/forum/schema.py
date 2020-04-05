import graphene
from graphene import relay, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation

from forum.forms import TopicForm
from forum.models import Topic, Answer
from oauth.models import UserProfile
from oauth.schema import UserProfileNode


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        fields = '__all__'
        filter_fields = ()
        interfaces = (relay.Node,)


class TopicNode(DjangoObjectType):
    class Meta:
        model = Topic
        fields = '__all__'
        filter_fields = ()
        interfaces = (relay.Node,)

    @classmethod
    def search(cls, query, indfo):
        return cls._meta.model.objects.search(query)

from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType

from oauth.models import UserProfile


class UserNode(DjangoObjectType):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'userprofile')
        model = User
        interfaces = (relay.Node,)


class UserProfileNode(DjangoObjectType):
    user = UserNode()

    class Meta:
        filter_fields = []
        model = UserProfile
        interfaces = (relay.Node,)

    @classmethod
    def search(cls, query, info):
        return cls._meta.model.objects.search(query)

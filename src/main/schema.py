from graphene import relay

from main.models import Society, Club
from graphene_django import DjangoObjectType


class SocietyNode(DjangoObjectType):
    class Meta:
        model = Society
        fields = '__all__'
        interfaces = (relay.Node,)


class ClubNode(DjangoObjectType):
    class Meta:
        model = Club
        fields = '__all__'
        interfaces = (relay.Node,)

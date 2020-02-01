from graphene import relay

from main.models import Society, Club
from graphene_django import DjangoObjectType


class SocietyNode(DjangoObjectType):
    class Meta:
        model = Society
        fields = ('name', 'slug', 'secretary', 'joint_secretary', 'mentor', 'club_set', )
        filter_fields = ('slug', )
        interfaces = (relay.Node,)


class ClubNode(DjangoObjectType):
    class Meta:
        model = Club
        fields = '__all__'
        filter_fields = ('slug', )
        interfaces = (relay.Node,)

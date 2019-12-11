from graphene_django.filter import DjangoFilterConnectionField
from oauth.schema import UserProfileNode


class Query(object):
    all_user_profiles = DjangoFilterConnectionField(UserProfileNode)

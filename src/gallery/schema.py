from graphene import ObjectType, String, List


class RenditionType(ObjectType):
    name = String()
    url = String()


class ImageType(ObjectType):
    sizes = List(RenditionType)

import graphene


class TagObjectType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()

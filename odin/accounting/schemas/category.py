import graphene


class CategoryObjectType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()

import graphene


class EventObjectType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    init_date = graphene.DateTime()
    end_date = graphene.DateTime()

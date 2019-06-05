import graphene


class WalletObjectType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    initial_balance = graphene.Int()
    balance = graphene.Int()
    created = graphene.DateTime()

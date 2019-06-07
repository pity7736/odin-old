import graphene

from odin.accounting.models.movement import MovementTypeEnum
from .event import EventObjectType
from .category import CategoryObjectType
from .wallet import WalletObjectType


MovementType = graphene.Enum.from_enum(MovementTypeEnum)


class MovementObjectType(graphene.ObjectType):
    id = graphene.Int()
    type = MovementType()
    date = graphene.Date()
    value = graphene.Int()
    note = graphene.String()
    category = graphene.Field(CategoryObjectType)
    wallet = graphene.Field(WalletObjectType)
    event = graphene.Field(EventObjectType)

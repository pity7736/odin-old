import graphene

from .category import CategoryObjectType
from odin.accounting.models.movement import MovementTypeEnum


MovementType = graphene.Enum.from_enum(MovementTypeEnum)


class MovementObjectType(graphene.ObjectType):
    id = graphene.Int()
    type = MovementType()
    date = graphene.Date()
    value = graphene.Int()
    note = graphene.String()
    category = graphene.Field(CategoryObjectType)

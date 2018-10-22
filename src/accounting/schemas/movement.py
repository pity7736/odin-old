import graphene

from .category import CategoryObjectType
from src.accounting.models.movement import MovementTypeEnum


class MovementObjectType(graphene.ObjectType):
    id = graphene.Int()
    type = graphene.Enum.from_enum(MovementTypeEnum)()
    date = graphene.Date()
    value = graphene.Int()
    note = graphene.String()
    category = graphene.Field(CategoryObjectType)

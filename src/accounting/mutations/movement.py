import graphene

from src.accounting.models import Movement
from src.accounting.schemas import MovementObjectType
from src.accounting.schemas.movement import MovementType


class MovementInput(graphene.InputObjectType):
    type = MovementType()
    date = graphene.Date()
    value = graphene.Int()
    note = graphene.String()
    category_id = graphene.Int()


class CreateMovementMutation(graphene.Mutation):
    movement =graphene.Field(MovementObjectType)

    class Arguments:
        data = MovementInput(required=True)

    @staticmethod
    async def mutate(root, info, data):
        movement = Movement(**data)
        await movement.save()
        return CreateMovementMutation(MovementObjectType(
            id=movement.id,
            type=movement.type,
            date=movement.date,
            value=movement.value,
            note=movement.note,
            category=await movement.get_category()
        ))


import asyncio
import datetime

import graphene

from odin.accounting.models import Movement, Tag
from odin.accounting.models.movement import MovementTypeEnum
from odin.accounting.schemas import MovementObjectType
from odin.auth.decorators import login_required


class ExpenseInput(graphene.InputObjectType):
    date = graphene.Date()
    value = graphene.Int(required=True)
    note = graphene.String()
    category_id = graphene.Int(required=True)
    wallet_id = graphene.Int(required=True)
    event_id = graphene.Int()
    tags = graphene.List(graphene.Int)


class CreateExpenseMutation(graphene.Mutation):
    expense = graphene.Field(MovementObjectType)

    class Arguments:
        data = ExpenseInput(required=True)

    @staticmethod
    @login_required
    async def mutate(root, info, data):
        data['type'] = MovementTypeEnum.EXPENSE.value
        data.setdefault('date', datetime.date.today())
        movement = Movement(**data)
        await movement.save()
        tags = [await Tag.get(id=tag_id) for tag_id in data['tags']]
        await asyncio.gather(
            movement.get_category_(),
            movement.get_wallet_(),
            movement.get_event_(),
            movement.add_tags(*tags)
        )
        return CreateExpenseMutation(movement)

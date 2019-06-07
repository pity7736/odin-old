import asyncio
import datetime

import graphene

from odin.accounting.models import Movement
from odin.accounting.schemas import MovementObjectType


class ExpenseInput(graphene.InputObjectType):
    date = graphene.Date()
    value = graphene.Int(required=True)
    note = graphene.String()
    category_id = graphene.Int(required=True)
    wallet_id = graphene.Int(required=True)
    event_id = graphene.Int()


class CreateExpenseMutation(graphene.Mutation):
    expense = graphene.Field(MovementObjectType)

    class Arguments:
        data = ExpenseInput(required=True)

    @staticmethod
    async def mutate(root, info, data):
        data['type'] = 'expense'
        data.setdefault('date', datetime.date.today())
        movement = Movement(**data)
        await movement.save()
        await asyncio.gather(
            movement.get_category(),
            movement.get_wallet(),
            movement.get_event()
        )
        return CreateExpenseMutation(movement)

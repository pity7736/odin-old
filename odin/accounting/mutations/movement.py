import asyncio

import graphene

from odin.accounting.models import Movement
from odin.accounting.schemas import MovementObjectType


class ExpenseInput(graphene.InputObjectType):
    date = graphene.Date()
    value = graphene.Int()
    note = graphene.String()
    category_id = graphene.Int()
    wallet_id = graphene.Int()


class CreateExpenseMutation(graphene.Mutation):
    expense = graphene.Field(MovementObjectType)

    class Arguments:
        data = ExpenseInput(required=True)

    @staticmethod
    async def mutate(root, info, data):
        data['type'] = 'expense'
        movement = Movement(**data)
        await movement.save()
        category, wallet = await asyncio.gather(movement.get_category(), movement.get_wallet())
        return CreateExpenseMutation(MovementObjectType(
            id=movement.id,
            type=movement.type,
            date=movement.date,
            value=movement.value,
            note=movement.note,
            category=category,
            wallet=wallet
        ))

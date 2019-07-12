import asyncio

import graphene

from odin.accounting.models import Category, Movement, Event
from odin.accounting.mutations.category import CreateCategoryMutation
from odin.accounting.mutations.movement import CreateExpenseMutation
from odin.accounting.schemas import CategoryObjectType, MovementObjectType, EventObjectType


def login_required(f):
    print('f', f)

    def qwe(root, info, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        user = info.context['request'].user
        print('user', user)
        print(user.is_authenticated)
        if user.is_authenticated is False:
            raise ValueError('login required!')
        return f(root, info, *args, **kwargs)

    return qwe


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryObjectType, id=graphene.Int(required=True))
    categories = graphene.List(CategoryObjectType)
    movement = graphene.Field(MovementObjectType, id=graphene.Int(required=True))
    expenses = graphene.List(MovementObjectType)
    event = graphene.Field(EventObjectType, id=graphene.Int(required=True))

    @staticmethod
    async def resolve_category(root, info, id):
        category = await Category.get(id=id)
        return category

    @staticmethod
    @login_required
    async def resolve_categories(root, info):
        print('context', info.context['request'].user)
        categories = await Category.all()
        result = []
        for category in categories:
            result.append(category)
        return result

    @staticmethod
    async def resolve_movement(root, info, id):
        movement = await Movement.get(id=id)
        if movement:
            await movement.get_category()
            return movement

    @staticmethod
    async def resolve_expenses(root, info):
        expenses = await Movement.all_expenses()
        result = []
        for expense in expenses:
            await asyncio.gather(expense.get_category(), expense.get_wallet())
            result.append(expense)
        return result

    @staticmethod
    async def resolve_event(root, info, id):
        return await Event.get(id=id)


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    create_expense = CreateExpenseMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

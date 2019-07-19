import asyncio

import graphene

from odin.accounting.models import Category, Movement, Event
from odin.accounting.mutations.category import CreateCategoryMutation
from odin.accounting.mutations.movement import CreateExpenseMutation
from odin.accounting.schemas import CategoryObjectType, MovementObjectType, EventObjectType
from odin.auth.decorators import login_required
from odin.auth.mutations import LoginMutation


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryObjectType, id=graphene.Int(required=True))
    categories = graphene.List(CategoryObjectType)
    movement = graphene.Field(MovementObjectType, id=graphene.Int(required=True))
    expenses = graphene.List(MovementObjectType)
    event = graphene.Field(EventObjectType, id=graphene.Int(required=True))

    @staticmethod
    @login_required
    async def resolve_category(root, info, id):
        return await Category.get(id=id)

    @staticmethod
    @login_required
    async def resolve_categories(root, info):
        categories = await Category.all()
        result = []
        for category in categories:
            result.append(category)
        return result

    @staticmethod
    @login_required
    async def resolve_movement(root, info, id):
        movement = await Movement.get(id=id)
        if movement:
            await movement.get_category_()
            return movement

    @staticmethod
    @login_required
    async def resolve_expenses(root, info):
        expenses = await Movement.all_expenses()
        result = []
        for expense in expenses:
            await asyncio.gather(expense.get_category_(), expense.get_wallet_())
            result.append(expense)
        return result

    @staticmethod
    @login_required
    async def resolve_event(root, info, id):
        return await Event.get(id=id)


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    create_expense = CreateExpenseMutation.Field()
    login = LoginMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

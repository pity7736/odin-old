import graphene

from odin.accounting.models import Category, Movement
from odin.accounting.mutations.category import CreateCategoryMutation
from odin.accounting.mutations.movement import CreateExpenseMutation
from odin.accounting.schemas import CategoryObjectType, MovementObjectType
from odin.accounting.schemas.wallet import WalletObjectType


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryObjectType, id=graphene.Int(required=True))
    categories = graphene.List(CategoryObjectType)
    movement = graphene.Field(MovementObjectType, id=graphene.Int(required=True))
    expenses = graphene.List(MovementObjectType)

    @staticmethod
    async def resolve_category(root, info, id):
        category = await Category.get(id=id)
        if category:
            return CategoryObjectType(id=category.id, name=category.name, description=category.description)

    @staticmethod
    async def resolve_categories(root, info):
        categories = await Category.all()
        result = []
        for category in categories:
            result.append(CategoryObjectType(id=category.id, name=category.name, description=category.description))
        return result

    @staticmethod
    async def resolve_movement(root, info, id):
        movement = await Movement.get(id=id)
        if movement:
            category = await movement.get_category()
            return MovementObjectType(
                id=movement.id,
                type=movement.type,
                date=movement.date,
                value=movement.value,
                note=movement.note,
                category=CategoryObjectType(id=category.id, name=category.name, description=category.description)
            )

    @staticmethod
    async def resolve_expenses(root, info):
        expenses = await Movement.all_expenses()
        result = []
        for expense in expenses:
            category = await expense.get_category()
            wallet = await expense.get_wallet()
            result.append(MovementObjectType(
                id=expense.id,
                type=expense.type,
                date=expense.date,
                value=expense.value,
                note=expense.note,
                category=CategoryObjectType(id=category.id, name=category.name, description=category.description),
                wallet=WalletObjectType(
                    id=wallet.id,
                    name=wallet.name,
                    initial_balance=wallet.initial_balance,
                    balance=wallet.balance,
                    created=wallet.created
                )
            ))
        return result


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    create_expense = CreateExpenseMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

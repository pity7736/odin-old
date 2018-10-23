import graphene

from src.accounting.models import Category, Movement
from src.accounting.mutations.category import CreateCategoryMutation
from src.accounting.schemas import CategoryObjectType, MovementObjectType


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryObjectType, id=graphene.Int(required=True))
    categories = graphene.List(CategoryObjectType)
    movement = graphene.Field(MovementObjectType, id=graphene.Int(required=True))

    async def resolve_category(self, info, id):
        category = await Category.get(id=id)
        if category:
            return CategoryObjectType(id=category.id, name=category.name, description=category.description)

    async def resolve_movement(self, info, id):
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


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

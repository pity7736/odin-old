import graphene

from odin.accounting.models import Category
from odin.accounting.schemas import CategoryObjectType


class CreateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryObjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    async def mutate(self, info, name, description):
        category = Category(name=name, description=description)
        await category.save()
        return CreateCategoryMutation(
            category=CategoryObjectType(id=category.id, name=category.name, description=category.description)
        )

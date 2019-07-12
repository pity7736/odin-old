import graphene

from odin.accounting.models import Category
from odin.accounting.schemas import CategoryObjectType
from odin.auth.decorators import login_required


class CreateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryObjectType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    @login_required
    async def mutate(self, info, name, description):
        category = Category(name=name, description=description)
        await category.save()
        return CreateCategoryMutation(
            category=CategoryObjectType(id=category.id, name=category.name, description=category.description)
        )

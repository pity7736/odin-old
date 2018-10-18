import factory

from src.accounting.models import Category


class CategoryFactory(factory.Factory):
    name = 'test name'
    description = 'test description'

    class Meta:
        model = Category

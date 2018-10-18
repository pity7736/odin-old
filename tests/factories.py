import factory

from src.accounting.models import Category


class CategoryFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test name'
    description = 'test description'

    class Meta:
        model = Category
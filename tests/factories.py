import datetime

import factory

from odin.accounting.models import Category, Movement, Tag


class CategoryFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test name'
    description = 'test description'

    class Meta:
        model = Category


class TagFactory(factory.Factory):
    name = 'test tag'

    class Meta:
        model = Tag


class MovementFactory(factory.Factory):
    type = 'expense'
    date = factory.LazyFunction(datetime.date.today)
    value = 10000
    note = 'note'

    class Meta:
        model = Movement

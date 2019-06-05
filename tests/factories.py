import datetime

import factory

from odin.accounting.models import Category, Movement, Tag, Wallet


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


class WalletFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = 'test wallet'
    initial_balance = 5_000_000
    balance = 5_000_000
    created = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = Wallet


class MovementFactory(factory.Factory):
    type = 'expense'
    date = factory.LazyFunction(datetime.date.today)
    value = 10000
    note = 'note'

    class Meta:
        model = Movement

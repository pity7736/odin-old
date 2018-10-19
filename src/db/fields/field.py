class Field:

    __slots__ = ('name',)

    def __init__(self, name=''):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return vars(instance)[self.name]

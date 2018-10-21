from src.db.fields import Field


class ForeignKeyField(Field):

    def __init__(self, to, name):
        super().__init__(name=name)
        self._to = to

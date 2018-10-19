from src.db.fields.field import Field


class MetaModel(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        # TODO: use inmmutable map lib
        fields = {}
        for attr, value in namespace.items():
            if isinstance(value, Field):
                fields[attr] = value

        model = type.__new__(mcs, name, bases, namespace)
        model._fields = fields
        return model


class Model(metaclass=MetaModel):

    def __init__(self, **kwargs):
        for key, value in self._fields.items():
            value = kwargs.get(key)
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in self._fields.keys():
                raise TypeError(f'Invalid field: {key} is not a field of {self.__class__}')
            setattr(self, key, value)

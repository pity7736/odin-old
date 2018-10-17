from src.accounting.models import Category


def test_attributes():
    category = Category(name='Test', description='description test')

    assert category.id is None
    assert category.name == 'Test'
    assert category.description == 'description test'

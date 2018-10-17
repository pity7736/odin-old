from src.accounting.models import Category


def test_attributes():
    category = Category(name='Test', description='description test')
    assert category.name == 'Test'
    assert category.description == 'description test'

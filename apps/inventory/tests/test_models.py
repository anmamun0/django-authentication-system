import pytest
from django.db import IntegrityError
from apps.users.tests.factories import UserFactory, CategoryFactory, InventoryFactory

pytestmark = pytest.mark.django_db

# ----------------------------
# Model Tests
# ---------------------------- 
def test_category_str():
    """
    Test that category obj __str__ 
    """
    category = CategoryFactory()
    assert str(category) == category.name
 
def test_inventory_str():
    """
    Test that inventory __str__ return 
    """
    inventory = InventoryFactory()
    assert str(inventory) == f"{inventory.number} {inventory.name} - {inventory.priority}"
 
def test_inventory_count_property():
    """
    Test that how many inventory added any category its counting properly
    """
    category = CategoryFactory()
    InventoryFactory(category=category)
    InventoryFactory(category=category)
    assert category.inventory_count == 2

def test_unique_category_per_user():
    """
    Test that duplicated category not create.
    """
    user = UserFactory()
    CategoryFactory(user=user, name="Laptop")

    with pytest.raises(IntegrityError):
        CategoryFactory(user=user, name="Laptop") 


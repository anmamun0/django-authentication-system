import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.inventory.models import Category, Inventory
from apps.inventory.models import User
from apps.users.tests.factories import UserFactory, CategoryFactory, InventoryFactory

# ----------------------------
# Fixtures
# ----------------------------
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def category(user):
    return CategoryFactory(user=user)

@pytest.fixture
def inventory(user, category):
    return InventoryFactory(user=user, category=category)

# ----------------------------
# CategoryView Tests
# ---------------------------- 
def test_get_categories(auth_client, category):
    """
    Test auth user get his list of category
    """
    url = reverse('inventory:category')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == category.name
 
def test_get_category_detail(auth_client, category):
    """
    Test that retrive spacific category data
    """
    url = reverse('inventory:category-detail', args=[category.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == category.name
 
def test_create_category(auth_client):
    """
    Test that create a new categroy data
    """
    url = reverse('inventory:category')
    data = {'name': 'NewCategory'}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'NewCategory'
 
def test_update_category(auth_client, category):
    """
    Test that update category data
    """
    url = reverse('inventory:category-detail', args=[category.id])
    data = {'name': 'UpdatedCategory'}
    response = auth_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == 'UpdatedCategory'
 
def test_delete_category(auth_client, category):
    """
    Test that delete category data
    """
    url = reverse('inventory:category-detail', args=[category.id])
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Category.objects.filter(id=category.id).exists()

# ----------------------------
# InventoryView Tests
# ---------------------------- 
def test_inventory_list(auth_client, inventory):
    """
    Test that get auth user his list of inventory data
    """
    url = reverse('inventory:inventory-list')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == inventory.name
 
def test_inventory_create(auth_client, category):
    "Test that get auth user create inventory data"
    url = reverse('inventory:inventory-list')
    data = {
        'name': 'NewItem',
        'category': str(category.id),
        'priority': 'High',
        'number': 5
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'NewItem'

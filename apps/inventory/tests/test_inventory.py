from apps.inventory.models import Category,Inventory
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_inventory_create(auth_client,test_user,urls_inve,category):
    """
    Test that inventory item successfully created
    Ensure that return 201 OK
    """
    response = auth_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"TestInventory","category":category.id,"priority":"Low","number":3},format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_inventory_update(auth_client,test_user,urls_inve,category):
    """
    Test that inventory item successfully updatede
    Ensure that return OK
    """
    new_category = Category.objects.create(user=test_user,name='TestInventoryUpdate')
    response = auth_client.patch(urls_inve['inventory-detail'],{"name":"TestInventoryPatch","category":new_category.id,"priority":"High","number":4},format='json')
 
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "TestInventoryPatch"
    assert response.data['priority'] == "High"
    assert str(response.data['category']) == str(new_category.id)

# Inventory data delete 
@pytest.mark.django_db
def test_inventory_delete(auth_client,test_user,urls_inve):
    """
    Test that for user can successfully delete an inventory item
    Ensures that the DELETE endpoint returns HTTP 204.
    """
    response = auth_client.delete(urls_inve['inventory-detail'])
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_inventory_category_if_delete(auth_client,urls_inve,inventory,category):
    """
    Test that any category if added in inventory item, 
    and then if that category delete then in inventory.category item return null
    """
    assert inventory.category.id == category.id
    category.delete()
    inventory.refresh_from_db()
    assert inventory.category == None

@pytest.mark.django_db
def test_priority_outer_choice(auth_client,urls_inve,inventory):
    """
    Test that inventory item update any other data that not available in priority choice list
    Ensure that return 404 Bad Reqeust
    """
    response = auth_client.patch(urls_inve['inventory-detail'],{'priority':"random"},format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_empty_name(auth_client,urls_inve,test_user,category):
    """
    Test that inventory cant create with empty name
    """
    response = auth_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"","category":category.id,"priority":"Low","number":3},format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_negative_number(auth_client,urls_inve,test_user,category):
    """
    Test that allow negative number
    Ensure that retrun 
    """
    response = auth_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"TestInventory","category":category.id,"priority":"Low","number":-3},format='json')
    assert response.status_code == status.HTTP_201_CREATED

# ------------------------------------
# Test for Anonmouse User
# ------------------------------------
@pytest.mark.django_db
def test_inventory_create_annonmous(api_client,test_user,urls_inve,category):
    """
    Test that for any anonmous user can't create inventory item
    Ensure that POST endpoint retrun UnAuthtorized
    """
    response = api_client.post(urls_inve['inventory-list'],{"user":test_user.id,"name":"TestInventory","category":category.id,"priority":"Low","number":3},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_inventory_update_annonmous(api_client,test_user,urls_inve,category):
    """
    Test that for annonmous user cant' Update (Patch,PUT) inventory item if has any item id,
    Ensure that return UnAuthorized
    """
    new_category = Category.objects.create(user=test_user,name='TestInventoryUpdate')
    response = api_client.patch(urls_inve['inventory-detail'],{"name":"TestInventoryPatch","category":new_category.id,"priority":"High","number":4},format='json')
 
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



from apps.inventory.models import Category, Inventory
from rest_framework import status
from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_category_create(auth_client,urls_cats,):
    """
    Test that category item create successfully
    Ensure that POST method work properly and  return CREATED 201
    """
    response = auth_client.post(urls_cats['category-list'],{'name':'ByCycleUnique'},format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_category_delete(auth_client,urls_cats): 
    """
    Test that category item delete successfull
    Ensure that Delete Method wrok properly and return 204 NO CONTENT
    """
    response = auth_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_category_delete_with_inventory(auth_client,test_user,urls_cats,category): 
    """
    Test that Category hav't delete if the category item already add in any Inventory items
    Ensure that Working properly and return 403 FORBIDDEN 
    """
    inventory = Inventory.objects.create(user=test_user,name='Test1',category=category,priority='High',number=3)
    response = auth_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_category_edit(auth_client,urls_cats,category):
    """
    Test that category edit successfull
    Ensure that Patch Method working properly and return OK 200
    """
    response = auth_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_200_OK

    category.refresh_from_db()
    assert  category.name == 'ByCycleEdit'

@pytest.mark.django_db
def test_category_edit_after_added_inventory(auth_client,test_user,urls_cats,category):
    """
    Test that category item hav't update/edit if this category already added any Inventory items
    Ensure that return 403 FORBIDDEN 
    """
    inventory = Inventory.objects.create(user=test_user,name='Test1',category=category,priority='High',number=3)
    response = auth_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
     
@pytest.mark.django_db
def test_duplicate_category(auth_client,urls_cats,category):
    """
    Test that can't create any duplicated category
    Ensrue that return 400
    """
    duplicate_name = category.name
    response = auth_client.post(urls_cats['category-list'],{'name':duplicate_name},format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_max_langth_category(auth_client,urls_cats,category): 
    """
    Test that can't add lengthy category name
    Ensure that return 404
    """
    lan_40 = "x"*40
    response = auth_client.post(urls_cats['category-list'],{'name':str(lan_40)},format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ------------------------------------
# Test for Anonymous User
# ------------------------------------
@pytest.mark.django_db
def test_category_view_anonymous(api_client,urls_cats,category):
    """
    Test that for anonymous user can't View Category list
    Ensure that return UN-AUTHORIZED request
    """
    response = api_client.get(urls_cats['category-list'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_create_anonymous(api_client,urls_cats,category):
    """
    Test that for anonymous user can't create any category item
    Ensure that return UN-AUTHORIZED request
    """
    response = api_client.post(urls_cats['category-list'],{'name':"Test2"},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_edit_anonymous(api_client,urls_cats,category):
    """
    Test that anonymous user can't update/edit data if has any category id
    Ensure that return UN-AUTHORIZED request
    """
    response = api_client.patch(urls_cats['category-detail'],{'name':'ByCycleEdit'},format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_category_delete_anonymous(api_client,urls_cats,category): 
    """
    Test that for anonymous user can't delete data if has any category id
    Ensrue that return UN-AUTHORIZED request
    """
    response = api_client.delete(urls_cats['category-detail'])
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
 
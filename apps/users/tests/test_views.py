# test_views.py	Response status, content, templates
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models import User
from apps.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db
# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def auth_client(api_client, user):
    user.is_email_verify = True
    user.save()
    
    api_client.force_authenticate(user=user)
    return api_client

# ----------------------------
# User self-service tests
# ---------------------------- 
def test_get_user_profile(auth_client, user):
    """
    Test that for authenticated user get his own user data
    """
    url = reverse('users:self-me')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username
 
def test_update_user_profile(auth_client, user):
    """
    Test that for authenticated user update his own data
    """
    url = reverse('users:self-me')
    data = {'first_name': 'NewName'}
    response = auth_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == 'NewName'
 
def test_delete_user(auth_client, user):
    """
    Test that for own user data delete work properly
    """
    url = reverse('users:self-me')
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.filter(id=user.id).exists() is False

# ----------------------------
# Change password tests
# ---------------------------- 
def test_change_password(auth_client, user):
    """
    Test that authenticated own user password change
    """
    url = reverse('users:change-password')
    data = {'old_password': 'password123', 'new_password': 'newPassword123'}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.check_password('newPassword123') is True
 
def test_change_password_wrong_old(auth_client, user):
    """
    Test that for authenticated own user password change if send old wrong password
    """
    url = reverse('users:change-password')
    data = {'old_password': 'wrongpassword', 'new_password': 'newpass123'}
    response = auth_client.post(url, data)
    assert response.status_code == 400

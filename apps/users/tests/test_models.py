# test_models.py - Fields, methods, __str__
import pytest
import factory
from apps.users.models import User
from apps.users.models import UserManager
from apps.users.tests.factories import UserFactory

# ----------------------------
# Model Tests
# ----------------------------
@pytest.mark.django_db
def test_create_user():
    """
    Test that for user creating successfully!
    """
    user = User.objects.create_user(email="test@example.com", password="pass1234", username="testuser")
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.check_password("pass1234") is True
    assert user.is_active is True


@pytest.mark.django_db
def test_create_superuser():
    """
    Test that for superuser creatinn successfully
    """
    admin = User.objects.create_superuser(email="admin@example.com", password="admin1234", username="adminuser")
    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.is_active is True


@pytest.mark.django_db
def test_user_str():
    """
    Test that user __str__ return successfully
    """
    user = UserFactory()
    assert str(user) == user.username

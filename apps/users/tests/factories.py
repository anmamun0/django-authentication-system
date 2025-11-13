import factory
from apps.users.models import User
from apps.verification.models import EmailOTP
from apps.inventory.models import Category, Inventory
from django.utils import timezone
import random
 
# ----------------------------
# Factories
# ----------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    phone_number = "0123456789"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")


class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory

    # foreign fields
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    name = factory.Sequence(lambda n: f"Inventory {n}")
    priority = factory.LazyFunction(lambda: random.choice(["Low", "Medium", "High"]))
    date = factory.LazyFunction(timezone.now)
    number = factory.Sequence(lambda n: n + 1)


class EmailOTPFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailOTP

    user = factory.SubFactory(UserFactory)
    otp = factory.LazyFunction(lambda: f"{random.randint(100000,999999)}")
    created_at = factory.LazyFunction(timezone.now)
    is_verified = False
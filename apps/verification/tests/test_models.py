import pytest
from django.utils import timezone
from datetime import timedelta
from apps.verification.models import EmailOTP
from apps.users.tests.factories import UserFactory, EmailOTPFactory

pytestmark = pytest.mark.django_db

def test_email_otp_creation():
    """
    Test that OTP creating successfully!
    """
    user = UserFactory()
    otp = EmailOTPFactory(user=user)
    assert otp.user == user
    assert len(otp.otp) == 6
    assert not otp.is_verified
    assert not otp.is_expired  # just created, should not be expired
 
def test_email_otp_expired():
    """
    Test that OTP expired getting wrok successfully!
    """
    user = UserFactory()
    otp = EmailOTPFactory(user=user)

    otp.created_at = timezone.now() - timedelta(minutes=11) # forceing custom time set prevous 11 mintue age
    otp.save()

    assert otp.is_expired
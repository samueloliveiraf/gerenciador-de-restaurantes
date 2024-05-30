import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email='test@example.com', password='password123')
    assert user.email == 'test@example.com'
    assert user.check_password('password123') is True
    assert user.is_active
    assert not user.is_staff
    assert not user.is_admin


@pytest.mark.django_db
def test_user_str():
    user = User.objects.create_user(email='test@example.com', password='password123')
    assert str(user) == 'test@example.com'


@pytest.mark.django_db
def test_user_short_name():
    user = User.objects.create_user(email='test@example.com', password='password123', name_complete='Test User')
    assert user.get_short_name() == 'Test User'


@pytest.mark.django_db
def test_user_permissions():
    user = User.objects.create_user(email='test@example.com', password='password123')
    assert user.has_perm('any_perm') is True
    assert user.has_module_perms('any_app') is True


@pytest.mark.django_db
def test_user_is_staff_property():
    user = User.objects.create_user(email='test@example.com', password='password123', is_admin=True)
    assert user.is_staff is True

    user.is_admin = False
    user.save()
    assert user.is_staff is False

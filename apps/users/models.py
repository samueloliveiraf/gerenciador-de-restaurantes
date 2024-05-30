from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db import models

from .managers import UserManager

import uuid


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('Endereço de email'), unique=True)
    name_complete = models.CharField(_('Nome completo'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('Data de cadastro'), auto_now_add=True)
    is_active = models.BooleanField(_('Ativo'), default=True)
    is_staff = models.BooleanField(_('Membro da equipe'), default=False)
    is_admin = models.BooleanField(_('Administrador'), default=False)
    user_type = models.CharField(_('Tipo de usuário'), max_length=20, choices=(
        ('admin', 'Admin'),
        ('manager', 'Gerente'),
        ('waiter', 'Garçom'),
        ('kitchen', 'Cozinha'),
        ('box', 'Caixa'),
    ))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.name_complete

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

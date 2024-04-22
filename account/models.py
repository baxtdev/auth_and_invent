from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class User(AbstractUser):
    phone=PhoneNumberField(
        'Телефон',
        unique=True,
        blank=True, 
        null=True
    )
    username = None
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=('last activity'),
    )
    eamil = models.EmailField(
        _("Email"), 
        max_length=254,
        unique= True,
        blank=True,
        null=True
        )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'


    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f"{self.email}-{self.phone}"

class AuthorizationCode(models.Model):
    user_profile = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"



class InviteCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user_profile = models.OneToOneField('User', on_delete=models.CASCADE, related_name='invited_code')
    users = models.ManyToManyField(
        'User',
        related_name="invited_users",
        blank=True,
        verbose_name='Приглашенные пользователи',
        null=True
    )
    def __str__(self):
        return f"{self.code}"

    @property
    def count_invited_users(self):
        return self.users.count()
    
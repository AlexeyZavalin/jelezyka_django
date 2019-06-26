from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    LEGAL_LIST = (
        ('fiz', 'Физическое'),
        ('yur', 'Юридическое')
    )
    full_name = models.CharField(max_length=128, verbose_name='Ф.И.О.')
    email = models.EmailField(max_length=128, verbose_name='Эл. почта')
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    legal = models.CharField(max_length=3, choices=LEGAL_LIST, default='fiz')
    balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Баланс')
    address_delivery = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

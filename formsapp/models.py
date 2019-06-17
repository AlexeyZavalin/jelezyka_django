from django.db import models


class Register(models.Model):
    """ Модель записи в автосервис """
    email = models.EmailField(blank=True, null=True, max_length=90, verbose_name='Эл. почта')
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.email} | {self.phone}'


class Request(models.Model):
    """ Модель заявки на запчасть """
    vin = models.CharField(blank=True, null=True, max_length=30, verbose_name='VIN')
    number_or_name = models.CharField(max_length=60, verbose_name='Номер или название')
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    email = models.EmailField(blank=True, null=True, max_length=90, verbose_name='Эл. почта')


class CallMe(models.Model):
    """ Модель заявки на обратный звонок """
    email = models.EmailField(blank=True, null=True, max_length=90, verbose_name='Эл. почта')
    phone = models.CharField(max_length=16, verbose_name='Телефон')

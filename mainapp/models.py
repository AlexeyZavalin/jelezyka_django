from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings


class Slider(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование слайдера')

    def __str__(self):
        return self.name


class Slide(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE, verbose_name='Слайдер')
    background = models.ImageField(verbose_name='Фоновое изображение')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка слайда')

    def __str__(self):
        return f'Слайд {self.id} | {self.slider}'


class MenuItem(MPTTModel):
    MAIN = 'ma'
    CATALOG = 'ca'
    APPLICATION_CHOICES = [
        (MAIN, 'mainapp'),
        (CATALOG, 'catalogapp')
    ]

    name = models.CharField(max_length=50, verbose_name='Имя пункта меню')
    app = models.CharField(max_length=2, verbose_name='Приложение', choices=APPLICATION_CHOICES, default=MAIN)
    path = models.CharField(max_length=255, verbose_name='Путь', unique=True)
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True,
                            verbose_name='Родительский пункт меню')

    class Meta:
        verbose_name = 'Пункты меню'
        verbose_name_plural = 'Пункты меню'

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

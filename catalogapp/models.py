from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименование категории')
    key = models.CharField(max_length=30, unique=True, verbose_name='Идентификатор категории')
    slug = models.SlugField(max_length=128, unique=True, default='')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='Родитесльская категория')

    def __str__(self):
        return f'{self.name} | {self.key}'

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['name']


class Brand(models.Model):
    name = models.CharField(verbose_name='Наименование бренда', max_length=50)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(verbose_name='Наименование страны', max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    slug = models.SlugField(max_length=128, unique=True, default='')
    key = models.CharField(max_length=30, verbose_name='Идентификатор товара')
    vendor = models.CharField(max_length=30, blank=True, verbose_name='Артикул товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена товара')
    old_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Старая цена товара', blank=True,
                                    null=True)
    image = models.ImageField(blank=True, null=True, upload_to="products", default='products/default.png',
                              verbose_name='Изображение товара')
    country = models.ForeignKey(Country, verbose_name='Страна производитель', blank=True, null=True,
                                on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', blank=True, null=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True, verbose_name='Статус публикации')

    def __str__(self):
        return f'{self.name} | {self.category} | {self.key}'


class Stock(models.Model):
    address = models.CharField(max_length=255, verbose_name='Адрес склада')
    key = models.PositiveSmallIntegerField(verbose_name='Идентификатор склада')
    info = models.TextField(verbose_name='Информация о складе')
    latitude = models.CharField(max_length=150, verbose_name='Широта')
    longitude = models.CharField(max_length=150, verbose_name='Долгота')

    def __str__(self):
        return f'{self.address} | {self.key}'


class StockProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Склад')
    count = models.PositiveIntegerField(verbose_name='Количество на складе')

    def __str__(self):
        return f'{self.product.name} - {self.stock.address} = ({self.count})'

    class Meta:
        unique_together = (('product', 'stock'),)

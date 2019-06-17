from django.core.management.base import BaseCommand, CommandError
from catalogapp.models import Product, Category, StockProduct, Brand, Country
from django.utils.text import slugify

import json
import os
import re

JSON_PATH = 'catalogapp/sync'


def transliterate(word):
    """:return Транслитерированное слово на кириллице"""
    ru_en_alphabet = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'ы': 'y',
        'э': 'e',
        'ю': 'u',
        'я': 'ya',
        'ь': '',
        'ъ': ''
    }
    symbols_ru = list(word.lower())
    symbols_en = []
    for symbol in symbols_ru:
        if symbol in ru_en_alphabet:
            symbols_en.append(ru_en_alphabet[symbol])
        else:
            symbols_en.append(symbol)
    return ''.join(symbols_en)


def load_from_json(file_name):
    """:return содержимое файла в формате json"""
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def create_update_category(category):
    """Обновление или создание категории"""
    load_category = Category.objects.filter(key=category['key']).first()
    if load_category is not None:
        load_category.name = category['name']
        load_category.slug = category['slug']
        if 'parent' in category:
            parent = Category.objects.filter(key=category['parent']).first()
            load_category.parent = parent
        load_category.save()
    else:
        new_category = Category(name=category['name'], key=category['key'], slug=category['slug'])
        if 'parent' in category:
            parent = Category.objects.filter(key=category['parent']).first()
            new_category.parent = parent
        new_category.save()


def create_update_product(product):
    """"Обновление или создание товара"""
    load_product = Product.objects.filter(key=product['xml_id']).first()
    price = re.sub(r',', '.', product['price'])
    slug = slugify(transliterate(product['title']))
    if load_product is not None:
        load_product.name = product['title']
        load_product.vendor = product['vendor']
        load_product.price = price
        load_product.category = Category.objects.filter(key=product['category']).first()
        load_product.save()
    else:
        new_product = Product(name=product['title'], slug=slug, key=product['xml_id'],
                              vendor=product['vendor'], price=price)
        new_product.category = Category.objects.filter(key=product['category']).first()
        new_product.save()


class Command(BaseCommand):
    """Обработка категорий и товаров"""
    help = 'Синхронизация товаров'

    def handle(self, *args, **options):
        categories = load_from_json('categories')
        for category in categories['categories']:
            create_update_category(category)

        products = load_from_json('products')
        for product in products['items']:
            create_update_product(product)

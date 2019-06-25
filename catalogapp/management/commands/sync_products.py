from django.core.management.base import BaseCommand, CommandError
from catalogapp.models import Product, Category, StockProduct, Brand, Country, Stock

from xml.etree import ElementTree as ET
import json
import os
import re

JSON_PATH = 'catalogapp/sync'


def load_from_json(file_name):
    """:return содержимое файла в формате json"""
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def load_from_xml(file_path):
    tree = ET.ElementTree(file=file_path)
    root = tree.getroot()
    categories = []
    for child in root:
        category = {}
        for step_child in child:
            if step_child.tag == 'XML_ID' and step_child.text:
                category.update({'key': step_child.text})
            if step_child.tag == 'NAME' and step_child.text:
                category.update({'name': step_child.text})
            if step_child.tag == 'PARENT_XML_ID' and step_child.text:
                category.update({'parent': step_child.text})
        categories.append(category)
    return categories


def create_update_category(category):
    """Обновление или создание категории"""
    load_category = Category.objects.filter(key=category['key']).first()
    if load_category:
        load_category.name = category['name']
        if 'parent' in category:
            parent = Category.objects.filter(key=category['parent']).first()
            load_category.parent = parent
        load_category.save()
    else:
        new_category = Category(name=category['name'], key=category['key'])
        if 'parent' in category:
            parent = Category.objects.filter(key=category['parent']).first()
            new_category.parent = parent
        new_category.save()


def create_update_product(product):
    """"Обновление или создание товара"""
    load_product = Product.objects.filter(key=product['xml_id']).first()
    price = re.sub(r',', '.', product['price'])
    if load_product:
        if product['delete_marker'] == '0':
            load_product.is_active = False
        else:
            load_product.name = product['title']
            load_product.vendor = product['vendor']
            load_product.price = price
            load_product.category = Category.objects.filter(key=product['category']).first()
        load_product.save()
        return load_product
    else:
        if 'title' in product:
            name = product['title']
        else:
            name = product['xml_id']
        new_product = Product(name=name, key=product['xml_id'], vendor=product['vendor'], price=price)
        new_product.category = Category.objects.filter(key='20281').first()
        new_product.save()
        return new_product


def create_update_stock_count(stock, product, count):
    stock_count_load = StockProduct.objects.filter(stock=stock, product=product).first()
    if stock_count_load:
        stock_count_load.product = product
        stock_count_load.stock = stock
        stock_count_load.count = count
        stock_count_load.save()
    else:
        new_stock_count = StockProduct(product=product, stock=stock, count=count)
        new_stock_count.save()


class Command(BaseCommand):
    """Обработка категорий и товаров"""
    help = 'Синхронизация товаров и категорий'

    def handle(self, *args, **options):
        # categories = load_from_xml(JSON_PATH + '/categories.xml')
        # for category in categories:
        #     create_update_category(category)

        stocks = Stock.objects.all()
        products = load_from_json('products')
        for product in products['items']:
            product_ = create_update_product(product)
            for stock in product['stock_count']:
                for stock_ in stocks:
                    if str(stock_.id) in stock:
                        create_update_stock_count(stock_, product_, stock[str(stock_.id)])

from django import template
from django.template.defaultfilters import stringfilter
import re
from catalogapp.models import Category, Product

register = template.Library()


@register.inclusion_tag('catalogapp/list.html')
def catalog_list(location='header', depth='all', parent=0):
    if depth != 'all' and parent != 0:
        category = Category.objects.filter(id=parent).first()
        categories = category.get_children()
    else:
        categories = Category.objects.all()
    for category in categories:
        products_amount = 0
        for category_item in category.get_descendants(include_self=True):
            products = Product.objects.filter(category=category_item, is_active=True).count()
            products_amount += products
        if products_amount == 0:
            categories = categories.exclude(id=category.id)
    return {'catalog': categories, 'location': location}


@register.filter(name='price_format')
@stringfilter
def price_format(value):
    parts = re.match(r'\d+\.\d{2}', value)
    if parts is not None:
        whole_part = parts.group(0)
        test = f'{float(whole_part):.2f}'
        whole_part = '{0:,.2f}'.format(float(whole_part)).replace(',', ' ')
        return whole_part
    return value


@register.filter(name='uppercase')
@stringfilter
def uppercase(value):
    return value.upper()

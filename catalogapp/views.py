from django.shortcuts import render, get_object_or_404
from catalogapp.models import Category, Product, StockProduct
from django.db.models import Max, Min

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from catalogapp.forms import AddForm

from .filters import ProductFilter


class ProductsListView(ListView):
    model = Product
    paginate_by = 15

    @staticmethod
    def get_category_products(self, category):
        """ Получаем все товары текущей и дочерних категорий """
        products = Product.objects.filter(category__slug=category.slug)
        for category_item in category.get_descendants(include_self=False):
            products |= Product.objects.filter(category=category_item)
        return products

    def get_queryset(self):
        order = 'price'
        if 'order_by' in self.request.GET:
            if self.request.GET['order_by'] == 'price_desc':
                order = '-price'
            else:
                order = 'price'
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        products = self.get_category_products(self, category).order_by(order)
        return products

    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            self.paginate_by = int(self.request.GET['paginate_by'])
        return self.paginate_by

    def get_context_data(self, **kwargs):
        """ Получаем id категории + минимальную и максимальную цену категории включая дочерние """
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        category = Category.objects.filter(slug=self.kwargs['slug']).first()
        products = self.get_category_products(self, category)
        context['cid'] = category.id
        context['max'] = products.aggregate(Max('price'))['price__max']
        context['min'] = products.aggregate(Min('price'))['price__min']
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        stocks = StockProduct.objects.filter(product=product)
        add_form = AddForm(product_id=product.id)
        context['form'] = add_form
        context['stocks'] = stocks
        return context

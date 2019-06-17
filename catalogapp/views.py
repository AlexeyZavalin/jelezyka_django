from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from catalogapp.models import Category, Product, StockProduct
from django.db.models import Max, Min

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from catalogapp.forms import AddForm


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
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        products = self.get_category_products(self, category).order_by('price')
        return products

    def get_context_data(self, **kwargs):
        """ Получаем id категории + минимальную и максимальную цену категории включая дочерние """
        context = super().get_context_data(**kwargs)
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
        add_form = AddForm(product_id=product.id)
        context['form'] = add_form
        return context

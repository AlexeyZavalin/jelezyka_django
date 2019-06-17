from django.contrib import admin
from catalogapp.models import Category, Product, Country, Brand, Stock, StockProduct
from django import forms
from ckeditor.widgets import CKEditorWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Описание товара', required=False)

    class Meta:
        model = Product
        exclude = []


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Country)
admin.site.register(Brand)
admin.site.register(Stock)
admin.site.register(StockProduct)

from django.urls import path
from catalogapp import views as catalog

app_name = 'catalogapp'

urlpatterns = [
    path('<slug:slug>/', catalog.ProductsListView.as_view(), name='category-products'),
    path('<slug:category_slug>/<slug:slug>/', catalog.ProductDetailView.as_view(), name='product-detail')
]

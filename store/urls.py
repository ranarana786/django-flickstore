from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store-page'),
    path('category/<slug:category>',views.store, name='category-link'),
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product-detail'),
    path('search', views.search, name='search')

]
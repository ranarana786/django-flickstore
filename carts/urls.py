from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart-page'),
    path('<int:product_id>/added_to_cart', views.add_to_cart, name='add-product'),
    path('<int:product_id>/<int:cart_item_id>/product_removed', views.remove_cart, name='remove-cart-product'),
    path('<int:product_id>/<int:cart_item_id>/cart_remove', views.remove_cart_item, name='remove-cart')

    
]
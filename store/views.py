from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product
from category.models import Category
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Q


# Create your views here.

def pagination(request, products, per_page):
        paginator = Paginator(products, per_page)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        return paged_product


def store(request, category='none'):

    if(category != 'none'):
        category = get_object_or_404(Category, slug=category)
        all_products = Product.objects.all().filter(category=category)
        paged_product = pagination(request, all_products, 2)
    else:
        all_products = Product.objects.all().filter(is_avaliable = True)
        paged_product = pagination(request, all_products, 6)
    
    context = {
        'all_products' : paged_product,
        'products_count' : all_products.count()
    }

    print(paged_product)

    return render(request, 'store.html', context=context)


def product_detail(request, category_slug, product_slug):
    try:
      product = Product.objects.get(category__slug=category_slug, slug=product_slug)
      is_cart_product = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()
      print(is_cart_product)
    except Exception as e:
        raise e
    context = {
        'single_product': product,
        'in_cart': is_cart_product
    }
    return render (request, 'product-detail.html', context=context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'all_products': products,
        'products_count': product_count,
    }
    return render(request, 'store.html', context)
    
    

from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, ProductProxy


def products_view(request):
    products = ProductProxy.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    context = {
        'product': product,
    }

    return render(request, 'shop/product_detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'shop/category_list.html', context)

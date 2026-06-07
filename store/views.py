from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (
    Product,
    Category,
    Manufacturer,
    Cart,
    CartItem
)


def product_list(request):

    products = Product.objects.all()

    search = request.GET.get("search")

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    category = request.GET.get("category")

    if category:
        products = products.filter(
            category_id=category
        )

    manufacturer = request.GET.get("manufacturer")

    if manufacturer:
        products = products.filter(
            manufacturer_id=manufacturer
        )

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
            "categories": categories,
            "manufacturers": manufacturers,
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product
        }
    )


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
    cart=cart,
    product=product,
    defaults={"quantity": 1}
)

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")


@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = CartItem.objects.filter(
        cart=cart
    )

    return render(
        request,
        "store/cart.html",
        {
            "cart": cart,
            "items": items,
        }
    )


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.delete()

    return redirect("cart")


@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if request.method == "POST":

        quantity = int(
            request.POST.get("quantity")
        )

        if quantity <= item.product.stock_quantity:

            item.quantity = quantity
            item.save()

    return redirect("cart")
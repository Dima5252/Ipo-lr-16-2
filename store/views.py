from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import EmailMessage
from openpyxl import Workbook
from .models import Order, OrderItem
import os
from django.conf import settings

from django.shortcuts import render
from .models import Product, Category


def index(request):

    products = Product.objects.all()[:6]

    categories = Category.objects.all()

    return render(
        request,
        'shop/index.html',
        {
            'products': products,
            'categories': categories
        }
    )

from .models import (
    Product,
    Category,
    Manufacturer,
    Cart,
    CartItem
)

from rest_framework import viewsets

from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ManufacturerSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
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

@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = CartItem.objects.filter(
        cart=cart
    )

    if request.method == "POST":

        address = request.POST.get(
            "address"
        )

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=cart.total_cost()
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        wb = Workbook()

        ws = wb.active

        ws.append(
            [
                "Товар",
                "Количество",
                "Цена"
            ]
        )

        for item in items:

            ws.append(
                [
                    item.product.name,
                    item.quantity,
                    float(item.product.price)
                ]
            )

        ws.append([])
        ws.append(
            [
                "Итого",
                float(cart.total_cost())
            ]
        )

        filename = f"receipt_{order.id}.xlsx"

        wb.save(filename)

        email = EmailMessage(
            "Ваш заказ",
            "Спасибо за покупку",
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )

        email.attach_file(filename)

        email.send()

        items.delete()

        return render(
            request,
            "store/success.html"
        )

    return render(
        request,
        "store/checkout.html"
    )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(
    r'products',
    views.ProductViewSet,
    basename='products'
)

router.register(
    r'categories',
    views.CategoryViewSet,
    basename='categories'
)

router.register(
    r'manufacturers',
    views.ManufacturerViewSet,
    basename='manufacturers'
)

router.register(
    r'carts',
    views.CartViewSet,
    basename='carts'
)

router.register(
    r'cart-items',
    views.CartItemViewSet,
    basename='cart-items'
)

router.register(
    r'orders',
    views.OrderViewSet,
    basename='orders'
)

router.register(
    r'order-items',
    views.OrderItemViewSet,
    basename='order-items'
)

urlpatterns = [
    path('', views.product_list),
    path(
        'product/<int:product_id>/',
        views.product_detail
    ),

    path(
        'api/',
        include(router.urls)
    ),
]
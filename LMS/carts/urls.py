from django.urls import path
from .views import (
    episode_cart_home,
    cart_details_api_view,
    episode_cart_update,
    episode_checkout_home,
    checkout_done
)


urlpatterns = [
    path('', episode_cart_home, name='episode-cart'),
    path('apt/cart/', cart_details_api_view, name='api-cart'),
    path('update/', episode_cart_update, name='episode-cart-update'),
    path('checkout/', episode_checkout_home, name='checkout'),
    path('checkout/success/', checkout_done, name='checkout-success'),

]

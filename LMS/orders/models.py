from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from billing.models import BillingProfile

from lms.utils import unique_order_id_generator

ORDER_STATUS_CHOOSE = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refund', 'Refund')
)


# Create your manager here.
class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=60, default='created', choices=ORDER_STATUS_CHOOSE)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        new_total = self.cart.total
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        total = self.total
        if billing_profile and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status


def pre_save_receiver_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_receiver_order_id, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Order)

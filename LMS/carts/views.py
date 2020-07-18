import decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Max
from django.template.loader import render_to_string

from accounts.forms import UserLoginForm
from instructor.models import CompanySettings
from home.models import Header
from courses.models import Courses, Episode
from billing.models import BillingProfile
from orders.models import Order
from .models import Cart, Invoice
from accounts.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_51H57IJJxOEjGpot0g90FYUAtdF0QLzCIGZhNZ85v3yuS3zE6VbBknxbPinCsSENcGjlRglOIUIVtv5ABCzeyz0co009B28MhA0")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_51H57IJJxOEjGpot0FVXHdWspLrl3QiqTVu7KoDOrKcFoyHZgeqgPfavsxCYhRals1GZfxjWe8fbxbSWctFaPQGC500pnUSlftv")


# Create your views here.
def cart_details_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    episode = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.title,
        "price": x.price} for x in cart_obj.episode.all()]

    cart_data = {
        "episode": episode,
        "subtotal": cart_obj.subtotal,
        "totla": cart_obj.total
    }
    return JsonResponse(cart_obj)


def episode_cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    template_name = 'carts/home.html'
    context = {
        "cart": cart_obj,
        "title": 'Cart',
        "header_context": Header.objects.all()[:1]
    }
    return render(request, template_name, context)


def episode_cart_update(request):
    episode_id = request.POST.get('episode')
    if episode_id is not None:
        try:
            episode_obj = Episode.objects.get(id=episode_id)
        except Episode.DoesNotExist:
            print('Episode Video is gone!? May be technical bug! We will fixed it sooner.')
            return redirect('episode-cart')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if episode_obj in cart_obj.episode.all():
            cart_obj.episode.remove(episode_obj)
            added = False
            request.session['cart_items'] = cart_obj.episode.count()
        else:
            cart_obj.episode.add(episode_obj)
            added = True
            request.session['cart_items'] = cart_obj.episode.count()
        # Ajax Handler
        if request.is_ajax():
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.episode.count()
            }
            return JsonResponse(json_data, status=200)
    return redirect('episode-cart')


def episode_checkout_home(request):
    template_name = 'carts/checkout.html'
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.episode.count() == 0:
        return redirect('episode-cart')

    login_form = UserLoginForm(request=request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    has_card = False
    if billing_profile is not None:
        order_obj, order_object_created = Order.objects.new_or_get(billing_profile, cart_obj)
        has_card = billing_profile.has_card

    if request.method == "POST":
        '''check that order is done'''
        is_prepared = order_obj.check_done()
        if is_prepared:
            billing_profile.charge(order_obj)
            order_obj.mark_paid()
            request.session['cart_item'] = 0
            del request.session['cart_id']
            if not billing_profile.user:
                billing_profile.set_cards_inactive()
            return redirect('success/')
        else:
            return redirect('checkout')

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "cart": cart_obj,
        "title": "Login",
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        "header_context": Header.objects.all()[:1]
    }
    return render(request, template_name, context)


def checkout_done(request):
    cart_id = request.session.get("cart_id", None)
    carts_data = list(Cart.objects.filter(id=cart_id).values('id', 'user_id', 'episode', 'subtotal', 'total'))
    print(carts_data)
    user = list(User.objects.filter(id=carts_data[0]['user_id']))[0]
    company_details = list(CompanySettings.objects.all().values())[0]
    max_invoice_number = Invoice.objects.aggregate(Max('invoice_number')).get('invoice_number__max')
    if max_invoice_number is None:
        max_invoice_number = 1
    max_invoice_number += 1
    total = decimal.Decimal(0)
    vat = company_details['vat_percentage']
    for item in carts_data:
        price = list(Episode.objects.filter(id=int(item['episode'])).values('price'))[0]
        total += price['price']
    grand_total = total + (vat/decimal.Decimal(100)) * total
    invoice = None
    for item in carts_data:
        episode_price = list(Episode.objects.filter(id=int(item['episode'])).values('price'))[0]
        invoice = Invoice.objects.create(
            invoice_number=max_invoice_number,
            student_id=user,
            episode_id=list(Episode.objects.filter(id=item['episode']))[0],
            subtotal=episode_price['price'],
            total=total,
            vat=company_details['vat_percentage'],
            grand_total=grand_total
        )
    Cart.objects.filter(id=cart_id).delete()
    request.session['cart_items'] = 0
    request.session.modified = True
    invoice_data = list(Invoice.objects.filter(invoice_number=invoice.invoice_number).values('episode_id__title', 'subtotal', 'invoice_number', 'issue_date'))


    # order_obj = None
    # if cart_created or cart_obj.episode.count() == 0:
    #     return redirect('episode-cart')
    subject, from_email, to = 'Purchase invoice from PakizaTVL', settings.DEFAULT_FROM_EMAIL, str(user)
    text_content = 'Click to open your invoice.'
    html_content = f"<a href='http://202.164.212.238:9020/instructor/instructor_invoice/details/{invoice.invoice_number}'>Click here to open your invoice</a>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    template_name = 'carts/checkout-done.html'
    context = {}
    return render(request, template_name, context)


def checkout_done(request):
    cart_id = request.session.get("cart_id", None)
    carts_data = list(Cart.objects.filter(id=cart_id).values('id', 'user_id', 'episode', 'subtotal', 'total'))
    print(carts_data)
    user = list(User.objects.filter(id=carts_data[0]['user_id']))[0]
    company_details = list(CompanySettings.objects.all().values())[0]
    max_invoice_number = Invoice.objects.aggregate(Max('invoice_number')).get('invoice_number__max')
    if max_invoice_number is None:
        max_invoice_number = 1
    max_invoice_number += 1
    total = decimal.Decimal(0)
    vat = company_details['vat_percentage']
    for item in carts_data:
        price = list(Episode.objects.filter(id=int(item['episode'])).values('price'))[0]
        total += price['price']
    grand_total = total + (vat/decimal.Decimal(100)) * total
    invoice = None
    for item in carts_data:
        price = list(Episode.objects.filter(id=int(item['episode'])).values('price'))[0]
        invoice = Invoice.objects.create(
            invoice_number=max_invoice_number,
            student_id=user,
            episode_id=list(Episode.objects.filter(id=item['episode']))[0],
            subtotal=price['price'],
            total=total,
            vat=company_details['vat_percentage'],
            grand_total=grand_total
        )
    Cart.objects.filter(id=cart_id).delete()
    request.session['cart_items'] = 0
    request.session.modified = True
    invoice_data = list(Invoice.objects.filter(invoice_number=invoice.invoice_number).values('episode_id__title', 'subtotal', 'invoice_number', 'issue_date'))


    # order_obj = None
    # if cart_created or cart_obj.episode.count() == 0:
    #     return redirect('episode-cart')
    subject, from_email, to = 'Purchase invoice from PakizaTVL', settings.DEFAULT_FROM_EMAIL, str(user)
    text_content = 'Click to open your invoice.'
    html_content = f"<a href='http://202.164.212.238:9020/instructor/instructor_invoice/details/{invoice.invoice_number}'>Click here to open your invoice</a>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    template_name = 'carts/checkout-done.html'
    context = {
        "title": 'Payment Success',
        "header_context": Header.objects.all()[:1],
        "invoice_data": invoice_data,
        "company_details": company_details,
        "user": user,
        "vat": vat,
        "total": total,
        "subtotal": grand_total
    }
    return render(request, template_name, context)

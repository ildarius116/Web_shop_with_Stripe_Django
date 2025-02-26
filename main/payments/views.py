import stripe
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from .models import Item, Order


def buy_item(request: HttpRequest, id: int) -> JsonResponse:
    """
    Функция обработки эндпоинта оплаты единичного товара 'buy/<int:id>/'

    :param request:
    :param id: идентификатор товара в таблице БД
    :return: json-ответ от 'stripe.com'
    """
    item = get_object_or_404(Item, id=id)
    currency = item.currency

    # Выбираем Stripe ключи в зависимости от валюты
    stripe.api_key = settings.STRIPE_KEYS[currency]['secret_key']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {'currency': currency,
                           'product_data': {'name': item.name, },
                           'unit_amount': int(item.price * 100),
                           },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'session_id': session.id})


def buy_order(request: HttpRequest, order_id: int) -> JsonResponse:
    """
    Функция обработки эндпоинта оплаты заказа товаров 'buy_order/<int:order_id>/'

    :param request:
    :param order_id: идентификатор заказа товаров в таблице БД
    :return: json-ответ от 'stripe.com'
    """
    order = get_object_or_404(Order, id=order_id)
    currency = order.items.first().currency

    # Проверяем, что все товары в заказе имеют одинаковую валюту
    if any(item.currency != currency for item in order.items.all()):
        return JsonResponse({'Ошибка': 'Все товары в заказе должны иметь одинаковую валюту'}, status=400)

    # Выбираем Stripe ключи в зависимости от валюты
    stripe.api_key = settings.STRIPE_KEYS[currency]['secret_key']

    line_items = []
    for order_item in order.orderitem_set.all():
        line_items.append({
            'price_data': {'currency': currency,
                           'product_data': {'name': order_item.item.name, },
                           'unit_amount': int(order_item.item.price * 100),
                           },
            'quantity': order_item.quantity,
        })

    # Добавляем скидку, если она есть
    discounts = []
    if order.discount:
        if order.discount.percent:
            discounts.append({
                'coupon': stripe.Coupon.create(
                    percent_off=order.discount.percent,
                    duration='once',
                ).id
            })
        elif order.discount.amount:
            discounts.append({
                'coupon': stripe.Coupon.create(
                    amount_off=int(order.discount.amount * 100),
                    currency='usd',
                    duration='once',
                ).id
            })

    # Добавляем налог, если он есть
    tax_rates = []
    if order.tax:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.name,
            percentage=order.tax.rate,
            inclusive=False,
        )
        tax_rates.append(tax_rate.id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        discounts=discounts if discounts else None,
        automatic_tax={'enabled': True if tax_rates else False, },
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'session_id': session.id})


def item_detail(request: HttpRequest, id: int) -> render:
    """
    Функция обработки эндпоинта просмотра деталей (данных) единичного товара 'item/<int:id>/'

    :param request:
    :param id: идентификатор товара в таблице БД
    :return: html страница
    """
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html',
                  {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


def order_detail(request: HttpRequest, order_id: int) -> render:
    """
    Функция обработки эндпоинта просмотра деталей (данных) заказа товаров 'order/<int:order_id>/'

    :param request:
    :param order_id: идентификатор заказа товаров в таблице БД
    :return: html страница
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html',
                  {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

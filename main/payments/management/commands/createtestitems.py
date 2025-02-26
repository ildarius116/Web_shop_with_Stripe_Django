import logging
from random import randint, random, choice
from django.core.management.base import BaseCommand

from ...models import Item, Order, OrderItem, Discount, Tax

logger = logging.Logger(__name__)


def create_order(order_no, item_no_offset, items_qty, currency):
    items_list = []
    for i in range(items_qty):
        item_no_offset += 1
        items_list.append(Item.objects.create(
            name=f'Item {item_no_offset}',
            description=f'Description {item_no_offset}',
            price=randint(10, 20),
            currency=currency,
            # currency=choice(['usd', 'eur'])
        ))
        logger.info(f"created item: {items_list[i]}")

    discount = Discount.objects.create(
        name=f'Discount {order_no + 1}',
        percent=randint(1, 20),
    )
    logger.info(f"created Discount: {discount}")

    tax = Tax.objects.create(
        name=f'Tax {order_no + 1}',
        rate=randint(5, 18),
    )
    logger.info(f"created Tax: {tax}")

    # Создаем заказ
    order = Order.objects.create(
        total_price=0,
        discount=discount,
        tax=tax,
    )
    logger.info(f"created order: {order}")

    # Добавляем товары в заказ через промежуточную модель OrderItem
    orders_list = []
    for i in range(items_qty):
        orders_list.append(OrderItem.objects.create(
            order=order,
            item=items_list[i],
            quantity=randint(1, 5),
        ))
        logger.info(f"created OrderItem: {orders_list[i]}")

    # Обновляем общую стоимость заказа
    order.total_price = sum(item.item.price * item.quantity for item in order.orderitem_set.all())
    logger.info(f"created order.total_price: {order.total_price}")
    order.save()
    return item_no_offset, order


class Command(BaseCommand):
    def handle(self, *args, **options):
        offset, order = create_order(0, 0, 2, 'usd')
        logger.info(f"created order {order} with {offset} items")
        offset, order = create_order(1, offset, 3, 'eur')
        logger.info(f"created order {order} with {offset} items")


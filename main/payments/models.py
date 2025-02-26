from django.db import models


class Item(models.Model):
    """
    Модель таблицы товаров
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd', choices=[('usd', 'USD'), ('eur', 'EUR')])

    def __str__(self):
        return self.name


class Discount(models.Model):
    """
    Модель таблицы скидок
    """
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Скидка в фиксированной сумме", null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Скидка в процентах", null=True, blank=True)

    def __str__(self):
        return self.name


class Tax(models.Model):
    """
    Модель таблицы налогов
    """
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Налоговая ставка в процентах")

    def __str__(self):
        return f"{self.name} ({self.rate}%)"


class Order(models.Model):
    """
    Модель таблицы заказов
    """
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    """
    Промежуточная модель таблицы Заказов и Товаров в них
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} (Order {self.order.id})"

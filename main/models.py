from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sessions.models import Session

# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=100, default="Гітара")

    def __str__(self):
        return self.category


class Product(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, db_index=True, verbose_name="URL")
    type = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Категорія")
    brand = models.CharField(max_length=100, verbose_name="Виробник")
    model = models.CharField(max_length=100, verbose_name="Модель")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    description = models.TextField( verbose_name="Опис")
    string_number = models.IntegerField(default=6, verbose_name="Кількість струн")
    quantity = models.IntegerField(default=1, verbose_name="Кількість товару")
    picture = models.ImageField(null=True, blank=True, upload_to="product_images/", default="product_images/1.png", verbose_name="Фото")

    def __str__(self):
        return str(self.type) + ' ' + str(self.brand)+ ' ' + ' ' + str(self.price)


class Order(models.Model):
    id = models.AutoField(primary_key=True, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(Product)
    first_name = models.CharField(max_length=100, verbose_name="Імя")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    telephone = models.CharField(max_length=100, verbose_name="Номер телефону")
    address = models.CharField(max_length=100, verbose_name="Адреса доставки")
    comment = models.TextField(max_length=100, verbose_name="Коментарій до замовлення", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.user:
            return f"Order #{self.id} by {self.user.username}"
        else:
            return f"Order #{self.id}"

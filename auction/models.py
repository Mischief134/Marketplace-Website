from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    # date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class ProductRating(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.TextField()  # use json.dumps to stringify the list of items

    def __str__(self):
        return str(self.user) + " Cart"


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.TextField()  # use json.dumps to stringify the list of items
    time_placed = models.DateTimeField()

    def __str__(self):
        return str(self.user) + " Orders"


class Inventory(models.Model):
    item = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item) + " Inventory"

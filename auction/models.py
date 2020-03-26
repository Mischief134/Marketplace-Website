from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    # date = models.DateTimeField('date published')
    # image = models.ImageField(default='default.jpg', upload_to='product_pics')

    def __str__(self):
        return self.title
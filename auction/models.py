from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
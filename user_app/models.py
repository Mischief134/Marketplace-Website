from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    shipping_address = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'

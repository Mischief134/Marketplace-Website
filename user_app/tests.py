from django.test import TestCase
from .models import Profile
# Create your tests here.

class ProfileModelTests(TestCase):

    def test_shipping_address_max_length(self):
        user = Profile(shipping_address = 100)
        max_length = user._meta.get_field('shipping_address').max_length
        self.assertEquals(max_length, 100)

    def test_imagefield(self):
        user = Profile()
        #must be default page
        self.assertIs(user.image == 'default.jpg',True)





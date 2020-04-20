from django.test import TestCase
from .models import Inventory, Product
# Create your tests here.

class InventoryModelTests(TestCase):
    def test_in_stock(self):
        product1 = Product()
        product2 = Product()
        inv1 = Inventory(item=product1, stock_count=3)
        self.assertIs(inv1.in_stock(), True)
        inv2 = Inventory(item=product2, stock_count=0)
        self.assertIs(inv2.in_stock(), False)
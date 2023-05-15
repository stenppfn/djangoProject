# from django.test import TestCase

# Create your tests here.
from faker import Faker
from customer.models import ListModel

fake = Faker()


def create_fake_product():
    product = ListModel()
    product.save()


for i in range(10):
    create_fake_product()

from django.db import models

from users.models import User


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=120)
    risk = models.CharField(max_length=120)
    url = models.CharField(max_length=120)
    # interest = models.CharField(max_length=120)
    tenure = models.CharField(max_length=120)
    def __str__(self):
        return self.name


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=120)
    # interest = models.CharField(max_length=120)
    tenure = models.CharField(max_length=120)
    risk = models.CharField(max_length=120)
    goals = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=120, unique=True)
    returnn = models.CharField(max_length=120)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Drop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    classs = models.CharField(max_length=120)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('complete', 'Complete'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    typee = models.CharField(max_length=50)
    amt = models.CharField(max_length=50)
    # amt = models.DecimalField(max_digits=10, decimal_places=2) 
    notes = models.TextField(max_length=220)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    # drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('complete', 'Complete'), ('decline', 'Decline')])

    def __str__(self):
        return self.courier_name

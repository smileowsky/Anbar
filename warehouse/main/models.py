from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime as d
from math import ceil
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta

class Brand(models.Model):
    brand_name = models.CharField(max_length=20)
    brand_pic = models.ImageField(upload_to='media/', blank=False, null=False)
    add_date = models.DateField(auto_now_add=True)

class Clients(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=15)
    add_date = models.DateField(auto_now_add=True)

class Expenses(models.Model):
    assignment = models.CharField(max_length=255)
    amount = models.FloatField(max_length=200)
    add_date = models.DateField(auto_now_add=True)

class Supplier(models.Model):
    supplier_photo = models.ImageField(upload_to='media/', blank=True, null=True)
    supplier_name = models.CharField(max_length=15)
    supplier_surname = models.CharField(max_length=15)
    supplier_email = models.EmailField(max_length=20)
    supplier_phone = models.CharField(max_length=15)
    supplier_address = models.CharField(max_length=50)
    supplier_add_d = models.DateField(auto_now=True)
    supplier_company_name = models.CharField(max_length=20)

class Products(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.CharField(max_length=15)
    product_photo = models.ImageField(upload_to='media/', blank=False, null=False)
    buy = models.FloatField(max_length=100)
    sell = models.FloatField(max_length=100)
    quantity = models.IntegerField(100)
    add_date = models.DateField(auto_now=True)

    @property

    def profit(self):
        x = (self.sell - self.buy) * self.quantity
        return round(x, 3)

class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount =models.IntegerField(100)
    add_date = models.DateField(auto_now_add=True)
    tesdiq = models.IntegerField(default = 0)
    
    @property

    def profit(self):
        x = (self.product.sell - self.product.buy) * self.amount
        return round(x, 3)
    
class Departments(models.Model):
    department_name = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)

class Positions(models.Model):
    dep_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    positions = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)

class Staff(models.Model):
    pos_id = models.ForeignKey(Positions, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='media/', blank=False, null=False)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    sallary = models.FloatField(max_length=20)
    j_start_d = models.DateField()

class Documents(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    doc_num = models.IntegerField(20)
    about = models.TextField()
    scan_photo = models.ImageField(upload_to='media/', blank=False, null=False)

class myUser(AbstractUser):
    profile_photo = models.ImageField(upload_to='media/', blank=True, null=True)
    comp_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15)

class Assignments(models.Model):
    assignment_name = models.CharField(max_length=50)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    approve = models.IntegerField(default = 0)

    @property
    def time_remaining(self):
        now = timezone.now()
        remaining_time = self.deadline - now

        if remaining_time <= timedelta():
            completed = "Finished"
            if self.task_done == 0:
                self.task_done = 2
                self.save()
        elif self.task_done == 1:
            completed = "Completed"
        else:
            days = remaining_time.days
            seconds = remaining_time.seconds
            hours = ceil(seconds / 3600)
            completed = f"{days} days, {hours} hours"

        return completed
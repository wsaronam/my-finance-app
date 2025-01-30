from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Transaction(models.Model):

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('rent', 'Rent'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('transport', 'Transport'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} - {self.category}"